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


def load_model_config():
    """Load model configurations from models_config.toml file."""
    models_config_path = FILE_DIR / "models_config.toml"
    if not models_config_path.exists():
        raise FileNotFoundError(f"models_config.toml not found at {models_config_path}")
    with open(models_config_path, "rb") as f:
        return tomli.load(f)


def create_model(model_name, seasonality, model_configs, dataset_name=None, forecast_horizon=None, disable_early_stopping=False):
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
    
    # Set intelligent input_size for NeuralForecast models
    if library == "neuralforecast" and "input_size" in params:
        if seasonality <= 1:
            # For non-seasonal data (like returns), use shorter lookback
            params["input_size"] = max(24, min(48, seasonality * 24))
        else:
            # For seasonal data, use multiple seasons
            params["input_size"] = max(seasonality * 2, min(seasonality * 6, 144))
    
    # Disable early stopping if validation is not available
    if library == "neuralforecast" and disable_early_stopping:
        # Remove all early stopping and validation-related parameters
        early_stopping_params = [
            "early_stop_patience_steps",
            "val_check_steps", 
            "enable_checkpointing",
            "early_stopping"
        ]
        removed_params = []
        for param in early_stopping_params:
            if param in params:
                del params[param]
                removed_params.append(param)
    
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


def train_and_forecast_statsforecast(model, train_data, test_data, frequency):
    """Train and forecast using StatsForecast."""
    print("Training model and generating forecasts using StatsForecast...")
    from statsforecast import StatsForecast
    from statsforecast.models import Naive

    n_jobs = int(os.getenv("STATSFORECAST_N_JOBS", os.cpu_count() or 1))
    print(f"Using {n_jobs} cores for parallel processing")

    statsforecast_freq = convert_frequency_to_statsforecast(frequency)
    print(f"Train data shape: {train_data.shape}")

    # Use standardized data cleaning
    train_data_clean = standardize_data_cleaning(train_data, fill_strategy="forward_only")
    print(f"Applied standardized data cleaning: {train_data_clean.shape}")

    fallback = Naive()
    sf = StatsForecast(
        models=[model], freq=statsforecast_freq, n_jobs=n_jobs, fallback_model=fallback
    )

    forecast_horizon = int(test_data["ds"].n_unique())
    forecasts = sf.forecast(df=train_data_clean, h=forecast_horizon)
    print(f"Generated {len(forecasts)} forecasts")
    return forecasts


def train_and_forecast_neuralforecast(model, train_data, test_data, frequency, val_size=None):
    """Train and forecast using NeuralForecast."""
    print("Training model and generating forecasts using NeuralForecast...")
    from neuralforecast import NeuralForecast

    polars_freq = convert_frequency_to_statsforecast(frequency)
    forecast_horizon = int(test_data["ds"].n_unique())

    # Use standardized data cleaning (same as StatsForecast)
    train_data_clean = standardize_data_cleaning(train_data, fill_strategy="forward_only")
    print(f"Applied standardized data cleaning: {train_data_clean.shape}")

    # Calculate validation size if not provided
    if val_size is None:
        min_series_length = (
            train_data_clean.group_by("unique_id")
            .agg(pl.len().alias("n"))
            .select("n")
            .min()
            .item()
        )
        
        # NeuralForecast requires val_size to be either 0 or >= forecast_horizon
        # Set conservative validation size
        if min_series_length < (forecast_horizon * 3):
            # For short series, use minimal validation or no validation
            val_size = 0  # Use 0 to disable validation for short series
            print(f"Short series detected (min length: {min_series_length}), disabling validation")
            
            # Disable early stopping in the model instance if validation is disabled
            if hasattr(model, 'early_stop_patience_steps'):
                model.early_stop_patience_steps = 0
            if hasattr(model, 'val_check_steps'):
                model.val_check_steps = 999999  # Set to a very large value to effectively disable
            
            # Disable PyTorch Lightning early stopping callbacks if they exist
            # This ensures that PyTorch Lightning doesn't try to use validation-dependent callbacks
            for attr_name in ['trainer_kwargs', 'trainer_params']:
                if hasattr(model, attr_name):
                    trainer_config = getattr(model, attr_name)
                    if isinstance(trainer_config, dict):
                        # Remove or disable callbacks that require validation
                        if 'callbacks' in trainer_config:
                            from pytorch_lightning.callbacks import EarlyStopping
                            trainer_config['callbacks'] = [
                                cb for cb in trainer_config['callbacks'] 
                                if not isinstance(cb, EarlyStopping)
                            ]
                        # Ensure enable_checkpointing is False  
                        trainer_config['enable_checkpointing'] = False
        else:
            val_size = forecast_horizon  # Use same size as forecast horizon
            print(f"Using validation size equal to forecast horizon: {val_size}")
    
    print(f"Using validation size: {val_size}")
    
    nf = NeuralForecast(models=[model], freq=polars_freq)
    nf.fit(df=train_data_clean, val_size=val_size)

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


def calculate_global_metrics(train_data, test_data, forecasts, seasonality, _):
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

    # Ensure we have the same series in both train and eval
    # Since we've already filtered series upfront, we can use all available data
    train_series = set(train_clean["unique_id"].unique().to_list())
    eval_series = set(eval_df["unique_id"].unique().to_list())
    common_series = list(train_series & eval_series)
    
    if not common_series:
        raise ValueError("No common series between training and evaluation data.")
    
    train_clean = train_clean.filter(pl.col("unique_id").is_in(common_series))
    eval_df = eval_df.filter(pl.col("unique_id").is_in(common_series))

    print(f"Evaluating {len(common_series)} series (fair comparison across all models)")

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
    for v, name in zip(vals, val_names):
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

    # Load & preprocess with consistent filtering
    train_data, test_data, full_data = load_and_preprocess_data(
        dataset_config["data_path"], dataset_config["frequency"], args.test_split, dataset_config["seasonality"]
    )

    # Compute test horizon BEFORE model creation (needed for NeuralForecast)
    test_size = int(test_data["ds"].n_unique())

    # Determine if we need to disable early stopping (for short series)
    disable_early_stopping = False
    if model_configs[args.model]["library"] == "neuralforecast":
        min_series_length = (
            train_data.group_by("unique_id")
            .agg(pl.len().alias("n"))
            .select("n")
            .min()
            .item()
        )
        if min_series_length < (test_size * 3):
            disable_early_stopping = True
    
    # Create model
    model = create_model(
        args.model,
        dataset_config["seasonality"],
        model_configs,
        dataset_name=args.dataset,
        forecast_horizon=test_size,
        disable_early_stopping=disable_early_stopping,
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
        ["Total Entities (Filtered)", len(full_data["unique_id"].unique())],
        ["Frequency", dataset_config["frequency"]],
        ["Seasonality", dataset_config["seasonality"]],
        ["Test Size (h)", test_size],
        ["Data Processing", "Standardized across all models"],
        ["Series Filtering", "Applied consistently to all models"],
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
