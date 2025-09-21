"""
Simple Cross-Validation Forecasting Statistics Script

This script demonstrates cross-validation forecasting using StatsForecast
with statistical models.

Usage:
    python forecast_stats.py --dataset ftsfr_he_kelly_manela_factors_monthly --model auto_arima
"""

import warnings
import time
import argparse
import polars as pl
from pathlib import Path
from tabulate import tabulate
import os

import sys

sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))

from forecast_utils import (
    align_train_data_with_cutoffs,
    convert_pandas_freq_to_polars,
    evaluate_cv,
    get_test_size_from_frequency,
    determine_cv_windows,
    MAX_CV_WINDOWS,
    read_dataset_config,
    should_skip_forecast,
)
from robust_preprocessing import robust_preprocess_pipeline

from statsforecast import StatsForecast
from statsforecast.models import (
    AutoARIMA,
    AutoETS,
    HoltWinters,
    SeasonalNaive,
    HistoricAverage,
    DynamicOptimizedTheta as DOT,
    CrostonClassic as Croston,
    SimpleExponentialSmoothing,
    Theta,
    AutoCES,
)

warnings.filterwarnings("ignore")


def main():
    """Main function for forecast statistics."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Statistical Forecasting with StatsForecast Models"
    )
    parser.add_argument(
        "--dataset", required=True, help="Dataset name from datasets.toml"
    )
    parser.add_argument(
        "--model",
        required=True,
        choices=[
            "historic_average",
            "seasonal_naive",
            "auto_arima",
            "auto_ces",
            "auto_ets",
            "croston",
            "dot",
            "holt_winters",
            "ses",
            "theta",
        ],
        help="Statistical model to use",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode for faster testing with limited data",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip if valid error metrics already exist",
    )
    args = parser.parse_args()

    DATASET_NAME = args.dataset
    MODEL_NAME = args.model
    DEBUG_MODE = args.debug
    SKIP_EXISTING = args.skip_existing

    # Check if we should skip this forecast
    if SKIP_EXISTING and should_skip_forecast(DATASET_NAME, MODEL_NAME, verbose=True):
        print(f"Skipping {MODEL_NAME} for {DATASET_NAME} - valid metrics already exist")
        sys.exit(0)

    print("=" * 60)
    print("Simple Forecast Statistics with Cross-Validation")
    if DEBUG_MODE:
        print("*** DEBUG MODE ENABLED ***")
    print("=" * 60)
    print(f"Dataset: {DATASET_NAME}")
    print(f"Model: {MODEL_NAME}")

    print(f"\n1. Loading Dataset: {DATASET_NAME}")
    print("-" * 40)

    # Load dataset configuration
    dataset_config = read_dataset_config(DATASET_NAME)
    frequency = dataset_config["frequency"]
    seasonality = dataset_config["seasonality"]

    # Convert frequency to Polars format
    polars_frequency = convert_pandas_freq_to_polars(frequency)

    print(f"Frequency: {frequency} (Polars: {polars_frequency})")
    print(f"Seasonality: {seasonality}")

    # Get test size based on frequency (reduce for debug mode)
    if DEBUG_MODE:
        test_size = 6  # Small test size for debug
        print(f"Test size (DEBUG): {test_size}")
    else:
        test_size = get_test_size_from_frequency(frequency)
    print(f"Test size (forecast horizon): {test_size}")

    # Load and preprocess data
    print("\n2. Loading and Preprocessing Data")
    print("-" * 40)

    # Load raw data
    df_raw = pl.read_parquet(dataset_config["data_path"])
    if "id" in df_raw.columns:
        df_raw = df_raw.rename({"id": "unique_id"})

    # Clean column names and basic preprocessing
    drop_cols = [c for c in df_raw.columns if c.startswith("__index_level_")]
    if drop_cols:
        df_raw = df_raw.drop(drop_cols)
    df_raw = df_raw.select(["unique_id", "ds", "y"])

    # Ensure proper dtypes
    df_raw = df_raw.with_columns(pl.col("y").cast(pl.Float32))
    df_raw = df_raw.with_columns(
        pl.when((pl.col("y").is_infinite()) | (pl.col("y").is_nan()))
        .then(None)
        .otherwise(pl.col("y"))
        .alias("y")
    )

    print(
        f"Raw data loaded: {len(df_raw)} observations, {df_raw['unique_id'].n_unique()} series"
    )

    # Apply robust preprocessing pipeline
    train_df, test_df = robust_preprocess_pipeline(
        df_raw,
        frequency=frequency,
        test_size=test_size,
        seasonality=seasonality,
        apply_train_imputation=True,
        debug_limit=20 if DEBUG_MODE else None,
    )

    # For cross-validation, we need the full dataset (train + test combined)
    # Use imputed values if available for training portion
    if "y_imputed" in train_df.columns:
        # For training portion, use imputed values; for test, keep original
        train_for_cv = train_df.select(["unique_id", "ds", "y_imputed"]).rename(
            {"y_imputed": "y"}
        )
        test_for_cv = test_df.select(["unique_id", "ds", "y"])
        df = pl.concat([train_for_cv, test_for_cv])
    else:
        # No imputation, just use original y values
        train_for_cv = train_df.select(["unique_id", "ds", "y"])
        test_for_cv = test_df.select(["unique_id", "ds", "y"])
        df = pl.concat([train_for_cv, test_for_cv])

    # Additional data validation for StatsForecast models
    def validate_statistical_series(df):
        """Validate and clean data for StatsForecast models."""
        print("  Validating data for StatsForecast models...")
        import pandas as pd
        import numpy as np

        # Check for series with insufficient non-null values
        series_to_remove = []
        for unique_id in df["unique_id"].unique():
            series_data = df.filter(pl.col("unique_id") == unique_id)
            y_vals = series_data["y"].to_numpy()

            # Count non-null values
            non_null_count = np.sum(~pd.isna(y_vals))
            total_count = len(y_vals)

            # Remove series with too many nulls (>50% null)
            if non_null_count < total_count * 0.5:
                series_to_remove.append(
                    (unique_id, f"too many nulls: {non_null_count}/{total_count}")
                )
                continue

            # Remove series with insufficient non-null values for forecasting
            if non_null_count < 10:  # Need at least 10 non-null points
                series_to_remove.append(
                    (unique_id, f"insufficient data: {non_null_count} non-null values")
                )
                continue

            # Check for problematic patterns
            finite_vals = y_vals[np.isfinite(y_vals)]
            if len(finite_vals) > 1:
                std_val = np.std(finite_vals, ddof=1)
                if std_val < 1e-12:  # Near-zero variance
                    series_to_remove.append(
                        (unique_id, f"near-zero variance ({std_val:.2e})")
                    )
                    continue

        if series_to_remove:
            removed_ids = [uid for uid, _ in series_to_remove]
            print(
                f"    Removing {len(removed_ids)} series with statistical model issues:"
            )
            for uid, reason in series_to_remove[:3]:  # Show first 3
                print(f"      {uid}: {reason}")
            if len(series_to_remove) > 3:
                print(f"      ... and {len(series_to_remove) - 3} more")

            return removed_ids
        return []

    # Validate and clean data
    problematic_ids = validate_statistical_series(df)
    if problematic_ids:
        df = df.filter(~pl.col("unique_id").is_in(problematic_ids))
        # Also filter train and test data to maintain consistency
        train_df = train_df.filter(~pl.col("unique_id").is_in(problematic_ids))
        test_df = test_df.filter(~pl.col("unique_id").is_in(problematic_ids))

    print(
        f"Final validated data for CV: {len(df):,} observations, {df['unique_id'].n_unique()} series"
    )

    # Define models
    print("\n3. Setting Up Models")
    print("-" * 40)

    # Create the selected statistical model
    model_mapping = {
        "historic_average": HistoricAverage(),
        "seasonal_naive": SeasonalNaive(season_length=seasonality),
        "auto_arima": AutoARIMA(season_length=seasonality),
        "auto_ces": AutoCES(season_length=seasonality),
        "auto_ets": AutoETS(season_length=seasonality),
        "croston": Croston(),
        "dot": DOT(season_length=seasonality),
        "holt_winters": HoltWinters(),
        "ses": SimpleExponentialSmoothing(alpha=0.1),
        "theta": Theta(season_length=seasonality),
    }

    selected_model = model_mapping[MODEL_NAME]
    models = [selected_model]

    model_names = [type(model).__name__ for model in models]
    print(f"Model: {', '.join(model_names)}")

    # Defensive validation before model training
    def validate_data_for_training(df, model_type="statistical"):
        """Final validation to ensure data is ready for model training."""
        print(f"  Performing final validation for {model_type} models...")

        if len(df) == 0:
            raise ValueError(
                f"Empty dataset for {model_type} models after preprocessing"
            )

        series_count = df["unique_id"].n_unique()
        if series_count == 0:
            raise ValueError(
                f"No series remaining for {model_type} models after preprocessing"
            )

        # Check for minimum series requirement
        if series_count < 5:
            print(
                f"    Warning: Only {series_count} series remaining for {model_type} models"
            )

        # Validate each series has minimum data
        min_length_per_series = 5  # Minimum observations per series
        short_series = []
        for unique_id in df["unique_id"].unique():
            series_data = df.filter(pl.col("unique_id") == unique_id)
            if len(series_data) < min_length_per_series:
                short_series.append(unique_id)

        if short_series:
            print(
                f"    Warning: {len(short_series)} series have less than {min_length_per_series} observations"
            )

        print(
            f"    {model_type.capitalize()} data validation passed: {series_count} series, {len(df)} observations"
        )
        return True

    # Validate data before training
    validate_data_for_training(df, "statistical")

    # Initialize StatsForecast
    sf = StatsForecast(
        models=models,
        freq=polars_frequency,
        n_jobs=-1,
        fallback_model=SeasonalNaive(season_length=seasonality),
        verbose=True,
    )

    # Perform cross-validation with one window at the end
    print("\n4. Performing Cross-Validation")
    print("-" * 40)
    print(f"Forecast horizon: {test_size}")
    cv_windows = determine_cv_windows(df, test_size)
    print(f"Cross-validation windows (max {MAX_CV_WINDOWS}): {cv_windows}")
    if cv_windows < MAX_CV_WINDOWS:
        print("  Shortest series length limits the number of windows.")

    start_time = time.time()
    cv_df = sf.cross_validation(
        df=df, h=test_size, step_size=test_size, n_windows=cv_windows
    )
    cv_time = time.time() - start_time
    print(f"Cross-validation completed in {cv_time:.2f} seconds")

    # Evaluate models (cv_df is already in Polars format)
    print("\n5. Evaluating Model Performance")
    print("-" * 40)

    # Align training data with per-series cutoffs reported by cross-validation
    if "y_imputed" in train_df.columns:
        train_data_for_eval = train_df.select(["unique_id", "ds", "y_imputed"]).rename(
            {"y_imputed": "y"}
        )
    else:
        train_data_for_eval = train_df.select(["unique_id", "ds", "y"])
    train_data = align_train_data_with_cutoffs(train_data_for_eval, cv_df)

    mase_scores, mse_scores, rmse_scores, r2oos_scores, actual_model_cols = evaluate_cv(
        cv_df, train_data, seasonality
    )

    # Calculate average metrics across all series
    avg_metrics = {}
    for model_col in actual_model_cols:
        # Count how many series have valid (non-null) metrics
        valid_mase = mase_scores[model_col].drop_nulls().len()
        valid_mse = mse_scores[model_col].drop_nulls().len()
        total_series = len(mase_scores)

        # Check if we have enough valid metrics
        if valid_mase == 0 or valid_mse == 0:
            raise ValueError(
                f"No valid metrics could be calculated for model {model_col}. "
                f"All series have null test periods or invalid predictions. "
                f"Valid MASE: {valid_mase}/{total_series}, Valid MSE: {valid_mse}/{total_series}"
            )

        if valid_mase < total_series * 0.1:  # Less than 10% valid
            print(
                f"  Warning: Only {valid_mase}/{total_series} series have valid MASE scores"
            )

        avg_metrics[model_col] = {
            "MASE": mase_scores[model_col].mean(),
            "MSE": mse_scores[model_col].mean(),
            "RMSE": rmse_scores[model_col].mean(),
            "R2oos": r2oos_scores[model_col].mean(),
        }

    # Create comparison table
    print("\n6. Model Performance Summary")
    print("-" * 40)

    comparison_data = [["Model", "Avg MASE", "Avg MSE", "Avg RMSE", "Avg R2oos"]]
    for model_col in actual_model_cols:
        comparison_data.append(
            [
                model_col,
                f"{avg_metrics[model_col]['MASE']:.4f}",
                f"{avg_metrics[model_col]['MSE']:.4f}",
                f"{avg_metrics[model_col]['RMSE']:.4f}",
                f"{avg_metrics[model_col]['R2oos']:.4f}",
            ]
        )

    print(tabulate(comparison_data, headers="firstrow", tablefmt="grid"))

    # Save CSV error metrics for the selected model
    print("\n7. Saving Error Metrics")
    print("-" * 40)

    # Create error metrics directory
    error_metrics_dir = f"./_output/forecasting/error_metrics/{DATASET_NAME}"
    os.makedirs(error_metrics_dir, exist_ok=True)

    # Get the selected model's metrics
    model_name = model_names[0]  # Should be only one model

    # StatsForecast may use different names in columns (e.g., "SES" instead of "SimpleExponentialSmoothing")
    # Since we're running with a single model, use the actual column name from results
    metrics_key = actual_model_cols[0] if actual_model_cols else model_name

    if metrics_key in avg_metrics:
        # Validate metrics before saving
        mase_val = avg_metrics[metrics_key]["MASE"]
        mse_val = avg_metrics[metrics_key]["MSE"]
        rmse_val = avg_metrics[metrics_key]["RMSE"]
        r2oos_val = avg_metrics[metrics_key]["R2oos"]

        # Check for invalid metric values
        import numpy as np

        if mase_val == 0.0:
            print(
                f"Warning: MASE is exactly 0.0 for model {model_name}. This typically indicates:"
            )
            print("  - The model produces constant predictions")
            print("  - Data quality issues with training/test series")
            print("  - Insufficient variation in the time series")
            print("  Continuing with other metrics, but results may not be meaningful.")
            # Don't raise an error, just warn and continue

        if (
            np.isnan(mase_val)
            or np.isnan(mse_val)
            or np.isnan(rmse_val)
            or np.isnan(r2oos_val)
        ):
            raise ValueError(
                f"NaN values detected in metrics for model {model_name}:\n"
                f"  MASE: {mase_val}\n"
                f"  MSE: {mse_val}\n"
                f"  RMSE: {rmse_val}\n"
                f"  R2oos: {r2oos_val}\n"
                f"This typically indicates insufficient valid data for metric calculation."
            )

        metrics_data = {
            "model_name": [MODEL_NAME],
            "dataset_name": [DATASET_NAME],
            "MASE": [mase_val],
            "MSE": [mse_val],
            "RMSE": [rmse_val],
            "R2oos": [r2oos_val],
            "time_taken": [cv_time],
        }

        metrics_df = pl.DataFrame(metrics_data)
        csv_path = f"{error_metrics_dir}/{MODEL_NAME}.csv"
        metrics_df.write_csv(csv_path)
        print(f"Error metrics saved to: {csv_path}")
    else:
        print(
            f"Warning: Could not find metrics for model. Looking for key '{metrics_key}' in {list(avg_metrics.keys())}"
        )

    print("\n" + "=" * 60)
    print("Forecast Statistics Complete!")
    print("=" * 60)
    print(f"Total time: {cv_time:.2f} seconds")


if __name__ == "__main__":
    main()
