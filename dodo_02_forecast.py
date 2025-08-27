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
import tomli
from pathlib import Path

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


def load_models_config(config_path="models/models_config.toml"):
    """Load the models configuration from TOML file."""
    with open(config_path, "rb") as f:
        return tomli.load(f)


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


def task_forecast_darts_local():
    """Run forecasting with DartsLocal models on all available datasets"""
    # Load models configuration
    models_config = load_models_config()
    
    # Filter for DartsLocal models
    darts_local_models = {
        model_name: model_config 
        for model_name, model_config in models_config.items()
        if model_config.get("class") == "DartsLocal"
    }
    
    # Get available datasets
    available_datasets = get_available_datasets(module_requirements, DATA_DIR)
    
    # Generate subtasks for each model-dataset combination
    for model_name in darts_local_models.keys():
        for dataset_name, dataset_info in available_datasets.items():
            if dataset_info["path"].exists():
                # Remove ftsfr_ prefix from dataset name for cleaner output paths
                clean_dataset_name = dataset_name.replace("ftsfr_", "")
                
                yield {
                    "name": f"{model_name}:{clean_dataset_name}",
                    "actions": [
                        f"python models/run_model.py --model {model_name} --dataset-path {dataset_info['path']}"
                    ],
                    "file_dep": [
                        "models/run_model.py",
                        "models/models_config.toml",
                        str(dataset_info["path"]),
                        OUTPUT_DIR / "available_datasets.csv",
                    ],
                    "targets": [
                        OUTPUT_DIR / "forecasting" / "error_metrics" / model_name / f"{clean_dataset_name}.csv",
                        OUTPUT_DIR / "forecasting" / "forecasts" / model_name / clean_dataset_name / "forecasts.parquet",
                    ],
                    "clean": True,
                }


def task_forecast_darts_global():
    """Run forecasting with DartsGlobal models on all available datasets"""
    # Load models configuration
    models_config = load_models_config()
    
    # Filter for DartsGlobal models
    darts_global_models = {
        model_name: model_config 
        for model_name, model_config in models_config.items()
        if model_config.get("class") == "DartsGlobal"
    }
    
    # Get available datasets
    available_datasets = get_available_datasets(module_requirements, DATA_DIR)
    
    # Generate subtasks for each model-dataset combination
    for model_name in darts_global_models.keys():
        for dataset_name, dataset_info in available_datasets.items():
            if dataset_info["path"].exists():
                # Remove ftsfr_ prefix from dataset name for cleaner output paths
                clean_dataset_name = dataset_name.replace("ftsfr_", "")
                
                yield {
                    "name": f"{model_name}:{clean_dataset_name}",
                    "actions": [
                        f"python models/run_model.py --model {model_name} --dataset-path {dataset_info['path']}"
                    ],
                    "file_dep": [
                        "models/run_model.py",
                        "models/models_config.toml",
                        str(dataset_info["path"]),
                        OUTPUT_DIR / "available_datasets.csv",
                    ],
                    "targets": [
                        OUTPUT_DIR / "forecasting" / "error_metrics" / model_name / f"{clean_dataset_name}.csv",
                        OUTPUT_DIR / "forecasting" / "forecasts" / model_name / clean_dataset_name / "forecasts.parquet",
                    ],
                    "clean": True,
                }


def task_forecast_nixtla():
    """Run forecasting with NixtlaMain models on all available datasets"""
    # Load models configuration
    models_config = load_models_config()
    
    # Filter for NixtlaMain models
    nixtla_models = {
        model_name: model_config 
        for model_name, model_config in models_config.items()
        if model_config.get("class") == "NixtlaMain"
    }
    
    # Get available datasets
    available_datasets = get_available_datasets(module_requirements, DATA_DIR)
    
    # Generate subtasks for each model-dataset combination
    for model_name in nixtla_models.keys():
        for dataset_name, dataset_info in available_datasets.items():
            if dataset_info["path"].exists():
                # Remove ftsfr_ prefix from dataset name for cleaner output paths
                clean_dataset_name = dataset_name.replace("ftsfr_", "")
                
                yield {
                    "name": f"{model_name}:{clean_dataset_name}",
                    "actions": [
                        f"python models/run_model.py --model {model_name} --dataset-path {dataset_info['path']}"
                    ],
                    "file_dep": [
                        "models/run_model.py",
                        "models/models_config.toml",
                        str(dataset_info["path"]),
                        OUTPUT_DIR / "available_datasets.csv",
                    ],
                    "targets": [
                        OUTPUT_DIR / "forecasting" / "error_metrics" / model_name / f"{clean_dataset_name}.csv",
                        OUTPUT_DIR / "forecasting" / "forecasts" / model_name / clean_dataset_name / "forecasts.parquet",
                    ],
                    "clean": True,
                }


def task_forecast_gluonts():
    """Run forecasting with GluontsMain models on all available datasets"""
    # Load models configuration
    models_config = load_models_config()
    
    # Filter for GluontsMain models
    gluonts_models = {
        model_name: model_config 
        for model_name, model_config in models_config.items()
        if model_config.get("class") == "GluontsMain"
    }
    
    # Get available datasets
    available_datasets = get_available_datasets(module_requirements, DATA_DIR)
    
    # Generate subtasks for each model-dataset combination
    for model_name in gluonts_models.keys():
        for dataset_name, dataset_info in available_datasets.items():
            if dataset_info["path"].exists():
                # Remove ftsfr_ prefix from dataset name for cleaner output paths
                clean_dataset_name = dataset_name.replace("ftsfr_", "")
                
                yield {
                    "name": f"{model_name}:{clean_dataset_name}",
                    "actions": [
                        f"python models/run_model.py --model {model_name} --dataset-path {dataset_info['path']}"
                    ],
                    "file_dep": [
                        "models/run_model.py",
                        "models/models_config.toml",
                        str(dataset_info["path"]),
                        OUTPUT_DIR / "available_datasets.csv",
                    ],
                    "targets": [
                        OUTPUT_DIR / "forecasting" / "error_metrics" / model_name / f"{clean_dataset_name}.csv",
                        OUTPUT_DIR / "forecasting" / "forecasts" / model_name / clean_dataset_name / "forecasts.parquet",
                    ],
                    "clean": True,
                }


def task_forecast_timesfm():
    """Run forecasting with TimesFM models on all available datasets"""
    # Load models configuration
    models_config = load_models_config()
    
    # Filter for TimesFM models
    timesfm_models = {
        model_name: model_config 
        for model_name, model_config in models_config.items()
        if model_config.get("class") == "TimesFM"
    }
    
    # Get available datasets
    available_datasets = get_available_datasets(module_requirements, DATA_DIR)
    
    # Generate subtasks for each model-dataset combination
    for model_name in timesfm_models.keys():
        for dataset_name, dataset_info in available_datasets.items():
            if dataset_info["path"].exists():
                # Remove ftsfr_ prefix from dataset name for cleaner output paths
                clean_dataset_name = dataset_name.replace("ftsfr_", "")
                
                yield {
                    "name": f"{model_name}:{clean_dataset_name}",
                    "actions": [
                        f"python models/run_model.py --model {model_name} --dataset-path {dataset_info['path']}"
                    ],
                    "file_dep": [
                        "models/run_model.py",
                        "models/models_config.toml",
                        str(dataset_info["path"]),
                        OUTPUT_DIR / "available_datasets.csv",
                    ],
                    "targets": [
                        OUTPUT_DIR / "forecasting" / "error_metrics" / model_name / f"{clean_dataset_name}.csv",
                        OUTPUT_DIR / "forecasting" / "forecasts" / model_name / clean_dataset_name / "forecasts.parquet",
                    ],
                    "clean": True,
                }
