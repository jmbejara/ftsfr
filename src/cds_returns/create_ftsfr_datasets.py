"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

- ftsfr_cds_portfolio_returns: CDS monthly portfolio returns
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import calc_cds_returns 
import pandas as pd
from settings import config

DATA_DIR = config("DATA_DIR")

cds_returns_portfolio = calc_cds_returns.load_portfolio()

def convert_cds_portfolio_to_long_format(df):
    """
    Convert CDS portfolio returns from wide to long format.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with columns: Month, 3Y_Q1, 3Y_Q2, ..., 10Y_Q5
        
    Returns:
    --------
    pd.DataFrame
        Long format DataFrame with columns: unique_id, ds, y
        where unique_id contains the portfolio names (e.g., '3Y_Q1'), 
        ds contains dates, and y contains returns
    """
    # Reset index to make Month a column if it's the index
    if df.index.name == 'Month':
        df = df.reset_index()
    
    # Use pandas melt to convert from wide to long format
    long_df = df.melt(
        id_vars=["Month"], 
        var_name="unique_id", 
        value_name="y"
    )
    
    # Rename Month column to ds to match the project convention
    long_df = long_df.rename(columns={"Month": "ds"})
    
    # Reorder columns to match the project convention
    long_df = long_df[["unique_id", "ds", "y"]]
    
    # Drop NaN values from y column
    long_df = long_df.dropna(subset=["y"])
    
    return long_df

# Convert to long format
cds_returns_portfolio_long = convert_cds_portfolio_to_long_format(cds_returns_portfolio)

# Save the long format dataset
cds_returns_portfolio_long.to_parquet(DATA_DIR / "ftsfr_cds_portfolio_returns.parquet")


