"""
dodo_0X_forecasting.py - New forecasting system tasks

This file contains all tasks related to:
- Running the refactored forecasting system using forecasting/forecast.py
- Testing all models from forecasting/models_config.toml on all datasets from datasets.toml
- Using the new CLI interface: --dataset DATASET_NAME --model MODEL_NAME
"""

# Import common utilities
from dodo_common import (
    DATA_DIR,
    OUTPUT_DIR,
    debug_action,
    setup_module_requirements,
)
from dependency_tracker import get_available_datasets
import tomli

# Load configuration
module_requirements, subscriptions_toml = setup_module_requirements()


def load_forecasting_models_config():
    """Load the models configuration from forecasting/models_config.toml file."""
    with open("forecasting/models_config.toml", "rb") as f:
        return tomli.load(f)


def task_forecast_new():
    """Run forecasting with the new forecast.py script on all available model-dataset combinations"""
    # Load models configuration
    models_config = load_forecasting_models_config()

    # Get available datasets
    available_datasets = get_available_datasets(module_requirements, DATA_DIR)

    # Generate subtasks for each model-dataset combination
    for model_name in models_config.keys():
        for dataset_name, dataset_info in available_datasets.items():
            if dataset_info["path"].exists():
                # Remove ftsfr_ prefix from dataset name for cleaner output paths
                clean_dataset_name = dataset_name.replace("ftsfr_", "")

                # The get_available_datasets function strips ftsfr_ prefix, but forecast.py expects it
                full_dataset_name = f"ftsfr_{dataset_name}" if not dataset_name.startswith("ftsfr_") else dataset_name
                
                yield {
                    "name": f"{model_name}:{clean_dataset_name}",
                    "actions": [
                        (
                            debug_action,
                            [
                                f"python ./forecasting/forecast.py --dataset {full_dataset_name} --model {model_name}"
                            ],
                        )
                    ],
                    "file_dep": [
                        "forecasting/forecast.py",
                        "forecasting/models_config.toml", 
                        "datasets.toml",
                        str(dataset_info["path"]),
                        OUTPUT_DIR / "available_datasets.csv",
                    ],
                    "targets": [
                        OUTPUT_DIR / "forecasting2" / "error_metrics" / full_dataset_name / f"{model_name}.csv",
                    ],
                    "clean": True,
                    "verbosity": 2,
                }


def task_generate_forecasting_jobs():
    """Generate the forecasting_jobs.txt file used by SLURM submission"""
    return {
        "actions": [
            (debug_action, ["python generate_forecasting_jobs.py"])
        ],
        "file_dep": [
            "generate_forecasting_jobs.py",
            "forecasting/models_config.toml",
            "datasets.toml",
            OUTPUT_DIR / "available_datasets.csv",
        ],
        "targets": [
            "forecasting_jobs.txt"
        ],
        "clean": True,
        "verbosity": 2,
    }