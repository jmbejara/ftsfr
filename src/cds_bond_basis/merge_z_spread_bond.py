"""
Add Z-spread estimates to the merged CDS-bond panel.

Runs after merge_cds_bond.py; preserves the existing row structure and
appends Z-spread diagnostics.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd

from process_z_spread import calculate_z_spread, get_nss_params_for_date
from settings import config

DATA_DIR = Path(config("DATA_DIR")) / "cds_bond_basis"

INPUT_FILE_NAME = "Final_data.parquet"
OUTPUT_FILE_NAME = "final_data_with_z_spread.parquet"


def _safe_coupon_frequency(x):
    """Convert ncoups-like values to an integer frequency, defaulting to 2."""
    if pd.isna(x):
        return 2
    try:
        val = int(round(float(x)))
    except Exception:
        return 2
    return val if val > 0 else 2


def add_z_spread_columns(df: pd.DataFrame, principal: float = 100.0) -> pd.DataFrame:
    """
    Add Z-spread columns to bond rows.

    Required input columns: date, maturity, coupon, price_eom.
    Optional inputs used when present: day_count_basis, nextcoup, ncoups, coupacc.
    """
    required_cols = ["date", "maturity", "coupon", "price_eom"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Input dataframe missing required columns: {missing}")

    out = df.copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out["maturity"] = pd.to_datetime(out["maturity"], errors="coerce")
    if "nextcoup" in out.columns:
        out["nextcoup"] = pd.to_datetime(out["nextcoup"], errors="coerce")

    out = out.dropna(subset=["date", "maturity", "coupon", "price_eom"]).copy()

    nss_cache: dict[pd.Timestamp, np.ndarray] = {}

    def _row_zspread(row):
        qd = pd.Timestamp(row["date"])
        if qd not in nss_cache:
            nss_cache[qd] = get_nss_params_for_date(qd)

        coupon_frequency = (
            _safe_coupon_frequency(row["ncoups"]) if "ncoups" in row else 2
        )
        ai = row["coupacc"] if "coupacc" in row else None
        dcb = row["day_count_basis"] if "day_count_basis" in row else "30/360"
        ncd = row["nextcoup"] if "nextcoup" in row else None

        z_out = calculate_z_spread(
            quote_date=qd,
            maturity_date=row["maturity"],
            coupon_rate=row["coupon"],
            observed_price=row["price_eom"],
            nss_params=nss_cache[qd],
            day_count_basis=dcb,
            next_coupon_date=ncd,
            principal=principal,
            coupon_frequency=coupon_frequency,
            coupon_is_percent=True,
            price_is_clean=True,
            accrued_interest=ai,
        )
        return pd.Series(
            {
                "z_spread": z_out.get("z_spread", np.nan),
                "z_spread_bps": z_out.get("z_spread_bps", np.nan),
                "z_model_price": z_out.get("model_price", np.nan),
                "z_status": z_out.get("status", ""),
            }
        )

    z_cols = out.apply(_row_zspread, axis=1)
    out = pd.concat([out, z_cols], axis=1)
    return out


def main():
    print("Loading merged CDS-bond data...")
    in_path = DATA_DIR / INPUT_FILE_NAME
    out_path = DATA_DIR / OUTPUT_FILE_NAME
    df = pd.read_parquet(in_path)

    print(f"Computing Z-spreads for {len(df)} rows...")
    df_out = add_z_spread_columns(df)

    print("Saving output...")
    df_out.to_parquet(out_path)
    print(f"Saved: {out_path} ({len(df_out)} rows)")


if __name__ == "__main__":
    main()
