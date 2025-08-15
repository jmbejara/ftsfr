"""
pull_bbg_basis_treas_sf.py

Pull USD OIS term structure and Treasury futures inputs from Bloomberg via xbbg,
and write standardized parquet files used downstream by `calc_basis_treas_sf.py`.

Outputs (saved under DATA_DIR/basis_treas_sf):
- ois.parquet: Date + OIS tenors (1W, 1M, 3M, 6M, 1Y)
- treasury_df.parquet: Date + per-tenor columns for near (1) and deferred (2)
  contracts: Implied_Repo_v_<tenor>, Vol_v_<tenor>, Contract_v_<tenor>, Price_v_<tenor>
- last_day.parquet: Mapping of (Mat_Year, Mat_Month) -> Mat_Day (last calendar day)

Notes
-----
- No printing to stdout per project style guide.
- Replaces prior reliance on a manual Excel file.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd
from xbbg import blp
import warnings

from settings import config


# Configuration via settings.py
DATA_DIR: Path = config("DATA_DIR")
START_DATE: str = config("START_DATE", default="2004-01-01")
END_DATE: str = config("END_DATE", default=str(date.today()))
MIN_NON_NULL_RATIO: float = 0.5


def ois_tickers() -> List[str]:
    """Bloomberg tickers for USD OIS curve used downstream."""
    return [
        "USSO1Z CMPN Curncy",  # 1W
        "USSOA CMPN Curncy",  # 1M
        "USSOB CMPN Curncy",  # 2M
        "USSOC CMPN Curncy",  # 3M
        "USSOF CMPN Curncy",  # 6M
        "USSO1 CMPN Curncy",  # 1Y
    ]


def pull_ois_history(
    start_date: str = START_DATE, end_date: str = END_DATE
) -> pd.DataFrame:
    """Fetch historical USD OIS levels (PX_LAST) from Bloomberg via xbbg.

    Returns Date + ticker columns. Consumers rename to compact labels later.
    """
    tickers = ois_tickers()
    df = blp.bdh(
        tickers=tickers, flds=["PX_LAST"], start_date=start_date, end_date=end_date
    )

    if isinstance(df.columns, pd.MultiIndex) and df.columns.nlevels == 2:
        df.columns = df.columns.droplevel(level=1)

    df = df.reset_index().rename(columns={"index": "Date", "date": "Date"})
    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
    df = df[["Date", *tickers]]

    # Coverage checks per ticker series
    total_rows = len(df)
    for tkr in tickers:
        if tkr in df.columns:
            non_null_ratio = (df[tkr].notna().sum() / total_rows) if total_rows > 0 else 0.0
            if non_null_ratio < MIN_NON_NULL_RATIO:
                warnings.warn(
                    f"Low data coverage for {tkr} [PX_LAST] from {start_date} to {end_date}: "
                    f"{non_null_ratio:.1%} non-null",
                    category=UserWarning,
                )
    return df


def _first_available_field(
    ticker: str, candidates: Iterable[str], start_date: str, end_date: str
) -> Optional[str]:
    """Return the first Bloomberg field that yields data for the given ticker."""
    for fld in candidates:
        try:
            df = blp.bdh(
                tickers=[ticker], flds=[fld], start_date=start_date, end_date=end_date
            )
            if df is None or df.empty:
                continue
            series = (
                df.droplevel(1, axis=1) if isinstance(df.columns, pd.MultiIndex) else df
            )
            if series.iloc[:, 0].notna().any():
                return fld
        except Exception:
            continue
    return None


def futures_ticker_map() -> Dict[int, Tuple[str, str]]:
    """Map tenor (years) to (near, deferred) generic Bloomberg futures tickers."""
    mapping: Dict[int, Tuple[str, str]] = {
        2: ("TU1 Comdty", "TU2 Comdty"),
        5: ("FV1 Comdty", "FV2 Comdty"),
        10: ("TY1 Comdty", "TY2 Comdty"),
        30: ("US1 Comdty", "US2 Comdty"),
        # Optional proxy for 20Y: Ultra 10y (TN). Keep guarded; may be sparse.
        20: ("TN1 Comdty", "TN2 Comdty"),
    }
    return mapping


def _quarter_contract_label(dt: pd.Timestamp, offset_quarters: int = 0) -> str:
    """Return a contract label like 'DEC 21' for the given date plus offset."""
    q_months = [3, 6, 9, 12]
    y, m = dt.year, dt.month
    next_month = next((qm for qm in q_months if qm > m), None)
    if next_month is None:
        next_month = 3
        y += 1
    total_quarters = q_months.index(next_month) + offset_quarters
    y += total_quarters // 4
    m_idx = total_quarters % 4
    month = q_months[m_idx]
    month_abbr = {3: "MAR", 6: "JUN", 9: "SEP", 12: "DEC"}[month]
    yy = y % 100
    return f"{month_abbr} {yy:02d}"


def pull_futures_history(
    start_date: str = START_DATE, end_date: str = END_DATE
) -> pd.DataFrame:
    """Fetch Treasury futures inputs needed downstream.

    For each tenor and for near (1) and deferred (2) generic contracts, pull:
    - Price (PX_LAST)
    - Volume (VOLUME)
    - Implied Repo (first available among common field names)
    """
    tenor_to_tickers = futures_ticker_map()

    sample_ticker = next(iter(tenor_to_tickers.values()))[0]
    implied_repo_field = _first_available_field(
        sample_ticker,
        candidates=["IMPL_REPO", "IMP_REPO", "IMPLIED_REPO", "FUT_IMP_REPO", "IRR"],
        start_date=start_date,
        end_date=end_date,
    )

    frames: List[pd.DataFrame] = []
    for tenor, (near_tkr, def_tkr) in tenor_to_tickers.items():
        # Price
        px = blp.bdh(
            tickers=[near_tkr, def_tkr],
            flds=["PX_LAST"],
            start_date=start_date,
            end_date=end_date,
        )
        if isinstance(px.columns, pd.MultiIndex):
            px = px.droplevel(1, axis=1)
        # Coverage checks for Price series (by ticker)
        if isinstance(px, pd.DataFrame) and not px.empty:
            total_rows_px = len(px)
        else:
            total_rows_px = 0
        for tkr in [near_tkr, def_tkr]:
            series_non_null_ratio = (
                (px[tkr].notna().sum() / total_rows_px) if (total_rows_px > 0 and tkr in px.columns) else 0.0
            )
            if series_non_null_ratio < MIN_NON_NULL_RATIO:
                warnings.warn(
                    f"Low data coverage for {tkr} [PX_LAST] from {start_date} to {end_date}: "
                    f"{series_non_null_ratio:.1%} non-null",
                    category=UserWarning,
                )
        px = px.reset_index().rename(columns={"index": "Date", "date": "Date"})
        px.columns = ["Date", f"Price_1_{tenor}", f"Price_2_{tenor}"]

        # Volume
        vol = blp.bdh(
            tickers=[near_tkr, def_tkr],
            flds=["VOLUME"],
            start_date=start_date,
            end_date=end_date,
        )
        if isinstance(vol.columns, pd.MultiIndex):
            vol = vol.droplevel(1, axis=1)
        # Coverage checks for Volume series (by ticker)
        if isinstance(vol, pd.DataFrame) and not vol.empty:
            total_rows_vol = len(vol)
        else:
            total_rows_vol = 0
        for tkr in [near_tkr, def_tkr]:
            series_non_null_ratio = (
                (vol[tkr].notna().sum() / total_rows_vol) if (total_rows_vol > 0 and tkr in vol.columns) else 0.0
            )
            if series_non_null_ratio < MIN_NON_NULL_RATIO:
                warnings.warn(
                    f"Low data coverage for {tkr} [VOLUME] from {start_date} to {end_date}: "
                    f"{series_non_null_ratio:.1%} non-null",
                    category=UserWarning,
                )
        vol = vol.reset_index().rename(columns={"index": "Date", "date": "Date"})
        vol.columns = ["Date", f"Vol_1_{tenor}", f"Vol_2_{tenor}"]

        # Implied Repo (optional)
        if implied_repo_field is not None:
            irr = blp.bdh(
                tickers=[near_tkr, def_tkr],
                flds=[implied_repo_field],
                start_date=start_date,
                end_date=end_date,
            )
            if isinstance(irr.columns, pd.MultiIndex):
                irr = irr.droplevel(1, axis=1)
            # Coverage checks for Implied Repo series (by ticker)
            if isinstance(irr, pd.DataFrame) and not irr.empty:
                total_rows_irr = len(irr)
            else:
                total_rows_irr = 0
            for tkr in [near_tkr, def_tkr]:
                series_non_null_ratio = (
                    (irr[tkr].notna().sum() / total_rows_irr) if (total_rows_irr > 0 and tkr in irr.columns) else 0.0
                )
                if series_non_null_ratio < MIN_NON_NULL_RATIO:
                    warnings.warn(
                        f"Low data coverage for {tkr} [{implied_repo_field}] from {start_date} to {end_date}: "
                        f"{series_non_null_ratio:.1%} non-null",
                        category=UserWarning,
                    )
            irr = irr.reset_index().rename(columns={"index": "Date", "date": "Date"})
            irr.columns = ["Date", f"Implied_Repo_1_{tenor}", f"Implied_Repo_2_{tenor}"]
        else:
            irr = px[["Date"]].copy()
            irr[f"Implied_Repo_1_{tenor}"] = pd.NA
            irr[f"Implied_Repo_2_{tenor}"] = pd.NA
            # Warn explicitly for missing implied repo field (0% coverage)
            warnings.warn(
                f"Low data coverage for {near_tkr} [IMPLIED_REPO] from {start_date} to {end_date}: 0.0% non-null",
                category=UserWarning,
            )
            warnings.warn(
                f"Low data coverage for {def_tkr} [IMPLIED_REPO] from {start_date} to {end_date}: 0.0% non-null",
                category=UserWarning,
            )

        # Merge on Date
        df = px.merge(vol, on="Date", how="outer").merge(irr, on="Date", how="outer")
        frames.append(df)

    # Combine all tenors on Date
    from functools import reduce

    treasury_df = reduce(lambda a, b: a.merge(b, on="Date", how="outer"), frames)
    treasury_df.sort_values("Date", inplace=True)
    treasury_df.reset_index(drop=True, inplace=True)

    # Add Contract columns derived from Date (quarter cycle)
    for v, offset in [(1, 0), (2, 1)]:
        contracts = treasury_df["Date"].apply(
            lambda dt: _quarter_contract_label(
                pd.to_datetime(dt), offset_quarters=offset
            )
        )
        for tenor in tenor_to_tickers.keys():
            treasury_df[f"Contract_{v}_{tenor}"] = contracts

    return treasury_df


def rename_ois_columns(df_ois: pd.DataFrame) -> pd.DataFrame:
    """Rename Bloomberg OIS tickers to compact labels expected downstream."""
    rename_map = {
        "USSO1Z CMPN Curncy": "OIS_1W",
        "USSOA CMPN Curncy": "OIS_1M",
        "USSOC CMPN Curncy": "OIS_3M",
        "USSOF CMPN Curncy": "OIS_6M",
        "USSO1 CMPN Curncy": "OIS_1Y",
    }
    df = df_ois.copy()
    df.columns = [c if c not in rename_map else rename_map[c] for c in df.columns]
    return df


def build_last_day_mapping_from_dates(dates: pd.Series) -> pd.DataFrame:
    """Construct (Mat_Year, Mat_Month) -> Mat_Day mapping as last calendar day."""
    df_dates = pd.DataFrame({"Date": pd.to_datetime(dates)})
    df_dates["Mat_Month"] = df_dates["Date"].dt.month
    df_dates["Mat_Year"] = df_dates["Date"].dt.year
    df_dates = df_dates.sort_values("Date").drop_duplicates(
        ["Mat_Year", "Mat_Month"], keep="last"
    )
    df_dates["Mat_Day"] = df_dates["Date"].dt.day
    return df_dates[["Date", "Mat_Month", "Mat_Year", "Mat_Day"]].reset_index(drop=True)


def load_ois(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    return pd.read_parquet(Path(data_dir) / "basis_treas_sf" / "ois.parquet")


def load_treasury_df(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    return pd.read_parquet(Path(data_dir) / "basis_treas_sf" / "treasury_df.parquet")


def load_last_day(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    return pd.read_parquet(Path(data_dir) / "basis_treas_sf" / "last_day.parquet")


if __name__ == "__main__":
    ois = pull_ois_history()
    ois = rename_ois_columns(ois)
    ois.to_parquet(DATA_DIR / "ois.parquet", index=False)

    tre = pull_futures_history()
    tre.to_parquet(DATA_DIR / "treasury_df.parquet", index=False)

    last_day = build_last_day_mapping_from_dates(tre["Date"])
    last_day.to_parquet(DATA_DIR / "last_day.parquet", index=False)
