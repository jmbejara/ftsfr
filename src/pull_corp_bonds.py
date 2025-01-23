import os
from pathlib import Path

import pandas as pd
import requests

from settings import config

DATA_DIR = config("DATA_DIR")
MIN_N_ROWS_EXPECTED = 500

SUBFOLDER = "us_corp_bonds"
DATA_INFO = {
    "Treasury Bond Returns": {
        "url": "https://openbondassetpricing.com/wp-content/uploads/2024/06/bondret_treasury.csv",
        "csv": "bondret_treasury.csv",
        "parquet": "treasury_bond_returns.parquet",
        "readme": "https://openbondassetpricing.com/wp-content/uploads/2024/06/BNS_README.pdf",
    },
    "Corporate Bond Returns": {
        "url": "https://openbondassetpricing.com/wp-content/uploads/2024/07/WRDS_MMN_Corrected_Data_2024_July.csv",
        "csv": "WRDS_MMN_Corrected_Data.csv",
        "parquet": "corporate_bond_returns.parquet",
        "readme": "https://openbondassetpricing.com/wp-content/uploads/2024/07/DRR-README.pdf",
    },
}


def _demo():
    df_treasury_bond_returns = pd.read_parquet(
        DATA_DIR / SUBFOLDER / "treasury_bond_returns.parquet"
    )
    df_treasury_bond_returns.info()
    df_corporate_bond_returns = pd.read_parquet(
        DATA_DIR / SUBFOLDER / "corporate_bond_returns.parquet"
    )


def download_file(url, output_path):
    """
    Downloads a file from the given URL.

    Parameters:
        url (str): URL to the file to download.
        output_path (Path): Path where the file should be saved.

    Returns:
        Path: Path to the downloaded file.
    """
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


def download_data(url, csv, data_dir=DATA_DIR):
    """
    Downloads data from the given URL.

    Parameters:
        url (str): URL to the CSV file containing the data.
        csv (str): Name of the CSV file to save.
        data_dir (Path): Path to the directory where data will be saved.

    Returns:
        Path: Path to the downloaded CSV file.
    """
    return download_file(url, data_dir / csv)


def load_data_into_dataframe(csv_path: Path, check_n_rows: bool = True):
    """
    Loads the CSV file into a Pandas DataFrame.

    Parameters:
        csv_path (Path): Path to the CSV file.
        check_n_rows (bool): Whether to check for minimum number of rows.

    Returns:
        pd.DataFrame: DataFrame containing the bond data.
    """
    df = pd.read_csv(csv_path)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    if check_n_rows:
        if len(df) < MIN_N_ROWS_EXPECTED:
            raise ValueError(
                f"Expected at least {MIN_N_ROWS_EXPECTED} rows, but found {len(df)}. "
                + "Validate the csv file or set 'check_n_rows=False'."
            )

    return df


if __name__ == "__main__":
    for dataset, info in DATA_INFO.items():
        data_dir = DATA_DIR / SUBFOLDER
        data_dir.mkdir(parents=True, exist_ok=True)

        # Download and process data file
        csv_path = download_data(info["url"], info["csv"], data_dir=data_dir)
        df = load_data_into_dataframe(csv_path)
        df.to_parquet(data_dir / info["parquet"])
        os.remove(csv_path)

        # Download README file
        readme_filename = f"{info['parquet'].replace('.parquet', '_README.pdf')}"
        download_file(info["readme"], data_dir / readme_filename)
