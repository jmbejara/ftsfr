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


# def load_wrds_futures(data_dir=DATA_DIR):
#     path = data_dir / "wrds_futures.parquet"
#     return pd.read_parquet(path)


def load_wrds_cseries_info(data_dir=DATA_DIR):
    path = data_dir / "wrds_cseries_info.parquet"
    return pd.read_parquet(path)


def load_futures_returns(data_dir=DATA_DIR):
    path = data_dir / "futures_returns.parquet"
    return pd.read_parquet(path)


def load_futcal(data_dir=DATA_DIR):
    path = data_dir / "dsfutcalcserval.parquet"
    return pd.read_parquet(path)


def load_gsci_data(data_dir=DATA_DIR):
    df = pd.read_parquet("gsci_indices.parquet")
    df["Date"] = pd.to_datetime(df["index"])
    df = df.sort_values("Date")
    df = df.drop(columns="index")

    df_monthly = df.groupby(df["Date"].dt.to_period("M")).last().reset_index(drop=True)
    index_cols = [col for col in df_monthly.columns if col.endswith("_PX_LAST")]

    for col in index_cols:
        df_monthly[col + "_Return"] = df_monthly[col].pct_change()

    df_monthly["yyyymm"] = df_monthly["Date"].dt.strftime("%Y%m")
    df_return = df_monthly.drop(columns=index_cols).set_index("yyyymm")

    return df_return


def load_commodities_future():
    df = pd.read_parquet("commodities_f")
