"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

"""

import calc_cip
import pandas as pd
from settings import config

DATA_DIR = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "wrds_crsp_compustat"


## Calculate fx returns
df_all = calc_cip.calculate_cip(end_date="2025-03-01", data_dir=DATA_DIR)
df_stacked = df_all.stack().reset_index()
df_stacked.columns = ['ds', 'unique_id', 'y']

df_stacked.to_parquet(DATA_DIR / "ftsfr_CIP_spreads.parquet")

