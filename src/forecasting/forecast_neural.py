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
    AutoLSTM
)
from neuralforecast.losses.pytorch import MAE, DistributionLoss

from statsforecast import StatsForecast
from statsforecast.models import (
    HistoricAverage,
    SeasonalNaive
)

warnings.filterwarnings("ignore")

# Default NUM_SAMPLES - overridden by debug mode
NUM_SAMPLES = 20


def create_auto_config_nhits(seasonality, lightning_logs_dir=None, debug=False):
    """Create configuration for AutoNHITS with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (6, 12) if debug else (12, 24, 48)  # Smaller for debug
            ),
            "start_padding_enabled": True,  # Enable padding for short series
            "n_blocks": 5 * [1],
            "mlp_units": 5 * [[64, 64]],
            "n_pool_kernel_size": trial.suggest_categorical(
                "n_pool_kernel_size",
                (5*[1], 5*[2], 5*[4])  # Remove most aggressive pooling
            ),
            "n_freq_downsample": trial.suggest_categorical(
                "n_freq_downsample",
                ([1, 1, 1, 1, 1], [2, 2, 1, 1, 1])  # Less aggressive downsampling
            ),
            "learning_rate": trial.suggest_float(
                "learning_rate",
                low=1e-4,
                high=1e-2,
                log=True,
            ),
            "scaler_type": "robust",
            "max_steps": trial.suggest_categorical(
                "max_steps", (100, 200) if debug else (500, 1000)  # Reduced for debug
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
        return config_dict
    return config


def create_auto_config_lstm(seasonality, debug=False):
    """Create configuration for AutoLSTM with optuna backend."""
    def config(trial):
        return {
            "input_size": trial.suggest_categorical(
                "input_size", (6, 12) if debug else (12, 24, 48)  # Smaller for debug
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
            "scaler_type": 'robust',
            "max_steps": trial.suggest_categorical(
                "max_steps",
                (100, 200) if debug else (500, 1000)  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical(
                "batch_size",
                (32, 64)  # Larger batches for stability
            ),
            "random_seed": trial.suggest_int(
                "random_seed",
                low=1,
                high=20
            ),
            "start_padding_enabled": True,  # Enable padding for short series
            "decoder_layers": trial.suggest_categorical(
                "decoder_layers", (1, 2)  # Add decoder configuration
            ),
            "decoder_hidden_size": trial.suggest_categorical(
                "decoder_hidden_size", (64, 128)  # Match encoder hidden size
            ),
        }
    return config


def create_auto_config_simple(seasonality, lightning_logs_dir=None, debug=False):
    """Create simple configuration for linear models with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (6, 12) if debug else (12, 24, 48)  # Smaller for debug
            ),
            "learning_rate": trial.suggest_float(
                "learning_rate",
                low=1e-4,
                high=1e-2,
                log=True,
            ),
            "scaler_type": 'robust',
            "max_steps": trial.suggest_categorical(
                "max_steps",
                (100, 200) if debug else (500, 1000)  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical(
                "batch_size",
                (32, 64)  # Larger batches for stability
            ),
            "random_seed": trial.suggest_int(
                "random_seed",
                low=1,
                high=20
            ),
            "start_padding_enabled": True,  # Enable padding for short series
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir
        return config_dict
    return config


def create_auto_config_deepar(seasonality, lightning_logs_dir=None, debug=False):
    """Create configuration for AutoDeepAR with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (6, 12) if debug else (12, 24, 48)  # Smaller for debug
            ),
            "lstm_hidden_size": trial.suggest_categorical(
                "lstm_hidden_size", (64, 128, 256)
            ),
            "lstm_n_layers": trial.suggest_categorical(
                "lstm_n_layers", (2, 3)
            ),
            "lstm_dropout": trial.suggest_float(
                "lstm_dropout", 0.1, 0.4
            ),
            "learning_rate": trial.suggest_float(
                "learning_rate", low=1e-4, high=1e-2, log=True
            ),
            "scaler_type": trial.suggest_categorical(
                "scaler_type", ("robust", "standard", "minmax1")
            ),
            "max_steps": trial.suggest_categorical(
                "max_steps", (100, 200) if debug else (500, 1000)  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical(
                "batch_size", (32, 64, 128)
            ),
            "random_seed": trial.suggest_int(
                "random_seed", low=1, high=20
            ),
            "start_padding_enabled": True,  # Enable padding for short series
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir
        return config_dict
    return config


def create_auto_config_nbeats(seasonality, lightning_logs_dir=None, debug=False):
    """Create configuration for AutoNBEATS with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (6, 12) if debug else (12, 24, 48)  # Smaller for debug
            ),
            "max_steps": trial.suggest_categorical(
                "max_steps", (100, 200) if debug else (500, 1000)  # Reduced for debug
            ),
            "learning_rate": trial.suggest_float(
                "learning_rate", low=1e-4, high=1e-2, log=True
            ),
            "scaler_type": "robust",
            "batch_size": trial.suggest_categorical(
                "batch_size", (32, 64)
            ),
            "stack_types": trial.suggest_categorical(
                "stack_types", (["identity", "identity"], ["trend", "seasonality"])
            ),
            "n_blocks": trial.suggest_categorical(
                "n_blocks", ([2, 2], [3, 3])
            ),
            "mlp_units": trial.suggest_categorical(
                "mlp_units", ([[64, 64], [64, 64]], [[128, 128], [128, 128]])
            ),
            "random_seed": trial.suggest_int(
                "random_seed", low=1, high=20
            ),
            "start_padding_enabled": True,  # Enable padding for short series
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir
        return config_dict
    return config


def create_auto_config_transformer(seasonality, lightning_logs_dir=None, debug=False):
    """Create configuration for AutoVanillaTransformer with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (6, 12) if debug else (12, 24, 48)  # Smaller for debug
            ),
            "hidden_size": trial.suggest_categorical(
                "hidden_size", (64, 128, 256)
            ),
            "n_head": trial.suggest_categorical(
                "n_head", (4, 8)
            ),
            "learning_rate": trial.suggest_float(
                "learning_rate", low=1e-4, high=1e-2, log=True
            ),
            "scaler_type": "robust",
            "max_steps": trial.suggest_categorical(
                "max_steps", (100, 200) if debug else (500, 1000)  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical(
                "batch_size", (32, 64)
            ),
            "random_seed": trial.suggest_int(
                "random_seed", low=1, high=20
            ),
            "start_padding_enabled": True,  # Enable padding for short series
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir
        return config_dict
    return config


def create_auto_config_tide(seasonality, lightning_logs_dir=None, debug=False):
    """Create configuration for AutoTiDE with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (6, 12) if debug else (12, 24, 48)  # Smaller for debug
            ),
            "hidden_size": trial.suggest_categorical(
                "hidden_size", (256, 512)
            ),
            "decoder_output_dim": trial.suggest_categorical(
                "decoder_output_dim", (16, 32, 64)
            ),
            "temporal_decoder_dim": trial.suggest_categorical(
                "temporal_decoder_dim", (64, 128)
            ),
            "dropout": trial.suggest_float(
                "dropout", 0.1, 0.5
            ),
            "learning_rate": trial.suggest_float(
                "learning_rate", low=1e-4, high=1e-2, log=True
            ),
            "scaler_type": "robust",
            "max_steps": trial.suggest_categorical(
                "max_steps", (100, 200) if debug else (500, 1000)  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical(
                "batch_size", (32, 64)
            ),
            "random_seed": trial.suggest_int(
                "random_seed", low=1, high=20
            ),
            "start_padding_enabled": True,  # Enable padding for short series
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir
        return config_dict
    return config


def create_auto_config_kan(seasonality, lightning_logs_dir=None, debug=False):
    """Create configuration for AutoKAN with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (6, 12) if debug else (12, 24, 48)  # Smaller for debug
            ),
            "grid_size": trial.suggest_categorical(
                "grid_size", (3, 5, 7)
            ),
            "spline_order": trial.suggest_categorical(
                "spline_order", (3, 4)
            ),
            "n_hidden_layers": trial.suggest_categorical(
                "n_hidden_layers", (1, 2)
            ),
            "hidden_size": trial.suggest_categorical(
                "hidden_size", (256, 512)
            ),
            "learning_rate": trial.suggest_float(
                "learning_rate", low=1e-4, high=1e-2, log=True
            ),
            "scaler_type": "robust",
            "max_steps": trial.suggest_categorical(
                "max_steps", (100, 200) if debug else (500, 1000)  # Reduced for debug
            ),
            "batch_size": trial.suggest_categorical(
                "batch_size", (32, 64)
            ),
            "random_seed": trial.suggest_int(
                "random_seed", low=1, high=20
            ),
            "start_padding_enabled": True,  # Enable padding for short series
        }
        if lightning_logs_dir:
            config_dict["default_root_dir"] = lightning_logs_dir
        return config_dict
    return config


def main():
    """Main function for neural forecast with cross-validation."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Neural Forecasting with Auto Hyperparameter Optimization")
    parser.add_argument("--dataset", required=True, help="Dataset name from datasets.toml")
    parser.add_argument("--model", required=True,
                       choices=["auto_deepar", "auto_nbeats", "auto_nhits", "auto_dlinear",
                               "auto_nlinear", "auto_vanilla_transformer", "auto_tide", "auto_kan"],
                       help="Neural model to use")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode for faster testing with limited data")
    args = parser.parse_args()

    DATASET_NAME = args.dataset
    MODEL_NAME = args.model
    DEBUG_MODE = args.debug

    # Set NUM_SAMPLES based on debug mode
    if DEBUG_MODE:
        NUM_SAMPLES = 2  # Very few samples for debug
    else:
        NUM_SAMPLES = 20  # Normal number of samples

    print("=" * 60)
    print("Neural Forecast with Cross-Validation")
    if DEBUG_MODE:
        print("*** DEBUG MODE ENABLED ***")
    print("=" * 60)
    print(f"Dataset: {DATASET_NAME}")
    print(f"Model: {MODEL_NAME}")
    print(f"Hyperparameter samples: {NUM_SAMPLES}")

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

    # Test size will be calculated from actual data split below

    # Load and preprocess data
    print("\n2. Loading and Preprocessing Data")
    print("-" * 40)

    # Load data with proper train/test split for calculating test size
    train_data, test_data, full_data = load_and_preprocess_data(
        dataset_config["data_path"],
        frequency,
        test_split=0.2,  # Use 20% for test to calculate proper horizon
        seasonality=seasonality
    )

    # Get proper test size from actual test split (reduce for debug mode)
    if DEBUG_MODE:
        test_size = 6  # Small test size for debug
        print(f"Test size (DEBUG): {test_size}")
    else:
        test_size = int(test_data["ds"].n_unique())
        print(f"Calculated test size from data split: {test_size}")

    # Use full dataset for cross-validation (concatenate train and test)
    full_data = train_data.select(['unique_id', 'ds', 'y']).vstack(
        test_data.select(['unique_id', 'ds', 'y'])
    ).sort(['unique_id', 'ds'])

    # Filter series based on cross-validation requirements
    df = filter_series_by_cv_requirements(full_data, test_size, debug=DEBUG_MODE)

    print(f"Total samples: {len(df):,}")
    print(f"Number of series: {df['unique_id'].n_unique()}")

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
        "auto_deepar": AutoDeepAR(h=test_size, config=create_auto_config_deepar(seasonality, lightning_logs_dir, debug=DEBUG_MODE),
                                  loss=DistributionLoss(distribution='Normal'),
                                  backend='optuna', num_samples=NUM_SAMPLES),
        "auto_nbeats": AutoNBEATS(h=test_size, config=create_auto_config_nbeats(seasonality, lightning_logs_dir, debug=DEBUG_MODE),
                                  loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
        "auto_nhits": AutoNHITS(h=test_size, config=create_auto_config_nhits(seasonality, lightning_logs_dir, debug=DEBUG_MODE),
                                loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
        "auto_dlinear": AutoDLinear(h=test_size, config=create_auto_config_simple(seasonality, lightning_logs_dir, debug=DEBUG_MODE),
                                    loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
        "auto_nlinear": AutoNLinear(h=test_size, config=create_auto_config_simple(seasonality, lightning_logs_dir, debug=DEBUG_MODE),
                                    loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
        "auto_vanilla_transformer": AutoVanillaTransformer(h=test_size, config=create_auto_config_transformer(seasonality, lightning_logs_dir, debug=DEBUG_MODE),
                                                           loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
        "auto_tide": AutoTiDE(h=test_size, config=create_auto_config_tide(seasonality, lightning_logs_dir, debug=DEBUG_MODE),
                              loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
        "auto_kan": AutoKAN(h=test_size, config=create_auto_config_kan(seasonality, lightning_logs_dir, debug=DEBUG_MODE),
                            loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
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

    sf = StatsForecast(
        models=baseline_models,
        freq=polars_frequency,
        n_jobs=-1,
        verbose=True
    )

    start_time = time.time()
    baseline_cv_df = sf.cross_validation(
        df=df,
        h=test_size,
        step_size=test_size,
        n_windows=1
    )
    baseline_time = time.time() - start_time
    print(f"Baseline cross-validation completed in {baseline_time:.2f} seconds")

    # Perform cross-validation with neural models
    print("\n5. Performing Cross-Validation with Neural Models")
    print("-" * 40)
    print("Note: This will take longer due to hyperparameter optimization")
    print(f"Lightning logs will be saved to: {lightning_logs_dir}")

    nf = NeuralForecast(
        models=neural_models,
        freq=polars_frequency
    )

    start_time = time.time()
    neural_cv_df = nf.cross_validation(
        df=df,
        val_size=test_size,
        n_windows=1,
        step_size=test_size
    )
    neural_time = time.time() - start_time
    print(f"Neural cross-validation completed in {neural_time:.2f} seconds")

    # Combine results
    print("\n6. Combining Results")
    print("-" * 40)

    # Join baseline and neural forecasts
    cv_df = baseline_cv_df.join(
        neural_cv_df.drop(['y', 'cutoff']),
        on=['unique_id', 'ds'],
        how='left'
    )

    # Extract the cutoff date
    cutoff_date = cv_df['cutoff'].unique()[0]

    # Create training data by filtering original data up to cutoff
    train_data = df.filter(pl.col('ds') <= cutoff_date)

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
            print(f"  Warning: Only {valid_mase}/{total_series} series have valid MASE scores")

        avg_metrics[model_col] = {
            'MASE': mase_scores[model_col].mean(),
            'MSE': mse_scores[model_col].mean(),
            'RMSE': rmse_scores[model_col].mean(),
            'R2oos': r2oos_scores[model_col].mean()
        }

    # Create comparison table
    print("\n8. Model Performance Summary")
    print("-" * 40)

    comparison_data = [["Model", "Type", "Avg MASE", "Avg MSE", "Avg RMSE", "Avg R2oos"]]

    # Add baseline models
    for model_col in actual_model_cols:
        if model_col in baseline_model_names:
            model_type = "Baseline"
        else:
            model_type = "Neural"

        comparison_data.append([
            model_col,
            model_type,
            f"{avg_metrics[model_col]['MASE']:.4f}",
            f"{avg_metrics[model_col]['MSE']:.4f}",
            f"{avg_metrics[model_col]['RMSE']:.4f}",
            f"{avg_metrics[model_col]['R2oos']:.4f}"
        ])

    print(tabulate(comparison_data, headers="firstrow", tablefmt="grid"))

    # Find best model by each metric
    print("\n9. Best Models by Metric")
    print("-" * 40)

    best_models = {}
    for metric in ['MASE', 'MSE', 'RMSE']:
        best_model = min(avg_metrics.items(), key=lambda x: x[1][metric])[0]
        best_models[metric] = best_model
        print(f"Best {metric}: {best_model} ({avg_metrics[best_model][metric]:.4f})")

    # For R2oos, higher is better
    best_model = max(avg_metrics.items(), key=lambda x: x[1]['R2oos'])[0]
    best_models['R2oos'] = best_model
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
        mase_val = avg_metrics[neural_model_name]['MASE']
        mse_val = avg_metrics[neural_model_name]['MSE']
        rmse_val = avg_metrics[neural_model_name]['RMSE']
        r2oos_val = avg_metrics[neural_model_name]['R2oos']

        # Check for invalid metric values
        import numpy as np
        if mase_val == 0.0:
            raise ValueError(
                f"MASE is exactly 0.0 for model {neural_model_name}. "
                f"This indicates a calculation error, possibly due to data quality issues."
            )

        if np.isnan(mase_val) or np.isnan(mse_val) or np.isnan(rmse_val) or np.isnan(r2oos_val):
            raise ValueError(
                f"NaN values detected in metrics for model {neural_model_name}:\n"
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
            "time_taken": [neural_time]
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
