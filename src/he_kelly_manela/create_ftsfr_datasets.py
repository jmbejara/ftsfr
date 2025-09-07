"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

- ftsfr_he_kelly_manela_factors_monthly: monthly factors from He, Kelly, and Manela (2017)
- ftsfr_he_kelly_manela_factors_daily: daily factors from He, Kelly, and Manela (2017)
- ftsfr_he_kelly_manela_all: all factors from He, Kelly, and Manela (2017)
"""

import pull_he_kelly_manela
from settings import config

DATA_DIR = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "he_kelly_manela"

he_kelly_manela_factors_monthly = (
    pull_he_kelly_manela.load_he_kelly_manela_factors_monthly(data_dir=DATA_DIR)
)
he_kelly_manela_factors_daily = pull_he_kelly_manela.load_he_kelly_manela_factors_daily(
    data_dir=DATA_DIR
)
he_kelly_manela_all = pull_he_kelly_manela.load_he_kelly_manela_all(data_dir=DATA_DIR)


def convert_intermediary_to_long_format(df):
    """
    Convert intermediary columns from wide to long format.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with columns: date, intermediary_capital_ratio,
        intermediary_capital_risk_factor, intermediary_value_weighted_investment_return,
        intermediary_leverage_ratio_squared

    Returns:
    --------
    pd.DataFrame
        Long format DataFrame with columns: unique_id, ds, y
        where unique_id contains the variable names, ds contains dates, and y contains values
    """
    # Define the columns to convert to long format
    value_columns = [
        "intermediary_capital_ratio",
        "intermediary_capital_risk_factor",
        "intermediary_value_weighted_investment_return",
        "intermediary_leverage_ratio_squared",
    ]

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


he_kelly_manela_factors_monthly = convert_intermediary_to_long_format(
    he_kelly_manela_factors_monthly
)
he_kelly_manela_factors_daily = convert_intermediary_to_long_format(
    he_kelly_manela_factors_daily
)
he_kelly_manela_all = convert_intermediary_to_long_format(he_kelly_manela_all)


# Save the datasets
he_kelly_manela_factors_monthly.reset_index(drop=True, inplace=True)
he_kelly_manela_factors_monthly = he_kelly_manela_factors_monthly.dropna()
he_kelly_manela_factors_monthly.to_parquet(
    DATA_DIR / "ftsfr_he_kelly_manela_factors_monthly.parquet"
)
he_kelly_manela_factors_daily.reset_index(drop=True, inplace=True)
he_kelly_manela_factors_daily = he_kelly_manela_factors_daily.dropna()
he_kelly_manela_factors_daily.to_parquet(
    DATA_DIR / "ftsfr_he_kelly_manela_factors_daily.parquet"
)
he_kelly_manela_all.reset_index(drop=True, inplace=True)
he_kelly_manela_all = he_kelly_manela_all.dropna()
he_kelly_manela_all.to_parquet(DATA_DIR / "ftsfr_he_kelly_manela_all.parquet")
