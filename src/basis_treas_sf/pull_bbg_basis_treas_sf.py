"""
pull_bbg_basis_treas_sf.py

Pull USD OIS term structure and Treasury futures inputs from Bloomberg via xbbg,
and save individual parquet files for each data pull. The formatting and combining
is handled separately by format_bbg_basis_treas_sf.py.

Outputs (saved under DATA_DIR/basis_treas_sf):
- ois.parquet: Date + OIS tenors (1W, 1M, 3M, 6M, 1Y)
- Individual futures files for each tenor:
  - treasury_2y.parquet: 2Y futures data
  - treasury_5y.parquet: 5Y futures data  
  - treasury_10y.parquet: 10Y futures data
  - treasury_30y.parquet: 30Y futures data
  - treasury_20y.parquet: 20Y futures data (Ultra 10Y proxy)

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
- Each futures tenor is saved separately to avoid column naming conflicts.
- Formatting and combining is handled by format_bbg_basis_treas_sf.py.

Definitions
-----------

- CNVS_FACTOR_EOD: End of day conversion factor of the cheapest to deliver bond. For current day CTD 
data, use the end of day fields: Cheapest to Deliver CUSIP - End of Day (FO049, CTD_CUSIP_EOD) and 
Conversion Factor - End of Day (FO050, CNVS_FACTOR_EOD). The fields will return blank/'0' until some 
time (to be determined) after future's close. For historical CTD data, use fields: Cheapest to Deliver 
CUSIP (FO064, FUT_CTD_CUSIP) and Conversion Factor (FO052, FUT_CNVS_FACTOR (FUT_CONV_FACTOR).

- CONVENTIONAL_CTD_FORWARD_FRSK: Price sensitivity of the future contract to changes in yield, computed 
according to the contract's conventional forward basis. The cheapest to deliver (CTD) bond is used in 
this calculation, where the settlement date is the last delivery date and the maturity date is the 
maturity of the cheapest to deliver. The price at delivery date is the futures price times the CTD 
conversion factor. The resulting risk is divided by the conversion factor. Options: Option risk is 
obtained by delta scaling of the futures risk.

- CTD_CUSIP_EOD: End of day Committee on Uniform Securities Identification Procedures (CUSIP) number of 
the cheapest to deliver (CTD) bond. For current day CTD data, use the end of day fields: Cheapest to 
Deliver CUSIP - End of Day (FO049, CTD_CUSIP_EOD) and Conversion Factor - End of Day (FO050, 
CNVS_FACTOR_EOD). The fields will return blank/'0' until some time (to be determined) after future's 
close. For historical CTD data, use fields: Cheapest to Deliver CUSIP (FO064, FUT_CTD_CUSIP) and 
Conversion Factor (FO052, FUT_CNVS_FACTOR (FUT_CONV_FACTOR).

- CURRENT_CONTRACT_MONTH_YR: Current Contract Month/Year

- FUT_ACTUAL_REPO_RT: The cash-and-carry return for the indicated number of days and day count of the 
CTD bond.

- FUT_AGGTE_OPEN_INT: The total number of futures contracts that have not been closed, liquidated, or 
delivered for all currently listed contracts in a series.

- FUT_AGGTE_VOL: The total number of futures contracts traded for all currently listed contracts in a 
series.

- FUT_CNVS_FACTOR: An adjustment factor used to compute the proper futures invoice price for bonds with 
differing coupons/maturities deliverable into the same futures contract. The conversion factor is 
calculated by the exchange. Returns the cheapest to deliver (CTD) factor by default.

- FUT_CTD_CUSIP: The Cusip of the cheapest to deliver bond.

- FUT_CTD_GROSS_BASIS: The cheapest to deliver bond's price minus the delivery price. The pricing 
source for historical values of FO075 is based on the futures settlement price and bond prices using 
the following pricing source: Treasury futures: BBT3, Gilt futures: BVL4, Euro-Zone futures (French, 
German, Italy, Spain, etc.): BVL4, Canada bond futures: BVN4, Japan bond futures: BVT3, All other bond 
futures: BGN.

- FUT_CTD_NET_BASIS: The cheapest to deliver bond's gross basis adjusted for net carry.

- FUT_CUR_GEN_TICKER: Current Generic Futures Ticker

- FUT_IMPLIED_REPO_RT: The cash-and-carry return for the indicated number of days and day count of the 
Cheapest to Deliver bond.

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


def pull_futures_for_tenor(
    tenor: int, start_date: str = START_DATE, end_date: str = END_DATE
) -> pd.DataFrame:
    """Fetch Treasury futures data for a specific tenor.
    
    Pulls both near (1) and deferred (2) contracts for all specified Bloomberg fields.
    Returns DataFrame with properly named columns to avoid conflicts.
    """
    tenor_to_tickers = futures_ticker_map()
    if tenor not in tenor_to_tickers:
        raise ValueError(f"Unsupported tenor: {tenor}")
    
    near_tkr, def_tkr = tenor_to_tickers[tenor]
    
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

    # Pull data for both contracts
    df = blp.bdh(
        tickers=[near_tkr, def_tkr],
        flds=fields,
        start_date=start_date,
        end_date=end_date,
        timeout=10000,
    )
    
    if isinstance(df.columns, pd.MultiIndex):
        df = df.droplevel(1, axis=1)
    
    # Reset index and rename columns
    df = df.reset_index().rename(columns={"index": "Date", "date": "Date"})
    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
    
    # Rename columns to include tenor and contract version (1 for near, 2 for deferred)
    # This avoids column name conflicts when combining later
    rename_map = {}
    for field in fields:
        # Find columns containing this field
        field_cols = [col for col in df.columns if field in col and col != "Date"]
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
    
    return df


def load_ois(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    return pd.read_parquet(Path(data_dir) / "basis_treas_sf" / "ois.parquet")


def load_treasury_tenor(tenor: int, data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load Treasury futures data for a specific tenor."""
    return pd.read_parquet(Path(data_dir) / "basis_treas_sf" / f"treasury_{tenor}y.parquet")


if __name__ == "__main__":
    # Create output directory
    output_dir = DATA_DIR / "basis_treas_sf"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Pull and save OIS data
    print("Pulling OIS data...")
    ois = pull_ois_history()
    # Save in multiple formats as requested
    ois.to_parquet(output_dir / "ois.parquet", index=False)
    ois.to_csv(output_dir / "ois.csv", index=False)
    ois.to_excel(output_dir / "ois.xlsx", index=False)
    print("Successfully pulled and saved OIS data in all formats")
    
    # Pull and save futures data for each tenor separately
    tenors = [2, 5, 10, 20, 30]
    for tenor in tenors:
        try:
            futures_data = pull_futures_for_tenor(tenor)
            # Save in multiple formats as requested
            futures_data.to_parquet(output_dir / f"treasury_{tenor}y.parquet", index=False)
            futures_data.to_csv(output_dir / f"treasury_{tenor}y.csv", index=False)
            futures_data.to_excel(output_dir / f"treasury_{tenor}y.xlsx", index=False)
            print(f"Successfully pulled and saved {tenor}Y futures data in all formats")
        except Exception as e:
            warnings.warn(f"Failed to pull data for {tenor}Y tenor: {e}", category=UserWarning)
            print(f"Warning: Failed to pull data for {tenor}Y tenor: {e}")
