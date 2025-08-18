"""
Configuration reader that combines dataset configuration with environment variables.

Priority order:
1. Environment variables (if set) - for overrides
2. Dataset-specific configuration from datasets.toml
3. Default values if dataset not found
"""

import os
import tomli
from pathlib import Path
from cutoff_calc import cutoff_calc

def read_dataset_config(dataset_path, datasets_toml_path="../datasets.toml"):
    """
    Read configuration for a specific dataset from the root datasets.toml.

    Args:
        dataset_path: Path to the dataset file
        datasets_toml_path: Path to the datasets.toml file (relative to models/)

    Returns:
        dict: Configuration parameters for the dataset
    """
    # Extract dataset name from path
    dataset_name = Path(dataset_path).stem

    # Load datasets.toml
    config_path = Path(__file__).parent / datasets_toml_path
    with open(config_path, "rb") as f:
        datasets_config = tomli.load(f)

    # Search for the dataset configuration in the nested structure
    config = None

    # Look through all sections to find our dataset
    for section, content in datasets_config.items():
        if isinstance(content, dict):
            # Check if this section has our dataset as a subsection
            if dataset_name in content:
                config = content[dataset_name].copy()
                break
            # Also check with section prefix (e.g., section.dataset_name)
            full_name = f"{section}.{dataset_name}"
            if full_name in datasets_config:
                config = datasets_config[full_name].copy()
                break

    # If not found, provide defaults
    if config is None:
        print(
            f"Warning: Dataset '{dataset_name}' not found in datasets.toml. Using defaults."
        )
        config = {"frequency": "D", "seasonality": 7, "test_split": 0.2}

    return config, dataset_name


def get_model_config(environment_dict=None):
    """
    Get model configuration combining dataset config and environment variables.

    Environment variables override dataset configuration if set.

    Args:
        environment_dict: Dictionary of environment variables (defaults to os.environ)

    Returns:
        tuple: (test_split, frequency, seasonality, dataset_path, output_dir, dataset_name)
    """
    if environment_dict is None:
        environment_dict = os.environ

    # Get dataset path from environment
    dataset_path = Path(environment_dict["DATASET_PATH"])

    # Read dataset configuration
    dataset_config, dataset_name = read_dataset_config(dataset_path)

    # Apply environment variable overrides
    frequency = environment_dict.get("FREQUENCY", dataset_config.get("frequency", "D"))
    seasonality = int(
        environment_dict.get("SEASONALITY", dataset_config.get("seasonality", 7))
    )

    # Handle test_split (default to 0.2 if not in config)
    test_split_env = environment_dict.get(
        "TEST_SPLIT", dataset_config.get("test_split", 0.2)
    )
    if test_split_env == "seasonal":
        test_split = "seasonal"
    else:
        test_split = float(test_split_env)
        if test_split > 1.0:
            raise ValueError("Test split can't be greater than 1.")

    # Output directory
    if environment_dict.get("OUTPUT_DIR", None) is not None:
        output_dir = Path(environment_dict["OUTPUT_DIR"])
    else:
        output_dir = Path(__file__).resolve().parent.parent / "_output"

    cutoff_date = cutoff_calc(dataset_path,
                              dataset_name,
                              frequency,
                              seasonality,
                              test_split)

    # Print configuration being used
    print(f"\nConfiguration for dataset: {dataset_name}")
    print(f"  Frequency: {frequency}")
    print(f"  Seasonality: {seasonality}")
    print(f"  Test cutoff date: {cutoff_date}")
    if "description" in dataset_config:
        print(f"  Description: {dataset_config['description']}")
    print()

    return (test_split, frequency, seasonality, dataset_path, output_dir, dataset_name)
