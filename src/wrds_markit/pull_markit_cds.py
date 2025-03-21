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

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_DATE = pd.Timestamp("1925-01-01")
END_DATE = pd.Timestamp("2024-01-01")


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
        SELECT
            date, -- The date on which points on a curve were calculated
            ticker, -- The Markit ticker for the organization.
            RedCode, -- The RED Code for identification of the entity. 
            parspread, -- The par spread associated to the contributed CDS curve.
            convspreard, -- The conversion spread associated to the contributed CDS curve.
            tenor
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
            tenor IN ('1Y', '3Y', '5Y', '7Y', '10Y')
        """
        cds_data[year] = db.raw_sql(query, date_cols=["date"])
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


def load_cds_data(data_dir=DATA_DIR):
    path = data_dir / "markit_cds.parquet"
    return pd.read_parquet(path)


def get_unique_doc_clauses(wrds_username=WRDS_USERNAME):
    """
    -- The documentation clause. Values are: MM (Modified
    -- Modified Restructuring), MR (Modified Restructuring), CR
    -- (Old Restructuring), XR (No Restructuring).
    -- Among all the data, these are the unique values for docclause:
    --  CR, CR14, MM, MM14, MR, MR14, XR, XR14
    """
    db = wrds.Connection(wrds_username=wrds_username)

    # The SQL query as defined above
    query = """
    WITH all_doc_clauses AS (
        SELECT DISTINCT docclause FROM markit.CDS2001
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2002
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2003
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2004
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2005
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2006
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2007
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2008
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2009
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2010
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2011
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2012
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2013
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2014
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2015
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2016
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2017
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2018
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2019
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2020
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2021
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2022
        UNION
        SELECT DISTINCT docclause FROM markit.CDS2023
    )
    SELECT DISTINCT
        docclause
    FROM 
        all_doc_clauses
    GROUP BY 
        docclause
    ORDER BY 
        docclause;
    """

    result = db.raw_sql(query)
    return result


def _demo():
    # Call the function and display results
    unique_clauses = get_unique_doc_clauses()
    print(unique_clauses)  # CR, CR14, MM, MM14, MR, MR14, XR, XR14


if __name__ == "__main__":
    combined_df = pull_cds_data(wrds_username=WRDS_USERNAME)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    combined_df.to_parquet(DATA_DIR / "markit_cds.parquet")
