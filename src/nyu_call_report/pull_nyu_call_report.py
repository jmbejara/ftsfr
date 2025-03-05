"""
Download, unzip, and format the NYU Call Report data found here:
https://pages.stern.nyu.edu/~pschnabl/data/data_callreport.htm

The data dictionary alongside the source code
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

from settings import config

# Set SUBFOLDER to the folder containing this file
SUBFOLDER = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = config("DATA_DIR")


def pull_nyu_call_report(
    data_dir=DATA_DIR, subfolder=SUBFOLDER, delete_temp_files=True
):
    # Download the file
    url = "https://pages.stern.nyu.edu/~pschnabl/research/callreports_1976_2020_WRDS.dta.zip"
    zip_path = data_dir / subfolder / "callreports_1976_2020_WRDS.dta.zip"
    os.makedirs(data_dir / subfolder, exist_ok=True)
    urllib.request.urlretrieve(url, zip_path)

    # Unzip the file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(data_dir / subfolder)

    # Load the file into a pandas dataframe
    data_path = data_dir / subfolder / "callreports_1976_2020_WRDS.dta"
    df = pd.read_stata(data_path)

    if delete_temp_files:
        os.remove(zip_path)
        os.remove(data_path)

    columns_to_convert_to_int = [
        "rssdid",
        "chartertype",
        "cert",
        "bhcid",
        "date",
        "year",
        "month",
        "quarter",
        "day",
    ]
    df[columns_to_convert_to_int] = (
        df[columns_to_convert_to_int].fillna(99999).astype("int")
    )
    df[columns_to_convert_to_int] = df[columns_to_convert_to_int].astype("str")
    df[columns_to_convert_to_int] = df[columns_to_convert_to_int].replace(
        "99999", pd.NA
    )

    # df[columns_to_convert_to_int].info()
    # df[columns_to_convert_to_int].head()
    # df[columns_to_convert_to_int].isna().sum()

    return df


def load_nyu_call_report(data_dir=DATA_DIR, subfolder=SUBFOLDER):
    parquet_path = data_dir / subfolder / "nyu_call_report.parquet"
    df = pd.read_parquet(parquet_path)
    return df


def _demo():
    df = load_nyu_call_report()
    df.head()
    df.info(verbose=True)


if __name__ == "__main__":
    df = pull_nyu_call_report(data_dir=DATA_DIR, subfolder=SUBFOLDER)
    # Save the dataframe as a parquet file
    destination_dir = DATA_DIR / SUBFOLDER
    os.makedirs(destination_dir, exist_ok=True)
    parquet_path = destination_dir / "nyu_call_report.parquet"
    df.to_parquet(parquet_path)
