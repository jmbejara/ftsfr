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

from datetime import datetime
from pathlib import Path

import pandas as pd
import wrds

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")


def pull_CRSP_treasury_daily(
    start_date="1970-01-01",
    end_date="2023-12-31",
    wrds_username=WRDS_USERNAME,
):
    """Pull daily CRSP Treasury data from WRDS within the specified date range.

    This function queries the CRSP Treasury database's daily time series (tfz_dly)
    table for the specified date range.

    Parameters
    ----------
    start_date : str
        Start date for the query in 'YYYY-MM-DD' format.
    end_date : str
        End date for the query in 'YYYY-MM-DD' format.
    wrds_username : str
        WRDS username to use for the connection.

    Returns
    -------
    pd.DataFrame
        DataFrame containing daily CRSP Treasury data with the following columns:

        - kytreasno: Treasury record identifier
        - kycrspid: CRSP-assigned unique ID
        - caldt: Quotation date
        - tdbid: Daily bid price (clean)
        - tdask: Daily ask price (clean)
        - tdaccint: Daily series of total accrued interest
        - tdyld: Daily series of promised daily yield
        - price: Calculated as ((tdbid + tdask) / 2.0 + tdaccint), the dirty price
        - tdduratn: Duration (price sensitivity to yield changes)
        - tdretnua: Unadjusted return (use as holding period return)
        - tdpubout: Publicly Held Face Value Outstanding integer
        - tdtotout: Face Value Outstanding integer
        - pdint: Interest Paid on the interest payment date

    Notes
    -----
    Field Details:
    - tdretnua: Unadjusted return, which represents the simple price change plus accrued interest
    - tdpubout: Publicly Held Face Value Outstanding, the amount (face value) held by the public
      in millions of dollars
    - tdtotout: Face Value Outstanding, the total amount (face value) issued and still outstanding
      in millions of dollars
    - pdint: Interest Paid on the interest payment date
    """
    query = f"""
    SELECT 
        kytreasno, kycrspid, caldt, tdbid, tdask, tdaccint, tdyld,
        ((tdbid + tdask) / 2.0 + tdaccint) AS price,
        tdduratn, 
        tdretnua,
        tdpubout,
        tdtotout,
        tdpdint
    FROM 
        crspm.tfz_dly
    WHERE 
        caldt BETWEEN '{start_date}' AND '{end_date}'
    """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["caldt"])
    db.close()
    return df


def pull_CRSP_treasury_info(wrds_username=WRDS_USERNAME):
    """Pull Treasury issue information from CRSP.

    This function queries the CRSP Treasury database's issue information (tfz_iss) table
    for bonds and notes (itype 1 or 2).

    Parameters
    ----------
    wrds_username : str
        WRDS username to use for the connection.

    Returns
    -------
    pd.DataFrame
        DataFrame containing Treasury issue information with the following columns:

        - kytreasno: Treasury record identifier
        - kycrspid: CRSP-assigned unique ID
        - tcusip: Treasury CUSIP identifier
        - tdatdt: Date dated by Treasury (YYYYMMDD Format)
        - tmatdt: Maturity date at time of issue
        - tcouprt: Coupon rate
        - itype: Type of issue (1: noncallable bonds, 2: noncallable notes)
        - original_maturity: Calculated original maturity at issuance (in years)

    Notes
    -----
    DATDT: Date Dated by Treasury, in YYYYMMDD Format integer
        Coupon issues accrue interest beginning on the dated date. This may result in a modified first
        coupon payment if the dated date is not a regular interest payment date.
        DATDT is 0 if it is not available or not applicable, as is the case with Treasury bills.
    """
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
    """Calculate the 'runness' measure for Treasury securities.

    'Runness' refers to how recently a Treasury security was issued relative to
    other securities with similar maturities. This is important because the most
    recently issued securities ('on-the-run') often trade at a premium compared
    to older issues ('off-the-run') due to their higher liquidity.

    This function calculates the runness ranking, where:
    - 0 = on-the-run (most recently issued)
    - 1 = first off-the-run
    - 2 = second off-the-run
    - etc.

    The calculation follows Gurkaynak, Sack, and Wright (2007) methodology:
    - Security runness is calculated for securities issued in 1980 or later
    - For each date and original maturity, securities are ranked by issue date

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing Treasury data with at least 'caldt', 'original_maturity',
        and 'tdatdt' columns.

    Returns
    -------
    pd.DataFrame
        Input DataFrame with an additional 'run' column indicating the runness
        of each security. On-the-run securities have run=0, first off-the-run
        have run=1, etc.

    Notes
    -----
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

    This function joins daily Treasury quotes (tfz_dly) with Treasury issue information (tfz_iss),
    returning a comprehensive dataset with identifiers, dates, prices, and security characteristics.

    Parameters
    ----------
    start_date : str
        Start date for the query in 'YYYY-MM-DD' format.
    end_date : str
        End date for the query in 'YYYY-MM-DD' format.
    wrds_username : str
        WRDS username to use for the connection.

    Returns
    -------
    pd.DataFrame
        DataFrame containing consolidated Treasury data with the following columns:

        Identification Fields:
        - kytreasno: Treasury record identifier
        - kycrspid: CRSP-assigned unique ID
        - tcusip: Treasury CUSIP identifier

        Date Fields:
        - caldt: Quote date (date of price observation)
        - tdatdt: Date dated (original issue date when interest starts accruing)
        - tmatdt: Maturity date (when principal is repaid)
        - tfcaldt: First call date (0 if not callable)

        Price and Yield Fields:
        - tdbid: Bid price (clean)
        - tdask: Ask price (clean)
        - tdaccint: Accrued interest since last coupon
        - tdyld: Bond equivalent yield
        - price: Dirty price (clean price + accrued interest)

        Outstanding Amount Fields:
        - tdpubout: Publicly held face value outstanding (in millions of dollars)
        - tdtotout: Face value outstanding in total (in millions of dollars)
        - dqdate: Effective date of amount outstanding values in YYYYMMDD format

        Interest Fields:
        - pdint: Interest paid on the interest payment date

        Issue Characteristics:
        - tcouprt: Coupon rate (annual)
        - itype: Type of issue (1: bonds, 2: notes)
        - original_maturity: Original maturity at issuance (in years)
        - years_to_maturity: Remaining time to maturity (in years)

        Trading Information:
        - tdduratn: Duration (price sensitivity to yield changes)
        - tdretnua: Return (unadjusted) - simple price change + accrued interest
        - days_to_maturity: Calculated days to maturity (derived field)
        - callable: Boolean indicating if the security is callable (derived field)

    Notes
    -----
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

    Field Details:
    DQDATE: Effective Date of Amount Outstanding Values in YYYYMMDD Format

    TOTOUT: Face Value Outstanding integer
        Amount (face value) issued and still outstanding in millions of dollars. Set to 0 for unknown
        values up to December 31, 1961 and set to -1 for unknown values thereafter.

    tdpubout: Publicly Held Face Value Outstanding integer
        Amount (face value) held by the public in millions of dollars. This is the total amount
        outstanding (TOTOUT) minus the amount held in U.S. Government accounts and Federal Reserve
        Banks. This amount is not available for Treasury Bills and is always set to 0. For other issues,
        set to 0 for unknown values up to December 31, 1961 and set to -1 for unavailable values after
        December 31, 1961. After December 31, 1982, these numbers are reported quarterly instead of
        monthly, and the reported values are carried forward the next two months.

    PDINT: Interest Paid real*8
        PDINT is the coupon payable on the interest payment date.
    """

    query = f"""
    SELECT 
        tfz.kytreasno, tfz.kycrspid, iss.tcusip,
        tfz.caldt,
        iss.tdatdt,
        iss.tmatdt,
        iss.tfcaldt,
        tfz.tdbid,
        tfz.tdask,
        tfz.tdaccint,
        tfz.tdyld,
        ((tfz.tdbid + tfz.tdask) / 2.0 + tfz.tdaccint) AS price,
        tfz.tdpubout,
        tfz.tdtotout,
        tfz.tdpdint,
        iss.tcouprt,
        iss.itype,
        ROUND((iss.tmatdt - iss.tdatdt) / 365.0) AS original_maturity,
        ROUND((iss.tmatdt - tfz.caldt) / 365.0) AS years_to_maturity,
        tfz.tdduratn,
        tfz.tdretnua
    FROM 
        crspm.tfz_dly AS tfz
    LEFT JOIN 
        crspm.tfz_iss AS iss 
    ON 
        tfz.kytreasno = iss.kytreasno AND 
        tfz.kycrspid = iss.kycrspid
    WHERE 
        tfz.caldt BETWEEN '{start_date}' AND '{end_date}' AND 
        iss.itype IN (1, 2)
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
    """Load daily CRSP Treasury data from a Parquet file.

    Parameters
    ----------
    data_dir : Path or str
        Directory where the Parquet file is stored

    Returns
    -------
    pd.DataFrame
        DataFrame containing daily CRSP Treasury data. See pull_CRSP_treasury_daily
        docstring for details on the columns.
    """
    path = data_dir / "CRSP_TFZ_DAILY.parquet"
    df = pd.read_parquet(path)
    return df


def load_CRSP_treasury_info(data_dir=DATA_DIR):
    """Load CRSP Treasury issue information from a Parquet file.

    Parameters
    ----------
    data_dir : Path or str
        Directory where the Parquet file is stored

    Returns
    -------
    pd.DataFrame
        DataFrame containing Treasury issue information. See pull_CRSP_treasury_info
        docstring for details on the columns.
    """
    path = data_dir / "CRSP_TFZ_INFO.parquet"
    df = pd.read_parquet(path)
    return df


def load_CRSP_treasury_consolidated(data_dir=DATA_DIR, with_runness=True):
    """Load consolidated CRSP Treasury data from a Parquet file.

    Parameters
    ----------
    data_dir : Path or str
        Directory where the Parquet file is stored
    with_runness : bool, default=True
        If True, load the file with runness information included.
        If False, load the file without runness information.

    Returns
    -------
    pd.DataFrame
        DataFrame containing consolidated Treasury data. See pull_CRSP_treasury_consolidated
        docstring for details on the columns. If with_runness=True, also includes a 'run'
        column indicating the runness measure for each security.
    """
    if with_runness:
        path = data_dir / "CRSP_TFZ_with_runness.parquet"
    else:
        path = data_dir / "CRSP_TFZ_consolidated.parquet"
    df = pd.read_parquet(path)
    return df


def _demo():
    DATA_DIR = Path(config("DATA_DIR")) / "us_treasury_returns"
    df = load_CRSP_treasury_daily(data_dir=DATA_DIR)
    df.info()
    df = load_CRSP_treasury_info(data_dir=DATA_DIR)
    df.info()
    df = load_CRSP_treasury_consolidated(data_dir=DATA_DIR)
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
    path = DATA_DIR / "CRSP_TFZ_DAILY.parquet"
    df.to_parquet(path)

    df = pull_CRSP_treasury_info(wrds_username=WRDS_USERNAME)
    path = DATA_DIR / "CRSP_TFZ_INFO.parquet"
    df.to_parquet(path)

    df = pull_CRSP_treasury_consolidated(wrds_username=WRDS_USERNAME)
    path = DATA_DIR / "CRSP_TFZ_consolidated.parquet"
    df.to_parquet(path)

    df = calc_runness(df)
    path = DATA_DIR / "CRSP_TFZ_with_runness.parquet"
    df.to_parquet(path)
