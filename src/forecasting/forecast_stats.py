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

from forecast_utils import read_dataset_config, load_and_preprocess_data

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
    GARCH,
    AutoCES
)
from utilsforecast.losses import mase, mse, rmse

warnings.filterwarnings("ignore")

def get_test_size_from_frequency(frequency):
    """Get test size based on frequency."""
    freq_map = {
        'ME': 36,    # Monthly: 36 months
        'MS': 36,    # Month start: 36 months
        'B': 90,     # Business day: 90 days
        'D': 90,     # Daily: 90 days
        'QE': 12,    # Quarterly: 12 quarters
        'QS': 12,    # Quarter start: 12 quarters
    }
    return freq_map.get(frequency, 36)


def convert_pandas_freq_to_polars(pandas_freq):
    """Convert pandas frequency string to Polars-compatible frequency."""
    freq_map = {
        'MS': '1mo',    # Month start -> 1 month
        'ME': '1mo',    # Month end -> 1 month
        'B': '1d',      # Business day -> 1 day
        'D': '1d',      # Daily -> 1 day
        'QS': '3mo',    # Quarter start -> 3 months
        'QE': '3mo',    # Quarter end -> 3 months
        'YS': '1y',     # Year start -> 1 year
        'YE': '1y',     # Year end -> 1 year
        'h': '1h',      # Hourly -> 1 hour
        'min': '1m',    # Minutely -> 1 minute
        's': '1s',      # Secondly -> 1 second
    }
    return freq_map.get(pandas_freq, '1mo')  # Default to monthly


def calculate_oos_r2(cv_df, train_df, models):
    """Calculate out-of-sample R-squared: R2oos = 1 - MSE_model / MSE_benchmark."""

    # Calculate historical mean for each series from training data
    historical_means = train_df.group_by('unique_id').agg(pl.col('y').mean().alias('historical_mean'))

    # Join historical means with cv_df
    cv_with_means = cv_df.join(historical_means, on='unique_id')

    # Calculate MSE_benchmark (using historical mean as forecast)
    cv_with_benchmark = cv_with_means.with_columns(
        ((pl.col('y') - pl.col('historical_mean')) ** 2).alias('squared_error_benchmark')
    )

    # Calculate MSE_benchmark for each series
    mse_benchmark_by_series = cv_with_benchmark.group_by('unique_id').agg(
        pl.col('squared_error_benchmark').mean().alias('MSE_benchmark')
    )

    # Calculate MSE_model for each model and series
    r2_results = []
    for model in models:
        # Calculate squared errors for this model
        cv_with_model_errors = cv_with_means.with_columns(
            ((pl.col('y') - pl.col(model)) ** 2).alias('squared_error_model')
        )

        # Calculate MSE_model for each series
        mse_model_by_series = cv_with_model_errors.group_by('unique_id').agg(
            pl.col('squared_error_model').mean().alias('MSE_model')
        )

        # Join with benchmark MSE and calculate R2oos
        r2_by_series = mse_model_by_series.join(mse_benchmark_by_series, on='unique_id').with_columns(
            (1 - (pl.col('MSE_model') / pl.col('MSE_benchmark'))).alias(model)
        ).select('unique_id', model)

        r2_results.append(r2_by_series)

    # Combine all model R2 results
    final_r2 = r2_results[0]
    for r2_df in r2_results[1:]:
        final_r2 = final_r2.join(r2_df, on='unique_id')

    return final_r2


def evaluate_cv(cv_df, models, train_df, seasonality):
    """Evaluate cross-validation results using multiple metrics."""

    # Get actual column names from cv_df (excluding metadata columns)
    metadata_cols = ['unique_id', 'ds', 'cutoff', 'y']
    actual_model_cols = [col for col in cv_df.columns if col not in metadata_cols]

    # Calculate MASE (requires seasonality and train_df)
    mase_scores = mase(cv_df, models=actual_model_cols, seasonality=seasonality, train_df=train_df)

    # Calculate MSE
    mse_scores = mse(cv_df, models=actual_model_cols)

    # Calculate RMSE
    rmse_scores = rmse(cv_df, models=actual_model_cols)

    # Calculate out-of-sample R-squared
    r2oos_scores = calculate_oos_r2(cv_df, train_df, actual_model_cols)

    return mase_scores, mse_scores, rmse_scores, r2oos_scores, actual_model_cols


def main():
    """Main function for forecast statistics."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Statistical Forecasting with StatsForecast Models")
    parser.add_argument("--dataset", required=True, help="Dataset name from datasets.toml")
    parser.add_argument("--model", required=True,
                       choices=["historic_average", "seasonal_naive", "auto_arima", "auto_ces",
                               "auto_ets", "croston", "dot", "holt_winters", "ses", "theta"],
                       help="Statistical model to use")
    args = parser.parse_args()

    DATASET_NAME = args.dataset
    MODEL_NAME = args.model

    print("=" * 60)
    print("Simple Forecast Statistics with Cross-Validation")
    print("=" * 60)
    print(f"Dataset: {DATASET_NAME}")
    print(f"Model: {MODEL_NAME}")

    print(f"\n1. Loading Dataset: {DATASET_NAME}")
    print("-" * 40)

    # Load dataset configuration
    dataset_config = read_dataset_config(DATASET_NAME)
    frequency = dataset_config['frequency']
    seasonality = dataset_config['seasonality']

    # Convert frequency to Polars format
    polars_frequency = convert_pandas_freq_to_polars(frequency)

    print(f"Frequency: {frequency} (Polars: {polars_frequency})")
    print(f"Seasonality: {seasonality}")

    # Get test size based on frequency
    test_size = get_test_size_from_frequency(frequency)
    print(f"Test size (last N observations): {test_size}")

    # Load and preprocess data
    print("\n2. Loading and Preprocessing Data")
    print("-" * 40)

    # Use full dataset for cross-validation
    _, _, full_data = load_and_preprocess_data(
        dataset_config["data_path"],
        frequency,
        test_split=0.0,  # Use full data for cross-validation
        seasonality=seasonality
    )

    # Enforce a minimum series length compatible with the cross-validation horizon
    min_cv_length = test_size + 1
    series_lengths = full_data.group_by('unique_id').agg(pl.len().alias('length'))
    valid_ids = series_lengths.filter(pl.col('length') >= min_cv_length)['unique_id']
    if len(valid_ids) == 0:
        raise ValueError(
            f"No series have at least {min_cv_length} observations required for cross-validation horizon {test_size}."
        )

    initial_series = full_data['unique_id'].n_unique()
    df = full_data.filter(pl.col('unique_id').is_in(valid_ids))
    removed_series = initial_series - len(valid_ids)
    if removed_series > 0:
        print(
            f"  Removed {removed_series} series shorter than {min_cv_length} observations to satisfy cross-validation horizon"
        )

    # Additional filter: Remove series that would have insufficient data in test period
    # Require at least 30% non-null values in the test period for meaningful metrics
    min_test_coverage = 0.3  # Require at least 30% non-null values
    min_test_points = max(int(test_size * min_test_coverage), 3)  # At least 3 points

    series_with_sufficient_test_data = []
    for unique_id in df['unique_id'].unique():
        series_data = df.filter(pl.col('unique_id') == unique_id).sort('ds')
        # Get the last test_size observations
        test_period_data = series_data.tail(test_size)
        # Count non-null values in what would be the test period
        non_null_count = test_period_data['y'].drop_nulls().len()
        if non_null_count >= min_test_points:
            series_with_sufficient_test_data.append(unique_id)

    if len(series_with_sufficient_test_data) == 0:
        raise ValueError(
            f"No series have at least {min_test_points} non-null values in their last {test_size} observations (test period). "
            f"Data quality issue: all series have insufficient test data for reliable metrics."
        )

    initial_count = len(df['unique_id'].unique())
    df = df.filter(pl.col('unique_id').is_in(series_with_sufficient_test_data))
    removed_for_sparse = initial_count - len(series_with_sufficient_test_data)
    if removed_for_sparse > 0:
        print(
            f"  Removed {removed_for_sparse} series with <{min_test_points} non-null values in test period"
        )

    print(f"Total samples: {len(df):,}")
    print(f"Number of series: {df['unique_id'].n_unique()}")

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

    # Initialize StatsForecast
    sf = StatsForecast(
        models=models,
        freq=polars_frequency,
        n_jobs=-1,
        fallback_model=SeasonalNaive(season_length=seasonality),
        verbose=True
    )

    # Perform cross-validation with one window at the end
    print("\n4. Performing Cross-Validation")
    print("-" * 40)
    print(f"Forecast horizon: {test_size}")
    print("Cross-validation windows: 1 (end of series)")

    start_time = time.time()
    cv_df = sf.cross_validation(
        df=df,
        h=test_size,
        step_size=test_size,
        n_windows=1
    )
    cv_time = time.time() - start_time
    print(f"Cross-validation completed in {cv_time:.2f} seconds")

    # Evaluate models (cv_df is already in Polars format)
    print("\n5. Evaluating Model Performance")
    print("-" * 40)

    # Extract the cutoff date from cross-validation results
    cutoff_date = cv_df['cutoff'].unique()[0]

    # Create training data by filtering original data up to cutoff
    train_data = df.filter(pl.col('ds') <= cutoff_date)

    mase_scores, mse_scores, rmse_scores, r2oos_scores, actual_model_cols = evaluate_cv(cv_df, model_names, train_data, seasonality)

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
            print(f"  Warning: Only {valid_mase}/{total_series} series have valid MASE scores")

        avg_metrics[model_col] = {
            'MASE': mase_scores[model_col].mean(),
            'MSE': mse_scores[model_col].mean(),
            'RMSE': rmse_scores[model_col].mean(),
            'R2oos': r2oos_scores[model_col].mean()
        }

    # Create comparison table
    print("\n6. Model Performance Summary")
    print("-" * 40)

    comparison_data = [["Model", "Avg MASE", "Avg MSE", "Avg RMSE", "Avg R2oos"]]
    for model_col in actual_model_cols:
        comparison_data.append([
            model_col,
            f"{avg_metrics[model_col]['MASE']:.4f}",
            f"{avg_metrics[model_col]['MSE']:.4f}",
            f"{avg_metrics[model_col]['RMSE']:.4f}",
            f"{avg_metrics[model_col]['R2oos']:.4f}"
        ])

    print(tabulate(comparison_data, headers="firstrow", tablefmt="grid"))

    # Save CSV error metrics for the selected model
    print("\n7. Saving Error Metrics")
    print("-" * 40)

    # Create error metrics directory
    error_metrics_dir = f"./_output/forecasting/error_metrics/{DATASET_NAME}"
    os.makedirs(error_metrics_dir, exist_ok=True)

    # Get the selected model's metrics
    model_name = model_names[0]  # Should be only one model
    if model_name in avg_metrics:
        # Validate metrics before saving
        mase_val = avg_metrics[model_name]['MASE']
        mse_val = avg_metrics[model_name]['MSE']
        rmse_val = avg_metrics[model_name]['RMSE']
        r2oos_val = avg_metrics[model_name]['R2oos']

        # Check for invalid metric values
        import numpy as np
        if mase_val == 0.0:
            raise ValueError(
                f"MASE is exactly 0.0 for model {model_name}. "
                f"This indicates a calculation error, possibly due to data quality issues."
            )

        if np.isnan(mase_val) or np.isnan(mse_val) or np.isnan(rmse_val) or np.isnan(r2oos_val):
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
            "time_taken": [cv_time]
        }

        metrics_df = pl.DataFrame(metrics_data)
        csv_path = f"{error_metrics_dir}/{MODEL_NAME}.csv"
        metrics_df.write_csv(csv_path)
        print(f"Error metrics saved to: {csv_path}")
    else:
        print(f"Warning: Could not find metrics for {model_name}")

    print("\n" + "=" * 60)
    print("Forecast Statistics Complete!")
    print("=" * 60)
    print(f"Total time: {cv_time:.2f} seconds")


if __name__ == "__main__":
    main()
