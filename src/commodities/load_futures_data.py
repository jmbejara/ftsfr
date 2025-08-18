"""
This is a temporary file used to load all the necessary data.
It can be added to the pull-file once the dataset to use has been determined.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


import pandas as pd

from settings import config

DATA_DIR = config("DATA_DIR")


def load_futures_returns(data_dir=DATA_DIR):
    path = data_dir / "futures_returns.parquet"
    return pd.read_parquet(path)


def load_lme_metals(data_dir=DATA_DIR):
    path = data_dir / "lme_metals.parquet"
    return pd.read_parquet(path)


def load_gsci_data(data_dir=DATA_DIR):
    df = pd.read_parquet(data_dir / "gsci_indices.parquet")
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


def load_commodities_future(data_dir=DATA_DIR):
    df = pd.read_parquet(data_dir / "commodity_futures.parquet")
    return df


def load_commodities_manual_old(data_dir=DATA_DIR):
    df = pd.read_csv(data_dir / "clean_1970_2008_commodities_data.csv")
    return df


def load_commodities_manual_new(data_dir=DATA_DIR):
    df = pd.read_csv(data_dir / "clean_2009_2024_commodities_data.csv")
    return df


def load_commodities_manual():
    clean_data_df_1970 = load_commodities_manual_old()
    clean_data_df_2009 = load_commodities_manual_new()
    df = pd.concat([clean_data_df_1970, clean_data_df_2009], ignore_index=True)
    return df
