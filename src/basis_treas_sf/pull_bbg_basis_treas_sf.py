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
import warnings
import polars as pl

from settings import config


# Configuration via settings.py
DATA_DIR: Path = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "basis_treas_sf"
START_DATE: str = config("START_DATE", default="2000-01-01")
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
) -> pl.DataFrame:
    """Fetch historical USD OIS levels (PX_LAST) from Bloomberg via xbbg.

    Returns Date + ticker columns. Consumers rename to compact labels later.

    >>> ois.glimpse(max_items_per_column=2)
    Rows: 5587
    Columns: 7
    $ Date               <datetime[ns]> 2004-01-01 00:00:00, 2004-01-02 00:00:00
    $ USSO1Z CMPN Curncy          <f64> 1.0, 1.0
    $ USSOA CMPN Curncy           <f64> 1.01, 1.005
    $ USSOB CMPN Curncy           <f64> 1.008, 1.009
    $ USSOC CMPN Curncy           <f64> 1.015, 1.016
    $ USSOF CMPN Curncy           <f64> 1.058, 1.077
    $ USSO1 CMPN Curncy           <f64> 1.29, 1.353
    """
    from xbbg import blp
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
            non_null_ratio = (
                (df[tkr].notna().sum() / total_rows) if total_rows > 0 else 0.0
            )
            if non_null_ratio < MIN_NON_NULL_RATIO:
                warnings.warn(
                    f"Low data coverage for {tkr} [PX_LAST] from {start_date} to {end_date}: "
                    f"{non_null_ratio:.1%} non-null",
                    category=UserWarning,
                )
    df = pl.from_pandas(df)
    return df


def futures_ticker_map() -> Dict[int, Tuple[str, str]]:
    """Map tenor (years) to (near, deferred) generic Bloomberg futures tickers."""
    mapping: Dict[int, Tuple[str, str]] = {
        2: ("TU1 Comdty", "TU2 Comdty"),
        5: ("FV1 Comdty", "FV2 Comdty"),
        10: ("TY1 Comdty", "TY2 Comdty"),
        20: ("US1 Comdty", "US2 Comdty"),
        30: ("WN1 Comdty", "WN2 Comdty"),
        # 10: ("TN1 Comdty", "TN2 Comdty"), # Ultra Ten Year. All implied repo rates are missing
    }
    return mapping


def _check_coverage(df: pl.DataFrame, message="") -> None:
    """Check coverage of a DataFrame."""
    total_rows = len(df)
    for col in df.columns:
        non_null_ratio = (
            (df[col].is_not_null().sum() / total_rows) if total_rows > 0 else 0.0
        )
        if non_null_ratio < MIN_NON_NULL_RATIO:
            print(message)
            warnings.warn(
                f"Low data coverage for {col}: {non_null_ratio:.1%} non-null",
                category=UserWarning,
            )


def pull_futures_for_tenor(
    tenor: int, start_date: str = START_DATE, end_date: str = END_DATE
) -> Tuple[pl.DataFrame, pl.DataFrame]:
    """Fetch Treasury futures data for a specific tenor.

    Pulls both near (1) and deferred (2) contracts for all specified Bloomberg fields.
    Returns DataFrame with properly named columns to avoid conflicts.

    >>> futures_data1.tail().glimpse(max_items_per_column=2)
    Rows: 5
    Columns: 16
    $ Date                          <date> 2025-05-26, 2025-05-27
    $ PX_LAST                        <f64> None, 112.90625
    $ CURRENT_CONTRACT_MONTH_YR      <str> None, 'JUN 25'
    $ FUT_ACTUAL_REPO_RT             <f64> None, 4.32315
    $ FUT_AGGTE_OPEN_INT             <f64> None, 1899157.0
    $ FUT_AGGTE_VOL                  <f64> 111905.0, 2322952.0
    $ FUT_CNVS_FACTOR                <f64> None, 0.875
    $ FUT_CTD_CUSIP                  <str> None, '912810QN'
    $ FUT_CTD_GROSS_BASIS            <f64> None, 6.6236
    $ FUT_CTD_NET_BASIS              <f64> None, 5.4914
    $ FUT_CUR_GEN_TICKER             <str> None, 'USM5'
    $ FUT_IMPLIED_REPO_RT            <f64> None, 2.4574
    $ FUT_PX                         <f64> None, 112.6875
    $ CONVENTIONAL_CTD_FORWARD_FRSK  <f64> None, 12.3176
    $ CTD_CUSIP_EOD                  <str> None, '912810QN'
    $ CNVS_FACTOR_EOD                <f64> None, 0.875

    >>> futures_data2.tail().glimpse(max_items_per_column=2)
    Rows: 5
    Columns: 16
    $ Date                          <date> 2025-05-26, 2025-05-27
    $ PX_LAST                        <f64> None, 112.5625
    $ CURRENT_CONTRACT_MONTH_YR      <str> None, 'SEP 25'
    $ FUT_ACTUAL_REPO_RT             <f64> None, 4.32281
    $ FUT_AGGTE_OPEN_INT             <f64> None, 1899157.0
    $ FUT_AGGTE_VOL                  <f64> 111905.0, 2322952.0
    $ FUT_CNVS_FACTOR                <f64> None, 0.8762
    $ FUT_CTD_CUSIP                  <str> None, '912810QN'
    $ FUT_CTD_GROSS_BASIS            <f64> None, 11.9276
    $ FUT_CTD_NET_BASIS              <f64> None, 7.5302
    $ FUT_CUR_GEN_TICKER             <str> None, 'USU5'
    $ FUT_IMPLIED_REPO_RT            <f64> None, 3.64143
    $ FUT_PX                         <f64> None, 112.375
    $ CONVENTIONAL_CTD_FORWARD_FRSK  <f64> None, 12.14
    $ CTD_CUSIP_EOD                  <str> None, '912810QN'
    $ CNVS_FACTOR_EOD                <f64> None, 0.8762

    """
    from xbbg import blp
    tenor_to_tickers = futures_ticker_map()
    if tenor not in tenor_to_tickers:
        raise ValueError(f"Unsupported tenor: {tenor}")

    near_tkr, def_tkr = tenor_to_tickers[tenor]

    # Define all Bloomberg fields to pull
    fields = [
        "PX_LAST",  # Last Price
        "CURRENT_CONTRACT_MONTH_YR",  # Current Contract Month/Year
        "FUT_ACTUAL_REPO_RT",  # Actual Repo Rate
        "FUT_AGGTE_OPEN_INT",  # Aggregate Open Interest
        "FUT_AGGTE_VOL",  # Aggregate Volume of Futures Contracts
        "FUT_CNVS_FACTOR",  # Conversion Factor
        "FUT_CTD_CUSIP",  # Cheapest to Deliver CUSIP
        "FUT_CTD_GROSS_BASIS",  # Cheapest to Deliver Gross Basis
        "FUT_CTD_NET_BASIS",  # Cheapest to Deliver Net Basis
        "FUT_CUR_GEN_TICKER",  # Current Generic Futures Ticker
        "FUT_IMPLIED_REPO_RT",  # Implied Repo Rate of CTD Bond
        "FUT_PX",  # Futures Trade Price
        "CONVENTIONAL_CTD_FORWARD_FRSK",  # Conventional CTD Forward Risk
        "CTD_CUSIP_EOD",  # Cheapest to Deliver CUSIP - End of Day
        "CNVS_FACTOR_EOD",  # Conversion Factor - End of Day
    ]

    # Pull data for both contracts
    df = blp.bdh(
        tickers=[near_tkr, def_tkr],
        flds=fields,
        start_date=start_date,
        end_date=end_date,
        timeout=10000,
    )

    df1 = df[near_tkr]
    df2 = df[def_tkr]
    df1.index.name = "Date"
    df2.index.name = "Date"
    df1.reset_index(inplace=True)
    df2.reset_index(inplace=True)

    df1 = pl.from_pandas(df1)
    df2 = pl.from_pandas(df2)

    _check_coverage(df1, message=f"Tenor={tenor}")
    _check_coverage(df2, message=f"Tenor={tenor}")

    return df1, df2


def load_ois(data_dir: Path = DATA_DIR) -> pl.DataFrame:
    return pl.read_parquet(Path(data_dir) / "ois.parquet")


def load_treasury_tenor(
    tenor: int, data_dir: Path = DATA_DIR
) -> Tuple[pl.DataFrame, pl.DataFrame]:
    """Load Treasury futures data for a specific tenor."""
    df1 = pl.read_parquet(Path(data_dir) / f"treasury_{tenor}y_1.parquet")
    df2 = pl.read_parquet(Path(data_dir) / f"treasury_{tenor}y_2.parquet")
    return df1, df2


if __name__ == "__main__":

    # Pull and save OIS data
    ois = pull_ois_history()
    ois.write_parquet(DATA_DIR / "ois.parquet")

    # Pull and save futures data for each tenor separately
    tenors = [2, 5, 10, 20, 30]
    for tenor in tenors:
        futures_data1, futures_data2 = pull_futures_for_tenor(tenor)
        # Save futures data for each tenor
        futures_data1.write_parquet(DATA_DIR / f"treasury_{tenor}y_1.parquet")
        futures_data2.write_parquet(DATA_DIR / f"treasury_{tenor}y_2.parquet")
        futures_data1.write_csv(DATA_DIR / f"treasury_{tenor}y_1.csv")
        futures_data2.write_csv(DATA_DIR / f"treasury_{tenor}y_2.csv")
