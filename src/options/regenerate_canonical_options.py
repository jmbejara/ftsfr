"""
Regenerate the canonical CJS-54 and HKM-18 monthly option-portfolio
intermediates (`cjs_portfolio_returns_*.parquet`, `hkm_portfolio_returns_*.parquet`)
after the contract-lag bug fix in portfolios.ipynb cell 12.

This script does NOT duplicate the notebook's construction logic: it loads and
exec's the notebook's own function-definition cells (Black-Scholes elasticity,
kernel weights, and the now-fixed `compute_cjs_return_leverage_investment`) so
the regenerated data is byte-for-byte what re-running the fixed notebook would
produce -- but pinned to the 1996-01..2019-12 window that the downstream
`create_ftsfr_datasets.py` consumes (the notebook's interactive END_DATE_02 is
2024-12).

Run after editing portfolios.ipynb; then run create_ftsfr_datasets.py.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).parent.parent))
from settings import config  # noqa: E402

DATA_DIR = Path(config("DATA_DIR"))
OPT_DIR = DATA_DIR / "options"
DATE_RANGE = "1996-01_2019-12"
NB_PATH = Path(__file__).parent / "portfolios.ipynb"

# --- Pull the notebook's (now-fixed) function cells in as live functions -----
_nb = json.loads(NB_PATH.read_text())
_g = {"np": np, "pd": pd, "norm": norm}
for _i in (9, 10, 11, 12):  # bs_elasticity/kernel/calc_*, read_option_data, compute_cjs
    exec("".join(_nb["cells"][_i]["source"]), _g)

read_option_data = _g["read_option_data"]
calc_option_delta_elasticity = _g["calc_option_delta_elasticity"]
calc_kernel_weights = _g["calc_kernel_weights"]
compute_cjs_return_leverage_investment = _g["compute_cjs_return_leverage_investment"]


def main():
    # --- notebook cell 15: read filtered data, moneyness_id from bin -----
    src = OPT_DIR / f"spx_filtered_final_{DATE_RANGE}.parquet"
    print(f"Reading {src}")
    spx = read_option_data(src).reset_index()
    spx["moneyness_id"] = spx["moneyness_bin"].apply(
        lambda x: x.right if pd.notnull(x) else np.nan
    )
    spx = spx.dropna(subset=["moneyness_id"])

    # --- cell 19: maturity_id + ftfsa_id -----
    mat = pd.concat(
        (
            abs(spx["days_to_maturity"].dt.days - 30),
            abs(spx["days_to_maturity"].dt.days - 60),
            abs(spx["days_to_maturity"].dt.days - 90),
        ),
        axis=1,
    )
    mat.columns = [30, 60, 90]
    spx["maturity_id"] = mat.idxmin(axis=1)
    spx["ftfsa_id"] = (
        spx["cp_flag"]
        + "_"
        + (spx["moneyness_id"] * 1000).apply(
            lambda x: str(int(x)) if pd.notnull(x) and x == int(x) else str(x)
        )
        + "_"
        + spx["maturity_id"].astype(str)
    )
    spx = spx.set_index(["ftfsa_id", "date"])

    # --- cell 23/26: elasticity + kernel weights (NO early floor) -----
    # The 1% floor is applied inside compute_cjs_return_leverage_investment on
    # the formation-date (lagged) weights, together with renormalization, so
    # basket selection and weighting are both as of t-1 (no look-ahead).
    spx_mod = calc_option_delta_elasticity(spx)
    print("Computing kernel weights (per-cell loop)...")
    spx_mod = calc_kernel_weights(spx_mod)
    spx_mod = spx_mod.reset_index(drop=True)

    # --- cell 31/34: daily -> monthly CJS-54 -----
    port = compute_cjs_return_leverage_investment(spx_mod)
    port = port.set_index(["date", "ftfsa_id"]).pivot_table(
        index="date", columns="ftfsa_id", values="portfolio_return"
    )
    cjs = port.resample("ME").apply(lambda x: (1 + x).prod() - 1)
    cjs = cjs.reset_index().melt(id_vars="date", var_name="ftfsa_id", value_name="return")
    cjs["ftfsa_id"] = "cjs_" + cjs["ftfsa_id"]
    cjs = cjs[["ftfsa_id", "date", "return"]].set_index(["ftfsa_id", "date"])
    cjs_out = OPT_DIR / f"cjs_portfolio_returns_{DATE_RANGE}.parquet"
    cjs.to_parquet(cjs_out, index=True)
    print(f"Wrote {cjs_out}  ({cjs.index.get_level_values(0).nunique()} portfolios)")

    # --- cell 36: HKM-18 (average CJS-54 over maturity) -----
    hkm = cjs.copy().reset_index()
    hkm = hkm.assign(
        type=hkm["ftfsa_id"].apply(lambda x: x.split("_")[1]),
        moneyness_id=hkm["ftfsa_id"].apply(lambda x: x.split("_")[2]),
        maturity_id=hkm["ftfsa_id"].apply(lambda x: x.split("_")[3]),
    ).drop(columns=["ftfsa_id"])
    hkm = hkm.set_index(["date", "type", "moneyness_id", "maturity_id"])
    hkm = hkm.groupby(["date", "type", "moneyness_id"]).mean()
    hkm["ftfsa_id"] = (
        "hkm_"
        + hkm.index.get_level_values("type")
        + "_"
        + hkm.index.get_level_values("moneyness_id")
    )
    hkm = (
        hkm.reset_index()
        .drop(columns=["type", "moneyness_id"])
        .set_index(["ftfsa_id", "date"])
        .sort_index()
    )
    hkm_out = OPT_DIR / f"hkm_portfolio_returns_{DATE_RANGE}.parquet"
    hkm.to_parquet(hkm_out, index=True)
    print(f"Wrote {hkm_out}  ({hkm.index.get_level_values(0).nunique()} portfolios)")

    # --- quick sanity print -----
    print(
        f"CJS return: mean={cjs['return'].mean():.4f} "
        f"max={cjs['return'].max():.4f} min={cjs['return'].min():.4f}"
    )
    print(
        f"HKM return: mean={hkm['return'].mean():.4f} "
        f"max={hkm['return'].max():.4f} min={hkm['return'].min():.4f}"
    )


if __name__ == "__main__":
    main()
