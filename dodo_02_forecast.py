"""
dodo_02_forecast.py - Model forecasting and inference tasks

This file contains all tasks related to:
- Running forecasting models on datasets
- Checking for required data files before running
"""
import sys
from pathlib import Path
from doit.action import CmdAction

# Import common utilities
from dodo_common import (
    DATA_DIR, OUTPUT_DIR, PIXI_EXECUTABLE,
    load_config, load_all_module_requirements
)
from dependency_tracker import get_available_datasets, get_format_task_name

# Load configuration
config_toml = load_config()
models = config_toml["models"]
models_activated = [model for model in models if models[model]]

# Load module requirements to determine available datasets
module_requirements_dict = load_all_module_requirements()
module_requirements = {}
for module_name, required_sources in module_requirements_dict.items():
    module_requirements[module_name] = all(
        config_toml["data_sources"].get(source, False) for source in required_sources
    )


def check_required_files():
    """Check if required data files exist before running forecasts"""
    available_datasets = get_available_datasets(module_requirements, DATA_DIR)
    
    missing_files = []
    for dataset_name, dataset_info in available_datasets.items():
        if not dataset_info["path"].exists():
            missing_files.append(str(dataset_info["path"]))
    
    if missing_files:
        print("\nWarning: The following required data files are missing:")
        for f in missing_files:
            print(f"  - {f}")
        print("\nPlease run 'doit -f dodo_01_pull.py' first to generate these files.")
        print("Continuing anyway...\n")


def task_forecast():
    """Generate forecast tasks for each combination of model and dataset."""
    
    # Check for required files at task generation time
    check_required_files()
    
    available_datasets = get_available_datasets(module_requirements, DATA_DIR)

    for model in models_activated:
        for dataset_name, dataset_info in available_datasets.items():
            # Skip if the dataset file doesn't exist
            if not dataset_info["path"].exists():
                continue
                
            yield {
                "name": f"{model}:{dataset_name}",
                "actions": [
                    CmdAction(
                        f"{PIXI_EXECUTABLE} run main",
                        cwd=f"./models/{model}",
                        env={
                            "DATASET_PATH": str(dataset_info["path"]),
                            "FREQUENCY": dataset_info["frequency"],
                            "SEASONALITY": str(dataset_info["seasonality"]),
                            "OUTPUT_DIR": str(OUTPUT_DIR),
                        },
                    )
                ],
                "targets": [
                    OUTPUT_DIR / "raw_results" / f"{model}_{dataset_name}_results.csv"
                ],
                "file_dep": [
                    f"./models/{model}/main.py",
                    f"./models/{model}/pixi.toml",
                ],
                "clean": [],
                "verbosity": 0,
            }