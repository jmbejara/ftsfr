"""
create_dataset_statistics.py

This script creates comprehensive dataset statistics tables for all active datasets
defined in datasets.toml. It calculates entity counts, time series lengths, 
unique timestamps, and date ranges including train/test split cutoff dates.

The output includes both CSV and LaTeX table formats grouped by dataset category.
"""

import sys
from pathlib import Path
import polars as pl
import tomli

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "models"))

from settings import config

# Configuration
DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))
FORECAST2_DIR = OUTPUT_DIR / "forecasting2"
DOCS_SRC_DIR = Path(__file__).parent.parent / "docs_src"


def load_active_datasets():
    """Load active (uncommented) datasets from datasets.toml"""
    datasets_toml_path = Path(__file__).parent.parent / "datasets.toml"
    
    if not datasets_toml_path.exists():
        raise FileNotFoundError(f"datasets.toml not found at {datasets_toml_path}")
    
    with open(datasets_toml_path, 'rb') as f:
        datasets_config = tomli.load(f)
    
    # Extract active dataset information
    active_datasets = []
    
    for module_name, module_config in datasets_config.items():
        if isinstance(module_config, dict):
            # Look for dataset entries within each module
            for key, value in module_config.items():
                if isinstance(value, dict) and key.startswith('ftsfr_'):
                    # This is a dataset entry
                    dataset_info = {
                        'dataset_name': key,
                        'table_name': value.get('table_name', key),
                        'short_name': value.get('short_name', key),
                        'group': value.get('group', 'other'),
                        'frequency': value.get('frequency', 'ME'),
                        'seasonality': value.get('seasonality', 12),
                        'module_name': module_name
                    }
                    active_datasets.append(dataset_info)
    
    print(f"Found {len(active_datasets)} active datasets in datasets.toml")
    return active_datasets


def calculate_train_test_split_cutoff(df, test_split=0.2):
    """
    Calculate the cutoff date for train/test split using Polars
    
    Args:
        df: Polars DataFrame with 'ds' (date) and 'unique_id' columns
        test_split: Fraction of data to use for testing (default 0.2)
        
    Returns:
        cutoff_date: The date that separates train and test data
    """
    # Get unique dates and sort them
    unique_dates = df.select('ds').unique().sort('ds')
    total_dates = len(unique_dates)
    
    # Calculate split point (80% train, 20% test)
    split_index = int(total_dates * (1 - test_split))
    
    # Get the cutoff date (first date in test set)
    cutoff_date = unique_dates.row(split_index)[0]
    
    return cutoff_date


def calculate_dataset_statistics(dataset_info):
    """
    Calculate comprehensive statistics for a single dataset using Polars
    
    Args:
        dataset_info: Dictionary containing dataset metadata from TOML
        
    Returns:
        Dictionary containing all calculated statistics
    """
    dataset_name = dataset_info['dataset_name']
    module_name = dataset_info['module_name']
    
    # Construct path to parquet file
    dataset_path = DATA_DIR / module_name / f"{dataset_name}.parquet"
    
    if not dataset_path.exists():
        print(f"  Warning: Parquet file not found for {dataset_name} at {dataset_path}")
        return {
            'table_name': dataset_info['table_name'],
            'group': dataset_info['group'],
            'unique_entities': 'N/A',
            'min_length': 'N/A',
            'median_length': 'N/A',
            'max_length': 'N/A',
            'unique_timestamps': 'N/A',
            'min_date': 'N/A',
            'cutoff_date': 'N/A',
            'max_date': 'N/A',
            'error': f'File not found: {dataset_path}'
        }
    
    try:
        # Load the dataset with Polars
        df = pl.read_parquet(dataset_path)
        
        # Identify date and identifier columns
        date_col = None
        id_col = None
        
        # Look for common date column names
        date_candidates = ['ds', 'date', 'time', 'timestamp']
        for col in date_candidates:
            if col in df.columns:
                date_col = col
                break
        
        # Look for common ID column names
        id_candidates = ['unique_id', 'id', 'entity_id', 'series_id']
        for col in id_candidates:
            if col in df.columns:
                id_col = col
                break
        
        # If we don't find standard columns, try to infer from data types
        if date_col is None:
            for col in df.columns:
                if df[col].dtype in [pl.Date, pl.Datetime]:
                    date_col = col
                    break
        
        if id_col is None:
            # Look for string columns that could be identifiers
            for col in df.columns:
                if df[col].dtype == pl.Utf8 and col != date_col:
                    id_col = col
                    break
        
        # If still no ID column, create one (assuming single time series)
        if id_col is None:
            df = df.with_columns(pl.lit("series_1").alias("unique_id"))
            id_col = "unique_id"
        
        # If no date column found, raise error
        if date_col is None:
            raise ValueError(f"Could not identify date column in {dataset_path}")
        
        # Ensure date column is properly typed
        if df[date_col].dtype not in [pl.Date, pl.Datetime]:
            df = df.with_columns(pl.col(date_col).str.to_datetime().alias(date_col))
        
        # Calculate basic date statistics
        min_date = df[date_col].min()
        max_date = df[date_col].max()
        
        # Calculate cutoff date for train/test split
        cutoff_date = calculate_train_test_split_cutoff(df.select([date_col, id_col]).rename({date_col: 'ds', id_col: 'unique_id'}))
        
        # Calculate entity and time series statistics
        unique_entities = df[id_col].n_unique()
        unique_timestamps = df[date_col].n_unique()
        
        # Calculate time series lengths per entity
        entity_lengths = (df
                         .group_by(id_col)
                         .agg(pl.len().alias('length'))
                         ['length'])
        
        min_length = entity_lengths.min()
        median_length = entity_lengths.median()
        max_length = entity_lengths.max()
        
        return {
            'table_name': dataset_info['table_name'],
            'group': dataset_info['group'],
            'unique_entities': int(unique_entities),
            'min_length': int(min_length),
            'median_length': int(median_length),
            'max_length': int(max_length),
            'unique_timestamps': int(unique_timestamps),
            'min_date': min_date.strftime('%Y-%m-%d') if min_date else 'N/A',
            'cutoff_date': cutoff_date.strftime('%Y-%m-%d') if cutoff_date else 'N/A',
            'max_date': max_date.strftime('%Y-%m-%d') if max_date else 'N/A',
            'error': None
        }
        
    except Exception as e:
        print(f"  Error processing {dataset_name}: {str(e)}")
        return {
            'table_name': dataset_info['table_name'],
            'group': dataset_info['group'],
            'unique_entities': 'Error',
            'min_length': 'Error',
            'median_length': 'Error',
            'max_length': 'Error',
            'unique_timestamps': 'Error',
            'min_date': 'Error',
            'cutoff_date': 'Error',
            'max_date': 'Error',
            'error': str(e)
        }


def group_datasets_by_category(stats_list):
    """Group datasets by their category and sort alphabetically within groups"""
    
    # Define group display names and order
    group_mapping = {
        'basis_spreads': 'Basis Spreads',
        'returns_portfolios': 'Returns (Portfolios)',
        'returns_disaggregated': 'Returns (Disaggregated)', 
        'other': 'Other'
    }
    
    group_order = ['basis_spreads', 'returns_portfolios', 'returns_disaggregated', 'other']
    
    # Group datasets
    grouped = {}
    for group_key in group_order:
        group_datasets = [stats for stats in stats_list if stats['group'] == group_key]
        if group_datasets:
            # Sort alphabetically by table name within each group
            group_datasets.sort(key=lambda x: x['table_name'])
            grouped[group_mapping[group_key]] = group_datasets
    
    return grouped


def create_latex_table(grouped_stats, output_path):
    """Create LaTeX table from grouped statistics"""
    
    latex_content = [
        "% Dataset Statistics Summary",
        "% Generated automatically by create_dataset_statistics.py",
        "",
        "\\begin{table}[htbp]",
        "\\centering",
        "\\caption{Dataset Statistics Summary}",
        "\\label{tab:dataset_stats}",
        "\\footnotesize",
        "\\setlength{\\tabcolsep}{1.2pt}",
        "\\renewcommand{\\arraystretch}{0.9}",
        "\\begin{tabular}{@{}lrrrrrlll@{}}",
        "\\toprule",
        " & \\begin{tabular}[c]{@{}r@{}}Unique\\\\Entities\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Min\\\\Length\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Median\\\\Length\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Max\\\\Length\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Unique\\\\Timestamps\\end{tabular} & Min Date & Cutoff Date & Max Date \\\\",
        "\\midrule"
    ]
    
    for group_name, datasets in grouped_stats.items():
        # Add group header
        latex_content.append(f"\\multicolumn{{9}}{{l}}{{\\textbf{{{group_name}}}}} \\\\")
        
        # Add datasets in this group
        for stats in datasets:
            row_data = [
                stats['table_name'],
                str(stats['unique_entities']),
                str(stats['min_length']),
                str(stats['median_length']),
                str(stats['max_length']),
                str(stats['unique_timestamps']),
                stats['min_date'],
                stats['cutoff_date'],
                stats['max_date']
            ]
            latex_content.append(" & ".join(row_data) + " \\\\")
        
        # Add midrule between groups (except after last group)
        if group_name != list(grouped_stats.keys())[-1]:
            latex_content.append("\\midrule")
    
    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\vspace{0.1cm}",
        "\\begin{minipage}{\\textwidth}",
        "\\scriptsize",
        "\\textbf{Notes:} Unique Entities = distinct time series identifiers; Min/Median/Max Length = time series lengths per entity; Unique Timestamps = distinct time observations; Cutoff Date = train/test split date (80\\%/20\\% split).",
        "\\end{minipage}",
        "\\end{table}"
    ])
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(latex_content))
    
    print(f"LaTeX table saved to: {output_path}")


def create_csv_table(stats_list, output_path):
    """Create CSV table from statistics using Polars"""
    
    # Convert to Polars DataFrame
    df = pl.DataFrame(stats_list)
    
    # Reorder columns
    column_order = [
        'table_name', 'group', 'unique_entities', 'min_length', 'median_length',
        'max_length', 'unique_timestamps', 'min_date', 'cutoff_date', 'max_date'
    ]
    
    if 'error' in df.columns:
        column_order.append('error')
    
    df = df.select(column_order)
    
    # Sort by group and table name
    group_order = ['basis_spreads', 'returns_portfolios', 'returns_disaggregated', 'other']
    
    def group_sort_key(group):
        try:
            return group_order.index(group)
        except ValueError:
            return len(group_order)
    
    df = df.with_columns(
        pl.col('group').map_elements(group_sort_key, return_dtype=pl.Int64).alias('group_sort')
    ).sort(['group_sort', 'table_name']).drop('group_sort')
    
    # Save to CSV
    df.write_csv(output_path)
    print(f"CSV table saved to: {output_path}")
    
    return df


def main():
    """Main function to create dataset statistics tables"""
    print("Creating dataset statistics tables...")
    
    # Ensure output directories exist
    FORECAST2_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_SRC_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load active datasets from TOML
    active_datasets = load_active_datasets()
    
    if not active_datasets:
        print("No active datasets found in datasets.toml")
        return
    
    # Calculate statistics for each dataset
    all_stats = []
    failed_datasets = []
    
    print("Calculating statistics for each dataset...")
    for dataset_info in active_datasets:
        print(f"  Processing {dataset_info['dataset_name']}...")
        stats = calculate_dataset_statistics(dataset_info)
        all_stats.append(stats)
        
        if stats.get('error'):
            failed_datasets.append(stats)
    
    print(f"\nProcessed {len(all_stats)} datasets")
    if failed_datasets:
        print(f"Failed to process {len(failed_datasets)} datasets:")
        for failed in failed_datasets:
            print(f"  - {failed['table_name']}: {failed['error']}")
    
    # Group datasets by category
    grouped_stats = group_datasets_by_category(all_stats)
    
    # Create output files
    base_filename = "dataset_statistics"
    
    # CSV files
    csv_forecast_path = FORECAST2_DIR / f"{base_filename}.csv"
    csv_docs_path = DOCS_SRC_DIR / f"{base_filename}.csv"
    
    df = create_csv_table(all_stats, csv_forecast_path)
    df.write_csv(csv_docs_path)  # Copy to docs_src
    
    # LaTeX files
    latex_forecast_path = FORECAST2_DIR / f"{base_filename}.tex"
    latex_docs_path = DOCS_SRC_DIR / f"{base_filename}.tex"
    
    create_latex_table(grouped_stats, latex_forecast_path)
    
    # Copy LaTeX file to docs_src
    with open(latex_forecast_path, 'r') as f:
        latex_content = f.read()
    with open(latex_docs_path, 'w') as f:
        f.write(latex_content)
    
    print(f"\nDataset statistics tables created successfully!")
    print(f"Files saved to:")
    print(f"  - {csv_forecast_path}")
    print(f"  - {csv_docs_path}")
    print(f"  - {latex_forecast_path}")
    print(f"  - {latex_docs_path}")
    
    # Display summary
    print(f"\nSummary by group:")
    for group_name, datasets in grouped_stats.items():
        print(f"  {group_name}: {len(datasets)} datasets")


if __name__ == "__main__":
    main()