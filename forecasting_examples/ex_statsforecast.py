"""
Vanilla StatsForecast Example Script

This script mimics the behavior of running:
python models/run_model.py --model auto_arima_fast --dataset-path /Users/jbejarano/GitRepositories/ftsfr/_data/ken_french_data_library/ftsfr_french_portfolios_25_daily_size_and_bm.parquet

But using vanilla polars + statsforecast without custom classes.
Based on the nixtlaverse walkthrough: https://nixtlaverse.nixtla.io/statsforecast/docs/getting-started/3_Getting_Started_complete_polars

Key Features:
- Uses AutoARIMA with fast configuration (approximation=True, stepwise=True, limited model search)
- Implements the same data preprocessing as the original codebase
- Calculates MASE, MAE, and RMSE error metrics
- Supports parallel processing
- Saves forecasts to parquet format

Configuration:
- By default, uses a subset of 5 entities and 2 years for demonstration
- For full dataset processing, modify subset_entities and subset_years in main()
- The French portfolios dataset has 25 entities with daily data from 1926-2024
"""

import os
import numpy as np
import pandas as pd
import polars as pl
from pathlib import Path
from tabulate import tabulate
from utilsforecast.preprocessing import fill_gaps
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA

FILE_DIR = Path(__file__).parent

def load_and_preprocess_data(data_path, frequency="D", seasonality=252, test_split=0.2, subset_entities=5, subset_years=2):
    """Load and preprocess the dataset following the same logic as the original codebase."""
    print("Loading and preprocessing data...")
    
    # Load data using polars
    df = pl.read_parquet(data_path)
    
    # Convert to pandas for compatibility with statsforecast utilities
    df_pd = df.to_pandas()
    
    # Rename 'id' to 'unique_id' as expected by statsforecast
    if 'id' in df_pd.columns:
        df_pd = df_pd.rename(columns={'id': 'unique_id'})
    
    # For demonstration purposes, use only a subset of entities and recent years
    unique_entities = df_pd['unique_id'].unique()[:subset_entities]
    df_pd = df_pd[df_pd['unique_id'].isin(unique_entities)]
    
    # Keep only recent years for faster processing
    latest_date = df_pd['ds'].max()
    cutoff_date = latest_date - pd.DateOffset(years=subset_years)
    df_pd = df_pd[df_pd['ds'] >= cutoff_date]
    
    print(f"Using subset: {len(unique_entities)} entities, last {subset_years} years")
    
    # Ensure proper data types
    df_pd['y'] = df_pd['y'].astype(np.float32)
    
    # Handle infinite values
    df_pd.loc[(df_pd['y'] == float('inf')) | (df_pd['y'] == float('-inf')), 'y'] = np.nan
    
    # Fill missing dates
    df_pd = fill_gaps(df_pd, freq=frequency, start='global', end='global')
    
    # Calculate train/test split
    unique_dates = sorted(df_pd['ds'].unique())
    split_idx = int(len(unique_dates) * (1 - test_split))
    train_cutoff = unique_dates[split_idx - 1]
    
    # Split into train and test
    train_data = df_pd[df_pd['ds'] <= train_cutoff].copy()
    test_data = df_pd[df_pd['ds'] > train_cutoff].copy()
    
    print(f"Data split: {len(train_data)} training samples, {len(test_data)} test samples")
    print(f"Total entities: {len(df_pd['unique_id'].unique())}")
    
    return train_data, test_data, df_pd


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
        nmodels=5
    )


def perform_forecasting(sf_model, train_data, test_data):
    """Perform multi-step forecasting for efficiency."""
    print("Starting forecasting...")
    
    # Calculate forecast horizon
    test_dates = sorted(test_data['ds'].unique())
    h = len(test_dates)
    
    print(f"Forecasting {h} steps ahead...")
    
    # Generate forecasts
    forecasts = sf_model.forecast(df=train_data, h=h)
    
    # The forecasts come with a ds column that represents forecast steps
    # We need to map these to actual test dates
    forecasts = forecasts.reset_index()
    
    # Map forecast indices to test dates (for future use if needed)
    # test_dates_mapping = {i: date for i, date in enumerate(test_dates)}
    
    # Add proper dates to forecasts
    expanded_forecasts = []
    for _, row in forecasts.iterrows():
        # Get the forecast step (0-based index)
        if 'ds' in row:
            forecast_step = pd.to_datetime(row['ds'])
            # Find the corresponding test date index
            last_train_date = train_data['ds'].max()
            days_ahead = (forecast_step - last_train_date).days - 1
            if days_ahead < len(test_dates):
                actual_date = test_dates[days_ahead]
            else:
                continue
        else:
            # Fallback - use row index
            actual_date = test_dates[len(expanded_forecasts) % len(test_dates)]
        
        # Get model prediction
        model_pred = row.get('AutoARIMA', 0)
        
        expanded_forecasts.append({
            'unique_id': row['unique_id'],
            'ds': actual_date,
            'y': model_pred
        })
    
    pred_data = pd.DataFrame(expanded_forecasts)
    print(f"Generated {len(pred_data)} forecasts")
    print("Forecasting completed")
    return pred_data


def calculate_error_metrics(test_data, pred_data, train_data, seasonality):
    """Calculate MASE, MAE, and RMSE metrics using simple pandas operations."""
    print("Calculating error metrics...")
    
    # Align test and prediction data
    merged = test_data.merge(pred_data, on=['unique_id', 'ds'], suffixes=('_actual', '_pred'))
    
    # Calculate MAE
    mae_value = np.mean(np.abs(merged['y_actual'] - merged['y_pred']))
    
    # Calculate RMSE
    rmse_value = np.sqrt(np.mean((merged['y_actual'] - merged['y_pred']) ** 2))
    
    # Calculate MASE (simplified version)
    # MASE = MAE / naive_mae where naive_mae is seasonal naive forecast error
    entities_mase = []
    for entity in merged['unique_id'].unique():
        entity_data = merged[merged['unique_id'] == entity].sort_values('ds')
        entity_train = train_data[train_data['unique_id'] == entity].sort_values('ds')
        
        if len(entity_train) > seasonality:
            # Calculate seasonal naive forecast error on training data
            train_values = entity_train['y'].values
            seasonal_naive_errors = np.abs(train_values[seasonality:] - train_values[:-seasonality])
            naive_mae = np.mean(seasonal_naive_errors)
            
            if naive_mae > 0:
                entity_mae = np.mean(np.abs(entity_data['y_actual'] - entity_data['y_pred']))
                entities_mase.append(entity_mae / naive_mae)
    
    mase_value = np.mean(entities_mase) if entities_mase else mae_value
    
    return {
        'MASE': mase_value,
        'MAE': mae_value,
        'RMSE': rmse_value
    }


def main():
    """Main execution function."""
    # Configuration (matching the command line arguments)
    data_path = "/Users/jbejarano/GitRepositories/ftsfr/_data/ken_french_data_library/ftsfr_french_portfolios_25_daily_size_and_bm.parquet"
    model_name = "auto_arima_fast"
    frequency = "D"
    seasonality = 252
    test_split = 0.2
    
    # Subset configuration for faster processing
    # For full dataset processing, set subset_entities=25 and subset_years=10+
    # Current settings use 5 entities and 2 years for demonstration
    subset_entities = 5
    subset_years = 2
    
    print("=" * 60)
    print("Vanilla StatsForecast Example - AutoARIMA Fast")
    print("=" * 60)
    
    # Load and preprocess data
    train_data, test_data, full_data = load_and_preprocess_data(
        data_path, frequency, seasonality, test_split, subset_entities, subset_years
    )
    
    # Print initialization summary
    print("\nObject Initialized:")
    print(tabulate([
        ["Model", model_name],
        ["Dataset", "french_portfolios_25_daily_size_and_bm"],
        ["Total Entities", len(full_data['unique_id'].unique())],
    ], tablefmt="fancy_grid"))
    
    # Create model
    print("\nCreating AutoARIMA model with fast configuration...")
    model = create_autoarima_model(seasonality)
    
    # Create StatsForecast wrapper
    n_jobs = int(os.getenv("STATSFORECAST_N_JOBS", os.cpu_count() or 1))
    print(f"Using {n_jobs} cores for parallel processing")
    
    sf = StatsForecast(
        models=[model],
        freq=frequency,
        n_jobs=n_jobs
    )
    
    # Train model
    print("Training model...")
    sf.fit(df=train_data)
    print("Model training completed")
    
    # Perform forecasting
    pred_data = perform_forecasting(sf, train_data, test_data)
    
    # Calculate error metrics
    errors = calculate_error_metrics(test_data, pred_data, train_data, seasonality)
    
    # Print results summary
    print("\nFinal Results:")
    print(tabulate([
        ["Model", model_name],
        ["Dataset", "french_portfolios_25_daily_size_and_bm"],
        ["Entities", len(train_data['unique_id'].unique())],
        ["Frequency", frequency],
        ["Seasonality", seasonality],
        ["Global MASE", f"{errors['MASE']:.4f}"],
        ["Global MAE", f"{errors['MAE']:.4f}"],
        ["Global RMSE", f"{errors['RMSE']:.4f}"],
    ], tablefmt="fancy_grid"))
    
    # Save forecasts
    output_dir = FILE_DIR / "forecasting_examples_output"
    output_dir.mkdir(exist_ok=True)
    forecast_path = output_dir / "ex_statsforecast_forecasts.parquet"
    
    # Convert to polars for saving
    pred_data_pl = pl.from_pandas(pred_data)
    pred_data_pl.write_parquet(forecast_path)
    print(f"\nForecasts saved to: {forecast_path}")
    
    print("\n" + "=" * 60)
    print("StatsForecast example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()