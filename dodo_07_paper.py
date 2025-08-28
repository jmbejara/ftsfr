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
)
from dependency_tracker import get_available_datasets

# Load configuration
subscriptions_toml = load_subscriptions()
models = subscriptions_toml["models"]
models_activated = [model for model in models if models[model]]

# Load module requirements to determine available datasets
module_requirements_dict = load_all_module_requirements()
module_requirements = {}
for module_name, required_sources in module_requirements_dict.items():
    module_requirements[module_name] = all(
        subscriptions_toml["data_sources"].get(source, False)
        for source in required_sources
    )


def check_forecast_results():
    """Check if forecast result files exist"""
    available_datasets = get_available_datasets(module_requirements, DATA_DIR)
    results_dir = OUTPUT_DIR / "raw_results"

    if not results_dir.exists():
        print("\nWarning: No results directory found at:", results_dir)
        print(
            "Please run 'doit -f dodo_02_forecast.py' first to generate forecast results."
        )
        return False

    expected_files = []
    for model in models_activated:
        for dataset_name in available_datasets:
            expected_files.append(results_dir / f"{model}_{dataset_name}_results.csv")

    missing_files = [f for f in expected_files if not f.exists()]

    if missing_files:
        print(f"\nWarning: {len(missing_files)} result files are missing.")
        print(
            "Some expected result files not found. You may want to run forecasting first."
        )
        print("Continuing with available results...\n")

    return len(missing_files) == 0


def task_assemble_results():
    """Assemble results from all model-dataset combinations."""

    # Check for result files at task generation time
    check_forecast_results()

    # Simplified file dependencies - only depend on the assemble script
    # The script itself will handle missing files gracefully
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
        ],
        "clean": [],
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
            "./reports/draft_ftsfr.tex",
            "./src/assemble_results.py",
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
