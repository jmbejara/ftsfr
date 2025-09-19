"""
Forecasting Utility Functions

This module contains utility functions extracted from forecast.py for reuse
across forecast_stats.py and forecast_neural.py scripts.
"""

import tomli
import polars as pl
from pathlib import Path
from utilsforecast.preprocessing import fill_gaps

FILE_DIR = Path(__file__).parent
REPO_ROOT = FILE_DIR.parent


def convert_frequency_to_statsforecast(frequency):
    """Convert pandas/dataset frequency to StatsForecast frequency format."""
    frequency_map = {
        "D": "1d",  # Daily
        "W": "1w",  # Weekly
        "M": "1mo",  # Month end
        "MS": "1mo",  # Month start
        "ME": "1mo",  # Month end
        "Y": "1y",  # Year end
        "YS": "1y",  # Year start
        "YE": "1y",  # Year end
        "Q": "3mo",  # Quarter end
        "QS": "3mo",  # Quarter start
        "QE": "3mo",  # Quarter end
        "B": "1d",  # Business day (approximate as daily)
        "h": "1h",  # Hourly
        "min": "1m",  # Minutely
        "s": "1s",  # Secondly
    }
    return frequency_map.get(frequency, frequency)


def read_dataset_config(dataset_name):
    """Read dataset configuration from datasets.toml file."""
    datasets_path = REPO_ROOT / "datasets.toml"
    if not datasets_path.exists():
        raise FileNotFoundError(f"datasets.toml not found at {datasets_path}")
    with open(datasets_path, "rb") as f:
        config = tomli.load(f)

    dataset_config = None
    data_path = None
    for module_name, module_config in config.items():
        if isinstance(module_config, dict) and not module_name.startswith("_"):
            for dataset_key, dataset_info in module_config.items():
                if dataset_key == dataset_name and isinstance(dataset_info, dict):
                    dataset_config = dataset_info
                    data_path = (
                        REPO_ROOT / "_data" / "formatted" / module_name / f"{dataset_name}.parquet"
                    )
                    break
            if dataset_config:
                break

    if not dataset_config:
        available_datasets = []
        for module_name, module_config in config.items():
            if isinstance(module_config, dict) and not module_name.startswith("_"):
                for dataset_key in module_config.keys():
                    if not dataset_key.startswith("_") and dataset_key not in [
                        "data_module_name",
                        "data_module_description",
                        "required_data_sources",
                    ]:
                        available_datasets.append(dataset_key)
        raise ValueError(
            f"Dataset '{dataset_name}' not found. Available datasets: {available_datasets}"
        )

    return {
        "data_path": str(data_path),
        "frequency": dataset_config.get("frequency", "D"),
        "seasonality": dataset_config.get("seasonality", 252),
        "description": dataset_config.get("description", ""),
        "dataset_name": dataset_name,
    }


def standardize_data_cleaning(data, fill_strategy="forward_only"):
    """Apply consistent data cleaning across all models."""
    cleaned_series = []
    for entity in data["unique_id"].unique():
        entity_data = data.filter(pl.col("unique_id") == entity)
        non_null_data = entity_data.filter(pl.col("y").is_not_null())
        if len(non_null_data) > 0:
            last_non_null_date = non_null_data["ds"].max()
            entity_data_trimmed = entity_data.filter(pl.col("ds") <= last_non_null_date)

            # Apply consistent filling strategy
            if fill_strategy == "forward_only":
                entity_data_filled = entity_data_trimmed.with_columns(
                    pl.col("y").fill_null(strategy="forward")
                )
            elif fill_strategy == "forward_and_backward":
                entity_data_filled = entity_data_trimmed.with_columns(
                    pl.col("y").fill_null(strategy="forward").fill_null(strategy="backward")
                )
            else:
                entity_data_filled = entity_data_trimmed

            cleaned_series.append(entity_data_filled)

    return pl.concat(cleaned_series) if cleaned_series else data


def filter_series_for_forecasting(data, forecast_horizon, seasonality, min_buffer=6):
    """Apply consistent series filtering for all models with protection for small datasets."""
    series_lengths = (
        data.group_by("unique_id")
        .agg(pl.len().alias("n"))
    )

    original_count = len(data["unique_id"].unique())

    # For very small datasets (≤ 10 entities), skip filtering entirely
    if original_count <= 10:
        print(f"  Very small dataset detected ({original_count} entities), skipping filtering to preserve all data...")
        # Return all data without filtering
        final_count = original_count
        return data, original_count, final_count, 0
    else:
        # Calculate adaptive minimum length based on data characteristics
        # For monthly data with no seasonality (seasonality=1), be more lenient
        if seasonality <= 1:
            # Monthly returns data - use lighter minimum requirements
            base_min = max(forecast_horizon + min_buffer, 18)
        else:
            # Data with seasonality - need more observations
            base_min = max(seasonality + 1, forecast_horizon + min_buffer)

        # Cap at reasonable maximum, but be more flexible than before
        min_required_length = max(base_min, 18)  # Reduced from 24 to 18

    valid_series = series_lengths.filter(pl.col("n") >= min_required_length).get_column("unique_id")

    # Enhanced fallback logic
    if len(valid_series) == 0:
        print(f"  No series meet minimum length {min_required_length}, applying fallback...")
        # First fallback: more lenient requirements
        min_required_length = max(forecast_horizon + 2, 12)
        valid_series = series_lengths.filter(pl.col("n") >= min_required_length).get_column("unique_id")

        if len(valid_series) == 0:
            # No small dataset case here since they're handled earlier
            raise ValueError("No series meet the minimum length requirement for forecasting")

    filtered_data = data.filter(pl.col("unique_id").is_in(valid_series.to_list()))
    final_count = len(filtered_data["unique_id"].unique())

    # Log filtering results
    removed_count = original_count - final_count
    if removed_count > 0:
        removal_pct = (removed_count / original_count) * 100
        print(f"  Filtered: {original_count} → {final_count} entities ({removed_count} removed, {removal_pct:.1f}%)")
        print(f"  Minimum length requirement: {min_required_length}")

    return filtered_data, original_count, final_count, min_required_length


def load_and_preprocess_data(data_path, frequency="D", test_split=0.2, seasonality=252):
    """Load and preprocess the dataset using Polars throughout with consistent filtering."""
    print("Loading and preprocessing data...")

    df = pl.read_parquet(data_path)
    # Rename 'id' to 'unique_id' if needed
    if "id" in df.columns:
        df = df.rename({"id": "unique_id"})

    drop_cols = [c for c in df.columns if c.startswith("__index_level_")]
    if drop_cols:
        df = df.drop(drop_cols)
    df = df.select(["unique_id", "ds", "y"])

    print(f"Initial dataset: {len(df['unique_id'].unique())} entities")

    # Ensure proper dtypes & guard against inf/nan
    df = df.with_columns(pl.col("y").cast(pl.Float32))
    df = df.with_columns(
        pl.when((pl.col("y").is_infinite()) | (pl.col("y").is_nan()))
        .then(None)
        .otherwise(pl.col("y"))
        .alias("y")
    )

    # Calculate forecast horizon based on ORIGINAL entity lengths before fill_gaps
    # This prevents fill_gaps from artificially inflating entity lengths
    original_entity_lengths = df.group_by("unique_id").agg(pl.len().alias("length"))
    median_entity_length = original_entity_lengths["length"].median()

    # Fill date grid: avoid padding leading nulls (start='per_serie'); keep aligned tail
    polars_freq = convert_frequency_to_statsforecast(frequency)
    df = fill_gaps(df, freq=polars_freq, start="per_serie", end="global")

    # Use entity-based forecast horizon calculation
    if median_entity_length < 100:  # Short-lived entities (< 100 observations)
        # Use a reasonable fraction of median entity length for forecast horizon
        forecast_horizon = max(int(median_entity_length * test_split), 6)
        print(f"Using entity-based forecast horizon: {forecast_horizon} (median entity length: {int(median_entity_length)})")
    else:
        # For long series, use global timeline approach
        unique_dates = df["ds"].unique().sort()
        split_idx = int(len(unique_dates) * (1 - test_split))
        train_cutoff = unique_dates[split_idx - 1]
        forecast_horizon = len(unique_dates) - split_idx
        print(f"Using global forecast horizon: {forecast_horizon}")

    # For entity-based approach, we still need a train_cutoff for data splitting
    if median_entity_length < 100:
        # Use a more recent cutoff based on the last portion of data
        unique_dates = df["ds"].unique().sort()
        # Take the last portion for testing, but cap it reasonably
        test_dates_count = min(forecast_horizon, len(unique_dates) // 5)  # Max 20% of global dates
        train_cutoff = unique_dates[len(unique_dates) - test_dates_count - 1]

    train_data = df.filter(pl.col("ds") <= train_cutoff)
    test_data = df.filter(pl.col("ds") > train_cutoff)

    # Apply consistent filtering BEFORE any model-specific processing
    train_data_filtered, original_count, final_count, min_length = filter_series_for_forecasting(
        train_data, forecast_horizon, seasonality
    )

    # Filter test data to match training series
    valid_series = train_data_filtered["unique_id"].unique().to_list()
    test_data_filtered = test_data.filter(pl.col("unique_id").is_in(valid_series))
    full_data_filtered = df.filter(pl.col("unique_id").is_in(valid_series))

    print(f"Filtered out {original_count - final_count} series shorter than {min_length} periods")
    print(f"Final dataset: {final_count} entities for fair model comparison")
    print(f"Data split: {len(train_data_filtered)} training samples, {len(test_data_filtered)} test samples")

    return train_data_filtered, test_data_filtered, full_data_filtered