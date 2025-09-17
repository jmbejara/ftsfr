"""
dodo_07_paper.py - Results assembly, report generation, and LaTeX compilation

This file contains all tasks related to:
- Assembling results from model runs
- Generating LaTeX documents and reports
- Converting PDFs to markdown
"""

# Import common utilities
from dodo_common import (
    DATA_DIR,
    OUTPUT_DIR,
    load_subscriptions,
    load_all_module_requirements,
    load_models_config,
)
from dependency_tracker import get_available_datasets
from pathlib import Path

# Load configuration
subscriptions_toml = load_subscriptions()

# Load models configuration to get available models
models_config = load_models_config()
models_activated = list(models_config.keys())

# Load module requirements to determine available datasets
module_requirements_dict = load_all_module_requirements()
module_requirements = {}
for module_name, required_sources in module_requirements_dict.items():
    module_requirements[module_name] = all(
        subscriptions_toml["data_sources"].get(source, False)
        for source in required_sources
    )


def check_forecast_results():
    """Check if forecast result files exist in the new forecasting3 structure"""
    error_metrics_dir = OUTPUT_DIR / "forecasting3" / "error_metrics"

    # if not error_metrics_dir.exists():
    #     print(
    #         f"\nWarning: No forecasting3 error metrics directory found at {error_metrics_dir}"
    #     )
    #     print(
    #         "Please run forecasting tasks first using the new forecast_stats.py and forecast_neural.py system"
    #     )
    #     return False

    available_datasets = get_available_datasets(module_requirements, DATA_DIR)

    # Count available vs expected results in the new structure: {dataset}/{model}.csv
    total_expected = len(models_activated) * len(available_datasets)
    results_found = 0

    for dataset_name in available_datasets:
        dataset_dir = error_metrics_dir / dataset_name
        if dataset_dir.exists():
            for model in models_activated:
                result_file = dataset_dir / f"{model}.csv"
                if result_file.exists():
                    results_found += 1

    if results_found < total_expected:
        missing_count = total_expected - results_found
        print(
            f"\nWarning: {missing_count} of {total_expected} expected result files are missing."
        )
        print(
            "Some models may have failed to run. Continuing with available results...\n"
        )
    else:
        print(f"\nAll {total_expected} expected result files found.\n")

    return results_found > 0  # Return True if we have any results at all


def task_assemble_results():
    """Assemble results from all model-dataset combinations using the new forecasting3 system."""
    import glob

    # Check for result files at task generation time
    check_forecast_results()

    # Get all CSV files in the forecasting3 error metrics directory
    error_metrics_csv_files = glob.glob(
        str(OUTPUT_DIR / "forecasting3" / "error_metrics" / "**" / "*.csv"),
        recursive=True,
    )

    return {
        "actions": [
            "python ./src/assemble_results3.py",
        ],
        "targets": [
            OUTPUT_DIR / "forecasting3" / "results_all.csv",
        ],
        "file_dep": [
            "./src/assemble_results3.py",
            *error_metrics_csv_files,
        ],
        "clean": True,
    }


def task_create_dataset_statistics():
    """Create dataset statistics table from active datasets in datasets.toml"""
    import glob
    
    # Get all parquet files from formatted directory only
    dataset_parquet_files = glob.glob(
        str(DATA_DIR / "formatted" / "**" / "ftsfr_*.parquet"),
        recursive=True,
    )
    
    return {
        "actions": [
            "python ./src/create_dataset_statistics.py",
        ],
        "targets": [
            # Dataset statistics table files
            Path("./docs_src") / "dataset_statistics.csv",
            Path("./docs_src") / "dataset_statistics.tex",
            OUTPUT_DIR / "forecasting3" / "dataset_statistics.csv",
            OUTPUT_DIR / "forecasting3" / "dataset_statistics.tex",
        ],
        "file_dep": [
            "./src/create_dataset_statistics.py",
            "./datasets.toml",  # Primary dependency - drives which datasets to include
            *dataset_parquet_files,  # Secondary dependencies - actual data files
        ],
        "clean": True,
    }


def task_create_filtered_dataset_statistics():
    """Create filtered dataset statistics table showing effects of forecasting system filtering"""
    import glob
    
    # Get all parquet files from formatted directory only
    dataset_parquet_files = glob.glob(
        str(DATA_DIR / "formatted" / "**" / "ftsfr_*.parquet"),
        recursive=True,
    )
    
    return {
        "actions": [
            "python ./src/create_filtered_dataset_statistics.py",
        ],
        "targets": [
            # Filtered dataset statistics table files
            Path("./docs_src") / "filtered_dataset_statistics.csv",
            Path("./docs_src") / "filtered_dataset_statistics.tex",
            OUTPUT_DIR / "forecasting3" / "filtered_dataset_statistics.csv",
            OUTPUT_DIR / "forecasting3" / "filtered_dataset_statistics.tex",
        ],
        "file_dep": [
            "./src/create_filtered_dataset_statistics.py",
            "./forecasting/forecast.py",  # Contains filtering logic we're applying
            "./datasets.toml",  # Primary dependency - drives which datasets to include
            *dataset_parquet_files,  # Secondary dependencies - actual data files
        ],
        "clean": True,
    }


def task_create_results_tables():
    """Create analytical tables from assembled results using forecasting3 system"""
    return {
        "actions": [
            "python ./src/create_results_tables2.py",
        ],
        "targets": [
            # MASE pivot table files
            Path("./docs_src") / "mase_pivot_table.csv",
            Path("./docs_src") / "mase_pivot_table.tex",
            OUTPUT_DIR / "forecasting3" / "mase_pivot_table.csv",
            OUTPUT_DIR / "forecasting3" / "mase_pivot_table.tex",
            # RMSE pivot table files
            Path("./docs_src") / "rmse_pivot_table.csv",
            Path("./docs_src") / "rmse_pivot_table.tex",
            OUTPUT_DIR / "forecasting3" / "rmse_pivot_table.csv",
            OUTPUT_DIR / "forecasting3" / "rmse_pivot_table.tex",
            # sMAPE pivot table files (conditional on data availability)
            Path("./docs_src") / "smape_pivot_table.csv",
            Path("./docs_src") / "smape_pivot_table.tex",
            OUTPUT_DIR / "forecasting3" / "smape_pivot_table.csv",
            OUTPUT_DIR / "forecasting3" / "smape_pivot_table.tex",
            # MAE pivot table files (conditional on data availability)
            Path("./docs_src") / "mae_pivot_table.csv",
            Path("./docs_src") / "mae_pivot_table.tex",
            OUTPUT_DIR / "forecasting3" / "mae_pivot_table.csv",
            OUTPUT_DIR / "forecasting3" / "mae_pivot_table.tex",
            # Relative MASE pivot table files (comparing to Naive baseline)
            Path("./docs_src") / "relative_mase_pivot_table.csv",
            Path("./docs_src") / "relative_mase_pivot_table.tex",
            OUTPUT_DIR / "forecasting3" / "relative_mase_pivot_table.csv",
            OUTPUT_DIR / "forecasting3" / "relative_mase_pivot_table.tex",
            # R2oos pivot table files (out-of-sample R-squared)
            Path("./docs_src") / "r2oos_pivot_table.csv",
            Path("./docs_src") / "r2oos_pivot_table.tex",
            OUTPUT_DIR / "forecasting3" / "r2oos_pivot_table.csv",
            OUTPUT_DIR / "forecasting3" / "r2oos_pivot_table.tex",
            # Summary statistics
            OUTPUT_DIR / "forecasting3" / "model_summary_statistics.csv",
            OUTPUT_DIR / "forecasting3" / "model_summary_statistics.tex",
            # Heatmap plots
            OUTPUT_DIR / "forecasting3" / "mase_heatmap.png",
            OUTPUT_DIR / "forecasting3" / "rmse_heatmap.png",
            OUTPUT_DIR / "forecasting3" / "smape_heatmap.png",
            OUTPUT_DIR / "forecasting3" / "mae_heatmap.png",
            OUTPUT_DIR / "forecasting3" / "r2oos_heatmap.png",
        ],
        "file_dep": [
            "./src/create_results_tables2.py",
            OUTPUT_DIR / "forecasting3" / "results_all.csv",
            "./forecasting/models_config.toml",  # Add dependency on models config for column ordering
            "./datasets.toml",  # Add dependency on datasets config for column ordering
        ],
        "clean": True,
    }


def task_run_ex_statsforecast():
    """Run the AutoARIMA tutorial example demonstrating the forecasting pipeline"""
    import glob
    
    # Get parquet files that the tutorial might use
    dataset_parquet_files = glob.glob(
        str(DATA_DIR / "formatted" / "**" / "ftsfr_french_portfolios_25_daily_size_and_bm.parquet"),
        recursive=True,
    )
    
    return {
        "actions": [
            "python ./forecasting/ex_statsforecast.py",
            "echo 'Tutorial completed successfully on $(date)' > " + str(OUTPUT_DIR / "forecasting3" / "ex_statsforecast_completed.txt"),
        ],
        "targets": [
            # No specific output files since this is a tutorial that prints and shows plots
            # But we can create a simple completion marker
            OUTPUT_DIR / "forecasting3" / "ex_statsforecast_completed.txt",
        ],
        "file_dep": [
            "./forecasting/ex_statsforecast.py",
            "./forecasting/forecast.py",  # Main dependency since tutorial imports from it
            "./forecasting/models_config.toml",
            "./datasets.toml",
            *dataset_parquet_files,  # Data dependency
        ],
        "clean": True,
        "verbosity": 2,  # Show output for educational purposes
    }


def task_compile_latex_docs():
    """Compile the LaTeX documents to PDFs using forecasting3 outputs"""

    return {
        "actions": [
            "latexmk -xelatex -halt-on-error -cd ./reports/draft_ftsfr.tex",  # Compile
            "latexmk -xelatex -halt-on-error -c -cd ./reports/draft_ftsfr.tex",  # Clean
        ],
        "targets": [
            "./reports/draft_ftsfr.pdf",
        ],
        "file_dep": [
            "./src/create_results_tables2.py",
            "./src/create_dataset_statistics.py",
            "./reports/draft_ftsfr.tex",
            # LaTeX table dependencies (from _output/forecasting3/ as these are referenced in the paper)
            OUTPUT_DIR / "forecasting3" / "dataset_statistics.tex",
            OUTPUT_DIR / "forecasting3" / "mase_pivot_table.tex",
            OUTPUT_DIR / "forecasting3" / "rmse_pivot_table.tex",
            OUTPUT_DIR / "forecasting3" / "smape_pivot_table.tex",
            OUTPUT_DIR / "forecasting3" / "mae_pivot_table.tex",
            OUTPUT_DIR / "forecasting3" / "relative_mase_pivot_table.tex",
            OUTPUT_DIR / "forecasting3" / "r2oos_pivot_table.tex",
            OUTPUT_DIR / "forecasting3" / "model_summary_statistics.tex",
            # Heatmap plot dependencies
            OUTPUT_DIR / "forecasting3" / "mase_heatmap.png",
            OUTPUT_DIR / "forecasting3" / "rmse_heatmap.png",
            OUTPUT_DIR / "forecasting3" / "smape_heatmap.png",
            OUTPUT_DIR / "forecasting3" / "mae_heatmap.png",
            OUTPUT_DIR / "forecasting3" / "r2oos_heatmap.png",
        ],
        "clean": True,
    }


# def task_convert_pdfs_to_markdown():
#     """Convert PDFs to Markdown (currently commented out in original)"""

#     # This task was commented out in the original dodo.py
#     # Uncomment and modify as needed

#     return {
#         "actions": [
#             "python ./src/mistral_ocr.py",
#         ],
#         "targets": [
#             "./notes/monash_time_series_forecasting_appendix.md",
#             "./notes/monash_time_series_forecasting.md",
#         ],
#         "file_dep": [
#             "./references_md/309_monash_time_series_forecasting-Supplementary_Material.pdf",
#             "./references_md/309_monash_time_series_forecasting.pdf",
#         ],
#         "clean": True,
#         "verbosity": 2,
#     }
