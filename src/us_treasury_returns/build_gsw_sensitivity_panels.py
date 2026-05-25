"""
Build two parallel Treasury bond portfolio panels that differ only in the
cleaning filters applied to the bond universe before the maturity-bucket sort:

- Permissive variant: keep all itypes 1-4 (noncallable + callable bonds and
  notes), keep on-the-run and 1st off-the-run issues. This is the panel a
  researcher gets if they pull CRSP Treasury data without applying the
  Gurkaynak, Sack, and Wright (2007) filters.

- Strict (GSW) variant: drop callable issues (itype 3, 4) and drop on-the-run
  + 1st off-the-run issues for securities issued after 1980 (Gurkaynak, Sack,
  and Wright 2007, criterion iv).

Both variants then group bonds into the same 6-month maturity buckets (0.5 to
5.0 years) and equal-weight returns within each bucket. The realized return,
date range, and aggregation are identical across panels; only the universe
filters differ.

Output: two parquet files in FTSFR long format (unique_id, ds, y) at
DATA_DIR/us_treasury_returns/.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd

from calc_treasury_bond_returns import calc_monthly_returns
from pull_CRSP_treasury import load_CRSP_treasury_consolidated
from settings import config

DATA_DIR = Path(config("DATA_DIR"))


def apply_gsw_filters(bond_data: pd.DataFrame) -> pd.DataFrame:
    """Apply the GSW (2007) universe filters.

    Drops callables (itype in {3, 4}) and drops on-the-run + 1st off-the-run
    issues (run < 2) for securities issued in 1980 or later. Runness is
    expected to already be computed; for pre-1980 issues `run` is 0 by the
    convention in calc_runness.
    """
    df = bond_data.copy()
    # Drop callables
    df = df[~df["itype"].isin([3, 4])]
    # Drop on-the-run and 1st off-the-run for post-1980 securities.
    # calc_runness sets run=0 for pre-1980 issues, so the run filter does
    # not touch them.
    df = df[~((df["caldt"] >= "1980-01-01") & (df["run"] < 2))]
    return df


def group_portfolios(bond_returns: pd.DataFrame) -> pd.DataFrame:
    """Group bonds into 6-month maturity buckets (0.5 to 5.0 years) and
    equal-weight returns within each bucket.

    Mirrors `calc_treasury_bond_returns.group_portfolios` but expects monthly
    returns indexed on `month_end` rather than daily returns.
    """
    df = bond_returns.copy()
    df["years_to_maturity_at_obs"] = df["days_to_maturity"] / 365.25

    bins = np.arange(0.0, 5.5, 0.5)
    labels = [f"{i + 1}" for i in range(len(bins) - 1)]

    df["tau_group"] = pd.cut(
        df["years_to_maturity_at_obs"], bins=bins, labels=labels, right=False
    )
    df = df.dropna(subset=["tau_group", "tdretnua"])
    df["tau_group"] = df["tau_group"].astype(int)

    grouped = (
        df.groupby(["month_end", "tau_group"])["tdretnua"].mean().reset_index()
    )
    pivoted = grouped.pivot(index="month_end", columns="tau_group", values="tdretnua")
    pivoted.columns = [f"{int(col)}" for col in pivoted.columns]
    return pivoted.reset_index().rename(columns={"month_end": "DATE"})


def to_ftsfr_long(pivoted: pd.DataFrame, label: str) -> pd.DataFrame:
    melted = pivoted.melt(id_vars=["DATE"], var_name="bucket", value_name="y")
    melted = melted.dropna(subset=["y"])
    melted["unique_id"] = f"{label}_bucket_" + melted["bucket"].astype(str).str.zfill(2)
    melted = melted.rename(columns={"DATE": "ds"})
    melted = melted[["unique_id", "ds", "y"]].reset_index(drop=True)
    return melted


def build_panel(daily_returns: pd.DataFrame, label: str) -> pd.DataFrame:
    monthly = calc_monthly_returns(daily_returns)
    pivoted = group_portfolios(monthly)
    return to_ftsfr_long(pivoted, label=label)


def main():
    # The all-itypes file is produced by the modified pull_CRSP_treasury.py.
    # It is the only file that contains callables; the noncallable-only file
    # is the existing CRSP_TFZ_with_runness.parquet.
    bond_data = load_CRSP_treasury_consolidated(
        data_dir=DATA_DIR / "us_treasury_returns",
        with_runness=True,
        include_callables=True,
    )

    # Build the two variants from the same source dataframe so date coverage
    # is identical up to the filter step.
    permissive = bond_data.copy()
    strict = apply_gsw_filters(bond_data)

    permissive_panel = build_panel(permissive, label="treas_permissive")
    strict_panel = build_panel(strict, label="treas_strict")

    out_dir = DATA_DIR / "us_treasury_returns"
    out_dir.mkdir(parents=True, exist_ok=True)

    permissive_path = out_dir / "ftsfr_treas_portfolios_permissive.parquet"
    strict_path = out_dir / "ftsfr_treas_portfolios_strict.parquet"
    permissive_panel.to_parquet(permissive_path)
    strict_panel.to_parquet(strict_path)

    print(f"Wrote {permissive_path} (shape={permissive_panel.shape})")
    print(f"Wrote {strict_path} (shape={strict_panel.shape})")
    print(
        f"Permissive unique_ids: {sorted(permissive_panel['unique_id'].unique())} "
        f"({permissive_panel['unique_id'].nunique()} total)"
    )
    print(
        f"Strict unique_ids:    {sorted(strict_panel['unique_id'].unique())} "
        f"({strict_panel['unique_id'].nunique()} total)"
    )
    print(
        f"Date range: {permissive_panel['ds'].min()} -> {permissive_panel['ds'].max()}"
    )


if __name__ == "__main__":
    main()
