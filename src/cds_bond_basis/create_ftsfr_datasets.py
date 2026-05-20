"""
Build the (unique_id, ds, y) panels consumed by the forecasting pipeline.

Reads cds_basis_aggregated.parquet (rating-bucket monthly mean basis) and
cds_basis_non_aggregated.parquet (bond-level basis) and stacks them into the
ftsfr long format expected downstream.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd

from settings import config

DATA_DIR = Path(config("DATA_DIR")) / "cds_bond_basis"


def _stack_to_long(df: pd.DataFrame, id_col: str, value_col: str) -> pd.DataFrame:
    """Reshape a (id, date, value) frame into the ftsfr (unique_id, ds, y) panel."""
    out = df[[id_col, "date", value_col]].copy()
    out = out.dropna(subset=[id_col, "date", value_col])
    out["unique_id"] = out[id_col].astype(str)
    out = out.rename(columns={"date": "ds", value_col: "y"})
    out = out[["unique_id", "ds", "y"]]
    out = out.drop_duplicates(subset=["unique_id", "ds"], keep="last")
    return out.reset_index(drop=True)


def main():
    agg_path = DATA_DIR / "cds_basis_aggregated.parquet"
    non_agg_path = DATA_DIR / "cds_basis_non_aggregated.parquet"

    agg_df = pd.read_parquet(agg_path)
    non_agg_df = pd.read_parquet(non_agg_path)

    # Use only the full-sample period for the ftsfr datasets to avoid duplicate
    # (unique_id, ds) pairs across analysis_period slices.
    if "analysis_period" in agg_df.columns:
        agg_df = agg_df[agg_df["analysis_period"] == "full_period"].copy()
    if "analysis_period" in non_agg_df.columns:
        non_agg_df = non_agg_df[
            non_agg_df["analysis_period"] == "full_period"
        ].copy()

    # Rating-bucket aggregate: one series per c_rating, CDS basis in bps.
    df_agg_long = _stack_to_long(
        agg_df.assign(unique_label=agg_df["c_rating"].astype(str)),
        id_col="unique_label",
        value_col="cds_basis_spread_bps",
    )
    df_agg_long.to_parquet(DATA_DIR / "ftsfr_CDS_bond_basis_aggregated.parquet")
    print(
        "Saved: ftsfr_CDS_bond_basis_aggregated.parquet "
        f"({len(df_agg_long)} rows, {df_agg_long['unique_id'].nunique()} series)"
    )

    # Bond-level: one series per ISIN (preferred) or cusip, CDS basis in bps.
    if "isin" in non_agg_df.columns:
        id_col = "isin"
    elif "cusip" in non_agg_df.columns:
        id_col = "cusip"
    else:
        raise ValueError(
            "non-aggregated panel must contain 'isin' or 'cusip' for unique_id."
        )

    df_nonagg_long = _stack_to_long(
        non_agg_df,
        id_col=id_col,
        value_col="cds_basis_spread_bps",
    )
    df_nonagg_long.to_parquet(
        DATA_DIR / "ftsfr_CDS_bond_basis_non_aggregated.parquet"
    )
    print(
        "Saved: ftsfr_CDS_bond_basis_non_aggregated.parquet "
        f"({len(df_nonagg_long)} rows, {df_nonagg_long['unique_id'].nunique()} series)"
    )


if __name__ == "__main__":
    main()
