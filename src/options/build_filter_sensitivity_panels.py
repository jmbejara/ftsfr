"""
Build two parallel CJS 54-portfolio panels that differ only in the
options-data cleaning level applied before portfolio construction:

- Level-1 variant: only the Constantinides-Jackwerth-Savov (2013) Level 1
  filters have been applied (identical-quote removal, identical-but-price
  rule, zero-bid removal, zero-volume removal). The IV range, moneyness
  range, implied-rate, and IV-curve outlier filters have NOT been applied.

- Level-3 variant: the full Level 1 + Level 2 + Level 3 stack has been
  applied (CJS canonical). This is the cleaning used to produce
  `ftsfr_cjs_option_returns` and `ftsfr_hkm_option_returns`.

Both variants share the same CJS portfolio-construction logic (Gaussian
kernel weighting over moneyness x maturity, BSM leverage adjustment) and the
same set of 54 (cp_flag, moneyness, maturity) target cells. Only the input
universe of option quotes differs.

Output: two parquet files in FTSFR long format (unique_id, ds, y) at
DATA_DIR/options/.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd

from settings import config
from options.build_cjs_portfolios import build_cjs_portfolios

DATA_DIR = Path(config("DATA_DIR"))

# Use the existing cached intermediate files from the canonical filter run.
# These cover 1996-01 through 2019-12 (matching the existing FTSFR options
# datasets) and are produced by combined_filters.ipynb.
DATE_RANGE = "1996-01_2019-12"
L1_PATH = DATA_DIR / "options" / f"L1_filtered_{DATE_RANGE}.parquet"
L3_PATH = DATA_DIR / "options" / f"spx_filtered_final_{DATE_RANGE}.parquet"


def main():
    print(f"Loading L1 panel from {L1_PATH}")
    l1 = pd.read_parquet(L1_PATH)
    print(f"  rows={len(l1):,}, cols={list(l1.columns)}")

    print(f"Loading L3 panel from {L3_PATH}")
    l3 = pd.read_parquet(L3_PATH)
    print(f"  rows={len(l3):,}, cols={list(l3.columns)}")

    # L1 has raw OptionMetrics IV stored as `impl_volatility`; align name so
    # downstream code can treat the two panels uniformly. (combined_filters
    # renames this column early; L1 may or may not have it renamed depending
    # on when the file was written.)
    for df in (l1, l3):
        if "IV" not in df.columns and "impl_volatility" in df.columns:
            df.rename(columns={"impl_volatility": "IV"}, inplace=True)

    print("Building L1 CJS portfolios...")
    l1_panel = build_cjs_portfolios(l1, label_prefix="cjs_l1")
    print(f"  L1 panel shape: {l1_panel.shape}")

    print("Building L3 CJS portfolios...")
    l3_panel = build_cjs_portfolios(l3, label_prefix="cjs_l3")
    print(f"  L3 panel shape: {l3_panel.shape}")

    out_dir = DATA_DIR / "options"
    out_dir.mkdir(parents=True, exist_ok=True)
    l1_out = out_dir / "ftsfr_cjs_option_returns_l1_filters.parquet"
    l3_out = out_dir / "ftsfr_cjs_option_returns_l3_filters.parquet"
    l1_panel.to_parquet(l1_out)
    l3_panel.to_parquet(l3_out)

    print(f"Wrote {l1_out}")
    print(f"Wrote {l3_out}")
    print(f"  unique_ids (L1): {l1_panel['unique_id'].nunique()} total")
    print(f"  unique_ids (L3): {l3_panel['unique_id'].nunique()} total")
    print(f"  Date range L1: {l1_panel['ds'].min()} -> {l1_panel['ds'].max()}")
    print(f"  Date range L3: {l3_panel['ds'].min()} -> {l3_panel['ds'].max()}")


if __name__ == "__main__":
    main()
