"""Functions to generate supplementary table and plots"""

import pandas as pd
from pathlib import Path

from settings import config
from pull_bloomberg import (
    pull_raw_syields,
    pull_raw_tyields,
    clean_raw_syields,
    clean_raw_tyields,
)
from calc_swap_spreads import calc_swap_spreads

OUTPUT_DIR = Path(config("OUTPUT_DIR"))


def replication_df(treasury_df, swap_df):
    """Creates a merged DataFrame of the treasury and swap yields
    :param treasury_df: DataFrame containing the treasury yield data
    :type treasury_df: pd.DataFrame
    :param swap_df: DataFrame containing the swap yield data
    :type swap_df: pd.DataFrame
    :return: The merged data frame
    :rtype: pd.DataFrame
    """
    years = [1, 2, 3, 5, 10, 20, 30]
    t_list = [f"GT{year} Govt" for year in years]
    s_list = [f"USSO{year} CMPN Curncy" for year in years]
    return pd.merge(
        treasury_df[t_list].loc[pd.Timestamp("2010").date() :],
        swap_df[s_list].loc[pd.Timestamp("2010").date() :],
        left_index=True,
        right_index=True,
        how="inner",
    )


def sup_table(calc_df, file_name="table.txt"):
    """Creates the table of means for spreads. Also saves the LaTeX table to a text file.

    :param calc_df: DataFrame containing the swap yield data
    :type calc_df: pd.DataFrame
    :param file_name: name of the text file to save LaTeX table to
    :type file_name: string
    :return: The data frame containing means
    :rtype: pd.DataFrame
    """
    years = [1, 2, 3, 5, 10, 20, 30]
    df = calc_df[[f"Arb_Swap_{year}" for year in years]]
    for year in years:
        df = df.rename(columns={f"Arb_Swap_{year}": f"Arb Swap {year}"})
    means = df.mean()
    means.rename()
    means_str = pd.DataFrame(means, columns=["Mean(bps)"]).to_latex()
    file = OUTPUT_DIR / file_name
    with open(file, "w") as table:
        table.write(means_str)
    return means


def supplementary_main():
    """Main function which runs the functions for supplementary data/table."""
    swap_df = clean_raw_syields(pull_raw_syields())
    treasury_df = clean_raw_tyields(pull_raw_tyields())
    sup_table(calc_swap_spreads(treasury_df, swap_df))
    return replication_df(treasury_df, swap_df)


if __name__ == "__main__":
    supplementary_main()
