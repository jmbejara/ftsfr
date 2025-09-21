"""
Neural Cross-Validation Forecasting Script

This script demonstrates cross-validation forecasting using NeuralForecast
with automatic hyperparameter optimization for neural network models,
along with baseline models from StatsForecast.

Usage:
    python forecast_neural.py --dataset ftsfr_he_kelly_manela_factors_monthly --model auto_deepar
"""

import warnings
import time
import argparse
import polars as pl
import pandas as pd
from pathlib import Path
from tabulate import tabulate
import os
import multiprocessing
import torch

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

from neuralforecast import NeuralForecast
from neuralforecast.auto import (
    AutoDeepAR,
    AutoNBEATS,
    AutoNHITS,
    AutoDLinear,
    AutoNLinear,
    AutoVanillaTransformer,
    AutoTiDE,
    AutoKAN,
)
from neuralforecast.losses.pytorch import MAE, DistributionLoss

from statsforecast import StatsForecast
from statsforecast.models import HistoricAverage, SeasonalNaive

warnings.filterwarnings("ignore")

# Default NUM_SAMPLES - overridden by debug mode
NUM_SAMPLES = 20


# Hardware detection functions
def detect_hardware():
    """Detect available hardware and configure optimal settings."""
    cpu_count = os.cpu_count() or multiprocessing.cpu_count()

    # Check for different GPU backends
    cuda_available = torch.cuda.is_available()
    cuda_count = torch.cuda.device_count() if cuda_available else 0

    mps_available = hasattr(torch.backends, "mps") and torch.backends.mps.is_available()

    print("Hardware detected:")
    print(f"  CPUs: {cpu_count}")
    print(f"  CUDA GPUs: {cuda_count}")
    print(f"  MPS available: {mps_available}")

    # Configure Lightning accelerator and devices (prioritize CUDA > MPS > CPU)
    if cuda_count > 1:
        accelerator = "gpu"  # CUDA
        devices = cuda_count
        strategy = "ddp"
        print(f"  Using multi-CUDA GPU training with {cuda_count} GPUs")
    elif cuda_count == 1:
        accelerator = "gpu"  # CUDA
        devices = 1
        strategy = "auto"
        print("  Using single CUDA GPU training")
    elif mps_available:
        accelerator = "mps"  # Apple Silicon
        devices = 1
        strategy = "auto"
        print("  Using Apple MPS GPU training")
    else:
        accelerator = "cpu"
        devices = 1
        strategy = "auto"
        print("  Using CPU training")

    # Configure workers and parallel jobs based on CPU count
    # Conservative estimates to avoid overwhelming the system
    num_workers = max(1, min(cpu_count // 4, 16))
    optuna_jobs = max(1, min(cpu_count // 8, 8))

    # For high-core systems, be more aggressive with Optuna parallelization
    if cpu_count >= 32:
        optuna_jobs = min(cpu_count // 4, 16)
    elif cpu_count >= 16:
        optuna_jobs = min(cpu_count // 4, 8)

    print(f"  Data loading workers: {num_workers}")
    print(f"  Optuna parallel jobs: {optuna_jobs}")

    return {
        "cpu_count": cpu_count,
        "cuda_count": cuda_count,
        "mps_available": mps_available,
        "accelerator": accelerator,
        "devices": devices,
        "strategy": strategy,
        "num_workers": num_workers,
        "optuna_jobs": optuna_jobs,
    }


def create_auto_config_nhits(
    seasonality, lightning_logs_dir=None, debug=False, hardware_config=None
):
    """Create configuration for AutoNHITS with optuna backend."""

    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size",
                (6, 12) if debug else (12, 24, 48),  # Smaller for debug
            ),
            "start_padding_enabled": True,  # Enable padding for short series
            "n_blocks": 5 * [1],
            "mlp_units": 5 * [[64, 64]],
            "n_pool_kernel_size": trial.suggest_categorical(
                "n_pool_kernel_size",
                (5 * [1], 5 * [2], 5 * [4]),  # Remove most aggressive pooling
            ),
            "n_freq_downsample": trial.suggest_categorical(
                "n_freq_downsample",
                ([1, 1, 1, 1, 1], [2, 2, 1, 1, 1]),  # Less aggressive downsampling
            ),
            "learning_rate": trial.suggest_float(
                "learning_rate",
                low=1e-4,
                high=1e-2,
                log=True,
            ),
            "scaler_type": "robust",
            "max_steps": trial.suggest_categorical(
                "max_steps",
                (100, 200) if debug else (500, 1000),  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical(
                "batch_size",
                (32, 64),  # Larger batches for stability
            ),
            "windows_batch_size": trial.suggest_categorical(
                "windows_batch_size",
                (128, 256),
            ),
            "random_seed": trial.suggest_int(
                "random_seed",
                low=1,
                high=20,
            ),
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir

        # Add hardware-aware settings for PyTorch Lightning
        if hardware_config:
            config_dict["accelerator"] = hardware_config["accelerator"]
            config_dict["devices"] = hardware_config["devices"]
            if hardware_config["strategy"] != "auto":
                config_dict["strategy"] = hardware_config["strategy"]

        return config_dict

    return config


def create_auto_config_lstm(seasonality, debug=False, hardware_config=None):
    """Create configuration for AutoLSTM with optuna backend."""

    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size",
                (6, 12) if debug else (12, 24, 48),  # Smaller for debug
            ),
            "encoder_hidden_size": trial.suggest_categorical(
                "encoder_hidden_size",
                (64, 128),
            ),
            "encoder_n_layers": trial.suggest_categorical(
                "encoder_n_layers",
                (2, 3),  # Reduced max layers
            ),
            "learning_rate": trial.suggest_float(
                "learning_rate",
                low=1e-4,
                high=1e-2,
                log=True,
            ),
            "scaler_type": "robust",
            "max_steps": trial.suggest_categorical(
                "max_steps",
                (100, 200) if debug else (500, 1000),  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical(
                "batch_size",
                (32, 64),  # Larger batches for stability
            ),
            "random_seed": trial.suggest_int("random_seed", low=1, high=20),
            "start_padding_enabled": True,  # Enable padding for short series
            "decoder_layers": trial.suggest_categorical(
                "decoder_layers",
                (1, 2),  # Add decoder configuration
            ),
            "decoder_hidden_size": trial.suggest_categorical(
                "decoder_hidden_size",
                (64, 128),  # Match encoder hidden size
            ),
        }

        # Add hardware-aware settings for PyTorch Lightning
        if hardware_config:
            config_dict["accelerator"] = hardware_config["accelerator"]
            config_dict["devices"] = hardware_config["devices"]
            if hardware_config["strategy"] != "auto":
                config_dict["strategy"] = hardware_config["strategy"]

        return config_dict

    return config


def create_auto_config_simple(
    seasonality, lightning_logs_dir=None, debug=False, hardware_config=None
):
    """Create simple configuration for linear models with optuna backend."""

    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size",
                (6, 12) if debug else (12, 24, 48),  # Smaller for debug
            ),
            "learning_rate": trial.suggest_float(
                "learning_rate",
                low=1e-4,
                high=1e-2,
                log=True,
            ),
            "scaler_type": "robust",
            "max_steps": trial.suggest_categorical(
                "max_steps",
                (100, 200) if debug else (500, 1000),  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical(
                "batch_size",
                (32, 64),  # Larger batches for stability
            ),
            "random_seed": trial.suggest_int("random_seed", low=1, high=20),
            "start_padding_enabled": True,  # Enable padding for short series
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir

        # Add hardware-aware settings for PyTorch Lightning
        if hardware_config:
            config_dict["accelerator"] = hardware_config["accelerator"]
            config_dict["devices"] = hardware_config["devices"]
            if hardware_config["strategy"] != "auto":
                config_dict["strategy"] = hardware_config["strategy"]

        return config_dict

    return config


def create_auto_config_deepar(
    seasonality, lightning_logs_dir=None, debug=False, hardware_config=None
):
    """Create configuration for AutoDeepAR with optuna backend with robust scaling."""

    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size",
                (6, 12) if debug else (12, 24, 48),  # Smaller for debug
            ),
            "lstm_hidden_size": trial.suggest_categorical(
                "lstm_hidden_size", (64, 128, 256)
            ),
            "lstm_n_layers": trial.suggest_categorical("lstm_n_layers", (2, 3)),
            "lstm_dropout": trial.suggest_float("lstm_dropout", 0.1, 0.4),
            "learning_rate": trial.suggest_float(
                "learning_rate", low=1e-4, high=1e-2, log=True
            ),
            # Remove minmax1 scaler which can cause -inf scale parameters
            "scaler_type": trial.suggest_categorical(
                "scaler_type", ("robust", "standard")
            ),
            "max_steps": trial.suggest_categorical(
                "max_steps",
                (100, 200) if debug else (500, 1000),  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical("batch_size", (32, 64, 128)),
            "random_seed": trial.suggest_int("random_seed", low=1, high=20),
            "start_padding_enabled": True,  # Enable padding for short series
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir

        # Add hardware-aware settings for PyTorch Lightning
        if hardware_config:
            config_dict["accelerator"] = hardware_config["accelerator"]
            config_dict["devices"] = hardware_config["devices"]
            if hardware_config["strategy"] != "auto":
                config_dict["strategy"] = hardware_config["strategy"]

        return config_dict

    return config


def create_auto_config_nbeats(
    seasonality, lightning_logs_dir=None, debug=False, hardware_config=None
):
    """Create configuration for AutoNBEATS with optuna backend."""

    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size",
                (6, 12) if debug else (12, 24, 48),  # Smaller for debug
            ),
            "max_steps": trial.suggest_categorical(
                "max_steps",
                (100, 200) if debug else (500, 1000),  # Reduced for debug
            ),
            "learning_rate": trial.suggest_float(
                "learning_rate", low=1e-4, high=1e-2, log=True
            ),
            "scaler_type": "robust",
            "batch_size": trial.suggest_categorical("batch_size", (32, 64)),
            "stack_types": trial.suggest_categorical(
                "stack_types", (["identity", "identity"], ["trend", "seasonality"])
            ),
            "n_blocks": trial.suggest_categorical("n_blocks", ([2, 2], [3, 3])),
            "mlp_units": trial.suggest_categorical(
                "mlp_units", ([[64, 64], [64, 64]], [[128, 128], [128, 128]])
            ),
            "random_seed": trial.suggest_int("random_seed", low=1, high=20),
            "start_padding_enabled": True,  # Enable padding for short series
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir

        # Add hardware-aware settings for PyTorch Lightning
        if hardware_config:
            config_dict["accelerator"] = hardware_config["accelerator"]
            config_dict["devices"] = hardware_config["devices"]
            if hardware_config["strategy"] != "auto":
                config_dict["strategy"] = hardware_config["strategy"]

        return config_dict

    return config


def create_auto_config_transformer(
    seasonality, lightning_logs_dir=None, debug=False, hardware_config=None
):
    """Create configuration for AutoVanillaTransformer with optuna backend."""

    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size",
                (6, 12) if debug else (12, 24, 48),  # Smaller for debug
            ),
            "hidden_size": trial.suggest_categorical("hidden_size", (64, 128, 256)),
            "n_head": trial.suggest_categorical("n_head", (4, 8)),
            "learning_rate": trial.suggest_float(
                "learning_rate", low=1e-4, high=1e-2, log=True
            ),
            "scaler_type": "robust",
            "max_steps": trial.suggest_categorical(
                "max_steps",
                (100, 200) if debug else (500, 1000),  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical("batch_size", (32, 64)),
            "random_seed": trial.suggest_int("random_seed", low=1, high=20),
            "start_padding_enabled": True,  # Enable padding for short series
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir

        # Add hardware-aware settings for PyTorch Lightning
        if hardware_config:
            config_dict["accelerator"] = hardware_config["accelerator"]
            config_dict["devices"] = hardware_config["devices"]
            if hardware_config["strategy"] != "auto":
                config_dict["strategy"] = hardware_config["strategy"]

        return config_dict

    return config


def create_auto_config_tide(
    seasonality, lightning_logs_dir=None, debug=False, hardware_config=None
):
    """Create configuration for AutoTiDE with optuna backend."""

    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size",
                (6, 12) if debug else (12, 24, 48),  # Smaller for debug
            ),
            "hidden_size": trial.suggest_categorical("hidden_size", (256, 512)),
            "decoder_output_dim": trial.suggest_categorical(
                "decoder_output_dim", (16, 32, 64)
            ),
            "temporal_decoder_dim": trial.suggest_categorical(
                "temporal_decoder_dim", (64, 128)
            ),
            "dropout": trial.suggest_float("dropout", 0.1, 0.5),
            "learning_rate": trial.suggest_float(
                "learning_rate", low=1e-4, high=1e-2, log=True
            ),
            "scaler_type": "robust",
            "max_steps": trial.suggest_categorical(
                "max_steps",
                (100, 200) if debug else (500, 1000),  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical("batch_size", (32, 64)),
            "random_seed": trial.suggest_int("random_seed", low=1, high=20),
            "start_padding_enabled": True,  # Enable padding for short series
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir

        # Add hardware-aware settings for PyTorch Lightning
        if hardware_config:
            config_dict["accelerator"] = hardware_config["accelerator"]
            config_dict["devices"] = hardware_config["devices"]
            if hardware_config["strategy"] != "auto":
                config_dict["strategy"] = hardware_config["strategy"]

        return config_dict

    return config


def create_auto_config_kan(
    seasonality, lightning_logs_dir=None, debug=False, hardware_config=None
):
    """Create configuration for AutoKAN with optuna backend."""

    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size",
                (6, 12) if debug else (12, 24, 48),  # Smaller for debug
            ),
            "grid_size": trial.suggest_categorical("grid_size", (3, 5, 7)),
            "spline_order": trial.suggest_categorical("spline_order", (3, 4)),
            "n_hidden_layers": trial.suggest_categorical("n_hidden_layers", (1, 2)),
            "hidden_size": trial.suggest_categorical("hidden_size", (256, 512)),
            "learning_rate": trial.suggest_float(
                "learning_rate", low=1e-4, high=1e-2, log=True
            ),
            "scaler_type": "robust",
            "max_steps": trial.suggest_categorical(
                "max_steps",
                (100, 200) if debug else (500, 1000),  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical("batch_size", (32, 64)),
            "random_seed": trial.suggest_int("random_seed", low=1, high=20),
            "start_padding_enabled": True,  # Enable padding for short series
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir

        # Add hardware-aware settings for PyTorch Lightning
        if hardware_config:
            config_dict["accelerator"] = hardware_config["accelerator"]
            config_dict["devices"] = hardware_config["devices"]
            if hardware_config["strategy"] != "auto":
                config_dict["strategy"] = hardware_config["strategy"]

        return config_dict

    return config


def main():
    """Main function for neural forecast with cross-validation."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Neural Forecasting with Auto Hyperparameter Optimization"
    )
    parser.add_argument(
        "--dataset", required=True, help="Dataset name from datasets.toml"
    )
    parser.add_argument(
        "--model",
        required=True,
        choices=[
            "auto_deepar",
            "auto_nbeats",
            "auto_nhits",
            "auto_dlinear",
            "auto_nlinear",
            "auto_vanilla_transformer",
            "auto_tide",
            "auto_kan",
        ],
        help="Neural model to use",
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
    parser.add_argument(
        "--skip-daily",
        action="store_true",
        help="Skip datasets with business day (B) or daily (D) frequency",
    )
    args = parser.parse_args()

    DATASET_NAME = args.dataset
    MODEL_NAME = args.model
    DEBUG_MODE = args.debug
    SKIP_EXISTING = args.skip_existing
    SKIP_DAILY = args.skip_daily

    # Check if we should skip this forecast
    if SKIP_EXISTING and should_skip_forecast(DATASET_NAME, MODEL_NAME, verbose=True):
        print(f"Skipping {MODEL_NAME} for {DATASET_NAME} - valid metrics already exist")
        sys.exit(0)

    print("=" * 60)
    print("Neural Forecast with Cross-Validation")
    if DEBUG_MODE:
        print("*** DEBUG MODE ENABLED ***")
    print("=" * 60)
    print(f"Dataset: {DATASET_NAME}")
    print(f"Model: {MODEL_NAME}")

    # Detect hardware and configure settings
    print("\n0. Hardware Detection")
    print("-" * 40)
    hardware_config = detect_hardware()

    print(f"\n1. Loading Dataset: {DATASET_NAME}")
    print("-" * 40)

    # Load dataset configuration
    dataset_config = read_dataset_config(DATASET_NAME)
    frequency = dataset_config["frequency"]
    seasonality = dataset_config["seasonality"]

    # Check if we should skip daily frequency datasets
    if SKIP_DAILY and frequency in ["B", "D"]:
        print(
            f"Skipping {MODEL_NAME} for {DATASET_NAME} - daily frequency dataset (frequency: {frequency})"
        )
        sys.exit(0)

    # Convert frequency to Polars format
    polars_frequency = convert_pandas_freq_to_polars(frequency)

    print(f"Frequency: {frequency} (Polars: {polars_frequency})")
    print(f"Seasonality: {seasonality}")

    # Set NUM_SAMPLES based on debug mode and data frequency
    if DEBUG_MODE:
        NUM_SAMPLES = 2  # Very few samples for debug
    else:
        # Detect if this is a daily frequency dataset
        # B = business days, D = daily
        if frequency in ["B", "D"]:
            NUM_SAMPLES = 5  # Much fewer samples for daily data
            print(
                f"Daily frequency detected, reducing hyperparameter samples to {NUM_SAMPLES}"
            )
        else:
            NUM_SAMPLES = 20  # Normal number of samples for monthly/quarterly data

    print(f"Hyperparameter samples: {NUM_SAMPLES}")

    # Get test size based on frequency (reduce for debug mode)
    if DEBUG_MODE:
        test_size = 6  # Small test size for debug
        print(f"Test size (DEBUG): {test_size}")
    else:
        test_size = get_test_size_from_frequency(frequency)
        print(f"Test size (forecast horizon): {test_size}")

    # Load and preprocess data using robust pipeline
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

    # Prepare two synchronized views of the panel:
    #  - df_baseline uses imputed values for baseline models (StatsForecast models need complete data)
    #  - df_neural forward-fills gaps for neural models that cannot ingest NaNs
    if "y_imputed" in train_df.columns:
        # Use imputed values for training portion to ensure baseline models work properly
        train_for_baseline = train_df.select(["unique_id", "ds", "y_imputed"]).rename(
            {"y_imputed": "y"}
        )
    else:
        train_for_baseline = train_df.select(["unique_id", "ds", "y"])

    test_for_baseline = test_df.select(["unique_id", "ds", "y"])

    df_baseline = pl.concat([train_for_baseline, test_for_baseline]).sort(
        ["unique_id", "ds"]
    )

    df_neural = df_baseline.with_columns(
        pl.col("y").forward_fill().over("unique_id").alias("y_filled")
    )

    # Robust validation for neural model data

    def validate_neural_series(df):
        """Validate series for neural model consumption."""
        import numpy as np

        problematic_series = []

        for unique_id in df["unique_id"].unique():
            series_data = df.filter(pl.col("unique_id") == unique_id)
            y_vals = series_data["y_filled"].to_numpy()

            # Check for remaining nulls
            if pd.isna(y_vals).any():
                problematic_series.append(
                    (unique_id, "remaining nulls after forward fill")
                )
                continue

            # Check for infinite values
            if not np.all(np.isfinite(y_vals)):
                problematic_series.append((unique_id, "infinite values"))
                continue

            # Check for extreme values that could cause scaling issues
            if len(y_vals) > 0:
                abs_max = np.max(np.abs(y_vals))
                if abs_max > 1e12:
                    problematic_series.append(
                        (unique_id, f"extreme values (max: {abs_max:.2e})")
                    )
                    continue

                # Check for zero variance (constant series)
                if len(y_vals) > 1:
                    std_val = np.std(y_vals, ddof=1)
                    if std_val < 1e-12:  # Near-zero variance
                        problematic_series.append(
                            (unique_id, f"near-zero variance ({std_val:.2e})")
                        )
                        continue

        return problematic_series

    # Validate and remove problematic series
    problematic = validate_neural_series(df_neural)
    if problematic:
        problematic_ids = [uid for uid, _ in problematic]
        print(
            f"  Warning: Removing {len(problematic_ids)} series with neural model issues:"
        )
        for uid, reason in problematic[:3]:  # Show first 3
            print(f"    {uid}: {reason}")
        if len(problematic) > 3:
            print(f"    ... and {len(problematic) - 3} more")

        # Filter out problematic series from all dataframes
        df_baseline = df_baseline.filter(~pl.col("unique_id").is_in(problematic_ids))
        df_neural = df_neural.filter(~pl.col("unique_id").is_in(problematic_ids))
        train_df = train_df.filter(~pl.col("unique_id").is_in(problematic_ids))
        test_df = test_df.filter(~pl.col("unique_id").is_in(problematic_ids))

    # Additional baseline data validation and cleaning
    def validate_baseline_series(df):
        """Validate and clean baseline data for StatsForecast models."""
        import numpy as np

        print("  Validating baseline data for StatsForecast models...")

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
            print(f"    Removing {len(removed_ids)} series with baseline model issues:")
            for uid, reason in series_to_remove[:3]:  # Show first 3
                print(f"      {uid}: {reason}")
            if len(series_to_remove) > 3:
                print(f"      ... and {len(series_to_remove) - 3} more")

            return removed_ids
        return []

    # Validate baseline data and remove additional problematic series
    baseline_problematic_ids = validate_baseline_series(df_baseline)
    if baseline_problematic_ids:
        # Remove from all dataframes to maintain synchronization
        df_baseline = df_baseline.filter(
            ~pl.col("unique_id").is_in(baseline_problematic_ids)
        )
        df_neural = df_neural.filter(
            ~pl.col("unique_id").is_in(baseline_problematic_ids)
        )
        train_df = train_df.filter(~pl.col("unique_id").is_in(baseline_problematic_ids))
        test_df = test_df.filter(~pl.col("unique_id").is_in(baseline_problematic_ids))

    # Drop any series that remain entirely missing after forward fill (defensive)
    empty_series = df_neural.filter(pl.col("y_filled").is_null())["unique_id"].unique()
    if empty_series.len() > 0:
        empty_ids = empty_series.to_list()
        print(
            "  Warning: Removing series with no available targets after forward fill:"
        )
        print(f"    {empty_ids}")
        df_baseline = df_baseline.filter(~pl.col("unique_id").is_in(empty_ids))
        df_neural = df_neural.filter(~pl.col("unique_id").is_in(empty_ids))
        train_df = train_df.filter(~pl.col("unique_id").is_in(empty_ids))
        test_df = test_df.filter(~pl.col("unique_id").is_in(empty_ids))

    df_neural = df_neural.select(["unique_id", "ds", pl.col("y_filled").alias("y")])

    # Final validation: ensure baseline and neural datasets are synchronized
    baseline_series = set(df_baseline["unique_id"].unique().to_list())
    neural_series = set(df_neural["unique_id"].unique().to_list())

    if baseline_series != neural_series:
        print("  Warning: Baseline and neural datasets have different series counts.")
        print(f"    Baseline: {len(baseline_series)} series")
        print(f"    Neural: {len(neural_series)} series")

        # Use intersection to ensure both datasets have exactly the same series
        common_series = list(baseline_series.intersection(neural_series))
        if len(common_series) < len(baseline_series) or len(common_series) < len(
            neural_series
        ):
            print(f"    Synchronizing to common {len(common_series)} series")
            df_baseline = df_baseline.filter(pl.col("unique_id").is_in(common_series))
            df_neural = df_neural.filter(pl.col("unique_id").is_in(common_series))
            train_df = train_df.filter(pl.col("unique_id").is_in(common_series))
            test_df = test_df.filter(pl.col("unique_id").is_in(common_series))

    print("Final synchronized data for CV:")
    print(
        f"  Baseline: {len(df_baseline):,} observations, {df_baseline['unique_id'].n_unique()} series"
    )
    print(
        f"  Neural: {len(df_neural):,} observations, {df_neural['unique_id'].n_unique()} series"
    )

    # Define models
    print("\n3. Setting Up Models")
    print("-" * 40)

    # Baseline models from StatsForecast
    baseline_models = [
        HistoricAverage(),
        SeasonalNaive(season_length=seasonality),
    ]

    # Create output directories early
    lightning_logs_dir = f"./_output/forecasting/logs/{DATASET_NAME}/{MODEL_NAME}"
    os.makedirs(lightning_logs_dir, exist_ok=True)

    # Create the selected neural model with custom configuration and lightning logs path
    model_mapping = {
        "auto_deepar": AutoDeepAR(
            h=test_size,
            config=create_auto_config_deepar(
                seasonality,
                lightning_logs_dir,
                debug=DEBUG_MODE,
                hardware_config=hardware_config,
            ),
            loss=DistributionLoss(distribution="Normal"),
            backend="optuna",
            num_samples=NUM_SAMPLES,
        ),
        "auto_nbeats": AutoNBEATS(
            h=test_size,
            config=create_auto_config_nbeats(
                seasonality,
                lightning_logs_dir,
                debug=DEBUG_MODE,
                hardware_config=hardware_config,
            ),
            loss=MAE(),
            backend="optuna",
            num_samples=NUM_SAMPLES,
        ),
        "auto_nhits": AutoNHITS(
            h=test_size,
            config=create_auto_config_nhits(
                seasonality,
                lightning_logs_dir,
                debug=DEBUG_MODE,
                hardware_config=hardware_config,
            ),
            loss=MAE(),
            backend="optuna",
            num_samples=NUM_SAMPLES,
        ),
        "auto_dlinear": AutoDLinear(
            h=test_size,
            config=create_auto_config_simple(
                seasonality,
                lightning_logs_dir,
                debug=DEBUG_MODE,
                hardware_config=hardware_config,
            ),
            loss=MAE(),
            backend="optuna",
            num_samples=NUM_SAMPLES,
        ),
        "auto_nlinear": AutoNLinear(
            h=test_size,
            config=create_auto_config_simple(
                seasonality,
                lightning_logs_dir,
                debug=DEBUG_MODE,
                hardware_config=hardware_config,
            ),
            loss=MAE(),
            backend="optuna",
            num_samples=NUM_SAMPLES,
        ),
        "auto_vanilla_transformer": AutoVanillaTransformer(
            h=test_size,
            config=create_auto_config_transformer(
                seasonality,
                lightning_logs_dir,
                debug=DEBUG_MODE,
                hardware_config=hardware_config,
            ),
            loss=MAE(),
            backend="optuna",
            num_samples=NUM_SAMPLES,
        ),
        "auto_tide": AutoTiDE(
            h=test_size,
            config=create_auto_config_tide(
                seasonality,
                lightning_logs_dir,
                debug=DEBUG_MODE,
                hardware_config=hardware_config,
            ),
            loss=MAE(),
            backend="optuna",
            num_samples=NUM_SAMPLES,
        ),
        "auto_kan": AutoKAN(
            h=test_size,
            config=create_auto_config_kan(
                seasonality,
                lightning_logs_dir,
                debug=DEBUG_MODE,
                hardware_config=hardware_config,
            ),
            loss=MAE(),
            backend="optuna",
            num_samples=NUM_SAMPLES,
        ),
    }

    selected_neural_model = model_mapping[MODEL_NAME]
    neural_models = [selected_neural_model]

    baseline_model_names = [type(model).__name__ for model in baseline_models]
    neural_model_names = [type(model).__name__ for model in neural_models]

    print(f"Baseline Models: {', '.join(baseline_model_names)}")
    print(f"Neural Model: {', '.join(neural_model_names)}")

    # Perform cross-validation with baseline models first
    print("\n4. Performing Cross-Validation with Baseline Models")
    print("-" * 40)

    # Defensive validation before baseline model training
    def validate_data_for_training(df, model_type="baseline"):
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

    # Validate baseline data
    validate_data_for_training(df_baseline, "baseline")

    sf = StatsForecast(
        models=baseline_models, freq=polars_frequency, n_jobs=-1, verbose=True
    )

    cv_windows = determine_cv_windows(df_baseline, test_size)
    print(f"  Cross-validation windows (max {MAX_CV_WINDOWS}): {cv_windows}")
    if cv_windows < MAX_CV_WINDOWS:
        print("  Shortest baseline series length limits the number of windows.")

    start_time = time.time()
    baseline_cv_df = sf.cross_validation(
        df=df_baseline, h=test_size, step_size=test_size, n_windows=cv_windows
    )
    baseline_time = time.time() - start_time
    print(f"Baseline cross-validation completed in {baseline_time:.2f} seconds")

    # Perform cross-validation with neural models
    print("\n5. Performing Cross-Validation with Neural Models")
    print("-" * 40)
    print("Note: This will take longer due to hyperparameter optimization")
    print(f"Lightning logs will be saved to: {lightning_logs_dir}")

    nf = NeuralForecast(models=neural_models, freq=polars_frequency)

    def debug_data_quality(df, name):
        """Debug function to check data quality before model training."""
        import numpy as np

        print(f"  Debug: {name} data quality check:")
        print(f"    Shape: {df.shape}")
        print(f"    Series: {df['unique_id'].n_unique()}")

        # Use the correct column based on the dataframe
        if "y_filled" in df.columns:
            y_col = "y_filled"
        else:
            y_col = "y"

        print(f"    Null values in {y_col}: {df[y_col].null_count()}")

        # Check for problematic values
        y_vals = df[y_col].to_numpy()
        finite_vals = y_vals[np.isfinite(y_vals)]
        if len(finite_vals) > 0:
            print(
                f"    Value range: [{finite_vals.min():.2e}, {finite_vals.max():.2e}]"
            )
            print(f"    Standard deviation: {finite_vals.std():.2e}")
        else:
            print("    Warning: No finite values found!")

    # Validate neural data before training
    validate_data_for_training(df_neural, "neural")

    # Debug data quality before training
    if DEBUG_MODE:
        debug_data_quality(df_neural, "Neural model input")

    print(f"  Cross-validation windows for neural models: {cv_windows}")
    if cv_windows < MAX_CV_WINDOWS:
        print("  Neural windows limited by available history.")

    start_time = time.time()
    try:
        neural_cv_df = nf.cross_validation(
            df=df_neural,
            val_size=test_size,
            n_windows=cv_windows,
            step_size=test_size,
        )
        neural_time = time.time() - start_time
        print(f"Neural cross-validation completed in {neural_time:.2f} seconds")

    except Exception as e:
        print(f"Error during neural model cross-validation: {e}")
        print(
            "This likely indicates data quality issues that weren't caught by preprocessing."
        )

        # Additional debugging information
        print("\nDiagnostic information:")
        debug_data_quality(df_neural, "Failed neural input")

        # Check for specific problematic patterns
        print("\nChecking for specific issues:")
        for unique_id in df_neural["unique_id"].unique()[:5]:  # Check first 5 series
            series_data = df_neural.filter(pl.col("unique_id") == unique_id)
            y_vals = series_data["y"].to_numpy()
            print(
                f"  Series {unique_id}: min={y_vals.min():.2e}, max={y_vals.max():.2e}, std={y_vals.std():.2e}"
            )

        raise  # Re-raise the exception

    # Combine results
    print("\n6. Combining Results")
    print("-" * 40)

    # Join baseline and neural forecasts
    cv_df = baseline_cv_df.join(
        neural_cv_df.drop(["y", "cutoff"]), on=["unique_id", "ds"], how="left"
    )

    # Create training data aligned with per-series cutoffs
    if "y_imputed" in train_df.columns:
        train_data_for_eval = train_df.select(["unique_id", "ds", "y_imputed"]).rename(
            {"y_imputed": "y"}
        )
    else:
        train_data_for_eval = train_df.select(["unique_id", "ds", "y"])
    train_data = align_train_data_with_cutoffs(train_data_for_eval, cv_df)

    # Evaluate all models
    print("\n7. Evaluating Model Performance")
    print("-" * 40)

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
    print("\n8. Model Performance Summary")
    print("-" * 40)

    comparison_data = [
        ["Model", "Type", "Avg MASE", "Avg MSE", "Avg RMSE", "Avg R2oos"]
    ]

    # Add baseline models
    for model_col in actual_model_cols:
        if model_col in baseline_model_names:
            model_type = "Baseline"
        else:
            model_type = "Neural"

        comparison_data.append(
            [
                model_col,
                model_type,
                f"{avg_metrics[model_col]['MASE']:.4f}",
                f"{avg_metrics[model_col]['MSE']:.4f}",
                f"{avg_metrics[model_col]['RMSE']:.4f}",
                f"{avg_metrics[model_col]['R2oos']:.4f}",
            ]
        )

    print(tabulate(comparison_data, headers="firstrow", tablefmt="grid"))

    # Find best model by each metric
    print("\n9. Best Models by Metric")
    print("-" * 40)

    best_models = {}
    for metric in ["MASE", "MSE", "RMSE"]:
        best_model = min(avg_metrics.items(), key=lambda x: x[1][metric])[0]
        best_models[metric] = best_model
        print(f"Best {metric}: {best_model} ({avg_metrics[best_model][metric]:.4f})")

    # For R2oos, higher is better
    best_model = max(avg_metrics.items(), key=lambda x: x[1]["R2oos"])[0]
    best_models["R2oos"] = best_model
    print(f"Best R2oos: {best_model} ({avg_metrics[best_model]['R2oos']:.4f})")

    # Save CSV error metrics for the neural model
    print("\n10. Saving Error Metrics")
    print("-" * 40)

    # Create error metrics directory
    error_metrics_dir = f"./_output/forecasting/error_metrics/{DATASET_NAME}"
    os.makedirs(error_metrics_dir, exist_ok=True)

    # Get the neural model's metrics (exclude baseline models for now)
    neural_model_name = neural_model_names[0]  # Should be only one model
    if neural_model_name in avg_metrics:
        # Validate metrics before saving
        mase_val = avg_metrics[neural_model_name]["MASE"]
        mse_val = avg_metrics[neural_model_name]["MSE"]
        rmse_val = avg_metrics[neural_model_name]["RMSE"]
        r2oos_val = avg_metrics[neural_model_name]["R2oos"]

        # Check for invalid metric values
        import numpy as np

        if mase_val == 0.0:
            print(
                f"Warning: MASE is exactly 0.0 for model {neural_model_name}. This typically indicates:"
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
            print(
                f"Warning: NaN values detected in metrics for model {neural_model_name}:"
            )
            print(f"  MASE: {mase_val}")
            print(f"  MSE: {mse_val}")
            print(f"  RMSE: {rmse_val}")
            print(f"  R2oos: {r2oos_val}")
            print(
                "  This typically indicates insufficient valid data for metric calculation."
            )
            print("  Saving available metrics and continuing.")
            # Don't raise an error, just warn and continue

        metrics_data = {
            "model_name": [MODEL_NAME],
            "dataset_name": [DATASET_NAME],
            "MASE": [mase_val],
            "MSE": [mse_val],
            "RMSE": [rmse_val],
            "R2oos": [r2oos_val],
            "time_taken": [neural_time],
        }

        metrics_df = pl.DataFrame(metrics_data)
        csv_path = f"{error_metrics_dir}/{MODEL_NAME}.csv"
        metrics_df.write_csv(csv_path)
        print(f"Error metrics saved to: {csv_path}")
    else:
        print(f"Warning: Could not find metrics for {neural_model_name}")

    print("\n" + "=" * 60)
    print("Neural Forecast Complete!")
    print("=" * 60)
    print(f"Total time: {baseline_time + neural_time:.2f} seconds")
    print(f"  - Baseline models: {baseline_time:.2f} seconds")
    print(f"  - Neural models: {neural_time:.2f} seconds")


if __name__ == "__main__":
    main()
