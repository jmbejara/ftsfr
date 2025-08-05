# Models - Configuration-Driven Forecasting System

This directory contains a flexible, configuration-driven system for running various time series forecasting models. Instead of generating separate directories for each model, all models are defined in a central configuration file and executed through a unified runner.

## Overview

The new system consists of:

1. **`models_config.toml`** - Central configuration file defining all available models
2. **`run_model.py`** - Unified runner that can execute any model based on configuration
3. **`model_controller.py`** - Controller for orchestrating multiple model runs
4. **`model_classes/`** - Reusable model classes (DartsLocal, DartsGlobal, NixtlaMain, GluontsMain)
5. **`pixi.toml`** - Single environment file with all dependencies

## Usage

### Running a Single Model

```bash
# Activate the environment
pixi shell

# Run a specific model (full workflow)
python run_model.py --model arima

# Run separate workflows
python run_model.py --model transformer --workflow train      # Train and save model
python run_model.py --model transformer --workflow inference  # Load model and predict
python run_model.py --model transformer --workflow evaluate   # Load predictions and calculate errors

# With custom config
python run_model.py --model deepar --config custom_config.toml --workflow train
```

### Running Multiple Models

```bash
# List all available models
python model_controller.py --list

# Run all models sequentially (full workflow)
python model_controller.py --all

# Run specific models with separate workflows
python model_controller.py --models arima transformer nbeats --workflow train
python model_controller.py --models arima transformer nbeats --workflow inference
python model_controller.py --models arima transformer nbeats --workflow evaluate

# Run all models of a specific class
python model_controller.py --class DartsLocal --workflow train

# Run models in parallel
python model_controller.py --all --parallel --workers 4 --workflow inference

# Save results to file
python model_controller.py --all --save-results results.json
```

## Environment Setup

All models use a single unified environment:

```bash
# For CPU (default)
pixi shell

# For GPU support
pixi shell -e gpu
```

### Testing GPU Availability
Before running GPU-accelerated models, test your GPU setup:
```bash
pixi shell -e gpu
python test_gpu.py
```

## Adding New Models

To add a new model, simply edit `models_config.toml`:

```toml
[my_new_model]
class = "DartsLocal"  # or DartsGlobal, NixtlaMain, GluontsMain
estimator_class = "darts.models.MyNewModel"
display_name = "My New Model"
estimator_params = { param1 = "value1" }

# Optional parameters for DartsGlobal models:
scaling = true
interpolation = true
f32 = false
```

Dataset-specific parameters (seasonality, frequency) are automatically injected based on model type.

## Model Classes

- **DartsLocal**: For univariate models that train separately on each time series
- **DartsGlobal**: For models that train globally across all time series
- **NixtlaMain**: For Nixtla's neuralforecast models
- **GluontsMain**: For GluonTS probabilistic models
- **TimesFM**: Special implementation for Google's TimesFM

## Configuration System

### Dataset Configuration

Dataset-specific parameters are defined in the root `datasets.toml`:

```toml
[us_treasury_returns.ftsfr_treas_bond_returns]
description = """This data module contains the returns of individual treasury bonds sourced from the CRSP database."""
frequency = "ME"
seasonality = 12
```

### Environment Variables

Only one environment variable is required:
- `DATASET_PATH`: Path to the parquet file containing the data

Optional overrides (these override dataset configuration):
- `FREQUENCY`: Time series frequency (e.g., "D", "M", "Q")
- `SEASONALITY`: Seasonal period (e.g., 7 for daily data)
- `OUTPUT_DIR`: Directory for saving results (default: `_output`)
- `TEST_SPLIT`: Fraction of data to use for testing

### Example Usage

```bash
# Basic usage - configuration is automatic
export DATASET_PATH="_data/ftsfr_us_treasury_returns.parquet"
python run_model.py --model arima

# Override seasonality for experimentation
export DATASET_PATH="_data/ftsfr_us_treasury_returns.parquet"
export SEASONALITY="10"
python run_model.py --model arima
```

## Output Structure

Results are saved in the following structure:
```
_output/
├── models/          # Saved trained model files
│   └── {model_name}/{dataset_name}/saved_model.*
├── forecasts/       # Model predictions
│   └── {model_name}/{dataset_name}/forecasts.parquet
├── raw_results/     # Performance metrics (MASE scores)
│   └── {model_name}/{dataset_name}.csv
└── model_logs/      # Execution logs
    └── {model_name}/{dataset_name}.log
```

## Model Workflows for Lambda Labs

Models support separated workflows to optimize costs on cloud computing:

- **`--workflow main`**: Complete pipeline (train → predict → evaluate)
- **`--workflow train`**: Train and save model only
- **`--workflow inference`**: Load model and generate predictions
- **`--workflow evaluate`**: Calculate metrics from saved predictions

### Lambda Labs Strategy

```bash
# 1. Train on GPU instance ($0.75/hour)
export DATASET_PATH="_data/ftsfr_us_treasury_returns.parquet"
pixi shell -e gpu
python model_controller.py --models transformer nbeats --workflow train --parallel

# 2. Switch to CPU instance ($0.20/hour) - models already in persistent storage
export DATASET_PATH="_data/ftsfr_us_treasury_returns.parquet"
pixi shell
python model_controller.py --models transformer nbeats --workflow inference --parallel
```

The `_output/` directory is automatically saved to the persistent filesystem.

**Note**: DartsLocal models (ARIMA, ETS, Prophet) save configuration only and train during inference.

### Troubleshooting

- **Model not found**: Run `--workflow train` before `--workflow inference`
- **Predictions not found**: Run `--workflow inference` before `--workflow evaluate`
- **Environment issues**: Use the same pixi environment for all workflows

## One-Step-Ahead Forecasting

All models use unified one-step-ahead forecasting for consistent evaluation:

- **Training**: Once on 80% of data
- **Testing**: For each test point, forecast one step using actual historical data (never predictions)
- **No retraining** during test period
- **Automatic verification** ensures prediction count matches test period

This avoids look-ahead bias and ensures fair comparison across all model types (Darts, Nixtla, GluonTS).

## Syncing Data with Lambda Labs

To copy data to Lambda Labs:
```bash

# Central Texas, USA us-south-3
NODE_IP="192.222.55.203"
SSH_KEY="jeremy.pem"
FS_FOLDER="central-texas-three-fs"

# Texas, USA us-south-1
NODE_IP="104.171.202.68"
SSH_KEY="jeremy.pem"
FS_FOLDER="texas-one-fs"

# Washington, USA us-east-3
NODE_IP="192.222.50.240"
SSH_KEY="jeremy.pem"
FS_FOLDER="washington-dc-three-fs"

# Utah, USA us-west-3
NODE_IP="209.20.158.246"
SSH_KEY="jeremy.pem"
FS_FOLDER="utah-fs"

ssh -i ~/.ssh/${SSH_KEY} ubuntu@${NODE_IP} "mkdir -p ~/${FS_FOLDER}/ftsfr"
rsync -avzh --progress --delete --exclude='_output/' --exclude='.pixi/' -e "ssh -i ~/.ssh/${SSH_KEY}" ./ ubuntu@${NODE_IP}:~/${FS_FOLDER}/ftsfr/
```

To Connect via SSH:
```bash
ssh -i ~/.ssh/${SSH_KEY} ubuntu@${NODE_IP}
```
