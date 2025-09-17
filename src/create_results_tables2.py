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
from dodo_common import load_models_config

OUTPUT_DIR = Path(config("OUTPUT_DIR"))
FORECAST3_DIR = OUTPUT_DIR / "forecasting3"  # New forecasting output directory

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
    models_config = load_models_config()
    
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
    models_config = load_models_config()
    
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

def get_active_model_display_names():
    """Get list of active model display names from models_config.toml (excluding commented out models)"""
    models_config = load_models_config()
    
    active_models = []
    for model_key, model_config in models_config.items():
        if isinstance(model_config, dict):
            display_name = model_config.get('display_name', model_key)
            active_models.append(display_name)
    
    print(f"Found {len(active_models)} active models: {active_models}")
    return active_models

def filter_results_by_active_models(results_df):
    """Filter results DataFrame to only include active models from config"""
    active_models = get_active_model_display_names()
    
    # Filter results to only include active models
    initial_count = len(results_df)
    filtered_results = results_df[results_df['Model'].isin(active_models)].copy()
    filtered_count = len(filtered_results)
    
    if filtered_count < initial_count:
        removed_count = initial_count - filtered_count
        removed_models = set(results_df['Model'].unique()) - set(active_models)
        print(f"Filtered out {removed_count} results from inactive models: {sorted(removed_models)}")
    
    print(f"Using {filtered_count} results from active models")
    return filtered_results

def get_active_dataset_names():
    """Get list of active dataset names from datasets.toml (excluding commented out datasets)"""
    datasets_toml_path = Path(__file__).parent.parent / "datasets.toml"
    
    if not datasets_toml_path.exists():
        print(f"Warning: datasets.toml not found at {datasets_toml_path}")
        return []
    
    with open(datasets_toml_path, 'rb') as f:
        datasets_config = tomli.load(f)
    
    active_datasets = []
    for module_name, module_config in datasets_config.items():
        if isinstance(module_config, dict):
            # Look for dataset entries within each module
            for key, value in module_config.items():
                if isinstance(value, dict) and key.startswith('ftsfr_'):
                    # This is a dataset entry
                    active_datasets.append(key)
    
    print(f"Found {len(active_datasets)} active datasets: {sorted(active_datasets)}")
    return active_datasets

def filter_results_by_active_datasets(results_df):
    """Filter results DataFrame to only include active datasets from config"""
    active_datasets = get_active_dataset_names()
    
    # Filter results to only include active datasets
    initial_count = len(results_df)
    filtered_results = results_df[results_df['Dataset'].isin(active_datasets)].copy()
    filtered_count = len(filtered_results)
    
    if filtered_count < initial_count:
        removed_count = initial_count - filtered_count
        removed_datasets = set(results_df['Dataset'].unique()) - set(active_datasets)
        print(f"Filtered out {removed_count} results from inactive datasets: {sorted(removed_datasets)}")
    
    print(f"Using {filtered_count} results from active datasets")
    return filtered_results

def filter_quality_results(results_df):
    """Filter out results with quality issues (NaN values or zero error metrics)"""
    
    print(f"Input results: {len(results_df)} rows")
    
    # Check the new column names from forecast_stats.py and forecast_neural.py output
    error_columns = ['MASE', 'RMSE']
    available_columns = [col for col in error_columns if col in results_df.columns]

    if not available_columns:
        print("Warning: No MASE or RMSE columns found for quality filtering")
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
    
    # Load models config using centralized function
    models_config = load_models_config()
    all_models = list(models_config.keys())
    print(f"Found {len(all_models)} models in config")
    
    # Get datasets from active datasets in config (not filesystem)
    all_datasets = get_active_dataset_names()
    print(f"Found {len(all_datasets)} active datasets in config")
    
    error_metrics_dir = FORECAST3_DIR / "error_metrics"
    if not error_metrics_dir.exists():
        print(f"Error: Error metrics directory not found at {error_metrics_dir}")
        return None
    
    # Load the assembled results for comparison
    results_file = FORECAST3_DIR / "results_all.csv"
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
                    error_columns = ['MASE', 'RMSE']
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
    quality_csv = FORECAST3_DIR / "quality_summary_detailed.csv"
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
    quality_pivot_csv = FORECAST3_DIR / "quality_summary_pivot.csv"
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
    
    quality_tex = FORECAST3_DIR / "quality_summary.tex"
    with open(quality_tex, 'w') as f:
        f.write(latex_summary)
    print(f"Saved quality summary (LaTeX) to: {quality_tex}")
    
    # Create tabular-only version for quality summary
    quality_tabular_full = summary_stats.to_latex(
        index=False,
        float_format="%.1f",
        escape=False
    )
    quality_tabular = extract_tabular_content(quality_tabular_full)
    
    quality_tabular_tex = FORECAST3_DIR / "quality_summary_tabular.tex"
    with open(quality_tabular_tex, 'w') as f:
        f.write(f"% Quality Summary - tabular content only\n% Generated automatically by create_results_tables2.py\n{quality_tabular}")
    print(f"Saved quality summary tabular (LaTeX) to: {quality_tabular_tex}")
    
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
    model_csv = FORECAST3_DIR / "model_failure_analysis.csv"
    model_analysis.to_csv(model_csv)
    print(f"Saved model failure analysis to: {model_csv}")
    
    # Create LaTeX version for model analysis
    model_latex = model_analysis.to_latex(
        caption="Model Failure Analysis: Success and Failure Rates by Model",
        label="tab:model_failures",
        float_format="%.1f",
        column_format='l' + 'r' * len(model_analysis.columns)
    )
    
    model_tex = FORECAST3_DIR / "model_failure_analysis.tex"
    with open(model_tex, 'w') as f:
        f.write(model_latex)
    print(f"Saved model failure analysis (LaTeX) to: {model_tex}")
    
    # Create tabular-only version for model analysis
    model_tabular_full = model_analysis.to_latex(
        float_format="%.1f",
        column_format='l' + 'r' * len(model_analysis.columns),
        escape=False
    )
    model_tabular = extract_tabular_content(model_tabular_full)
    
    model_tabular_tex = FORECAST3_DIR / "model_failure_analysis_tabular.tex"
    with open(model_tabular_tex, 'w') as f:
        f.write(f"% Model Failure Analysis - tabular content only\n% Generated automatically by create_results_tables2.py\n{model_tabular}")
    print(f"Saved model failure analysis tabular (LaTeX) to: {model_tabular_tex}")
    
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
    dataset_csv = FORECAST3_DIR / "dataset_failure_analysis.csv"
    dataset_analysis.to_csv(dataset_csv)
    print(f"Saved dataset failure analysis to: {dataset_csv}")
    
    # Create LaTeX version for dataset analysis
    dataset_latex = dataset_analysis.to_latex(
        caption="Dataset Failure Analysis: Success and Failure Rates by Dataset",
        label="tab:dataset_failures",
        float_format="%.1f",
        column_format='l' + 'r' * len(dataset_analysis.columns)
    )
    
    dataset_tex = FORECAST3_DIR / "dataset_failure_analysis.tex"
    with open(dataset_tex, 'w') as f:
        f.write(dataset_latex)
    print(f"Saved dataset failure analysis (LaTeX) to: {dataset_tex}")
    
    # Create tabular-only version for dataset analysis
    dataset_tabular_full = dataset_analysis.to_latex(
        float_format="%.1f",
        column_format='l' + 'r' * len(dataset_analysis.columns),
        escape=False
    )
    dataset_tabular = extract_tabular_content(dataset_tabular_full)
    
    dataset_tabular_tex = FORECAST3_DIR / "dataset_failure_analysis_tabular.tex"
    with open(dataset_tabular_tex, 'w') as f:
        f.write(f"% Dataset Failure Analysis - tabular content only\n% Generated automatically by create_results_tables2.py\n{dataset_tabular}")
    print(f"Saved dataset failure analysis tabular (LaTeX) to: {dataset_tabular_tex}")
    
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
    results_file = FORECAST3_DIR / "results_all.csv"
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
    
    # Filter to only include active models from config
    results = filter_results_by_active_models(results)
    
    # Filter to only include active datasets from config
    results = filter_results_by_active_datasets(results)
    
    # Apply quality filtering
    results = filter_quality_results(results)
    
    # Check if we have the required columns (new column names)
    if 'MASE' not in results.columns:
        print("Error: MASE column not found in results")
        print(f"Available columns: {list(results.columns)}")
        sys.exit(1)

    # Create pivot table: datasets as rows, models as columns, values as MASE
    mase_pivot = results.pivot_table(
        index='Dataset_Short',  # Short dataset names as rows
        columns='Model',  # Models as columns (display name)
        values='MASE',  # Changed from 'Global_MASE' to 'MASE'
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
    
    # Apply grouped dataset ordering (same as LaTeX tables)
    dataset_groups, dataset_table_names = load_dataset_groups_and_names()
    mase_pivot = apply_grouped_dataset_ordering(mase_pivot, dataset_groups, dataset_table_names)
    
    # Save as CSV for inspection
    csv_file = FORECAST3_DIR / "mase_pivot_table.csv"
    mase_pivot.to_csv(csv_file)
    print(f"Saved MASE pivot table (CSV) to: {csv_file}")
    
    # Save also to docs_src for easier access
    docs_csv_file = Path(__file__).parent.parent / "docs_src" / "mase_pivot_table.csv"
    docs_csv_file.parent.mkdir(parents=True, exist_ok=True)
    mase_pivot.to_csv(docs_csv_file)
    print(f"Saved MASE pivot table (CSV) to: {docs_csv_file}")
    
    # Convert to LaTeX table
    latex_output = create_latex_table(mase_pivot, "MASE Results by Dataset and Model", "tab:mase_results")
    latex_tabular_output = create_latex_tabular_only(mase_pivot, "MASE Results by Dataset and Model", "tab:mase_results")
    
    # Save LaTeX version to docs_src as well
    docs_tex_file = Path(__file__).parent.parent / "docs_src" / "mase_pivot_table.tex"
    with open(docs_tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved MASE pivot table (LaTeX) to: {docs_tex_file}")
    
    # Save tabular-only version to docs_src
    docs_tabular_file = Path(__file__).parent.parent / "docs_src" / "mase_pivot_tabular.tex"
    with open(docs_tabular_file, 'w') as f:
        f.write(latex_tabular_output)
    print(f"Saved MASE pivot tabular (LaTeX) to: {docs_tabular_file}")
    
    # Save as .tex file
    tex_file = FORECAST3_DIR / "mase_pivot_table.tex"
    with open(tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved MASE pivot table (LaTeX) to: {tex_file}")
    
    # Save tabular-only version
    tabular_file = FORECAST3_DIR / "mase_pivot_tabular.tex"
    with open(tabular_file, 'w') as f:
        f.write(latex_tabular_output)
    print(f"Saved MASE pivot tabular (LaTeX) to: {tabular_file}")
    
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
    results_file = FORECAST3_DIR / "results_all.csv"
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
    
    # Filter to only include active models from config
    results = filter_results_by_active_models(results)
    
    # Filter to only include active datasets from config
    results = filter_results_by_active_datasets(results)
    
    # Apply quality filtering
    results = filter_quality_results(results)
    
    # Check if we have the required columns
    if 'RMSE' not in results.columns:
        print("Error: RMSE column not found in results")
        print(f"Available columns: {list(results.columns)}")
        sys.exit(1)

    # Create pivot table: datasets as rows, models as columns, values as RMSE
    rmse_pivot = results.pivot_table(
        index='Dataset_Short',  # Short dataset names as rows
        columns='Model',  # Models as columns (display name)
        values='RMSE',
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
    
    # Apply grouped dataset ordering (same as LaTeX tables)
    dataset_groups, dataset_table_names = load_dataset_groups_and_names()
    rmse_pivot = apply_grouped_dataset_ordering(rmse_pivot, dataset_groups, dataset_table_names)
    
    # Save as CSV for inspection
    csv_file = FORECAST3_DIR / "rmse_pivot_table.csv"
    rmse_pivot.to_csv(csv_file)
    print(f"Saved RMSE pivot table (CSV) to: {csv_file}")
    
    # Save also to docs_src for easier access
    docs_csv_file = Path(__file__).parent.parent / "docs_src" / "rmse_pivot_table.csv"
    docs_csv_file.parent.mkdir(parents=True, exist_ok=True)
    rmse_pivot.to_csv(docs_csv_file)
    print(f"Saved RMSE pivot table (CSV) to: {docs_csv_file}")
    
    # Convert to LaTeX table
    latex_output = create_latex_table(rmse_pivot, "RMSE Results by Dataset and Model", "tab:rmse_results")
    latex_tabular_output = create_latex_tabular_only(rmse_pivot, "RMSE Results by Dataset and Model", "tab:rmse_results")
    
    # Save as .tex file
    tex_file = FORECAST3_DIR / "rmse_pivot_table.tex"
    with open(tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved RMSE pivot table (LaTeX) to: {tex_file}")
    
    # Save tabular-only version
    tabular_file = FORECAST3_DIR / "rmse_pivot_tabular.tex"
    with open(tabular_file, 'w') as f:
        f.write(latex_tabular_output)
    print(f"Saved RMSE pivot tabular (LaTeX) to: {tabular_file}")
    
    # Save LaTeX version to docs_src as well
    docs_tex_file = Path(__file__).parent.parent / "docs_src" / "rmse_pivot_table.tex"
    with open(docs_tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved RMSE pivot table (LaTeX) to: {docs_tex_file}")
    
    # Save tabular-only version to docs_src
    docs_tabular_file = Path(__file__).parent.parent / "docs_src" / "rmse_pivot_tabular.tex"
    with open(docs_tabular_file, 'w') as f:
        f.write(latex_tabular_output)
    print(f"Saved RMSE pivot tabular (LaTeX) to: {docs_tabular_file}")
    
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

# Note: sMAPE and MAE functions removed as they are not available in the new forecasting3 format

def create_relative_mase_pivot_table():
    """Create a pivot table with MASE values relative to Naive predictor: datasets as rows, models as columns"""
    
    print("Creating Relative MASE pivot table...")
    
    # Read the assembled results from new location
    results_file = FORECAST3_DIR / "results_all.csv"
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
    
    # Filter to only include active models from config
    results = filter_results_by_active_models(results)
    
    # Filter to only include active datasets from config
    results = filter_results_by_active_datasets(results)
    
    # Apply quality filtering
    results = filter_quality_results(results)
    
    # Check if we have the required columns and Naive model
    if 'MASE' not in results.columns:
        print("Error: MASE column not found in results")
        print(f"Available columns: {list(results.columns)}")
        sys.exit(1)
    
    if 'Naive' not in results['Model'].values:
        print("Error: Naive model not found in results")
        print(f"Available models: {sorted(results['Model'].unique())}")
        sys.exit(1)
    
    # Create pivot table: datasets as rows, models as columns, values as MASE
    mase_pivot = results.pivot_table(
        index='Dataset_Short',  # Short dataset names as rows
        columns='Model',  # Models as columns (display name)
        values='MASE',
        aggfunc='first'  # In case of duplicates, take the first value
    )
    
    print(f"Created initial pivot table with {len(mase_pivot)} datasets and {len(mase_pivot.columns)} models")
    
    # Check if Naive column exists in the pivot table
    if 'Naive' not in mase_pivot.columns:
        print("Error: Naive column not found in pivot table")
        print(f"Available columns: {list(mase_pivot.columns)}")
        sys.exit(1)
    
    # Create relative MASE table by dividing each model by Naive
    relative_mase_pivot = mase_pivot.copy()
    naive_values = mase_pivot['Naive']
    
    for col in mase_pivot.columns:
        if col != 'Naive':  # Don't divide Naive by itself
            relative_mase_pivot[col] = mase_pivot[col] / naive_values
    
    # Remove the Naive column since it would always be 1.0
    relative_mase_pivot = relative_mase_pivot.drop(columns=['Naive'])
    
    print(f"Created relative MASE table with {len(relative_mase_pivot)} datasets and {len(relative_mase_pivot.columns)} models")
    
    # Apply model ordering based on models_config.toml
    model_order = load_model_order()
    if model_order:
        # Create ordered list of display names that exist in the data (excluding Naive)
        ordered_display_names = [model['display_name'] for model in model_order if model['display_name'] != 'Naive']
        # Filter to only include columns that actually exist in the pivot table
        existing_ordered_columns = [col for col in ordered_display_names if col in relative_mase_pivot.columns]
        # Add any columns not in the config (shouldn't happen, but safety check)
        remaining_columns = [col for col in relative_mase_pivot.columns if col not in existing_ordered_columns]
        final_column_order = existing_ordered_columns + remaining_columns
        # Reorder the columns
        relative_mase_pivot = relative_mase_pivot.reindex(columns=final_column_order)
        print("Reordered model columns according to models_config.toml")
    
    # Apply grouped dataset ordering (same as LaTeX tables)
    dataset_groups, dataset_table_names = load_dataset_groups_and_names()
    relative_mase_pivot = apply_grouped_dataset_ordering(relative_mase_pivot, dataset_groups, dataset_table_names)
    
    # Save as CSV for inspection
    csv_file = FORECAST3_DIR / "relative_mase_pivot_table.csv"
    relative_mase_pivot.to_csv(csv_file)
    print(f"Saved Relative MASE pivot table (CSV) to: {csv_file}")
    
    # Save also to docs_src for easier access
    docs_csv_file = Path(__file__).parent.parent / "docs_src" / "relative_mase_pivot_table.csv"
    docs_csv_file.parent.mkdir(parents=True, exist_ok=True)
    relative_mase_pivot.to_csv(docs_csv_file)
    print(f"Saved Relative MASE pivot table (CSV) to: {docs_csv_file}")
    
    # Convert to LaTeX table
    latex_output = create_latex_table(relative_mase_pivot, "Relative MASE Results by Dataset and Model", "tab:relative_mase_results")
    latex_tabular_output = create_latex_tabular_only(relative_mase_pivot, "Relative MASE Results by Dataset and Model", "tab:relative_mase_results")
    
    # Save LaTeX version to docs_src as well
    docs_tex_file = Path(__file__).parent.parent / "docs_src" / "relative_mase_pivot_table.tex"
    with open(docs_tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved Relative MASE pivot table (LaTeX) to: {docs_tex_file}")
    
    # Save tabular-only version to docs_src
    docs_tabular_file = Path(__file__).parent.parent / "docs_src" / "relative_mase_pivot_tabular.tex"
    with open(docs_tabular_file, 'w') as f:
        f.write(latex_tabular_output)
    print(f"Saved Relative MASE pivot tabular (LaTeX) to: {docs_tabular_file}")
    
    # Save as .tex file
    tex_file = FORECAST3_DIR / "relative_mase_pivot_table.tex"
    with open(tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved Relative MASE pivot table (LaTeX) to: {tex_file}")
    
    # Save tabular-only version
    tabular_file = FORECAST3_DIR / "relative_mase_pivot_tabular.tex"
    with open(tabular_file, 'w') as f:
        f.write(latex_tabular_output)
    print(f"Saved Relative MASE pivot tabular (LaTeX) to: {tabular_file}")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Number of datasets: {len(relative_mase_pivot)}")
    print(f"Number of models: {len(relative_mase_pivot.columns)}")
    
    # Count missing values
    total_cells = len(relative_mase_pivot) * len(relative_mase_pivot.columns)
    missing_cells = relative_mase_pivot.isna().sum().sum()
    print(f"Missing values: {missing_cells} out of {total_cells} ({missing_cells/total_cells*100:.1f}%)")
    
    # Performance statistics relative to Naive
    valid_data = relative_mase_pivot.dropna(how='all', axis=0)  # Remove rows with all NaN
    if not valid_data.empty:
        print("\nRelative Performance Statistics (compared to Naive baseline):")
        # Count how many models beat Naive (< 1.0) for each dataset
        better_than_naive_count = (valid_data < 1.0).sum(axis=1)
        print(f"Average models beating Naive per dataset: {better_than_naive_count.mean():.1f}")
        
        # Show best and worst performing models overall
        overall_performance = valid_data.mean()  # Average relative performance across datasets
        best_model = overall_performance.idxmin()
        worst_model = overall_performance.idxmax()
        print(f"Best overall model: {best_model} (avg ratio: {overall_performance[best_model]:.3f})")
        print(f"Worst overall model: {worst_model} (avg ratio: {overall_performance[worst_model]:.3f})")
    
    if missing_cells > 0:
        print("\nDatasets with missing results:")
        for dataset in relative_mase_pivot.index:
            missing_count = relative_mase_pivot.loc[dataset].isna().sum()
            if missing_count > 0:
                print(f"  {dataset}: {missing_count} missing models")
    
    return relative_mase_pivot

def create_r2oos_pivot_table():
    """Create a pivot table with R2oos values: datasets as rows, models as columns"""

    print("Creating R2oos pivot table...")

    # Read the assembled results from new location
    results_file = FORECAST3_DIR / "results_all.csv"
    if not results_file.exists():
        print(f"Error: Results file not found at {results_file}")
        print("Please run the assemble_results3 task first")
        sys.exit(1)

    results = pd.read_csv(results_file)
    print(f"Loaded {len(results)} result rows")

    # Load dataset short names and apply to results
    dataset_short_names = load_dataset_short_names()
    results['Dataset_Short'] = results['Dataset'].map(dataset_short_names).fillna(results['Dataset'])

    # Rename model names for consistency
    results['Model'] = results['Model'].replace('AutoARIMA Fast', 'AutoARIMA')

    # Filter to only include active models from config
    results = filter_results_by_active_models(results)

    # Filter to only include active datasets from config
    results = filter_results_by_active_datasets(results)

    # Apply quality filtering
    results = filter_quality_results(results)

    # Check if we have the required columns
    if 'R2oos' not in results.columns:
        print("Warning: R2oos column not found in results, skipping R2oos table")
        return None

    # Create pivot table: datasets as rows, models as columns, values as R2oos
    r2oos_pivot = results.pivot_table(
        index='Dataset_Short',  # Short dataset names as rows
        columns='Model',  # Models as columns (display name)
        values='R2oos',
        aggfunc='first'  # In case of duplicates, take the first value
    )

    print(f"Created pivot table with {len(r2oos_pivot)} datasets and {len(r2oos_pivot.columns)} models")

    # Apply model ordering based on models_config.toml
    model_order = load_model_order()
    if model_order:
        # Create ordered list of display names that exist in the data
        ordered_display_names = [model['display_name'] for model in model_order]
        # Filter to only include columns that actually exist in the pivot table
        existing_ordered_columns = [col for col in ordered_display_names if col in r2oos_pivot.columns]
        # Add any columns not in the config (shouldn't happen, but safety check)
        remaining_columns = [col for col in r2oos_pivot.columns if col not in existing_ordered_columns]
        final_column_order = existing_ordered_columns + remaining_columns
        # Reorder the columns
        r2oos_pivot = r2oos_pivot.reindex(columns=final_column_order)
        print(f"Reordered model columns according to models_config.toml")

    # Apply grouped dataset ordering (same as LaTeX tables)
    dataset_groups, dataset_table_names = load_dataset_groups_and_names()
    r2oos_pivot = apply_grouped_dataset_ordering(r2oos_pivot, dataset_groups, dataset_table_names)

    # Save as CSV for inspection
    csv_file = FORECAST3_DIR / "r2oos_pivot_table.csv"
    r2oos_pivot.to_csv(csv_file)
    print(f"Saved R2oos pivot table (CSV) to: {csv_file}")

    # Save also to docs_src for easier access
    docs_csv_file = Path(__file__).parent.parent / "docs_src" / "r2oos_pivot_table.csv"
    docs_csv_file.parent.mkdir(parents=True, exist_ok=True)
    r2oos_pivot.to_csv(docs_csv_file)
    print(f"Saved R2oos pivot table (CSV) to: {docs_csv_file}")

    # Convert to LaTeX table
    latex_output = create_latex_table(r2oos_pivot, "R2oos Results by Dataset and Model", "tab:r2oos_results")
    latex_tabular_output = create_latex_tabular_only(r2oos_pivot, "R2oos Results by Dataset and Model", "tab:r2oos_results")

    # Save as .tex file
    tex_file = FORECAST3_DIR / "r2oos_pivot_table.tex"
    with open(tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved R2oos pivot table (LaTeX) to: {tex_file}")

    # Save tabular-only version
    tabular_file = FORECAST3_DIR / "r2oos_pivot_tabular.tex"
    with open(tabular_file, 'w') as f:
        f.write(latex_tabular_output)
    print(f"Saved R2oos pivot tabular (LaTeX) to: {tabular_file}")

    # Save LaTeX version to docs_src as well
    docs_tex_file = Path(__file__).parent.parent / "docs_src" / "r2oos_pivot_table.tex"
    with open(docs_tex_file, 'w') as f:
        f.write(latex_output)
    print(f"Saved R2oos pivot table (LaTeX) to: {docs_tex_file}")

    # Save tabular-only version to docs_src
    docs_tabular_file = Path(__file__).parent.parent / "docs_src" / "r2oos_pivot_tabular.tex"
    with open(docs_tabular_file, 'w') as f:
        f.write(latex_tabular_output)
    print(f"Saved R2oos pivot tabular (LaTeX) to: {docs_tabular_file}")

    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Number of datasets: {len(r2oos_pivot)}")
    print(f"Number of models: {len(r2oos_pivot.columns)}")

    # Count missing values
    total_cells = len(r2oos_pivot) * len(r2oos_pivot.columns)
    missing_cells = r2oos_pivot.isna().sum().sum()
    print(f"Missing values: {missing_cells} out of {total_cells} ({missing_cells/total_cells*100:.1f}%)")

    # Performance statistics for R2oos (higher is better)
    valid_data = r2oos_pivot.dropna(how='all', axis=0)  # Remove rows with all NaN
    if not valid_data.empty:
        print("\nR2oos Performance Statistics (higher is better):")
        # Count how many models beat 0 (positive predictive value) for each dataset
        positive_r2_count = (valid_data > 0).sum(axis=1)
        print(f"Average models with positive R2oos per dataset: {positive_r2_count.mean():.1f}")

        # Show best and worst performing models overall
        overall_performance = valid_data.mean()  # Average R2oos across datasets
        best_model = overall_performance.idxmax()
        worst_model = overall_performance.idxmin()
        print(f"Best overall model: {best_model} (avg R2oos: {overall_performance[best_model]:.3f})")
        print(f"Worst overall model: {worst_model} (avg R2oos: {overall_performance[worst_model]:.3f})")

    if missing_cells > 0:
        print("\nDatasets with missing results:")
        for dataset in r2oos_pivot.index:
            missing_count = r2oos_pivot.loc[dataset].isna().sum()
            if missing_count > 0:
                print(f"  {dataset}: {missing_count} missing models")

    return r2oos_pivot

def create_sectioned_latex_table(df, caption, label="tab:mase_results"):
    """Create a LaTeX table with dataset grouping sections"""
    
    # Load dataset groups and table names
    group_mapping, table_name_mapping = load_dataset_groups_and_names()
    
    # Handle missing values by replacing NaN with --
    df_formatted = df.copy()
    df_original = df.copy()  # Keep original for comparison
    df_formatted = df_formatted.fillna('--')
    
    # Identify best performing models for each dataset (before formatting)
    # For R2oos, higher is better; for other metrics, lower is better
    is_r2oos = "R2oos" in caption or "R²" in caption

    best_models = {}
    for dataset in df_original.index:
        # Get numeric values only (exclude NaN values)
        row_values = df_original.loc[dataset]
        numeric_values = pd.to_numeric(row_values, errors='coerce')

        if not numeric_values.isna().all():  # If we have any valid numbers
            if is_r2oos:
                # For R2oos, higher is better
                best_value = numeric_values.max()
                best_model_cols = numeric_values[numeric_values == best_value].index.tolist()
            else:
                # For other metrics, lower is better
                best_value = numeric_values.min()
                best_model_cols = numeric_values[numeric_values == best_value].index.tolist()
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
    note_text = "Values show {metric_name}. Lower values indicate better performance. -- indicates missing results."
    
    if "Relative MASE" in caption:
        metric_name = "MASE relative to Naive baseline"
        note_text = "Values show MASE ratios relative to the Naive baseline. Values $<$ 1.0 indicate better performance than Naive."
    elif "R2oos" in caption:
        metric_name = "Out-of-Sample R-squared (R²oos)"
        note_text = "Values show out-of-sample R-squared. Higher values indicate better performance. Negative values indicate worse performance than historical mean."
    elif "MASE" in caption:
        metric_name = "Mean Absolute Scaled Error (MASE)"
    elif "RMSE" in caption:
        metric_name = "Root Mean Square Error (RMSE)"
    elif "sMAPE" in caption:
        metric_name = "Symmetric Mean Absolute Percentage Error (sMAPE)"
    elif "MAE" in caption:
        metric_name = "Mean Absolute Error (MAE)"
    
    # Format note_text with metric_name if not already formatted
    if "Relative MASE" not in caption and "R2oos" not in caption:
        note_text = note_text.format(metric_name=metric_name)
    
    # Build complete tabular environment
    # Reduce spacing between columns for better fit
    column_format = '@{}l' + 'r' * num_cols + '@{}'
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
\\setlength{{\\tabcolsep}}{{1.5pt}}
\\renewcommand{{\\arraystretch}}{{0.9}}
{full_tabular}
\\vspace{{0.1cm}}

\\noindent {{\\scriptsize \\textbf{{Note:}} {note_text}}}
\\end{{table}}
"""
    
    return latex_formatted

def extract_tabular_content(latex_output):
    """Extract just the tabular content from a full LaTeX table"""
    import re
    
    # Find the tabular environment content
    tabular_match = re.search(r'\\begin\{tabular\}.*?\\end\{tabular\}', latex_output, re.DOTALL)
    if tabular_match:
        return tabular_match.group(0)
    else:
        return latex_output

def create_latex_tabular_only(df, caption, label="tab:mase_results", use_table_names=True):
    """Create only the tabular content without table environment for embedding in LaTeX documents"""
    
    # Create sectioned table
    tabular_content, header, num_cols = create_sectioned_latex_table(df, caption, label)
    
    # Build only tabular environment
    column_format = '@{}l' + 'r' * num_cols + '@{}'
    tabular_only = f"""% {caption} - tabular content only
% Generated automatically by create_results_tables2.py
\\scriptsize
\\setlength{{\\tabcolsep}}{{1.5pt}}
\\renewcommand{{\\arraystretch}}{{0.9}}
\\begin{{tabular}}{{{column_format}}}
\\toprule
{header}\\midrule
{tabular_content}\\bottomrule
\\end{{tabular}}"""
    
    return tabular_only

def apply_grouped_dataset_ordering(pivot_data, dataset_groups, dataset_table_names):
    """Apply the same grouped dataset ordering used in LaTeX tables to the pivot data"""
    
    # Create reverse mapping from table names back to full dataset names
    table_to_full_name = {}
    for full_name, table_name in dataset_table_names.items():
        table_to_full_name[table_name] = full_name
    
    # Map dataset table names (used in pivot_data index) to groups
    dataset_index_groups = {}
    for dataset_table_name in pivot_data.index:
        # Find the corresponding full dataset name
        full_dataset = table_to_full_name.get(dataset_table_name)
        if full_dataset and full_dataset in dataset_groups:
            group = dataset_groups[full_dataset]
        else:
            group = 'other'
        dataset_index_groups[dataset_table_name] = group
    
    # Define group order (same as LaTeX tables)
    group_order = ['basis_spreads', 'returns_portfolios', 'returns_disaggregated', 'other']
    
    # Group datasets by their categories
    grouped_datasets = {}
    for group in group_order:
        grouped_datasets[group] = []
    
    for dataset in pivot_data.index:
        group = dataset_index_groups[dataset]
        if group in grouped_datasets:
            grouped_datasets[group].append(dataset)
    
    # Create ordered list of datasets (alphabetically sorted within each group)
    ordered_datasets = []
    for group in group_order:
        datasets = grouped_datasets[group]
        if datasets:
            # Sort datasets alphabetically within each group
            ordered_datasets.extend(sorted(datasets))
    
    # Reorder the pivot data to match the grouped ordering
    pivot_data = pivot_data.reindex(index=ordered_datasets)
    
    return pivot_data

def create_heatmap_plots():
    """Create heatmap plots for all error metrics using the same data structure as tables"""
    
    print("\nCreating heatmap plots for error metrics...")
    
    # Read the assembled results
    results_file = FORECAST3_DIR / "results_all.csv"
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
    
    # Filter to only include active models from config
    results = filter_results_by_active_models(results)
    
    # Filter to only include active datasets from config
    results = filter_results_by_active_datasets(results)
    
    # Apply quality filtering
    results = filter_quality_results(results)
    
    # Define error metrics to create heatmaps for
    error_metrics = [
        ('MASE', 'MASE', 'mase_heatmap.png', 'Mean Absolute Scaled Error (MASE)'),
        ('RMSE', 'RMSE', 'rmse_heatmap.png', 'Root Mean Square Error (RMSE)'),
        ('R2oos', 'R2oos', 'r2oos_heatmap.png', 'Out-of-Sample R-squared (R²oos)'),
        ('Relative_MASE', 'Relative MASE', 'relative_mase_heatmap.png', 'Relative MASE (vs Naive Baseline)')
    ]
    
    for metric_col, metric_short, filename, metric_long in error_metrics:
        # Special handling for Relative MASE
        if metric_col == 'Relative_MASE':
            if 'MASE' not in results.columns:
                print(f"Skipping {metric_short} heatmap - MASE column not found")
                continue
            if 'Naive' not in results['Model'].values:
                print(f"Skipping {metric_short} heatmap - Naive model not found")
                continue
        elif metric_col not in results.columns:
            print(f"Skipping {metric_short} heatmap - column {metric_col} not found")
            continue
            
        print(f"Creating {metric_short} heatmap...")
        
        # Create pivot table (same structure as LaTeX tables)
        if metric_col == 'Relative_MASE':
            # For relative MASE, use MASE and calculate relative values
            pivot_data = results.pivot_table(
                index='Dataset_Short',
                columns='Model',
                values='MASE',
                aggfunc='mean'
            )
            
            # Check if Naive column exists in the pivot table
            if 'Naive' not in pivot_data.columns:
                print(f"Skipping {metric_short} heatmap - Naive column not found in pivot table")
                continue
            
            # Calculate relative MASE by dividing each model by Naive
            naive_values = pivot_data['Naive']
            for col in pivot_data.columns:
                if col != 'Naive':  # Don't divide Naive by itself
                    pivot_data[col] = pivot_data[col] / naive_values
            
            # Remove the Naive column since it would always be 1.0
            pivot_data = pivot_data.drop(columns=['Naive'])
        else:
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
            if metric_col == 'Relative_MASE':
                # Exclude Naive for relative MASE since it was removed
                ordered_display_names = [model['display_name'] for model in model_order if model['display_name'] != 'Naive']
            else:
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
        
        # Apply grouped dataset ordering (same as LaTeX tables)
        pivot_data = apply_grouped_dataset_ordering(pivot_data, dataset_groups, dataset_table_names)
        
        # Create the heatmap with increased size for better readability
        plt.figure(figsize=(18, 12))
        
        # Prepare data for heatmap (handle missing values)
        heatmap_data = pivot_data.copy()
        
        # Mask missing values and extreme outliers (999.0)
        mask = (heatmap_data.isna()) | (heatmap_data >= 999.0)
        
        # Color scheme and scaling depends on metric type
        if metric_col == 'Relative_MASE':
            # For relative MASE, use diverging colormap centered at 1.0 (equal to naive)
            # RdBu_r: Red for worse than naive (>1), White near 1, Blue for better than naive (<1)
            colormap = 'RdBu_r'
        elif metric_col == 'R2oos':
            # For R2oos, use diverging colormap centered at 0.0 (no predictive power)
            # RdBu: Red for negative (worse than mean), White near 0, Blue for positive (better than mean)
            colormap = 'RdBu'

            # Calculate color scale limits centered around 0.0
            if not heatmap_data.empty:
                # Get min and max values
                data_min = heatmap_data.min().min()
                data_max = heatmap_data.max().max()

                # For diverging colormap around 0, use symmetric bounds
                max_abs = max(abs(data_min), abs(data_max))

                # Cap extreme values to keep the scale reasonable
                max_abs = min(max_abs, 1.0)  # Most R2oos values should be between -1 and 1

                vmin_val = -max_abs
                vmax_val = max_abs
        elif metric_col == 'Relative_MASE':
            # Calculate color scale limits centered around 1.0
            if not heatmap_data.empty:
                # Get min and max values
                data_min = heatmap_data.min().min()
                data_max = heatmap_data.quantile(0.95).max()  # Use 95th percentile to handle outliers

                # For diverging colormap, we need to ensure 1.0 is at the center
                # Calculate deviations from 1.0
                min_deviation = abs(1.0 - data_min)
                max_deviation = abs(data_max - 1.0)

                # Use the larger deviation to create symmetric bounds around 1.0
                max_dev = max(min_deviation, max_deviation)

                # Cap extreme deviations to keep the scale reasonable
                max_dev = min(max_dev, 4.0)  # Don't go beyond 4x deviation from 1.0

                vmin_val = 1.0 - max_dev
                vmax_val = 1.0 + max_dev

                # Ensure we don't go below 0 for relative values
                if vmin_val < 0:
                    vmin_val = 0.0
                    vmax_val = 2.0  # Keep 1.0 as center between 0 and 2
            else:
                vmin_val = 0.5
                vmax_val = 1.5
        else:
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
        # Initialize annotation data as object dtype to avoid dtype warnings
        annot_data = pd.DataFrame(index=heatmap_data.index, columns=heatmap_data.columns, dtype=object)
        
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
                    else:
                        annot_data.iloc[i, j] = ""
                else:
                    annot_data.iloc[i, j] = ""
        
        # Create colorbar label and title based on metric type
        if metric_col == 'Relative_MASE':
            cbar_label = f'{metric_long} (1.0 = Equal to Naive, <1.0 = Better, >1.0 = Worse)'
            title_subtitle = '(Blue = Better than Naive, White ≈ Equal, Red = Worse than Naive)'
        elif metric_col == 'R2oos':
            cbar_label = f'{metric_long} (0.0 = No predictive power, >0.0 = Better than mean)'
            title_subtitle = '(Blue = Better than mean, White ≈ No predictive power, Red = Worse than mean)'
        else:
            cbar_label = f'{metric_long} (colors capped at 90th percentile)'
            title_subtitle = '(Lower values indicate better performance)'
        
        # Create the heatmap with improved scaling and larger fonts
        sns.heatmap(
            heatmap_data,
            mask=mask,
            annot=annot_data,
            fmt='',  # Use empty format since we're providing pre-formatted annotations
            cmap=colormap,
            cbar_kws={'label': cbar_label, 'shrink': 0.8},
            square=False,
            linewidths=0.5,
            annot_kws={'size': 10, 'weight': 'bold'},  # Increased font size and made bold
            vmin=vmin_val,
            vmax=vmax_val
        )
        
        plt.title(f'{metric_long} by Dataset and Model\n{title_subtitle}', 
                 fontsize=20, fontweight='bold', pad=25)
        plt.xlabel('Forecasting Models', fontsize=16, fontweight='bold')
        plt.ylabel('Datasets', fontsize=16, fontweight='bold')
        
        # Rotate x-axis labels for better readability with larger fonts
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.yticks(rotation=0, fontsize=12)
        
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
        
        # Save the heatmap with higher resolution
        output_file = FORECAST3_DIR / filename
        plt.savefig(output_file, dpi=600, bbox_inches='tight', facecolor='white', 
                   edgecolor='none', pad_inches=0.1)
        print(f"Saved heatmap to: {output_file}")
        
        plt.close()  # Close the figure to free memory
    
    print("Heatmap creation completed!")

def create_summary_statistics():
    """Create summary statistics table"""
    
    print("\nCreating summary statistics...")
    
    results_file = FORECAST3_DIR / "results_all.csv"
    results = pd.read_csv(results_file)
    
    # Filter to only include active models from config
    results = filter_results_by_active_models(results)
    
    # Filter to only include active datasets from config
    results = filter_results_by_active_datasets(results)
    
    # Apply quality filtering
    results = filter_quality_results(results)
    
    # Summary by model (using new column names)
    model_summary = results.groupby('Model').agg({
        'MASE': ['count', 'mean', 'std', 'min', 'max'],
        'Dataset': 'nunique'
    }).round(3)
    
    # Flatten column names
    model_summary.columns = ['N_Datasets', 'MASE_Avg', 'MASE_Std', 'MASE_Min', 'MASE_Max', 'N_Datasets_Check']
    model_summary = model_summary.drop('N_Datasets_Check', axis=1)
    
    # Add additional metrics if available
    if 'R2oos' in results.columns:
        r2oos_summary = results.groupby('Model')['R2oos'].agg(['mean', 'std']).round(3)
        r2oos_summary.columns = ['R2oos_Avg', 'R2oos_Std']
        model_summary = model_summary.join(r2oos_summary)
    
    if 'Forecast_Time_seconds' in results.columns:
        time_summary = results.groupby('Model')['Forecast_Time_seconds'].agg(['mean', 'sum']).round(2)
        time_summary.columns = ['Time_Avg_s', 'Time_Total_s']
        model_summary = model_summary.join(time_summary)
    
    # Save summary
    summary_file = FORECAST3_DIR / "model_summary_statistics.csv"
    model_summary.to_csv(summary_file)
    print(f"Saved model summary statistics to: {summary_file}")
    
    # Create LaTeX version
    summary_latex = model_summary.to_latex(
        caption="Summary Statistics by Model",
        label="tab:model_summary",
        float_format="%.3f",
        column_format='l' + 'r' * len(model_summary.columns)
    )
    
    summary_tex_file = FORECAST3_DIR / "model_summary_statistics.tex"
    with open(summary_tex_file, 'w') as f:
        f.write(summary_latex)
    print(f"Saved model summary statistics (LaTeX) to: {summary_tex_file}")
    
    # Create tabular-only version
    summary_tabular_full = model_summary.to_latex(
        float_format="%.3f",
        column_format='l' + 'r' * len(model_summary.columns),
        escape=False
    )
    summary_tabular = extract_tabular_content(summary_tabular_full)
    
    summary_tabular_tex_file = FORECAST3_DIR / "model_summary_statistics_tabular.tex"
    with open(summary_tabular_tex_file, 'w') as f:
        f.write(f"% Model Summary Statistics - tabular content only\n% Generated automatically by create_results_tables2.py\n{summary_tabular}")
    print(f"Saved model summary statistics tabular (LaTeX) to: {summary_tabular_tex_file}")
    
    return model_summary

def create_slurm_job_summary():
    """Create summary of SLURM job execution results"""
    
    print("\nCreating SLURM job summary...")
    
    logs_dir = OUTPUT_DIR / "forecasting3" / "logs"
    
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
    
    print("SLURM Job Summary:")
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
    summary_csv = FORECAST3_DIR / "slurm_job_summary.csv"
    summary_df.to_csv(summary_csv, index=False)
    print(f"Saved SLURM job summary to: {summary_csv}")
    
    return summary_df

if __name__ == "__main__":
    print("Creating results tables for new forecasting system...")
    
    # Create output directory if it doesn't exist
    FORECAST3_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create quality summary first
    quality_summary = create_quality_summary()
    
    # Create failure analysis reports
    model_failures, dataset_failures = create_failure_analysis(quality_summary)
    
    # Create the main MASE pivot table (now with quality filtering)
    mase_table = create_mase_pivot_table()
    
    # Create RMSE pivot table
    rmse_table = create_rmse_pivot_table()

    # Create R2oos pivot table (new metric)
    r2oos_table = create_r2oos_pivot_table()

    # Create relative MASE pivot table (comparing to Naive baseline)
    relative_mase_table = create_relative_mase_pivot_table()
    
    # Create summary statistics (now with quality filtering)
    summary_stats = create_summary_statistics()
    
    # Create SLURM job summary if applicable
    slurm_summary = create_slurm_job_summary()
    
    # Create heatmap plots for all error metrics
    create_heatmap_plots()
    
    print("\nResults table creation completed!")
    print("\nFiles created:")
    print("Quality Analysis:")
    print(f"  - {FORECAST3_DIR / 'quality_summary_detailed.csv'}")
    print(f"  - {FORECAST3_DIR / 'quality_summary_pivot.csv'}")
    print(f"  - {FORECAST3_DIR / 'quality_summary.tex'}")
    print(f"  - {FORECAST3_DIR / 'model_failure_analysis.csv'}")
    print(f"  - {FORECAST3_DIR / 'model_failure_analysis.tex'}")
    print(f"  - {FORECAST3_DIR / 'dataset_failure_analysis.csv'}")
    print(f"  - {FORECAST3_DIR / 'dataset_failure_analysis.tex'}")
    print("Main Tables (with quality filtering):")
    print(f"  - {FORECAST3_DIR / 'mase_pivot_table.csv'}")
    print(f"  - {FORECAST3_DIR / 'mase_pivot_table.tex'}")
    print(f"  - {FORECAST3_DIR / 'rmse_pivot_table.csv'}")
    print(f"  - {FORECAST3_DIR / 'rmse_pivot_table.tex'}")
    if r2oos_table is not None:
        print(f"  - {FORECAST3_DIR / 'r2oos_pivot_table.csv'}")
        print(f"  - {FORECAST3_DIR / 'r2oos_pivot_table.tex'}")
    print(f"  - {FORECAST3_DIR / 'relative_mase_pivot_table.csv'}")
    print(f"  - {FORECAST3_DIR / 'relative_mase_pivot_table.tex'}")
    print(f"  - {FORECAST3_DIR / 'model_summary_statistics.csv'}")
    print(f"  - {FORECAST3_DIR / 'model_summary_statistics.tex'}")
    if slurm_summary is not None:
        print("SLURM Job Analysis:")
        print(f"  - {FORECAST3_DIR / 'slurm_job_summary.csv'}")
    print("Additional Output (docs_src):")
    print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'mase_pivot_table.csv'}")
    print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'mase_pivot_table.tex'}")
    print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'rmse_pivot_table.csv'}")
    print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'rmse_pivot_table.tex'}")
    if r2oos_table is not None:
        print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'r2oos_pivot_table.csv'}")
        print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'r2oos_pivot_table.tex'}")
    print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'relative_mase_pivot_table.csv'}")
    print(f"  - {Path(__file__).parent.parent / 'docs_src' / 'relative_mase_pivot_table.tex'}")