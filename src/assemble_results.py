import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
import toml

from settings import config
from dependency_tracker import (
    load_module_requirements,
    check_module_availability,
    get_available_datasets,
)

BASE_DIR = config("BASE_DIR")
DATA_DIR = config("DATA_DIR")
OUTPUT_DIR = config("OUTPUT_DIR")

print("Assembling forecasting results...")

# Read subscriptions.toml for data sources
with open(BASE_DIR / "subscriptions.toml", "r") as f:
    subscriptions = toml.load(f)

data_sources = subscriptions["data_sources"]

# Read models configuration to get available models
with open(BASE_DIR / "models" / "models_config.toml", "r") as f:
    models_config = toml.load(f)

# Get all available model names from models_config.toml
models_activated = list(models_config.keys())

# Get available datasets
module_requirements_dict = load_module_requirements()
module_requirements = check_module_availability(module_requirements_dict, data_sources)
available_datasets = get_available_datasets(module_requirements, DATA_DIR)

print(f"Looking for results from {len(models_activated)} activated models across {len(available_datasets)} datasets")

# Find all result files in the new forecasting structure
results_files = []
missing_results = []
error_metrics_dir = OUTPUT_DIR / "forecasting" / "error_metrics"

if not error_metrics_dir.exists():
    print(f"Error: Forecasting error metrics directory not found at {error_metrics_dir}")
    print("Please run the forecasting tasks first (e.g., doit -f dodo_02_darts_local.py)")
    sys.exit(1)

for model in models_activated:
    model_dir = error_metrics_dir / model
    if not model_dir.exists():
        print(f"Warning: No results directory found for model '{model}' at {model_dir}")
        continue
        
    for dataset_name in available_datasets:
        # Remove ftsfr_ prefix if present to match the clean dataset names used in forecasting
        clean_dataset_name = dataset_name.replace("ftsfr_", "")
        result_file = model_dir / f"{clean_dataset_name}.csv"
        
        if result_file.exists():
            results_files.append(result_file)
        else:
            missing_results.append((model, clean_dataset_name))

print(f"Found {len(results_files)} result files")

if missing_results:
    print(f"Warning: {len(missing_results)} expected result files are missing:")
    for model, dataset in missing_results[:10]:  # Show first 10 missing files
        print(f"  - {model}: {dataset}")
    if len(missing_results) > 10:
        print(f"  ... and {len(missing_results) - 10} more")

if not results_files:
    print("No result files found!")
    print("Available model directories:")
    for item in error_metrics_dir.iterdir():
        if item.is_dir():
            print(f"  - {item.name}")
    sys.exit(1)

# Read all results files and concatenate them
results_list = []
successful_files = 0
failed_files = 0

for file in results_files:
    try:
        df = pd.read_csv(file)
        
        # The file structure is: error_metrics/{model_name}/{dataset_name}.csv
        # Extract model and dataset from file path
        model_name = file.parent.name
        dataset_name = file.stem
        
        # Verify this file actually contains MASE data - check for either format
        if 'Mean_MASE' not in df.columns and 'Global_MASE' not in df.columns:
            print(f"Warning: File {file} doesn't contain expected MASE columns (Mean_MASE or Global_MASE), skipping")
            failed_files += 1
            continue
            
        # Create standardized g_mase and g_rmse columns
        # g_mase: Global_MASE if available, otherwise Mean_MASE
        if 'Global_MASE' in df.columns:
            df['g_mase'] = df['Global_MASE']
        elif 'Mean_MASE' in df.columns:
            df['g_mase'] = df['Mean_MASE']
        else:
            print(f"Warning: File {file} has no MASE column, skipping")
            failed_files += 1
            continue
        
        # g_rmse: Global_RMSE if available, otherwise Mean_RMSE
        if 'Global_RMSE' in df.columns:
            df['g_rmse'] = df['Global_RMSE']
        elif 'Mean_RMSE' in df.columns:
            df['g_rmse'] = df['Mean_RMSE']
        else:
            print(f"Warning: File {file} has no RMSE column, setting g_rmse to NaN")
            df['g_rmse'] = np.nan
            
        # Add model and dataset columns if not already present
        if 'model' not in df.columns:
            df['model'] = model_name
        if 'dataset' not in df.columns:
            df['dataset'] = dataset_name
            
        results_list.append(df)
        successful_files += 1
        
    except Exception as e:
        print(f"Warning: Could not read {file}: {e}")
        failed_files += 1

print(f"Successfully processed {successful_files} files, failed to process {failed_files} files")

if not results_list:
    print("No valid result files could be processed!")
    sys.exit(1)

results = pd.concat(results_list, ignore_index=True)
print(f"Assembled results: {len(results)} rows from {results['model'].nunique()} models and {results['dataset'].nunique()} datasets")

# Save results
results.to_csv(OUTPUT_DIR / "results_all.csv", index=False)
print(f"Saved assembled results to: {OUTPUT_DIR / 'results_all.csv'}")

# Create LaTeX version
latex_string = results.to_latex(index=False, escape=True)
with open(OUTPUT_DIR / "results_all.tex", "w") as f:
    f.write(latex_string)
print(f"Saved LaTeX version to: {OUTPUT_DIR / 'results_all.tex'}")

print("Results assembly completed successfully!")
