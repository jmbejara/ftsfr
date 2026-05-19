"""
Build two parallel value-weighted decile-portfolio panels that differ ONLY in
the credit-spread signal used to assign bonds to deciles each month:

- MMN-biased variant: sort by `cs` (lower-case, MMN-contaminated), weight by
  `bond_value`. This is what a researcher gets if they use raw TRACE
  bid-ask-averaged prices for the cross-sectional signal.
- MMN-corrected variant: sort by `CS` (upper-case, MMN-adjusted), weight by
  `BOND_VALUE`. This is the construction recommended by Dickerson, Robotti &
  Rossetti (2024).

Both variants use the same realized return column (`bond_ret`), because the
OSBAP README explicitly states that MMN-adjusted return columns are *signals*
(short-term reversal), not realized returns to use as portfolio outcomes.

Output: two parquet files in FTSFR long format (unique_id, ds, y) at
DATA_DIR/corp_bond_returns/.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import warnings

import pandas as pd
import pull_open_source_bond
from settings import config

warnings.filterwarnings("ignore", category=DeprecationWarning)

DATA_DIR = config("DATA_DIR")


def assign_deciles(df, signal_col):
    """Assign bonds to credit-spread deciles within each date."""
    def _q(group):
        group = group.copy()
        if group[signal_col].dropna().shape[0] < 10:
            group["decile"] = pd.NA
            return group
        try:
            group["decile"] = (
                pd.qcut(group[signal_col], 10, labels=False, duplicates="drop") + 1
            )
        except ValueError:
            group["decile"] = pd.NA
        return group

    return df.groupby("date", group_keys=False).apply(_q)


def value_weighted_portfolio_returns(df, value_col, ret_col):
    """Aggregate to date × decile value-weighted returns."""
    df = df.dropna(subset=["decile"])

    def _wret(x):
        w = x[value_col]
        r = x[ret_col]
        m = w.notna() & r.notna()
        if m.sum() == 0:
            return pd.NA
        return (r[m] * w[m]).sum() / w[m].sum()

    agg = (
        df.groupby(["date", "decile"])
        .apply(_wret, include_groups=False)
        .reset_index(name="y")
    )
    return agg


def to_ftsfr_long(agg, label):
    """Convert (date, decile, y) to FTSFR long format."""
    out = agg.rename(columns={"date": "ds"}).copy()
    out["unique_id"] = label + "_decile_" + out["decile"].astype(int).astype(str).str.zfill(2)
    out = out[["unique_id", "ds", "y"]].dropna()
    out.reset_index(drop=True, inplace=True)
    return out


def build_panel(bond_data, *, signal_col, value_col, ret_col, label):
    deciled = assign_deciles(bond_data, signal_col=signal_col)
    agg = value_weighted_portfolio_returns(deciled, value_col=value_col, ret_col=ret_col)
    panel = to_ftsfr_long(agg, label=label)
    return panel


def main():
    bond_data = pull_open_source_bond.load_corporate_bond_returns(
        data_dir=DATA_DIR / "corp_bond_returns"
    )

    # Both variants use the same realized return (`bond_ret`); only the signal
    # and the size weighting differ. Filter to rows with all needed inputs for
    # *both* variants so that the date coverage is identical across panels.
    needed = ["date", "cusip", "cs", "CS", "bond_value", "BOND_VALUE", "bond_ret"]
    bond_data = bond_data[needed].dropna(subset=["cs", "CS", "bond_ret"]).copy()

    biased = build_panel(
        bond_data,
        signal_col="cs",
        value_col="bond_value",
        ret_col="bond_ret",
        label="cs_mmn_biased",
    )
    corrected = build_panel(
        bond_data,
        signal_col="CS",
        value_col="BOND_VALUE",
        ret_col="bond_ret",
        label="cs_mmn_corrected",
    )

    out_dir = DATA_DIR / "corp_bond_returns"
    out_dir.mkdir(parents=True, exist_ok=True)

    biased_path = out_dir / "ftsfr_corp_bond_cs_deciles_mmn_biased.parquet"
    corrected_path = out_dir / "ftsfr_corp_bond_cs_deciles_mmn_corrected.parquet"
    biased.to_parquet(biased_path)
    corrected.to_parquet(corrected_path)

    print(f"Wrote {biased_path} (shape={biased.shape})")
    print(f"Wrote {corrected_path} (shape={corrected.shape})")
    print(f"Date range: {biased['ds'].min()} -> {biased['ds'].max()}")
    print(f"unique_ids (biased): {sorted(biased['unique_id'].unique())[:3]} ... ({biased['unique_id'].nunique()} total)")


if __name__ == "__main__":
    main()
