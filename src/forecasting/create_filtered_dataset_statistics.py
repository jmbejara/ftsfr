"""
create_filtered_dataset_statistics.py

This script creates comprehensive dataset statistics tables showing the effects of
filtering applied in the forecasting system. It compares datasets before and after
the filtering logic from forecasting/forecast.py to show the actual impact on
entity counts and median time series lengths.

The output includes both CSV and LaTeX table formats grouped by dataset category.
"""

import sys
from pathlib import Path
import polars as pl
import tomli

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "forecasting"))

from settings import config

from forecast_utils import get_test_size_from_frequency
from robust_preprocessing import (
    normalize_month_end_dates,
    build_canonical_grid,
    split_train_test_aligned,
    get_data_requirements,
    filter_series_by_quality,
    add_gap_indicators,
    light_train_imputation,
)

# Configuration
DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))
FORECAST_DIR = OUTPUT_DIR / "forecasting"
PAPER_DIR = FORECAST_DIR / "paper"


def load_active_datasets():
    """Load active (uncommented) datasets from datasets.toml"""
    datasets_toml_path = Path(__file__).parent.parent.parent / "datasets.toml"

    if not datasets_toml_path.exists():
        raise FileNotFoundError(f"datasets.toml not found at {datasets_toml_path}")

    with open(datasets_toml_path, "rb") as f:
        datasets_config = tomli.load(f)

    # Extract active dataset information
    active_datasets = []

    for module_name, module_config in datasets_config.items():
        if isinstance(module_config, dict):
            # Look for dataset entries within each module
            for key, value in module_config.items():
                if isinstance(value, dict) and key.startswith("ftsfr_"):
                    # This is a dataset entry
                    dataset_info = {
                        "dataset_name": key,
                        "table_name": value.get("table_name", key),
                        "short_name": value.get("short_name", key),
                        "group": value.get("group", "other"),
                        "frequency": value.get("frequency", "ME"),
                        "seasonality": value.get("seasonality", 12),
                        "module_name": module_name,
                    }
                    active_datasets.append(dataset_info)

    print(f"Found {len(active_datasets)} active datasets in datasets.toml")
    return active_datasets


def simplify_frequency(freq_code):
    """
    Convert frequency codes to simplified labels

    Args:
        freq_code: Frequency code from datasets.toml (e.g., 'ME', 'B', 'D', 'QE')

    Returns:
        Simplified frequency label ('Daily', 'Monthly', 'Quarterly')
    """
    # Map frequency codes to simple labels
    freq_mapping = {
        "D": "Daily",  # Calendar day
        "B": "Daily",  # Business day
        "ME": "Monthly",  # Month end
        "MS": "Monthly",  # Month start
        "BME": "Monthly",  # Business month end
        "BMS": "Monthly",  # Business month start
        "QE": "Quarterly",  # Quarter end
        "QS": "Quarterly",  # Quarter start
        "BQE": "Quarterly",  # Business quarter end
        "BQS": "Quarterly",  # Business quarter start
    }

    return freq_mapping.get(freq_code, freq_code)  # Return original if not found


def format_date_range(min_date, max_date):
    """Format a date range for display in the table."""
    if min_date is None or max_date is None:
        return "N/A"

    min_str = min_date.strftime("%Y-%m-%d") if hasattr(min_date, "strftime") else str(min_date)
    max_str = max_date.strftime("%Y-%m-%d") if hasattr(max_date, "strftime") else str(max_date)
    return f"{min_str} -- {max_str}"


def calculate_filtering_statistics(dataset_info):
    """
    Calculate comprehensive statistics for a single dataset showing before/after filtering effects

    Args:
        dataset_info: Dictionary containing dataset metadata from TOML

    Returns:
        Dictionary containing all calculated statistics (before and after filtering)
    """
    dataset_name = dataset_info["dataset_name"]
    module_name = dataset_info["module_name"]

    # Construct path to parquet file in formatted directory
    dataset_path = DATA_DIR / "formatted" / module_name / f"{dataset_name}.parquet"

    if not dataset_path.exists():
        print(f"  Warning: Parquet file not found for {dataset_name} at {dataset_path}")
        return {
            "table_name": dataset_info["table_name"],
            "group": dataset_info["group"],
            "frequency": simplify_frequency(dataset_info["frequency"]),
            "entities_before": "N/A",
            "entities_after": "N/A",
            "median_length_before": "N/A",
            "median_length_after": "N/A",
            "min_date": "N/A",
            "max_date": "N/A",
            "error": f"File not found: {dataset_path}",
        }

    try:
        # Load the dataset with Polars
        df = pl.read_parquet(dataset_path)

        # Basic cleanup matching forecasting pipeline
        if "id" in df.columns:
            df = df.rename({"id": "unique_id"})
        drop_cols = [c for c in df.columns if c.startswith("__index_level_")]
        if drop_cols:
            df = df.drop(drop_cols)
        df = df.select(["unique_id", "ds", "y"])

        df = df.with_columns(pl.col("y").cast(pl.Float32))
        df = df.with_columns(
            pl.when((pl.col("y").is_infinite()) | (pl.col("y").is_nan()))
            .then(None)
            .otherwise(pl.col("y"))
            .alias("y")
        )

        frequency = dataset_info["frequency"]
        seasonality = dataset_info["seasonality"]
        test_size = get_test_size_from_frequency(frequency)

        # Baseline (pre-filter) statistics from cleaned raw data
        entities_before = df["unique_id"].n_unique()
        lengths_before = df.group_by("unique_id").agg(pl.len().alias("length"))["length"]
        median_length_before = lengths_before.median() if len(lengths_before) else 0
        min_date_before = df["ds"].min()
        max_date_before = df["ds"].max()

        # Reproduce robust preprocessing pipeline step-by-step to capture filtering impact
        df_normalized = normalize_month_end_dates(df, frequency)
        df_grid = build_canonical_grid(df_normalized, frequency)

        train_df, test_df = split_train_test_aligned(df_grid, test_size)

        requirements = get_data_requirements(frequency, test_size, seasonality)

        try:
            train_filtered, test_filtered, valid_series = filter_series_by_quality(
                train_df, test_df, requirements
            )
        except ValueError as ve:
            if "No series pass quality requirements" not in str(ve):
                raise
            # All series removed – capture before stats and return
            return {
                "table_name": dataset_info["table_name"],
                "group": dataset_info["group"],
                "frequency": simplify_frequency(frequency),
                "entities_before": int(entities_before),
                "entities_after": 0,
                "entities_removed": int(entities_before),
                "retention_pct": 0.0,
                "median_length_before": int(median_length_before)
                if median_length_before
                else 0,
                "median_length_after": 0,
                "min_required_obs": int(requirements["min_total_obs"]),
                "date_range": format_date_range(min_date_before, max_date_before),
                "error": None,
            }

        # Add gap indicators (matches forecasting pipeline) and apply imputation stage
        train_with_gaps = add_gap_indicators(train_filtered)
        test_with_gaps = add_gap_indicators(test_filtered)

        train_imputed = light_train_imputation(
            train_with_gaps, seasonality, method="forward_fill"
        )

        valid_series_after = train_imputed["unique_id"].unique()
        valid_series_list = valid_series_after.to_list()
        test_synced = test_with_gaps.filter(
            pl.col("unique_id").is_in(valid_series_list)
        )

        entities_after = len(valid_series_after)

        if entities_after == 0:
            median_length_after = 0
            date_range_after = "N/A"
        else:
            combined_after = pl.concat(
                [
                    train_imputed.select(["unique_id", "ds"]),
                    test_synced.select(["unique_id", "ds"]),
                ]
            )
            lengths_after = combined_after.group_by("unique_id").agg(
                pl.len().alias("length")
            )["length"]
            median_length_after = lengths_after.median() if len(lengths_after) else 0
            min_date_after = combined_after["ds"].min()
            max_date_after = combined_after["ds"].max()
            date_range_after = format_date_range(min_date_after, max_date_after)

        entities_removed = int(entities_before) - int(entities_after)
        retention_pct = (
            round((entities_after / entities_before) * 100, 1)
            if entities_before
            else 0.0
        )

        return {
            "table_name": dataset_info["table_name"],
            "group": dataset_info["group"],
            "frequency": simplify_frequency(frequency),
            "entities_before": int(entities_before),
            "entities_after": int(entities_after),
            "entities_removed": int(entities_removed),
            "retention_pct": retention_pct,
            "median_length_before": int(median_length_before)
            if median_length_before
            else 0,
            "median_length_after": int(median_length_after)
            if median_length_after
            else 0,
            "min_required_obs": int(requirements["min_total_obs"]),
            "date_range": date_range_after
            if entities_after
            else format_date_range(min_date_before, max_date_before),
            "error": None,
        }

    except Exception as e:
        print(f"  Error processing {dataset_name}: {str(e)}")
        return {
            "table_name": dataset_info["table_name"],
            "group": dataset_info["group"],
            "frequency": simplify_frequency(dataset_info["frequency"]),
            "entities_before": "Error",
            "entities_after": "Error",
            "entities_removed": "Error",
            "retention_pct": "Error",
            "median_length_before": "Error",
            "median_length_after": "Error",
            "min_required_obs": "Error",
            "date_range": "Error",
            "error": str(e),
        }


def group_datasets_by_category(stats_list):
    """Group datasets by their category and sort alphabetically within groups"""

    # Define group display names and order
    group_mapping = {
        "basis_spreads": "Basis Spreads",
        "returns_portfolios": "Returns (Portfolios)",
        "returns_disaggregated": "Returns (Disaggregated)",
        "other": "Other",
    }

    group_order = [
        "basis_spreads",
        "returns_portfolios",
        "returns_disaggregated",
        "other",
    ]

    # Group datasets
    grouped = {}
    for group_key in group_order:
        group_datasets = [stats for stats in stats_list if stats["group"] == group_key]
        if group_datasets:
            # Sort alphabetically by table name within each group
            group_datasets.sort(key=lambda x: x["table_name"])
            grouped[group_mapping[group_key]] = group_datasets

    return grouped


def create_latex_table(grouped_stats, output_path):
    """Create LaTeX table from grouped statistics showing before/after filtering"""

    latex_content = [
        "% Filtered Dataset Statistics Summary",
        "% Generated automatically by create_filtered_dataset_statistics.py",
        "",
        "\\begin{table}[htbp]",
        "\\centering",
        "\\caption{Dataset Statistics After Robust Forecasting Preprocessing}",
        "\\label{tab:filtered_dataset_stats}",
        "\\footnotesize",
        "\\setlength{\\tabcolsep}{1.0pt}",
        "\\renewcommand{\\arraystretch}{0.9}",
        "\\begin{tabular}{@{}llrrrrrrrl@{}}",
        "\\toprule",
        " & Frequency & \\begin{tabular}[c]{@{}r@{}}Entities\\\\Before\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Entities\\\\After\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Entities\\\\Removed\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Retention\\\\(\\%)\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Median Len\\\\Before\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Median Len\\\\After\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Min Req.\\\\Obs\\end{tabular} & Date Range \\\\",
        "\\midrule",
    ]

    for group_name, datasets in grouped_stats.items():
        # Add group header
        latex_content.append(
            f"\\multicolumn{{10}}{{l}}{{\\textbf{{{group_name}}}}} \\\\"
        )

        # Add datasets in this group
        for stats in datasets:
            row_data = [
                stats["table_name"],
                stats["frequency"],
                str(stats["entities_before"]),
                str(stats["entities_after"]),
                str(stats["entities_removed"]),
                f"{stats['retention_pct']:.1f}\\%",
                str(stats["median_length_before"]),
                str(stats["median_length_after"]),
                str(stats["min_required_obs"]),
                stats["date_range"],
            ]
            latex_content.append(" & ".join(row_data) + " \\\\")

        # Add midrule between groups (except after last group)
        if group_name != list(grouped_stats.keys())[-1]:
            latex_content.append("\\midrule")

    latex_content.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\vspace{0.1cm}",
            "\\begin{minipage}{\\textwidth}",
            "\\scriptsize",
            "\\textbf{Notes:} Statistics reflect the robust preprocessing pipeline used prior to model estimation. ",
            "Entities Before/After = unique time series counts before and after filtering; Entities Removed and Retention (\\%) highlight the impact of quality screens; ",
            "Median Len Before/After = median series length (train+test) in observations; Min Req. Obs = adaptive minimum total observations required by the pipeline. ",
            "Filtering enforces data-quality standards (variance, gap ratio, coverage) and consistent cleaning across models.",
            "\\end{minipage}",
            "\\end{table}",
        ]
    )

    with open(output_path, "w") as f:
        f.write("\n".join(latex_content))

    print(f"LaTeX table saved to: {output_path}")


def create_latex_tabular_only(grouped_stats, output_path):
    """Create only the tabular content without table environment for embedding in LaTeX documents"""

    latex_content = [
        "% Filtered Dataset Statistics Summary - tabular content only",
        "% Generated automatically by create_filtered_dataset_statistics.py",
        "\\footnotesize",
        "\\setlength{\\tabcolsep}{1.0pt}",
        "\\renewcommand{\\arraystretch}{0.9}",
        "\\begin{tabular}{@{}llrrrrrrrl@{}}",
        "\\toprule",
        " & Frequency & \\begin{tabular}[c]{@{}r@{}}Entities\\\\Before\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Entities\\\\After\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Entities\\\\Removed\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Retention\\\\(\\%)\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Median Len\\\\Before\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Median Len\\\\After\\end{tabular} & \\begin{tabular}[c]{@{}r@{}}Min Req.\\\\Obs\\end{tabular} & Date Range \\\\",
        "\\midrule",
    ]

    for group_name, datasets in grouped_stats.items():
        # Add group header
        latex_content.append(
            f"\\multicolumn{{10}}{{l}}{{\\textbf{{{group_name}}}}} \\\\"
        )

        # Add datasets in this group
        for stats in datasets:
            row_data = [
                stats["table_name"],
                stats["frequency"],
                str(stats["entities_before"]),
                str(stats["entities_after"]),
                str(stats["entities_removed"]),
                f"{stats['retention_pct']:.1f}\\%",
                str(stats["median_length_before"]),
                str(stats["median_length_after"]),
                str(stats["min_required_obs"]),
                stats["date_range"],
            ]
            latex_content.append(" & ".join(row_data) + " \\\\")

        # Add midrule between groups (except after last group)
        if group_name != list(grouped_stats.keys())[-1]:
            latex_content.append("\\midrule")

    latex_content.extend(["\\bottomrule", "\\end{tabular}"])

    with open(output_path, "w") as f:
        f.write("\n".join(latex_content))

    print(f"LaTeX tabular saved to: {output_path}")


def create_csv_table(stats_list, output_path):
    """Create CSV table from statistics using Polars"""

    # Convert to Polars DataFrame
    df = pl.DataFrame(stats_list)

    # Reorder columns
    column_order = [
        "table_name",
        "group",
        "frequency",
        "entities_before",
        "entities_after",
        "entities_removed",
        "retention_pct",
        "median_length_before",
        "median_length_after",
        "min_required_obs",
        "date_range",
    ]

    if "error" in df.columns:
        column_order.append("error")

    df = df.select(column_order)

    # Sort by group and table name
    group_order = [
        "basis_spreads",
        "returns_portfolios",
        "returns_disaggregated",
        "other",
    ]

    def group_sort_key(group):
        try:
            return group_order.index(group)
        except ValueError:
            return len(group_order)

    df = (
        df.with_columns(
            pl.col("group")
            .map_elements(group_sort_key, return_dtype=pl.Int64)
            .alias("group_sort")
        )
        .sort(["group_sort", "table_name"])
        .drop("group_sort")
    )

    # Save to CSV
    df.write_csv(output_path)
    print(f"CSV table saved to: {output_path}")

    return df


def main():
    """Main function to create filtered dataset statistics tables"""
    print("Creating filtered dataset statistics tables...")
    print("This shows the effects of filtering applied in the forecasting system.")

    # Ensure output directories exist
    FORECAST_DIR.mkdir(parents=True, exist_ok=True)
    PAPER_DIR.mkdir(parents=True, exist_ok=True)

    # Load active datasets from TOML
    active_datasets = load_active_datasets()

    if not active_datasets:
        print("No active datasets found in datasets.toml")
        return

    # Calculate filtering statistics for each dataset
    all_stats = []
    failed_datasets = []

    print("Calculating before/after filtering statistics for each dataset...")
    for dataset_info in active_datasets:
        print(f"  Processing {dataset_info['dataset_name']}...")
        stats = calculate_filtering_statistics(dataset_info)
        all_stats.append(stats)

        if stats.get("error"):
            failed_datasets.append(stats)
        else:
            # Print summary for this dataset
            entities_removed = stats["entities_before"] - stats["entities_after"]
            if stats["entities_after"] == 0:
                print(
                    f"    Entities: {stats['entities_before']} → 0 (ALL FILTERED OUT - series too short)"
                )
                print(
                    f"    Median length before: {stats['median_length_before']} (insufficient for forecasting)"
                )
            else:
                print(
                    f"    Entities: {stats['entities_before']} → {stats['entities_after']} ({entities_removed} removed)"
                )
                print(
                    f"    Median length: {stats['median_length_before']} → {stats['median_length_after']}"
                )

    print(f"\nProcessed {len(all_stats)} datasets")
    if failed_datasets:
        print(f"Failed to process {len(failed_datasets)} datasets:")
        for failed in failed_datasets:
            print(f"  - {failed['table_name']}: {failed['error']}")

    # Group datasets by category
    grouped_stats = group_datasets_by_category(all_stats)

    # Create output files
    base_filename = "filtered_dataset_statistics"

    # CSV files
    csv_path = PAPER_DIR / f"{base_filename}.csv"
    csv_forecast_path = (
        FORECAST_DIR / f"{base_filename}.csv"
    )  # Keep legacy location for compatibility

    df = create_csv_table(all_stats, csv_path)
    df.write_csv(csv_forecast_path)  # Copy to main forecasting directory

    # LaTeX files
    latex_path = PAPER_DIR / f"{base_filename}.tex"
    latex_forecast_path = (
        FORECAST_DIR / f"{base_filename}.tex"
    )  # Keep legacy location for compatibility
    latex_tabular_path = PAPER_DIR / f"{base_filename}_tabular.tex"

    create_latex_table(grouped_stats, latex_path)
    create_latex_tabular_only(grouped_stats, latex_tabular_path)

    # Copy LaTeX files to main forecasting directory for compatibility
    with open(latex_path, "r") as f:
        latex_content = f.read()
    with open(latex_forecast_path, "w") as f:
        f.write(latex_content)

    print("\nFiltered dataset statistics tables created successfully!")
    print("Files saved to:")
    print(f"  - {csv_path}")
    print(f"  - {csv_forecast_path}")
    print(f"  - {latex_path}")
    print(f"  - {latex_forecast_path}")
    print(f"  - {latex_tabular_path}")

    # Display summary
    print("\nSummary by group:")
    for group_name, datasets in grouped_stats.items():
        print(f"  {group_name}: {len(datasets)} datasets")

    # Display overall filtering impact
    total_entities_before = sum(
        s["entities_before"] for s in all_stats if isinstance(s["entities_before"], int)
    )
    total_entities_after = sum(
        s["entities_after"] for s in all_stats if isinstance(s["entities_after"], int)
    )
    total_removed = total_entities_before - total_entities_after

    print("\nOverall filtering impact:")
    print(f"  Total entities before filtering: {total_entities_before}")
    print(f"  Total entities after filtering: {total_entities_after}")
    print(f"  Total entities removed by filtering: {total_removed}")


if __name__ == "__main__":
    main()
