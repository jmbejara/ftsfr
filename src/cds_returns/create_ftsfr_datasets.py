"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

- CDS_portfolio_returns: Monthly CDS portfolio returns (20 portfolios: 4 tenors × 5 credit quintiles)
- CDS_contract_returns: Monthly CDS returns at the individual contract level

"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from settings import config
import calc_cds_returns

DATA_DIR = config("DATA_DIR")

## ftsfr_CDS_portfolio_returns - Portfolio level returns
# Load the portfolio returns calculated by calc_cds_returns.py
# This contains monthly returns for 20 CDS portfolios formed by:
# - 4 tenors: 3Y, 5Y, 7Y, 10Y
# - 5 credit quality quintiles (Q1=safest to Q5=riskiest)
# Columns are named like "3Y_Q1", "5Y_Q3", "10Y_Q5", etc.
df_portfolios = calc_cds_returns.load_portfolio(data_dir=DATA_DIR)

# The data has Month column and portfolio columns like "3Y_Q1", "3Y_Q2", ..., "10Y_Q5"
# Convert from wide to long format for ftsfr standard

# Melt the dataframe to get unique_id (portfolio), ds (date), and y (return value)
df_portfolio_long = df_portfolios.melt(
    id_vars=["Month"], var_name="unique_id", value_name="y"
)

# Rename columns to match ftsfr standard
df_portfolio_long = df_portfolio_long.rename(columns={"Month": "ds"})

# Sort by portfolio and date
df_portfolio_long = df_portfolio_long.sort_values(by=["unique_id", "ds"]).reset_index(
    drop=True
)

# Save as ftsfr dataset
df_portfolio_long.to_parquet(DATA_DIR / "ftsfr_CDS_portfolio_returns.parquet")


## ftsfr_CDS_contract_returns - Contract level returns
# Load the contract returns calculated by calc_cds_returns.py
# This contains monthly returns for individual CDS contracts
# Columns: ticker, tenor, Month, credit_quantile, monthly_return
df_contracts = calc_cds_returns.load_contract_returns(data_dir=DATA_DIR)

# Create unique_id by combining ticker and tenor
df_contracts["unique_id"] = df_contracts["ticker"] + "_" + df_contracts["tenor"]

# Select and rename columns to match ftsfr standard
df_contract_long = df_contracts[["unique_id", "Month", "monthly_return"]].rename(
    columns={"Month": "ds", "monthly_return": "y"}
)

# Sort by contract and date
df_contract_long = df_contract_long.sort_values(by=["unique_id", "ds"]).reset_index(
    drop=True
)

# Save as ftsfr dataset
df_contract_long.to_parquet(DATA_DIR / "ftsfr_CDS_contract_returns.parquet")
