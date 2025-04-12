"""
This scripts pulls a table that maps RED codes from the Markit CDS database to 
ISIN codes in the Mergent Bond database.
Code by adjusted by Alex Wang
"""

# Add src directory to Python path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import os

import pandas as pd
import wrds

from settings import config

# Set SUBFOLDER to the folder containing this file
SUBFOLDER = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_DATE = pd.Timestamp("1925-01-01")
END_DATE = pd.Timestamp("2024-01-01")


def get_mapping(wrds_username=WRDS_USERNAME):
    """
    Connects to a WRDS (Wharton Research Data Services) database and fetches data from Markit
    from the table named `markit_red.redobllookup`. The data fetched includes the mapping between ISIN
    and REDCODE for our bond&CDS pairs of interest.

    Returns:
        dict: A dictionary where each key is a year from 2001 to 2023 and each value is a DataFrame containing
        the date, ticker, and parspread for that year.
    """
    db = wrds.Connection(wrds_username=wrds_username)
    bond_data = {}

    table_name = "markit_red.redobllookup" 
    query = f"""
    SELECT
        redcode, -- REDCODE (Markit Primary Entity ID)
        ticker, -- 	Markit Entity Ticker
        obl_cusip, -- Obligation CUSIP.
        isin, -- The International Securities Identification Number associated with this issue.
        tier

    FROM
        {table_name} AS a
    WHERE
        (a.tier = 'SNRFOR')
    """
    bond_data = db.raw_sql(query, date_cols=["date"])
    return bond_data

if __name__ == "__main__":
    combined_df = get_mapping(wrds_username=WRDS_USERNAME)
    (DATA_DIR).mkdir(parents=True, exist_ok=True)
    combined_df.to_parquet(DATA_DIR / "RED_and_ISIN_mapping.parquet")
