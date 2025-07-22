"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

- treasury_bond_portfolio_returns: treasury bond portfolio returns
- treasury_bond_returns_long: individual treasury bond returns in long format
"""

import calc_treasury_bond_returns
import pull_CRSP_treasury
import pandas as pd
from settings import config

DATA_DIR = config("DATA_DIR")

# Load individual treasury bond returns
daily_returns = pull_CRSP_treasury.load_CRSP_treasury_consolidated(data_dir=DATA_DIR, with_runness=False)
df_individual_bonds_returns = calc_treasury_bond_returns.calc_monthly_returns(daily_returns)

# Create long format DataFrame with ds, unique_id, and y columns
df_individual_bonds_returns = df_individual_bonds_returns[['month_end', 'kytreasno', 'tdretnua']].copy()
df_individual_bonds_returns.columns = ['ds', 'unique_id', 'y']

# Drop NaN values from y column
df_individual_bonds_returns = df_individual_bonds_returns.dropna(subset=['y'])

# Save the long format bond returns
df_individual_bonds_returns.to_parquet(DATA_DIR / "ftsfr_treas_bond_returns.parquet")

# Also save the portfolio returns in the original format
df_portfolio = calc_treasury_bond_returns.calc_returns(data_dir=DATA_DIR)
df_portfolio_stacked = df_portfolio.set_index('DATE').stack().reset_index()
df_portfolio_stacked.columns = ['ds', 'unique_id', 'y']

# Drop NaN values from y column
df_portfolio_stacked = df_portfolio_stacked.dropna(subset=['y'])

df_portfolio_stacked.to_parquet(DATA_DIR / "ftsfr_treas_bond_portfolio_returns.parquet")

