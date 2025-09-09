import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
import tomli
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

from settings import config

OUTPUT_DIR = Path(config("OUTPUT_DIR"))
FORECAST2_DIR = OUTPUT_DIR / "forecasting2"  # New forecasting output directory

def load_dataset_short_names():
    """Load dataset short names from datasets.toml"""
    datasets_toml_path = Path(__file__).parent.parent / "datasets.toml"
    
    if not datasets_toml_path.exists():
        print(f"Warning: datasets.toml not found at {datasets_toml_path}")
        return {}
    
    with open(datasets_toml_path, 'rb') as f:
        datasets_config = tomli.load(f)
    
    # Create mapping from full dataset name to short name
    name_mapping = {}
    
    for module_name, module_config in datasets_config.items():
        if isinstance(module_config, dict):
            # Look for dataset entries within each module
            for key, value in module_config.items():
                if isinstance(value, dict) and key.startswith('ftsfr_'):
                    # This is a dataset entry
                    dataset_name = key
                    short_name = value.get('short_name', dataset_name)  # fallback to full name
                    name_mapping[dataset_name] = short_name
    
    print(f"Loaded {len(name_mapping)} dataset short names")
    return name_mapping

def load_dataset_groups_and_names():
    """Load dataset groups and table names from datasets.toml"""
    datasets_toml_path = Path(__file__).parent.parent / "datasets.toml"
    
    if not datasets_toml_path.exists():
        print(f"Warning: datasets.toml not found at {datasets_toml_path}")
        return {}, {}
    
    with open(datasets_toml_path, 'rb') as f:
        datasets_config = tomli.load(f)
    
    # Create mappings from full dataset name to group and table name
    group_mapping = {}
    table_name_mapping = {}
    
    for module_name, module_config in datasets_config.items():
        if isinstance(module_config, dict):
            # Look for dataset entries within each module
            for key, value in module_config.items():
                if isinstance(value, dict) and key.startswith('ftsfr_'):
                    # This is a dataset entry
                    dataset_name = key
                    group = value.get('group', 'other')
                    table_name = value.get('table_name', value.get('short_name', dataset_name))
                    group_mapping[dataset_name] = group
                    table_name_mapping[dataset_name] = table_name
    
    print(f"Loaded {len(group_mapping)} dataset groups and table names")
    return group_mapping, table_name_mapping

def load_model_table_names():
    """Load model table names from models_config.toml"""
    models_config_path = Path(__file__).parent.parent / "forecasting" / "models_config.toml"
    
    if not models_config_path.exists():
        print(f"Warning: models_config.toml not found at {models_config_path}")
        return {}
    
    with open(models_config_path, 'rb') as f:
        models_config = tomli.load(f)
    
    # Create mapping from display_name to table_name
    name_mapping = {}
    
    for model_key, model_config in models_config.items():
        if isinstance(model_config, dict):
            display_name = model_config.get('display_name', model_key)
            table_name = model_config.get('table_name', display_name)  # fallback to display_name
            name_mapping[display_name] = table_name
    
    print(f"Loaded {len(name_mapping)} model table names")
    return name_mapping

def load_model_order():
    """Load ordered list of model names from models_config.toml to preserve column order"""
    models_config_path = Path(__file__).parent.parent / "forecasting" / "models_config.toml"
    
    if not models_config_path.exists():
        print(f"Warning: models_config.toml not found at {models_config_path}")
        return []
    
    with open(models_config_path, 'rb') as f:
        models_config = tomli.load(f)
    
    # Get ordered list of models as they appear in the config file
    ordered_models = []
    
    for model_key, model_config in models_config.items():
        if isinstance(model_config, dict):
            display_name = model_config.get('display_name', model_key)
            # Also get table_name for potential use
            table_name = model_config.get('table_name', display_name)
            ordered_models.append({
                'key': model_key,
                'display_name': display_name,
                'table_name': table_name
            })
    
    print(f"Loaded model order with {len(ordered_models)} models from config")
    return ordered_models

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
    
    # Load dataset short names and apply to results
    dataset_short_names = load_dataset_short_names()
    results['Dataset_Short'] = results['Dataset'].map(dataset_short_names).fillna(results['Dataset'])
    
    # Rename model names for consistency
    results['Model'] = results['Model'].replace('AutoARIMA Fast', 'AutoARIMA')
    
    # Apply quality filtering
    results = filter_quality_results(results)
    
    # Check if we have the required columns (new column names)
    if 'Global_MASE' not in results.columns:
        print("Error: Global_MASE column not found in results")
        print(f"Available columns: {list(results.columns)}")
        sys.exit(1)
    
    # Create pivot table: datasets as rows, models as columns, values as Global_MASE
    # Note: Using 'Model' (display name) and 'Dataset_Short' columns from new format
    mase_pivot = results.pivot_table(
        index='Dataset_Short',  # Short dataset names as rows
        columns='Model',  # Models as columns (display name)
        values='Global_MASE',  # Changed from 'g_mase' to 'Global_MASE'
        aggfunc='first'  # In case of duplicates, take the first value
    )
    
    print(f"Created pivot table with {len(mase_pivot)} datasets and {len(mase_pivot.columns)} models")
    
    # Apply model ordering based on models_config.toml
    model_order = load_model_order()
    if model_order:
        # Create ordered list of display names that exist in the data
        ordered_display_names = [model['display_name'] for model in model_order]
        # Filter to only include columns that actually exist in the pivot table
        existing_ordered_columns = [col for col in ordered_display_names if col in mase_pivot.columns]
        # Add any columns not in the config (shouldn't happen, but safety check)
        remaining_columns = [col for col in mase_pivot.columns if col not in existing_ordered_columns]
        final_column_order = existing_ordered_columns + remaining_columns
        # Reorder the columns
        mase_pivot = mase_pivot.reindex(columns=final_column_order)
        print(f"Reordered model columns according to models_config.toml")
    
    # Sort datasets alphabetically for consistent output
    mase_pivot = mase_pivot.sort_index()
    
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
    latex_output = create_latex_table(mase_pivot, "MASE Results by Dataset and Model", "tab:mase_results")
    
    # Save LaTeX version to docs_src as well
    docs_tex_file = Path(__file__).parent.parent / "docs_src" / "mase_pivot_table.tex"
    with open(docs_tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved MASE pivot table (LaTeX) to: {docs_tex_file}")
    
    # Save as .tex file
    tex_file = FORECAST2_DIR / "mase_pivot_table.tex"
    with open(tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved MASE pivot table (LaTeX) to: {tex_file}")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Number of datasets: {len(mase_pivot)}")
    print(f"Number of models: {len(mase_pivot.columns)}")
    
    # Count missing values
    total_cells = len(mase_pivot) * len(mase_pivot.columns)
    missing_cells = mase_pivot.isna().sum().sum()
    print(f"Missing values: {missing_cells} out of {total_cells} ({missing_cells/total_cells*100:.1f}%)")
    
    if missing_cells > 0:
        print("\nDatasets with missing results:")
        for dataset in mase_pivot.index:
            missing_count = mase_pivot.loc[dataset].isna().sum()
            if missing_count > 0:
                print(f"  {dataset}: {missing_count} missing models")
    
    return mase_pivot

def create_rmse_pivot_table():
    """Create a pivot table with RMSE values: datasets as rows, models as columns"""
    
    print("Creating RMSE pivot table...")
    
    # Read the assembled results from new location
    results_file = FORECAST2_DIR / "results_all.csv"
    if not results_file.exists():
        print(f"Error: Results file not found at {results_file}")
        print("Please run the assemble_results2 task first")
        sys.exit(1)
    
    results = pd.read_csv(results_file)
    print(f"Loaded {len(results)} result rows")
    
    # Load dataset short names and apply to results
    dataset_short_names = load_dataset_short_names()
    results['Dataset_Short'] = results['Dataset'].map(dataset_short_names).fillna(results['Dataset'])
    
    # Rename model names for consistency
    results['Model'] = results['Model'].replace('AutoARIMA Fast', 'AutoARIMA')
    
    # Apply quality filtering
    results = filter_quality_results(results)
    
    # Check if we have the required columns
    if 'Global_RMSE' not in results.columns:
        print("Error: Global_RMSE column not found in results")
        print(f"Available columns: {list(results.columns)}")
        sys.exit(1)
    
    # Create pivot table: datasets as rows, models as columns, values as Global_RMSE
    rmse_pivot = results.pivot_table(
        index='Dataset_Short',  # Short dataset names as rows
        columns='Model',  # Models as columns (display name)
        values='Global_RMSE',
        aggfunc='first'  # In case of duplicates, take the first value
    )
    
    print(f"Created pivot table with {len(rmse_pivot)} datasets and {len(rmse_pivot.columns)} models")
    
    # Apply model ordering based on models_config.toml
    model_order = load_model_order()
    if model_order:
        # Create ordered list of display names that exist in the data
        ordered_display_names = [model['display_name'] for model in model_order]
        # Filter to only include columns that actually exist in the pivot table
        existing_ordered_columns = [col for col in ordered_display_names if col in rmse_pivot.columns]
        # Add any columns not in the config (shouldn't happen, but safety check)
        remaining_columns = [col for col in rmse_pivot.columns if col not in existing_ordered_columns]
        final_column_order = existing_ordered_columns + remaining_columns
        # Reorder the columns
        rmse_pivot = rmse_pivot.reindex(columns=final_column_order)
        print(f"Reordered model columns according to models_config.toml")
    
    # Sort datasets alphabetically for consistent output
    rmse_pivot = rmse_pivot.sort_index()
    
    # Save as CSV for inspection
    csv_file = FORECAST2_DIR / "rmse_pivot_table.csv"
    rmse_pivot.to_csv(csv_file)
    print(f"Saved RMSE pivot table (CSV) to: {csv_file}")
    
    # Save also to docs_src for easier access
    docs_csv_file = Path(__file__).parent.parent / "docs_src" / "rmse_pivot_table.csv"
    docs_csv_file.parent.mkdir(parents=True, exist_ok=True)
    rmse_pivot.to_csv(docs_csv_file)
    print(f"Saved RMSE pivot table (CSV) to: {docs_csv_file}")
    
    # Convert to LaTeX table
    latex_output = create_latex_table(rmse_pivot, "RMSE Results by Dataset and Model", "tab:rmse_results")
    
    # Save as .tex file
    tex_file = FORECAST2_DIR / "rmse_pivot_table.tex"
    with open(tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved RMSE pivot table (LaTeX) to: {tex_file}")
    
    # Save LaTeX version to docs_src as well
    docs_tex_file = Path(__file__).parent.parent / "docs_src" / "rmse_pivot_table.tex"
    with open(docs_tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved RMSE pivot table (LaTeX) to: {docs_tex_file}")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Number of datasets: {len(rmse_pivot)}")
    print(f"Number of models: {len(rmse_pivot.columns)}")
    
    # Count missing values
    total_cells = len(rmse_pivot) * len(rmse_pivot.columns)
    missing_cells = rmse_pivot.isna().sum().sum()
    print(f"Missing values: {missing_cells} out of {total_cells} ({missing_cells/total_cells*100:.1f}%)")
    
    if missing_cells > 0:
        print("\nDatasets with missing results:")
        for dataset in rmse_pivot.index:
            missing_count = rmse_pivot.loc[dataset].isna().sum()
            if missing_count > 0:
                print(f"  {dataset}: {missing_count} missing models")
    
    return rmse_pivot

def create_smape_pivot_table():
    """Create a pivot table with sMAPE values: datasets as rows, models as columns"""
    
    print("Creating sMAPE pivot table...")
    
    # Read the assembled results from new location
    results_file = FORECAST2_DIR / "results_all.csv"
    if not results_file.exists():
        print(f"Error: Results file not found at {results_file}")
        print("Please run the assemble_results2 task first")
        sys.exit(1)
    
    results = pd.read_csv(results_file)
    print(f"Loaded {len(results)} result rows")
    
    # Load dataset short names and apply to results
    dataset_short_names = load_dataset_short_names()
    results['Dataset_Short'] = results['Dataset'].map(dataset_short_names).fillna(results['Dataset'])
    
    # Rename model names for consistency
    results['Model'] = results['Model'].replace('AutoARIMA Fast', 'AutoARIMA')
    
    # Apply quality filtering
    results = filter_quality_results(results)
    
    # Check if we have the required columns
    if 'Global_sMAPE' not in results.columns:
        print("Warning: Global_sMAPE column not found in results, skipping sMAPE table")
        return None
    
    # Create pivot table: datasets as rows, models as columns, values as Global_sMAPE
    smape_pivot = results.pivot_table(
        index='Dataset_Short',  # Short dataset names as rows
        columns='Model',  # Models as columns (display name)
        values='Global_sMAPE',
        aggfunc='first'  # In case of duplicates, take the first value
    )
    
    print(f"Created pivot table with {len(smape_pivot)} datasets and {len(smape_pivot.columns)} models")
    
    # Apply model ordering based on models_config.toml
    model_order = load_model_order()
    if model_order:
        # Create ordered list of display names that exist in the data
        ordered_display_names = [model['display_name'] for model in model_order]
        # Filter to only include columns that actually exist in the pivot table
        existing_ordered_columns = [col for col in ordered_display_names if col in smape_pivot.columns]
        # Add any columns not in the config (shouldn't happen, but safety check)
        remaining_columns = [col for col in smape_pivot.columns if col not in existing_ordered_columns]
        final_column_order = existing_ordered_columns + remaining_columns
        # Reorder the columns
        smape_pivot = smape_pivot.reindex(columns=final_column_order)
        print(f"Reordered model columns according to models_config.toml")
    
    # Sort datasets alphabetically for consistent output
    smape_pivot = smape_pivot.sort_index()
    
    # Save as CSV for inspection
    csv_file = FORECAST2_DIR / "smape_pivot_table.csv"
    smape_pivot.to_csv(csv_file)
    print(f"Saved sMAPE pivot table (CSV) to: {csv_file}")
    
    # Save also to docs_src for easier access
    docs_csv_file = Path(__file__).parent.parent / "docs_src" / "smape_pivot_table.csv"
    docs_csv_file.parent.mkdir(parents=True, exist_ok=True)
    smape_pivot.to_csv(docs_csv_file)
    print(f"Saved sMAPE pivot table (CSV) to: {docs_csv_file}")
    
    # Convert to LaTeX table
    latex_output = create_latex_table(smape_pivot, "sMAPE Results by Dataset and Model", "tab:smape_results")
    
    # Save as .tex file
    tex_file = FORECAST2_DIR / "smape_pivot_table.tex"
    with open(tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved sMAPE pivot table (LaTeX) to: {tex_file}")
    
    # Save LaTeX version to docs_src as well
    docs_tex_file = Path(__file__).parent.parent / "docs_src" / "smape_pivot_table.tex"
    with open(docs_tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved sMAPE pivot table (LaTeX) to: {docs_tex_file}")
    
    return smape_pivot

def create_mae_pivot_table():
    """Create a pivot table with MAE values: datasets as rows, models as columns"""
    
    print("Creating MAE pivot table...")
    
    # Read the assembled results from new location
    results_file = FORECAST2_DIR / "results_all.csv"
    if not results_file.exists():
        print(f"Error: Results file not found at {results_file}")
        print("Please run the assemble_results2 task first")
        sys.exit(1)
    
    results = pd.read_csv(results_file)
    print(f"Loaded {len(results)} result rows")
    
    # Load dataset short names and apply to results
    dataset_short_names = load_dataset_short_names()
    results['Dataset_Short'] = results['Dataset'].map(dataset_short_names).fillna(results['Dataset'])
    
    # Rename model names for consistency
    results['Model'] = results['Model'].replace('AutoARIMA Fast', 'AutoARIMA')
    
    # Apply quality filtering
    results = filter_quality_results(results)
    
    # Check if we have the required columns
    if 'Global_MAE' not in results.columns:
        print("Warning: Global_MAE column not found in results, skipping MAE table")
        return None
    
    # Create pivot table: datasets as rows, models as columns, values as Global_MAE
    mae_pivot = results.pivot_table(
        index='Dataset_Short',  # Short dataset names as rows
        columns='Model',  # Models as columns (display name)
        values='Global_MAE',
        aggfunc='first'  # In case of duplicates, take the first value
    )
    
    print(f"Created pivot table with {len(mae_pivot)} datasets and {len(mae_pivot.columns)} models")
    
    # Apply model ordering based on models_config.toml
    model_order = load_model_order()
    if model_order:
        # Create ordered list of display names that exist in the data
        ordered_display_names = [model['display_name'] for model in model_order]
        # Filter to only include columns that actually exist in the pivot table
        existing_ordered_columns = [col for col in ordered_display_names if col in mae_pivot.columns]
        # Add any columns not in the config (shouldn't happen, but safety check)
        remaining_columns = [col for col in mae_pivot.columns if col not in existing_ordered_columns]
        final_column_order = existing_ordered_columns + remaining_columns
        # Reorder the columns
        mae_pivot = mae_pivot.reindex(columns=final_column_order)
        print(f"Reordered model columns according to models_config.toml")
    
    # Sort datasets alphabetically for consistent output
    mae_pivot = mae_pivot.sort_index()
    
    # Save as CSV for inspection
    csv_file = FORECAST2_DIR / "mae_pivot_table.csv"
    mae_pivot.to_csv(csv_file)
    print(f"Saved MAE pivot table (CSV) to: {csv_file}")
    
    # Save also to docs_src for easier access
    docs_csv_file = Path(__file__).parent.parent / "docs_src" / "mae_pivot_table.csv"
    docs_csv_file.parent.mkdir(parents=True, exist_ok=True)
    mae_pivot.to_csv(docs_csv_file)
    print(f"Saved MAE pivot table (CSV) to: {docs_csv_file}")
    
    # Convert to LaTeX table
    latex_output = create_latex_table(mae_pivot, "MAE Results by Dataset and Model", "tab:mae_results")
    
    # Save as .tex file
    tex_file = FORECAST2_DIR / "mae_pivot_table.tex"
    with open(tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved MAE pivot table (LaTeX) to: {tex_file}")
    
    # Save LaTeX version to docs_src as well
    docs_tex_file = Path(__file__).parent.parent / "docs_src" / "mae_pivot_table.tex"
    with open(docs_tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved MAE pivot table (LaTeX) to: {docs_tex_file}")
    
    return mae_pivot

def create_sectioned_latex_table(df, caption, label="tab:mase_results"):
    """Create a LaTeX table with dataset grouping sections"""
    
    # Load dataset groups and table names
    group_mapping, table_name_mapping = load_dataset_groups_and_names()
    
    # Handle missing values by replacing NaN with --
    df_formatted = df.copy()
    df_original = df.copy()  # Keep original for comparison
    df_formatted = df_formatted.fillna('--')
    
    # Identify best performing models for each dataset (before formatting)
    best_models = {}
    for dataset in df_original.index:
        # Get numeric values only (exclude NaN values)  
        row_values = df_original.loc[dataset]
        numeric_values = pd.to_numeric(row_values, errors='coerce')
        
        if not numeric_values.isna().all():  # If we have any valid numbers
            min_value = numeric_values.min()
            # Find which model(s) achieved this minimum (handle ties)
            best_model_cols = numeric_values[numeric_values == min_value].index.tolist()
            best_models[dataset] = best_model_cols
        else:
            best_models[dataset] = []  # No valid values, no bolding
    
    # Format numbers to 2 decimal places (except for -- values)
    for col in df_formatted.columns:
        df_formatted[col] = df_formatted[col].apply(
            lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else str(x)
        )
    
    # Use abbreviated model names for LaTeX
    model_table_names = load_model_table_names()
    # Rename columns to use table names
    new_columns = []
    for col in df_formatted.columns:
        new_columns.append(model_table_names.get(col, col))
    df_formatted.columns = new_columns
    
    # Map dataset names to groups and table names
    dataset_groups = {}
    dataset_table_names = {}
    
    for dataset in df_formatted.index:
        # Find the corresponding full dataset name
        full_dataset = None
        for k, v in load_dataset_short_names().items():
            if v == dataset:
                full_dataset = k
                break
        
        if full_dataset and full_dataset in group_mapping:
            group = group_mapping[full_dataset]
            table_name = table_name_mapping[full_dataset]
        else:
            group = 'other'
            table_name = dataset
            
        dataset_groups[dataset] = group
        dataset_table_names[dataset] = table_name
    
    # Define group order and labels
    group_order = ['basis_spreads', 'returns_portfolios', 'returns_disaggregated', 'other']
    group_labels = {
        'basis_spreads': '\\textbf{Basis Spreads}',
        'returns_portfolios': '\\textbf{Returns (Portfolios)}',
        'returns_disaggregated': '\\textbf{Returns (Disaggregated)}', 
        'other': '\\textbf{Other}'
    }
    
    # Group datasets
    grouped_datasets = {}
    for group in group_order:
        grouped_datasets[group] = []
    
    for dataset in df_formatted.index:
        group = dataset_groups[dataset]
        if group in grouped_datasets:
            grouped_datasets[group].append(dataset)
    
    # Build LaTeX table content
    tabular_content = ""
    num_cols = len(df_formatted.columns)
    
    # Create header
    header = " & " + " & ".join(df_formatted.columns) + " \\\\\n"
    
    # Build table content with sections
    first_group = True
    for group in group_order:
        datasets = grouped_datasets[group]
        if not datasets:
            continue
            
        if not first_group:
            tabular_content += "\\midrule\n"
        
        # Add group header
        tabular_content += f"\\multicolumn{{{num_cols + 1}}}{{l}}{{{group_labels[group]}}} \\\\\n"
        
        # Add datasets in this group
        for dataset in datasets:
            table_name = dataset_table_names[dataset].replace('_', '\\_')
            
            # Create row data with bold formatting for best performers
            row_data_formatted = []
            original_cols = list(df_original.columns)  # Use original column names for comparison
            
            for i, col in enumerate(df_formatted.columns):
                value_str = str(df_formatted.loc[dataset, col])
                # Check if this model was best for this dataset (using original column names)
                original_col = original_cols[i] if i < len(original_cols) else col
                if original_col in best_models.get(dataset, []):
                    value_str = f"\\textbf{{{value_str}}}"
                row_data_formatted.append(value_str)
            
            row_data = " & ".join(row_data_formatted)
            tabular_content += f"{table_name} & {row_data} \\\\\n"
        
        first_group = False
    
    return tabular_content, header, num_cols

def create_latex_table(df, caption, label="tab:mase_results", use_table_names=True):
    """Create a LaTeX table with proper formatting and dataset grouping"""
    
    # Create sectioned table
    tabular_content, header, num_cols = create_sectioned_latex_table(df, caption, label)
    
    # Add some additional LaTeX formatting
    metric_name = "error metric"
    if "MASE" in caption:
        metric_name = "Mean Absolute Scaled Error (MASE)"
    elif "RMSE" in caption:
        metric_name = "Root Mean Square Error (RMSE)"
    elif "sMAPE" in caption:
        metric_name = "Symmetric Mean Absolute Percentage Error (sMAPE)"
    elif "MAE" in caption:
        metric_name = "Mean Absolute Error (MAE)"
    
    # Build complete tabular environment
    column_format = '@{}l@{\\hspace{2pt}}' + '@{\\hspace{1pt}}r@{\\hspace{1pt}}' * num_cols + '@{}'
    full_tabular = f"""\\begin{{tabular}}{{{column_format}}}
\\toprule
{header}\\midrule
{tabular_content}\\bottomrule
\\end{{tabular}}"""
    
    latex_formatted = f"""% {caption}
% Generated automatically by create_results_tables2.py

\\begin{{table}}[htbp]
\\centering
\\caption{{{caption}}}
\\label{{{label}}}
\\scriptsize
\\setlength{{\\tabcolsep}}{{2pt}}
\\renewcommand{{\\arraystretch}}{{0.85}}
{full_tabular}
\\vspace{{0.05cm}}
\\noindent {{\\scriptsize \\textbf{{Note:}} Values show {metric_name}. Lower values indicate better performance. -- indicates missing results.}}
\\end{{table}}
"""
    
    return latex_formatted

def create_heatmap_plots():
    """Create heatmap plots for all error metrics using the same data structure as tables"""
    
    print("\nCreating heatmap plots for error metrics...")
    
    # Read the assembled results
    results_file = FORECAST2_DIR / "results_all.csv"
    if not results_file.exists():
        print(f"Error: Results file not found at {results_file}")
        return
    
    results = pd.read_csv(results_file)
    print(f"Loaded {len(results)} result rows for heatmap generation")
    
    # Load dataset groups and names for sectioning
    dataset_groups, dataset_table_names = load_dataset_groups_and_names()
    results['Dataset_Short'] = results['Dataset'].map(dataset_table_names).fillna(results['Dataset'])
    
    # Load model table names for abbreviations
    model_names = load_model_table_names()
    results['Model'] = results['Model'].replace('AutoARIMA Fast', 'AutoARIMA')
    
    # Apply quality filtering
    results = filter_quality_results(results)
    
    # Define error metrics to create heatmaps for
    error_metrics = [
        ('Global_MASE', 'MASE', 'mase_heatmap.png', 'Mean Absolute Scaled Error (MASE)'),
        ('Global_RMSE', 'RMSE', 'rmse_heatmap.png', 'Root Mean Square Error (RMSE)'),
        ('Global_sMAPE', 'sMAPE', 'smape_heatmap.png', 'Symmetric Mean Absolute Percentage Error (sMAPE)'),
        ('Global_MAE', 'MAE', 'mae_heatmap.png', 'Mean Absolute Error (MAE)')
    ]
    
    for metric_col, metric_short, filename, metric_long in error_metrics:
        if metric_col not in results.columns:
            print(f"Skipping {metric_short} heatmap - column {metric_col} not found")
            continue
            
        print(f"Creating {metric_short} heatmap...")
        
        # Create pivot table (same structure as LaTeX tables)
        pivot_data = results.pivot_table(
            index='Dataset_Short',
            columns='Model',
            values=metric_col,
            aggfunc='mean'
        )
        
        # Apply model ordering based on models_config.toml (before name abbreviation)
        model_order = load_model_order()
        if model_order:
            # Create ordered list of display names that exist in the data
            ordered_display_names = [model['display_name'] for model in model_order]
            # Filter to only include columns that actually exist in the pivot table
            existing_ordered_columns = [col for col in ordered_display_names if col in pivot_data.columns]
            # Add any columns not in the config (shouldn't happen, but safety check)
            remaining_columns = [col for col in pivot_data.columns if col not in existing_ordered_columns]
            final_column_order = existing_ordered_columns + remaining_columns
            # Reorder the columns
            pivot_data = pivot_data.reindex(columns=final_column_order)
        
        # Apply model name abbreviations
        new_columns = []
        for col in pivot_data.columns:
            if col in model_names:
                new_columns.append(model_names[col])
            else:
                new_columns.append(col)
        pivot_data.columns = new_columns
        
        # Create the heatmap
        plt.figure(figsize=(14, 10))
        
        # Prepare data for heatmap (handle missing values)
        heatmap_data = pivot_data.copy()
        
        # Mask missing values and extreme outliers (999.0)
        mask = (heatmap_data.isna()) | (heatmap_data >= 999.0)
        
        # Use a color scheme where lower values (better performance) are lighter/cooler
        # RdYlBu_r gives red for high (bad), yellow for medium, blue for low (good)
        colormap = 'RdYlBu_r'
        
        # Calculate robust color scale limits to handle outliers
        if not heatmap_data.empty:
            # Use 90th percentile for upper limit to better handle extreme outliers
            vmin_val = heatmap_data.min().min()
            vmax_val = heatmap_data.quantile(0.90).max()  # Changed from 0.95 to 0.90
            
            # As a fallback, use median + 3*IQR if 90th percentile is still too extreme
            q25 = heatmap_data.quantile(0.25).median()
            q75 = heatmap_data.quantile(0.75).median()
            iqr = q75 - q25
            median_val = heatmap_data.median().median()
            iqr_based_max = median_val + 3 * iqr
            
            # Use the more conservative (smaller) of the two approaches
            vmax_val = min(vmax_val, iqr_based_max)
            
            # Ensure we have a reasonable minimum range
            if vmax_val - vmin_val < 1:
                vmax_val = vmin_val + 1
        else:
            vmin_val = 0
            vmax_val = 1
        
        # Identify outliers for special annotation formatting
        outlier_threshold = vmax_val
        
        # Create custom annotations with special formatting for outliers
        annot_data = heatmap_data.copy()
        for i in range(len(heatmap_data.index)):
            for j in range(len(heatmap_data.columns)):
                if not mask.iloc[i, j]:  # Only process non-masked values
                    val = heatmap_data.iloc[i, j]
                    if pd.notna(val):
                        if val > outlier_threshold:
                            # Format outliers differently - keep precision but mark them
                            annot_data.iloc[i, j] = f"{val:.1f}*"
                        else:
                            # Normal formatting for non-outliers
                            annot_data.iloc[i, j] = f"{val:.2f}"
        
        # Create the heatmap with improved scaling
        sns.heatmap(
            heatmap_data,
            mask=mask,
            annot=annot_data,
            fmt='',  # Use empty format since we're providing pre-formatted annotations
            cmap=colormap,
            cbar_kws={'label': f'{metric_long} (colors capped at 90th percentile)'},
            square=False,
            linewidths=0.5,
            annot_kws={'size': 8},
            vmin=vmin_val,
            vmax=vmax_val
        )
        
        plt.title(f'{metric_long} by Dataset and Model\n(Lower values indicate better performance)', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Forecasting Models', fontsize=12, fontweight='bold')
        plt.ylabel('Datasets', fontsize=12, fontweight='bold')
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        # Add dataset group separators (visual sections)
        ax = plt.gca()
        
        # Group datasets by their categories for visual separation
        dataset_indices = {}
        for i, dataset in enumerate(pivot_data.index):
            # Find the group for this dataset
            original_dataset = None
            for orig_name, table_name in dataset_table_names.items():
                if table_name == dataset:
                    original_dataset = orig_name
                    break
            
            if original_dataset and original_dataset in dataset_groups:
                group = dataset_groups[original_dataset]
                if group not in dataset_indices:
                    dataset_indices[group] = []
                dataset_indices[group].append(i)
        
        # Add horizontal lines to separate groups
        y_positions = []
        prev_end = 0
        for group in ['basis_spreads', 'returns_portfolios', 'returns_disaggregated', 'other']:
            if group in dataset_indices:
                group_indices = sorted(dataset_indices[group])
                if group_indices:
                    start_idx = min(group_indices)
                    end_idx = max(group_indices) + 1
                    if start_idx > prev_end:
                        y_positions.append(start_idx)
                    prev_end = end_idx
        
        # Draw separator lines
        for y_pos in y_positions[1:]:  # Skip first line (top border)
            ax.axhline(y=y_pos, color='black', linewidth=2, alpha=0.8)
        
        plt.tight_layout()
        
        # Save the heatmap
        output_file = FORECAST2_DIR / filename
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved heatmap to: {output_file}")
        
        plt.close()  # Close the figure to free memory
    
    print("Heatmap creation completed!")

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
    
    # Create RMSE pivot table
    rmse_table = create_rmse_pivot_table()
    
    # Create sMAPE pivot table (may return None if column doesn't exist)
    smape_table = create_smape_pivot_table()
    
    # Create MAE pivot table (may return None if column doesn't exist)
    mae_table = create_mae_pivot_table()
    
    # Create summary statistics (now with quality filtering)
    summary_stats = create_summary_statistics()
    
    # Create SLURM job summary if applicable
    slurm_summary = create_slurm_job_summary()
    
    # Create heatmap plots for all error metrics
    create_heatmap_plots()
    
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
    print(f"  - {FORECAST2_DIR / 'rmse_pivot_table.csv'}")
    print(f"  - {FORECAST2_DIR / 'rmse_pivot_table.tex'}")
    if smape_table is not None:
        print(f"  - {FORECAST2_DIR / 'smape_pivot_table.csv'}")
        print(f"  - {FORECAST2_DIR / 'smape_pivot_table.tex'}")
    if mae_table is not None:
        print(f"  - {FORECAST2_DIR / 'mae_pivot_table.csv'}")
        print(f"  - {FORECAST2_DIR / 'mae_pivot_table.tex'}")
    print(f"  - {FORECAST2_DIR / 'model_summary_statistics.csv'}")
    print(f"  - {FORECAST2_DIR / 'model_summary_statistics.tex'}")
    if slurm_summary is not None:
        print("SLURM Job Analysis:")
        print(f"  - {FORECAST2_DIR / 'slurm_job_summary.csv'}")
    print("Additional Output (docs_src):")
    print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'mase_pivot_table.csv'}")
    print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'mase_pivot_table.tex'}")
    print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'rmse_pivot_table.csv'}")
    print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'rmse_pivot_table.tex'}")
    if smape_table is not None:
        print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'smape_pivot_table.csv'}")
        print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'smape_pivot_table.tex'}")
    if mae_table is not None:
        print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'mae_pivot_table.csv'}")
        print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'mae_pivot_table.tex'}")