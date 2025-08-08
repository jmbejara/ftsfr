"""
Functions to plot the replicated, updated, and supplementary plots, and save them.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from settings import config
from calc_swap_spreads import calc_swap_spreads
from supplementary import supplementary_main

output_dir = Path(config("OUTPUT_DIR"))


def plot_figure(arb_df, savePath, end=None):
    """Creating and saving the plot generated using the data provided.

    :param arb_df: DataFrame containing the arbitrage calculations per year
    :type arb_df: pd.DataFrame
    :param savePath: Path for saving the plot
    :type savePath: str
    :param end: end date for the plot, defaults to None which then means using
    the last date in arb_df
    :type end: pd.Timestamp

    :return: void
    """
    start = pd.Timestamp(config("START_DATE")).date()
    for year in [1, 20, 2, 30, 3, 5, 10]:
        label = f"{year}Y"
        if end:
            plt.plot(arb_df[f"Arb_Swap_{year}"].loc[start:end].dropna(), label=label)
        else:
            plt.plot(arb_df[f"Arb_Swap_{year}"].loc[start:].dropna(), label=label)
    plt.title("Treasury-Swap")
    plt.xlabel("Dates")
    plt.ylabel("Arbitrage Spread (bps)")
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=5)
    plt.grid(axis="y")
    plt.savefig(savePath, bbox_inches="tight")
    plt.close()


def plot_supplementary(replication_df, savePath):
    """Creating and saving the supplementary plot generated using the data provided.

    :param replication_df: DataFrame containing the cleaned treasury and swap data
    :type replication_df: pd.DataFrame
    :param savePath: Path for saving the plot
    :type savePath: str

    :return: void
    """
    for year in [1, 20, 2, 30, 3, 5, 10]:
        plt.plot(
            np.log(100 * replication_df[f"GT{year} Govt"].dropna()),
            label=f"{year}Y Treasury",
            linewidth=1,
        )
        plt.plot(
            np.log(100 * replication_df[f"USSO{year} CMPN Curncy"].dropna()),
            label=f"{year}Y Swap",
            linewidth=1,
        )
        plt.title("Treasury and Swap Rates")
        plt.xlabel("Dates")
        plt.ylabel("Log Rates")
        plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=5)
        plt.grid(axis="y")
        plt.savefig(
            "".join([x for x in savePath[: len(savePath) - 4]] + [f"{year}", ".png"]),
            bbox_inches="tight",
        )
        plt.close()


def plot_main():
    """
    Main function that creates and saves the replicated, updated, and supplementary plots
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    data_dir = Path(config("DATA_DIR")) / "basis_treas_swap"
    file = data_dir / "calc_spread" / "calc_merged.pkl"
    if file.exists():
        arb_df = pd.read_pickle(file)
    else:
        # Fallback: run bloom and compute
        from pull_bloomberg import (
            pull_raw_syields,
            pull_raw_tyields,
            clean_raw_syields,
            clean_raw_tyields,
        )

        s_df = clean_raw_syields(pull_raw_syields())
        t_df = clean_raw_tyields(pull_raw_tyields())
        arb_df = calc_swap_spreads(t_df, s_df)
    end = pd.Timestamp(config("END_DATE")).date()

    rep_df = supplementary_main()

    plot_figure(
        arb_df, os.path.join(output_dir, "replicated_swap_spread_arb_figure.png"), end
    )
    plot_figure(arb_df, os.path.join(output_dir, "updated_swap_spread_arb_figure.png"))

    plot_supplementary(rep_df, os.path.join(output_dir, "replication_figure.png"))


if __name__ == "__main__":
    plot_main()
