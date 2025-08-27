"""
cutoff_calc.py

This script calculates cutoff dates for all available datasets and saves them
to a common parquet file. The cutoff date is the first date in the test_data
obtained by splitting the dataset using the process_df function.

The script reads the list of available datasets from available_datasets.csv
and processes each one to determine its test cutoff date.
"""

import pandas as pd
import polars as pl
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model_classes.helper_func import process_df


def load_available_datasets(output_dir):
    """Load the list of available datasets from CSV."""
    csv_path = output_dir / "available_datasets.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(
            f"available_datasets.csv not found at {csv_path}. "
            "Please run 'doit determine_available_datasets' first."
        )
    
    return pd.read_csv(csv_path)


def calculate_cutoff_for_dataset(dataset_path, frequency, seasonality, test_split):
    """
    Calculate the cutoff date for a single dataset.
    
    Args:
        dataset_path: Path to the dataset parquet file
        frequency: Data frequency (e.g., 'D', 'M', 'Q')
        seasonality: Seasonal period length
        test_split: Fraction of data to use for testing
        
    Returns:
        The cutoff date (first date in test set)
    """
    # Load the dataset
    df = pd.read_parquet(dataset_path)
    
    # Ensure the dataframe has the expected format
    if 'ds' not in df.columns or 'y' not in df.columns:
        # Try to convert from wide to long format if needed
        if len(df.columns) > 2:  # Likely wide format
            df = df.reset_index()
            if 'date' in df.columns:
                df = df.rename(columns={'date': 'ds'})
            elif 'time' in df.columns:
                df = df.rename(columns={'time': 'ds'})
            else:
                # Assume first column is date
                df = df.rename(columns={df.columns[0]: 'ds'})
            
            # Melt to long format
            df = df.melt(id_vars=['ds'], var_name='unique_id', value_name='y')
        else:
            raise ValueError(f"Dataset {dataset_path} doesn't have expected 'ds' and 'y' columns")
    
    # Add unique_id if not present (required by process_df)
    if 'unique_id' not in df.columns:
        df['unique_id'] = 'series_1'
    
    # Process the dataframe to get train/test split
    _, test_data, _ = process_df(df, frequency, seasonality, test_split)
    
    # Get the cutoff date (first date in test set)
    cutoff_date = test_data['ds'].min()
    
    return cutoff_date


def calculate_all_cutoff_dates(output_dir):
    """
    Calculate cutoff dates for all available datasets.
    
    Args:
        output_dir: Directory containing available_datasets.csv and where to save cutoff_dates.parquet
        
    Returns:
        DataFrame with all cutoff dates
    """
    # Load available datasets
    available_datasets = load_available_datasets(output_dir)
    
    if available_datasets.empty:
        print("Warning: No available datasets found!")
        return pd.DataFrame(columns=["dataset_name", "full_name", "cutoff_date", "frequency", "seasonality"])
    
    print(f"Calculating cutoff dates for {len(available_datasets)} datasets...")
    
    cutoff_results = []
    
    for _, row in available_datasets.iterrows():
        try:
            dataset_path = Path(row['file_path'])
            frequency = row['frequency']
            seasonality = int(row['seasonality'])
            test_split = 0.2  # Default test split
            
            print(f"  Processing {row['full_name']}...")
            
            cutoff_date = calculate_cutoff_for_dataset(
                dataset_path, frequency, seasonality, test_split
            )
            
            cutoff_results.append({
                "dataset_name": row['dataset_name'],
                "full_name": row['full_name'],
                "cutoff_date": cutoff_date,
                "frequency": frequency,
                "seasonality": seasonality,
                "file_path": str(dataset_path)
            })
            
            print(f"    Cutoff date: {cutoff_date}")
            
        except Exception as e:
            print(f"    Error processing {row['full_name']}: {str(e)}")
            continue
    
    # Create DataFrame from results
    cutoff_df = pd.DataFrame(cutoff_results)
    
    if not cutoff_df.empty:
        print(f"\nSuccessfully calculated cutoff dates for {len(cutoff_df)} datasets.")
    else:
        print("\nNo cutoff dates were calculated successfully.")
    
    return cutoff_df


def main():
    """Main function to calculate cutoff dates for all available datasets."""
    # Get output directory
    try:
        from settings import config
        output_dir = Path(config("OUTPUT_DIR"))
    except ImportError:
        output_dir = Path(__file__).parent.parent / "_output"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Calculate cutoff dates for all datasets
    cutoff_df = calculate_all_cutoff_dates(output_dir)
    
    # Save results to parquet file
    output_path = output_dir / "cutoff_dates.parquet"
    cutoff_df.to_parquet(output_path, index=False)
    
    print(f"\nSaved cutoff dates to: {output_path}")
    
    # Display summary
    if not cutoff_df.empty:
        print("\nCutoff dates summary:")
        print(cutoff_df[['full_name', 'cutoff_date', 'frequency', 'seasonality']].to_string(index=False))
    
    return cutoff_df


if __name__ == "__main__":
    main()