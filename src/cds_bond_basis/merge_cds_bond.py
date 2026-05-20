"""
Merge WRDS bond returns + RED-code mapping + Markit CDS spreads.

ISIN-based bond-to-RED merge with CDS-coverage tie-breaking, then per-(redcode,
date) cubic-spline interpolation of CDS par spreads onto each bond's
time-to-maturity.

Replaces the prior issuer_cusip-based merge so the panel can be priced with
real Z-spreads (which need coupon, nextcoup, etc. from WRDS Bond Returns).
"""

import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

from process_z_spread import year_fraction
from settings import config

DATA_DIR = Path(config("DATA_DIR")) / "cds_bond_basis"
BOND_RED_CODE_FILE_NAME = "wrds_bondret_project.parquet"
CDS_FILE_NAME = "markit_cds.parquet"
FINAL_ANALYSIS_FILE_NAME = "Final_data.parquet"
RED_CODE_FILE_NAME = "RED_and_ISIN_mapping.parquet"
RED_MERGED_FILE_NAME = "Red_Data.parquet"


def _compute_mat_days_from_zspread_convention(df: pd.DataFrame) -> pd.Series:
    """Time-to-maturity in 365-day units using the same convention as process_z_spread."""
    has_day_count = "day_count_basis" in df.columns

    def _one_row(row):
        d = row["date"]
        m = row["maturity"]
        if pd.isna(d) or pd.isna(m):
            return np.nan
        dcb = row["day_count_basis"] if has_day_count else "30/360"
        return 365.0 * year_fraction(d, m, day_count_basis=dcb)

    return df.apply(_one_row, axis=1)


def merge_red_code_into_bond_treas(bond_treas_df, red_c_df, cds_df=None):
    """
    Merge RED codes into the WRDS bondret panel using ISIN.

    When an ISIN maps to multiple RED codes, prefer the RED code with more
    Markit CDS observations (tie-broken by RED code ascending). Falls back to
    "keep first" if no CDS panel is supplied.
    """
    if "isin" not in bond_treas_df.columns:
        raise ValueError("bond_treas_df must include an 'isin' column.")
    if "isin" not in red_c_df.columns or "redcode" not in red_c_df.columns:
        raise ValueError("red_c_df must include 'isin' and 'redcode' columns.")

    bond_df = bond_treas_df.copy()
    map_df = red_c_df[["isin", "redcode"]].copy()

    bond_df["isin"] = bond_df["isin"].astype(str).str.strip().str.upper()
    map_df["isin"] = map_df["isin"].astype(str).str.strip().str.upper()
    map_df["redcode"] = map_df["redcode"].astype(str).str.strip().str.upper()

    invalid_isin = {"", "NAN", "NONE"}
    invalid_red = {"", "NAN", "NONE"}

    bond_df = bond_df[~bond_df["isin"].isin(invalid_isin)]
    map_df = map_df[
        (~map_df["isin"].isin(invalid_isin)) & (~map_df["redcode"].isin(invalid_red))
    ]

    map_df = map_df.drop_duplicates(subset=["isin", "redcode"])
    isin_multi_red = map_df.groupby("isin")["redcode"].nunique()
    multi_count = int((isin_multi_red > 1).sum())
    if multi_count > 0:
        ambiguous_isins = set(isin_multi_red[isin_multi_red > 1].index)
        if cds_df is not None and "redcode" in cds_df.columns:
            red_counts = (
                cds_df[["redcode"]]
                .copy()
                .assign(
                    redcode=lambda d: d["redcode"].astype(str).str.strip().str.upper()
                )
            )
            red_counts = red_counts[~red_counts["redcode"].isin(invalid_red)]
            red_counts = (
                red_counts.groupby("redcode")
                .size()
                .reset_index(name="cds_obs_count")
            )

            map_amb = map_df[map_df["isin"].isin(ambiguous_isins)].copy()
            map_amb = map_amb.merge(red_counts, on="redcode", how="left")
            map_amb["cds_obs_count"] = map_amb["cds_obs_count"].fillna(0)
            map_amb = map_amb.sort_values(
                ["isin", "cds_obs_count", "redcode"],
                ascending=[True, False, True],
            )
            map_amb = map_amb.drop_duplicates(subset=["isin"], keep="first")
            map_amb = map_amb[["isin", "redcode"]]

            map_unamb = map_df[~map_df["isin"].isin(ambiguous_isins)]
            map_df = pd.concat([map_unamb, map_amb], ignore_index=True)
            warnings.warn(
                f"{multi_count} ISINs map to multiple RED codes; "
                "resolved using CDS coverage count (tie-break: redcode ascending)."
            )
        else:
            map_df = map_df.drop_duplicates(subset=["isin"], keep="first")
            warnings.warn(
                f"{multi_count} ISINs map to multiple RED codes; "
                "CDS data not provided, keeping first mapping per ISIN."
            )
    else:
        map_df = map_df.drop_duplicates(subset=["isin"], keep="first")

    merged_df = bond_df.merge(map_df, on="isin", how="inner")

    if {"date", "maturity"}.issubset(merged_df.columns):
        merged_df["date"] = pd.to_datetime(merged_df["date"], errors="coerce")
        merged_df["maturity"] = pd.to_datetime(merged_df["maturity"], errors="coerce")
        merged_df["mat_days"] = _compute_mat_days_from_zspread_convention(merged_df)

    return merged_df.reset_index(drop=True)


def merge_cds_into_bonds(bond_red_df, cds_df):
    """
    Merge CDS par spreads into bond data via per-(redcode, date) cubic spline
    interpolation on tenor. Aligns each bond observation to the latest prior
    CDS quote date in the same month.
    """
    required_bond_cols = {"date", "redcode", "mat_days"}
    missing_bond = sorted(required_bond_cols.difference(bond_red_df.columns))
    if missing_bond:
        raise ValueError(f"bond_red_df is missing required columns: {missing_bond}")

    bond_df = bond_red_df.copy()
    cds_work = cds_df.copy()

    required_cds_cols = {"date", "redcode", "tenor", "parspread"}
    missing_cds = sorted(required_cds_cols.difference(cds_work.columns))
    if missing_cds:
        raise ValueError(f"cds_df is missing required columns: {missing_cds}")

    bond_df["date"] = pd.to_datetime(bond_df["date"], errors="coerce").dt.normalize()
    bond_df["redcode"] = bond_df["redcode"].astype(str).str.strip().str.upper()
    bond_df["mat_days"] = pd.to_numeric(bond_df["mat_days"], errors="coerce")
    bond_df = bond_df.dropna(subset=["date", "redcode", "mat_days"])

    cds_work["date"] = pd.to_datetime(cds_work["date"], errors="coerce").dt.normalize()
    cds_work["redcode"] = cds_work["redcode"].astype(str).str.strip().str.upper()
    cds_work["tenor"] = cds_work["tenor"].astype(str).str.strip().str.upper()
    cds_work["parspread"] = pd.to_numeric(cds_work["parspread"], errors="coerce")

    cds_work = cds_work.dropna(subset=["date", "parspread", "tenor", "redcode"])

    cds_available_dates = pd.DatetimeIndex(
        pd.to_datetime(cds_work["date"]).dropna().drop_duplicates().sort_values()
    )
    if cds_available_dates.empty:
        warnings.warn("No usable CDS dates available after input cleaning.")
        out = bond_df.iloc[0:0].copy()
        out["par_spread"] = np.nan
        return out

    def _resolve_cds_date(target_date):
        d = pd.Timestamp(target_date)
        if d in cds_available_dates:
            return d
        prior = cds_available_dates[cds_available_dates <= d]
        if len(prior) == 0:
            return pd.NaT
        candidate = prior[-1]
        if candidate.to_period("M") == d.to_period("M"):
            return candidate
        return pd.NaT

    date_map = {d: _resolve_cds_date(d) for d in bond_df["date"].dropna().unique()}
    bond_df["cds_date"] = bond_df["date"].map(date_map)
    dropped_no_cds_date = int(bond_df["cds_date"].isna().sum())
    if dropped_no_cds_date > 0:
        warnings.warn(
            f"{dropped_no_cds_date} bond rows have no prior same-month CDS date; "
            "dropping."
        )
    bond_df = bond_df.dropna(subset=["cds_date"]).copy()

    if bond_df.empty:
        warnings.warn("No bond rows remain after CDS date alignment.")
        out = bond_df.iloc[0:0].copy()
        if "cds_date" in out.columns:
            out = out.drop(columns=["cds_date"])
        out["par_spread"] = np.nan
        return out

    cds_date_set = set(bond_df["cds_date"].unique())
    cds_work = cds_work[cds_work["date"].isin(cds_date_set)].copy()

    c_df_avg = cds_work.groupby(
        cds_work.columns.difference(["parspread"]).tolist(), as_index=False
    ).agg({"parspread": "median"})

    df_unique_count = (
        c_df_avg.groupby(["redcode", "date"])["tenor"].nunique().reset_index()
    )
    df_unique_count.rename(columns={"tenor": "unique_tenor_count"}, inplace=True)
    df_unique_count = df_unique_count[df_unique_count["unique_tenor_count"] > 1]

    filtered_cds_df = c_df_avg.merge(
        df_unique_count[["redcode", "date"]], on=["redcode", "date"], how="inner"
    )

    if filtered_cds_df.empty:
        warnings.warn(
            "No (redcode, date) groups with at least two CDS tenors; "
            "returning empty CDS-bond merge output."
        )
        out = bond_df.iloc[0:0].copy()
        if "cds_date" in out.columns:
            out = out.drop(columns=["cds_date"])
        out["par_spread"] = np.nan
        return out

    tenor_to_days = {
        "1Y": 365,
        "3Y": 3 * 365,
        "5Y": 5 * 365,
        "7Y": 7 * 365,
        "10Y": 10 * 365,
    }

    filtered_cds_df["tenor_days"] = filtered_cds_df["tenor"].map(tenor_to_days)

    cubic_splines = {}
    WARN = False
    for (redcode, date), group in filtered_cds_df.groupby(["redcode", "date"]):
        x = group["tenor_days"].values
        y = group["parspread"].values
        sorted_indices = np.argsort(x)
        x_sorted, y_sorted = x[sorted_indices], y[sorted_indices]
        try:
            cubic_splines[(redcode, date)] = CubicSpline(x_sorted, y_sorted)
        except Exception:
            WARN = True

    if WARN:
        warnings.warn("Failed to fit cubic spline for some (redcode, date) pairs")

    red_set = set(filtered_cds_df["redcode"].unique())
    bond_df = bond_df[bond_df["redcode"].isin(red_set)]

    def add_par_spread_vectorized(df):
        df = df.copy()
        if df.empty:
            df["par_spread"] = np.nan
            return df

        mask = df.set_index(["redcode", "cds_date"]).index.isin(cubic_splines.keys())
        valid_rows = df.loc[mask]
        df.loc[mask, "par_spread"] = valid_rows.apply(
            lambda row: cubic_splines[(row["redcode"], row["cds_date"])](
                row["mat_days"]
            ),
            axis=1,
        )
        df["par_spread"] = df["par_spread"].fillna(np.nan)
        return df

    par_df = add_par_spread_vectorized(bond_df)
    par_df = par_df.dropna(subset=["par_spread"])
    if "cds_date" in par_df.columns:
        par_df = par_df.drop(columns=["cds_date"])

    def safe_convert(x):
        if isinstance(x, list):
            return tuple(x)
        elif isinstance(x, np.ndarray):
            return tuple(x.tolist()) if x.ndim > 0 else x.item()
        else:
            return x

    par_df = par_df.map(safe_convert)
    par_df = par_df.drop_duplicates()

    return par_df


def main():
    print("Loading data...")
    corp_bonds_data = pd.read_parquet(DATA_DIR / BOND_RED_CODE_FILE_NAME)
    red_data = pd.read_parquet(DATA_DIR / RED_CODE_FILE_NAME)
    cds_data = pd.read_parquet(DATA_DIR / CDS_FILE_NAME)

    print("Merging RED codes into bond data...")
    corp_red_data = merge_red_code_into_bond_treas(
        corp_bonds_data, red_data, cds_data
    )
    print("Interpolating CDS spreads onto bond maturities...")
    final_data = merge_cds_into_bonds(corp_red_data, cds_data)

    print("Saving processed data...")
    corp_red_path = DATA_DIR / RED_MERGED_FILE_NAME
    final_path = DATA_DIR / FINAL_ANALYSIS_FILE_NAME
    corp_red_data.to_parquet(corp_red_path)
    final_data.to_parquet(final_path)

    print(f"Saved RED-merged bond data: {corp_red_path} ({len(corp_red_data)} rows)")
    print(f"Saved final CDS-bond merged data: {final_path} ({len(final_data)} rows)")


if __name__ == "__main__":
    main()
