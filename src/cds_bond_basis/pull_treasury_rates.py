"""
This scripts pulls treasury data from WRDS.
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


def get_monthly_ts_data_as_dict(wrds_username=WRDS_USERNAME):
    """
    Connects to a WRDS (Wharton Research Data Services) database and fetches bond data from WRDS
    on the the table named `wrdsapps_bondret.bondret`.

    Returns:
        dict: A dictionary where each key is a year from 2001 to 2023 and each value is a DataFrame containing
        the date, ticker, and parspread for that year.
    """
    db = wrds.Connection(wrds_username=wrds_username)
    bond_data = {}

    table_name = "crsp_m_treasuries.tfz_mth"
    query = f"""
    SELECT
        kycrspid,
        kytreasno,
        mcaldt,
        tmpubout,
        tmyld
    FROM
        {table_name} AS a
    """        
    bond_data = db.raw_sql(query, date_cols=["date"])
    return bond_data

def get_issue_data_as_dict(wrds_username=WRDS_USERNAME):
    """
    Connects to a WRDS (Wharton Research Data Services) database and fetches bond data from WRDS
    on the the table named `wrdsapps_bondret.bondret`.

    Returns:
        dict: A dictionary where each key is a year from 2001 to 2023 and each value is a DataFrame containing
        the date, ticker, and parspread for that year.
    """
    db = wrds.Connection(wrds_username=wrds_username)
    bond_data = {}

    table_name = "crsp_m_treasuries.tfz_iss"
    query = f"""
    SELECT
        kycrspid,
        kytreasno,
        tmatdt
    FROM
        {table_name} AS a
    """        
    bond_data = db.raw_sql(query, date_cols=["date"])
    return bond_data

if __name__ == "__main__":
    df1 = get_monthly_ts_data_as_dict(wrds_username=WRDS_USERNAME)
    df2 = get_issue_data_as_dict(wrds_username=WRDS_USERNAME)
    (DATA_DIR).mkdir(parents=True, exist_ok=True)
    df1.to_parquet(DATA_DIR / "monthly_ts_data.parquet")
    df2.to_parquet(DATA_DIR / "issue_data.parquet")
