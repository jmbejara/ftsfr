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
    read_dataset_config,
    load_and_preprocess_data,
    get_test_size_from_frequency,
    convert_pandas_freq_to_polars,
    evaluate_cv,
    filter_series_by_cv_requirements
)

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
    AutoCES
)

warnings.filterwarnings("ignore")


def main():
    """Main function for forecast statistics."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Statistical Forecasting with StatsForecast Models")
    parser.add_argument("--dataset", required=True, help="Dataset name from datasets.toml")
    parser.add_argument("--model", required=True,
                       choices=["historic_average", "seasonal_naive", "auto_arima", "auto_ces",
                               "auto_ets", "croston", "dot", "holt_winters", "ses", "theta"],
                       help="Statistical model to use")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode for faster testing with limited data")
    args = parser.parse_args()

    DATASET_NAME = args.dataset
    MODEL_NAME = args.model
    DEBUG_MODE = args.debug

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
    frequency = dataset_config['frequency']
    seasonality = dataset_config['seasonality']

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

    # Filter series based on cross-validation requirements
    df = filter_series_by_cv_requirements(full_data, test_size, debug=DEBUG_MODE)

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

    mase_scores, mse_scores, rmse_scores, r2oos_scores, actual_model_cols = evaluate_cv(cv_df, train_data, seasonality)

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
