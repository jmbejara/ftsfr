"""
Simplified StatsForecast Example Script

This script demonstrates a simplified approach to time series forecasting using StatsForecast
with built-in functions for train/test splitting and metric calculation. Dataset configurations
are automatically loaded from datasets.toml.

Key Features:
- Automatically reads dataset configs (frequency, seasonality, paths) from datasets.toml
- Uses AutoARIMA with fast configuration (approximation=True, stepwise=True, limited model search)
- Performs simple train/test split (80%/20%)
- Uses utilsforecast.losses.mase() for accurate MASE calculation and numpy for RMSE
- Uses built-in StatsForecast.forecast() for predictions
- Returns None instead of invalid values when calculations fail
- Supports parallel processing
- Saves forecasts to parquet format

Usage:
- Simply change the dataset_name in the __main__ block to any dataset from datasets.toml
- The script will automatically use the correct frequency, seasonality, and data path
- Processes the full dataset by default
"""

import os
import time
import numpy as np
import polars as pl
import tomli
from pathlib import Path
from tabulate import tabulate
from utilsforecast.preprocessing import fill_gaps
from utilsforecast.losses import mase
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA

FILE_DIR = Path(__file__).parent
REPO_ROOT = FILE_DIR.parent


def read_dataset_config(dataset_name):
    """Read dataset configuration from datasets.toml file."""
    datasets_path = REPO_ROOT / "datasets.toml"

    if not datasets_path.exists():
        raise FileNotFoundError(f"datasets.toml not found at {datasets_path}")

    with open(datasets_path, "rb") as f:
        config = tomli.load(f)

    # Find the dataset configuration
    dataset_config = None
    data_path = None

    for module_name, module_config in config.items():
        if isinstance(module_config, dict) and not module_name.startswith("_"):
            # Check if this module has our dataset
            for dataset_key, dataset_info in module_config.items():
                if dataset_key == dataset_name and isinstance(dataset_info, dict):
                    dataset_config = dataset_info
                    # Construct the data path
                    data_path = (
                        REPO_ROOT / "_data" / module_name / f"{dataset_name}.parquet"
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


def load_and_preprocess_data(
    data_path,
    frequency="D",
    test_split=0.2,
):
    """Load and preprocess the dataset using Polars throughout."""
    print("Loading and preprocessing data...")

    # Load data using polars
    df = pl.read_parquet(data_path)

    # Rename 'id' to 'unique_id' as expected by statsforecast
    if "id" in df.columns:
        df = df.rename({"id": "unique_id"})

    # Ensure proper data types
    df = df.with_columns(pl.col("y").cast(pl.Float32))

    # Handle infinite values
    df = df.with_columns(
        pl.when((pl.col("y").is_infinite()) | (pl.col("y").is_nan()))
        .then(None)
        .otherwise(pl.col("y"))
        .alias("y")
    )

    # Fill missing dates
    # Note: fill_gaps requires Polars-specific frequency strings for Polars DataFrames
    # Convert pandas-style frequency to Polars format
    if frequency == "D":
        polars_freq = "1d"
    elif frequency == "W":
        polars_freq = "1w"
    elif frequency in ["M", "MS"]:
        polars_freq = "1mo"
    elif frequency in ["Y", "YS"]:
        polars_freq = "1y"
    else:
        polars_freq = frequency  # Assume it's already in Polars format

    df = fill_gaps(df, freq=polars_freq, start="global", end="global")

    # Calculate train/test split
    unique_dates = df["ds"].unique().sort()
    split_idx = int(len(unique_dates) * (1 - test_split))
    train_cutoff = unique_dates[split_idx - 1]

    # Split into train and test
    train_data = df.filter(pl.col("ds") <= train_cutoff)
    test_data = df.filter(pl.col("ds") > train_cutoff)

    print(
        f"Data split: {len(train_data)} training samples, {len(test_data)} test samples"
    )
    print(f"Total entities: {len(df['unique_id'].unique())}")

    return train_data, test_data, df


def create_autoarima_model(seasonality=252):
    """Create AutoARIMA model with fast configuration parameters."""
    return AutoARIMA(
        season_length=seasonality,
        approximation=True,
        stepwise=True,
        max_p=2,
        max_q=2,
        max_P=1,
        max_Q=1,
        nmodels=5,
    )


def train_and_forecast(sf_model, train_data, test_data):
    """Simple train and forecast using built-in StatsForecast functionality with Polars."""
    print("Training model and generating forecasts...")

    # Generate forecasts for test period
    forecast_horizon = len(test_data["ds"].unique())
    forecasts = sf_model.forecast(df=train_data, h=forecast_horizon)

    print(f"Generated {len(forecasts)} forecasts")
    return forecasts


def calculate_global_metrics(train_data, test_data, forecasts, seasonality=252):
    """Calculate global MASE and RMSE metrics using Polars."""
    print("Calculating global MASE and RMSE...")

    try:
        # Forecasts might be a pandas DataFrame from StatsForecast, convert if needed
        if not isinstance(forecasts, pl.DataFrame):
            forecasts_pl = pl.from_pandas(forecasts.reset_index())
        else:
            forecasts_pl = forecasts

        # Merge test data with forecasts
        test_with_forecasts = test_data.join(
            forecasts_pl, on=["unique_id", "ds"], how="inner"
        )

        if len(test_with_forecasts) == 0:
            print("Error: No matching forecasts found for test data")
            return None, None

        # Check for required columns
        if "AutoARIMA" not in test_with_forecasts.columns:
            print("Error: AutoARIMA predictions not found in forecasts")
            return None, None

        # Calculate MASE using utilsforecast function (works with Polars DataFrames)
        mase_results = mase(
            df=test_with_forecasts,
            models=["AutoARIMA"],
            seasonality=seasonality,
            train_df=train_data,
            id_col="unique_id",
            target_col="y",
        )

        # Calculate global MASE (mean across all entities)
        # mase_results is a Polars DataFrame with columns unique_id and AutoARIMA
        global_mase = mase_results["AutoARIMA"].mean()

        # Calculate global RMSE using Polars expressions
        rmse_calc = test_with_forecasts.select(
            [((pl.col("y") - pl.col("AutoARIMA")) ** 2).alias("squared_error")]
        ).filter(
            pl.col("squared_error").is_not_null() & pl.col("squared_error").is_not_nan()
        )

        if len(rmse_calc) == 0:
            print("Warning: No valid values for RMSE calculation")
            return None, None

        global_rmse = np.sqrt(rmse_calc["squared_error"].mean())

        if global_mase is None or np.isnan(global_mase) or np.isnan(global_rmse):
            print("Warning: Metric calculation returned NaN")
            return None, None

        return global_mase, global_rmse

    except Exception as e:
        print(f"Error calculating metrics: {str(e)}")
        return None, None


def main(
    data_path,
    dataset_name,
    frequency,
    seasonality,
    model_name="auto_arima_fast",
    test_split=0.2,
):
    start_time = time.time()
    
    print("=" * 60)
    print("Vanilla StatsForecast Example - AutoARIMA Fast")
    print("=" * 60)

    # Load and preprocess data
    train_data, test_data, full_data = load_and_preprocess_data(
        data_path, frequency, test_split
    )

    # Calculate test size for forecasting
    test_size = len(sorted(test_data["ds"].unique()))

    # Print initialization summary
    print("\nObject Initialized:")
    print(
        tabulate(
            [
                ["Model", model_name],
                ["Dataset", dataset_name],
                ["Total Entities", len(full_data["unique_id"].unique())],
                ["Test Size (h)", test_size],
            ],
            tablefmt="fancy_grid",
        )
    )

    # Create model
    print("\nCreating AutoARIMA model with fast configuration...")
    model = create_autoarima_model(seasonality)

    # Create StatsForecast wrapper
    n_jobs = int(os.getenv("STATSFORECAST_N_JOBS", os.cpu_count() or 1))
    print(f"Using {n_jobs} cores for parallel processing")

    # StatsForecast needs Polars-compatible frequency for Polars DataFrames
    # Convert pandas-style frequency to Polars format
    if frequency == "D":
        statsforecast_freq = "1d"
    elif frequency == "W":
        statsforecast_freq = "1w"
    elif frequency in ["M", "MS"]:
        statsforecast_freq = "1mo"
    elif frequency in ["Y", "YS"]:
        statsforecast_freq = "1y"
    else:
        statsforecast_freq = frequency

    sf = StatsForecast(models=[model], freq=statsforecast_freq, n_jobs=n_jobs)

    # Train model and generate forecasts
    forecasts = train_and_forecast(sf, train_data, test_data)

    # Calculate global metrics using built-in functions
    global_mase, global_rmse = calculate_global_metrics(
        train_data, test_data, forecasts, seasonality
    )

    # Calculate total runtime
    end_time = time.time()
    total_runtime = end_time - start_time

    # Print results summary
    print("\nFinal Results:")
    mase_display = f"{global_mase:.4f}" if global_mase is not None else "Error"
    rmse_display = f"{global_rmse:.4f}" if global_rmse is not None else "Error"
    runtime_display = f"{total_runtime:.2f} seconds"
    print(
        tabulate(
            [
                ["Model", model_name],
                ["Dataset", dataset_name],
                ["Entities", len(full_data["unique_id"].unique())],
                ["Frequency", frequency],
                ["Seasonality", seasonality],
                ["Test Size (h)", test_size],
                ["Global MASE", mase_display],
                ["Global RMSE", rmse_display],
                ["Total Runtime", runtime_display],
            ],
            tablefmt="fancy_grid",
        )
    )

    # Save forecasts
    output_dir = FILE_DIR / "forecasting_examples_output"
    output_dir.mkdir(exist_ok=True)
    forecast_path = output_dir / "ex_statsforecast_forecasts.parquet"

    # Save forecasts (convert from pandas if needed)
    if not isinstance(forecasts, pl.DataFrame):
        pred_data_pl = pl.from_pandas(forecasts.reset_index())
    else:
        pred_data_pl = forecasts
    pred_data_pl.write_parquet(forecast_path)
    print(f"\nForecasts saved to: {forecast_path}")

    print("\n" + "=" * 60)
    print("StatsForecast example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    # Specify the dataset name here - it will auto-load configs from datasets.toml
    dataset_name = "ftsfr_french_portfolios_25_daily_size_and_bm"
    # dataset_name = "ftsfr_CRSP_monthly_stock_ret"
    # dataset_name = "ftsfr_CDS_bond_basis_non_aggregated"

    # Read configuration from datasets.toml
    config = read_dataset_config(dataset_name)
    print(f"Loaded configuration for: {dataset_name}")
    print(f"Description: {config['description']}")

    # Call main with the loaded configuration
    main(
        data_path=config["data_path"],
        dataset_name=config["dataset_name"],
        frequency=config["frequency"],
        seasonality=config["seasonality"],
    )
