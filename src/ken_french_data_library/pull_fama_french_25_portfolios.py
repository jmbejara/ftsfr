import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import zipfile
from pathlib import Path

import pandas as pd
import requests

from settings import config

DATA_DIR = config("DATA_DIR")
MIN_N_ROWS_EXPECTED = 500

DATA_INFO = {
    "Size and Book-to-Market": {
        "url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_5x5_CSV.zip",
        "zip": "25_Portfolios_5x5_CSV.zip",
        "csv": "25_Portfolios_5x5.csv",
        "parquet": "french_portfolios_25_monthly_size_and_bm.parquet",
    },
    "Size and Book-to-Market Daily": {
        "url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_5x5_Daily_CSV.zip",
        "zip": "25_Portfolios_5x5_Daily_CSV.zip",
        "csv": "25_Portfolios_5x5_Daily.csv",
        "parquet": "french_portfolios_25_daily_size_and_bm.parquet",
    },
    "Size and Operating Profitability": {
        "url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_ME_OP_5x5_CSV.zip",
        "zip": "25_Portfolios_ME_OP_5x5_CSV.zip",
        "csv": "25_Portfolios_ME_OP_5x5.csv",
        "parquet": "french_portfolios_25_monthly_size_and_op.parquet",
    },
    "Size and Operating Profitability Daily": {
        "url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_ME_OP_5x5_daily_CSV.zip",
        "zip": "25_Portfolios_ME_OP_daily_CSV.zip",
        "csv": "25_Portfolios_ME_OP_5x5_daily.csv",
        "parquet": "french_portfolios_25_daily_size_and_op.parquet",
    },
    "Size and Investment": {
        "url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_ME_INV_5x5_CSV.zip",
        "zip": "25_Portfolios_ME_INV_5x5_CSV.zip",
        "csv": "25_Portfolios_ME_INV_5x5.csv",
        "parquet": "french_portfolios_25_monthly_size_and_inv.parquet",
    },
    "Size and Investment Daily": {
        "url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_ME_INV_5x5_daily_CSV.zip",
        "zip": "25_Portfolios_ME_INV_daily_CSV.zip",
        "csv": "25_Portfolios_ME_INV_5x5_daily.csv",
        "parquet": "french_portfolios_25_daily_size_and_inv.parquet",
    },
}


def download_and_extract_data(url, zip, csv, data_dir=DATA_DIR):
    """
    Downloads and extracts the Fama-French 25 Portfolios 5x5 data from the given URL.

    Parameters:
        url (str): URL to the zip file containing the data.
        data_dir (Path): Path to the directory where data will be saved.

    Returns:
        str: Path to the extracted CSV file.
    """
    zip_path = data_dir / zip
    extracted_csv_path = data_dir / csv

    response = requests.get(url)
    response.raise_for_status()
    with open(zip_path, "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(data_dir)

    # Check if the file was extracted with uppercase extension, change to lowercase
    # Some of the Ken French files have .CSV as an extension instead of .csv
    uppercase_csv_path = data_dir / csv.upper()
    if uppercase_csv_path.exists():
        uppercase_csv_path.rename(extracted_csv_path)

    return extracted_csv_path


def load_data_into_dataframe(
    csv_path: Path, equal_weighted: bool = False, check_n_rows: bool = True
):
    """
    Loads the extracted CSV file into a Pandas DataFrame, dynamically starting
    after the specified title and optionally filtering the Equal Weighted section.

    Parameters:
        csv_path (str): Path to the extracted CSV file.
        equal_weighted (bool): Whether to filter for the Equal Weighted section.

    Returns:
        pd.DataFrame: DataFrame containing the filtered Fama-French data.
    """

    with open(csv_path, "r") as f:
        lines = f.readlines()

    start_index = (
        next(
            i
            for i, line in enumerate(lines)
            if "Average Value Weighted Returns" in line
        )
        + 1
    )

    df = pd.read_csv(csv_path, skiprows=start_index, engine="python")

    df = df.rename({"Unnamed: 0": "date"}, axis=1).reset_index(drop=True)

    separation_index = df[
        df.iloc[:, 0].str.contains("Average Equal Weighted", na=False)
    ].index[0]

    if equal_weighted:
        df = df.iloc[(separation_index + 1) :]
    else:
        df = df.iloc[:separation_index]

    df.columns = [col.strip() for col in df.columns]
    df["date"] = df["date"].str.strip()

    if "daily" in csv_path.name.lower():
        df["date"] = pd.to_datetime(df["date"], format="%Y%m%d", errors="coerce")
    else:
        df["date"] = pd.to_datetime(df["date"], format="%Y%m", errors="coerce")
    df = df.dropna(subset=["date"])

    if check_n_rows:
        if len(df.date) < MIN_N_ROWS_EXPECTED:
            raise ValueError(
                f"Expected at least {MIN_N_ROWS_EXPECTED} rows, but found {len(df.date)}. "
                + "Validate the csv file or set 'check_n_rows=False'."
            )

    return df.set_index("date").apply(lambda df: df.astype(float) / 100).reset_index()


def save_dataframe_to_parquet(
    df, parquet_name, data_dir=DATA_DIR, equal_weighted=False
):
    """
    Saves the DataFrame to a Parquet file.

    Parameters:
        df (pd.DataFrame): The DataFrame to save.
        data_dir (Path): Directory where the Parquet file will be saved.
    """
    if equal_weighted:
        parquet_name = parquet_name.replace(".parquet", "_equal_weighted.parquet")

    output_path = data_dir / parquet_name
    df.to_parquet(output_path)


if __name__ == "__main__":
    for port, info in DATA_INFO.items():
        data_dir = DATA_DIR
        data_dir.mkdir(parents=True, exist_ok=True)
        csv_path = download_and_extract_data(
            info["url"], info["zip"], info["csv"], data_dir=data_dir
        )
        for equal_weighted in [False, True]:
            df = load_data_into_dataframe(csv_path, equal_weighted=equal_weighted)
            if df.date.value_counts().loc[lambda x: x > 1].any():
                print(
                    f"Duplicate dates found in {port} data with equal_weighted={str(equal_weighted)}."
                )
                continue
            save_dataframe_to_parquet(
                df, info["parquet"], data_dir=data_dir, equal_weighted=equal_weighted
            )
        os.remove(data_dir / info["csv"])
        os.remove(data_dir / info["zip"])
