"""
This scripts pulls the Markit CDS data from WRDS.
Code by Kausthub Kesheva
"""

# Add src directory to Python path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import wrds
from thefuzz import fuzz
import polars as pl

from settings import config

DATA_DIR = Path(config("DATA_DIR")) / "wrds_markit"
WRDS_USERNAME = config("WRDS_USERNAME")
START_DATE = pd.Timestamp("2001-01-01")
END_DATE = pd.Timestamp("2025-01-01")


def get_cds_data_as_dict(wrds_username=WRDS_USERNAME):
    """
    Connects to a WRDS (Wharton Research Data Services) database and fetches Credit Default Swap (CDS) data
    for each year from 2001 to 2023 from tables named `markit.CDS{year}`. The data fetched includes the date,
    ticker, and parspread where the tenor is '5Y' and the country is 'United States'. The fetched data for each
    year is stored in a dictionary with the year as the key. The function finally returns this dictionary.

    Returns:
        dict: A dictionary where each key is a year from 2001 to 2023 and each value is a DataFrame containing
        the date, ticker, and parspread for that year.
    """
    db = wrds.Connection(wrds_username=wrds_username)
    cds_data = {}
    for year in range(2001, 2024):  # Loop from 2001 to 2005
        table_name = f"markit.CDS{year}"  # Generate table name dynamically
        query = f"""
        SELECT DISTINCT
            date, -- The date on which points on a curve were calculated
            ticker, -- The Markit ticker for the organization.
            RedCode, -- The RED Code for identification of the entity. 
            parspread, -- The par spread associated to the contributed CDS curve.
            convspreard, -- The conversion spread associated to the contributed CDS curve.
            tenor,
            country,
            creditdv01, -- If the submission is in par spread, the values will match
            -- those in ContributedLevel(X).
            riskypv01, -- The risky annuity of a trade of the maturity of the CDS
            -- instrument calculated from the CDS Composite curve.
            irdv01, -- The change in the mark to market from a basis point change
            -- in the interest rate
            rec01, -- The change in the mark to market from a change in the
            -- recovery rate by 1 percent
            dp, -- The implied default probability of the reference entity,
            jtd, -- The jump to default of the reference entity. The change in 
            -- mark to market assuming an instantaneous credit event
            dtz -- The jump to zero. The change in the mark to market
            -- assuming an instantaneous credit event and a recovery rate of 0
        FROM
            {table_name}
        WHERE
            -- country = 'United States'
            currency = 'USD' AND
            docclause LIKE 'XR%%' AND 
                -- The documentation clause. Values are: MM (Modified
                -- Modified Restructuring), MR (Modified Restructuring), CR
                -- (Old Restructuring), XR (No Restructuring).
                -- Among all the data, these are the unique values for docclause:
                --  CR, CR14, MM, MM14, MR, MR14, XR, XR14
            CompositeDepth5Y >= 3 AND
            tenor IN ('1Y', '3Y', '5Y', '7Y', '10Y')
        """
        cds_data[year] = db.raw_sql(query, date_cols=["date"])
    # cds_data = cds_data.drop_duplicates()
    return cds_data


def combine_cds_data(cds_data: dict) -> pd.DataFrame:
    """
    Combines the CDS data stored in a dictionary into a single DataFrame.

    For each key-value pair in `cds_data`, a new column "year" is added to the
    DataFrame containing the value of the key (i.e., the year). Then, all
    DataFrames are concatenated.

    Args:
        cds_data (dict): A dictionary where each key is a year and its value is
        a DataFrame with CDS data for that year.

    Returns:
        pd.DataFrame: A single concatenated DataFrame with an additional "year"
        column.
    """
    dataframes = []
    for year, df in cds_data.items():
        # Create a copy to avoid modifying the original DataFrame
        df_with_year = df.copy()
        df_with_year["year"] = year
        dataframes.append(df_with_year)

    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df


def pull_cds_data(wrds_username=WRDS_USERNAME):
    cds_data = get_cds_data_as_dict(wrds_username=wrds_username)
    combined_df = combine_cds_data(cds_data)
    return combined_df


def get_value_counts(variable, wrds_username=WRDS_USERNAME):
    """
    Retrieves all unique values across all Markit CDS tables
    and counts their total frequency of occurrence.
    """
    db = wrds.Connection(wrds_username=wrds_username)
    yearly_counts = []

    for year in range(2001, 2024):
        query = f"""
        SELECT 
            {variable}, 
            COUNT(*) as count
        FROM 
            markit.CDS{year}
        GROUP BY 
            {variable}
        """
        result = db.raw_sql(query)
        yearly_counts.append(result)

    # Concatenate all the yearly counts
    all_counts = pd.concat(yearly_counts)

    # Sum the counts for each docclause across all years
    total_counts = all_counts.groupby(variable)["count"].sum().reset_index()

    return total_counts.sort_values("count", ascending=False)


def pull_markit_red_crsp_link(wrds_username=WRDS_USERNAME):
    """
    Link Markit RED data with CRSP data.

    This returns a table that can be used to link Markit CDS data with CRSP data.
    You'll link the Markit RED Code with the CRSP Permno. It contains a column called flg
    that indicates the type of link. It can be either 'cusip' or 'ticker'.
    When these are matched by ticket, you should double check that the
    company names are roughly the same. You can do this by looking at the nameRatio column,
    which is a fuzzy match between the two company names. A nameRatio of 100 is a perfect match.
    I recommend that you at least require a nameRatio of 50.

    I adapted the code and guidelines from here:
    https://wrds-www.wharton.upenn.edu/pages/wrds-research/database-linking-matrix/linking-markit-with-crsp/

    Identifiers from RED Markit RED (RED) is the market standard for reference data
    in the credit markets. RED provides a unique 6-digit identifier, redcode, for
    each entity in the database. In addition, it also carries several other common
    entity identifiers, such as 6-digit entity_cusip, ticker as well as company name
    strings.

    Researchers can use these identifiers to link the CDS data with other data
    sources, such as CRSP and TRACE for equity and fixed income respectively.

    Connecting with CRSP We illustrate below how to link RED data to CRSP data using
    the new CIZ format of CRSP data. The logic would be the same for the legacy
    SIZ format of CRSP data, just with different database syntax.

    The primary linking key is through the 6-digit CUSIP. We also try to establish
    linkage through a secondary linking key, the ticker. However, it is important to
    emphasize here that the linking quality through ticker is fairly poor. As a
    result, we include an additional layer of quality check using the string
    comparison between the two databases' company names.

    We strongly advise our users to carefully examine the linking output, and set
    their own quality criteria suitable for their individual research agenda.
    """
    conn = wrds.Connection(wrds_username=wrds_username)

    ### Get red entity information
    redent = conn.get_table(library="markit", table="redent")

    # Quick check to confirm that it is the header information
    # i.e. each redcode is mapped to only one entity
    # and doesn't contain historical records
    redcnt = (
        redent.groupby(["redcode"])["entity_cusip"]
        .count()
        .reset_index()
        .rename(columns={"entity_cusip": "cusipCnt"})
    )
    assert (
        redcnt.cusipCnt.max() == 1
    ), "Each redcode should be mapped to only one entity"

    ### Get information from CRSP header table
    crspHdr = conn.raw_sql(
        """SELECT 
            permno, permco, hdrcusip, ticker, issuernm 
        FROM 
            crsp.stksecurityinfohdr
        """
    )
    crspHdr["cusip6"] = crspHdr.hdrcusip.str[:6]
    crspHdr = crspHdr.rename(columns={"ticker": "crspTicker"})

    ### First Route - Link with 6-digit cusip
    _cdscrsp1 = pd.merge(
        redent, crspHdr, how="left", left_on="entity_cusip", right_on="cusip6"
    )

    # store linked results through CUSIP
    _cdscrsp_cusip = _cdscrsp1.loc[_cdscrsp1.permno.notna()].copy()
    _cdscrsp_cusip["flg"] = "cusip"

    # continue to work with non-linked records
    _cdscrsp2 = (
        _cdscrsp1.loc[_cdscrsp1.permno.isna()]
        .copy()
        .drop(
            columns=["permno", "permco", "hdrcusip", "crspTicker", "issuernm", "cusip6"]
        )
    )

    ### Second Route - Link with Ticker
    _cdscrsp3 = pd.merge(
        _cdscrsp2, crspHdr, how="left", left_on="ticker", right_on="crspTicker"
    )
    _cdscrsp_ticker = _cdscrsp3.loc[_cdscrsp3.permno.notna()].copy()
    _cdscrsp_ticker["flg"] = "ticker"
    ### Consolidate Output and Company Name Distance Check
    cdscrsp = pd.concat([_cdscrsp_cusip, _cdscrsp_ticker], ignore_index=True, axis=0)

    # Check similarity ratio of company names
    crspNameLst = cdscrsp.issuernm.str.upper().tolist()
    redNameLst = cdscrsp.shortname.str.upper().tolist()
    # len(crspNameLst), len(redNameLst)

    nameRatio = []  # blank list to store fuzzy ratio

    for i in range(len(redNameLst)):
        ratio = fuzz.partial_ratio(redNameLst[i], crspNameLst[i])
        nameRatio.append(ratio)

    cdscrsp["nameRatio"] = nameRatio
    return cdscrsp


def right_merge_cds_crsp(
    cds_data: pd.DataFrame, cds_crsp_link: pd.DataFrame, ratio_threshold: int = 50
):
    """
    Right merge the CDS data with the CRSP data.
    """
    columns_to_keep = ["redcode", "permno", "permco", "flg", "nameRatio"]
    merged_df = pd.merge(
        cds_data, cds_crsp_link[columns_to_keep], how="right", on="redcode"
    )
    merged_df = merged_df[merged_df["nameRatio"] >= ratio_threshold]
    return merged_df


def load_cds_data(data_dir=DATA_DIR):
    path = data_dir / "markit_cds.parquet"
    return pd.read_parquet(path)


def load_cds_crsp_link(data_dir=DATA_DIR):
    path = data_dir / "markit_red_crsp_link.parquet"
    return pd.read_parquet(path)


def load_cds_subsetted_to_crsp(data_dir=DATA_DIR):
    path = data_dir / "markit_cds_subsetted_to_crsp.parquet"
    return pd.read_parquet(path)


def _demo():
    cds_data = load_cds_data(data_dir=DATA_DIR)
    cds_data.info()

    cds_crsp_link = load_cds_crsp_link(data_dir=DATA_DIR)
    cds_crsp_link.info()

    cds_crsp_merged = load_cds_subsetted_to_crsp(data_dir=DATA_DIR)
    cds_crsp_merged.info()

    # Call the function and display results
    unique_clauses = get_value_counts("docclause", wrds_username=WRDS_USERNAME)
    print(unique_clauses)  # CR, CR14, MM, MM14, MR, MR14, XR, XR14
    # docclause      count
    # 5      MR14  248223660
    # 1      CR14  244073801
    # 3      MM14  229572235
    # 7      XR14  188329844
    # 0        CR   47921059
    # 2        MM   46839107
    # 4        MR   13846587
    # 6        XR    4535354
    value_counts = get_value_counts("batch", wrds_username=WRDS_USERNAME)
    print(value_counts)
    # batch       count
    # 0   EOD  1023341647

    ## Explore quotes
    db = wrds.Connection(wrds_username=WRDS_USERNAME)
    year = 2021
    table_name = f"markit.CDS{year}"  # Generate table name dynamically
    query = f"""
        SELECT DISTINCT
            date, -- The date on which points on a curve were calculated
            ticker, -- The Markit ticker for the organization.
            RedCode, -- The RED Code for identification of the entity. 
            parspread, -- The par spread associated to the contributed CDS curve.
            convspreard, -- The conversion spread associated to the contributed CDS curve.
            tenor,
            country,
            quotesdepthcontr,
            quotesdepthpassed,
            dealersclearingcountcruve,
            dealersquotescountcurve,
            dealersquotescountcurve1wma,
            dealersquotescountcurve1mma,
            dealersquotescounttenor,
            quotescountcurve,
            quotescountcurve1wma,
            quotescountcurve1mma,
            quotescounttenor,
            CompositeDepth5Y,
            creditdv01, -- If the submission is in par spread, the values will match
            -- those in ContributedLevel(X).
            riskypv01, -- The risky annuity of a trade of the maturity of the CDS
            -- instrument calculated from the CDS Composite curve.
            irdv01, -- The change in the mark to market from a basis point change
            -- in the interest rate
            rec01, -- The change in the mark to market from a change in the
            -- recovery rate by 1 percent
            dp, -- The implied default probability of the reference entity,
            jtd, -- The jump to default of the reference entity. The change in 
            -- mark to market assuming an instantaneous credit event
            dtz -- The jump to zero. The change in the mark to market
            -- assuming an instantaneous credit event and a recovery rate of 0
        FROM
            {table_name}
        WHERE
            -- country = 'United States'
            currency = 'USD' AND
            docclause LIKE 'XR%%' AND 
                -- The documentation clause. Values are: MM (Modified
                -- Modified Restructuring), MR (Modified Restructuring), CR
                -- (Old Restructuring), XR (No Restructuring).
                -- Among all the data, these are the unique values for docclause:
                --  CR, CR14, MM, MM14, MR, MR14, XR, XR14
            CompositeDepth5Y >= 3 AND
            tenor IN ('1Y', '3Y', '5Y', '7Y', '10Y')
        LIMIT 100
        """
    df = db.raw_sql(query, date_cols=["date"])

    df = pl.from_pandas(df)
    df.glimpse()


if __name__ == "__main__":
    cds_data = pull_cds_data(wrds_username=WRDS_USERNAME)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cds_data.to_parquet(DATA_DIR / "markit_cds.parquet")

    cds_crsp_link = pull_markit_red_crsp_link(wrds_username=WRDS_USERNAME)
    cds_crsp_link.to_parquet(DATA_DIR / "markit_red_crsp_link.parquet")

    cds_crsp_merged = right_merge_cds_crsp(cds_data, cds_crsp_link, ratio_threshold=50)
    cds_crsp_merged.to_parquet(DATA_DIR / "markit_cds_subsetted_to_crsp.parquet")
