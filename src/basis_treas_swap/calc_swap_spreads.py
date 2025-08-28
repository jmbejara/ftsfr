"""
Responsible for calculating the Treasury-Swap arbitrage spreads and saving them.

Format step only: loads cleaned data from disk and performs calculations.
"""

from pathlib import Path

import pandas as pd

from settings import config
from pull_bbg_treas_swap import load_syields, load_tyields

DATA_DIR = config("DATA_DIR")


def calc_swap_spreads(treasury_df: pd.DataFrame, swap_df: pd.DataFrame) -> pd.DataFrame:
    """Combines the treasury and swap data and calculates the spreads

    :param treasury_df: DataFrame containing the treasury yield data
    :type treasury_df: pd.DataFrame
    :param swap_df: DataFrame containing the swap yield data
    :type swap_df: pd.DataFrame
    :return: The merged data frame containing the clean and calculated data
    :rtype: pd.DataFrame
    """

    s_years = [1, 2, 3, 5, 10, 20, 30]
    merged_df = pd.merge(
        swap_df, treasury_df, left_index=True, right_index=True, how="inner"
    )
    for i in s_years:
        merged_df[f"Arb_Swap_{i}"] = 100 * (
            -merged_df[f"GT{i} Govt"] + merged_df[f"USSO{i} CMPN Curncy"]
        )
        merged_df[f"tswap_{i}_rf"] = merged_df[f"USSO{i} CMPN Curncy"] * 100

    merged_df["Year"] = pd.to_datetime(merged_df.index).year
    merged_df = merged_df[merged_df["Year"] >= 2000]

    arb_list = [f"Arb_Swap_{x}" for x in s_years]
    tswap_list = [f"tswap_{x}_rf" for x in s_years]
    merged_df = merged_df[arb_list + tswap_list]
    merged_df = merged_df.dropna(how="all")

    # Ensure columns are a single Index, not MultiIndex
    if isinstance(merged_df.columns, pd.MultiIndex):
        merged_df.columns = merged_df.columns.get_level_values(0)

    return merged_df


def assemble_swap_spreads(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load cleaned inputs from disk, compute spreads, and save results."""
    swap_df = load_syields(data_dir=data_dir)
    treasury_df = load_tyields(data_dir=data_dir)

    arb_df = calc_swap_spreads(treasury_df, swap_df)
    return arb_df


def load_swap_spreads(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load swap spreads from disk."""
    file = data_dir / "swap_spreads.parquet"
    return pd.read_parquet(file)


if __name__ == "__main__":
    df = assemble_swap_spreads(data_dir=DATA_DIR)
    file = DATA_DIR / "swap_spreads.parquet"
    df.to_parquet(file)
