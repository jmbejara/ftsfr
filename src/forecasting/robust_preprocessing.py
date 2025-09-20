"""
Robust preprocessing pipeline for time series forecasting following best practices.

This module implements the comprehensive preprocessing approach:
1. Build canonical grid with fill_gaps (per_serie start/end)
2. Split train/test correctly (no imputation in test)
3. Filter short/fragmented series
4. Optional light train-only imputation
5. Add gap flags for models that can use them
"""

import math

import polars as pl
import pandas as pd
from utilsforecast.preprocessing import fill_gaps
import numpy as np


def get_data_requirements(frequency, test_size, seasonality=1):
    """Calculate minimum data requirements based on frequency and context."""

    # Base requirements by frequency with dynamic scaling for long horizons
    freq_configs = {
        "ME": {
            "base_min_total": 16,
            "base_min_train": 12,
            "base_min_test": 4,
            "train_ratio": 0.75,
            "test_ratio": 0.25,
            "variance_threshold": 0.001,
            "max_gap_ratio": 0.6,
            "min_train_seasons": 1,
        },
        "MS": {
            "base_min_total": 16,
            "base_min_train": 12,
            "base_min_test": 4,
            "train_ratio": 0.75,
            "test_ratio": 0.25,
            "variance_threshold": 0.001,
            "max_gap_ratio": 0.6,
            "min_train_seasons": 1,
        },
        "D": {
            "base_min_total": 16,
            "base_min_train": 12,
            "base_min_test": 4,
            "train_ratio": 0.5,
            "test_ratio": 0.2,
            "variance_threshold": 0.001,
            "max_gap_ratio": 0.7,
            "min_train_seasons": 1,
        },
        "B": {
            "base_min_total": 16,
            "base_min_train": 12,
            "base_min_test": 4,
            "train_ratio": 0.5,
            "test_ratio": 0.2,
            "variance_threshold": 0.001,
            "max_gap_ratio": 0.7,
            "min_train_seasons": 1,
        },
        "QE": {
            "base_min_total": 27,
            "base_min_train": 18,
            "base_min_test": 9,
            "train_ratio": 1.0,
            "test_ratio": 0.5,
            "variance_threshold": 0.01,
            "max_gap_ratio": 0.6,
            "min_train_seasons": 2,
        },
        "QS": {
            "base_min_total": 27,
            "base_min_train": 18,
            "base_min_test": 9,
            "train_ratio": 1.0,
            "test_ratio": 0.5,
            "variance_threshold": 0.01,
            "max_gap_ratio": 0.6,
            "min_train_seasons": 2,
        },
        "YE": {
            "base_min_total": 40,
            "base_min_train": 30,
            "base_min_test": 10,
            "train_ratio": 1.0,
            "test_ratio": 0.5,
            "variance_threshold": 0.05,
            "max_gap_ratio": 0.6,
            "min_train_seasons": 3,
        },
        "YS": {
            "base_min_total": 40,
            "base_min_train": 30,
            "base_min_test": 10,
            "train_ratio": 1.0,
            "test_ratio": 0.5,
            "variance_threshold": 0.05,
            "max_gap_ratio": 0.6,
            "min_train_seasons": 3,
        },
    }

    config = freq_configs.get(frequency, freq_configs["ME"])

    # Ensure we have enough train/test coverage relative to the evaluation window
    min_train_obs = max(
        config["base_min_train"],
        math.ceil(test_size * config["train_ratio"]),
        seasonality * config["min_train_seasons"]
        if seasonality > 1
        else config["base_min_train"],
    )

    min_test_obs = max(
        config["base_min_test"],
        min(test_size, math.ceil(test_size * config["test_ratio"])),
    )

    # Require enough total observations to support the train/test split
    min_total_obs = max(
        config["base_min_total"],
        min_train_obs + min_test_obs,
        test_size + min_train_obs,
    )

    return {
        "min_total_obs": min_total_obs,
        "min_train_obs": min_train_obs,
        "min_test_obs": min_test_obs,
        "variance_threshold": config["variance_threshold"],
        "max_gap_ratio": config["max_gap_ratio"],
    }


def normalize_month_end_dates(df, frequency):
    """Normalize dates to consistent month-end format for ME frequency.

    This is crucial for datasets with inconsistent month-end dates (e.g., Jan 30, Feb 27)
    to align properly with the canonical grid.
    """
    if frequency == "ME":
        # Convert to true month-end using Polars date manipulation
        # This ensures all dates are the actual last day of their month
        df = df.with_columns(pl.col("ds").dt.month_end().alias("ds"))

        # Remove any duplicates that might arise from normalization
        # (e.g., if Jan 30 and Jan 31 both existed, they'd both become Jan 31)
        # Keep the last value if duplicates exist
        df = df.group_by(["unique_id", "ds"]).last()
    return df


def build_canonical_grid(df, frequency):
    """Build canonical time grid using fill_gaps with per_serie start/end."""
    print("  Building canonical time grid...")

    if frequency == "ME":
        # For month-end data that's already normalized, create a proper canonical grid
        # by filling gaps manually to ensure alignment
        return build_month_end_grid(df)
    else:
        # Convert frequency to format expected by fill_gaps
        freq_map = {
            "MS": "1mo",
            "D": "1d",
            "B": "1d",
            "QE": "3mo",
            "QS": "3mo",
            "YE": "1y",
            "YS": "1y",
        }
        polars_freq = freq_map.get(frequency, "1mo")

        # Use per_serie for both start and end to avoid artificial padding
        df_filled = fill_gaps(df, freq=polars_freq, start="per_serie", end="per_serie")

        original_series = df["unique_id"].n_unique()
        filled_series = df_filled["unique_id"].n_unique()

        print(f"    Grid built: {original_series} → {filled_series} series")
        return df_filled


def build_month_end_grid(df):
    """Build canonical month-end grid for ME frequency data.

    This creates a complete monthly grid for each series using proper month-end dates.
    """
    result_dfs = []

    for unique_id in df["unique_id"].unique():
        series = df.filter(pl.col("unique_id") == unique_id).sort("ds")

        if len(series) == 0:
            continue

        # Get start and end dates
        start_date = series["ds"].min()
        end_date = series["ds"].max()

        # Create complete month-end date range
        date_range = (
            pl.date_range(start_date, end_date, interval="1mo", eager=True)
            .dt.month_end()
            .cast(pl.Datetime("ns"))
        )

        # Create grid dataframe
        grid_df = pl.DataFrame(
            {"unique_id": [unique_id] * len(date_range), "ds": date_range}
        )

        # Left join with original data to preserve values and add nulls for gaps
        filled_series = grid_df.join(series, on=["unique_id", "ds"], how="left")
        result_dfs.append(filled_series)

    final_df = pl.concat(result_dfs)

    original_series = df["unique_id"].n_unique()
    filled_series = final_df["unique_id"].n_unique()

    print(f"    Grid built: {original_series} → {filled_series} series")
    return final_df


def split_train_test_aligned(df, test_size):
    """Split into train/test with proper alignment - test = last test_size observations per series."""
    print(f"  Splitting train/test (test_size={test_size})...")

    def add_split_flags(series_df):
        series_df = series_df.sort("ds")
        n_obs = len(series_df)

        # Create index for splitting
        indices = list(range(n_obs))
        split_point = max(0, n_obs - test_size)

        # Add row index and split flag
        series_df = series_df.with_row_index("row_idx")
        series_df = series_df.with_columns(
            pl.when(pl.col("row_idx") >= split_point)
            .then(True)
            .otherwise(False)
            .alias("is_test")
        )
        return series_df.drop("row_idx")

    # Apply split per series
    df_split = df.group_by("unique_id").map_groups(add_split_flags)

    train_df = df_split.filter(pl.col("is_test") == False)
    test_df = df_split.filter(pl.col("is_test") == True)

    print(
        f"    Split completed: {len(train_df)} train, {len(test_df)} test observations"
    )
    return train_df, test_df


def filter_series_by_quality(train_df, test_df, requirements):
    """Filter series based on comprehensive quality requirements."""
    print("  Filtering series by data quality...")
    print(f"    Requirements: {requirements}")

    valid_series = []
    total_series = train_df["unique_id"].n_unique()
    debug_info = []

    for unique_id in train_df["unique_id"].unique():
        train_series = train_df.filter(pl.col("unique_id") == unique_id)
        test_series = test_df.filter(pl.col("unique_id") == unique_id)

        train_values = train_series["y"].to_numpy()
        test_values = test_series["y"].to_numpy()
        train_valid_mask = np.isfinite(train_values)
        test_valid_mask = np.isfinite(test_values)

        series_debug = {"id": unique_id}

        # Check total length
        total_obs = len(train_series) + len(test_series)
        series_debug["total_obs"] = total_obs
        if total_obs < requirements["min_total_obs"]:
            series_debug["fail_reason"] = (
                f"total_obs {total_obs} < {requirements['min_total_obs']}"
            )
            debug_info.append(series_debug)
            continue

        # Check training data quality
        train_non_null = int(train_valid_mask.sum())
        series_debug["train_non_null"] = train_non_null
        if train_non_null < requirements["min_train_obs"]:
            series_debug["fail_reason"] = (
                f"train_non_null {train_non_null} < {requirements['min_train_obs']}"
            )
            debug_info.append(series_debug)
            continue

        # Check training variance
        if train_non_null > 1:
            train_std = float(np.nanstd(train_values[train_valid_mask], ddof=1))
            series_debug["train_std"] = train_std
            if np.isnan(train_std) or train_std < requirements["variance_threshold"]:
                series_debug["fail_reason"] = (
                    f"train_std {train_std} < {requirements['variance_threshold']}"
                )
                debug_info.append(series_debug)
                continue

        # Check gap ratio in training
        gap_ratio = (
            1.0 - (train_non_null / len(train_series)) if len(train_series) else 1.0
        )
        series_debug["gap_ratio"] = gap_ratio
        if gap_ratio > requirements["max_gap_ratio"]:
            series_debug["fail_reason"] = (
                f"gap_ratio {gap_ratio} > {requirements['max_gap_ratio']}"
            )
            debug_info.append(series_debug)
            continue

        # Check test data availability
        test_non_null = int(test_valid_mask.sum())
        series_debug["test_non_null"] = test_non_null
        if test_non_null < requirements["min_test_obs"]:
            series_debug["fail_reason"] = (
                f"test_non_null {test_non_null} < {requirements['min_test_obs']}"
            )
            debug_info.append(series_debug)
            continue

        series_debug["status"] = "PASSED"
        debug_info.append(series_debug)
        valid_series.append(unique_id)

    # Print debug info for first few series
    print("    Debug: First 5 series quality checks:")
    for i, info in enumerate(debug_info[:5]):
        status = info.get("status", f"FAILED - {info.get('fail_reason', 'unknown')}")
        print(f"      {info['id']}: {status}")
        if "total_obs" in info:
            print(
                f"        - total_obs: {info['total_obs']}, train_non_null: {info.get('train_non_null', 'N/A')}"
            )
            print(
                f"        - train_std: {info.get('train_std', 'N/A')}, gap_ratio: {info.get('gap_ratio', 'N/A')}"
            )
            print(f"        - test_non_null: {info.get('test_non_null', 'N/A')}")

    # Filter datasets
    train_filtered = train_df.filter(pl.col("unique_id").is_in(valid_series))
    test_filtered = test_df.filter(pl.col("unique_id").is_in(valid_series))

    removed = total_series - len(valid_series)
    print(
        f"    Filtered: {total_series} → {len(valid_series)} series ({removed} removed)"
    )

    if len(valid_series) == 0:
        raise ValueError(
            "No series pass quality requirements. Consider relaxing filters or improving data quality."
        )

    return train_filtered, test_filtered, valid_series


def add_gap_indicators(df):
    """Add gap indicator flags for models that can use them."""
    df = df.with_columns(
        [
            pl.col("y").is_null().alias("is_gap"),
            pl.col("y").is_not_null().alias("has_value"),
        ]
    )
    return df


def validate_series_after_imputation(y_vals, unique_id):
    """Validate series data after imputation to catch problematic patterns."""
    if len(y_vals) == 0:
        return False, "empty series"

    # Check for infinite or extremely large values
    if not np.all(np.isfinite(y_vals[~pd.isna(y_vals)])):
        return False, "contains infinite values"

    # Check for extreme outliers that could cause scaling issues
    finite_vals = y_vals[np.isfinite(y_vals)]
    if len(finite_vals) > 0:
        q99 = np.percentile(finite_vals, 99)
        q01 = np.percentile(finite_vals, 1)
        if q99 > 1e10 or q01 < -1e10:
            return False, f"extreme values (range: {q01:.2e} to {q99:.2e})"

    # Check for degenerate variance (all same values after imputation)
    if len(finite_vals) > 1:
        std_val = np.std(finite_vals, ddof=1)
        if std_val < 1e-15:  # Extremely small variance
            return False, f"degenerate variance ({std_val:.2e})"

    return True, "valid"


def light_train_imputation(train_df, seasonality=1, method="seasonal_naive"):
    """Apply light imputation only to training data with robust validation."""
    print(f"  Applying light train imputation (method={method})...")

    def impute_series(series_df):
        series_df = series_df.sort("ds")
        y_vals = series_df["y"].to_numpy()
        is_null = pd.isna(y_vals)

        if method == "seasonal_naive" and seasonality > 1:
            # Fill with seasonal lag
            for i in range(len(y_vals)):
                if is_null[i]:
                    lag_idx = i - seasonality
                    if lag_idx >= 0 and not pd.isna(y_vals[lag_idx]):
                        y_vals[i] = y_vals[lag_idx]
        elif method == "forward_fill":
            # Simple forward fill
            y_vals = pd.Series(y_vals).fillna(method="ffill").values

        return series_df.with_columns(pl.Series("y_imputed", y_vals))

    train_imputed = train_df.group_by("unique_id").map_groups(impute_series)

    # Validate imputed data and remove problematic series
    valid_series = []
    invalid_series = []

    for unique_id in train_imputed["unique_id"].unique():
        series_data = train_imputed.filter(pl.col("unique_id") == unique_id)
        y_vals = series_data["y_imputed"].to_numpy()

        is_valid, reason = validate_series_after_imputation(y_vals, unique_id)
        if is_valid:
            valid_series.append(unique_id)
        else:
            invalid_series.append((unique_id, reason))

    if invalid_series:
        print(
            f"    Warning: Removing {len(invalid_series)} series with problematic imputation:"
        )
        for uid, reason in invalid_series[:3]:  # Show first 3
            print(f"      {uid}: {reason}")
        if len(invalid_series) > 3:
            print(f"      ... and {len(invalid_series) - 3} more")

        # Filter to only valid series
        train_imputed = train_imputed.filter(pl.col("unique_id").is_in(valid_series))

    # Count imputed values
    original_nulls = train_df.filter(pl.col("unique_id").is_in(valid_series))[
        "y"
    ].null_count()
    remaining_nulls = train_imputed["y_imputed"].null_count()
    filled = original_nulls - remaining_nulls

    print(
        f"    Imputation completed: {filled} values filled, {remaining_nulls} nulls remain"
    )
    print(f"    Final valid series: {len(valid_series)}")
    return train_imputed


def robust_preprocess_pipeline(
    df,
    frequency,
    test_size,
    seasonality=1,
    apply_train_imputation=True,
    debug_limit=None,
):
    """
    Complete robust preprocessing pipeline for time series forecasting.

    Args:
        df: Input dataframe with 'unique_id', 'ds', 'y' columns
        frequency: Data frequency (ME, D, etc.)
        test_size: Number of periods for test set
        seasonality: Seasonality parameter
        apply_train_imputation: Whether to apply light train imputation
        debug_limit: If set, limit to this many series for debugging

    Returns:
        train_df, test_df: Preprocessed train and test dataframes
    """
    print("=" * 50)
    print("ROBUST PREPROCESSING PIPELINE")
    print("=" * 50)

    # Debug mode
    if debug_limit:
        initial_series = df["unique_id"].n_unique()
        limited_series = df["unique_id"].unique()[:debug_limit]
        df = df.filter(pl.col("unique_id").is_in(limited_series))
        print(f"Debug mode: Limited to {debug_limit} series (from {initial_series})")

    # Normalize dates for month-end frequency to ensure alignment with canonical grid
    df = normalize_month_end_dates(df, frequency)

    # Step 1: Build canonical grid
    df_grid = build_canonical_grid(df, frequency)

    # Step 2: Split train/test aligned
    train_df, test_df = split_train_test_aligned(df_grid, test_size)

    # Step 3: Get data requirements
    requirements = get_data_requirements(frequency, test_size, seasonality)

    # Step 4: Filter by quality requirements
    train_filtered, test_filtered, valid_series = filter_series_by_quality(
        train_df, test_df, requirements
    )

    # Step 5: Add gap indicators
    train_filtered = add_gap_indicators(train_filtered)
    test_filtered = add_gap_indicators(test_filtered)

    # Step 6: Optional train imputation
    if apply_train_imputation and train_filtered["y"].null_count() > 0:
        train_filtered = light_train_imputation(
            train_filtered, seasonality, "forward_fill"
        )

        # After imputation validation, we need to sync test data with remaining series
        remaining_series = train_filtered["unique_id"].unique()
        test_filtered = test_filtered.filter(
            pl.col("unique_id").is_in(remaining_series)
        )
        valid_series = remaining_series.to_list()

    print("=" * 50)
    print("PREPROCESSING COMPLETED")
    print(f"Final datasets: {len(valid_series)} series")
    print(f"Train: {len(train_filtered)} observations")
    print(f"Test: {len(test_filtered)} observations")
    print("=" * 50)

    return train_filtered, test_filtered
