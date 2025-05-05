"""
This script pulls the open source bond data from the Open Bond Asset Pricing website.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import polars as pl
import requests

from settings import config

DATA_DIR = Path(config("DATA_DIR"))


def download_file(data_dir=DATA_DIR):
    url_path = "https://openbondassetpricing.com/wp-content/uploads/2024/06/bondret_treasury.csv"
    file_name = "bondret_treasury.csv"
    destination_path = data_dir / file_name
    data_dir.mkdir(parents=True, exist_ok=True)
    response = requests.get(url_path)
    with open(destination_path, "wb") as file:
        file.write(response.content)


def format_bond_data(data_dir=DATA_DIR):
    file_name = "bondret_treasury.csv"
    df = pl.read_csv(data_dir / file_name)
    df = df.rename({"DATE": "date_int"})
    # convert date_int (20020731) to date type
    df = df.with_columns(
        date=pl.col("date_int").cast(str).str.strptime(pl.Date, "%Y%m%d")
    )
    df = df.drop("date_int")
    return df


def load_bond_data(data_dir=DATA_DIR):
    file_name = "bondret_treasury.parquet"
    df = pl.read_parquet(data_dir / file_name)
    return df


if __name__ == "__main__":
    download_file(data_dir=DATA_DIR)
    df = format_bond_data(data_dir=DATA_DIR)
    df.write_parquet(DATA_DIR / "bondret_treasury.parquet")
