import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import warnings

import numpy as np
import pandas as pd

import pull_CRSP_treasury
from settings import config

warnings.filterwarnings("ignore", category=DeprecationWarning)

DATA_DIR = config("DATA_DIR")


def group_portfolios(bond_returns=None):
    bins = np.arange(0, 5.5, 0.5)  # [0.0, 0.5, 1.0, ..., 5.0]
    labels = [f"{i + 1}" for i in range(len(bins) - 1)]  # ['1', '2', ..., '10']

    # Filter for CUSIPs starting with '91' and make an explicit copy
    bond_returns = bond_returns[bond_returns["CUSIP"].str.startswith("91")].copy()

    # Convert tr_return to decimal values by dividing by 100
    bond_returns["tr_return"] = bond_returns["tr_return"] / 100

    bond_returns = bond_returns[bond_returns["tr_return"] <= 0.5]

    # Assign tau bins
    bond_returns["tau_group"] = pd.cut(
        bond_returns["tau"], bins=bins, labels=labels, right=False
    )
    bond_returns = bond_returns.dropna(subset=["tau_group"])
    bond_returns["tau_group"] = bond_returns["tau_group"].astype(int)
    bond_returns = bond_returns.dropna(subset=["tr_return"])

    # Step 2: Group by DATE and tau_group, then compute the mean return
    grouped = (
        bond_returns.groupby(["DATE", "tau_group"])["tr_return"].mean().reset_index()
    )

    # Step 3: Pivot the table
    pivoted = grouped.pivot(index="DATE", columns="tau_group", values="tr_return")

    # Step 4 (optional): Rename columns to something like Group_1, Group_2, etc.
    pivoted.columns = [f"{int(col)}" for col in pivoted.columns]

    return pivoted


def calc_treasury_bond_returns(data_dir=DATA_DIR):
    bond_returns = pull_CRSP_treasury.load_CRSP_treasury_consolidated(data_dir=data_dir)
    portfolio_returns = group_portfolios(bond_returns)
    return portfolio_returns


if __name__ == "__main__":
    # DATA_DIR = DATA_DIR / "us_treasury_returns"
    bond_returns = pull_CRSP_treasury.load_CRSP_treasury_consolidated(data_dir=DATA_DIR)
    # portfolio_returns = group_portfolios(bond_returns)
    # portfolio_returns.to_parquet(DATA_DIR / "treasury_bond_portfolio_returns.parquet")
