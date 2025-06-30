"""
Fetches and loads raw foreign exchange data from Bloomberg or Excel.

This module handles only data retrieval and storage. All calculations
(CIP spreads, reciprocal conversions, etc.) are handled in calc_cip.py.

This code is adapted with permission from https://github.com/Kunj121/CIP
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import pandas as pd
import polars as pl
from settings import config

DATA_DIR = config("DATA_DIR")
END_DATE = pd.Timestamp.today().strftime("%Y-%m-%d")


def pull_fx_data(start_date="1950-01-01", end_date=END_DATE):
    """
    Fetch historical foreign exchange data from Bloomberg using xbbg.

    Parameters
    ----------
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format

    Returns
    -------
    dict
        Dictionary with three DataFrames:
        - 'spot_rates': Spot exchange rates
        - 'forward_rates': 3M forward rates
        - 'interest_rates': Interest rates (OIS)
    """
    # import here to enchance compatibility with devices that don't support xbbg
    from xbbg import blp

    # Tickers for interest rates (OIS)
    interest_rate_tickers = [
        "ADSOC CMPN Curncy",  # AUD
        "CDSOC CMPN Curncy",  # CAD
        "SFSNTC CMPN Curncy",  # CHF
        "EUSWEC CMPN Curncy",  # EUR
        "BPSWSC CMPN Curncy",  # GBP
        "JYSOC CMPN Curncy",  # JPY
        "NDSOC CMPN Curncy",  # NZD
        "SKSWTNC BGN Curncy",  # SEK
        "USSOC CMPN Curncy",  # USD
    ]

    # Tickers for 3M forward points
    forward_point_tickers = [
        "AUD3M CMPN Curncy",
        "CAD3M CMPN Curncy",
        "CHF3M CMPN Curncy",
        "EUR3M CMPN Curncy",
        "GBP3M CMPN Curncy",
        "JPY3M CMPN Curncy",
        "NZD3M CMPN Curncy",
        "SEK3M CMPN Curncy",
    ]

    # Tickers for spot rates
    spot_rate_tickers = [
        "AUD CMPN Curncy",
        "CAD CMPN Curncy",
        "CHF CMPN Curncy",
        "EUR CMPN Curncy",
        "GBP CMPN Curncy",
        "JPY CMPN Curncy",
        "NZD CMPN Curncy",
        "SEK CMPN Curncy",
    ]

    fields = ["PX_LAST"]

    # Helper to flatten multi-index columns from xbbg
    def process_bloomberg_df(df):
        if not df.empty and isinstance(df.columns, pd.MultiIndex):
            df.columns = [f"{t[0]}_{t[1]}" for t in df.columns]
            df.reset_index(inplace=True)
        return df

    # Pull each set of tickers
    interest_rates_df = process_bloomberg_df(
        blp.bdh(
            tickers=interest_rate_tickers,
            flds=fields,
            start_date=start_date,
            end_date=end_date,
        )
    )

    forward_points_df = process_bloomberg_df(
        blp.bdh(
            tickers=forward_point_tickers,
            flds=fields,
            start_date=start_date,
            end_date=end_date,
        )
    )

    spot_rates_df = process_bloomberg_df(
        blp.bdh(
            tickers=spot_rate_tickers,
            flds=fields,
            start_date=start_date,
            end_date=end_date,
        )
    )

    return {
        "spot_rates": spot_rates_df,
        "forward_points": forward_points_df,
        "interest_rates": interest_rates_df,
    }


def load_fx_spot_rates(data_dir=DATA_DIR):
    """Load spot exchange rates from parquet file.
    df = load_fx_spot_rates(data_dir=DATA_DIR)
    df = pl.from_pandas(df)
    df.glimpse(max_items_per_column=1)
    Rows: 14207
    Columns: 9
    $ index                   <date> 1971-01-04
    $ AUD CMPN Curncy_PX_LAST  <f64> 1.1127
    $ CAD CMPN Curncy_PX_LAST  <f64> 1.0109
    $ CHF CMPN Curncy_PX_LAST  <f64> 4.318
    $ EUR CMPN Curncy_PX_LAST  <f64> None
    $ GBP CMPN Curncy_PX_LAST  <f64> 2.3938
    $ JPY CMPN Curncy_PX_LAST  <f64> 357.73
    $ NZD CMPN Curncy_PX_LAST  <f64> 1.1138
    $ SEK CMPN Curncy_PX_LAST  <f64> 5.1643
    """
    path = data_dir / "fx_spot_rates.parquet"
    return pd.read_parquet(path)


def load_fx_forward_points(data_dir=DATA_DIR):
    """Load 3M forward points from parquet file.

    df = load_fx_forward_points(data_dir=DATA_DIR)
    df = pl.from_pandas(df)
    df.glimpse(max_items_per_column=1)
    Rows: 10376
    Columns: 9
    $ index                     <date> 1983-12-13
    $ AUD3M CMPN Curncy_PX_LAST  <f64> 21.4
    $ CAD3M CMPN Curncy_PX_LAST  <f64> None
    $ CHF3M CMPN Curncy_PX_LAST  <f64> None
    $ EUR3M CMPN Curncy_PX_LAST  <f64> None
    $ GBP3M CMPN Curncy_PX_LAST  <f64> None
    $ JPY3M CMPN Curncy_PX_LAST  <f64> None
    $ NZD3M CMPN Curncy_PX_LAST  <f64> None
    $ SEK3M CMPN Curncy_PX_LAST  <f64> None
    """
    path = data_dir / "fx_forward_points.parquet"
    return pd.read_parquet(path)


def load_fx_interest_rates(data_dir=DATA_DIR):
    """Load interest rates (OIS) from parquet file.

    df = load_fx_interest_rates(data_dir=DATA_DIR)
    df = pl.from_pandas(df)
    df.glimpse(max_items_per_column=1)
    Rows: 6867
    Columns: 10
    $ index                      <date> 1999-02-08
    $ ADSOC CMPN Curncy_PX_LAST   <f64> None
    $ CDSOC CMPN Curncy_PX_LAST   <f64> None
    $ SFSNTC CMPN Curncy_PX_LAST  <f64> None
    $ EUSWEC CMPN Curncy_PX_LAST  <f64> 3.102
    $ BPSWSC CMPN Curncy_PX_LAST  <f64> None
    $ JYSOC CMPN Curncy_PX_LAST   <f64> None
    $ NDSOC CMPN Curncy_PX_LAST   <f64> None
    $ SKSWTNC BGN Curncy_PX_LAST  <f64> None
    $ USSOC CMPN Curncy_PX_LAST   <f64> None

    """
    path = data_dir / "fx_interest_rates.parquet"
    return pd.read_parquet(path)


if __name__ == "__main__":
    # DATA_DIR = DATA_DIR / "foreign_exchange"
    # Pull data from source
    fx_data = pull_fx_data()

    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Save each dataset to parquet
    fx_data["spot_rates"].to_parquet(DATA_DIR / "fx_spot_rates.parquet")
    fx_data["forward_points"].to_parquet(DATA_DIR / "fx_forward_points.parquet")
    fx_data["interest_rates"].to_parquet(DATA_DIR / "fx_interest_rates.parquet")
