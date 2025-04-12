"""
This scripts pulls bond data from WRDS.
Code by adjusted by Alex Wang
"""

# Add src directory to Python path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import os

import pandas as pd
import numpy as np
import wrds

from settings import config

# Set SUBFOLDER to the folder containing this file
SUBFOLDER = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")


def get_bond_data_as_dict(wrds_username=WRDS_USERNAME):
    """
    Connects to a WRDS (Wharton Research Data Services) database and fetches bond data from WRDS
    on the the table named `wrdsapps_bondret.bondret`.

    Returns:
        dict: A dictionary where each key is a year from 2001 to 2023 and each value is a DataFrame containing
        the date, ticker, and parspread for that year.
    """
    db = wrds.Connection(wrds_username=wrds_username)
    bond_data = {}

    table_name = "wrdsapps_bondret.bondret"
    query = f"""
    SELECT
        offering_date, -- The date the issue was originally offered.
        company_symbol, -- Company Symbol (issuer stock ticker).
        maturity, -- Date that the issue's principal is due for repayment.
        amount_outstanding, -- The amount of the issue remaining outstanding.
        security_level, -- SEN is Senior Unsecured Debt i think
        date, -- Monthly Date
        yield, -- Yield to maturity at the time of issuance.
        cusip,
        isin,
        rating_class, -- Combined Rating Class: 0.IG or 1.HY
        conv, -- Flag Convertible (1 or 0)
        offering_price, -- Offering Price
        price_eom, -- Price-End of Month
        t_spread, -- Avg Bid/Ask Spread
        principal_amt -- The face or par value of a single bond (i.e., the sum that is to be paid at maturity, usually $1000).
    FROM
        {table_name} AS a
    WHERE
        (a.isin != '') AND
        (a.conv = '0') AND
        (a.security_level = 'SEN') AND
        (a.principal_amt > 10) AND
        (a.amount_outstanding > 99999)
    """        
    bond_data = db.raw_sql(query, date_cols=["date"])
    return bond_data

def filter_data(data):
    """
    Filters the bonds based on the required filters in the paper
    """
    #bonds = data[data["amount_outstanding"] >= 100000]
    bonds = data
    bonds.loc[:,"maturity_time_frame"] = bonds.loc[:,"maturity"] - bonds.loc[:,"offering_date"]
    bonds.loc[:,"maturity_time_frame"] = bonds.loc[:,"maturity_time_frame"].astype(str).str.split(',').str[0]
    bonds.loc[:,"maturity_time_frame"] = bonds.loc[:,"maturity_time_frame"].astype(str).str.split(' ').str[0]
    bonds.loc[:,"maturity_time_frame"] = pd.to_numeric(bonds.loc[:,"maturity_time_frame"], errors='coerce') / 365.25
    bonds = bonds.dropna(subset=['maturity_time_frame'])
    bonds['maturity_time_frame'] = bonds['maturity_time_frame'].round().astype(int)
    bonds['rating'] = bonds.loc[:,"rating_class"].astype(str).str.split('.').str[0].astype(int)
    bonds.drop('rating_class', axis=1, inplace=True)
  
    #bonds = bonds[(bonds['price_eom'] != 0) & ((bonds['price_eom'] / bonds['principal_amt']) >= 0.5)]

    mask_g1 = bonds["maturity_time_frame"] >= 1
    mask_l10 = bonds['maturity_time_frame'] <= 10
    mask_yield_0 = bonds['yield'] > 0
    mask_yield_05 = bonds['yield'] < 0.5
    mask_eom50 = bonds['price_eom'] > 50
    mask_eom150 = bonds['price_eom'] < 150

    return bonds[mask_g1 & mask_l10 & mask_yield_0 & mask_yield_05 & mask_eom50 & mask_eom150].set_index("date")

if __name__ == "__main__":
    combined_df = get_bond_data_as_dict(wrds_username=WRDS_USERNAME)
    filered = filter_data(combined_df)
    (DATA_DIR).mkdir(parents=True, exist_ok=True)
    filered.to_parquet(DATA_DIR / "wrds_bond.parquet")
