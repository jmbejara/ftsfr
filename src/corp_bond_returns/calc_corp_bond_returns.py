import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import warnings

import pandas as pd
import pull_open_source_bond

from settings import config

warnings.filterwarnings("ignore", category=DeprecationWarning)

DATA_DIR = config("DATA_DIR")


def detect_column_format(df):
    """
    Detect whether the data uses old or new column format.

    Old format (WRDS_MMN_Corrected_Data): CS, BOND_VALUE, bond_ret
    New format (osbap_main_data_2025): cs, sze, ret_vw

    Returns:
        dict: Column names for cs, value, and return columns.
    """
    if "CS" in df.columns:
        # Old format
        return {
            "cs_col": "CS",
            "value_col": "BOND_VALUE",
            "ret_col": "bond_ret",
        }
    elif "cs" in df.columns:
        # New Open Source Bond format
        return {
            "cs_col": "cs",
            "value_col": "sze",
            "ret_col": "ret_vw",
        }
    else:
        raise ValueError(
            "Could not detect data format. Expected either 'CS' (old format) "
            "or 'cs' (new Open Source Bond format) column."
        )


def assign_cs_deciles(df, cs_col="CS"):
    """
    Assign deciles based on the credit spread column within each date.

    Parameters:
        df: DataFrame with bond data
        cs_col: Name of the credit spread column (CS for old, cs for new format)
    """

    def assign_deciles(group):
        group = group.copy()
        valid_cs = group[cs_col].dropna()
        if len(valid_cs) < 10:
            group["cs_decile"] = pd.NA
            return group
        try:
            group["cs_decile"] = (
                pd.qcut(group[cs_col], 10, labels=False, duplicates="drop") + 1
            )
        except ValueError:
            group["cs_decile"] = pd.NA
        return group

    return df.groupby("date", group_keys=False).apply(assign_deciles)


def calc_value_weighted_decile_returns(df, value_col="BOND_VALUE", ret_col="bond_ret"):
    """
    Calculate value-weighted bond returns by date and cs_decile.

    Parameters:
        df: DataFrame with cs_decile assigned
        value_col: Name of the value/size column (BOND_VALUE for old, sze for new)
        ret_col: Name of the return column (bond_ret for old, ret_vw for new)
    """
    df = df.dropna(subset=["cs_decile"])

    def weighted_return(x):
        weights = x[value_col]
        returns = x[ret_col]
        mask = weights.notna() & returns.notna()
        if mask.sum() == 0:
            return pd.NA
        return (returns[mask] * weights[mask]).sum() / weights[mask].sum()

    agg = (
        df.groupby(["date", "cs_decile"])
        .apply(weighted_return, include_groups=False)
        .reset_index(name="weighted_bond_ret")
    )
    pivoted = agg.pivot(index="date", columns="cs_decile", values="weighted_bond_ret")
    pivoted = pivoted.sort_index(axis=1)
    return pivoted


def calc_corp_bond_returns(data_dir=DATA_DIR):
    bond_returns = pull_open_source_bond.load_corporate_bond_returns(data_dir=data_dir)

    # Detect column format
    cols = detect_column_format(bond_returns)

    deciled_bond_returns = assign_cs_deciles(bond_returns, cs_col=cols["cs_col"])
    # Value-weighted returns
    value_weighted = calc_value_weighted_decile_returns(
        deciled_bond_returns, value_col=cols["value_col"], ret_col=cols["ret_col"]
    )
    return value_weighted


if __name__ == "__main__":
    bond_returns = pull_open_source_bond.load_corporate_bond_returns(data_dir=DATA_DIR)

    # Detect column format
    cols = detect_column_format(bond_returns)

    deciled_bond_returns = assign_cs_deciles(bond_returns, cs_col=cols["cs_col"])
    # Value-weighted returns
    value_weighted = calc_value_weighted_decile_returns(
        deciled_bond_returns, value_col=cols["value_col"], ret_col=cols["ret_col"]
    )
    value_weighted.to_parquet(DATA_DIR / "corp_bond_portfolio_returns.parquet")
