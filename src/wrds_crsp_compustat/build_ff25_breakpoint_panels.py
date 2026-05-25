"""
Build two parallel 5x5 size x book-to-market portfolio panels from raw
CRSP/Compustat that differ only in the universe used to compute the size and
book-to-market breakpoints:

- NYSE breakpoints variant: quintile breakpoints are computed using only
  NYSE-listed stocks (the Fama-French canonical convention; documented in
  Fama and French 1993 and reaffirmed in Fama and French 2015).

- CRSP-wide breakpoints variant: quintile breakpoints are computed using all
  NYSE, AMEX, and NASDAQ common stocks. This convention loads the small-cap
  corner of the 5x5 grid with microcaps and is used in some studies.

Both variants share the same monthly value-weighted return aggregation and the
same Fama-French universe filters (common stock, U.S. incorporated, NYSE /
AMEX / NASDAQ, at least 1 year in Compustat, positive book equity). Only the
breakpoint reference set differs.

Output: two parquet files in FTSFR long format (unique_id, ds, y) at
DATA_DIR/wrds_crsp_compustat/.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd
from pandas.tseries.offsets import MonthEnd, YearEnd

import pull_CRSP_Compustat
from calc_Fama_French_1993 import (
    calculate_market_equity,
    subset_CRSP_to_common_stock_and_exchanges,
    use_dec_market_equity,
)
from settings import config

DATA_DIR = Path(config("DATA_DIR"))

QUINTILES = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
SIZE_LABELS = [1, 2, 3, 4, 5]
BM_LABELS = [1, 2, 3, 4, 5]


def calc_book_equity_and_years_in_compustat(comp: pd.DataFrame) -> pd.DataFrame:
    """NA-safe re-implementation of the canonical Compustat book-equity
    calculation. The shared helper in calc_Fama_French_1993.py trips over
    nullable-NA booleans on newer pandas versions; this version uses
    `.where` and explicit float coercion to avoid that.
    """
    comp = comp.copy()
    for col in ["pstkrv", "pstkl", "pstk", "txditc", "seq"]:
        if col in comp.columns:
            comp[col] = pd.to_numeric(comp[col], errors="coerce").astype(float)

    comp["ps"] = comp["pstkrv"]
    comp["ps"] = comp["ps"].where(comp["ps"].notna(), comp["pstkl"])
    comp["ps"] = comp["ps"].where(comp["ps"].notna(), comp["pstk"])
    comp["ps"] = comp["ps"].fillna(0.0)
    comp["txditc"] = comp["txditc"].fillna(0.0)

    comp["be"] = comp["seq"] + comp["txditc"] - comp["ps"]
    comp["be"] = comp["be"].where(comp["be"] > 0)

    comp = comp.sort_values(by=["gvkey", "datadate"])
    comp["count"] = comp.groupby(["gvkey"]).cumcount()
    return comp[["gvkey", "datadate", "year", "be", "count"]]


def merge_CRSP_and_Compustat(crsp_jun, comp, ccm):
    """Local copy of merge_CRSP_and_Compustat with no changes; kept here so
    this script is self-contained and easy to read alongside the two-by-three
    construction in calc_Fama_French_1993.py."""
    ccm = ccm.copy()
    ccm["linkenddt"] = ccm["linkenddt"].fillna(pd.to_datetime("today"))
    ccm1 = pd.merge(
        comp[["gvkey", "datadate", "be", "count"]], ccm, how="left", on=["gvkey"]
    )
    ccm1["yearend"] = ccm1["datadate"] + YearEnd(0)
    ccm1["jdate"] = ccm1["yearend"] + MonthEnd(6)
    ccm2 = ccm1[
        (ccm1["jdate"] >= ccm1["linkdt"]) & (ccm1["jdate"] <= ccm1["linkenddt"])
    ]
    ccm2 = ccm2[["gvkey", "permno", "datadate", "yearend", "jdate", "be", "count"]]

    ccm_jun = pd.merge(crsp_jun, ccm2, how="inner", on=["permno", "jdate"])
    ccm_jun["beme"] = ccm_jun["be"] * 1000 / ccm_jun["dec_me"]
    return ccm_jun


def assign_5x5(ccm_jun, crsp3, breakpoint_source: str):
    """Assign each stock to a 5x5 size x book-to-market portfolio at the
    annual rebalance (end of June).

    Parameters
    ----------
    breakpoint_source : {"nyse", "crsp"}
        "nyse" replicates the Fama-French canonical convention (NYSE-only
        breakpoints). "crsp" computes breakpoints over the full NYSE / AMEX
        / NASDAQ common-stock universe.
    """
    candidates = ccm_jun[
        (ccm_jun["beme"] > 0) & (ccm_jun["me"] > 0) & (ccm_jun["count"] >= 1)
    ].copy()

    if breakpoint_source == "nyse":
        breakpoint_universe = candidates[candidates["primaryexch"] == "N"]
    elif breakpoint_source == "crsp":
        breakpoint_universe = candidates
    else:
        raise ValueError(
            f"breakpoint_source must be 'nyse' or 'crsp', got {breakpoint_source!r}"
        )

    size_breaks = (
        breakpoint_universe.groupby("jdate")["me"]
        .quantile(QUINTILES[1:-1])
        .unstack()
        .rename(columns={q: f"sz_b{int(q * 100)}" for q in QUINTILES[1:-1]})
    )
    bm_breaks = (
        breakpoint_universe.groupby("jdate")["beme"]
        .quantile(QUINTILES[1:-1])
        .unstack()
        .rename(columns={q: f"bm_b{int(q * 100)}" for q in QUINTILES[1:-1]})
    )

    breaks = size_breaks.join(bm_breaks, how="inner").reset_index()
    candidates = candidates.merge(breaks, on="jdate", how="left")

    def assign_quintile(values, b20, b40, b60, b80):
        # `values`, `b*` are pandas Series of equal length.
        out = np.full(len(values), np.nan)
        v = values.values
        out[v <= b20.values] = 1
        out[(v > b20.values) & (v <= b40.values)] = 2
        out[(v > b40.values) & (v <= b60.values)] = 3
        out[(v > b60.values) & (v <= b80.values)] = 4
        out[v > b80.values] = 5
        return out

    candidates["szport"] = assign_quintile(
        candidates["me"],
        candidates["sz_b20"],
        candidates["sz_b40"],
        candidates["sz_b60"],
        candidates["sz_b80"],
    )
    candidates["bmport"] = assign_quintile(
        candidates["beme"],
        candidates["bm_b20"],
        candidates["bm_b40"],
        candidates["bm_b60"],
        candidates["bm_b80"],
    )

    candidates = candidates.dropna(subset=["szport", "bmport"])
    candidates["szport"] = candidates["szport"].astype(int)
    candidates["bmport"] = candidates["bmport"].astype(int)

    candidates["ffyear"] = candidates["jdate"].dt.year
    june = candidates[["permno", "ffyear", "szport", "bmport"]].copy()

    crsp_keep = crsp3[
        ["mthcaldt", "permno", "primaryexch", "mthret", "wt", "ffyear", "jdate"]
    ]
    merged = pd.merge(crsp_keep, june, how="inner", on=["permno", "ffyear"])
    merged = merged[(merged["wt"] > 0) & merged["mthret"].notna()]
    return merged


def value_weighted_5x5(merged: pd.DataFrame) -> pd.DataFrame:
    def wavg(group):
        w = group["wt"]
        r = group["mthret"]
        if w.sum() <= 0:
            return np.nan
        return (r * w).sum() / w.sum()

    vw = (
        merged.groupby(["jdate", "szport", "bmport"])
        .apply(wavg, include_groups=False)
        .to_frame("y")
        .reset_index()
    )
    vw["unique_id"] = (
        "sz" + vw["szport"].astype(int).astype(str)
        + "_bm" + vw["bmport"].astype(int).astype(str)
    )
    vw = vw.rename(columns={"jdate": "ds"})
    vw = vw[["unique_id", "ds", "y"]].dropna().reset_index(drop=True)
    return vw


def build_panel(breakpoint_source: str, data_dir: Path) -> pd.DataFrame:
    comp = pull_CRSP_Compustat.load_compustat(data_dir=data_dir)
    crsp = pull_CRSP_Compustat.load_CRSP_stock_ciz(data_dir=data_dir)
    ccm = pull_CRSP_Compustat.load_CRSP_Comp_Link_Table(data_dir=data_dir)

    comp = calc_book_equity_and_years_in_compustat(comp)
    crsp = subset_CRSP_to_common_stock_and_exchanges(crsp)
    crsp2 = calculate_market_equity(crsp)
    crsp3, crsp_jun = use_dec_market_equity(crsp2)
    ccm_jun = merge_CRSP_and_Compustat(crsp_jun, comp, ccm)

    merged = assign_5x5(ccm_jun, crsp3, breakpoint_source=breakpoint_source)
    panel = value_weighted_5x5(merged)
    return panel


def main():
    data_dir = DATA_DIR / "wrds_crsp_compustat"

    nyse_panel = build_panel("nyse", data_dir=data_dir)
    crsp_panel = build_panel("crsp", data_dir=data_dir)

    out_dir = data_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    nyse_path = out_dir / "ftsfr_ff25_size_bm_nyse_breaks.parquet"
    crsp_path = out_dir / "ftsfr_ff25_size_bm_crsp_breaks.parquet"
    nyse_panel.to_parquet(nyse_path)
    crsp_panel.to_parquet(crsp_path)

    print(f"Wrote {nyse_path} (shape={nyse_panel.shape})")
    print(f"Wrote {crsp_path} (shape={crsp_panel.shape})")
    print(
        f"NYSE-breaks unique_ids: {sorted(nyse_panel['unique_id'].unique())} "
        f"({nyse_panel['unique_id'].nunique()} total)"
    )
    print(
        f"CRSP-breaks unique_ids: {sorted(crsp_panel['unique_id'].unique())} "
        f"({crsp_panel['unique_id'].nunique()} total)"
    )
    print(f"Date range: {nyse_panel['ds'].min()} -> {nyse_panel['ds'].max()}")


if __name__ == "__main__":
    main()
