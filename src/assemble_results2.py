"""
Assemble results from the new forecasting system output structure.

This script reads all CSV files from ./_output/forecasting2/error_metrics/{dataset}/{model}.csv
and assembles them into a single consolidated CSV file.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from settings import config

OUTPUT_DIR = Path(config("OUTPUT_DIR"))
FORECAST2_DIR = OUTPUT_DIR / "forecasting2"

def assemble_forecast_results():
    """
    Assemble all forecasting results from the new directory structure.
    
    Directory structure:
    ./_output/forecasting2/error_metrics/{dataset_name}/{model_name}.csv
    
    Each CSV contains columns:
    - Model: Display name of the model
    - Library: statsforecast or neuralforecast
    - Dataset: Dataset name (e.g., ftsfr_treasury_sf_basis)
    - Entities: Number of entities
    - Frequency: Time frequency (D, ME, etc.)
    - Seasonality: Seasonal period
    - Test_Size_h: Test horizon size
    - Global_MASE: Mean Absolute Scaled Error
    - Global_sMAPE: Symmetric Mean Absolute Percentage Error
    - Global_MAE: Mean Absolute Error
    - Global_RMSE: Root Mean Square Error
    - Forecast_Time_seconds: Time taken for forecasting
    """
    
    error_metrics_dir = FORECAST2_DIR / "error_metrics"
    
    if not error_metrics_dir.exists():
        print(f"Error: Error metrics directory not found at {error_metrics_dir}")
        print("Please run forecasting tasks first")
        sys.exit(1)
    
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
                
                # Add to results list
                all_results.append(df)
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
    output_file = FORECAST2_DIR / "results_all.csv"
    results_df.to_csv(output_file, index=False)
    print(f"Saved assembled results to: {output_file}")
    
    # Create LaTeX version
    latex_output = create_latex_summary(results_df)
    latex_file = FORECAST2_DIR / "results_all.tex"
    with open(latex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved LaTeX summary to: {latex_file}")
    
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
    
    # Check for missing values
    print("\n" + "="*60)
    print("DATA QUALITY CHECK")
    print("="*60)
    
    for col in results_df.columns:
        missing_count = results_df[col].isna().sum()
        if missing_count > 0:
            print(f"Column '{col}': {missing_count} missing values ({missing_count/len(results_df)*100:.1f}%)")
    
    # Check for invalid metric values
    metric_columns = ['Global_MASE', 'Global_sMAPE', 'Global_MAE', 'Global_RMSE']
    for col in metric_columns:
        if col in results_df.columns:
            # Check for 'Error' strings
            error_count = (results_df[col] == 'Error').sum()
            if error_count > 0:
                print(f"Warning: {col} has {error_count} 'Error' values")
            
            # Convert to numeric for other checks
            numeric_col = pd.to_numeric(results_df[col], errors='coerce')
            
            # Check for negative values
            negative_count = (numeric_col < 0).sum()
            if negative_count > 0:
                print(f"Warning: {col} has {negative_count} negative values")
            
            # Check for infinite values
            inf_count = np.isinf(numeric_col).sum()
            if inf_count > 0:
                print(f"Warning: {col} has {inf_count} infinite values")
            
            # Check for zero values (might indicate issues)
            zero_count = (numeric_col == 0).sum()
            if zero_count > 0:
                print(f"Warning: {col} has {zero_count} zero values")
    
    # Show top and bottom performers by MASE
    if 'Global_MASE' in results_df.columns:
        # Convert to numeric and filter out errors
        mase_numeric = pd.to_numeric(results_df['Global_MASE'], errors='coerce')
        valid_mase_df = results_df[mase_numeric.notna()].copy()
        valid_mase_df['Global_MASE'] = mase_numeric[mase_numeric.notna()]
        
        if len(valid_mase_df) > 0:
            print("\n" + "="*60)
            print("TOP 5 BEST PERFORMERS (by MASE)")
            print("="*60)
            top_5 = valid_mase_df.nsmallest(5, 'Global_MASE')[['Model', 'Dataset', 'Global_MASE']]
            print(top_5.to_string(index=False))
            
            print("\n" + "="*60)
            print("TOP 5 WORST PERFORMERS (by MASE)")
            print("="*60)
            bottom_5 = valid_mase_df.nlargest(5, 'Global_MASE')[['Model', 'Dataset', 'Global_MASE']]
            print(bottom_5.to_string(index=False))
    
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
            valid_time_df['Forecast_Time_seconds'] = time_numeric[time_numeric.notna()]
            slowest = valid_time_df.nlargest(5, 'Forecast_Time_seconds')[['Model', 'Dataset', 'Forecast_Time_seconds']]
            print(slowest.to_string(index=False))
    
    return results_df

def create_latex_summary(df):
    """Create a LaTeX table summary of the results"""
    
    # Create a summary by model
    if 'Global_MASE' in df.columns:
        # Convert 'Error' strings to NaN for numeric operations
        df_numeric = df.copy()
        metric_cols = ['Global_MASE', 'Global_sMAPE', 'Global_MAE', 'Global_RMSE']
        for col in metric_cols:
            if col in df_numeric.columns:
                df_numeric[col] = pd.to_numeric(df_numeric[col], errors='coerce')
        
        summary = df_numeric.groupby('Model').agg({
            'Global_MASE': ['count', 'mean', 'std', 'min', 'max'],
            'Dataset': 'nunique'
        }).round(3)
        
        # Flatten column names
        summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
        
        latex_str = summary.to_latex(
            caption="Forecasting Results Summary by Model",
            label="tab:results_summary",
            float_format="%.3f"
        )
        
        return f"""% Forecasting Results Summary
% Generated automatically by assemble_results2.py

{latex_str}
"""
    else:
        return "% No MASE results available for LaTeX summary\n"

if __name__ == "__main__":
    print("Assembling forecasting results from new directory structure...")
    print(f"Reading from: {FORECAST2_DIR / 'error_metrics'}/")
    print("="*60)
    
    results = assemble_forecast_results()
    
    print("\n" + "="*60)
    print("Assembly complete!")
    print("="*60)