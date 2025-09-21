# Forecasting System

Simple time series forecasting using statistical and neural models.

## Overview

This system provides two forecasting approaches:

- **`forecast_stats.py`** - Statistical models (AutoARIMA, Seasonal Naive, etc.)
- **`forecast_neural.py`** - Neural models (AutoNBEATS, AutoDeepAR, etc.) with baseline comparisons

Both scripts use the same preprocessing pipeline to ensure consistent, fair comparisons.

## Quick Start

### Statistical Models
```bash
# Run AutoARIMA on CDS data
python forecast_stats.py --dataset ftsfr_CDS_bond_basis_non_aggregated --model auto_arima

# Debug mode (faster, limited data)
python forecast_stats.py --dataset ftsfr_CDS_bond_basis_non_aggregated --model auto_arima --debug
```

### Neural Models
```bash
# Run AutoNBEATS with baseline comparisons
python forecast_neural.py --dataset ftsfr_CDS_bond_basis_non_aggregated --model auto_nbeats

# Debug mode (fewer hyperparameter samples)
python forecast_neural.py --dataset ftsfr_CDS_bond_basis_non_aggregated --model auto_deepar --debug
```

## Available Models

### Statistical Models (`forecast_stats.py`)
- `auto_arima` - Automatic ARIMA selection
- `auto_ets` - Automatic exponential smoothing
- `seasonal_naive` - Seasonal random walk baseline
- `historic_average` - Simple mean baseline
- `theta` - Theta method forecasting

### Neural Models (`forecast_neural.py`)
- `auto_nbeats` - Neural basis expansion
- `auto_nhits` - Hierarchical interpolation transformer
- `auto_deepar` - Deep autoregressive model
- `auto_dlinear` - Deep linear model
- `auto_vanilla_transformer` - Vanilla transformer

## How It Works

Both scripts follow the same 3-step process:

### 1. Core Preprocessing (`robust_preprocess_pipeline`)
- Load and clean raw data
- Build regular time grids (fill missing dates)
- Split into train/test sets
- Filter out poor-quality series
- Apply light train-only imputation

### 2. Model-Specific Validation
- Additional quality checks for each model type
- Remove series with insufficient data or extreme values
- Ensure data compatibility with chosen models

### 3. Cross-Validation & Evaluation
- Run forecasting with up to 6 rolling windows (capped by the shortest series)
- Calculate multiple metrics: MASE, MSE, RMSE, R²oos
- Save results to CSV files

## What You Get

### Console Output
```
============================================================
Simple Forecast Statistics with Cross-Validation
============================================================
Dataset: ftsfr_CDS_bond_basis_non_aggregated
Model: auto_arima

1. Loading Dataset: ftsfr_CDS_bond_basis_non_aggregated
----------------------------------------
Frequency: ME (Polars: 1mo)
Seasonality: 1
Test size (forecast horizon): 1
Cross-validation windows (max 6): 6

2. Loading and Preprocessing Data
----------------------------------------
Raw data loaded: 91,742 observations, 3,402 series
==================================================
ROBUST PREPROCESSING PIPELINE
==================================================
Final datasets: 291 series
Train: 18,526 observations
Test: 10,476 observations
==================================================

[... model training ...]

6. Model Performance Summary (rolling windows)
----------------------------------------------
+-----------+------------+-----------+------------+-------------+
| Model     |   Avg MASE |   Avg MSE |   Avg RMSE |   Avg R2oos |
+===========+============+===========+============+=============+
| AutoARIMA |     0.8234 |    2.4567 |     1.5674 |      0.1234 |
+-----------+------------+-----------+------------+-------------+
```

### File Outputs

**Error Metrics** (`./_output/forecasting/error_metrics/{dataset}/{model}.csv`):
```csv
model_name,dataset_name,MASE,MSE,RMSE,R2oos,time_taken
auto_arima,ftsfr_CDS_bond_basis_non_aggregated,0.8234,2.4567,1.5674,0.1234,45.67
```

**Training Logs** (Neural models only: `./_output/forecasting/logs/{dataset}/{model}/`):
- Hyperparameter optimization trials
- Model checkpoints and performance

## When to Use Which

### Use Statistical Models When:
- You want fast, interpretable baselines
- Working with well-behaved time series
- Need quick results for comparison
- Data has clear seasonal patterns

### Use Neural Models When:
- You have complex, non-linear patterns
- Working with many related series (panel data)
- Want state-of-the-art performance
- Have time for hyperparameter optimization

## Common Issues

### "No series meet the data quality requirements"
**Problem**: All series filtered out during preprocessing.

**Solutions**:
- Use `--debug` mode to see what's being filtered and why
- Try datasets with longer, more complete series
- Check data quality (many missing values?)

### Neural models taking too long
**Solutions**:
- Use `--debug` mode (much faster)
- Try simpler models like `auto_dlinear`
- Use smaller datasets for testing

### Memory issues
**Solutions**:
- Use `--debug` mode to limit data size
- Process datasets in chunks
- Use cloud instances with more memory

### Inconsistent results
**Causes**:
- Neural models use random initialization
- Different data quality filtering

**Solutions**:
- Run multiple times and average results
- Use statistical models for reproducible baselines
- Set random seeds in configs

## Debug Mode

Both scripts support `--debug` mode for faster development:

- **Statistical**: Limits to 20 series
- **Neural**: Limits to 20 series + 2 hyperparameter samples (vs 20)

Perfect for testing before running full experiments.

## Output Structure
```
_output/forecasting/
├── error_metrics/
│   └── {dataset}/
│       ├── auto_arima.csv
│       ├── auto_nbeats.csv
│       └── ...
└── logs/
    └── {dataset}/
        └── {neural_model}/
            └── [training logs]
```

## Technical Details

### Dependencies
- **Polars**: Fast dataframe operations
- **StatsForecast**: Classical time series models
- **NeuralForecast**: Neural models with auto-tuning
- **Optuna**: Hyperparameter optimization

### Data Requirements
- Parquet files with `unique_id`, `ds`, `y` columns
- Regular time frequencies (daily, monthly, etc.)
- Sufficient series length for train/test splitting

### Forecast Horizons & Windows
- Daily (`D`): 30-day horizon, step size 30, up to 6 rolling windows (capped by history)
- Business day (`B`): 21-trading-day horizon, step size 21, up to 6 windows
- Monthly (`ME`/`MS`): 1-month horizon, step size 1, up to 6 windows
- Quarterly (`QE`/`QS`): 1-quarter horizon, step size 1, up to 6 windows
- Other frequencies default to a single-step horizon with a maximum of 6 windows

### Key Functions
- `robust_preprocess_pipeline()`: Core preprocessing
- `evaluate_cv()`: Model evaluation and metrics
- `get_data_requirements()`: Quality filtering rules

Both scripts are designed to handle real-world financial time series with missing values, irregular patterns, and varying lengths while ensuring fair, consistent comparisons between different modeling approaches.
