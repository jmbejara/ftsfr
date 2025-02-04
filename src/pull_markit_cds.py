"""
This scripts pulls the Markit CDS data from WRDS.
Code by Kausthub Kesheva
"""

from pathlib import Path

import pandas as pd
import wrds

from settings import config

SUBFOLDER = "markit_cds"
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
            date, ticker, parspread
        FROM
            {table_name} a
        WHERE
            a.tenor = '5Y' AND
            a.country = 'United States'
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


if __name__ == "__main__":
    combined_df = pull_cds_data(wrds_username=WRDS_USERNAME)
    (DATA_DIR / SUBFOLDER).mkdir(parents=True, exist_ok=True)
    combined_df.to_parquet(DATA_DIR / SUBFOLDER / "markit_cds.parquet")
