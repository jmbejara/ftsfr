"""
This scripts pulls FX rates from the fed reserve FX table on WRDS.
Code by by Alex Wang

DEPRECATED
KEEPING IN CASE OF MIGRATION FROM BBG TO WRDS FOR DATA SOURCING
"""

# Add src directory to Python path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import wrds

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_DATE = pd.Timestamp("1925-01-01")
END_DATE = pd.Timestamp("2024-01-01")


def get_daily_data(wrds_username=WRDS_USERNAME):
    """
    Connects to a WRDS (Wharton Research Data Services) database and fetches data
    Fed reserve FX table named `frb_all`. The data fetched includes the mapping between ISIN
    and REDCODE for our bond&CDS pairs of interest.

    Returns:
        dict: A dictionary where each key is a year from 2001 to 2023 and each value is a DataFrame containing
        the date, ticker, and parspread for that year.
    """
    db = wrds.Connection(wrds_username=wrds_username)
    daily_data = {}

    table_name = "frb_all.fx_daily"
    query = f"""
    SELECT
        *
    FROM
        {table_name} AS a
    """
    daily_data = db.raw_sql(query, date_cols=["date"])
    return daily_data


def get_monthly_data(wrds_username=WRDS_USERNAME):
    """
    Connects to a WRDS (Wharton Research Data Services) database and fetches data
    Fed reserve FX table named `frb_all`. The data fetched includes the mapping between ISIN
    and REDCODE for our bond&CDS pairs of interest.

    Returns:
        dict: A dictionary where each key is a year from 2001 to 2023 and each value is a DataFrame containing
        the date, ticker, and parspread for that year.
    """
    db = wrds.Connection(wrds_username=wrds_username)
    monthly_data = {}

    table_name = "frb_all.fx_monthly"
    query = f"""
    SELECT
        *
    FROM
        {table_name} AS a
    """
    monthly_data = db.raw_sql(query, date_cols=["date"])
    return monthly_data


if __name__ == "__main__":
    daily_df = get_daily_data(wrds_username=WRDS_USERNAME)
    monthly_df = get_monthly_data(wrds_username=WRDS_USERNAME)
    (DATA_DIR).mkdir(parents=True, exist_ok=True)
    daily_df.to_parquet(DATA_DIR / "fx_daily_data.parquet")
    monthly_df.to_parquet(DATA_DIR / "fx_monthly_data.parquet")
