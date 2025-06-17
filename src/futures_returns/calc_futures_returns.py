import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import polars as pl

import pull_wrds_futures
from settings import config

DATA_DIR = config("DATA_DIR")


def calc_futures_returns(data_dir=DATA_DIR):
    df = pull_wrds_futures.load_combined_futures_data(data_dir=data_dir, format="pandas")
    # TODO
    return df


if __name__ == "__main__":
    df = calc_futures_returns(data_dir=DATA_DIR)
    path = DATA_DIR / "futures_returns.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path)