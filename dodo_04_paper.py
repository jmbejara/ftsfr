"""
dodo_04_paper.py - Results assembly, report generation, and LaTeX compilation

This file contains all tasks related to:
- Assembling results from model runs
- Generating LaTeX documents and reports
- Converting PDFs to markdown
"""

# Import common utilities
from dodo_common import (
    DATA_DIR,
    OUTPUT_DIR,
    notebook_subtask,
)


def task_assemble_results():
    """Assemble results from all model-dataset combinations using the new forecasting system."""

    return {
        "actions": [
            "python ./src/assemble_results.py",
        ],
        "targets": [
            OUTPUT_DIR / "forecasting" / "results_all.csv",
        ],
        "file_dep": [
            "./src/assemble_results.py",
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
            "python ./src/forecasting/create_dataset_statistics.py",
        ],
        "targets": [
            OUTPUT_DIR / "forecasting" / "paper" / "dataset_statistics.csv",
            OUTPUT_DIR / "forecasting" / "paper" / "dataset_statistics.tex",
        ],
        "file_dep": [
            "./src/forecasting/create_dataset_statistics.py",
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
            "python ./src/forecasting/create_filtered_dataset_statistics.py",
        ],
        "targets": [
            OUTPUT_DIR / "forecasting" / "paper" / "filtered_dataset_statistics.csv",
            OUTPUT_DIR / "forecasting" / "paper" / "filtered_dataset_statistics.tex",
        ],
        "file_dep": [
            "./src/forecasting/create_filtered_dataset_statistics.py",
            "./src/forecasting/forecast_utils.py",  # Contains filtering logic we're applying
            "./datasets.toml",  # Primary dependency - drives which datasets to include
            *dataset_parquet_files,  # Secondary dependencies - actual data files
        ],
        "clean": True,
    }


def task_create_results_tables():
    """Create analytical tables from assembled results using forecasting system"""
    return {
        "actions": [
            "python ./src/forecasting/create_results_tables.py",
        ],
        "targets": [
            # Tables and plots in the paper directory
            OUTPUT_DIR / "forecasting" / "paper" / "mase_pivot_table.csv",
            OUTPUT_DIR / "forecasting" / "paper" / "rmse_pivot_table.csv",
            OUTPUT_DIR / "forecasting" / "paper" / "r2oos_pivot_table.csv",
            OUTPUT_DIR / "forecasting" / "paper" / "median_mase_summary.csv",
            OUTPUT_DIR / "forecasting" / "paper" / "model_summary_by_type_overall.csv",
            OUTPUT_DIR / "forecasting" / "paper" / "model_summary_by_type_tabular.tex",
            # Heatmap plots (PNG files)
            OUTPUT_DIR / "forecasting" / "paper" / "mase_heatmap.png",
            OUTPUT_DIR / "forecasting" / "paper" / "rmse_heatmap.png",
            OUTPUT_DIR / "forecasting" / "paper" / "r2oos_heatmap.png",
        ],
        "file_dep": [
            "./src/forecasting/create_results_tables.py",
            OUTPUT_DIR / "forecasting" / "results_all.csv",
            "./src/forecasting/models_config.toml",  # Add dependency on models config for column ordering
            "./datasets.toml",  # Add dependency on datasets config for column ordering
        ],
        "clean": True,
    }


# Commented out due to missing functions - tutorial example not essential for main pipeline
# def task_run_ex_statsforecast():
#     """Run the AutoARIMA tutorial example demonstrating the forecasting pipeline"""
#     import glob
#
#     # Get parquet files that the tutorial might use
#     dataset_parquet_files = glob.glob(
#         str(DATA_DIR / "formatted" / "**" / "ftsfr_french_portfolios_25_daily_size_and_bm.parquet"),
#         recursive=True,
#     )
#
#     return {
#         "actions": [
#             "python ./src/forecasting/ex_statsforecast.py",
#             "echo 'Tutorial completed successfully on $(date)' > " + str(OUTPUT_DIR / "forecasting" / "ex_statsforecast_completed.txt"),
#         ],
#         "targets": [
#             # No specific output files since this is a tutorial that prints and shows plots
#             # But we can create a simple completion marker
#             OUTPUT_DIR / "forecasting" / "ex_statsforecast_completed.txt",
#         ],
#         "file_dep": [
#             "./src/forecasting/ex_statsforecast.py",
#             "./src/forecasting/forecast_utils.py",  # Main dependency since tutorial imports from it
#             "./src/forecasting/models_config.toml",
#             "./datasets.toml",
#             *dataset_parquet_files,  # Data dependency
#         ],
#         "clean": True,
#         "verbosity": 2,  # Show output for educational purposes
#     }

def task_run_example_forecasts():
    """Run the example forecasts walkthrough demonstrating the forecasting pipeline"""

    yield from notebook_subtask(
        {
            "name": "example_forecasts_ipynb",
            "notebook_path": "./src/forecasting/example_forecasts_ipynb.py",
            "file_dep": [
                "./src/forecasting/example_forecasts_ipynb.py",
                "./src/forecasting/forecast_neural_auto.py",
                DATA_DIR / "formatted" / "basis_tips_treas" / "ftsfr_tips_treasury_basis.parquet",
            ],
            "targets": [],
        }
    )


def task_validate_latex_paths():
    """Enforce that reports/*.tex stays self-contained (no `..`, _output, _data).

    The reports/ directory is intended to be portable: a collaborator should
    be able to copy reports/ alone and compile. This check fails the build
    if any .tex file uses parent traversal or references the gitignored
    _output/ or _data/ trees. Runs every build; needs nothing pre-built.
    """
    return {
        "actions": ["python ./src/validate_latex_paths.py"],
        "file_dep": [
            "./src/validate_latex_paths.py",
            "./reports/draft_ftsfr.tex",
            "./reports/slides_ftsfr.tex",
            "./reports/internet_appendix.tex",
        ],
        "verbosity": 2,
    }


def task_cache_latex_artifacts():
    """Refresh reports/output/ and reports/docs_src/ from source artifacts.

    Extracts \\input/\\includegraphics references from reports/*.tex and
    copies just those files from ./_output/ and ./docs_src/ into the
    self-contained caches under reports/. Authors run this after a full
    pipeline refresh, before committing the cache. Not a dep of
    compile_latex_docs so collaborators can compile from the committed
    caches without ./_output/ present.
    """
    return {
        "actions": ["python ./src/cache_latex_artifacts.py"],
        "file_dep": [
            "./src/cache_latex_artifacts.py",
            "./reports/draft_ftsfr.tex",
            "./reports/slides_ftsfr.tex",
            "./reports/internet_appendix.tex",
        ],
        "uptodate": [False],
        "verbosity": 2,
    }


def task_compile_latex_docs():
    """Compile the LaTeX documents to PDFs.

    Reads tables/figures from reports/output/ and reports/docs_src/ — the
    committed caches populated by task_cache_latex_artifacts. The reports/
    directory is self-contained, so this task works without ./_output/ or
    the top-level ./docs_src/ being present. Validation runs first via
    task_dep.
    """
    import glob
    from pathlib import Path

    cache_files: list[str] = []
    for cache_dir in (Path("./reports/output"), Path("./reports/docs_src")):
        if cache_dir.exists():
            cache_files.extend(
                f
                for f in glob.glob(str(cache_dir / "**" / "*"), recursive=True)
                if Path(f).is_file()
            )
    cache_files.sort()

    return {
        "actions": [
            "latexmk -xelatex -halt-on-error -cd ./reports/draft_ftsfr.tex",  # Compile
            "latexmk -xelatex -halt-on-error -c -cd ./reports/draft_ftsfr.tex",  # Clean
            "latexmk -xelatex -halt-on-error -cd ./reports/slides_ftsfr.tex",  # Compile
            "latexmk -xelatex -halt-on-error -c -cd ./reports/slides_ftsfr.tex",  # Clean
            "latexmk -xelatex -halt-on-error -cd ./reports/internet_appendix.tex",  # Compile
            "latexmk -xelatex -halt-on-error -c -cd ./reports/internet_appendix.tex",  # Clean
        ],
        "targets": [
            "./reports/draft_ftsfr.pdf",
            "./reports/slides_ftsfr.pdf",
            "./reports/internet_appendix.pdf",
        ],
        "task_dep": ["validate_latex_paths"],
        "file_dep": [
            "./reports/draft_ftsfr.tex",
            "./reports/slides_ftsfr.tex",
            "./reports/internet_appendix.tex",
            *cache_files,
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
