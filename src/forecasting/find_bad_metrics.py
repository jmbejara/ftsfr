#!/usr/bin/env python3
"""
find_bad_metrics.py - Find model x dataset combinations with null or zero error metrics

This script scans the error metrics directory to identify which model x dataset 
combinations have resulted in either zeros or null values for any of the error metrics.
This helps identify runs that completed but produced bad/invalid outputs.

Usage:
    python find_bad_metrics.py

Output:
    Creates bad_outputs.txt in the project root directory with one model:dataset 
    combination per line that has null or zero error metrics.
"""

import pandas as pd
from pathlib import Path
import sys
from typing import List, Tuple

# Import configuration utilities
from dodo_common import OUTPUT_DIR


def check_bad_metrics(error_metrics_file: Path) -> bool:
    """
    Check if a model x dataset combination has bad metrics (null or zero values).
    
    Args:
        error_metrics_file: Path to the error metrics CSV file
        
    Returns:
        bool: True if metrics are bad (contains null or zero values)
    """
    if not error_metrics_file.exists():
        return False
    
    try:
        df = pd.read_csv(error_metrics_file)
        
        # Check if we have data
        if len(df) == 0:
            return True  # Empty file is bad
            
        # Check for MASE column (could be Mean_MASE for local models or Global_MASE for global models)
        mase_column = None
        if 'Mean_MASE' in df.columns:
            mase_column = 'Mean_MASE'
        elif 'Global_MASE' in df.columns:
            mase_column = 'Global_MASE'
        
        if mase_column:
            mase_value = df[mase_column].iloc[0]
            # Consider bad if MASE is NaN, 0, or empty
            if pd.isna(mase_value) or mase_value == 0.0:
                return True
        
        # Also check other error metrics for null/zero values
        metric_columns = []
        for col in df.columns:
            if any(metric in col.upper() for metric in ['MASE', 'MAE', 'RMSE']):
                metric_columns.append(col)
        
        # Check if any metric column has null or zero values
        for col in metric_columns:
            value = df[col].iloc[0]
            if pd.isna(value) or value == 0.0:
                return True
        
        return False
        
    except Exception as e:
        print(f"Error reading {error_metrics_file}: {e}")
        return True  # If we can't read it, consider it bad


def scan_bad_metrics() -> List[str]:
    """
    Scan error metrics directory to find model x dataset combinations with bad metrics.
    
    Returns:
        List of model:dataset combinations with bad metrics
    """
    error_metrics_dir = OUTPUT_DIR / "forecasting" / "error_metrics"
    
    if not error_metrics_dir.exists():
        print(f"Error: {error_metrics_dir} does not exist!")
        return []
    
    bad_combinations = []
    
    # Get all model directories that actually exist
    existing_model_dirs = [d for d in error_metrics_dir.iterdir() if d.is_dir()]
    model_names_with_output = [d.name for d in existing_model_dirs]
    
    print(f"Found {len(existing_model_dirs)} model directories: {model_names_with_output}")
    
    # Check each model directory
    for model_dir in existing_model_dirs:
        model_name = model_dir.name
        
        print(f"  Checking model: {model_name}")
        
        # Get all CSV files in the model directory
        csv_files = list(model_dir.glob("*.csv"))
        processed_datasets = [f.stem for f in csv_files]
        
        print(f"    Found {len(processed_datasets)} processed datasets")
        
        for dataset_name in processed_datasets:
            error_file = model_dir / f"{dataset_name}.csv"
            task_name = f"{model_name}:{dataset_name}"
            
            if check_bad_metrics(error_file):
                bad_combinations.append(task_name)
                print(f"      BAD  {task_name}")
            else:
                print(f"      OK   {task_name}")
    
    return bad_combinations


def main():
    """Main entry point for the script."""
    print("Scanning for model x dataset combinations with bad error metrics...")
    print("=" * 60)
    
    # Scan for bad metrics
    bad_combinations = scan_bad_metrics()
    
    # Write results to bad_outputs.txt
    output_file = Path("bad_outputs.txt")
    
    with open(output_file, 'w') as f:
        for combination in sorted(bad_combinations):
            f.write(f"{combination}\n")
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Found {len(bad_combinations)} model x dataset combinations with bad metrics")
    print(f"Results saved to: {output_file}")
    
    if bad_combinations:
        print("\nBad combinations:")
        for combination in sorted(bad_combinations):
            print(f"  {combination}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())