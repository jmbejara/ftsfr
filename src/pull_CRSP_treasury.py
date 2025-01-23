from pathlib import Path

import pandas as pd
import wrds

from settings import config

SUBFOLDER = "crsp_treasury"
DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_DATE = pd.Timestamp("1925-01-01")
END_DATE = pd.Timestamp("2024-01-01")


"""
Reference:
    CRSP US TREASURY DATABASE GUIDE
    https://www.crsp.org/wp-content/uploads/guides/CRSP_US_Treasury_Database_Guide_for_SAS_ASCII_EXCEL_R.pdf

Data Description
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

"""


def pull_CRSP_treasury_daily(
    start_date=START_DATE,
    end_date=END_DATE,
    wrds_username=WRDS_USERNAME,
):
    query = f"""
        SELECT kytreasno, kycrspid, caldt, tdbid, tdask, tdaccint, tdyld,
        ((tdbid + tdask) / 2.0 + tdaccint) AS price
        FROM crspm.tfz_dly AS tfz
        WHERE tfz.caldt BETWEEN '{start_date}' AND '{end_date}'
    """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["caldt"]).reset_index(drop=True)
    db.close()
    return df


def pull_CRSP_treasury_info(wrds_username=WRDS_USERNAME):
    query = """
        SELECT kytreasno, kycrspid, tcusip, tdatdt, tmatdt, tcouprt, itype,
            ROUND((tmatdt - tdatdt) / 365.0) AS term
        FROM crspm.tfz_iss AS iss
        WHERE iss.itype IN (1, 2)
    """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["tdatdt", "tmatdt"]).reset_index(drop=True)
    db.close()
    return df


def pull_CRSP_treasury_consolidated(
    start_date=START_DATE,
    end_date=END_DATE,
    wrds_username=WRDS_USERNAME,
):
    query = f"""
        SELECT
            tfz.kytreasno, tfz.kycrspid, tfz.caldt, tfz.tdbid, tfz.tdask, tfz.tdaccint, tfz.tdyld,
            ((tfz.tdbid + tfz.tdask) / 2.0 + tfz.tdaccint) AS price,
            iss.tcusip, iss.tdatdt, iss.tmatdt, iss.tcouprt, iss.itype,
            ROUND((iss.tmatdt - iss.tdatdt) / 365.0) AS term
        FROM
            crspm.tfz_dly AS tfz
        LEFT JOIN
            crspm.tfz_iss AS iss
        ON
            tfz.kytreasno = iss.kytreasno AND
            tfz.kycrspid = iss.kycrspid
        WHERE
            tfz.caldt BETWEEN '{start_date}' AND '{end_date}'
            AND iss.itype IN (1, 2)
    """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["caldt", "tdatdt", "tmatdt"])
    df = df.reset_index(drop=True)
    df = calc_runness(df)
    db.close()
    return df


def calc_runness(data):
    """
    Calculate runness for the securities issued in 1980 or later.

    This is due to the following condition of Gurkaynak, Sack, and Wright (2007):
        iv) Exclude on-the-run issues and 1st off-the-run issues for 2,3,5,7,
            10, 20, 30 years securities issued in 1980 or later.
    """

    def _calc_runness(df):
        temp = df.sort_values(by=["caldt", "term", "tdatdt"])
        return (
            temp.groupby(["caldt", "term"])["tdatdt"].rank(
                method="first", ascending=False
            )
            - 1
        )

    data_run_ = data[data.caldt >= "1980"]
    runs = _calc_runness(data_run_)
    data["run"] = 0
    data.loc[data_run_.index, "run"] = runs
    return data


def load_CRSP_treasury_daily(data_dir=DATA_DIR):
    path = Path(data_dir) / SUBFOLDER / "CRSP_TFZ_DAILY.parquet"
    df = pd.read_parquet(path)
    return df


def load_CRSP_treasury_info(data_dir=DATA_DIR):
    path = Path(data_dir) / SUBFOLDER / "CRSP_TFZ_INFO.parquet"
    df = pd.read_parquet(path)
    return df


def load_CRSP_treasury_consolidated(data_dir=DATA_DIR):
    path = Path(data_dir) / SUBFOLDER / "CRSP_TFZ_CONSOLIDATED.parquet"
    df = pd.read_parquet(path)
    return df


def _demo():
    df_daily = load_CRSP_treasury_daily()
    df_info = load_CRSP_treasury_info()
    df_consolidated = load_CRSP_treasury_consolidated()


if __name__ == "__main__":
    # Create subfolder
    data_dir = DATA_DIR / SUBFOLDER
    data_dir.mkdir(parents=True, exist_ok=True)

    df_daily = pull_CRSP_treasury_daily(start_date=START_DATE, end_date=END_DATE)
    df_daily.to_parquet(data_dir / "CRSP_TFZ_DAILY.parquet")

    df_info = pull_CRSP_treasury_info()
    df_info.to_parquet(data_dir / "CRSP_TFZ_INFO.parquet")

    df_consolidated = pull_CRSP_treasury_consolidated(
        start_date=START_DATE, end_date=END_DATE
    )
    df_consolidated.to_parquet(data_dir / "CRSP_TFZ_CONSOLIDATED.parquet")
