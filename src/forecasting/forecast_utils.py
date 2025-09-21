"""
Forecasting Utility Functions

This module contains utility functions extracted from forecast.py for reuse
across forecast_stats.py and forecast_neural.py scripts.
"""

import tomli
import polars as pl
from pathlib import Path
from utilsforecast.preprocessing import fill_gaps
from utilsforecast.losses import mase, mse, rmse

FILE_DIR = Path(__file__).resolve().parent
REPO_ROOT = FILE_DIR.parent.parent

MAX_CV_WINDOWS = 6


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
                        REPO_ROOT
                        / "_data"
                        / "formatted"
                        / module_name
                        / f"{dataset_name}.parquet"
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
                    pl.col("y")
                    .fill_null(strategy="forward")
                    .fill_null(strategy="backward")
                )
            else:
                entity_data_filled = entity_data_trimmed

            cleaned_series.append(entity_data_filled)

    return pl.concat(cleaned_series) if cleaned_series else data


def filter_series_for_forecasting(data, forecast_horizon, seasonality, min_buffer=6):
    """Apply consistent series filtering for all models with protection for small datasets."""
    series_lengths = data.group_by("unique_id").agg(pl.len().alias("n"))

    original_count = len(data["unique_id"].unique())

    # For very small datasets (≤ 10 entities), skip filtering entirely
    if original_count <= 10:
        print(
            f"  Very small dataset detected ({original_count} entities), skipping filtering to preserve all data..."
        )
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

    valid_series = series_lengths.filter(pl.col("n") >= min_required_length).get_column(
        "unique_id"
    )

    # Enhanced fallback logic
    if len(valid_series) == 0:
        print(
            f"  No series meet minimum length {min_required_length}, applying fallback..."
        )
        # First fallback: more lenient requirements
        min_required_length = max(forecast_horizon + 2, 12)
        valid_series = series_lengths.filter(
            pl.col("n") >= min_required_length
        ).get_column("unique_id")

        if len(valid_series) == 0:
            # No small dataset case here since they're handled earlier
            raise ValueError(
                "No series meet the minimum length requirement for forecasting"
            )

    filtered_data = data.filter(pl.col("unique_id").is_in(valid_series.to_list()))
    final_count = len(filtered_data["unique_id"].unique())

    # Log filtering results
    removed_count = original_count - final_count
    if removed_count > 0:
        removal_pct = (removed_count / original_count) * 100
        print(
            f"  Filtered: {original_count} → {final_count} entities ({removed_count} removed, {removal_pct:.1f}%)"
        )
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
        print(
            f"Using entity-based forecast horizon: {forecast_horizon} (median entity length: {int(median_entity_length)})"
        )
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
        test_dates_count = min(
            forecast_horizon, len(unique_dates) // 5
        )  # Max 20% of global dates
        train_cutoff = unique_dates[len(unique_dates) - test_dates_count - 1]

    train_data = df.filter(pl.col("ds") <= train_cutoff)
    test_data = df.filter(pl.col("ds") > train_cutoff)

    # Apply consistent filtering BEFORE any model-specific processing
    train_data_filtered, original_count, final_count, min_length = (
        filter_series_for_forecasting(train_data, forecast_horizon, seasonality)
    )

    # Filter test data to match training series
    valid_series = train_data_filtered["unique_id"].unique().to_list()
    test_data_filtered = test_data.filter(pl.col("unique_id").is_in(valid_series))
    full_data_filtered = df.filter(pl.col("unique_id").is_in(valid_series))

    print(
        f"Filtered out {original_count - final_count} series shorter than {min_length} periods"
    )
    print(f"Final dataset: {final_count} entities for fair model comparison")
    print(
        f"Data split: {len(train_data_filtered)} training samples, {len(test_data_filtered)} test samples"
    )

    return train_data_filtered, test_data_filtered, full_data_filtered


def get_test_size_from_frequency(frequency):
    """Get test size based on frequency."""
    freq_map = {
        "ME": 1,  # Monthly: 1 month ahead
        "MS": 1,  # Month start: 1 month ahead
        "B": 21,  # Business day: ~1 trading month ahead
        "D": 30,  # Calendar day: ~1 calendar month ahead
        "QE": 1,  # Quarterly: 1 quarter ahead
        "QS": 1,  # Quarter start: 1 quarter ahead
    }
    return freq_map.get(frequency, 1)


def determine_cv_windows(
    panel_df: pl.DataFrame, horizon: int, max_windows: int = MAX_CV_WINDOWS
) -> int:
    """Determine how many cross-validation windows can be supported."""

    if horizon <= 0:
        return 1

    if panel_df.height == 0:
        return 1

    lengths = panel_df.group_by("unique_id").len().rename({"len": "length"})
    if lengths.height == 0:
        return 1

    min_length = int(lengths["length"].min())
    possible_windows = max(1, min_length // horizon)
    return max(1, min(max_windows, possible_windows))


def convert_pandas_freq_to_polars(pandas_freq):
    """Convert pandas frequency string to Polars-compatible frequency."""
    freq_map = {
        "MS": "1mo",  # Month start -> 1 month
        "ME": "1mo",  # Month end -> 1 month
        "B": "1d",  # Business day -> 1 day
        "D": "1d",  # Daily -> 1 day
        "QS": "3mo",  # Quarter start -> 3 months
        "QE": "3mo",  # Quarter end -> 3 months
        "YS": "1y",  # Year start -> 1 year
        "YE": "1y",  # Year end -> 1 year
        "h": "1h",  # Hourly -> 1 hour
        "min": "1m",  # Minutely -> 1 minute
        "s": "1s",  # Secondly -> 1 second
    }
    return freq_map.get(pandas_freq, "1mo")  # Default to monthly


def calculate_oos_r2(cv_df, train_df, models):
    """Calculate out-of-sample R-squared: R2oos = 1 - MSE_model / MSE_benchmark."""

    # Calculate historical mean for each series from training data
    historical_means = train_df.group_by("unique_id").agg(
        pl.col("y").mean().alias("historical_mean")
    )

    # Join historical means with cv_df
    cv_with_means = cv_df.join(historical_means, on="unique_id")

    # Calculate MSE_benchmark (using historical mean as forecast)
    cv_with_benchmark = cv_with_means.with_columns(
        ((pl.col("y") - pl.col("historical_mean")) ** 2).alias(
            "squared_error_benchmark"
        )
    )

    # Calculate MSE_benchmark for each series
    mse_benchmark_by_series = cv_with_benchmark.group_by("unique_id").agg(
        pl.col("squared_error_benchmark").mean().alias("MSE_benchmark")
    )

    # Calculate MSE_model for each model and series
    r2_results = []
    for model in models:
        # Calculate squared errors for this model
        cv_with_model_errors = cv_with_means.with_columns(
            ((pl.col("y") - pl.col(model)) ** 2).alias("squared_error_model")
        )

        # Calculate MSE_model for each series
        mse_model_by_series = cv_with_model_errors.group_by("unique_id").agg(
            pl.col("squared_error_model").mean().alias("MSE_model")
        )

        # Join with benchmark MSE and calculate R2oos
        r2_by_series = (
            mse_model_by_series.join(mse_benchmark_by_series, on="unique_id")
            .with_columns(
                (1 - (pl.col("MSE_model") / pl.col("MSE_benchmark"))).alias(model)
            )
            .select("unique_id", model)
        )

        r2_results.append(r2_by_series)

    # Combine all model R2 results
    final_r2 = r2_results[0]
    for r2_df in r2_results[1:]:
        final_r2 = final_r2.join(r2_df, on="unique_id")

    return final_r2


def evaluate_cv(cv_df, train_df, seasonality):
    """Evaluate cross-validation results using multiple metrics."""

    # Get actual column names from cv_df (excluding metadata columns)
    metadata_cols = ["unique_id", "ds", "cutoff", "y"]
    actual_model_cols = [col for col in cv_df.columns if col not in metadata_cols]

    # Convert NaN values to null so downstream metrics ignore them cleanly
    nan_to_null_exprs = [
        pl.when(pl.col("y").is_nan()).then(None).otherwise(pl.col("y")).alias("y")
    ]
    for col in actual_model_cols:
        nan_to_null_exprs.append(
            pl.when(pl.col(col).is_nan()).then(None).otherwise(pl.col(col)).alias(col)
        )
    cv_df = cv_df.with_columns(nan_to_null_exprs)

    print(f"Debug: CV dataframe shape: {cv_df.shape}")
    print(f"Debug: Model columns: {actual_model_cols}")
    print(f"Debug: Seasonality: {seasonality}")

    # Debug: Check CV data quality
    for col in actual_model_cols:
        print(
            f"Debug: Model {col} - nulls: {cv_df[col].null_count()}, unique values: {cv_df[col].n_unique()}"
        )
        if cv_df[col].null_count() == 0:
            print(f"Debug: Model {col} - stats: {cv_df[col].describe()}")

    print(
        f"Debug: Actual y values - nulls: {cv_df['y'].null_count()}, unique values: {cv_df['y'].n_unique()}"
    )
    if cv_df["y"].null_count() == 0:
        print(f"Debug: Actual y values - stats: {cv_df['y'].describe()}")

    # Check for constant predictions
    for col in actual_model_cols:
        y_vals = cv_df["y"].drop_nulls()
        pred_vals = cv_df[col].drop_nulls()
        if len(y_vals) > 0 and len(pred_vals) > 0:
            y_range = y_vals.max() - y_vals.min()
            pred_range = pred_vals.max() - pred_vals.min()
            print(f"Debug: {col} - y_range: {y_range}, pred_range: {pred_range}")

            # Check if predictions are constant
            if pred_range == 0:
                print(
                    f"Warning: Model {col} produces constant predictions: {pred_vals[0]}"
                )

            # Check if actuals are constant
            if y_range == 0:
                print(f"Warning: Actual values are constant: {y_vals[0]}")

    try:
        # Calculate MASE (requires seasonality and train_df)
        mase_scores = mase(
            cv_df, models=actual_model_cols, seasonality=seasonality, train_df=train_df
        )
        print("Debug: MASE calculation succeeded")
    except Exception as e:
        print(f"Debug: MASE calculation failed: {e}")
        # Create a fallback MASE dataframe with NaN values
        mase_scores = cv_df.select(["unique_id"]).unique()
        for col in actual_model_cols:
            mase_scores = mase_scores.with_columns(pl.lit(float("nan")).alias(col))

    # Calculate MSE
    mse_scores = mse(cv_df, models=actual_model_cols)

    # Calculate RMSE
    rmse_scores = rmse(cv_df, models=actual_model_cols)

    # Calculate out-of-sample R-squared
    r2oos_scores = calculate_oos_r2(cv_df, train_df, actual_model_cols)

    return mase_scores, mse_scores, rmse_scores, r2oos_scores, actual_model_cols


def align_train_data_with_cutoffs(train_df, cv_df, cutoff_col="cutoff"):
    """Align training data with per-series cross-validation cutoffs.

    StatsForecast reports a cutoff for each series/window. When multiple series
    end on different dates, using a single global cutoff can truncate most of
    the training history for many series. This in turn makes scale-based error
    metrics like MASE blow up (division by ~0) because the training sample for
    those series appears nearly constant. This helper preserves the correct
    history for each series by filtering with its own cutoff.

    Args:
        train_df: Polars DataFrame containing the (imputed) training data with
            at least ``unique_id`` and ``ds`` columns.
        cv_df: Polars DataFrame with cross-validation results that include a
            ``cutoff`` column per series.
        cutoff_col: Name of the cutoff column in ``cv_df`` (default ``cutoff``).

    Returns:
        Polars DataFrame with the same schema as ``train_df`` but filtered so
        that, for each series, only observations with ``ds`` up to that
        series' last cutoff are retained.
    """

    if cutoff_col not in cv_df.columns:
        raise ValueError(
            f"Cross-validation dataframe is missing required '{cutoff_col}' column"
        )

    # Each series may have a different cutoff; keep the most recent one per id
    per_series_cutoffs = (
        cv_df.select(["unique_id", cutoff_col])
        .group_by("unique_id")
        .agg(pl.col(cutoff_col).max().alias(cutoff_col))
    )

    # Align training data with those cutoffs
    train_with_cutoffs = train_df.join(per_series_cutoffs, on="unique_id", how="inner")
    aligned_train = train_with_cutoffs.filter(pl.col("ds") <= pl.col(cutoff_col))

    missing_series = per_series_cutoffs.height - aligned_train["unique_id"].n_unique()
    if missing_series > 0:
        print(
            "Warning: Dropped {missing_series} series when aligning train data with cutoffs.".format(
                missing_series=missing_series
            )
        )

    return aligned_train.drop(cutoff_col)


def get_minimum_requirements_by_frequency(frequency, test_size, seasonality=1):
    """Calculate minimum data requirements based on frequency and seasonality."""
    freq_multipliers = {
        "ME": 2.0,  # Monthly: need more periods for meaningful patterns
        "MS": 2.0,  # Month start: same as ME
        "D": 1.5,  # Daily: less stringent but still need adequate history
        "B": 1.5,  # Business daily: same as daily
        "QE": 3.0,  # Quarterly: need more periods due to lower frequency
        "QS": 3.0,  # Quarter start: same as QE
        "YE": 5.0,  # Yearly: need many more periods
        "YS": 5.0,  # Year start: same as YE
    }

    multiplier = freq_multipliers.get(frequency, 2.0)

    # Base minimum: test_size + buffer for training
    base_min_train = max(test_size * 2, seasonality * 2 if seasonality > 1 else 12)
    min_train_obs = int(base_min_train * multiplier)

    # Test requirements
    min_test_obs = max(int(test_size * 0.8), 3)  # At least 80% of test period or 3 obs

    # Total minimum
    min_total_obs = min_train_obs + min_test_obs

    return {
        "min_total_obs": min_total_obs,
        "min_train_obs": min_train_obs,
        "min_test_obs": min_test_obs,
        "min_variance": 0.001,  # Minimum standard deviation
    }


def should_skip_forecast(dataset_name, model_name, verbose=True):
    """Check if forecast should be skipped because valid results already exist.

    Args:
        dataset_name: Name of the dataset
        model_name: Name of the model (as used in filename, e.g., 'ses', 'auto_deepar')
        verbose: If True, print messages about skip decision

    Returns:
        bool: True if valid metrics exist and forecast can be skipped, False otherwise
    """
    import pandas as pd
    import numpy as np
    from pathlib import Path

    # Construct the path to the error metrics CSV
    csv_path = Path(
        f"./_output/forecasting/error_metrics/{dataset_name}/{model_name}.csv"
    )

    # Check if file exists
    if not csv_path.exists():
        if verbose:
            print(f"  Metrics file not found: {csv_path}")
        return False

    try:
        # Read the CSV file
        df = pd.read_csv(csv_path)

        if df.empty:
            if verbose:
                print(f"  Metrics file is empty: {csv_path}")
            return False

        # Check required columns exist
        required_cols = ["MASE", "MSE", "RMSE", "R2oos"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            if verbose:
                print(f"  Metrics file missing columns {missing_cols}: {csv_path}")
            return False

        # Get the first row of metrics
        if len(df) == 0:
            if verbose:
                print(f"  No metrics rows in file: {csv_path}")
            return False

        metrics = df.iloc[0]

        # Check that metrics are not null
        for col in required_cols:
            if pd.isna(metrics[col]):
                if verbose:
                    print(f"  Metric {col} is null in file: {csv_path}")
                return False

        # Check that key metrics are not zero (which would indicate failed computation)
        # Note: R2oos can legitimately be negative or zero, so we don't check it
        if metrics["MSE"] == 0 or metrics["RMSE"] == 0:
            if verbose:
                print(
                    f"  Metrics MSE or RMSE are zero (likely failed computation): {csv_path}"
                )
            return False

        # Check for invalid values (inf)
        for col in required_cols:
            if np.isinf(metrics[col]):
                if verbose:
                    print(f"  Metric {col} is infinite in file: {csv_path}")
                return False

        # All checks passed - valid metrics exist
        if verbose:
            print(f"  Valid metrics found, skipping: {csv_path}")
            print(
                f"    MASE={metrics['MASE']:.4f}, MSE={metrics['MSE']:.4f}, "
                f"RMSE={metrics['RMSE']:.4f}, R2oos={metrics['R2oos']:.4f}"
            )

        return True

    except Exception as e:
        if verbose:
            print(f"  Error reading metrics file {csv_path}: {e}")
        return False


def filter_series_by_cv_requirements(
    df, test_size, frequency="ME", seasonality=1, min_test_coverage=0.3, debug=False
):
    """Filter series based on cross-validation requirements.

    Args:
        df: Input dataframe with 'unique_id', 'ds', 'y' columns
        test_size: Size of the test period for cross-validation
        frequency: Data frequency (ME, D, etc.) for adaptive requirements
        seasonality: Seasonality parameter for the data
        min_test_coverage: Minimum fraction of non-null values required in test period
        debug: If True, limit to a small number of series for faster testing

    Returns:
        Filtered dataframe with series that meet requirements
    """
    # Get adaptive requirements based on frequency
    reqs = get_minimum_requirements_by_frequency(frequency, test_size, seasonality)

    print(f"  Data quality requirements for {frequency} frequency:")
    print(f"    Minimum total observations: {reqs['min_total_obs']}")
    print(f"    Minimum training observations: {reqs['min_train_obs']}")
    print(f"    Minimum test observations: {reqs['min_test_obs']}")
    print(f"    Minimum variance threshold: {reqs['min_variance']}")

    # If debug mode, limit to first N series
    if debug:
        debug_series_limit = 20  # Increased to get better sample
        unique_series = df["unique_id"].unique()[:debug_series_limit]
        df = df.filter(pl.col("unique_id").is_in(unique_series))
        print(f"  Debug mode: Limited to {len(unique_series)} series")

    initial_series = df["unique_id"].n_unique()
    print(f"  Starting with {initial_series} series")

    # Step 1: Filter by total length
    series_lengths = df.group_by("unique_id").agg(pl.len().alias("total_length"))
    valid_total_length = series_lengths.filter(
        pl.col("total_length") >= reqs["min_total_obs"]
    )["unique_id"]

    df_step1 = df.filter(pl.col("unique_id").is_in(valid_total_length))
    removed_step1 = initial_series - len(valid_total_length)
    print(
        f"  Step 1 - Total length filter: Removed {removed_step1} series (< {reqs['min_total_obs']} obs)"
    )

    # Step 2: Check train/test split quality
    series_with_sufficient_data = []
    for unique_id in df_step1["unique_id"].unique():
        series_data = df_step1.filter(pl.col("unique_id") == unique_id).sort("ds")

        # Check overall series quality
        non_null_data = series_data["y"].drop_nulls()
        if len(non_null_data) < reqs["min_total_obs"]:
            continue

        # Check variance - filter out near-constant series
        series_std = non_null_data.std()
        if series_std is None or series_std < reqs["min_variance"]:
            continue

        # Split into train/test periods (test = last test_size observations)
        train_data = series_data.head(-test_size)["y"].drop_nulls()
        test_data = series_data.tail(test_size)["y"].drop_nulls()

        # Check training data requirements
        if len(train_data) < reqs["min_train_obs"]:
            continue

        train_std = train_data.std()
        if train_std is None or train_std < reqs["min_variance"]:
            continue

        # Check test data requirements
        if len(test_data) < reqs["min_test_obs"]:
            continue

        series_with_sufficient_data.append(unique_id)

    if len(series_with_sufficient_data) == 0:
        raise ValueError(
            f"No series meet the data quality requirements:\n"
            f"  - Minimum total observations: {reqs['min_total_obs']}\n"
            f"  - Minimum training observations: {reqs['min_train_obs']}\n"
            f"  - Minimum test observations: {reqs['min_test_obs']}\n"
            f"  - Minimum variance: {reqs['min_variance']}\n"
            f"Data quality issue: all series have insufficient data for reliable forecasting."
        )

    step1_count = len(df_step1["unique_id"].unique())
    df_final = df_step1.filter(pl.col("unique_id").is_in(series_with_sufficient_data))
    removed_step2 = step1_count - len(series_with_sufficient_data)

    print(f"  Step 2 - Train/test quality filter: Removed {removed_step2} series")
    print(
        f"  Final result: {len(series_with_sufficient_data)} series passed all quality checks"
    )

    return df_final
