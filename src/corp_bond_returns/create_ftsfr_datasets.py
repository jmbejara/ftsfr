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

df_individual_bonds = pull_open_source_bond.load_corporate_bond_returns(
    data_dir=DATA_DIR
)

# Create long format DataFrame with unique_id, ds, and y columns
df_individual_bonds_returns = df_individual_bonds[["cusip", "date", "bond_ret"]].copy()
df_individual_bonds_returns.columns = ["unique_id", "ds", "y"]

# Drop NaN values from y column
df_individual_bonds_returns = df_individual_bonds_returns.dropna(subset=["y"])

# Save the long format bond returns
df_individual_bonds_returns.to_parquet(DATA_DIR / "ftsfr_corp_bond_returns.parquet")

# Also save the portfolio returns in the original format
df_portfolio = calc_corp_bond_returns.calc_corp_bond_returns(data_dir=DATA_DIR)
df_portfolio_melted = df_portfolio.reset_index().melt(
    id_vars=["date"], var_name="unique_id", value_name="y"
)
df_portfolio_melted = df_portfolio_melted[["unique_id", "date", "y"]]
df_portfolio_melted.columns = ["unique_id", "ds", "y"]
df_portfolio_melted.to_parquet(DATA_DIR / "ftsfr_corp_bond_portfolio_returns.parquet")
