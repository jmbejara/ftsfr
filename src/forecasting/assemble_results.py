"""
Assemble results from the new forecasting3 system output structure.

This script reads all CSV files from ./_output/forecasting3/error_metrics/{dataset}/{model}.csv
and assembles them into a single consolidated CSV file.

New format from forecast_stats.py and forecast_neural.py:
- model_name: The model key (e.g., 'auto_arima', 'auto_deepar')
- dataset_name: The dataset name
- MASE: Mean Absolute Scaled Error
- MSE: Mean Square Error
- RMSE: Root Mean Square Error
- R2oos: Out-of-sample R-squared
- time_taken: Time taken for forecasting
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
import tomli
from settings import config
from dodo_common import load_models_config

OUTPUT_DIR = Path(config("OUTPUT_DIR"))
FORECAST3_DIR = OUTPUT_DIR / "forecasting3"

def load_display_names():
    """Load model display names and dataset short names for enrichment."""

    # Load model display names from models_config.toml
    models_config = load_models_config()
    model_display_names = {}
    for model_key, model_config in models_config.items():
        if isinstance(model_config, dict):
            display_name = model_config.get('display_name', model_key)
            model_display_names[model_key] = display_name

    # Load dataset short names from datasets.toml
    datasets_toml_path = Path(__file__).parent.parent / "datasets.toml"
    dataset_short_names = {}

    if datasets_toml_path.exists():
        with open(datasets_toml_path, 'rb') as f:
            datasets_config = tomli.load(f)

        for module_name, module_config in datasets_config.items():
            if isinstance(module_config, dict):
                for key, value in module_config.items():
                    if isinstance(value, dict) and key.startswith('ftsfr_'):
                        dataset_name = key
                        short_name = value.get('short_name', dataset_name)
                        dataset_short_names[dataset_name] = short_name

    print(f"Loaded {len(model_display_names)} model display names")
    print(f"Loaded {len(dataset_short_names)} dataset short names")

    return model_display_names, dataset_short_names

def assemble_forecast_results():
    """
    Assemble all forecasting results from the new directory structure.

    Directory structure:
    ./_output/forecasting3/error_metrics/{dataset_name}/{model_name}.csv

    Each CSV contains columns:
    - model_name: Model key (e.g., 'auto_arima', 'auto_deepar')
    - dataset_name: Dataset name (e.g., 'ftsfr_treasury_sf_basis')
    - MASE: Mean Absolute Scaled Error
    - MSE: Mean Square Error
    - RMSE: Root Mean Square Error
    - R2oos: Out-of-sample R-squared
    - time_taken: Time taken for forecasting
    """

    error_metrics_dir = FORECAST3_DIR / "error_metrics"

    if not error_metrics_dir.exists():
        print(f"Error: Error metrics directory not found at {error_metrics_dir}")
        print("Please run forecasting tasks first using forecast_stats.py and forecast_neural.py")
        sys.exit(1)

    # Load mapping data for enrichment
    model_display_names, dataset_short_names = load_display_names()

    all_results = []
    processed_count = 0
    error_count = 0

    # Iterate through dataset directories
    for dataset_dir in sorted(error_metrics_dir.iterdir()):
        if not dataset_dir.is_dir():
            continue

        dataset_name = dataset_dir.name

        # Iterate through model CSV files in each dataset directory
        for csv_file in sorted(dataset_dir.glob("*.csv")):
            model_name = csv_file.stem

            try:
                # Read the CSV file
                df = pd.read_csv(csv_file)

                # Ensure we have a single row (one result per model-dataset pair)
                if len(df) != 1:
                    print(f"Warning: Expected 1 row in {csv_file}, found {len(df)}")
                    if len(df) == 0:
                        error_count += 1
                        continue
                    # Take the first row if multiple exist
                    df = df.head(1)

                # Enrich with display names and normalize column names
                df_enriched = df.copy()

                # Add display name for model
                model_key = df_enriched['model_name'].iloc[0]
                display_name = model_display_names.get(model_key, model_key)
                df_enriched['Model'] = display_name

                # Keep dataset name as-is for Dataset column
                df_enriched['Dataset'] = df_enriched['dataset_name'].iloc[0]

                # Add dataset short name
                dataset_short = dataset_short_names.get(dataset_name, dataset_name)
                df_enriched['Dataset_Short'] = dataset_short

                # Rename time column for consistency
                if 'time_taken' in df_enriched.columns:
                    df_enriched['Forecast_Time_seconds'] = df_enriched['time_taken']

                # Add to results list
                all_results.append(df_enriched)
                processed_count += 1

                if processed_count % 50 == 0:
                    print(f"Processed {processed_count} result files...")

            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
                error_count += 1
                continue

    if not all_results:
        print("Error: No valid result files found")
        sys.exit(1)

    # Concatenate all results
    print(f"\nConcatenating {len(all_results)} result DataFrames...")
    results_df = pd.concat(all_results, ignore_index=True)

    # Sort by Model and Dataset for consistent output
    results_df = results_df.sort_values(['Model', 'Dataset'])

    # Save assembled results
    output_file = FORECAST3_DIR / "results_all.csv"
    results_df.to_csv(output_file, index=False)
    print(f"Saved assembled results to: {output_file}")

    # Print summary statistics
    print("\n" + "="*60)
    print("ASSEMBLY SUMMARY")
    print("="*60)
    print(f"Total files processed: {processed_count}")
    print(f"Total errors: {error_count}")
    print(f"Total results assembled: {len(results_df)}")
    print(f"\nUnique models: {results_df['Model'].nunique()}")
    print(f"Unique datasets: {results_df['Dataset'].nunique()}")
    print(f"Unique model-dataset combinations: {len(results_df)}")

    # Print column information
    print(f"\nColumns in assembled data:")
    for col in sorted(results_df.columns):
        print(f"  - {col}")

    # Check for missing values
    print("\n" + "="*60)
    print("DATA QUALITY CHECK")
    print("="*60)

    for col in results_df.columns:
        missing_count = results_df[col].isna().sum()
        if missing_count > 0:
            print(f"Column '{col}': {missing_count} missing values ({missing_count/len(results_df)*100:.1f}%)")

    # Check for invalid metric values
    metric_columns = ['MASE', 'MSE', 'RMSE', 'R2oos']
    for col in metric_columns:
        if col in results_df.columns:
            # Check for 'Error' strings
            error_count = (results_df[col] == 'Error').sum()
            if error_count > 0:
                print(f"Warning: {col} has {error_count} 'Error' values")

            # Convert to numeric for other checks
            numeric_col = pd.to_numeric(results_df[col], errors='coerce')

            # Check for negative values (R2oos can be negative, others shouldn't be)
            if col != 'R2oos':
                negative_count = (numeric_col < 0).sum()
                if negative_count > 0:
                    print(f"Warning: {col} has {negative_count} negative values")

            # Check for infinite values
            inf_count = np.isinf(numeric_col).sum()
            if inf_count > 0:
                print(f"Warning: {col} has {inf_count} infinite values")

            # Check for zero values (might indicate issues for most metrics)
            zero_count = (numeric_col == 0).sum()
            if zero_count > 0:
                print(f"Warning: {col} has {zero_count} zero values")

    # Show top and bottom performers by MASE
    if 'MASE' in results_df.columns:
        # Convert to numeric and filter out errors
        mase_numeric = pd.to_numeric(results_df['MASE'], errors='coerce')
        valid_mase_df = results_df[mase_numeric.notna()].copy()
        valid_mase_df['MASE_numeric'] = mase_numeric[mase_numeric.notna()]

        if len(valid_mase_df) > 0:
            print("\n" + "="*60)
            print("TOP 5 BEST PERFORMERS (by MASE)")
            print("="*60)
            top_5 = valid_mase_df.nsmallest(5, 'MASE_numeric')[['Model', 'Dataset', 'MASE']]
            print(top_5.to_string(index=False))

            print("\n" + "="*60)
            print("TOP 5 WORST PERFORMERS (by MASE)")
            print("="*60)
            bottom_5 = valid_mase_df.nlargest(5, 'MASE_numeric')[['Model', 'Dataset', 'MASE']]
            print(bottom_5.to_string(index=False))

    # Show top performers by R2oos (higher is better)
    if 'R2oos' in results_df.columns:
        r2_numeric = pd.to_numeric(results_df['R2oos'], errors='coerce')
        valid_r2_df = results_df[r2_numeric.notna()].copy()
        valid_r2_df['R2oos_numeric'] = r2_numeric[r2_numeric.notna()]

        if len(valid_r2_df) > 0:
            print("\n" + "="*60)
            print("TOP 5 BEST PERFORMERS (by R2oos)")
            print("="*60)
            top_5_r2 = valid_r2_df.nlargest(5, 'R2oos_numeric')[['Model', 'Dataset', 'R2oos']]
            print(top_5_r2.to_string(index=False))

            print("\n" + "="*60)
            print("TOP 5 WORST PERFORMERS (by R2oos)")
            print("="*60)
            bottom_5_r2 = valid_r2_df.nsmallest(5, 'R2oos_numeric')[['Model', 'Dataset', 'R2oos']]
            print(bottom_5_r2.to_string(index=False))

    # Show timing statistics
    if 'Forecast_Time_seconds' in results_df.columns:
        # Convert to numeric to handle any potential errors
        time_numeric = pd.to_numeric(results_df['Forecast_Time_seconds'], errors='coerce')
        valid_times = time_numeric[time_numeric.notna()]

        if len(valid_times) > 0:
            print("\n" + "="*60)
            print("TIMING STATISTICS")
            print("="*60)
            print(f"Total computation time: {valid_times.sum():.2f} seconds")
            print(f"Average time per model-dataset: {valid_times.mean():.2f} seconds")
            print(f"Median time: {valid_times.median():.2f} seconds")
            print(f"Min time: {valid_times.min():.2f} seconds")
            print(f"Max time: {valid_times.max():.2f} seconds")

            # Top 5 slowest
            print("\nTop 5 slowest computations:")
            valid_time_df = results_df[time_numeric.notna()].copy()
            valid_time_df['Forecast_Time_numeric'] = time_numeric[time_numeric.notna()]
            slowest = valid_time_df.nlargest(5, 'Forecast_Time_numeric')[['Model', 'Dataset', 'Forecast_Time_seconds']]
            print(slowest.to_string(index=False))

    return results_df

if __name__ == "__main__":
    print("Assembling forecasting results from new forecasting3 directory structure...")
    print(f"Reading from: {FORECAST3_DIR / 'error_metrics'}/")
    print("="*60)

    results = assemble_forecast_results()

    print("\n" + "="*60)
    print("Assembly complete!")
    print("="*60)