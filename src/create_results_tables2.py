import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
import tomli

from settings import config

OUTPUT_DIR = Path(config("OUTPUT_DIR"))
FORECAST2_DIR = OUTPUT_DIR / "forecast2"  # New forecasting output directory

def filter_quality_results(results_df):
    """Filter out results with quality issues (NaN values or zero error metrics)"""
    
    print(f"Input results: {len(results_df)} rows")
    
    # Check the new column names from forecast.py output
    error_columns = ['Global_MASE', 'Global_RMSE']
    available_columns = [col for col in error_columns if col in results_df.columns]
    
    if not available_columns:
        print("Warning: No Global_MASE or Global_RMSE columns found for quality filtering")
        return results_df
    
    print(f"Checking quality for columns: {available_columns}")
    
    # Track filtering reasons
    initial_count = len(results_df)
    nan_mask = results_df[available_columns].isna().any(axis=1)
    zero_mask = (results_df[available_columns] == 0).any(axis=1)
    
    nan_count = nan_mask.sum()
    zero_count = zero_mask.sum()
    
    # Filter out rows with NaN or zero values
    quality_results = results_df[~(nan_mask | zero_mask)].copy()
    
    print(f"Filtered out:")
    print(f"  - {nan_count} rows with NaN values")
    print(f"  - {zero_count} rows with zero values")
    print(f"Final results: {len(quality_results)} rows ({len(quality_results)/initial_count*100:.1f}% retained)")
    
    return quality_results

def create_quality_summary():
    """Create a comprehensive quality summary showing completion status for all model x dataset pairs"""
    
    print("Creating quality summary...")
    
    # Load models config from new location
    models_config_path = Path(__file__).parent.parent / "forecasting" / "models_config.toml"
    if not models_config_path.exists():
        print(f"Warning: Models config not found at {models_config_path}")
        return None
        
    with open(models_config_path, 'rb') as f:
        models_config = tomli.load(f)
    
    all_models = list(models_config.keys())
    print(f"Found {len(all_models)} models in config")
    
    # Get datasets from new error_metrics directory structure
    error_metrics_dir = FORECAST2_DIR / "error_metrics"
    if not error_metrics_dir.exists():
        print(f"Error: Error metrics directory not found at {error_metrics_dir}")
        return None
    
    # Scan for all datasets (they are now subdirectories)
    all_datasets = set()
    for dataset_dir in error_metrics_dir.iterdir():
        if dataset_dir.is_dir():
            all_datasets.add(dataset_dir.name)
    
    all_datasets = sorted(list(all_datasets))
    print(f"Found {len(all_datasets)} unique datasets")
    
    # Load the assembled results for comparison
    results_file = FORECAST2_DIR / "results_all.csv"
    if results_file.exists():
        results_df = pd.read_csv(results_file)
        print(f"Loaded {len(results_df)} results from assembled file")
    else:
        print("Warning: No assembled results file found")
        results_df = pd.DataFrame()
    
    # Create quality summary data
    quality_data = []
    
    for model in all_models:
        for dataset in all_datasets:
            # Check if CSV file exists in new structure
            csv_path = error_metrics_dir / dataset / f"{model}.csv"
            
            if not csv_path.exists():
                status = "No_CSV"
                issue_details = "No CSV file generated"
            else:
                # Check if this model x dataset appears in assembled results
                result_row = results_df[
                    (results_df['Model'] == models_config[model]['display_name']) & 
                    (results_df['Dataset'] == dataset)
                ]
                
                if result_row.empty:
                    status = "CSV_But_No_Results"
                    issue_details = "CSV exists but not in assembled results"
                else:
                    # Check for quality issues in new column names
                    error_columns = ['Global_MASE', 'Global_RMSE']
                    available_columns = [col for col in error_columns if col in result_row.columns]
                    
                    has_nan = result_row[available_columns].isna().any().any() if available_columns else False
                    has_zero = (result_row[available_columns] == 0).any().any() if available_columns else False
                    
                    if has_nan or has_zero:
                        status = "Quality_Issues"
                        issues = []
                        if has_nan:
                            issues.append("NaN values")
                        if has_zero:
                            issues.append("Zero values")
                        issue_details = "; ".join(issues)
                    else:
                        status = "Success"
                        issue_details = "Completed successfully"
            
            quality_data.append({
                'Model': model,
                'Dataset': dataset,
                'Status': status,
                'Issue_Details': issue_details,
                'CSV_Exists': csv_path.exists()
            })
    
    quality_df = pd.DataFrame(quality_data)
    
    # Print summary statistics
    print("\nQuality Summary Statistics:")
    status_counts = quality_df['Status'].value_counts()
    total_combinations = len(quality_df)
    
    for status, count in status_counts.items():
        print(f"  {status}: {count} ({count/total_combinations*100:.1f}%)")
    
    # Save the detailed quality summary
    quality_csv = FORECAST2_DIR / "quality_summary_detailed.csv"
    quality_df.to_csv(quality_csv, index=False)
    print(f"\nSaved detailed quality summary to: {quality_csv}")
    
    # Create a pivot table showing status for each model x dataset
    quality_pivot = quality_df.pivot_table(
        index='Model',
        columns='Dataset', 
        values='Status',
        aggfunc='first',
        fill_value='Missing'
    )
    
    # Save pivot table
    quality_pivot_csv = FORECAST2_DIR / "quality_summary_pivot.csv"
    quality_pivot.to_csv(quality_pivot_csv)
    print(f"Saved quality pivot table to: {quality_pivot_csv}")
    
    # Create LaTeX table for the summary statistics
    summary_stats = pd.DataFrame({
        'Status': status_counts.index,
        'Count': status_counts.values,
        'Percentage': (status_counts.values / total_combinations * 100).round(1)
    })
    
    latex_summary = summary_stats.to_latex(
        caption="Quality Summary: Model x Dataset Completion Status",
        label="tab:quality_summary",
        index=False,
        float_format="%.1f"
    )
    
    quality_tex = FORECAST2_DIR / "quality_summary.tex"
    with open(quality_tex, 'w') as f:
        f.write(latex_summary)
    print(f"Saved quality summary (LaTeX) to: {quality_tex}")
    
    return quality_df

def create_failure_analysis(quality_df):
    """Create model and dataset failure analysis reports"""
    
    print("\nCreating failure analysis reports...")
    
    if quality_df is None or quality_df.empty:
        print("Warning: No quality data available for failure analysis")
        return None, None
    
    # Model failure analysis
    model_analysis = quality_df.groupby('Model').agg({
        'Status': ['count', lambda x: (x == 'Success').sum(), 
                   lambda x: (x == 'Quality_Issues').sum(),
                   lambda x: (x == 'No_CSV').sum(),
                   lambda x: (x == 'CSV_But_No_Results').sum()]
    }).round(2)
    
    # Flatten column names
    model_analysis.columns = ['Total_Datasets', 'Success_Count', 'Quality_Issues_Count', 
                             'No_CSV_Count', 'CSV_But_No_Results_Count']
    
    # Calculate success rates
    model_analysis['Success_Rate'] = (model_analysis['Success_Count'] / model_analysis['Total_Datasets'] * 100).round(1)
    model_analysis['Failure_Rate'] = (100 - model_analysis['Success_Rate']).round(1)
    
    # Sort by success rate (ascending to show worst performers first)
    model_analysis = model_analysis.sort_values('Success_Rate')
    
    # Save model analysis
    model_csv = FORECAST2_DIR / "model_failure_analysis.csv"
    model_analysis.to_csv(model_csv)
    print(f"Saved model failure analysis to: {model_csv}")
    
    # Create LaTeX version for model analysis
    model_latex = model_analysis.to_latex(
        caption="Model Failure Analysis: Success and Failure Rates by Model",
        label="tab:model_failures",
        float_format="%.1f",
        column_format='l' + 'r' * len(model_analysis.columns)
    )
    
    model_tex = FORECAST2_DIR / "model_failure_analysis.tex"
    with open(model_tex, 'w') as f:
        f.write(model_latex)
    print(f"Saved model failure analysis (LaTeX) to: {model_tex}")
    
    # Dataset failure analysis
    dataset_analysis = quality_df.groupby('Dataset').agg({
        'Status': ['count', lambda x: (x == 'Success').sum(), 
                   lambda x: (x == 'Quality_Issues').sum(),
                   lambda x: (x == 'No_CSV').sum(),
                   lambda x: (x == 'CSV_But_No_Results').sum()]
    }).round(2)
    
    # Flatten column names
    dataset_analysis.columns = ['Total_Models', 'Success_Count', 'Quality_Issues_Count', 
                               'No_CSV_Count', 'CSV_But_No_Results_Count']
    
    # Calculate success rates
    dataset_analysis['Success_Rate'] = (dataset_analysis['Success_Count'] / dataset_analysis['Total_Models'] * 100).round(1)
    dataset_analysis['Failure_Rate'] = (100 - dataset_analysis['Success_Rate']).round(1)
    
    # Sort by success rate (ascending to show worst performers first)
    dataset_analysis = dataset_analysis.sort_values('Success_Rate')
    
    # Save dataset analysis
    dataset_csv = FORECAST2_DIR / "dataset_failure_analysis.csv"
    dataset_analysis.to_csv(dataset_csv)
    print(f"Saved dataset failure analysis to: {dataset_csv}")
    
    # Create LaTeX version for dataset analysis
    dataset_latex = dataset_analysis.to_latex(
        caption="Dataset Failure Analysis: Success and Failure Rates by Dataset",
        label="tab:dataset_failures",
        float_format="%.1f",
        column_format='l' + 'r' * len(dataset_analysis.columns)
    )
    
    dataset_tex = FORECAST2_DIR / "dataset_failure_analysis.tex"
    with open(dataset_tex, 'w') as f:
        f.write(dataset_latex)
    print(f"Saved dataset failure analysis (LaTeX) to: {dataset_tex}")
    
    # Print top failures
    print("\nTop 5 Worst Performing Models:")
    print(model_analysis[['Success_Count', 'Failure_Rate']].head())
    
    print("\nTop 5 Most Problematic Datasets:")
    print(dataset_analysis[['Success_Count', 'Failure_Rate']].head())
    
    return model_analysis, dataset_analysis

def create_mase_pivot_table():
    """Create a pivot table with MASE values: datasets as columns, models as rows"""
    
    print("Creating MASE pivot table...")
    
    # Read the assembled results from new location
    results_file = FORECAST2_DIR / "results_all.csv"
    if not results_file.exists():
        print(f"Error: Results file not found at {results_file}")
        print("Please run the assemble_results2 task first")
        sys.exit(1)
    
    results = pd.read_csv(results_file)
    print(f"Loaded {len(results)} result rows")
    
    # Apply quality filtering
    results = filter_quality_results(results)
    
    # Check if we have the required columns (new column names)
    if 'Global_MASE' not in results.columns:
        print("Error: Global_MASE column not found in results")
        print(f"Available columns: {list(results.columns)}")
        sys.exit(1)
    
    # Create pivot table: models as rows, datasets as columns, values as Global_MASE
    # Note: Using 'Model' (display name) and 'Dataset' columns from new format
    mase_pivot = results.pivot_table(
        index='Model',  # Changed from 'model' to 'Model' (display name)
        columns='Dataset',  # Changed from 'dataset' to 'Dataset'
        values='Global_MASE',  # Changed from 'g_mase' to 'Global_MASE'
        aggfunc='first'  # In case of duplicates, take the first value
    )
    
    print(f"Created pivot table with {len(mase_pivot)} models and {len(mase_pivot.columns)} datasets")
    
    # Sort models alphabetically for consistent output
    mase_pivot = mase_pivot.sort_index()
    
    # Sort datasets alphabetically for consistent output
    mase_pivot = mase_pivot.reindex(sorted(mase_pivot.columns), axis=1)
    
    # Save as CSV for inspection
    csv_file = FORECAST2_DIR / "mase_pivot_table.csv"
    mase_pivot.to_csv(csv_file)
    print(f"Saved MASE pivot table (CSV) to: {csv_file}")
    
    # Save also to docs_src for easier access
    docs_csv_file = Path(__file__).parent.parent / "docs_src" / "mase_pivot_table.csv"
    docs_csv_file.parent.mkdir(parents=True, exist_ok=True)
    mase_pivot.to_csv(docs_csv_file)
    print(f"Saved MASE pivot table (CSV) to: {docs_csv_file}")
    
    # Convert to LaTeX table
    latex_output = create_latex_table(mase_pivot, "MASE Results by Model and Dataset")
    
    # Save as .tex file
    tex_file = FORECAST2_DIR / "mase_pivot_table.tex"
    with open(tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved MASE pivot table (LaTeX) to: {tex_file}")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Number of models: {len(mase_pivot)}")
    print(f"Number of datasets: {len(mase_pivot.columns)}")
    
    # Count missing values
    total_cells = len(mase_pivot) * len(mase_pivot.columns)
    missing_cells = mase_pivot.isna().sum().sum()
    print(f"Missing values: {missing_cells} out of {total_cells} ({missing_cells/total_cells*100:.1f}%)")
    
    if missing_cells > 0:
        print("\nModels with missing results:")
        for model in mase_pivot.index:
            missing_count = mase_pivot.loc[model].isna().sum()
            if missing_count > 0:
                print(f"  {model}: {missing_count} missing datasets")
    
    return mase_pivot

def create_latex_table(df, caption):
    """Create a LaTeX table with proper formatting"""
    
    # Handle missing values by replacing NaN with --
    df_formatted = df.copy()
    df_formatted = df_formatted.fillna('--')
    
    # Format numbers to 2 decimal places (except for -- values)
    for col in df_formatted.columns:
        df_formatted[col] = df_formatted[col].apply(
            lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else str(x)
        )
    
    # Convert to LaTeX
    latex_str = df_formatted.to_latex(
        escape=False,
        column_format='l' + 'r' * len(df_formatted.columns),
        caption=caption,
        label='tab:mase_results',
        position='htbp'
    )
    
    # Add some additional LaTeX formatting
    latex_formatted = f"""% MASE Results Table
% Generated automatically by create_results_tables2.py

\\begin{{table}}[htbp]
\\centering
\\caption{{{caption}}}
\\label{{tab:mase_results}}
\\footnotesize
{latex_str.split('\\begin{tabular}')[1].split('\\end{tabular}')[0]}
\\end{{tabular}}
\\note{{Values show Mean Absolute Scaled Error (MASE). Lower values indicate better performance. -- indicates missing results.}}
\\end{{table}}
"""
    
    return latex_formatted.replace('\\begin{tabular}', '\\begin{tabular}').replace('\\end{tabular}', '\\end{tabular}')

def create_summary_statistics():
    """Create summary statistics table"""
    
    print("\nCreating summary statistics...")
    
    results_file = FORECAST2_DIR / "results_all.csv"
    results = pd.read_csv(results_file)
    
    # Apply quality filtering
    results = filter_quality_results(results)
    
    # Summary by model (using new column names)
    model_summary = results.groupby('Model').agg({
        'Global_MASE': ['count', 'mean', 'std', 'min', 'max'],
        'Dataset': 'nunique'
    }).round(3)
    
    # Flatten column names
    model_summary.columns = ['N_Datasets', 'MASE_Avg', 'MASE_Std', 'MASE_Min', 'MASE_Max', 'N_Datasets_Check']
    model_summary = model_summary.drop('N_Datasets_Check', axis=1)
    
    # Add additional metrics if available
    if 'Global_sMAPE' in results.columns:
        smape_summary = results.groupby('Model')['Global_sMAPE'].agg(['mean', 'std']).round(3)
        smape_summary.columns = ['sMAPE_Avg', 'sMAPE_Std']
        model_summary = model_summary.join(smape_summary)
    
    if 'Forecast_Time_seconds' in results.columns:
        time_summary = results.groupby('Model')['Forecast_Time_seconds'].agg(['mean', 'sum']).round(2)
        time_summary.columns = ['Time_Avg_s', 'Time_Total_s']
        model_summary = model_summary.join(time_summary)
    
    # Save summary
    summary_file = FORECAST2_DIR / "model_summary_statistics.csv"
    model_summary.to_csv(summary_file)
    print(f"Saved model summary statistics to: {summary_file}")
    
    # Create LaTeX version
    summary_latex = model_summary.to_latex(
        caption="Summary Statistics by Model",
        label="tab:model_summary",
        float_format="%.3f",
        column_format='l' + 'r' * len(model_summary.columns)
    )
    
    summary_tex_file = FORECAST2_DIR / "model_summary_statistics.tex"
    with open(summary_tex_file, 'w') as f:
        f.write(summary_latex)
    print(f"Saved model summary statistics (LaTeX) to: {summary_tex_file}")
    
    return model_summary

def create_slurm_job_summary():
    """Create summary of SLURM job execution results"""
    
    print("\nCreating SLURM job summary...")
    
    logs_dir = OUTPUT_DIR / "forecasting2" / "logs"
    
    if not logs_dir.exists():
        print(f"Warning: No SLURM logs directory found at {logs_dir}")
        return None
    
    # Read successful and failed job logs if they exist
    successful_jobs = []
    failed_jobs = []
    warnings = []
    
    success_file = logs_dir / "successful_jobs.txt"
    if success_file.exists():
        with open(success_file, 'r') as f:
            successful_jobs = f.readlines()
    
    failed_file = logs_dir / "failed_jobs.txt"
    if failed_file.exists():
        with open(failed_file, 'r') as f:
            failed_jobs = f.readlines()
    
    warnings_file = logs_dir / "warnings.txt"
    if warnings_file.exists():
        with open(warnings_file, 'r') as f:
            warnings = f.readlines()
    
    print(f"SLURM Job Summary:")
    print(f"  Successful jobs: {len(successful_jobs)}")
    print(f"  Failed jobs: {len(failed_jobs)}")
    print(f"  Warnings: {len(warnings)}")
    
    # Create summary DataFrame
    summary_data = {
        'Status': ['Successful', 'Failed', 'Warnings'],
        'Count': [len(successful_jobs), len(failed_jobs), len(warnings)]
    }
    
    summary_df = pd.DataFrame(summary_data)
    
    # Save summary
    summary_csv = FORECAST2_DIR / "slurm_job_summary.csv"
    summary_df.to_csv(summary_csv, index=False)
    print(f"Saved SLURM job summary to: {summary_csv}")
    
    return summary_df

if __name__ == "__main__":
    print("Creating results tables for new forecasting system...")
    
    # Create output directory if it doesn't exist
    FORECAST2_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create quality summary first
    quality_summary = create_quality_summary()
    
    # Create failure analysis reports
    model_failures, dataset_failures = create_failure_analysis(quality_summary)
    
    # Create the main MASE pivot table (now with quality filtering)
    mase_table = create_mase_pivot_table()
    
    # Create summary statistics (now with quality filtering)
    summary_stats = create_summary_statistics()
    
    # Create SLURM job summary if applicable
    slurm_summary = create_slurm_job_summary()
    
    print("\nResults table creation completed!")
    print("\nFiles created:")
    print("Quality Analysis:")
    print(f"  - {FORECAST2_DIR / 'quality_summary_detailed.csv'}")
    print(f"  - {FORECAST2_DIR / 'quality_summary_pivot.csv'}")
    print(f"  - {FORECAST2_DIR / 'quality_summary.tex'}")
    print(f"  - {FORECAST2_DIR / 'model_failure_analysis.csv'}")
    print(f"  - {FORECAST2_DIR / 'model_failure_analysis.tex'}")
    print(f"  - {FORECAST2_DIR / 'dataset_failure_analysis.csv'}")
    print(f"  - {FORECAST2_DIR / 'dataset_failure_analysis.tex'}")
    print("Main Tables (with quality filtering):")
    print(f"  - {FORECAST2_DIR / 'mase_pivot_table.csv'}")
    print(f"  - {FORECAST2_DIR / 'mase_pivot_table.tex'}")
    print(f"  - {FORECAST2_DIR / 'model_summary_statistics.csv'}")
    print(f"  - {FORECAST2_DIR / 'model_summary_statistics.tex'}")
    if slurm_summary is not None:
        print("SLURM Job Analysis:")
        print(f"  - {FORECAST2_DIR / 'slurm_job_summary.csv'}")
    print("Additional Output:")
    print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'mase_pivot_table.csv'}")