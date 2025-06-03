import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import warnings

import pandas as pd
import pull_open_source_bond

from settings import config

warnings.filterwarnings("ignore", category=DeprecationWarning)

DATA_DIR = config("DATA_DIR")


def assign_cs_deciles(df):
    """
    Assign deciles based on the CS column within each date.
    """

    def assign_deciles(group):
        group = group.copy()
        group["cs_decile"] = pd.qcut(group["CS"], 10, labels=False) + 1
        return group

    return df.groupby("date", group_keys=False).apply(assign_deciles)


def calc_value_weighted_decile_returns(df, value_col="BOND_VALUE"):
    """
    Calculate value-weighted bond returns by date and cs_decile.
    """
    agg = (
        df.groupby(["date", "cs_decile"])
        .apply(lambda x: (x["bond_ret"] * x[value_col]).sum() / x[value_col].sum())
        .reset_index(name="weighted_bond_ret")
    )
    pivoted = agg.pivot(index="date", columns="cs_decile", values="weighted_bond_ret")
    pivoted = pivoted.sort_index(axis=1)
    return pivoted


def calc_corp_bond_returns(data_dir=DATA_DIR):
    bond_returns = pull_open_source_bond.load_corporate_bond_returns(data_dir=data_dir)
    deciled_bond_returns = assign_cs_deciles(bond_returns)
    # Value-weighted returns
    value_weighted = calc_value_weighted_decile_returns(
        deciled_bond_returns, value_col="BOND_VALUE"
    )
    return value_weighted


if __name__ == "__main__":
    bond_returns = pull_open_source_bond.load_corporate_bond_returns(data_dir=DATA_DIR)
    deciled_bond_returns = assign_cs_deciles(bond_returns)
    # Value-weighted returns
    value_weighted = calc_value_weighted_decile_returns(
        deciled_bond_returns, value_col="BOND_VALUE"
    )
    value_weighted.to_parquet(DATA_DIR / "corp_bond_portfolio_returns.parquet")
