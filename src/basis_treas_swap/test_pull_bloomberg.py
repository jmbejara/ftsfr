"""
Tests functions in pull_bbg_treas_swap responsible for the raw and clean data.
"""

import pandas as pd
import os
import pull_bbg_treas_swap
import numpy as np
from pathlib import Path
from settings import config

data_dir = Path(config("DATA_DIR"))


def test_pull_raw_tyields():
    """Checking if column names are correct
    and if raw data file is properly created
    """
    months = [1, 2, 3, 4, 6]
    years = [1, 2, 3, 5, 7, 10, 20, 30]
    t_list = [f"GB{x} Govt" for x in months] + [f"GT{x} Govt" for x in years]
    df = pull_bbg_treas_swap.pull_raw_tyields()
    colu = [a for a, _ in df.columns]
    assert colu == t_list

    file_dir = os.path.join(data_dir, "bbg")
    file = os.path.join(file_dir, "raw_tyields.pkl")
    assert os.path.exists(file)


def test_pull_raw_syields():
    """Checking if column names are correct
    and if raw data file is properly created
    """
    years = [1, 2, 3, 5, 10, 20, 30]
    swap_list = [f"USSO{x} CMPN Curncy" for x in years]
    df = pull_bbg_treas_swap.pull_raw_syields()
    colu = [a for a, _ in df.columns]
    assert colu == swap_list

    file_dir = os.path.join(data_dir, "bbg")
    file = os.path.join(file_dir, "raw_syields.pkl")
    assert os.path.exists(file)


def test_clean_raw_tyields():
    """Checking with dummy data that all outputs are in the cleaned
    dtype and that the length of the output df is the same as the
    input df
    """
    test_df_index = pd.date_range("2025-01-01", "2025-01-03")
    test_df = pd.DataFrame(index=test_df_index)
    test_df["test1"] = ["1", "2.3", "seven"]
    test_df["test2"] = ["1", "2", "0"]
    test_df["test3"] = ["1.3", "9.01", "3.62"]
    test_df["test4"] = ["sesdf", "teststr", "fakenews"]
    test_len = len(test_df)
    test_df = pull_bbg_treas_swap.clean_raw_tyields(test_df, override=False, save_data=False)
    assert ((test_df.dtypes == np.int64) | (test_df.dtypes == np.float64)).all()

    assert len(test_df) == test_len


def test_clean_raw_syields():
    """Checking with dummy data that all outputs are in the cleaned
    dtype and that the length of the output df is the same as the
    input df
    """
    test_df_index = pd.date_range("2025-01-01", "2025-01-03")
    test_df = pd.DataFrame(index=test_df_index)
    test_df["test1"] = ["1", "2.3", "seven"]
    test_df["test2"] = ["1", "2", "0"]
    test_df["test3"] = ["1.3", "9.01", "3.62"]
    test_df["test4"] = ["sesdf", "teststr", "fakenews"]
    test_len = len(test_df)
    test_df = pull_bbg_treas_swap.clean_raw_syields(test_df, override=False, save_data=False)
    assert ((test_df.dtypes == np.int64) | (test_df.dtypes == np.float64)).all()

    assert len(test_df) == test_len
