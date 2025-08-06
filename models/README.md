# Models - Configuration-Driven Forecasting System

Configuration-driven system for running various time series forecasting models with unified interface.

## Quick Start

### Step 1: Initial Setup (Lambda Labs)

```bash
# From the project root, run the setup script
./setup_lambdalabs.sh

# This will:
# - Install Miniconda and create 'ftsfr' environment
# - Install all Python dependencies
# - Install Pixi package manager
# - Download VS Code CLI for remote development
# - Optionally start VS Code tunnel

# After setup, navigate to models directory
cd models
```

### Step 2: Test Your Setup

```bash
# Activate the conda environment
conda activate ftsfr

# For GPU models, activate pixi GPU environment
pixi shell -e gpu
# Note: On LambdaLabs nodes:
# - For x86_64 H100/A100 nodes: Use `pixi shell -e gpu` (full CUDA support)
# - For ARM64 GH200 nodes: Use `pixi shell` (CPU-only due to PyTorch Triton limitations)
```

### Step 2.1: Using framework-specific Pixi configs

If you want to isolate GPU dependencies per library, use one of the new Pixi TOML files in this directory:

- **GluonTS**:  
  `pixi shell --manifest-path gluonts -e gpu`
- **Darts**:  
  `pixi shell --manifest-path darts -e gpu`
- **Nixtla (NeuralForecast)**:  
  `pixi shell --manifest-path nixtla -e gpu`
- **TimesFM**:  
  `pixi shell --manifest-path timesfm -e gpu`

### Step 2.2: Test GPU support
Before running any models, verify your GPU environments:

```bash
python test_gpu.py
```

# Verify data exists (datasets are in subfolders)
```bash
ls -la ../_data/*/ftsfr_*.parquet
```

### Step 3: Run Your First Model

```bash
# Set dataset (datasets are in module subfolders)
export DATASET_PATH="../_data/us_treasury_returns/ftsfr_treas_bond_returns.parquet"  # US Treasury
# export DATASET_PATH="../_data/corp_bond_returns/ftsfr_corp_bond_returns.parquet"  # Corporate bonds
# export DATASET_PATH="../_data/cds_returns/ftsfr_CDS_contract_returns.parquet"  # CDS

# Run a simple model (ARIMA), with Darts
python run_model.py --model arima

# Check results
ls -la ../_output/raw_results/arima/
```

## Production Run

### Step 4: Test Model Classes

```bash
# Local models (CPU, fast), implemented in Darts
python run_model.py --model arima
python run_model.py --model auto_arima

# GPU-enabled neural networks, implemented in Darts
python run_model.py --model dlinear
python run_model.py --model nlinear

# GluonTS models
python run_model.py --model deepar
python run_model.py --model simple_feed_forward

# Advanced models (if dependencies installed), implemented in TimesFM
python run_model.py --model timesfm
```

### Step 5: Run Multiple Models

```bash
# List all available models
python model_controller.py --list

# Run a subset of models
python model_controller.py --models arima dlinear deepar

# Run all models (takes time!)
python model_controller.py --all

# Run in parallel (uses more memory)
python model_controller.py --all --parallel --workers 4
```

### Step 6: Cost-Optimized Workflow (Lambda Labs)

```bash
# On GPU instance ($1.49/hr for H100) - train models
conda activate ftsfr
pixi shell -e gpu
export DATASET_PATH="../_data/us_treasury_returns/ftsfr_treas_bond_returns.parquet"
python model_controller.py --models transformer nbeats dlinear --workflow train --parallel

# Switch to CPU instance ($0.20/hr) - run inference
conda activate ftsfr
pixi shell
export DATASET_PATH="../_data/us_treasury_returns/ftsfr_treas_bond_returns.parquet"
python model_controller.py --models transformer nbeats dlinear --workflow inference --parallel
python model_controller.py --models transformer nbeats dlinear --workflow evaluate
```

## Monitor Your Runs

```bash
# Watch GPU usage (in another terminal)
watch -n 1 nvidia-smi

# Check output structure
tree ../_output/

# View results
cat ../_output/raw_results/arima/*.csv
```

## Troubleshooting

### Common Issues

```bash
# Out of memory on GPU
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Missing dependencies
# For the GPU environment, use:
pixi install -e gpu
python -m pip install --upgrade pip

# Prophet not installing on ARM64
pip install prophet --no-binary :all:

# Pixi environment issues on ARM64
# If pixi fails with "No candidates were found for prophet"
# Just use pip to install packages directly:
conda activate ftsfr
pip install -r ../requirements.txt
pip install darts "gluonts[torch]" neuralforecast timesfm catboost tabulate tomli prophet tensorflow
```

### Available Model Classes

- **DartsLocal**: ARIMA, AutoARIMA, ETS, Prophet (train per series)
- **DartsGlobal**: DLinear, NLinear, Transformer, NBEATs (train globally)
- **GluontsMain**: DeepAR, SimpleFeedForward (probabilistic forecasting)
- **NixtlaMain**: Various neural forecasting models
- **Special**: TimesFM (Google), Chronos (Amazon), CatBoost

## Configuration

### Required Environment Variable
```bash
# Datasets are organized in module subfolders
export DATASET_PATH="../_data/us_treasury_returns/ftsfr_treas_bond_returns.parquet"
```