"""
determine_available_datasets.py

This script determines which datasets from datasets.toml are actually available
as parquet files in the data directory. It creates a CSV file listing all
available datasets with their paths and metadata.
"""

import tomli
import pandas as pd
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def load_datasets_config():
    """Load the datasets configuration from TOML file."""
    config_path = Path(__file__).parent.parent / "datasets.toml"
    with open(config_path, "rb") as f:
        return tomli.load(f)


def find_available_datasets(data_dir, datasets_config):
    """
    Find which datasets from the config are actually available as parquet files.
    
    Args:
        data_dir: Path to the data directory
        datasets_config: Loaded datasets configuration
        
    Returns:
        List of dictionaries with dataset information
    """
    available_datasets = []
    
    # Search through all sections in the config
    for section, content in datasets_config.items():
        if isinstance(content, dict):
            # Check if this section has dataset subsections
            for dataset_name, dataset_config in content.items():
                if isinstance(dataset_config, dict) and "frequency" in dataset_config:
                    # This is a dataset configuration
                    # The dataset_name already includes the ftsfr_ prefix, so just add .parquet
                    dataset_file = f"{dataset_name}.parquet"
                    # Look in the section subdirectory first, then in the root data directory
                    dataset_path = data_dir / section / dataset_file
                    
                    if dataset_path.exists():
                        available_datasets.append({
                            "full_name": f"{section}.{dataset_name}",
                            "file_path": str(dataset_path),
                            "frequency": dataset_config.get("frequency", "D"),
                            "seasonality": dataset_config.get("seasonality", 7)
                        })
                    else:
                        # Try looking in the root data directory as fallback
                        dataset_path = data_dir / dataset_file
                        if dataset_path.exists():
                            available_datasets.append({
                                "full_name": f"{section}.{dataset_name}",
                                "file_path": str(dataset_path),
                                "frequency": dataset_config.get("frequency", "D"),
                                "seasonality": dataset_config.get("seasonality", 7)
                            })
    
    return available_datasets


def find_available_datasets_with_requirements(data_dir, datasets_config, data_sources):
    """
    Find which datasets from the config are available based on data source requirements
    and actual parquet file existence.
    
    Args:
        data_dir: Path to the data directory
        datasets_config: Loaded datasets configuration
        data_sources: Dictionary of data source availability (True/False)
        
    Returns:
        List of dictionaries with dataset information
    """
    available_datasets = []
    
    # Search through all sections in the config
    for section, content in datasets_config.items():
        if isinstance(content, dict):
            # Check if this module's required data sources are available
            module_required_sources = content.get("required_data_sources", [])
            if module_required_sources:
                # Check if all required data sources are available
                if not all(data_sources.get(source, False) for source in module_required_sources):
                    continue  # Skip this module if required sources aren't available
            
            # Check if this section has dataset subsections
            for dataset_name, dataset_config in content.items():
                if isinstance(dataset_config, dict) and "frequency" in dataset_config:
                    # This is a dataset configuration
                    # The dataset_name already includes the ftsfr_ prefix, so just add .parquet
                    dataset_file = f"{dataset_name}.parquet"
                    # Look in the section subdirectory first, then in the root data directory
                    dataset_path = data_dir / section / dataset_file
                    
                    if dataset_path.exists():
                        available_datasets.append({
                            "full_name": f"{section}.{dataset_name}",
                            "file_path": str(dataset_path),
                            "frequency": dataset_config.get("frequency", "D"),
                            "seasonality": dataset_config.get("seasonality", 7)
                        })
                    else:
                        # Try looking in the root data directory as fallback
                        dataset_path = data_dir / dataset_file
                        if dataset_path.exists():
                            available_datasets.append({
                                "section": section,
                                "dataset_name": dataset_name,
                                "full_name": f"{section}.{dataset_name}",
                                "file_path": str(dataset_path),
                                "frequency": dataset_config.get("frequency", "D"),
                                "seasonality": dataset_config.get("seasonality", 7),
                                "description": dataset_config.get("description", ""),
                                "required_data_sources": content.get("required_data_sources", [])
                            })
    
    return available_datasets


def main():
    """Main function to determine available datasets and save to CSV."""
    # Get the data directory from environment or use default
    try:
        # Try to get from environment first
        from settings import config
        data_dir = Path(config("DATA_DIR"))
    except ImportError:
        # Fallback to relative path
        data_dir = Path(__file__).parent.parent / "_data"
    
    # Load datasets configuration
    datasets_config = load_datasets_config()
    
    # Load subscriptions to check data source availability
    try:
        from dodo_common import load_subscriptions
        subscriptions_toml = load_subscriptions()
        data_sources = subscriptions_toml["data_sources"]
    except ImportError:
        # Fallback: assume all data sources are available
        data_sources = {
            "fed_yield_curve": True,
            "bloomberg_terminal": True,
            "wrds_markit": True,
            "open_source_bond": True,
            "he_kelly_manela": True,
            "ken_french_data_library": True,
            "nyu_call_report": True,
            "wrds_crsp": True,
            "wrds_compustat": True,
            "wrds_crsp_compustat": True,
            "wrds_datastream": True,
            "wrds_optionmetrics": True,
        }
    
    # Find available datasets based on data source availability
    available_datasets = find_available_datasets_with_requirements(data_dir, datasets_config, data_sources)
    
    if not available_datasets:
        print("Warning: No available datasets found!")
        print(f"Checked in: {data_dir}")
        print("Make sure to run data pull tasks first.")
        # Create empty DataFrame to avoid errors
        df = pd.DataFrame(columns=[
            "full_name", "file_path", "frequency", "seasonality"
        ])
    else:
        # Convert to DataFrame
        df = pd.DataFrame(available_datasets)
        print(f"Found {len(available_datasets)} available datasets:")
        for _, row in df.iterrows():
            print(f"  - {row['full_name']} ({row['frequency']}, seasonality={row['seasonality']})")
    
    # Save to CSV in OUTPUT_DIR
    try:
        from settings import config
        output_dir = Path(config("OUTPUT_DIR"))
    except ImportError:
        output_dir = Path(__file__).parent.parent / "_output"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "available_datasets.csv"
    
    df.to_csv(output_path, index=False)
    print(f"\nSaved available datasets to: {output_path}")
    
    return df


if __name__ == "__main__":
    main()
