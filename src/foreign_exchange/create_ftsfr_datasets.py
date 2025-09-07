"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

- fx_returns: foreign exchange returns
"""

import pandas as pd
import calc_fx
from settings import config

DATA_DIR = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "foreign_exchange"


## Calculate fx returns
df_all = calc_fx.calculate_fx(data_dir=DATA_DIR)
df_all.columns = ["unique_id", "ds", "y"]
df_all["ds"] = pd.to_datetime(df_all["ds"])
# df_all.info()

df_all = df_all.dropna()
df_all.to_parquet(DATA_DIR / "ftsfr_FX_returns.parquet")
