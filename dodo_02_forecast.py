"""
dodo_02_forecast.py - Model forecasting and inference tasks

This file contains all tasks related to:
- Running forecasting models on datasets
- Checking for required data files before running
"""

# Import common utilities
from dodo_common import (
    DATA_DIR,
    OUTPUT_DIR,
    load_subscriptions,
    load_all_module_requirements,
)
from dependency_tracker import get_available_datasets

# Load configuration
subscriptions_toml = load_subscriptions()

# Load module requirements to determine available datasets
module_requirements_dict = load_all_module_requirements()
module_requirements = {}
for module_name, required_sources in module_requirements_dict.items():
    module_requirements[module_name] = all(
        subscriptions_toml["data_sources"].get(source, False)
        for source in required_sources
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


def task_determine_available_datasets():
    """Determine available datasets"""
    return {
        "actions": ["python models/determine_available_datasets.py"],
        "file_dep": [
            "./models/determine_available_datasets.py",
        ],
        "targets": [
            OUTPUT_DIR / "available_datasets.csv",
        ],
    }


def task_determine_cutoff_dates():
    """Determine cutoff dates for each dataset"""
    return {
        "actions": ["python models/cutoff_calc.py"],
        "file_dep": [
            "./models/cutoff_calc.py",
            OUTPUT_DIR / "available_datasets.csv",
        ],
        "targets": [
            OUTPUT_DIR / "cutoff_dates.parquet",
        ],
    }
