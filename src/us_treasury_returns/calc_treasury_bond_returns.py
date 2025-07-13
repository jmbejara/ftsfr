import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import warnings

import numpy as np
import pandas as pd

from pull_CRSP_treasury import load_CRSP_treasury_consolidated
from settings import config

warnings.filterwarnings("ignore", category=DeprecationWarning)

DATA_DIR = config("DATA_DIR")


def group_portfolios(bond_returns=None):
    """Group Treasury bonds into portfolios based on remaining days to maturity.

    Parameters
    ----------
    bond_returns : pd.DataFrame
        DataFrame containing Treasury bond data with days_to_maturity and tdretnua columns

    Returns
    -------
    pd.DataFrame
        Pivoted DataFrame with portfolio returns by maturity group
    """
    # Convert days to years for maturity grouping
    bond_returns = bond_returns.copy()
    bond_returns["years_to_maturity"] = bond_returns["days_to_maturity"] / 365.25

    # Create 6-month maturity groups (0.5 year intervals)
    bins = np.arange(0, 5.5, 0.5)  # [0.0, 0.5, 1.0, ..., 5.0]
    labels = [f"{i + 1}" for i in range(len(bins) - 1)]

    # Assign maturity bins based on years to maturity
    bond_returns["tau_group"] = pd.cut(
        bond_returns["years_to_maturity"], bins=bins, labels=labels, right=False
    )
    bond_returns = bond_returns.dropna(subset=["tau_group"])
    bond_returns["tau_group"] = bond_returns["tau_group"].astype(int)
    bond_returns = bond_returns.dropna(subset=["tdretnua"])
    bond_returns["tdretnua"] = bond_returns["tdretnua"]

    # Group by date and maturity group, then compute the mean return
    grouped = (
        bond_returns.groupby(["month_end", "tau_group"])["tdretnua"]
        .mean()
        .reset_index()
    )

    # Pivot the table
    pivoted = grouped.pivot(index="month_end", columns="tau_group", values="tdretnua")

    # Rename columns to maturity group numbers
    pivoted.columns = [f"{int(col)}" for col in pivoted.columns]

    # Reset index to make DATE a column
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={"month_end": "DATE"})

    return pivoted


def calc_treasury_bond_returns(data_dir=DATA_DIR):
    """Calculate Treasury bond portfolio returns using consolidated data with runness.

    Parameters
    ----------
    data_dir : Path or str
        Directory where the data files are stored

    Returns
    -------
    pd.DataFrame
        Portfolio returns by maturity group
    """
    bond_returns = load_CRSP_treasury_consolidated(
        data_dir=data_dir, with_runness=False
    )
    portfolio_returns = group_portfolios(bond_returns)
    return portfolio_returns


def calc_monthly_returns(daily_returns):
    """Calculate monthly returns from daily returns and annualize them.

    Parameters
    ----------
    daily_returns : pd.DataFrame
        DataFrame containing daily returns with columns 'caldt' and 'tdretnua'

    Returns
    -------
    pd.DataFrame
        DataFrame with annualized monthly returns
    """
    # Create a copy to avoid modifying the original
    df = daily_returns.copy()

    # Convert caldt to datetime if it's not already
    df["caldt"] = pd.to_datetime(df["caldt"])

    # Create month-end dates
    df["month_end"] = df["caldt"] + pd.offsets.MonthEnd(0)

    # Group by month and calculate compound returns, then annualize
    monthly_returns = (
        df.groupby(["month_end", "kytreasno"])["tdretnua"]
        .apply(
            lambda x: ((1 + x).prod() - 1)  # First get monthly return
        )
        .reset_index()
    )

    other_cols = [
        col
        for col in df.columns
        if col not in ["caldt", "tdretnua", "month_end", "kytreasno"]
    ]
    last_values = (
        df.groupby(["month_end", "kytreasno"])[other_cols].last().reset_index()
    )

    # Merge monthly returns with other columns
    monthly_returns = monthly_returns.merge(
        last_values, on=["month_end", "kytreasno"], how="left"
    )

    return monthly_returns


def calc_returns(data_dir=DATA_DIR):
    daily_returns = load_CRSP_treasury_consolidated(
        data_dir=data_dir, with_runness=False
    )
    monthly_returns = calc_monthly_returns(daily_returns)
    portfolio_returns = group_portfolios(monthly_returns)
    return portfolio_returns


if __name__ == "__main__":
    # Load daily treasury returns
    daily_returns = load_CRSP_treasury_consolidated(
        data_dir=DATA_DIR, with_runness=False
    )

    # Calculate monthly returns
    monthly_returns = calc_monthly_returns(daily_returns)

    # Also calculate and save portfolio returns as before
    portfolio_returns = group_portfolios(monthly_returns)
    portfolio_returns.to_parquet(DATA_DIR / "treasury_bond_portfolio_returns.parquet")
