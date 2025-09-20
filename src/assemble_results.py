"""
Assemble results from forecasting CSV files with auto vs non-auto model filtering.

This script:
1. Reads all CSV files from _output/forecasting/error_metrics/{dataset}/{model}.csv
2. Filters auto vs non-auto model duplicates (prefer auto if valid, else non-auto)
3. Normalizes model names to non-auto versions
4. Adds 'auto' boolean column to track which version was used
5. Outputs consolidated results to _output/forecasting/results_all.csv
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path for settings import
sys.path.insert(0, str(Path(__file__).parent))

from settings import config

OUTPUT_DIR = Path(config("OUTPUT_DIR"))
FORECASTING_DIR = OUTPUT_DIR / "forecasting"
ERROR_METRICS_DIR = FORECASTING_DIR / "error_metrics"


def is_valid_result(row):
    """
    Check if a result row has valid MASE and R2oos values.
    Valid = non-zero, non-null, non-infinite
    """
    mase = row['MASE']
    r2oos = row['R2oos']

    # Convert to numeric if they're strings
    try:
        mase = float(mase)
        r2oos = float(r2oos)
    except (ValueError, TypeError):
        return False

    # Check if values are valid (not null, not infinite, not zero)
    if pd.isna(mase) or pd.isna(r2oos):
        return False
    if not np.isfinite(mase) or not np.isfinite(r2oos):
        return False
    if mase == 0 or r2oos == 0:
        return False

    return True


def normalize_model_name(model_name):
    """
    Convert model name to non-auto version.
    auto_deepar -> deepar
    auto_nbeats -> nbeats
    deepar -> deepar (unchanged)
    """
    if model_name.startswith('auto_'):
        return model_name[5:]  # Remove 'auto_' prefix
    return model_name


def load_all_csv_files():
    """
    Load all CSV files from the error_metrics directory structure.
    Returns a DataFrame with all results.
    """
    if not ERROR_METRICS_DIR.exists():
        print(f"Error: Directory not found: {ERROR_METRICS_DIR}")
        sys.exit(1)

    all_results = []

    # Iterate through dataset directories
    for dataset_dir in ERROR_METRICS_DIR.iterdir():
        if not dataset_dir.is_dir():
            continue

        dataset_name = dataset_dir.name

        # Iterate through model CSV files
        for csv_file in dataset_dir.glob("*.csv"):
            model_name = csv_file.stem

            try:
                df = pd.read_csv(csv_file)

                # Should have exactly one row per file
                if len(df) != 1:
                    print(f"Warning: Expected 1 row in {csv_file}, found {len(df)}")
                    if len(df) == 0:
                        continue
                    df = df.head(1)  # Take first row if multiple

                # Add file path info for debugging
                df['_dataset_from_path'] = dataset_name
                df['_model_from_path'] = model_name

                all_results.append(df)

            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
                continue

    if not all_results:
        print("Error: No CSV files found or all files failed to load")
        sys.exit(1)

    # Concatenate all results
    results_df = pd.concat(all_results, ignore_index=True)
    print(f"Loaded {len(results_df)} raw results from {len(all_results)} CSV files")

    return results_df


def filter_auto_vs_nonuto_duplicates(df):
    """
    Filter auto vs non-auto model duplicates for each dataset.
    Prefer auto version if valid, otherwise use non-auto version.
    """
    filtered_results = []

    # Group by dataset
    for dataset_name in df['dataset_name'].unique():
        dataset_df = df[df['dataset_name'] == dataset_name].copy()

        # Group models by their normalized names
        model_groups = {}
        for _, row in dataset_df.iterrows():
            model_name = row['model_name']
            normalized_name = normalize_model_name(model_name)

            if normalized_name not in model_groups:
                model_groups[normalized_name] = []
            model_groups[normalized_name].append(row)

        # For each model group, decide which version to keep
        for normalized_name, rows in model_groups.items():
            if len(rows) == 1:
                # Only one version exists, keep it
                chosen_row = rows[0].copy()
                chosen_row['auto'] = chosen_row['model_name'].startswith('auto_')
            else:
                # Multiple versions exist, apply filtering logic
                auto_rows = [r for r in rows if r['model_name'].startswith('auto_')]
                non_auto_rows = [r for r in rows if not r['model_name'].startswith('auto_')]

                # Try to find valid auto version first
                valid_auto = None
                for row in auto_rows:
                    if is_valid_result(row):
                        valid_auto = row
                        break

                if valid_auto is not None:
                    # Use valid auto version
                    chosen_row = valid_auto.copy()
                    chosen_row['auto'] = True
                    # Only print for datasets where we're choosing between versions
                    if len(rows) > 1:
                        print(f"Dataset {dataset_name}, model {normalized_name}: Using auto version (valid)")
                elif non_auto_rows:
                    # Use non-auto version
                    chosen_row = non_auto_rows[0].copy()
                    chosen_row['auto'] = False
                    print(f"Dataset {dataset_name}, model {normalized_name}: Using non-auto version (auto invalid/missing)")
                elif auto_rows:
                    # Use auto version even if invalid (last resort)
                    chosen_row = auto_rows[0].copy()
                    chosen_row['auto'] = True
                    print(f"Dataset {dataset_name}, model {normalized_name}: Using auto version (only option, but invalid)")
                else:
                    # This shouldn't happen, but handle it
                    chosen_row = rows[0].copy()
                    chosen_row['auto'] = chosen_row['model_name'].startswith('auto_')
                    print(f"Dataset {dataset_name}, model {normalized_name}: Using first available (fallback)")

            # Normalize the model name
            chosen_row['model_name'] = normalized_name

            filtered_results.append(chosen_row)

    return pd.DataFrame(filtered_results)


def main():
    print("Assembling forecasting results with auto vs non-auto filtering...")
    print(f"Reading from: {ERROR_METRICS_DIR}")
    print("=" * 60)

    # Load all CSV files
    raw_df = load_all_csv_files()

    # Show what we loaded
    print(f"\nRaw data summary:")
    print(f"  Total rows: {len(raw_df)}")
    print(f"  Unique datasets: {raw_df['dataset_name'].nunique()}")
    print(f"  Unique models: {raw_df['model_name'].nunique()}")

    # Filter auto vs non-auto duplicates
    print(f"\nFiltering auto vs non-auto duplicates...")
    filtered_df = filter_auto_vs_nonuto_duplicates(raw_df)

    # Show filtering results
    print(f"\nFiltered data summary:")
    print(f"  Total rows: {len(filtered_df)}")
    print(f"  Unique datasets: {filtered_df['dataset_name'].nunique()}")
    print(f"  Unique models: {filtered_df['model_name'].nunique()}")
    print(f"  Auto versions used: {filtered_df['auto'].sum()}")
    print(f"  Non-auto versions used: {(~filtered_df['auto']).sum()}")

    # Clean up columns
    columns_to_keep = ['model_name', 'dataset_name', 'MASE', 'MSE', 'RMSE', 'R2oos', 'time_taken', 'auto']
    final_df = filtered_df[columns_to_keep].copy()

    # Sort for consistent output
    final_df = final_df.sort_values(['dataset_name', 'model_name'])

    # Save results
    output_file = FORECASTING_DIR / "results_all.csv"
    final_df.to_csv(output_file, index=False)
    print(f"\nSaved results to: {output_file}")

    # Show some quality stats
    print(f"\nData quality summary:")
    mase_valid = pd.to_numeric(final_df['MASE'], errors='coerce')
    r2oos_valid = pd.to_numeric(final_df['R2oos'], errors='coerce')

    print(f"  MASE - Valid: {mase_valid.notna().sum()}, Invalid: {mase_valid.isna().sum()}")
    print(f"  R2oos - Valid: {r2oos_valid.notna().sum()}, Invalid: {r2oos_valid.isna().sum()}")

    if mase_valid.notna().any():
        print(f"  MASE range: {mase_valid.min():.4f} to {mase_valid.max():.4f}")
    if r2oos_valid.notna().any():
        print(f"  R2oos range: {r2oos_valid.min():.4f} to {r2oos_valid.max():.4f}")

    print("\n" + "=" * 60)
    print("Assembly complete!")


if __name__ == "__main__":
    main()