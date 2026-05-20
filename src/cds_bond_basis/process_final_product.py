"""
Final processing of the CDS-bond basis dataset.

CB_{i,t,tau} = par_spread_{i,t,tau} - z_spread_{i,t,tau}

Produces:
- bond-level processed panel
- IG / HY aggregates (mean basis by date)
- summary statistics table
- IG vs HY time-series plot (basis in bps), matching Figure A1g of
  Siriwardane, Sunderam, Wallen (2021).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from matplotlib import pyplot as plt

from settings import config

DATA_DIR = Path(config("DATA_DIR")) / "cds_bond_basis"
OUTPUT_DIR = Path(config("OUTPUT_DIR"))

ANALYSIS_PERIODS = [
    {
        "analysis_period": "replication_2010_2020",
        "period_label": "Replication (2010-01-01 to 2020-02-29)",
        "start_date": pd.Timestamp("2010-01-01"),
        "end_date": pd.Timestamp("2020-02-29"),
    },
    {
        "analysis_period": "full_period",
        "period_label": "Full available sample",
        "start_date": pd.Timestamp("1900-01-01"),
        "end_date": pd.Timestamp("2099-12-31"),
    },
]


def _rating_bucket_from_rating_class(s: pd.Series) -> pd.Series:
    """Map rating_class labels to High Yield / Investment Grade buckets."""
    out = pd.Series(index=s.index, dtype="object")
    labels = s.astype(str).str.upper()
    out.loc[labels.str.contains("HY|JUNK", na=False)] = "High Yield"
    out.loc[labels.str.contains("IG|INVESTMENT", na=False)] = "Investment Grade"
    return out


def process_cb_spread(
    df: pd.DataFrame,
    z_spread_bound_abs: float = 0.19,
    basis_clip_bps: float = 1000.0,
) -> pd.DataFrame:
    """
    Compute CDS basis spread from the merged + z-spread panel.

    Required: date, par_spread, z_spread. Optional but expected: rating_class.

    Two outlier filters are applied to remove bad bond observations:
    - rows where the Z-spread solver hit the brentq +/- bound
      (|z_spread| >= z_spread_bound_abs) are dropped, since those are
      failed fits rather than genuine spreads;
    - rows where the resulting basis magnitude exceeds basis_clip_bps
      bps are dropped (typically driven by spline extrapolation of CDS
      par spreads to bonds whose maturity sits at the edge of the
      [1Y, 10Y] CDS tenor grid).
    """
    required = {"date", "par_spread", "z_spread"}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out = df.copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out["par_spread"] = pd.to_numeric(out["par_spread"], errors="coerce")
    out["z_spread"] = pd.to_numeric(out["z_spread"], errors="coerce")

    # Drop Z-spread fits at the brentq boundary -- these are failed fits.
    out = out[out["z_spread"].abs() < z_spread_bound_abs]

    out["cds_basis_spread"] = out["par_spread"] - out["z_spread"]
    out["cds_basis_spread_bps"] = out["cds_basis_spread"] * 10000.0

    # Implied risk-free rate (kept for backward compatibility with older notebooks).
    out["rfr"] = out["cds_basis_spread"] * 100.0

    if "rating_class" in out.columns:
        out["c_rating"] = _rating_bucket_from_rating_class(out["rating_class"])
    else:
        out["c_rating"] = pd.NA

    out = out.dropna(subset=["date", "cds_basis_spread", "c_rating"])
    out = out[out["cds_basis_spread_bps"].abs() <= basis_clip_bps]
    return out.reset_index(drop=True)


def output_cb_final_products(df: pd.DataFrame, min_bonds_per_date: int = 5):
    """
    Return aggregated (one row per c_rating x date) and bond-level long panels.

    min_bonds_per_date drops (c_rating, date) cells that have fewer than this
    many bond observations. A single bond can dominate the mean and produce
    visible spikes in the rating-bucket time series, particularly for HY
    early in the sample where the universe is small.
    """
    work = df.copy()
    work = work[work["c_rating"].isin(["High Yield", "Investment Grade"])]

    agg_df = (
        work.groupby(["c_rating", "date"], as_index=False)
        .agg(
            cds_basis_spread=("cds_basis_spread", "mean"),
            cds_basis_spread_bps=("cds_basis_spread_bps", "mean"),
            rfr=("rfr", "mean"),
            n_bonds=("cds_basis_spread", "size"),
        )
        .sort_values(["date", "c_rating"])
        .reset_index(drop=True)
    )
    agg_df = agg_df[agg_df["n_bonds"] >= int(min_bonds_per_date)].reset_index(drop=True)

    id_col = "isin" if "isin" in work.columns else ("cusip" if "cusip" in work.columns else None)
    if id_col is None:
        non_agg_df = work[
            ["date", "cds_basis_spread", "cds_basis_spread_bps", "rfr", "c_rating"]
        ].copy()
    else:
        non_agg_df = work[
            [id_col, "date", "cds_basis_spread", "cds_basis_spread_bps", "rfr", "c_rating"]
        ].copy()

    return agg_df, non_agg_df


def summary_stats_table(df: pd.DataFrame) -> pd.DataFrame:
    """All / IG / HY summary stats from monthly means."""
    work = df.copy()
    work["date"] = pd.to_datetime(work["date"], errors="coerce")
    work["cds_basis_spread_bps"] = pd.to_numeric(
        work["cds_basis_spread_bps"], errors="coerce"
    )
    groups = {
        "All bonds": work,
        "Investment Grade": work[work["c_rating"] == "Investment Grade"],
        "High Yield": work[work["c_rating"] == "High Yield"],
    }

    rows = []
    for name, sub in groups.items():
        monthly = (
            sub.dropna(subset=["date", "cds_basis_spread_bps"])
            .groupby("date", as_index=False)["cds_basis_spread_bps"]
            .mean()
            .sort_values("date")
        )
        if monthly.empty:
            rows.append(
                {
                    "group": name,
                    "n_obs": 0,
                    "start_date": pd.NaT,
                    "end_date": pd.NaT,
                    "mean_bps": pd.NA,
                    "median_bps": pd.NA,
                    "std_bps": pd.NA,
                }
            )
            continue
        rows.append(
            {
                "group": name,
                "n_obs": int(len(monthly)),
                "start_date": monthly["date"].min(),
                "end_date": monthly["date"].max(),
                "mean_bps": float(monthly["cds_basis_spread_bps"].mean()),
                "median_bps": float(monthly["cds_basis_spread_bps"].median()),
                "std_bps": float(monthly["cds_basis_spread_bps"].std()),
            }
        )
    return pd.DataFrame(rows)


def _slice_period(df: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    out = df.copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    return out[
        (out["date"] >= pd.Timestamp(start_date))
        & (out["date"] <= pd.Timestamp(end_date))
    ].copy()


def output_cb_final_products_by_period(df: pd.DataFrame, periods=ANALYSIS_PERIODS):
    """Build aggregated/non-aggregated/stats outputs for each analysis period."""
    agg_parts = []
    non_agg_parts = []
    stats_parts = []

    for p in periods:
        sub = _slice_period(df, p["start_date"], p["end_date"])
        agg_df, non_agg_df = output_cb_final_products(sub)
        stats_df = summary_stats_table(sub)

        for obj in (agg_df, non_agg_df, stats_df):
            obj["analysis_period"] = p["analysis_period"]
            obj["period_label"] = p["period_label"]
            obj["period_start"] = pd.Timestamp(p["start_date"])
            obj["period_end"] = pd.Timestamp(p["end_date"])

        agg_parts.append(agg_df)
        non_agg_parts.append(non_agg_df)
        stats_parts.append(stats_df)

    agg_period_df = (
        pd.concat(agg_parts, ignore_index=True) if agg_parts else pd.DataFrame()
    )
    non_agg_period_df = (
        pd.concat(non_agg_parts, ignore_index=True)
        if non_agg_parts
        else pd.DataFrame()
    )
    stats_period_df = (
        pd.concat(stats_parts, ignore_index=True) if stats_parts else pd.DataFrame()
    )
    return agg_period_df, non_agg_period_df, stats_period_df


def generate_graph(df: pd.DataFrame, col="cds_basis_spread_bps"):
    """Plot monthly average CDS basis spread by rating bucket (bps)."""
    work = df.copy()
    work["date"] = pd.to_datetime(work["date"], errors="coerce")
    work = work.dropna(subset=["date", col, "c_rating"])
    work = work[work["c_rating"].isin(["High Yield", "Investment Grade"])]

    monthly = work.groupby(
        [pd.Grouper(key="date", freq="ME"), "c_rating"], as_index=False
    )[col].mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    for rating in ["Investment Grade", "High Yield"]:
        s = monthly[monthly["c_rating"] == rating]
        ax.plot(s["date"], s[col], label=rating, linewidth=1.2)

    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Date")
    ax.set_ylabel("CDS Basis Spread (bps)")
    ax.grid(True, linewidth=0.3, alpha=0.7)
    ax.legend()
    plt.tight_layout()
    return fig, ax


def generate_graph_by_period(df: pd.DataFrame, col="cds_basis_spread_bps"):
    """Plot CDS basis by rating for each analysis period in separate panels."""
    work = df.copy()
    work["date"] = pd.to_datetime(work["date"], errors="coerce")
    work = work.dropna(subset=["date", col, "c_rating", "analysis_period"])
    work = work[work["c_rating"].isin(["High Yield", "Investment Grade"])]

    period_order = [p["analysis_period"] for p in ANALYSIS_PERIODS]
    present_periods = [p for p in period_order if p in set(work["analysis_period"])]
    if not present_periods:
        fig, ax = plt.subplots(figsize=(12, 6))
        return fig, ax

    label_map = {p["analysis_period"]: p["period_label"] for p in ANALYSIS_PERIODS}
    fig, axes = plt.subplots(
        nrows=len(present_periods),
        ncols=1,
        figsize=(12, 5 * len(present_periods)),
        sharex=False,
    )
    if len(present_periods) == 1:
        axes = [axes]

    for ax, period in zip(axes, present_periods):
        s_period = work[work["analysis_period"] == period]
        monthly = (
            s_period.groupby(
                [pd.Grouper(key="date", freq="ME"), "c_rating"], as_index=False
            )[col]
            .mean()
            .sort_values("date")
        )
        for rating in ["Investment Grade", "High Yield"]:
            s = monthly[monthly["c_rating"] == rating]
            ax.plot(s["date"], s[col], label=rating, linewidth=1.2)
        ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax.set_title(label_map.get(period, period))
        ax.set_xlabel("Date")
        ax.set_ylabel("CDS Basis Spread (bps)")
        ax.grid(True, linewidth=0.3, alpha=0.7)
        ax.legend()

    plt.tight_layout()
    return fig, axes


def main():
    in_path = DATA_DIR / "final_data_with_z_spread.parquet"
    processed_path = DATA_DIR / "cds_basis_processed.parquet"
    agg_path = DATA_DIR / "cds_basis_aggregated.parquet"
    non_agg_path = DATA_DIR / "cds_basis_non_aggregated.parquet"
    stats_path = DATA_DIR / "cds_basis_summary_stats.csv"
    fig_path = OUTPUT_DIR / "cds_basis_by_rating.png"

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading {in_path} ...")
    df = pd.read_parquet(in_path)
    df_proc = process_cb_spread(df)

    agg_df, non_agg_df, stats_df = output_cb_final_products_by_period(df_proc)

    df_proc.to_parquet(processed_path)
    agg_df.to_parquet(agg_path)
    non_agg_df.to_parquet(non_agg_path)
    stats_df.to_csv(stats_path, index=False)

    fig, _ = generate_graph_by_period(agg_df, col="cds_basis_spread_bps")
    fig.savefig(fig_path, dpi=160)
    plt.close(fig)

    print(f"Saved processed rows: {len(df_proc)} -> {processed_path}")
    print(f"Saved aggregated rows: {len(agg_df)} -> {agg_path}")
    print(f"Saved non-aggregated rows: {len(non_agg_df)} -> {non_agg_path}")
    print(f"Saved summary stats -> {stats_path}")
    print(f"Saved chart -> {fig_path}")


if __name__ == "__main__":
    main()
