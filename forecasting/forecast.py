"""
Unified CLI Forecasting Script

This script provides a unified interface to run forecasting experiments using either
StatsForecast or NeuralForecast models via CLI arguments. It supports all models
defined in models_config.toml and automatically loads dataset configurations from
datasets.toml.

Key Features:
- CLI interface with --dataset and --model arguments
- Support for both StatsForecast and NeuralForecast models
- Automatic dataset configuration loading from datasets.toml
- Uses full dataset (all entities, all years) for production-ready results
- Delegates metrics to utilsforecast.evaluation.evaluate (MASE/MAE/RMSE/sMAPE)
- Proper MASE denominator using clean, sorted train_df
- Supports parallel processing for applicable models
- Saves forecasts to CSV (metrics)

Usage:
    python forecast.py --dataset ftsfr_french_portfolios_25_daily_size_and_bm --model auto_arima_fast
    python forecast.py --dataset ftsfr_CRSP_monthly_stock_ret --model auto_lstm
"""

import argparse
import os
import time
import numpy as np
import polars as pl
import tomli
from pathlib import Path
from tabulate import tabulate
from functools import partial

from utilsforecast.preprocessing import fill_gaps
from utilsforecast.losses import mase, mae, rmse, smape
from utilsforecast.evaluation import evaluate

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


def load_model_config():
    """Load model configurations from models_config.toml file."""
    models_config_path = FILE_DIR / "models_config.toml"
    if not models_config_path.exists():
        raise FileNotFoundError(f"models_config.toml not found at {models_config_path}")
    with open(models_config_path, "rb") as f:
        return tomli.load(f)


def create_model(model_name, seasonality, model_configs, dataset_name=None, forecast_horizon=None):
    """Create a model instance based on TOML configuration."""
    if model_name not in model_configs:
        available = ", ".join(model_configs.keys())
        raise ValueError(f"Unknown model: {model_name}. Available: {available}")

    config = model_configs[model_name]
    library = config["library"]
    model_class = config["class"]
    params = config.get("params", {}).copy()

    # Add seasonality (StatsForecast) where applicable
    if library == "statsforecast":
        models_without_season_length = [
            "SimpleExponentialSmoothingOptimized",
            "SimpleExponentialSmoothing",
            "Naive",
        ]
        if (
            model_class not in models_without_season_length
            and "season_length" not in params
        ):
            params["season_length"] = seasonality

    # Adjust horizon for NeuralForecast models at instantiation
    if library == "neuralforecast" and forecast_horizon is not None:
        params["h"] = int(forecast_horizon)
    
    # Add trainer args for NeuralForecast models to redirect logs
    if library == "neuralforecast" and dataset_name is not None:
        params["default_root_dir"] = f"./_output/forecasting2/logs/{dataset_name}/{model_name}"

    if library == "statsforecast":
        from statsforecast import models as sf_models

        model_cls = getattr(sf_models, model_class)
        return model_cls(**params)

    elif library == "neuralforecast":
        # Intentional compatibility fallback between Auto API and classic models.
        try:
            from neuralforecast import auto as nf_auto

            model_cls = getattr(nf_auto, model_class)
        except (ImportError, AttributeError):
            from neuralforecast import models as nf_models

            model_cls = getattr(nf_models, model_class)

        # Convert loss strings to loss classes if present
        if "loss" in params and isinstance(params["loss"], str):
            from neuralforecast.losses.pytorch import (
                MAE as NfMAE,
                MSE as NfMSE,
                DistributionLoss,
            )

            loss_map = {
                "MAE": NfMAE(),
                "MSE": NfMSE(),
                "DistributionLoss": DistributionLoss(distribution="Normal"),
            }
            if params["loss"] in loss_map:
                params["loss"] = loss_map[params["loss"]]
        if "valid_loss" in params and isinstance(params["valid_loss"], str):
            from neuralforecast.losses.pytorch import (
                MAE as NfMAE,
                MSE as NfMSE,
                DistributionLoss,
            )

            loss_map = {
                "MAE": NfMAE(),
                "MSE": NfMSE(),
                "DistributionLoss": DistributionLoss(distribution="Normal"),
            }
            if params["valid_loss"] in loss_map:
                params["valid_loss"] = loss_map[params["valid_loss"]]
        return model_cls(**params)

    else:
        raise ValueError(f"Unsupported library: {library}")


def load_and_preprocess_data(data_path, frequency="D", test_split=0.2):
    """Load and preprocess the dataset using Polars throughout (full dataset)."""
    print("Loading and preprocessing data...")

    df = pl.read_parquet(data_path)
    # Rename 'id' to 'unique_id' if needed
    if "id" in df.columns:
        df = df.rename({"id": "unique_id"})

    drop_cols = [c for c in df.columns if c.startswith("__index_level_")]
    if drop_cols: df = df.drop(drop_cols)
    df = df.select(["unique_id", "ds", "y"])


    print(f"Using full dataset: {len(df['unique_id'].unique())} entities")

    # Ensure proper dtypes & guard against inf/nan
    df = df.with_columns(pl.col("y").cast(pl.Float32))
    df = df.with_columns(
        pl.when((pl.col("y").is_infinite()) | (pl.col("y").is_nan()))
        .then(None)
        .otherwise(pl.col("y"))
        .alias("y")
    )

    # Fill date grid: avoid padding leading nulls (start='per_serie'); keep aligned tail
    polars_freq = convert_frequency_to_statsforecast(frequency)
    df = fill_gaps(df, freq=polars_freq, start="per_serie", end="global")

    # Train/test split on global timeline
    unique_dates = df["ds"].unique().sort()
    split_idx = int(len(unique_dates) * (1 - test_split))
    train_cutoff = unique_dates[split_idx - 1]

    train_data = df.filter(pl.col("ds") <= train_cutoff)
    test_data = df.filter(pl.col("ds") > train_cutoff)

    print(
        f"Data split: {len(train_data)} training samples, {len(test_data)} test samples"
    )
    print(f"Total entities: {len(df['unique_id'].unique())}")
    return train_data, test_data, df


def train_and_forecast_statsforecast(model, train_data, test_data, frequency):
    """Train and forecast using StatsForecast."""
    print("Training model and generating forecasts using StatsForecast...")
    from statsforecast import StatsForecast
    from statsforecast.models import Naive

    n_jobs = int(os.getenv("STATSFORECAST_N_JOBS", os.cpu_count() or 1))
    print(f"Using {n_jobs} cores for parallel processing")

    statsforecast_freq = convert_frequency_to_statsforecast(frequency)
    print(f"Train data shape: {train_data.shape}")

    # Trim trailing nulls per id so last train point is valid
    train_data_clean = []
    for entity in train_data["unique_id"].unique():
        entity_data = train_data.filter(pl.col("unique_id") == entity)
        non_null_data = entity_data.filter(pl.col("y").is_not_null())
        if len(non_null_data) > 0:
            last_non_null_date = non_null_data["ds"].max()
            entity_data_trimmed = entity_data.filter(pl.col("ds") <= last_non_null_date)
            train_data_clean.append(entity_data_trimmed)

    train_data_filtered = (
        pl.concat(train_data_clean) if train_data_clean else train_data
    )
    print(
        f"Trimmed training data to remove trailing nulls: {train_data_filtered.shape}"
    )

    fallback = Naive()
    sf = StatsForecast(
        models=[model], freq=statsforecast_freq, n_jobs=n_jobs, fallback_model=fallback
    )

    forecast_horizon = int(test_data["ds"].n_unique())
    forecasts = sf.forecast(df=train_data_filtered, h=forecast_horizon)
    print(f"Generated {len(forecasts)} forecasts")
    return forecasts


def train_and_forecast_neuralforecast(model, train_data, test_data, frequency):
    """Train and forecast using NeuralForecast."""
    print("Training model and generating forecasts using NeuralForecast...")
    from neuralforecast import NeuralForecast

    polars_freq = convert_frequency_to_statsforecast(frequency)

    # Clean train: trim to last non-null, then ffill/bfill internals
    train_data_clean = []
    for entity in train_data["unique_id"].unique():
        entity_data = train_data.filter(pl.col("unique_id") == entity)
        non_null_data = entity_data.filter(pl.col("y").is_not_null())
        if len(non_null_data) > 0:
            last_non_null_date = non_null_data["ds"].max()
            entity_data_trimmed = entity_data.filter(pl.col("ds") <= last_non_null_date)
            entity_data_filled = entity_data_trimmed.with_columns(
                pl.col("y").fill_null(strategy="forward").fill_null(strategy="backward")
            )
            train_data_clean.append(entity_data_filled)

    train_data_filtered = (
        pl.concat(train_data_clean)
        if train_data_clean
        else train_data.with_columns(
            pl.col("y").fill_null(strategy="forward").fill_null(strategy="backward")
        )
    )

    nf = NeuralForecast(models=[model], freq=polars_freq)
    nf.fit(df=train_data_filtered)

    forecasts = nf.predict()
    print(f"Generated {len(forecasts)} forecasts")
    return forecasts


def save_metrics_csv(metrics_dict, dataset_name, model_name):
    """Save error metrics to CSV file in the specified directory structure."""
    output_dir = Path("./_output/forecasting2/error_metrics") / dataset_name
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"{model_name}.csv"
    pl.DataFrame([metrics_dict]).write_csv(csv_path)
    print(f"Error metrics saved to: {csv_path}")
    return csv_path


def calculate_global_metrics(train_data, test_data, forecasts, seasonality, model_name):
    """Compute global MASE, sMAPE, MAE, RMSE using utilsforecast.evaluation.evaluate."""
    print("Calculating global metrics (MASE, sMAPE, MAE, RMSE)...")

    forecasts_pl = forecasts  # ok for StatsForecast
    forecast_cols = [c for c in forecasts_pl.columns if c not in ("unique_id", "ds")]
    # For StatsForecast this should be ["Naive"] or ["SeasonalNaive"], etc.
    assert forecast_cols, "No forecast columns found"
    pred_col = forecast_cols[0]
    print("Using prediction column:", pred_col)


    # Join test with forecasts
    test_with_forecasts = test_data.join(
        forecasts_pl, on=["unique_id", "ds"], how="inner"
    )
    if len(test_with_forecasts) == 0:
        raise ValueError("No matching forecasts found for test data.")

    # Find prediction column
    prediction_cols = [
        c for c in test_with_forecasts.columns if c not in ("unique_id", "ds", "y")
    ]
    if not prediction_cols:
        raise ValueError("No prediction columns found in forecasts.")
    pred_col = prediction_cols[0]
    print(f"Using prediction column: {pred_col}")

    eval_df = (
        test_with_forecasts.select("unique_id", "ds", "y", pred_col)
        .drop_nulls(["y", pred_col])
        .filter(pl.col("y").is_finite() & pl.col(pred_col).is_finite())
        .sort(["unique_id", "ds"])
    )


    # Clean train for MASE denominator: drop nulls, sort
    train_clean = (
        train_data.select("unique_id", "ds", "y")
        .drop_nulls(["y"])
        .sort(["unique_id", "ds"])
    )

    # Keep ids with enough non-null history for seasonal differencing
    ok_ids = (
        train_clean.group_by("unique_id")
        .agg(pl.len().alias("n"))
        .filter(pl.col("n") >= seasonality + 1)
        .get_column("unique_id")
    )
    train_clean = train_clean.filter(pl.col("unique_id").is_in(ok_ids))
    eval_df = eval_df.filter(pl.col("unique_id").is_in(ok_ids))

    if len(eval_df) == 0:
        raise ValueError("No series with sufficient history for evaluation.")

    print(
        f"Evaluating {len(eval_df['unique_id'].unique())} series with sufficient history"
    )

    # seasonality-aware MASE metric
    seasonality_mase = partial(mase, seasonality=seasonality)
    setattr(seasonality_mase, "__name__", "mase")  # so evaluator names the row 'mase'

    # Delegate to Nixtla's evaluator; aggregate by mean across ids
    metrics_results = evaluate(
        df=eval_df,
        metrics=[seasonality_mase, mae, rmse, smape],
        train_df=train_clean,
        models=[pred_col],
        id_col="unique_id",
        time_col="ds",
        target_col="y",
        agg_fn="mean",
    )

    def get_metric(row_name: str) -> float | None:
        row = metrics_results.filter(pl.col("metric") == row_name)
        if row.height == 0:
            return None
        return float(row.select(pl.col(pred_col)).to_series().item())

    global_mase = get_metric("mase")
    global_mae = get_metric("mae")
    global_rmse = get_metric("rmse")
    global_smape = get_metric("smape")

    vals = [global_mase, global_smape, global_mae, global_rmse]
    val_names = ["MASE", "sMAPE", "MAE", "RMSE"]
    
    # Handle infinite MASE by setting to a large but finite value
    if global_mase is not None and np.isinf(global_mase):
        print("WARNING: MASE is infinite (perfect seasonal naive forecast), setting to 999.0")
        global_mase = 999.0
    
    # Check for remaining invalid values
    vals = [global_mase, global_smape, global_mae, global_rmse]
    for i, (v, name) in enumerate(zip(vals, val_names)):
        if v is None or (isinstance(v, float) and (np.isnan(v) or np.isinf(v))):
            print(f"ERROR: {name} metric is invalid: {v}")
    
    if any(
        v is None or (isinstance(v, float) and (np.isnan(v) or np.isinf(v)))
        for v in vals
    ):
        raise ValueError("One or more metric calculations returned NaN/Inf.")

    return global_mase, global_smape, global_mae, global_rmse


def main():
    parser = argparse.ArgumentParser(description="Unified CLI Forecasting Script")
    parser.add_argument(
        "--dataset", required=True, help="Dataset name from datasets.toml"
    )
    parser.add_argument(
        "--model", required=True, help="Model name from models_config.toml"
    )
    parser.add_argument(
        "--test-split", type=float, default=0.2, help="Test split ratio (default: 0.2)"
    )
    args = parser.parse_args()

    print("=" * 70)
    print("Forecasting Script")
    print("=" * 70)

    # Load configurations
    dataset_config = read_dataset_config(args.dataset)
    model_configs = load_model_config()
    print(f"\nDataset: {args.dataset}")
    print(f"Description: {dataset_config['description']}")
    print(f"Model: {args.model}")
    print(f"Display Name: {model_configs[args.model]['display_name']}")
    print(f"Frequency: {dataset_config['frequency']}")
    print(f"Seasonality: {dataset_config['seasonality']}")

    # Load & preprocess
    train_data, test_data, full_data = load_and_preprocess_data(
        dataset_config["data_path"], dataset_config["frequency"], args.test_split
    )

    # Compute test horizon BEFORE model creation (needed for NeuralForecast)
    test_size = int(test_data["ds"].n_unique())

    # Create model
    model = create_model(
        args.model,
        dataset_config["seasonality"],
        model_configs,
        dataset_name=args.dataset,
        forecast_horizon=test_size,
    )
    library = model_configs[args.model]["library"]

    # Train & forecast
    print("\nStarting training and forecasting...")
    forecast_start_time = time.time()
    if library == "statsforecast":
        forecasts = train_and_forecast_statsforecast(
            model, train_data, test_data, dataset_config["frequency"]
        )
    else:
        forecasts = train_and_forecast_neuralforecast(
            model, train_data, test_data, dataset_config["frequency"]
        )
    forecast_time = time.time() - forecast_start_time
    print(f"Forecasting completed in {forecast_time:.2f} seconds")

    # Evaluate
    global_mase, global_smape, global_mae, global_rmse = calculate_global_metrics(
        train_data, test_data, forecasts, dataset_config["seasonality"], args.model
    )

    # Report
    print("\nFinal Results:")
    results_table = [
        ["Model", model_configs[args.model]["display_name"]],
        ["Library", library.title()],
        ["Dataset", args.dataset],
        ["Entities", len(full_data["unique_id"].unique())],
        ["Frequency", dataset_config["frequency"]],
        ["Seasonality", dataset_config["seasonality"]],
        ["Test Size (h)", test_size],
        ["Global MASE", f"{global_mase:.4f}"],
        ["Global sMAPE", f"{global_smape:.4f}"],
        ["Global MAE", f"{global_mae:.4f}"],
        ["Global RMSE", f"{global_rmse:.4f}"],
        ["Forecast Time (s)", f"{forecast_time:.2f}"],
    ]
    print(tabulate(results_table, tablefmt="fancy_grid"))

    metrics_dict = {
        "Model": model_configs[args.model]["display_name"],
        "Library": library.title(),
        "Dataset": args.dataset,
        "Entities": len(full_data["unique_id"].unique()),
        "Frequency": dataset_config["frequency"],
        "Seasonality": dataset_config["seasonality"],
        "Test_Size_h": test_size,
        "Global_MASE": global_mase,
        "Global_sMAPE": global_smape,
        "Global_MAE": global_mae,
        "Global_RMSE": global_rmse,
        "Forecast_Time_seconds": forecast_time,
    }
    save_metrics_csv(metrics_dict, args.dataset, args.model)
    print("Forecasting experiment completed successfully!")

if __name__ == "__main__":
    main()
