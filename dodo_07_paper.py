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
import glob

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
    """Check if forecast result files exist in the new structure"""
    error_metrics_dir = OUTPUT_DIR / "forecasting" / "error_metrics"

    if not error_metrics_dir.exists():
        print(
            f"\nWarning: No forecasting error metrics directory found at {error_metrics_dir}"
        )
        print(
            "Please run forecasting tasks first (e.g., 'doit -f dodo_02_darts_local.py')"
        )
        return False

    available_datasets = get_available_datasets(module_requirements, DATA_DIR)

    # Count available vs expected results
    total_expected = len(models_activated) * len(available_datasets)
    results_found = 0

    for model in models_activated:
        model_dir = error_metrics_dir / model
        if model_dir.exists():
            for dataset_name in available_datasets:
                clean_dataset_name = dataset_name.replace("ftsfr_", "")
                result_file = model_dir / f"{clean_dataset_name}.csv"
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
    """Assemble results from all model-dataset combinations."""

    # Check for result files at task generation time
    check_forecast_results()

    # Get all CSV files in the forecasting error metrics directory
    error_metrics_csv_files = glob.glob(
        str(OUTPUT_DIR / "forecasting" / "error_metrics" / "**" / "*.csv"),
        recursive=True,
    )

    return {
        "actions": [
            "python ./src/assemble_results.py",
        ],
        "targets": [
            OUTPUT_DIR / "results_all.csv",
            OUTPUT_DIR / "results_all.tex",
        ],
        "file_dep": [
            "./src/assemble_results.py",
            *error_metrics_csv_files,
        ],
        "clean": True,
    }


def task_create_results_tables():
    """Create analytical tables from assembled results"""
    return {
        "actions": [
            "python ./src/create_results_tables.py",
        ],
        "targets": [
            OUTPUT_DIR / "mase_pivot_table.csv",
            OUTPUT_DIR / "mase_pivot_table.tex",
            OUTPUT_DIR / "model_summary_statistics.csv",
            OUTPUT_DIR / "model_summary_statistics.tex",
        ],
        "file_dep": [
            "./src/assemble_results.py",
            "./src/create_results_tables.py",
            OUTPUT_DIR / "results_all.csv",
        ],
        "clean": True,
    }


def task_compile_latex_docs():
    """Compile the LaTeX documents to PDFs"""

    return {
        "actions": [
            "latexmk -xelatex -halt-on-error -cd ./reports/draft_ftsfr.tex",  # Compile
            "latexmk -xelatex -halt-on-error -c -cd ./reports/draft_ftsfr.tex",  # Clean
        ],
        "targets": [
            "./reports/draft_ftsfr.pdf",
        ],
        "file_dep": [
            "./src/create_results_tables.py",
            "./reports/draft_ftsfr.tex",
            OUTPUT_DIR / "mase_pivot_table.tex",
            OUTPUT_DIR / "model_summary_statistics.tex",
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
