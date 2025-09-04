"""
dodo_04_nixtla.py - Nixtla model forecasting and inference tasks

This file contains all tasks related to:
- Running Nixtla forecasting models (NeuralForecast and StatsForecast) on datasets
- Checking for required data files before running
"""

# Import common utilities
from dodo_common import (
    DATA_DIR,
    OUTPUT_DIR,
    debug_action,
    load_models_config,
    setup_module_requirements,
)
from dependency_tracker import get_available_datasets

# Load configuration
module_requirements, subscriptions_toml = setup_module_requirements()


def task_forecast_nixtla():
    """Run forecasting with NixtlaMain and StatsForecastMain models on all available datasets"""
    # Load models configuration
    models_config = load_models_config()

    # Filter for NixtlaMain and StatsForecastMain models
    nixtla_models = {
        model_name: model_config
        for model_name, model_config in models_config.items()
        if model_config.get("class") in ["NixtlaMain", "StatsForecastMain"]
    }

    # Get available datasets
    available_datasets = get_available_datasets(module_requirements, DATA_DIR)

    # Generate subtasks for each model-dataset combination
    for model_name in nixtla_models.keys():
        for dataset_name, dataset_info in available_datasets.items():
            if dataset_info["path"].exists():
                # Remove ftsfr_ prefix from dataset name for cleaner output paths
                clean_dataset_name = dataset_name.replace("ftsfr_", "")
                
                # # Print the command immediately for debugging
                # cmd = f"python models/run_model.py --model {model_name} --dataset-path {dataset_info['path']}"
                # print(f"\n🔍 DEBUG: Task {model_name}:{clean_dataset_name}")
                # print(f"Command: {cmd}")
                # print("=" * 60)

                yield {
                    "name": f"{model_name}:{clean_dataset_name}",
                    "actions": [
                        (
                            debug_action,
                            f"python models/run_model.py --model {model_name} --dataset-path {dataset_info['path']}"
                        )
                    ],
                    "file_dep": [
                        "models/run_model.py",
                        "models/models_config.toml",
                        str(dataset_info["path"]),
                        OUTPUT_DIR / "available_datasets.csv",
                    ],
                    "targets": [
                        OUTPUT_DIR
                        / "forecasting"
                        / "error_metrics"
                        / model_name
                        / f"{clean_dataset_name}.csv",
                        OUTPUT_DIR
                        / "forecasting"
                        / "forecasts"
                        / model_name
                        / clean_dataset_name
                        / "forecasts.parquet",
                        OUTPUT_DIR
                        / "forecasting"
                        / "timing"
                        / model_name
                        / f"{clean_dataset_name}_timing.csv",
                    ],
                    "clean": True,
                }
