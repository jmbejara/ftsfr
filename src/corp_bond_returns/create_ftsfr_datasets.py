"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

- corp_bond_portfolio_returns: corporate bond portfolio returns
"""

import calc_corp_bond_returns
import pandas as pd
from settings import config

DATA_DIR = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "wrds_crsp_compustat"


## Corporate Bond Portfolio Returns
df_all = calc_corp_bond_returns.calc_corp_bond_returns(data_dir=DATA_DIR)
df_stacked = df_all.stack().reset_index()
df_stacked.columns = ['ds', 'unique_id', 'y']

df_stacked.to_parquet(DATA_DIR / "ftsfr_Corp_Bond_Returns.parquet")

