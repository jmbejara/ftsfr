#!/usr/bin/env python3
"""
Generate forecasting_jobs.txt automatically from datasets.toml and models_config.toml

This script reads the configuration files to determine which datasets and models
are active, then generates all combinations for the SLURM array job script.

Usage:
    python generate_forecasting_jobs.py

Output:
    Creates/overwrites forecasting_jobs.txt with all dataset x model combinations
"""

import toml
import sys
from pathlib import Path
from typing import List, Dict, Any


def load_toml_file(filepath: Path) -> Dict[str, Any]:
    """Load and parse a TOML file."""
    try:
        with open(filepath, 'r') as f:
            return toml.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found")
        sys.exit(1)
    except toml.TomlDecodeError as e:
        print(f"Error parsing {filepath}: {e}")
        sys.exit(1)


def extract_datasets(datasets_config: Dict[str, Any]) -> List[str]:
    """Extract active dataset names from datasets.toml."""
    datasets = []
    
    for module_name, module_config in datasets_config.items():
        if isinstance(module_config, dict):
            for key, value in module_config.items():
                # Skip module-level metadata (strings)
                if isinstance(value, dict) and key.startswith('ftsfr_'):
                    datasets.append(key)
    
    return sorted(datasets)


def extract_models(models_config: Dict[str, Any]) -> List[Dict[str, str]]:
    """Extract active models with their script information from models_config.toml."""
    models = []

    for model_name, model_config in models_config.items():
        # Only include top-level keys that have configuration dictionaries with script field
        if isinstance(model_config, dict) and 'script' in model_config:
            models.append({
                'name': model_name,
                'script': model_config['script'],
                'display_name': model_config.get('display_name', model_name)
            })

    return sorted(models, key=lambda x: x['name'])


def generate_job_commands(datasets: List[str], models: List[Dict[str, str]]) -> List[str]:
    """Generate job commands for all dataset x model combinations."""
    commands = []

    for dataset in datasets:
        for model in models:
            model_name = model['name']
            script_name = model['script']
            command = f"python ./src/forecasting/{script_name} --dataset {dataset} --model {model_name}"
            commands.append(command)

    return commands


def write_jobs_file(commands: List[str], output_file: Path) -> None:
    """Write job commands to forecasting_jobs.txt."""
    try:
        with open(output_file, 'w') as f:
            for command in commands:
                f.write(command + '\n')
        print(f"Successfully wrote {len(commands)} jobs to {output_file}")
    except IOError as e:
        print(f"Error writing to {output_file}: {e}")
        sys.exit(1)


def main():
    """Main function to generate forecasting jobs."""
    # Define file paths
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent  # src/forecasting -> src -> repo root

    datasets_file = repo_root / "datasets.toml"
    models_file = script_dir / "models_config.toml"
    output_file = script_dir / "forecasting_jobs.txt"
    
    print("Generating forecasting_jobs.txt...")
    print(f"Reading datasets from: {datasets_file}")
    print(f"Reading models from: {models_file}")
    
    # Load configuration files
    datasets_config = load_toml_file(datasets_file)
    models_config = load_toml_file(models_file)
    
    # Extract active datasets and models
    datasets = extract_datasets(datasets_config)
    models = extract_models(models_config)
    
    print(f"\nFound {len(datasets)} datasets:")
    for dataset in datasets:
        print(f"  - {dataset}")
    
    print(f"\nFound {len(models)} models:")
    for model in models:
        print(f"  - {model['name']} → {model['script']} ({model['display_name']})")

    # Generate job commands
    commands = generate_job_commands(datasets, models)
    total_jobs = len(commands)

    print(f"\nGenerating {total_jobs} jobs ({len(datasets)} datasets × {len(models)} models)")
    
    # Write to file
    write_jobs_file(commands, output_file)
    
    # Update SLURM script if needed
    slurm_file = script_dir / "submit_forecasting_jobs.sh"
    if slurm_file.exists():
        print(f"\nReminder: Update the array size in {slurm_file} to 1-{total_jobs}")
    
    print("\nDone!")


if __name__ == "__main__":
    main()
