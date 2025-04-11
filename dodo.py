import re
import sys
from pathlib import Path

import toml
from doit.action import CmdAction

sys.path.insert(1, "./src/")

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))
OS_TYPE = config("OS_TYPE")


## Helpers for handling Jupyter Notebook tasks
# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
def jupyter_execute_notebook(notebook_path):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --inplace {notebook_path}"
def jupyter_to_html(notebook_path, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --output-dir={output_dir} {notebook_path}"
def jupyter_to_md(notebook_path, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --output-dir={output_dir} {notebook_path}"
def jupyter_to_python(notebook_path, notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --to python {notebook_path} --output _{notebook}.py --output-dir {build_dir}"
def jupyter_clear_output(notebook_path):
    """Clear the output of a notebook"""
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace {notebook_path}"
# fmt: on


def copy_notebook_to_folder(notebook_path, destination_folder, notebook_name):
    """Copy a notebook to a folder"""
    notebook_path = Path(notebook_path)
    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    if OS_TYPE == "nix":
        command = f"cp {notebook_path} {destination_folder / f'{notebook_name}.ipynb'}"
    else:
        command = f"copy  {notebook_path} {destination_folder / f'{notebook_name}.ipynb'}"
    return command


# Load benchmarks configuration
with open("benchmarks.toml", "r") as f:
    benchmarks_file = toml.load(f)


def task_config():
    """Create empty directories for data and output if they don't exist"""
    file_dep = [
        "./src/settings.py",
    ]
    targets = [DATA_DIR, OUTPUT_DIR]

    return {
        "actions": [
            "ipython ./src/settings.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": [],
    }


data_sources = benchmarks_file["data_sources"]
use_cache = benchmarks_file["cache"]["use_cache"]
# If use_cache is True, set all data_sources to pull = False
if use_cache:
    for data_source in data_sources:
        data_sources[data_source] = False


def task_data():
    """Pull selected data_sources based on benchmarks.toml configuration"""

    if data_sources["fed_yield_curve"]:
        subfolder = "fed_yield_curve"
        yield {
            "name": f"pull:{subfolder}",
            "actions": [
                f"python ./src/{subfolder}/pull_fed_yield_curve.py --DATA_DIR={DATA_DIR / subfolder}",
            ],
            "targets": [DATA_DIR / subfolder / "fed_yield_curve.parquet"],
            "file_dep": [f"./src/{subfolder}/pull_fed_yield_curve.py"],
            "clean": [],
        }
        yield {
            "name": f"format:{subfolder}",
            "actions": [
                f"python ./src/{subfolder}/create_ftsf_datasets.py --DATA_DIR={DATA_DIR / subfolder}",
            ],
            "targets": [
                DATA_DIR / subfolder / "ftsfa_treas_yield_curve_zero_coupon.parquet"
            ],
            "file_dep": [
                f"./src/{subfolder}/pull_fed_yield_curve.py",
                f"./src/{subfolder}/create_ftsf_datasets.py",
            ],
            "clean": [],
        }

    if data_sources["ken_french_data_library"]:
        from ken_french_data_library.pull_fama_french_25_portfolios import DATA_INFO

        subfolder = "ken_french_data_library"
        yield {
            "name": f"pull:{subfolder}",
            "actions": [
                f"python ./src/{subfolder}/pull_fama_french_25_portfolios.py --DATA_DIR={DATA_DIR / subfolder}"
            ],
            "targets": [
                DATA_DIR / "ken_french_data_library" / info["parquet"]
                for info in DATA_INFO.values()
            ],
            "file_dep": [f"./src/{subfolder}/pull_fama_french_25_portfolios.py"],
            "clean": [],
        }

    if data_sources["nyu_call_report"]:
        subfolder = "nyu_call_report"
        yield {
            "name": f"pull:{subfolder}",
            "actions": [
                f"python ./src/{subfolder}/pull_nyu_call_report.py --DATA_DIR={DATA_DIR / subfolder}"
            ],
            "targets": [DATA_DIR / subfolder / "nyu_call_report.parquet"],
            "file_dep": [f"./src/{subfolder}/pull_nyu_call_report.py"],
            "clean": [],
        }
        yield {
            "name": f"format:{subfolder}",
            "actions": [
                f"python ./src/{subfolder}/create_ftsf_datasets.py --DATA_DIR={DATA_DIR / subfolder}",
            ],
            "targets": [
                DATA_DIR / subfolder / "ftsfa_nyu_call_report_leverage.parquet",
                DATA_DIR
                / subfolder
                / "ftsfa_nyu_call_report_holding_company_leverage.parquet",
                DATA_DIR / subfolder / "ftsfa_nyu_call_report_cash_liquidity.parquet",
                DATA_DIR
                / subfolder
                / "ftsfa_nyu_call_report_holding_company_cash_liquidity.parquet",
            ],
            "file_dep": [
                f"./src/{subfolder}/pull_nyu_call_report.py",
                f"./src/{subfolder}/create_ftsf_datasets.py",
            ],
            "clean": [],
        }

    if data_sources["wrds_bank_premium"]:
        subfolder = "wrds_bank_premium"
        yield {
            "name": f"pull:{subfolder}",
            "actions": [
                f"python ./src/{subfolder}/pull_wrds_bank_premium.py --DATA_DIR={DATA_DIR / subfolder}"
            ],
            "targets": [
                DATA_DIR / subfolder / "wrds_struct_rel_ultimate.parquet",
                DATA_DIR / subfolder / "wrds_call_research.parquet",
                DATA_DIR / subfolder / "wrds_bank_crsp_link.parquet",
                DATA_DIR / subfolder / "idrssd_to_lei.parquet",
                DATA_DIR / subfolder / "lei_main.parquet",
                DATA_DIR / subfolder / "lei_legalevents.parquet",
                DATA_DIR / subfolder / "lei_otherentnames.parquet",
                DATA_DIR / subfolder / "lei_successorentity.parquet",
            ],
            "file_dep": [f"./src/{subfolder}/pull_wrds_bank_premium.py"],
            "clean": [],
        }

    if data_sources["wrds_crsp_compustat"]:
        subfolder = "wrds_crsp_compustat"

        yield {
            "name": f"pull:{subfolder}",
            "actions": [
                f"python ./src/{subfolder}/pull_CRSP_Compustat.py --DATA_DIR={DATA_DIR / subfolder}",
                f"python ./src/{subfolder}/create_ftsf_datasets.py --DATA_DIR={DATA_DIR / subfolder}",
            ],
            "targets": [
                DATA_DIR / subfolder / "Compustat.parquet",
                DATA_DIR / subfolder / "CRSP_stock_ciz.parquet",
                DATA_DIR / subfolder / "CRSP_Comp_Link_Table.parquet",
                DATA_DIR / subfolder / "FF_FACTORS.parquet",
            ],
            "file_dep": [f"./src/{subfolder}/pull_CRSP_Compustat.py"],
            "clean": [],
        }
        yield {
            "name": f"data_sets_{subfolder}",
            "actions": [
                f"python ./src/{subfolder}/create_ftsf_datasets.py --DATA_DIR={DATA_DIR / subfolder}",
            ],
            "targets": [
                DATA_DIR / subfolder / "ftsfa_CRSP_monthly_stock_ret.parquet",
                DATA_DIR / subfolder / "ftsfa_CRSP_monthly_stock_retx.parquet",
            ],
            "file_dep": [
                f"./src/{subfolder}/create_ftsf_datasets.py",
                f"./src/{subfolder}/pull_CRSP_Compustat.py",
                f"./src/{subfolder}/calc_Fama_French_1993.py",
            ],
            "clean": [],
        }

        yield {
            "name": "pull:CRSP_stock",
            "actions": [
                f"python ./src/{subfolder}/pull_CRSP_stock.py --DATA_DIR={DATA_DIR / subfolder}"
            ],
            "targets": [
                DATA_DIR / subfolder / "CRSP_MSF_INDEX_INPUTS.parquet",
                DATA_DIR / subfolder / "CRSP_MSIX.parquet",
            ],
            "file_dep": [f"./src/{subfolder}/pull_CRSP_stock.py"],
            "clean": [],
        }

        # TODO: Create dataset that merges the treasury auction, runness, and treasury yield data
        # The code right now only pulls them separately.

        yield {
            "name": "pull:CRSP_treasury",
            "actions": [
                f"python ./src/{subfolder}/pull_treasury_auction_stats.py --DATA_DIR={DATA_DIR / subfolder}",
                f"python ./src/{subfolder}/calculate_ontherun.py --DATA_DIR={DATA_DIR / subfolder}",
                f"python ./src/{subfolder}/pull_CRSP_treasury.py --DATA_DIR={DATA_DIR / subfolder}",
            ],
            "targets": [
                DATA_DIR / subfolder / "treasury_auction_stats.parquet",
                DATA_DIR / subfolder / "issue_dates.csv",
                DATA_DIR / subfolder / "ontherun.csv",
                DATA_DIR / subfolder / "CRSP_TFZ_DAILY.parquet",
                DATA_DIR / subfolder / "CRSP_TFZ_INFO.parquet",
                DATA_DIR / subfolder / "CRSP_TFZ_CONSOLIDATED.parquet",
                DATA_DIR / subfolder / "CRSP_TFZ_with_runness.parquet",
            ],
            "file_dep": [
                f"./src/{subfolder}/pull_treasury_auction_stats.py",
                f"./src/{subfolder}/calculate_ontherun.py",
                f"./src/{subfolder}/pull_CRSP_treasury.py",
            ],
            "clean": [],
        }

    # fmt: off
    if data_sources["wrds_corp_bonds"]:
        from wrds_corp_bonds.pull_corp_bonds import DATA_INFO
        subfolder = "wrds_corp_bonds"
        yield {
            "name": f"pull:{subfolder}",
            "actions": [f"python ./src/{subfolder}/pull_corp_bonds.py --DATA_DIR={DATA_DIR / subfolder}"],
            "targets": [
                DATA_DIR / subfolder / info["parquet"]
                for info in DATA_INFO.values()
            ]
            + [
                DATA_DIR / subfolder / f"{info['parquet'].replace('.parquet', '_README.pdf')}"
                for info in DATA_INFO.values()
            ],
            "file_dep": [f"./src/{subfolder}/pull_corp_bonds.py"],
            "clean": [],
        }
    # fmt: on

    if data_sources["wrds_markit"]:
        subfolder = "wrds_markit"
        yield {
            "name": f"pull:{subfolder}",
            "actions": [
                f"python ./src/{subfolder}/pull_fed_yield_curve.py --DATA_DIR={DATA_DIR / subfolder}",
                f"python ./src/{subfolder}/pull_markit_cds.py --DATA_DIR={DATA_DIR / subfolder}",
            ],
            "targets": [
                DATA_DIR / subfolder / "markit_cds.parquet",
                DATA_DIR / subfolder / "fed_yield_curve.parquet",
            ],
            "file_dep": [
                f"./src/{subfolder}/pull_fed_yield_curve.py",
                f"./src/{subfolder}/pull_markit_cds.py",
            ],
            "clean": [],
        }
        # yield {
        #     "name": "calc_cds_returns",
        #     "actions": [
        #         f"python ./src/{subfolder}/calc_cds_returns.py --DATA_DIR={DATA_DIR / subfolder}",
        #     ],
        #     "targets": [
        #         DATA_DIR / subfolder / "markit_cds_returns.parquet",
        #     ],
        #     "file_dep": [
        #         f"./src/{subfolder}/calc_cds_returns.py",
        #     ],
        #     "clean": [],
        # }

    # cds_bond_basis = (data_sources["wrds_mergent"] and data_sources["wrds_bond_returns"] and data_sources["wrds_markit"])
    # if cds_bond_basis:
    #     subfolder = "cds_bond_basis"
    #     yield {
    #         "name": f"pull:{subfolder}",
    #         "actions": [
    #             f"python ./src/{subfolder}/pull_wrds_markit.py --DATA_DIR={DATA_DIR / subfolder}",
    #             f"python ./src/{subfolder}/pull_wrds_bond_returns.py --DATA_DIR={DATA_DIR / subfolder}",
    #             f"python ./src/{subfolder}/pull_wrds_mergent.py --DATA_DIR={DATA_DIR / subfolder}",
    #             f"python ./src/{subfolder}/create_cds_bond_basis.py --DATA_DIR={DATA_DIR / subfolder}",
    #         ],
    #         "targets": [
    #             DATA_DIR / subfolder / "cds_bond_basis.parquet",
    #         ],
    #         "file_dep": [
    #             f"./src/{subfolder}/pull_wrds_markit.py",
    #             f"./src/{subfolder}/pull_wrds_bond_returns.py",
    #             f"./src/{subfolder}/pull_wrds_mergent.py",
    #             f"./src/{subfolder}/create_cds_bond_basis.py",
    #         ],
    #         "clean": [],
    #     }


def task_collect_ftsfa_datasets_info():
    return {
        "actions": [
            "python ./src/load_ftsfa_datasets.py",
        ],
        "file_dep": ["./src/load_ftsfa_datasets.py"],
        "targets": [DATA_DIR / "ftsfa_datasets_paths.toml"],
        "clean": [],
    }


models = benchmarks_file["models"]
models_activated = [model for model in models if models[model]]


def task_forecast():
    if models["simple_exponential_smoothing"]:
        yield {
            "name": "simple_exponential_smoothing",
            "actions": [
                CmdAction("pixi run main", cwd="./models/simple_exponential_smoothing")
            ],
            "targets": [
                OUTPUT_DIR / "raw_results" / "simple_exponential_smoothing_results.csv"
            ],
            "file_dep": [
                "./models/simple_exponential_smoothing/main.R",
                "./models/simple_exponential_smoothing/pixi.toml",
            ],
            "clean": [],
        }

    if models["arima"]:
        yield {
            "name": "arima",
            "actions": [CmdAction("pixi run main", cwd="./models/arima")],
            "targets": [OUTPUT_DIR / "raw_results" / "arima_results.csv"],
            "file_dep": [
                "./models/arima/main.py",
                "./models/arima/pixi.toml",
            ],
            "clean": [],
        }


def task_assemble_results():
    results_files = [
        OUTPUT_DIR / "raw_results" / f"{model}_results.csv"
        for model in models_activated
    ]
    return {
        "actions": [
            "python ./src/assemble_results.py",
        ],
        "targets": [
            OUTPUT_DIR / "results_all.csv",
            OUTPUT_DIR / "results_all.tex",
        ],
        "file_dep": [
            *results_files,
            "./src/assemble_results.py",
        ],
        "clean": [],
    }


notebook_tasks = {
    "example_notebook_markit": {
        "path": "./src/wrds_markit/example_notebook_markit.ipynb",
        "file_dep": [],
        "targets": [],
    },
}


def task_convert_notebooks_to_scripts():
    """Convert notebooks to script form to detect changes to source code rather
    than to the notebook's metadata.
    """
    build_dir = Path(OUTPUT_DIR)
    build_dir.mkdir(parents=True, exist_ok=True)

    for notebook in notebook_tasks.keys():
        notebook_path = notebook_tasks[notebook]["path"]
        yield {
            "name": notebook,
            "actions": [
                jupyter_clear_output(notebook_path),
                jupyter_to_python(notebook_path, notebook, build_dir),
            ],
            "file_dep": [notebook_path],
            "targets": [OUTPUT_DIR / f"_{notebook}.py"],
            "clean": True,
            "verbosity": 0,
        }


# fmt: off
def task_run_notebooks():
    """Preps the notebooks for presentation format.
    Execute notebooks if the script version of it has been changed.
    """

    for notebook in notebook_tasks.keys():
        notebook_path = notebook_tasks[notebook]["path"]
        yield {
            "name": notebook,
            "actions": [
                """python -c "import sys; from datetime import datetime; print(f'Start """ + notebook + """: {datetime.now()}', file=sys.stderr)" """,
                jupyter_execute_notebook(notebook_path),
                jupyter_to_html(notebook_path),
                copy_notebook_to_folder(notebook_path, "./docs_src/_notebook_build/", notebook),
                jupyter_clear_output(notebook_path),
                """python -c "import sys; from datetime import datetime; print(f'End """ + notebook + """: {datetime.now()}', file=sys.stderr)" """,
            ],
            "file_dep": [
                OUTPUT_DIR / f"_{notebook}.py",
                *notebook_tasks[notebook]["file_dep"],
            ],
            "targets": [
                OUTPUT_DIR / f"{notebook}.html",
                *notebook_tasks[notebook]["targets"],
            ],
            "clean": True,
            # "verbosity": 1,
        }
# fmt: on

sphinx_targets = [
    "./docs/html/index.html",
    "./docs/html/myst_markdown_demos.html",
]


def task_compile_sphinx_docs():
    """Compile Sphinx Docs"""
    file_dep = [
        "./docs_src/conf.py",
        "./docs_src/index.md",
        "./docs_src/myst_markdown_demos.md",
    ]

    return {
        "actions": [
            "sphinx-build -M html ./docs_src/ ./docs"
        ],  # Use docs as build destination
        # "actions": ["sphinx-build -M html ./docs/ ./docs/_build"], # Previous standard organization
        "targets": sphinx_targets,
        "file_dep": file_dep,
        "task_dep": ["run_notebooks"],
        "clean": True,
    }


def task_compile_latex_docs():
    """Compile the LaTeX documents to PDFs"""
    if benchmarks_file["reports"]["is_latex_installed"]:
        return {
            "actions": [
                "latexmk -xelatex -halt-on-error -cd ./reports/draft_ftsfa.tex",  # Compile
                "latexmk -xelatex -halt-on-error -c -cd ./reports/draft_ftsfa.tex",  # Clean
            ],
            "targets": [
                "./reports/draft_ftsfa.pdf",
            ],
            "file_dep": [
                "./reports/draft_ftsfa.tex",
                "./src/assemble_results.py",
            ],
            "clean": True,
        }
    else:
        return {
            "actions": [],
            "targets": [],
            "file_dep": [],
            "clean": [],
        }


# def task_convert_pdfs_to_markdown():
#     """Convert PDFs to Markdown"""
#
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
