"""
pull_bbg_basis_treas_sf.py

Pull USD OIS term structure and Treasury futures inputs from Bloomberg via xbbg,
and write standardized parquet files used downstream by `calc_basis_treas_sf.py`.

Outputs (saved under DATA_DIR/basis_treas_sf):
- ois.parquet: Date + OIS tenors (1W, 1M, 3M, 6M, 1Y)
- treasury_df.parquet: Date + per-tenor columns for near (1) and deferred (2)
  contracts with all specified Bloomberg fields (e.g., PX_LAST_1_<tenor>, FUT_AGGTE_VOL_2_<tenor>, etc.)
- last_day.parquet: Mapping of (Mat_Year, Mat_Month) -> Mat_Day (last calendar day)

Fields Pulled by Security Type
------------------------------

USD OIS Rates (via ois_tickers()):
- PX_LAST: Last Price for each OIS tenor (1W, 1M, 2M, 3M, 6M, 1Y)

Treasury Futures (via futures_ticker_map() for each tenor 2Y, 5Y, 10Y, 20Y, 30Y):
- PX_LAST: Last Price (Futures Trade Price)
- CURRENT_CONTRACT_MONTH_YR: Current Contract Month/Year
- FUT_ACTUAL_REPO_RT: Actual Repo Rate
- FUT_AGGTE_OPEN_INT: Aggregate Open Interest
- FUT_AGGTE_VOL: Aggregate Volume of Futures Contracts  
- FUT_CNVS_FACTOR: Conversion Factor
- FUT_CTD_CUSIP: Cheapest to Deliver CUSIP
- FUT_CTD_GROSS_BASIS: Cheapest to Deliver Gross Basis
- FUT_CTD_NET_BASIS: Cheapest to Deliver Net Basis
- FUT_CUR_GEN_TICKER: Current Generic Futures Ticker
- FUT_IMPLIED_REPO_RT: Implied Repo Rate of CTD Bond
- FUT_PX: Futures Trade Price
- CONVENTIONAL_CTD_FORWARD_FRSK: Conventional CTD Forward Risk
- CTD_CUSIP_EOD: Cheapest to Deliver CUSIP - End of Day
- CNVS_FACTOR_EOD: Conversion Factor - End of Day

Notes
-----
- No printing to stdout per project style guide.
- Replaces prior reliance on a manual Excel file.

Field Descriptions
-----------------
- CNVS_FACTOR_EOD: End of day conversion factor of the cheapest to deliver bond. For current day CTD data, use the end of day fields: Cheapest to Deliver CUSIP - End of Day (FO049, CTD_CUSIP_EOD) and Conversion Factor - End of Day (FO050, CNVS_FACTOR_EOD). The fields will return blank/'0' until some time (to be determined) after future's close. For historical CTD data, use fields: Cheapest to Deliver CUSIP (FO064, FUT_CTD_CUSIP) and Conversion Factor (FO052, FUT_CNVS_FACTOR (FUT_CONV_FACTOR).

- CONVENTIONAL_CTD_FORWARD_FRSK: Price sensitivity of the future contract to changes in yield, computed according to the contract's conventional forward basis. The cheapest to deliver (CTD) bond is used in this calculation, where the settlement date is the last delivery date and the maturity date is the maturity of the cheapest to deliver. The price at delivery date is the futures price times the CTD conversion factor. The resulting risk is divided by the conversion factor. Options: Option risk is obtained by delta scaling of the futures risk.

- CTD_CUSIP_EOD: End of day Committee on Uniform Securities Identification Procedures (CUSIP) number of the cheapest to deliver (CTD) bond. For current day CTD data, use the end of day fields: Cheapest to Deliver CUSIP - End of Day (FO049, CTD_CUSIP_EOD) and Conversion Factor - End of Day (FO050, CNVS_FACTOR_EOD). The fields will return blank/'0' until some time (to be determined) after future's close. For historical CTD data, use fields: Cheapest to Deliver CUSIP (FO064, FUT_CTD_CUSIP) and Conversion Factor (FO052, FUT_CNVS_FACTOR (FUT_CONV_FACTOR).

- CURRENT_CONTRACT_MONTH_YR: Current Contract Month/Year

- FUT_ACTUAL_REPO_RT: The cash-and-carry return for the indicated number of days and day count of the CTD bond.

- FUT_AGGTE_OPEN_INT: The total number of futures contracts that have not been closed, liquidated, or delivered for all currently listed contracts in a series.

- FUT_AGGTE_VOL: The total number of futures contracts traded for all currently listed contracts in a series.

- FUT_CNVS_FACTOR: An adjustment factor used to compute the proper futures invoice price for bonds with differing coupons/maturities deliverable into the same futures contract. The conversion factor is calculated by the exchange. Returns the cheapest to deliver (CTD) factor by default.

- FUT_CTD_CUSIP: The Cusip of the cheapest to deliver bond.

- FUT_CTD_GROSS_BASIS: The cheapest to deliver bond's price minus the delivery price. The pricing source for historical values of FO075 is based on the futures settlement price and bond prices using the following pricing source: Treasury futures: BBT3, Gilt futures: BVL4, Euro-Zone futures (French, German, Italy, Spain, etc.): BVL4, Canada bond futures: BVN4, Japan bond futures: BVT3, All other bond futures: BGN.

- FUT_CTD_NET_BASIS: The cheapest to deliver bond's gross basis adjusted for net carry.

- FUT_CUR_GEN_TICKER: Current Generic Futures Ticker

- FUT_IMPLIED_REPO_RT: The cash-and-carry return for the indicated number of days and day count of the Cheapest to Deliver bond.

- FUT_PX: Futures Trade Price

- PX_LAST: Last Price
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple

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

    For each tenor and for near (1) and deferred (2) generic contracts, pull all
    specified Bloomberg fields including price, volume, implied repo, CTD data,
    and other futures metrics.
    """
    tenor_to_tickers = futures_ticker_map()
    
    # Define all Bloomberg fields to pull
    fields = [
        "PX_LAST",                    # Last Price
        "CURRENT_CONTRACT_MONTH_YR",  # Current Contract Month/Year
        "FUT_ACTUAL_REPO_RT",         # Actual Repo Rate
        "FUT_AGGTE_OPEN_INT",         # Aggregate Open Interest
        "FUT_AGGTE_VOL",              # Aggregate Volume of Futures Contracts
        "FUT_CNVS_FACTOR",            # Conversion Factor
        "FUT_CTD_CUSIP",              # Cheapest to Deliver CUSIP
        "FUT_CTD_GROSS_BASIS",        # Cheapest to Deliver Gross Basis
        "FUT_CTD_NET_BASIS",          # Cheapest to Deliver Net Basis
        "FUT_CUR_GEN_TICKER",         # Current Generic Futures Ticker
        "FUT_IMPLIED_REPO_RT",        # Implied Repo Rate of CTD Bond
        "FUT_PX",                     # Futures Trade Price
        "CONVENTIONAL_CTD_FORWARD_FRSK", # Conventional CTD Forward Risk
        "CTD_CUSIP_EOD",              # Cheapest to Deliver CUSIP - End of Day
        "CNVS_FACTOR_EOD",            # Conversion Factor - End of Day
    ]

    frames: List[pd.DataFrame] = []
    for tenor, (near_tkr, def_tkr) in tenor_to_tickers.items():
        # Pull all fields for both near and deferred contracts
        df = blp.bdh(
            tickers=[near_tkr, def_tkr],
            flds=fields,
            start_date=start_date,
            end_date=end_date,
        )
        
        if isinstance(df.columns, pd.MultiIndex):
            df = df.droplevel(1, axis=1)
        
        # Reset index and rename columns
        df = df.reset_index().rename(columns={"index": "Date", "date": "Date"})
        
        # Rename columns to include tenor and contract version (1 for near, 2 for deferred)
        # Bloomberg returns columns with ticker names, so we need to map them correctly
        rename_map = {}
        for field in fields:
            if field in df.columns:
                # Find the column names that contain this field
                field_cols = [col for col in df.columns if field in col]
                if len(field_cols) >= 2:
                    # First occurrence is near contract (1), second is deferred (2)
                    rename_map[field_cols[0]] = f"{field}_1_{tenor}"
                    rename_map[field_cols[1]] = f"{field}_2_{tenor}"
                elif len(field_cols) == 1:
                    # Only one occurrence, treat as near contract
                    rename_map[field_cols[0]] = f"{field}_1_{tenor}"
        
        df = df.rename(columns=rename_map)
        
        # Coverage checks for all series
        total_rows = len(df)
        for field in fields:
            col_1 = f"{field}_1_{tenor}"
            col_2 = f"{field}_2_{tenor}"
            if col_1 in df.columns:
                non_null_ratio = df[col_1].notna().sum() / total_rows if total_rows > 0 else 0.0
                if non_null_ratio < MIN_NON_NULL_RATIO:
                    warnings.warn(
                        f"Low data coverage for {near_tkr} [{field}] from {start_date} to {end_date}: "
                        f"{non_null_ratio:.1%} non-null",
                        category=UserWarning,
                    )
            if col_2 in df.columns:
                non_null_ratio = df[col_2].notna().sum() / total_rows if total_rows > 0 else 0.0
                if non_null_ratio < MIN_NON_NULL_RATIO:
                    warnings.warn(
                        f"Low data coverage for {def_tkr} [{field}] from {start_date} to {end_date}: "
                        f"{non_null_ratio:.1%} non-null",
                        category=UserWarning,
                    )
        
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
