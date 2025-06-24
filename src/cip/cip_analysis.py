"""
Performs analysis on raw fx, exchange rate, and spot data
"""

import sys
import os
import pandas as pd
import numpy as np

# Add the project root (CIP/) to sys.path if not already present
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.pull_bloomberg_cip_data import *
except ModuleNotFoundError:
    from pull_bloomberg_cip_data import *




from settings import config

OUTPUT_DIR = config("OUTPUT_DIR")


def compute_cip_statistics(cip_data):
    """Compute CIP statistics from CIP data."""
    if cip_data is None or cip_data.empty:
        raise ValueError("Error: cip_data is empty or None. Check if compute_cip() is working correctly.")

    stats_dict = {}
    cip_columns = [col for col in cip_data.columns if col.startswith('CIP_') and col.endswith('_ln')]
    cip_df = cip_data[cip_columns]

    if cip_df.empty:
        raise ValueError("Error: cip_df is empty after filtering CIP columns.")

    stats_dict["overall_statistics"] = cip_df.describe()
    stats_dict["correlation_matrix"] = cip_df.corr()
    cip_data.index = pd.to_datetime(cip_data.index)
    stats_dict["annual_statistics"] = cip_df.resample('YE').agg(['mean', 'std', 'min', 'max'])

    return stats_dict



def display_cip_summary(stats_dict):
    """Display overall CIP statistics."""
    if "overall_statistics" not in stats_dict:
        raise KeyError("Key 'overall_statistics' not found in stats dictionary.")

    print("\n" + "=" * 80)
    print("OVERALL CIP STATISTICS (in basis points)")
    print("=" * 80)
    print(stats_dict["overall_statistics"].round(2))


def display_cip_corr(stats_dict):
    """Display the correlation matrix of CIP deviations."""
    if "correlation_matrix" not in stats_dict:
        raise KeyError("Key 'correlation_matrix' not found in stats dictionary.")

    print("\n" + "=" * 80)
    print("CORRELATION MATRIX")
    print("=" * 80)
    print(stats_dict["correlation_matrix"].round(3))


def display_cip_max_min(stats_dict):
    """Display min/max statistics for CIP analysis."""

    if "overall_statistics" not in stats_dict:
        raise KeyError("Key 'overall_statistics' not found in stats dictionary.")

    mean_values = stats_dict["overall_statistics"].loc["mean"]  # Fix: Use lowercase "mean"
    most_positive = mean_values.idxmax()
    most_negative = mean_values.idxmin()

    print("\n" + "=" * 80)
    print("EXTREME CIP DEVIATIONS")
    print("=" * 80)
    print(f"Most Positive CIP Deviation: {most_positive} ({mean_values[most_positive]:.2f} bps)")
    print(f"Most Negative CIP Deviation: {most_negative} ({mean_values[most_negative]:.2f} bps)")
