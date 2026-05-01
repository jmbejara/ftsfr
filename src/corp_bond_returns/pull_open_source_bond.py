import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import zipfile
from io import BytesIO

import pandas as pd
import requests

from settings import config

DATA_DIR = config("DATA_DIR")
MIN_N_ROWS_EXPECTED = 500


DATA_INFO = {
    "Treasury Bond Returns": {
        "url": "https://openbondassetpricing.com/wp-content/uploads/2024/06/bondret_treasury.csv",
        "source_format": "csv",
        "csv": "bondret_treasury.csv",
        "parquet": "treasury_bond_returns.parquet",
        "readme": "https://openbondassetpricing.com/wp-content/uploads/2024/06/BNS_README.pdf",
    },
    "Corporate Bond Returns": {
        "url": "https://openbondassetpricing.com/wp-content/uploads/2026/01/osbap_main_data_2025_public_beta.zip",
        "source_format": "zip_parquet",
        "zip_contents": "main_panel_2025.parquet",
        "parquet": "corporate_bond_returns.parquet",
        "readme_contents": "README.txt",
        "readme_file": "corporate_bond_returns_README.txt",
    },
}


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


def download_and_extract_zip_parquet(url, data_dir, expected_parquet, expected_readme=None):
    """
    Downloads a ZIP file and extracts the parquet (and optionally README).

    Parameters:
        url (str): URL to the ZIP file.
        data_dir (Path): Directory to extract files to.
        expected_parquet (str): Expected parquet filename inside ZIP.
        expected_readme (str): Expected README filename inside ZIP (optional).

    Returns:
        tuple: (parquet_path, readme_path) - paths to extracted files.
    """
    print(f"Downloading from {url}...")
    response = requests.get(url, timeout=600)
    response.raise_for_status()

    print("Extracting ZIP contents...")
    zip_file = BytesIO(response.content)
    readme_path = None

    with zipfile.ZipFile(zip_file, "r") as zf:
        if expected_parquet not in zf.namelist():
            available = ", ".join(zf.namelist())
            raise ValueError(
                f"Expected {expected_parquet} not found in ZIP. "
                f"Available files: {available}"
            )
        zf.extract(expected_parquet, data_dir)
        parquet_path = data_dir / expected_parquet

        if expected_readme and expected_readme in zf.namelist():
            zf.extract(expected_readme, data_dir)
            readme_path = data_dir / expected_readme

    return parquet_path, readme_path


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


def load_treasury_returns(data_dir=DATA_DIR):
    return pd.read_parquet(data_dir / "treasury_bond_returns.parquet")


def load_corporate_bond_returns(data_dir=DATA_DIR):
    return pd.read_parquet(data_dir / "corporate_bond_returns.parquet")


def _demo():
    treas = pd.read_parquet(DATA_DIR / "treasury_bond_returns.parquet")
    treas.info()
    treas.head()

    bonds = pd.read_parquet(DATA_DIR / "corporate_bond_returns.parquet")
    bonds.info()
    bonds.head()


if __name__ == "__main__":
    for dataset, info in DATA_INFO.items():
        data_dir = DATA_DIR
        data_dir.mkdir(parents=True, exist_ok=True)

        source_format = info.get("source_format", "csv")
        print(f"\n--- Pulling {dataset} ---")

        if source_format == "csv":
            # Download and process CSV file
            csv_path = download_data(info["url"], info["csv"], data_dir=data_dir)
            df = load_data_into_dataframe(csv_path)
            df.to_parquet(data_dir / info["parquet"])
            os.remove(csv_path)

            # Download README file
            readme_filename = f"{info['parquet'].replace('.parquet', '_README.pdf')}"
            download_file(info["readme"], data_dir / readme_filename)

        elif source_format == "zip_parquet":
            # Download and extract ZIP containing parquet
            extracted_parquet, extracted_readme = download_and_extract_zip_parquet(
                url=info["url"],
                data_dir=data_dir,
                expected_parquet=info["zip_contents"],
                expected_readme=info.get("readme_contents"),
            )

            # Validate row count
            df = pd.read_parquet(extracted_parquet)
            if len(df) < MIN_N_ROWS_EXPECTED:
                raise ValueError(
                    f"Expected at least {MIN_N_ROWS_EXPECTED} rows, but found {len(df)}. "
                    "Data file may be corrupted or incomplete."
                )

            # Rename to final parquet name if different
            final_parquet_path = data_dir / info["parquet"]
            if extracted_parquet != final_parquet_path:
                extracted_parquet.rename(final_parquet_path)
            print(f"Saved to {final_parquet_path}")

            # Rename README if present
            if extracted_readme and "readme_file" in info:
                final_readme_path = data_dir / info["readme_file"]
                if extracted_readme != final_readme_path:
                    extracted_readme.rename(final_readme_path)
                print(f"Saved README to {final_readme_path}")

    print("\nDone!")
