"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

- ftsfr_french_portfolios_25_daily_size_and_bm: Daily Fama-French 25 portfolios based on size and book-to-market
- ftsfr_french_portfolios_25_daily_size_and_op: Daily Fama-French 25 portfolios based on size and operating profitability
- ftsfr_french_portfolios_25_daily_size_and_inv: Daily Fama-French 25 portfolios based on size and investment
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from settings import config

DATA_DIR = config("DATA_DIR")


def convert_wide_to_long_format(df):
    """
    Convert a wide format DataFrame to long format.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with columns: date, and other value columns

    Returns:
    --------
    pd.DataFrame
        Long format DataFrame with columns: unique_id, ds, y
        where unique_id contains the column names (excluding date),
        ds contains dates, and y contains values
    """
    # Get all columns except 'date'
    value_columns = [col for col in df.columns if col != "date"]

    # Use pandas melt to convert from wide to long format
    long_df = df.melt(
        id_vars=["date"], value_vars=value_columns, var_name="unique_id", value_name="y"
    )

    # Rename date column to ds to match the project convention
    long_df = long_df.rename(columns={"date": "ds"})

    # Reorder columns to match the project convention
    long_df = long_df[["unique_id", "ds", "y"]]

    # Drop NaN values from y column
    long_df = long_df.dropna(subset=["y"])

    return long_df


def load_french_portfolios_25_daily_size_and_bm(data_dir=DATA_DIR):
    """Load daily Fama-French 25 portfolios based on size and book-to-market."""
    filepath = data_dir / "french_portfolios_25_daily_size_and_bm.parquet"
    return pd.read_parquet(filepath)


def load_french_portfolios_25_daily_size_and_op(data_dir=DATA_DIR):
    """Load daily Fama-French 25 portfolios based on size and operating profitability."""
    filepath = data_dir / "french_portfolios_25_daily_size_and_op.parquet"
    return pd.read_parquet(filepath)


def load_french_portfolios_25_daily_size_and_inv(data_dir=DATA_DIR):
    """Load daily Fama-French 25 portfolios based on size and investment."""
    filepath = data_dir / "french_portfolios_25_daily_size_and_inv.parquet"
    return pd.read_parquet(filepath)


# Load the daily datasets
french_portfolios_25_daily_size_and_bm = load_french_portfolios_25_daily_size_and_bm(
    data_dir=DATA_DIR
)
french_portfolios_25_daily_size_and_op = load_french_portfolios_25_daily_size_and_op(
    data_dir=DATA_DIR
)
french_portfolios_25_daily_size_and_inv = load_french_portfolios_25_daily_size_and_inv(
    data_dir=DATA_DIR
)

# Convert to long format
french_portfolios_25_daily_size_and_bm = convert_wide_to_long_format(
    french_portfolios_25_daily_size_and_bm
)
french_portfolios_25_daily_size_and_op = convert_wide_to_long_format(
    french_portfolios_25_daily_size_and_op
)
french_portfolios_25_daily_size_and_inv = convert_wide_to_long_format(
    french_portfolios_25_daily_size_and_inv
)

# Save the datasets
french_portfolios_25_daily_size_and_bm.to_parquet(
    DATA_DIR / "ftsfr_french_portfolios_25_daily_size_and_bm.parquet"
)
french_portfolios_25_daily_size_and_op.to_parquet(
    DATA_DIR / "ftsfr_french_portfolios_25_daily_size_and_op.parquet"
)
french_portfolios_25_daily_size_and_inv.to_parquet(
    DATA_DIR / "ftsfr_french_portfolios_25_daily_size_and_inv.parquet"
)
