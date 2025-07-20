"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

- corp_bond_portfolio_returns: corporate bond portfolio returns
- corp_bond_returns_long: individual corporate bond returns in long format
"""

import calc_corp_bond_returns
import pull_open_source_bond
import pandas as pd
from settings import config

DATA_DIR = config("DATA_DIR")

df_individual_bonds = pull_open_source_bond.load_corporate_bond_returns(data_dir=DATA_DIR)

# Create long format DataFrame with ds, unique_id, and y columns
df_individual_bonds_returns = df_individual_bonds[['date', 'cusip', 'bond_ret']].copy()
df_individual_bonds_returns.columns = ['ds', 'unique_id', 'y']

# Drop NaN values from y column
df_individual_bonds_returns = df_individual_bonds_returns.dropna(subset=['y'])

# Save the long format bond returns
df_individual_bonds_returns.to_parquet(DATA_DIR / "ftsfr_corp_bond_returns.parquet")

# Also save the portfolio returns in the original format
df_portfolio = calc_corp_bond_returns.calc_corp_bond_returns(data_dir=DATA_DIR)
df_portfolio_stacked = df_portfolio.stack().reset_index()
df_portfolio_stacked.columns = ['ds', 'unique_id', 'y']
df_portfolio_stacked.to_parquet(DATA_DIR / "ftsfr_corp_bond_portfolio_returns.parquet")

