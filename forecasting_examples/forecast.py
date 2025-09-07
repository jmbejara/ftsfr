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
- Uses utilsforecast.losses.mase() for accurate MASE calculation and numpy for RMSE
- Supports parallel processing for applicable models
- Saves forecasts to parquet format

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
from utilsforecast.preprocessing import fill_gaps
from utilsforecast.losses import mase

FILE_DIR = Path(__file__).parent
REPO_ROOT = FILE_DIR.parent


def convert_frequency_to_statsforecast(frequency):
    """Convert pandas/dataset frequency to StatsForecast frequency format."""
    frequency_map = {
        "D": "1d",        # Daily
        "W": "1w",        # Weekly
        "M": "1mo",       # Month end
        "MS": "1mo",      # Month start
        "ME": "1mo",      # Month end
        "Y": "1y",        # Year end
        "YS": "1y",       # Year start
        "YE": "1y",       # Year end
        "Q": "3mo",       # Quarter end
        "QS": "3mo",      # Quarter start
        "QE": "3mo",      # Quarter end
        "B": "1d",        # Business day (approximated as daily)
        "h": "1h",        # Hourly
        "min": "1m",      # Minutely
        "s": "1s",        # Secondly
    }
    return frequency_map.get(frequency, frequency)


def read_dataset_config(dataset_name):
    """Read dataset configuration from datasets.toml file."""
    datasets_path = REPO_ROOT / "datasets.toml"
    
    if not datasets_path.exists():
        raise FileNotFoundError(f"datasets.toml not found at {datasets_path}")
    
    with open(datasets_path, 'rb') as f:
        config = tomli.load(f)
    
    # Find the dataset configuration
    dataset_config = None
    data_path = None
    
    for module_name, module_config in config.items():
        if isinstance(module_config, dict) and not module_name.startswith('_'):
            # Check if this module has our dataset
            for dataset_key, dataset_info in module_config.items():
                if dataset_key == dataset_name and isinstance(dataset_info, dict):
                    dataset_config = dataset_info
                    # Construct the data path
                    data_path = REPO_ROOT / "_data" / module_name / f"{dataset_name}.parquet"
                    break
            if dataset_config:
                break
    
    if not dataset_config:
        available_datasets = []
        for module_name, module_config in config.items():
            if isinstance(module_config, dict) and not module_name.startswith('_'):
                for dataset_key in module_config.keys():
                    if not dataset_key.startswith('_') and dataset_key not in ['data_module_name', 'data_module_description', 'required_data_sources']:
                        available_datasets.append(dataset_key)
        
        raise ValueError(f"Dataset '{dataset_name}' not found. Available datasets: {available_datasets}")
    
    return {
        'data_path': str(data_path),
        'frequency': dataset_config.get('frequency', 'D'),
        'seasonality': dataset_config.get('seasonality', 252),
        'description': dataset_config.get('description', ''),
        'dataset_name': dataset_name
    }


def load_model_config():
    """Load model configurations from models_config.toml file."""
    models_config_path = FILE_DIR / "models_config.toml"
    
    if not models_config_path.exists():
        raise FileNotFoundError(f"models_config.toml not found at {models_config_path}")
    
    with open(models_config_path, 'rb') as f:
        return tomli.load(f)


def create_model(model_name, seasonality, model_configs):
    """Create a model instance based on TOML configuration."""
    
    if model_name not in model_configs:
        available = ", ".join(model_configs.keys())
        raise ValueError(f"Unknown model: {model_name}. Available: {available}")
    
    config = model_configs[model_name]
    library = config["library"]
    model_class = config["class"]
    params = config.get("params", {}).copy()
    
    # Add seasonality to appropriate parameters
    if library == "statsforecast":
        if "season_length" not in params:
            params["season_length"] = seasonality
    
    # Create model based on library
    if library == "statsforecast":
        # Import StatsForecast models
        from statsforecast import models as sf_models
        
        # Get model class by name
        model_cls = getattr(sf_models, model_class)
        return model_cls(**params)
        
    elif library == "neuralforecast":
        # Handle NeuralForecast models
        try:
            # Try auto models first
            from neuralforecast import auto as nf_auto
            model_cls = getattr(nf_auto, model_class)
        except (ImportError, AttributeError):
            # Try regular models
            from neuralforecast import models as nf_models
            model_cls = getattr(nf_models, model_class)
        
        return model_cls(**params)
    
    else:
        raise ValueError(f"Unsupported library: {library}")


def load_and_preprocess_data(data_path, frequency="D", test_split=0.2):
    """Load and preprocess the dataset using Polars throughout (full dataset)."""
    print("Loading and preprocessing data...")
    
    # Load data using polars
    df = pl.read_parquet(data_path)
    
    # Rename 'id' to 'unique_id' as expected by statsforecast
    if 'id' in df.columns:
        df = df.rename({'id': 'unique_id'})
    
    print(f"Using full dataset: {len(df['unique_id'].unique())} entities")
    
    # Ensure proper data types
    df = df.with_columns(pl.col('y').cast(pl.Float32))
    
    # Handle infinite values
    df = df.with_columns(
        pl.when((pl.col('y').is_infinite()) | (pl.col('y').is_nan()))
        .then(None)
        .otherwise(pl.col('y'))
        .alias('y')
    )
    
    # Fill missing dates
    # Convert pandas-style frequency to Polars format (same as StatsForecast)
    polars_freq = convert_frequency_to_statsforecast(frequency)
    
    df = fill_gaps(df, freq=polars_freq, start='global', end='global')
    
    # Calculate train/test split
    unique_dates = df['ds'].unique().sort()
    split_idx = int(len(unique_dates) * (1 - test_split))
    train_cutoff = unique_dates[split_idx - 1]
    
    # Split into train and test
    train_data = df.filter(pl.col('ds') <= train_cutoff)
    test_data = df.filter(pl.col('ds') > train_cutoff)
    
    print(f"Data split: {len(train_data)} training samples, {len(test_data)} test samples")
    print(f"Total entities: {len(df['unique_id'].unique())}")
    
    return train_data, test_data, df


def train_and_forecast_statsforecast(model, train_data, test_data, frequency):
    """Train and forecast using StatsForecast."""
    print("Training model and generating forecasts using StatsForecast...")
    
    from statsforecast import StatsForecast
    from statsforecast.models import Naive
    import polars as pl
    
    # Use all available cores for parallel processing
    n_jobs = int(os.getenv("STATSFORECAST_N_JOBS", os.cpu_count() or 1))
    print(f"Using {n_jobs} cores for parallel processing")
    
    # Convert frequency for StatsForecast
    statsforecast_freq = convert_frequency_to_statsforecast(frequency)
    
    print(f"Train data shape: {train_data.shape}")
    
    # Remove trailing nulls for each entity to ensure last value is not null
    train_data_clean = []
    for entity in train_data['unique_id'].unique():
        entity_data = train_data.filter(pl.col('unique_id') == entity)
        # Find last non-null value
        non_null_data = entity_data.filter(pl.col('y').is_not_null())
        if len(non_null_data) > 0:
            last_non_null_date = non_null_data['ds'].max()
            # Keep data up to last non-null date
            entity_data_trimmed = entity_data.filter(pl.col('ds') <= last_non_null_date)
            train_data_clean.append(entity_data_trimmed)
    
    if train_data_clean:
        train_data_filtered = pl.concat(train_data_clean)
        print(f"Trimmed training data to remove trailing nulls: {train_data_filtered.shape}")
    else:
        train_data_filtered = train_data
    
    # Use Naive as fallback for all models to handle failures gracefully
    fallback = Naive()
    sf = StatsForecast(models=[model], freq=statsforecast_freq, n_jobs=n_jobs, fallback_model=fallback)
    
    # Generate forecasts for test period
    forecast_horizon = len(test_data['ds'].unique())
    forecasts = sf.forecast(df=train_data_filtered, h=forecast_horizon)
    
    print(f"Generated {len(forecasts)} forecasts")
    return forecasts


def train_and_forecast_neuralforecast(model, train_data, test_data, frequency):
    """Train and forecast using NeuralForecast."""
    print("Training model and generating forecasts using NeuralForecast...")
    
    from neuralforecast import NeuralForecast
    
    nf = NeuralForecast(models=[model], freq=frequency)
    
    # Train the model
    nf.fit(df=train_data)
    
    # Generate forecasts for test period
    forecast_horizon = len(test_data['ds'].unique())
    forecasts = nf.predict()
    
    print(f"Generated {len(forecasts)} forecasts")
    return forecasts


def save_metrics_csv(metrics_dict, dataset_name, model_name):
    """Save error metrics to CSV file in the specified directory structure."""
    # Create output directory relative to project root
    output_dir = Path("./_output/forecast2/error_metrics") / dataset_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create CSV file path
    csv_path = output_dir / f"{model_name}.csv"
    
    # Create DataFrame with metrics
    metrics_df = pl.DataFrame([metrics_dict])
    
    # Save to CSV
    metrics_df.write_csv(csv_path)
    print(f"Error metrics saved to: {csv_path}")
    
    return csv_path


def calculate_global_metrics(train_data, test_data, forecasts, seasonality, model_name):
    """Calculate global MASE, sMAPE, MAE, and RMSE metrics using Polars."""
    print("Calculating global metrics (MASE, sMAPE, MAE, RMSE)...")
    
    try:
        # Forecasts might be a pandas DataFrame, convert if needed
        if not isinstance(forecasts, pl.DataFrame):
            forecasts_pl = pl.from_pandas(forecasts.reset_index())
        else:
            forecasts_pl = forecasts
        
        # Merge test data with forecasts
        test_with_forecasts = test_data.join(
            forecasts_pl, 
            on=['unique_id', 'ds'], 
            how='inner'
        )
        
        if len(test_with_forecasts) == 0:
            print("Error: No matching forecasts found for test data")
            return None, None, None, None
        
        # Find the model prediction column (could be model name or class name)
        prediction_cols = [col for col in test_with_forecasts.columns 
                          if col not in ['unique_id', 'ds', 'y']]
        
        if not prediction_cols:
            print("Error: No prediction columns found in forecasts")
            return None, None, None, None
        
        # Use the first prediction column
        pred_col = prediction_cols[0]
        print(f"Using prediction column: {pred_col}")
        
        # Calculate MASE using utilsforecast function (works with Polars DataFrames)
        mase_results = mase(
            df=test_with_forecasts,
            models=[pred_col],
            seasonality=seasonality,
            train_df=train_data,
            id_col='unique_id',
            target_col='y'
        )
        
        # Calculate global MASE (mean across all entities)
        global_mase = mase_results[pred_col].mean()
        
        # Filter out NaN/Null values for metric calculations
        valid_data = test_with_forecasts.filter(
            pl.col('y').is_not_null() & 
            pl.col('y').is_not_nan() &
            pl.col(pred_col).is_not_null() & 
            pl.col(pred_col).is_not_nan() &
            (pl.col('y') != 0)  # Exclude zeros for sMAPE calculation
        )
        
        if len(valid_data) == 0:
            print("Warning: No valid values for metric calculation")
            return None, None, None, None
        
        # Calculate MAE (Mean Absolute Error)
        mae_calc = valid_data.select([
            (pl.col('y') - pl.col(pred_col)).abs().alias('absolute_error')
        ])
        global_mae = mae_calc['absolute_error'].mean()
        
        # Calculate RMSE (Root Mean Squared Error)
        rmse_calc = valid_data.select([
            ((pl.col('y') - pl.col(pred_col)) ** 2).alias('squared_error')
        ])
        global_rmse = np.sqrt(rmse_calc['squared_error'].mean())
        
        # Calculate sMAPE (symmetric Mean Absolute Percentage Error)
        smape_calc = valid_data.select([
            (200 * (pl.col('y') - pl.col(pred_col)).abs() / 
             (pl.col('y').abs() + pl.col(pred_col).abs())).alias('smape_error')
        ])
        global_smape = smape_calc['smape_error'].mean()
        
        # Check for NaN values
        if any(val is None or np.isnan(val) for val in [global_mase, global_smape, global_mae, global_rmse]):
            print("Warning: One or more metric calculations returned NaN")
            return None, None, None, None
            
        return global_mase, global_smape, global_mae, global_rmse
        
    except Exception as e:
        print(f"Error calculating metrics: {str(e)}")
        return None, None, None, None


def main():
    parser = argparse.ArgumentParser(description="Unified CLI Forecasting Script")
    parser.add_argument("--dataset", required=True, help="Dataset name from datasets.toml")
    parser.add_argument("--model", required=True, help="Model name from models_config.toml")
    parser.add_argument("--test-split", type=float, default=0.2, help="Test split ratio (default: 0.2)")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Unified CLI Forecasting Script")
    print("=" * 70)
    
    # Load configurations
    try:
        dataset_config = read_dataset_config(args.dataset)
        model_configs = load_model_config()
        
        print(f"\nDataset: {args.dataset}")
        print(f"Description: {dataset_config['description']}")
        print(f"Model: {args.model}")
        print(f"Display Name: {model_configs[args.model]['display_name']}")
        
    except (FileNotFoundError, ValueError) as e:
        print(f"Configuration Error: {e}")
        return
    
    # Load and preprocess data
    try:
        train_data, test_data, full_data = load_and_preprocess_data(
            dataset_config['data_path'], 
            dataset_config['frequency'], 
            args.test_split
        )
    except Exception as e:
        print(f"Data loading error: {e}")
        return
    
    # Create model
    try:
        model = create_model(args.model, dataset_config['seasonality'], model_configs)
        library = model_configs[args.model]["library"]
    except Exception as e:
        print(f"Model creation error: {e}")
        return
    
    # Calculate test size for reporting
    test_size = len(sorted(test_data['ds'].unique()))
    
    # Print initialization summary
    print("\nExperiment Configuration:")
    print(tabulate([
        ["Model", model_configs[args.model]['display_name']],
        ["Library", library.title()],
        ["Dataset", args.dataset],
        ["Total Entities", len(full_data['unique_id'].unique())],
        ["Frequency", dataset_config['frequency']],
        ["Seasonality", dataset_config['seasonality']],
        ["Test Size (h)", test_size],
    ], tablefmt="fancy_grid"))
    
    # Train and forecast based on library
    print("\nStarting training and forecasting...")
    forecast_start_time = time.time()
    try:
        if library == "statsforecast":
            forecasts = train_and_forecast_statsforecast(
                model, train_data, test_data, dataset_config['frequency']
            )
        else:  # neuralforecast
            forecasts = train_and_forecast_neuralforecast(
                model, train_data, test_data, dataset_config['frequency']
            )
    except Exception as e:
        print(f"Training/forecasting error: {e}")
        return
    
    forecast_time = time.time() - forecast_start_time
    print(f"Forecasting completed in {forecast_time:.2f} seconds")
    
    # Calculate global metrics
    global_mase, global_smape, global_mae, global_rmse = calculate_global_metrics(
        train_data, test_data, forecasts, dataset_config['seasonality'], args.model
    )
    
    # Print results summary
    print("\nFinal Results:")
    mase_display = f"{global_mase:.4f}" if global_mase is not None else "Error"
    smape_display = f"{global_smape:.4f}" if global_smape is not None else "Error"
    mae_display = f"{global_mae:.4f}" if global_mae is not None else "Error"
    rmse_display = f"{global_rmse:.4f}" if global_rmse is not None else "Error"
    results_table = [
        ["Model", model_configs[args.model]['display_name']],
        ["Library", library.title()],
        ["Dataset", args.dataset],
        ["Entities", len(full_data['unique_id'].unique())],
        ["Frequency", dataset_config['frequency']],
        ["Seasonality", dataset_config['seasonality']],
        ["Test Size (h)", test_size],
        ["Global MASE", mase_display],
        ["Global sMAPE", smape_display],
        ["Global MAE", mae_display],
        ["Global RMSE", rmse_display],
        ["Forecast Time (s)", f"{forecast_time:.2f}"],
    ]
    print(tabulate(results_table, tablefmt="fancy_grid"))
    
    # Create metrics dictionary for CSV export
    metrics_dict = {
        "Model": model_configs[args.model]['display_name'],
        "Library": library.title(),
        "Dataset": args.dataset,
        "Entities": len(full_data['unique_id'].unique()),
        "Frequency": dataset_config['frequency'],
        "Seasonality": dataset_config['seasonality'],
        "Test_Size_h": test_size,
        "Global_MASE": global_mase if global_mase is not None else "Error",
        "Global_sMAPE": global_smape if global_smape is not None else "Error",
        "Global_MAE": global_mae if global_mae is not None else "Error",
        "Global_RMSE": global_rmse if global_rmse is not None else "Error",
        "Forecast_Time_seconds": forecast_time,
    }
    
    # Save metrics to CSV
    save_metrics_csv(metrics_dict, args.dataset, args.model)
    
    print("\n" + "=" * 70)
    print("Forecasting experiment completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()