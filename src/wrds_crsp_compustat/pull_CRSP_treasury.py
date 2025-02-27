"""Pull and load CRSP Treasury Data from WRDS.

Reference:
    CRSP US TREASURY DATABASE GUIDE
    https://www.crsp.org/wp-content/uploads/guides/CRSP_US_Treasury_Database_Guide_for_SAS_ASCII_EXCEL_R.pdf

Data Description:
    TFZ_DLY ( DAILY TIME SERIES ITEMS)
        kytreasno: TREASURY RECORD IDENTIFIER
        kycrspid: CRSP-ASSIGNED UNIQUE ID
        caldt: QUOTATION DATE
        tdbid: DAILY BID
        tdask: DAILY ASK
        tdaccint: DAILY SERIES OF TOTAL ACCRUED INTEREST
        tdyld: DAILY SERIES OF PROMISED DAILY YIELD

    TFZ_ISS (ISSUE DESCRIPTIONS)
        tcusip: TREASURY CUSIP
        tdatdt: DATE DATED BY TREASURY
        tmatdt: MATURITY DATE AT TIME OF ISSUE
        tcouprt: COUPON RATE
        itype: TYPE OF ISSUE (1: NONCALLABLE BONDS, 2: NONCALLABLE NOTES)

Thank you to Younghun Lee for preparing this script for use in class.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import wrds

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")

# Set SUBFOLDER to the folder containing this file
SUBFOLDER = os.path.basename(os.path.dirname(os.path.abspath(__file__)))


def pull_CRSP_treasury_daily(
    start_date="1970-01-01",
    end_date="2023-12-31",
    wrds_username=WRDS_USERNAME,
):
    query = f"""
    SELECT 
        kytreasno, kycrspid, caldt, tdbid, tdask, tdaccint, tdyld,
        ((tdbid + tdask) / 2.0 + tdaccint) AS price
    FROM 
        crspm.tfz_dly
    WHERE 
        caldt BETWEEN '{start_date}' AND '{end_date}'
    """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["tdatdt", "tmatdt"])
    db.close()
    return df


def pull_CRSP_treasury_info(wrds_username=WRDS_USERNAME):
    query = """
        SELECT 
            kytreasno, kycrspid, tcusip, tdatdt, tmatdt, tcouprt, itype,
            ROUND((tmatdt - tdatdt) / 365.0) AS original_maturity
        FROM 
            crspm.tfz_iss AS iss
        WHERE 
            iss.itype IN (1, 2)
    """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["tdatdt", "tmatdt"])
    db.close()
    return df


def calc_runness(data):
    """
    Calculate runness for the securities issued in 1980 or later.

    This is due to the following condition of Gurkaynak, Sack, and Wright (2007):
        iv) Exclude on-the-run issues and 1st off-the-run issues
        for 2,3,5, 7, 10, 20, 30 years securities issued in 1980 or later.
    """

    def _calc_runness(df):
        temp = df.sort_values(by=["caldt", "original_maturity", "tdatdt"])
        next_temp = (
            temp.groupby(["caldt", "original_maturity"])["tdatdt"].rank(
                method="first", ascending=False
            )
            - 1
        )
        return next_temp

    data_run_ = data[data["caldt"] >= "1980"]
    runs = _calc_runness(data_run_)
    data["run"] = 0
    data.loc[data_run_.index, "run"] = runs
    return data


def pull_CRSP_treasury_consolidated(
    start_date="1970-01-01",
    end_date=datetime.today().strftime("%Y-%m-%d"),
    wrds_username=WRDS_USERNAME,
):
    """Pull consolidated CRSP Treasury data with all relevant fields.

    Includes fields from these tables:
    - tfz_dly (daily quotes): bid/ask prices, accrued interest, yields
    - tfz_iss (issue info): CUSIP, dates, coupon rates, issue types

    Price Terminology:
    - Clean Price = (bid + ask)/2 = quoted price without accrued interest
    - Dirty Price = Clean Price + Accrued Interest = actual transaction price

    Date Fields:
    - Quote Date (caldt): Date of the price observation
    - Date Dated (tdatdt): Original issue date when interest starts accruing
    - Maturity Date (tmatdt): Date when the security matures

    Returns:
    - Unadjusted Return (tdretnua): Simple price change plus accrued interest,
      not accounting for tax effects or reinvestment

    Fields are based on CRSP Daily US Treasury Database Guide specifications.
    """

    query = f"""
    SELECT 
        -- Identification
        tfz.kytreasno, tfz.kycrspid, iss.tcusip,
        
        -- Dates
        tfz.caldt,                  -- Quote date: Date of price observation
        iss.tdatdt,                 -- Date dated: Original issue date when interest starts accruing
        iss.tmatdt,                 -- Maturity date: When principal is repaid
        iss.tfcaldt,                -- First call date (0 if not callable)
        
        -- Prices and Yields
        tfz.tdbid,                  -- Bid price (clean)
        tfz.tdask,                  -- Ask price (clean)
        tfz.tdaccint,               -- Accrued interest since last coupon
        tfz.tdyld,                  -- Bond equivalent yield
        ((tfz.tdbid + tfz.tdask) / 2.0 + tfz.tdaccint) AS price,  
                                    -- Dirty price (clean price + accrued interest)
        
        -- Issue Characteristics
        iss.tcouprt,                -- Coupon rate (annual)
        iss.itype,                  -- Type of issue (1: bonds, 2: notes)
        ROUND((iss.tmatdt - iss.tdatdt) / 365.0) AS original_maturity,  
                                    -- Original maturity at issuance
        
        -- Additional Derived Fields
        ROUND((iss.tmatdt - tfz.caldt) / 365.0) AS years_to_maturity,  
                                    -- Remaining time to maturity
        
        -- Trading info (if available)
        tfz.tdduratn,               -- Duration: Price sensitivity to yield changes
        tfz.tdretnua                -- Return (unadjusted): Simple price change + accrued interest
        
    FROM 
        crspm.tfz_dly AS tfz
    LEFT JOIN 
        crspm.tfz_iss AS iss 
    ON 
        tfz.kytreasno = iss.kytreasno AND 
        tfz.kycrspid = iss.kycrspid
    WHERE 
        tfz.caldt BETWEEN '{start_date}' AND '{end_date}' AND 
        iss.itype IN (1, 2)  -- Only include Treasury bonds (1) and notes (2)
    """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["caldt", "tdatdt", "tmatdt", "tfcaldt"])
    df["days_to_maturity"] = (df["tmatdt"] - df["caldt"]).dt.days
    df["tfcaldt"] = pd.to_datetime(df["tfcaldt"]).fillna(pd.Timestamp(0))
    df["callable"] = df["tfcaldt"] != pd.Timestamp(0)
    db.close()
    df = df.reset_index(drop=True)
    return df


def load_CRSP_treasury_daily(data_dir=DATA_DIR):
    path = data_dir / SUBFOLDER / "TFZ_DAILY.parquet"
    df = pd.read_parquet(path)
    return df


def load_CRSP_treasury_info(data_dir=DATA_DIR):
    path = data_dir / SUBFOLDER / "TFZ_INFO.parquet"
    df = pd.read_parquet(path)
    return df


def load_CRSP_treasury_consolidated(data_dir=DATA_DIR, with_runness=True):
    if with_runness:
        path = data_dir / SUBFOLDER / "TFZ_with_runness.parquet"
    else:
        path = data_dir / SUBFOLDER / "TFZ_consolidated.parquet"
    df = pd.read_parquet(path)
    return df


def _demo():
    df = pull_CRSP_treasury_daily(data_dir=DATA_DIR)
    df.info()
    df = pull_CRSP_treasury_info(data_dir=DATA_DIR)
    df.info()
    df = pull_CRSP_treasury_consolidated(data_dir=DATA_DIR)
    df.info()
    df = calc_runness(df)
    df.info()
    return df


if __name__ == "__main__":
    df = pull_CRSP_treasury_daily(
        start_date="1970-01-01",
        end_date="2023-12-31",
        wrds_username=WRDS_USERNAME,
    )
    path = DATA_DIR / SUBFOLDER / "CRSP_TFZ_DAILY.parquet"
    df.to_parquet(path)

    df = pull_CRSP_treasury_info(wrds_username=WRDS_USERNAME)
    path = DATA_DIR / SUBFOLDER / "CRSP_TFZ_INFO.parquet"
    df.to_parquet(path)

    df = pull_CRSP_treasury_consolidated(wrds_username=WRDS_USERNAME)
    path = DATA_DIR / SUBFOLDER / "CRSP_TFZ_consolidated.parquet"
    df.to_parquet(path)

    df = calc_runness(df)
    path = DATA_DIR / SUBFOLDER / "CRSP_TFZ_with_runness.parquet"
    df.to_parquet(path)
