"""
dependency_tracker.py

Tracks dependencies between data modules and data sources.
Reads dependency information from datasets.toml to determine which
data sources are required for each data module.
"""

import toml
from pathlib import Path


def load_module_requirements(datasets_toml_path="datasets.toml"):
    """
    Load module requirements from datasets.toml.

    Returns a dictionary mapping data module names to their required data sources.
    """
    with open(datasets_toml_path, "r") as f:
        datasets_config = toml.load(f)

    module_requirements = {}

    # Iterate through all sections in datasets.toml
    for module_name, module_config in datasets_config.items():
        if isinstance(module_config, dict) and "required_data_sources" in module_config:
            module_requirements[module_name] = module_config["required_data_sources"]

    return module_requirements


def check_module_availability(module_requirements, data_sources):
    """
    Check which modules can be run based on available data sources.

    Args:
        module_requirements: Dict mapping module names to required data sources
        data_sources: Dict of data source availability (True/False)

    Returns:
        Dict mapping module names to boolean availability
    """
    module_availability = {}

    for module_name, required_sources in module_requirements.items():
        # A module is available if all its required data sources are available
        module_availability[module_name] = all(
            data_sources.get(source, False) for source in required_sources
        )

    return module_availability


def get_missing_sources(module_name, module_requirements, data_sources):
    """
    Get list of missing data sources for a specific module.

    Args:
        module_name: Name of the data module
        module_requirements: Dict mapping module names to required data sources
        data_sources: Dict of data source availability (True/False)

    Returns:
        List of missing data source names
    """
    if module_name not in module_requirements:
        return []

    required = module_requirements[module_name]
    missing = [source for source in required if not data_sources.get(source, False)]

    return missing


def get_available_datasets(
    module_requirements, data_dir, datasets_toml_path="datasets.toml"
):
    """
    Get information about available datasets based on module availability.

    Args:
        module_requirements: Dict mapping module names to boolean availability
        data_dir: Path to the data directory
        datasets_toml_path: Path to datasets.toml file

    Returns:
        Dict mapping dataset names to their information including:
        - path: Path to the parquet file
        - module: Module name that produces this dataset
        - frequency: Dataset frequency (e.g., 'D', 'ME', 'QE')
        - is_balanced: Whether the dataset is balanced
        - description: Dataset description
    """
    with open(datasets_toml_path, "r") as f:
        datasets_config = toml.load(f)

    available_datasets = {}

    # Iterate through available modules
    for module_name, is_available in module_requirements.items():
        if not is_available:
            continue

        # Check if this module has dataset definitions
        if module_name in datasets_config and isinstance(
            datasets_config[module_name], dict
        ):
            module_config = datasets_config[module_name]

            # Look for nested dataset definitions
            for key, value in module_config.items():
                # Dataset definitions start with "ftsfr_" and are dictionaries with a description
                if (
                    key.startswith("ftsfr_")
                    and isinstance(value, dict)
                    and "description" in value
                ):
                    dataset_name = key.replace("ftsfr_", "")

                    available_datasets[dataset_name] = {
                        "path": Path(data_dir) / module_name / f"{key}.parquet",
                        "module": module_name,
                        "frequency": value.get("frequency", "D"),
                        "is_balanced": value.get("is_balanced", False),
                        "description": value.get("description", ""),
                    }

    return available_datasets


def get_format_task_name(module_name):
    """
    Get the correct format task name for a module.
    Some modules have different task names than their module names.

    Args:
        module_name: Name of the data module

    Returns:
        The task name to use for dependencies
    """
    # Special cases where task name differs from module name
    task_name_mapping = {
        "cds_returns": "calc_cds_returns",
    }

    return task_name_mapping.get(module_name, module_name)
