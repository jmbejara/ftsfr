"""
This is a temporary file used to load all the necessary data.
It can be added to the pull-file once the dataset to use has been determined.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from io import BytesIO

import pandas as pd
import requests

from settings import config

DATA_DIR = config("DATA_DIR") / "futures_returns"


def load_wrds_futures(data_dir=DATA_DIR):
    path = data_dir / "wrds_futures.parquet"
    return pd.read_parquet(path)


def load_wrds_cseries_info(data_dir=DATA_DIR):
    path = data_dir / "wrds_cseries_info.parquet"
    return pd.read_parquet(path)


def load_futures_returns(data_dir=DATA_DIR):
    path = data_dir / "futures_returns.parquet"
    return pd.read_parquet(path)


def load_futcal(data_dir=DATA_DIR):
    path = data_dir / "dsfutcalcserval.parquet"
    return pd.read_parquet(path)
