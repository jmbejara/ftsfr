#!/usr/bin/env python3
"""
restore_dodo_helper.py - Restore doit database by identifying completed tasks

This script scans the output directory to identify which forecasting tasks have
been successfully completed based on non-null MASE values in error metric files.
It then generates the appropriate 'doit ignore' commands to skip these tasks.
"""

import pandas as pd
from pathlib import Path
import sys
import argparse
from typing import Set, Dict, List, Tuple

# Import configuration utilities
from dodo_common import (
    OUTPUT_DIR,
    load_models_config,
)


def check_task_completion(error_metrics_file: Path) -> bool:
    """
    Check if a task is completed based on the error metrics file.

    Args:
        error_metrics_file: Path to the error metrics CSV file

    Returns:
        bool: True if task is completed (has non-null MASE values)
    """
    if not error_metrics_file.exists():
        return False

    try:
        df = pd.read_csv(error_metrics_file)

        # Check if we have data and Mean_MASE is not null/empty
        if len(df) == 0:
            return False

        # Check for MASE column (could be Mean_MASE for local models or Global_MASE for global models)
        mase_column = None
        if "Mean_MASE" in df.columns:
            mase_column = "Mean_MASE"
        elif "Global_MASE" in df.columns:
            mase_column = "Global_MASE"

        if mase_column:
            mase_value = df[mase_column].iloc[0]
            # Consider completed if MASE is not NaN, not 0, and not empty
            return pd.notna(mase_value) and mase_value != 0.0

        return False

    except Exception as e:
        print(f"Error reading {error_metrics_file}: {e}")
        return False


def get_darts_global_models() -> Dict[str, dict]:
    """Get all DartsGlobal models from configuration."""
    models_config = load_models_config()
    return {
        model_name: model_config
        for model_name, model_config in models_config.items()
        if model_config.get("class") == "DartsGlobal"
    }


def get_forecasting_dodo_files() -> List[str]:
    """Get all forecasting dodo files."""
    return [
        "dodo_02_darts_local.py",
        "dodo_03_darts_global.py",
        "dodo_04_nixtla.py",
        "dodo_05_gluonts.py",
        "dodo_06_timesfm.py",
    ]


def get_dodo_task_info(dodo_file: str) -> Tuple[str, str]:
    """
    Determine the task prefix and model class filter from dodo filename.

    Args:
        dodo_file: Path to the dodo file (e.g., 'dodo_02_darts_local.py')

    Returns:
        Tuple of (task_prefix, model_class_filter)
    """
    filename = Path(dodo_file).stem  # Remove .py extension

    # Map dodo files to their task info
    dodo_mappings = {
        "dodo_02_darts_local": ("forecast_darts_local", "DartsLocal"),
        "dodo_03_darts_global": ("forecast_darts_global", "DartsGlobal"),
        "dodo_04_nixtla": ("forecast_nixtla", "Nixtla"),
        "dodo_05_gluonts": ("forecast_gluonts", "GluontsMain"),
        "dodo_06_timesfm": ("forecast_timesfm", "TimesFM"),
    }

    if filename in dodo_mappings:
        return dodo_mappings[filename]

    # Try to infer from filename if not in mappings
    if "darts_local" in filename:
        return ("forecast_darts_local", "DartsLocal")
    elif "darts_global" in filename:
        return ("forecast_darts_global", "DartsGlobal")
    elif "nixtla" in filename:
        return ("forecast_nixtla", "Nixtla")
    elif "gluonts" in filename:
        return ("forecast_gluonts", "GluontsMain")
    elif "timesfm" in filename:
        return ("forecast_timesfm", "TimesFM")

    raise ValueError(f"Cannot determine task info for dodo file: {dodo_file}")


def get_models_by_class(model_class: str) -> Dict[str, dict]:
    """Get all models of a specific class from configuration."""
    models_config = load_models_config()
    return {
        model_name: model_config
        for model_name, model_config in models_config.items()
        if model_config.get("class") == model_class
    }


def scan_completed_tasks(
    model_class_filter: str = None,
) -> Tuple[Set[str], Dict[str, List[str]]]:
    """
    Scan output directory to find completed tasks.

    Args:
        model_class_filter: Optional filter to only include models of specific class

    Returns:
        Tuple of (completed_tasks, completion_status_by_model)
    """
    error_metrics_dir = OUTPUT_DIR / "forecasting" / "error_metrics"

    if not error_metrics_dir.exists():
        print(f"Error: {error_metrics_dir} does not exist!")
        return set(), {}

    completed_tasks = set()
    completion_status = {}

    # Get all model directories that actually exist
    existing_model_dirs = [d for d in error_metrics_dir.iterdir() if d.is_dir()]

    # Filter model directories by class if specified
    if model_class_filter:
        models_config = load_models_config()
        valid_model_names = {
            model_name
            for model_name, model_config in models_config.items()
            if model_config.get("class") == model_class_filter
        }
        existing_model_dirs = [
            d for d in existing_model_dirs if d.name in valid_model_names
        ]

    model_names_with_output = [d.name for d in existing_model_dirs]

    print(
        f"Found {len(existing_model_dirs)} model directories: {model_names_with_output}"
    )
    if model_class_filter:
        print(f"  (filtered for {model_class_filter} models)")

    # Check each model directory
    for model_dir in existing_model_dirs:
        model_name = model_dir.name
        completion_status[model_name] = []

        print(f"  Checking model: {model_name}")

        # Get all CSV files in the model directory to see what datasets were actually processed
        csv_files = list(model_dir.glob("*.csv"))
        processed_datasets = [f.stem for f in csv_files]

        print(f"    Found {len(processed_datasets)} processed datasets")

        for dataset_name in processed_datasets:
            error_file = model_dir / f"{dataset_name}.csv"
            task_name = f"{model_name}:{dataset_name}"

            if check_task_completion(error_file):
                completed_tasks.add(task_name)
                completion_status[model_name].append(f"DONE {dataset_name}")
                print(f"      DONE {task_name}")
            else:
                completion_status[model_name].append(f"FAIL {dataset_name}")
                print(f"      FAIL {task_name}")

    return completed_tasks, completion_status


def generate_ignore_commands(
    completed_tasks: Set[str], dodo_file: str, task_prefix: str
) -> List[str]:
    """Generate doit ignore commands for completed tasks."""
    commands = []

    for task_name in sorted(completed_tasks):
        commands.append(f"doit -f {dodo_file} ignore '{task_prefix}:{task_name}'")

    return commands


def print_summary(completed_tasks: Set[str], completion_status: Dict[str, List[str]]):
    """Print a summary of completed tasks by model."""
    print("\n" + "=" * 60)
    print("COMPLETION SUMMARY")
    print("=" * 60)

    total_possible = 0
    total_completed = 0

    for model_name, statuses in completion_status.items():
        completed = [s for s in statuses if s.startswith("DONE")]
        total = len(statuses)
        total_possible += total
        total_completed += len(completed)

        print(f"\n{model_name}: {len(completed)}/{total} completed")
        for status in statuses:
            print(f"  {status}")

    print(f"\nOVERALL: {total_completed}/{total_possible} tasks completed")
    print(f"Tasks to ignore: {len(completed_tasks)}")


def main():
    parser = argparse.ArgumentParser(
        description="Identify completed dodo tasks and generate ignore commands"
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Specific dodo file to generate ignore commands for (e.g., dodo_02_darts_local.py). If not specified, processes all forecasting dodo files.",
    )
    parser.add_argument(
        "--commands-only",
        action="store_true",
        help="Output only the ignore commands (no summary)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without generating commands",
    )

    args = parser.parse_args()

    # Determine which dodo files to process
    if args.file:
        dodo_files = [args.file]
    else:
        dodo_files = get_forecasting_dodo_files()
        if not args.commands_only:
            print(
                f"Processing {len(dodo_files)} forecasting dodo files: {', '.join(dodo_files)}"
            )

    all_completed_tasks = set()
    all_commands = []

    for dodo_file in dodo_files:
        try:
            task_prefix, model_class_filter = get_dodo_task_info(dodo_file)
        except ValueError as e:
            print(f"Error processing {dodo_file}: {e}")
            continue

        if not args.commands_only and len(dodo_files) > 1:
            print(f"\n{'=' * 60}")
            print(f"PROCESSING: {dodo_file}")
            print(f"{'=' * 60}")

        # Scan for completed tasks
        completed_tasks, completion_status = scan_completed_tasks(model_class_filter)
        all_completed_tasks.update(completed_tasks)

        if not args.commands_only:
            if len(dodo_files) == 1:
                print_summary(completed_tasks, completion_status)
            else:
                # Brief summary for multiple files
                total_completed = len(completed_tasks)
                total_possible = sum(
                    len(statuses) for statuses in completion_status.values()
                )
                print(f"Found {total_completed}/{total_possible} completed tasks")

        if not args.dry_run:
            # Generate ignore commands for this file
            ignore_commands = generate_ignore_commands(
                completed_tasks, dodo_file, task_prefix
            )
            all_commands.extend(ignore_commands)

    if not args.dry_run and all_commands:
        if args.commands_only:
            # Just print the commands
            for cmd in all_commands:
                print(cmd)
        else:
            # Print commands with header
            print("\n" + "=" * 60)
            print("DOIT IGNORE COMMANDS")
            print("=" * 60)
            print("Copy and paste these commands:")
            print()
            for cmd in all_commands:
                print(cmd)

            # Save to file as well
            output_file = Path("_output") / "restore_dodo_commands.sh"
            output_file.parent.mkdir(exist_ok=True)
            with open(output_file, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("# Generated doit ignore commands\n")
                f.write("# Run with: bash restore_dodo_commands.sh\n\n")
                for cmd in all_commands:
                    f.write(f"{cmd}\n")

            print(f"\nCommands also saved to: {output_file}")

    return 0 if all_completed_tasks else 1


if __name__ == "__main__":
    sys.exit(main())
