#!/usr/bin/env python3
"""
compare_error_metrics.py - Compare files between lambda_results and local error_metrics

This script compares the files in ./lambda_results to those in ./_output/forecasting/error_metrics/
and prints out which files are in one location but not the other.
"""

from pathlib import Path
from typing import Set, Dict


def get_all_files_recursive(directory: Path) -> Set[str]:
    """Get all files recursively from a directory, returning relative paths."""
    if not directory.exists():
        return set()
    
    files = set()
    for file_path in directory.rglob("*"):
        if file_path.is_file():
            # Get relative path from the base directory
            rel_path = file_path.relative_to(directory)
            files.add(str(rel_path))
    return files


def compare_directories():
    """Compare files between lambda_results and local error_metrics."""
    lambda_dir = Path("./lambda_results")
    local_dir = Path("./_output/forecasting/error_metrics")
    
    print("Comparing files between directories:")
    print(f"  Lambda results: {lambda_dir.absolute()}")
    print(f"  Local metrics:  {local_dir.absolute()}")
    print()
    
    # Get all files from both directories
    lambda_files = get_all_files_recursive(lambda_dir)
    local_files = get_all_files_recursive(local_dir)
    
    # Find differences
    only_in_lambda = lambda_files - local_files
    only_in_local = local_files - lambda_files
    in_both = lambda_files & local_files
    
    # Print results
    print(f"Files in both directories: {len(in_both)}")
    print(f"Files only in lambda_results: {len(only_in_lambda)}")
    print(f"Files only in local error_metrics: {len(only_in_local)}")
    print()
    
    if only_in_lambda:
        print("=" * 60)
        print("FILES ONLY IN lambda_results:")
        print("=" * 60)
        for file_path in sorted(only_in_lambda):
            print(f"  {file_path}")
        print()
    
    if only_in_local:
        print("=" * 60)
        print("FILES ONLY IN local error_metrics:")
        print("=" * 60)
        for file_path in sorted(only_in_local):
            print(f"  {file_path}")
        print()
    
    if not only_in_lambda and not only_in_local:
        print("✓ All files are present in both directories!")
    
    # Print summary by model directory
    lambda_models = set()
    local_models = set()
    
    for file_path in lambda_files:
        parts = Path(file_path).parts
        if len(parts) > 0:
            lambda_models.add(parts[0])
    
    for file_path in local_files:
        parts = Path(file_path).parts
        if len(parts) > 0:
            local_models.add(parts[0])
    
    only_lambda_models = lambda_models - local_models
    only_local_models = local_models - lambda_models
    
    if only_lambda_models or only_local_models:
        print("=" * 60)
        print("MODEL DIRECTORY DIFFERENCES:")
        print("=" * 60)
        
        if only_lambda_models:
            print("Model directories only in lambda_results:")
            for model in sorted(only_lambda_models):
                print(f"  {model}")
        
        if only_local_models:
            print("Model directories only in local error_metrics:")
            for model in sorted(only_local_models):
                print(f"  {model}")


if __name__ == "__main__":
    compare_directories()