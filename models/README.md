# Models - Configuration-Driven Forecasting System

This directory contains a flexible, configuration-driven system for running various time series forecasting models. Instead of generating separate directories for each model, all models are defined in a central configuration file and executed through a unified runner.

## Overview

The new system consists of:

1. **`models_config.toml`** - Central configuration file defining all available models
2. **`run_model.py`** - Unified runner that can execute any model based on configuration
3. **`model_controller.py`** - Controller for orchestrating multiple model runs
4. **`model_classes/`** - Reusable model classes (DartsLocal, DartsGlobal, NixtlaMain, GluontsMain)
5. **`pixi_*.toml`** - Consolidated environment files grouped by framework

## Usage

### Running a Single Model

```bash
# Activate the appropriate environment
pixi shell -f pixi_darts.toml

# Run a specific model
python run_model.py --model arima
python run_model.py --model transformer
python run_model.py --model deepar --config custom_config.toml
```

### Running Multiple Models

```bash
# List all available models
python model_controller.py --list

# Run all models sequentially
python model_controller.py --all

# Run specific models
python model_controller.py --models arima transformer nbeats

# Run all models of a specific class
python model_controller.py --class DartsLocal

# Run models in parallel
python model_controller.py --all --parallel --workers 4

# Save results to file
python model_controller.py --all --save-results results.json
```

## Environment Setup

Different frameworks require different environments:

### Testing GPU Availability
Before running GPU-accelerated models, test your GPU setup:
```bash
# Test all frameworks
python test_gpu.py

# Test specific framework
python test_gpu.py --framework torch
python test_gpu.py --framework tensorflow
```

### Darts Models
```bash
pixi shell -f pixi_darts.toml
# For GPU support:
pixi shell -f pixi_darts.toml -e gpu
```

### GluonTS Models
```bash
pixi shell -f pixi_gluonts.toml
```

### Nixtla Models
```bash
pixi shell -f pixi_nixtla.toml
```

### TimesFM
```bash
pixi shell -f pixi_timesfm.toml
```

## Adding New Models

To add a new model, simply edit `models_config.toml`:

```toml
[my_new_model]
class = "DartsLocal"  # or DartsGlobal, NixtlaMain, GluontsMain
estimator_class = "darts.models.MyNewModel"
display_name = "My New Model"
estimator_params = { param1 = "value1", param2 = "env_vars[2] * 4" }

# Optional parameters for DartsGlobal models:
scaling = true
interpolation = true
f32 = false
```

## Model Classes

- **DartsLocal**: For univariate models that train separately on each time series
- **DartsGlobal**: For models that train globally across all time series
- **NixtlaMain**: For Nixtla's neuralforecast models
- **GluontsMain**: For GluonTS probabilistic models
- **TimesFM**: Special implementation for Google's TimesFM

## Environment Variables

Models expect these environment variables:
- `DATASET_PATH`: Path to the parquet file containing the data
- `FREQUENCY`: Time series frequency (e.g., "D", "M", "Q")
- `SEASONALITY`: Seasonal period (e.g., 7 for daily data with weekly seasonality)
- `OUTPUT_DIR`: Directory for saving results (optional)
- `TEST_SPLIT`: Fraction of data to use for testing (optional, default: 0.2)

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

## Model Workflows

Each model supports three execution workflows:

- **Main Workflow** (default): Train → Save Model → Forecast → Save Results
- **Training Workflow**: Train → Save Model (for later inference)
- **Inference Workflow**: Load Saved Model → Forecast → Save Results

Models are automatically saved after training and can be loaded for later use.

## Benefits of the New System

1. **No Code Generation**: Configuration changes don't require regenerating files
2. **Easy Model Addition**: Add new models by editing the config file
3. **Flexible Execution**: Run single models, groups, or all models
4. **Parallel Processing**: Run multiple models simultaneously
5. **Unified Environments**: Shared environments reduce redundancy
6. **Better Maintenance**: Single implementation of workflows

## Migration from Old System

The old system generated separate directories for each model. If you have existing results from the old system, they should still be compatible as the output structure remains the same.

## One-Step-Ahead Forecasting

All models now use a unified one-step-ahead forecasting implementation for consistent evaluation:
- Models are trained once on 80% of the data
- For the 20% test period, models forecast one step at a time using actual historical values
- No recursive forecasting or retraining during evaluation
- See `UNIFIED_ONE_STEP_AHEAD.md` for implementation details

## Syncing Data with Lambda Labs

To copy data to Lambda Labs:
```bash

NODE_IP="192.222.55.71"
SSH_KEY="jeremy.pem"
FS_FOLDER="central-texas-three-fs"

# NODE_IP="104.171.202.244"
# SSH_KEY="jeremy.pem"
# FS_FOLDER="texas-one-fs"

# NODE_IP="192.222.58.241"
# SSH_KEY="jeremy.pem"
# FS_FOLDER="washington-dc-three-fs"

NODE_IP="209.20.158.246"
SSH_KEY="jeremy.pem"
FS_FOLDER="utah-fs"

ssh -i ~/.ssh/${SSH_KEY} ubuntu@${NODE_IP} "mkdir -p ~/${FS_FOLDER}/ftsfr"
rsync -avzh --progress --delete --exclude='_output/' -e "ssh -i ~/.ssh/${SSH_KEY}" ./ ubuntu@${NODE_IP}:~/${FS_FOLDER}/ftsfr/
```

To Connect via SSH:
```bash
ssh -i ~/.ssh/${SSH_KEY} ubuntu@${NODE_IP}
```

# Description of the Forecasting Approach
