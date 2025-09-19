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

from forecast_utils import read_dataset_config, load_and_preprocess_data

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
from utilsforecast.losses import mase, mse, rmse

warnings.filterwarnings("ignore")

# NUM_SAMPLES = 4
NUM_SAMPLES = 20

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


def evaluate_cv(cv_df, train_df, seasonality):
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


def create_auto_config_nhits(seasonality, lightning_logs_dir=None):
    """Create configuration for AutoNHITS with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (12, 24, 48)  # Fixed smaller sizes for short series
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
                "max_steps", (500, 1000)
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


def create_auto_config_lstm(seasonality):
    """Create configuration for AutoLSTM with optuna backend."""
    def config(trial):
        return {
            "input_size": trial.suggest_categorical(
                "input_size", (12, 24, 48)  # Fixed smaller sizes for short series
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
                (500, 1000)
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


def create_auto_config_simple(seasonality, lightning_logs_dir=None):
    """Create simple configuration for linear models with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (12, 24, 48)  # Fixed smaller sizes for short series
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
                (500, 1000)  # Reduced training time
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


def create_auto_config_deepar(seasonality, lightning_logs_dir=None):
    """Create configuration for AutoDeepAR with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (12, 24, 48)  # Fixed smaller sizes for short series
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
                "max_steps", (500, 1000)
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


def create_auto_config_nbeats(seasonality, lightning_logs_dir=None):
    """Create configuration for AutoNBEATS with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (12, 24, 48)  # Fixed smaller sizes for short series
            ),
            "max_steps": trial.suggest_categorical(
                "max_steps", (500, 1000)
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


def create_auto_config_transformer(seasonality, lightning_logs_dir=None):
    """Create configuration for AutoVanillaTransformer with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (12, 24, 48)  # Fixed smaller sizes for short series
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
                "max_steps", (500, 1000)
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


def create_auto_config_tide(seasonality, lightning_logs_dir=None):
    """Create configuration for AutoTiDE with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (12, 24, 48)  # Fixed smaller sizes for short series
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
                "max_steps", (500, 1000)
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


def create_auto_config_kan(seasonality, lightning_logs_dir=None):
    """Create configuration for AutoKAN with optuna backend."""
    def config(trial):
        config_dict = {
            "input_size": trial.suggest_categorical(
                "input_size", (12, 24, 48)  # Fixed smaller sizes for short series
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
                "max_steps", (500, 1000)
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
    args = parser.parse_args()

    DATASET_NAME = args.dataset
    MODEL_NAME = args.model

    print("=" * 60)
    print("Neural Forecast with Cross-Validation")
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

    # Get proper test size from actual test split
    test_size = int(test_data["ds"].n_unique())
    print(f"Calculated test size from data split: {test_size}")

    # Use full dataset for cross-validation (concatenate train and test)
    full_data = train_data.select(['unique_id', 'ds', 'y']).vstack(
        test_data.select(['unique_id', 'ds', 'y'])
    ).sort(['unique_id', 'ds'])

    # Keep data in Polars format
    df = full_data

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
        "auto_deepar": AutoDeepAR(h=test_size, config=create_auto_config_deepar(seasonality, lightning_logs_dir),
                                  loss=DistributionLoss(distribution='Normal'),
                                  backend='optuna', num_samples=NUM_SAMPLES),
        "auto_nbeats": AutoNBEATS(h=test_size, config=create_auto_config_nbeats(seasonality, lightning_logs_dir),
                                  loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
        "auto_nhits": AutoNHITS(h=test_size, config=create_auto_config_nhits(seasonality, lightning_logs_dir),
                                loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
        "auto_dlinear": AutoDLinear(h=test_size, config=create_auto_config_simple(seasonality, lightning_logs_dir),
                                    loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
        "auto_nlinear": AutoNLinear(h=test_size, config=create_auto_config_simple(seasonality, lightning_logs_dir),
                                    loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
        "auto_vanilla_transformer": AutoVanillaTransformer(h=test_size, config=create_auto_config_transformer(seasonality, lightning_logs_dir),
                                                           loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
        "auto_tide": AutoTiDE(h=test_size, config=create_auto_config_tide(seasonality, lightning_logs_dir),
                              loss=MAE(), backend='optuna', num_samples=NUM_SAMPLES),
        "auto_kan": AutoKAN(h=test_size, config=create_auto_config_kan(seasonality, lightning_logs_dir),
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
        metrics_data = {
            "model_name": [MODEL_NAME],
            "dataset_name": [DATASET_NAME],
            "MASE": [avg_metrics[neural_model_name]['MASE']],
            "MSE": [avg_metrics[neural_model_name]['MSE']],
            "RMSE": [avg_metrics[neural_model_name]['RMSE']],
            "R2oos": [avg_metrics[neural_model_name]['R2oos']],
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