import sys
from pathlib import Path
import shutil

import toml
from doit.action import CmdAction

sys.path.insert(1, "./src/")

from settings import config
from dependency_tracker import (
    load_module_requirements,
    get_available_datasets,
    get_format_task_name,
)

DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))
OS_TYPE = config("OS_TYPE")

# Get pixi executable path
PIXI_EXECUTABLE = shutil.which("pixi")
if not PIXI_EXECUTABLE:
    # Fallback to common installation paths
    if Path.home().joinpath(".pixi/bin/pixi").exists():
        PIXI_EXECUTABLE = str(Path.home() / ".pixi/bin/pixi")
    else:
        PIXI_EXECUTABLE = "pixi"  # Hope it's in PATH at runtime


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


def mv(from_path, to_path):
    """Copy a notebook to a folder"""
    from_path = Path(from_path)
    to_path = Path(to_path)
    to_path.mkdir(parents=True, exist_ok=True)
    if OS_TYPE == "nix":
        command = f"mv {from_path} {to_path}"
    else:
        command = f"move {from_path} {to_path}"
    return command


def copy_dir_contents_to_folder(dir_path, destination_folder):
    """Copy a directory to a folder"""
    dir_path = Path(dir_path)
    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    if OS_TYPE == "nix":
        command = f"cp -r {dir_path}/ {destination_folder}"
    else:
        command = f"xcopy /E /I {dir_path}/ {destination_folder}"
    return command


def notebook_subtask(task_config):
    """
    Generate notebook task configuration with unified workflow for .py and .ipynb files.

    Creates a two-stage process:
    1. Normalize: Convert source to stable .py file in OUTPUT_DIR
    2. Execute & Render: Run .py, convert to notebook, execute, generate HTML

    Parameters:
    - task_config: dict with keys:
        - name: str, task name
        - notebook_path: str, path to .py or .ipynb file
        - file_dep: list, additional file dependencies (optional)
        - targets: list, additional targets (optional)

    Yields task configuration(s) for doit.
    """
    name = task_config["name"]
    source_path = Path(task_config["notebook_path"])
    file_dep = task_config.get("file_dep", [])
    targets = task_config.get("targets", [])

    # Intermediate .py file in OUTPUT_DIR
    py_filename = f"_{name}_ipynb.py"
    py_path = OUTPUT_DIR / py_filename

    # Stage 1: Normalize to .py in OUTPUT_DIR
    # Create the normalize action based on file type
    if source_path.suffix == ".py":
        normalize_actions = [
            f"mkdir -p {OUTPUT_DIR}"
            if OS_TYPE == "nix"
            else f"mkdir {OUTPUT_DIR} 2>nul || echo.",
            f"cp {source_path} {py_path}"
            if OS_TYPE == "nix"
            else f"copy {source_path} {py_path}",
        ]
    elif source_path.suffix == ".ipynb":
        normalize_actions = [
            f"mkdir -p {OUTPUT_DIR}"
            if OS_TYPE == "nix"
            else f"mkdir {OUTPUT_DIR} 2>nul || echo.",
            f"jupyter nbconvert --to python --output {py_path} {source_path}",
        ]
    else:
        raise ValueError(
            f"Unsupported file type: {source_path.suffix}. Must be .py or .ipynb"
        )

    yield {
        "name": f"{name}_normalize",
        "actions": normalize_actions,
        "file_dep": [str(source_path)],
        "targets": [str(py_path)],
        "clean": True,
    }

    # Stage 2: Execute and render
    # Work in the source directory to preserve relative paths
    working_notebook = source_path.with_suffix(".ipynb")

    # Determine whether to move or copy based on source file type
    if source_path.suffix == ".py":
        # For .py sources, the .ipynb is intermediate, so move it
        notebook_transfer_cmd = mv(working_notebook, OUTPUT_DIR / "_notebook_build")
    else:
        # For .ipynb sources, preserve the original by copying
        if OS_TYPE == "nix":
            notebook_transfer_cmd = (
                f"cp {working_notebook} {OUTPUT_DIR / '_notebook_build'}"
            )
        else:
            notebook_transfer_cmd = (
                f"copy {working_notebook} {OUTPUT_DIR / '_notebook_build'}"
            )

    # For .py sources, clear outputs before moving; for .ipynb sources, after copying
    clear_output_action = (
        jupyter_clear_output(working_notebook) 
        if source_path.suffix == ".ipynb" 
        else "echo 'Skipping output clear for .py source'"
    )
    
    yield {
        "name": name,
        "actions": [
            f"""python -c "import sys; from datetime import datetime; print(f'Start {name}: {{datetime.now()}}', file=sys.stderr)" """,
            # Ensure output directories exist
            f"mkdir -p {OUTPUT_DIR / '_notebook_build'}"
            if OS_TYPE == "nix"
            else f"mkdir {OUTPUT_DIR / '_notebook_build'} 2>nul || echo.",
            # Convert source to notebook format (in source directory)
            f"ipynb-py-convert {source_path} {working_notebook}"
            if source_path.suffix == ".py"
            else "echo 'Using existing notebook'",
            # Execute notebook in its original directory (preserves relative paths)
            jupyter_execute_notebook(working_notebook),
            # Generate HTML
            jupyter_to_html(working_notebook, OUTPUT_DIR),
            # Move or copy executed notebook to build directory based on source type
            notebook_transfer_cmd,
            # Clear outputs to prevent constant re-runs (only for .ipynb sources)
            clear_output_action,
            f"""python -c "import sys; from datetime import datetime; print(f'End {name}: {{datetime.now()}}', file=sys.stderr)" """,
        ],
        "file_dep": [
            str(py_path),  # Depend on normalized .py for stability
            *file_dep,
        ],
        "targets": [
            OUTPUT_DIR / f"{name}.html",
            OUTPUT_DIR / "_notebook_build" / f"{name}.ipynb",
            *targets,
        ],
        "clean": True,
    }


# Load benchmarks configuration
with open("config.toml", "r") as f:
    config_toml = toml.load(f)


def task_config():
    """Create empty directories for data and output if they don't exist"""

    return {
        "actions": [
            "ipython ./src/settings.py",
        ],
        "targets": [DATA_DIR, OUTPUT_DIR],
        "file_dep": ["./src/settings.py", "./config.toml"],
        "clean": [],
    }


data_sources = config_toml["data_sources"].copy()

# Check if we're being called by create_data_glimpses.py
is_data_glimpses = any("create_data_glimpses" in arg for arg in sys.argv)

bbg_skip = False
# Skip Bloomberg Terminal prompt when being imported by create_data_glimpses.py
if data_sources["bloomberg_terminal"] and not is_data_glimpses:
    # Interactive check for Bloomberg Terminal
    while True:
        response = (
            input("Is the Bloomberg Terminal open in the background? (yes/no/SKIP): ")
            .strip()
            .lower()
        )
        if response in ["yes"]:  # Fixed: should be 'in' not '=='
            print("Proceeding with Bloomberg Terminal enabled...")
            break
        elif response == "no":
            print(
                "Aborting. Please open the Bloomberg Terminal and keep it running in the background."
            )
            sys.exit(1)
        elif response in ["skip", ""]:
            print("Skipping Bloomberg Terminal data sources...")
            bbg_skip = True
            break
        else:
            print("Please enter 'yes', 'no', or 'skip'.")


# Load module requirements from datasets.toml
module_requirements_dict = load_module_requirements()

# Check which modules are available based on data sources
module_requirements = {}
for module_name, required_sources in module_requirements_dict.items():
    module_requirements[module_name] = all(
        data_sources.get(source, False) for source in required_sources
    )

use_cache = config_toml["cache"]["use_cache"]


def task_pull():
    """Pull selected data_sources based on config.toml configuration"""

    data_module = "cds_bond_basis"
    if module_requirements[data_module] and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_open_source_bond.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/pull_wrds_markit.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/pull_markit_mapping.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "corporate_bond_returns.parquet",
                DATA_DIR / data_module / "treasury_bond_returns.parquet",
                DATA_DIR / data_module / "markit_cds.parquet",
                DATA_DIR / data_module / "markit_red_crsp_link.parquet",
                DATA_DIR / data_module / "markit_cds_subsetted_to_crsp.parquet",
                DATA_DIR / data_module / "RED_and_ISIN_mapping.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/pull_open_source_bond.py",
                f"./src/{data_module}/pull_wrds_markit.py",
                f"./src/{data_module}/pull_markit_mapping.py",
            ],
            "clean": [],
        }

    data_module = "cds_returns"
    if module_requirements[data_module] and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_fed_yield_curve.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/pull_markit_cds.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/pull_fred.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "markit_cds.parquet",
                DATA_DIR / data_module / "fed_yield_curve.parquet",
                DATA_DIR / data_module / "fred.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/pull_fed_yield_curve.py",
                f"./src/{data_module}/pull_markit_cds.py",
                f"./src/{data_module}/pull_fred.py",
            ],
            "clean": [],
        }

    data_module = "commodities"
    if module_requirements[data_module] and not use_cache and not bbg_skip:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_bbg_commodities.py --DATA_DIR={DATA_DIR / data_module}"
            ],
            "targets": [
                DATA_DIR / data_module / "commodity_futures.parquet",
                DATA_DIR / data_module / "lme_metals.parquet",
                DATA_DIR / data_module / "gsci_indices.parquet",
            ],
            "file_dep": [f"./src/{data_module}/pull_bbg_commodities.py"],
        }

    data_module = "cip"
    if module_requirements[data_module] and not use_cache and not bbg_skip:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_bbg_foreign_exchange.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "fx_spot_rates.parquet",
                DATA_DIR / data_module / "fx_forward_points.parquet",
                DATA_DIR / data_module / "fx_interest_rates.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/pull_bbg_foreign_exchange.py",
            ],
            "clean": [],
        }

    # fmt: off
    data_module = "corp_bond_returns"
    if module_requirements[data_module] and not use_cache:
        from corp_bond_returns.pull_open_source_bond import DATA_INFO
        yield {
            "name": data_module,
            "actions": [f"python ./src/{data_module}/pull_open_source_bond.py --DATA_DIR={DATA_DIR / data_module}"],
            "targets": [
                DATA_DIR / data_module / info["parquet"]
                for info in DATA_INFO.values()
            ]
            + [
                DATA_DIR / data_module / f"{info['parquet'].replace('.parquet', '_README.pdf')}"
                for info in DATA_INFO.values()
            ],
            "file_dep": [f"./src/{data_module}/pull_open_source_bond.py"],
            "clean": [],
        }
    # fmt: on

    data_module = "foreign_exchange"
    if module_requirements[data_module] and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_wrds_fx.py --DATA_DIR={DATA_DIR / data_module}"
            ],
            "targets": [
                DATA_DIR / data_module / "fx_daily_data.parquet",
                DATA_DIR / data_module / "fx_monthly_data.parquet",
            ],
            "file_dep": [f"./src/{data_module}/pull_wrds_fx.py"],
        }

    data_module = "futures_returns"
    if module_requirements[data_module] and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_wrds_futures.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [DATA_DIR / data_module / "wrds_futures.parquet"],
            "file_dep": [f"./src/{data_module}/pull_wrds_futures.py"],
            "clean": [],
        }

    data_module = "fed_yield_curve"
    if module_requirements[data_module] and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_fed_yield_curve.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [DATA_DIR / data_module / "fed_yield_curve.parquet"],
            "file_dep": [f"./src/{data_module}/pull_fed_yield_curve.py"],
            "clean": [],
        }

    data_module = "he_kelly_manela"
    if module_requirements[data_module] and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_he_kelly_manela.py --DATA_DIR={DATA_DIR / data_module}"
            ],
            "targets": [
                DATA_DIR
                / data_module
                / "He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv",
                DATA_DIR / data_module / "He_Kelly_Manela_Factors_monthly.csv",
                DATA_DIR / data_module / "He_Kelly_Manela_Factors_daily.csv",
            ],
            "file_dep": [f"./src/{data_module}/pull_he_kelly_manela.py"],
            "clean": [],
        }

    data_module = "ken_french_data_library"
    if module_requirements[data_module] and not use_cache:
        from ken_french_data_library.pull_fama_french_25_portfolios import DATA_INFO

        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_fama_french_25_portfolios.py --DATA_DIR={DATA_DIR / data_module}"
            ],
            "targets": [
                DATA_DIR / "ken_french_data_library" / info["parquet"]
                for info in DATA_INFO.values()
            ],
            "file_dep": [f"./src/{data_module}/pull_fama_french_25_portfolios.py"],
            "clean": [],
        }

    data_module = "nyu_call_report"
    if module_requirements[data_module] and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_nyu_call_report.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [DATA_DIR / data_module / "nyu_call_report.parquet"],
            "file_dep": [f"./src/{data_module}/pull_nyu_call_report.py"],
            "clean": [],
        }

    data_module = "options"
    if module_requirements[data_module] and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_option_data.py --DATA_DIR={DATA_DIR / data_module}"
            ],
            "targets": [
                DATA_DIR / data_module / "data_1996-01_2012-01.parquet",
                DATA_DIR / data_module / "data_2012-02_2019-12.parquet",
            ],
            "file_dep": [f"./src/{data_module}/pull_option_data.py"],
            "clean": [],
        }

    data_module = "us_treasury_returns"
    if module_requirements[data_module] and not use_cache:
        # TODO: Create dataset that merges the treasury auction, runness, and treasury yield data
        # The code right now only pulls them separately.

        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_treasury_auction_stats.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/pull_CRSP_treasury.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "treasury_auction_stats.parquet",
                DATA_DIR / data_module / "CRSP_TFZ_DAILY.parquet",
                DATA_DIR / data_module / "CRSP_TFZ_INFO.parquet",
                DATA_DIR / data_module / "CRSP_TFZ_CONSOLIDATED.parquet",
                DATA_DIR / data_module / "CRSP_TFZ_with_runness.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/pull_treasury_auction_stats.py",
                f"./src/{data_module}/pull_CRSP_treasury.py",
            ],
            "clean": [],
        }

    data_module = "wrds_bank_premium"
    if module_requirements[data_module] and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_wrds_bank_premium.py --DATA_DIR={DATA_DIR / data_module}"
            ],
            "targets": [
                DATA_DIR / data_module / "wrds_struct_rel_ultimate.parquet",
                DATA_DIR / data_module / "wrds_call_research.parquet",
                DATA_DIR / data_module / "wrds_bank_crsp_link.parquet",
                DATA_DIR / data_module / "idrssd_to_lei.parquet",
                DATA_DIR / data_module / "lei_main.parquet",
                DATA_DIR / data_module / "lei_legalevents.parquet",
                DATA_DIR / data_module / "lei_otherentnames.parquet",
                DATA_DIR / data_module / "lei_successorentity.parquet",
            ],
            "file_dep": [f"./src/{data_module}/pull_wrds_bank_premium.py"],
            "clean": [],
        }

    data_module = "wrds_crsp_compustat"
    if module_requirements[data_module] and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_CRSP_Compustat.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "Compustat.parquet",
                DATA_DIR / data_module / "CRSP_stock_ciz.parquet",
                DATA_DIR / data_module / "CRSP_Comp_Link_Table.parquet",
                DATA_DIR / data_module / "FF_FACTORS.parquet",
            ],
            "file_dep": [f"./src/{data_module}/pull_CRSP_Compustat.py"],
            "clean": [],
        }


def task_format():
    """Pull selected data_sources based on config.toml configuration"""

    data_module = "cds_bond_basis"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/merge_cds_bond.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "Red_Data.parquet",
                DATA_DIR / data_module / "Final_data.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/merge_cds_bond.py",
            ],
            "clean": [],
        }
        yield from notebook_subtask(
            {
                "name": "summary_cds_bond_basis_ipynb",
                "notebook_path": "./src/cds_bond_basis/summary_cds_bond_basis_ipynb.py",
                "file_dep": [
                    "./src/cds_bond_basis/merge_cds_bond.py",
                ],
                "targets": [],
            },
        )

    data_module = "cds_returns"
    if module_requirements[data_module]:
        yield {
            "name": "calc_cds_returns",
            "actions": [
                f"python ./src/{data_module}/calc_cds_returns.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "markit_cds_returns.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/calc_cds_returns.py",
            ],
            "clean": [],
        }
        yield from notebook_subtask(
            {
                "name": "summary_cds_returns_ipynb",
                "notebook_path": "./src/cds_returns/summary_cds_returns_ipynb.py",
                "file_dep": [
                    "./src/cds_returns/calc_cds_returns.py",
                ],
                "targets": [],
            }
        )

    data_module = "cip"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/calc_cip.py --DATA_DIR={DATA_DIR / data_module}",
                # f"python ./src/{data_module}/cip_analysis.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "cip_spreads.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/calc_cip.py",
                # f"./src/{data_module}/cip_analysis.py",
            ],
            "clean": [],
        }
        yield from notebook_subtask(
            {
                "name": "summary_cip_ipynb",
                "notebook_path": "./src/cip/summary_cip_ipynb.py",
                "file_dep": [
                    "./src/cip/calc_cip.py",
                ],
                "targets": [],
            }
        )

    data_module = "commodities"
    if module_requirements[data_module] and not use_cache and not bbg_skip:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/calc_commodities_returns.py --DATA_DIR={DATA_DIR / data_module}"
            ],
            "targets": [
                DATA_DIR / data_module / "commodities_returns.parquet",
            ],
            "file_dep": [f"./src/{data_module}/calc_commodities_returns.py"],
        }

    data_module = "corp_bond_returns"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/calc_corp_bond_returns.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}"
            ],
            "targets": [
                DATA_DIR / data_module / "corp_bond_portfolio_returns.parquet",
                DATA_DIR / data_module / "ftsfr_corp_bond_returns.parquet",
                DATA_DIR / data_module / "ftsfr_corp_bond_portfolio_returns.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/calc_corp_bond_returns.py",
                f"./src/{data_module}/create_ftsfr_datasets.py",
            ],
            "clean": [],
        }
        yield from notebook_subtask(
            {
                "name": "summary_corp_bond_returns_ipynb",
                "notebook_path": "./src/corp_bond_returns/summary_corp_bond_returns_ipynb.py",
                "file_dep": [
                    "./src/corp_bond_returns/calc_corp_bond_returns.py",
                    "./src/corp_bond_returns/create_ftsfr_datasets.py",
                ],
                "targets": [],
            }
        )

    # data_module = "foreign_exchange"
    # if module_requirements[data_module]:
    #     yield {
    #         "name": data_module,
    #         "actions": [
    #             f"python ./src/{data_module}/pull_wrds_fx.py --DATA_DIR={DATA_DIR / data_module}"
    #         ],
    #         "targets": [
    #             DATA_DIR / data_module / "fx_daily_data.parquet",
    #             DATA_DIR / data_module / "fx_monthly_data.parquet",
    #         ],
    #     }

    data_module = "fed_yield_curve"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "ftsfr_treas_yield_curve_zero_coupon.parquet"
            ],
            "file_dep": [
                f"./src/{data_module}/pull_fed_yield_curve.py",
                f"./src/{data_module}/create_ftsfr_datasets.py",
            ],
            "clean": [],
        }

    data_module = "futures_returns"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/calc_futures_returns.py --DATA_DIR={DATA_DIR / data_module}",
                # f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [DATA_DIR / data_module / "futures_returns.parquet"],
            "file_dep": [
                f"./src/{data_module}/calc_futures_returns.py",
            ],
            "clean": [],
        }

    # if data_sources["ken_french_data_library"]:
    #     from ken_french_data_library.pull_fama_french_25_portfolios import DATA_INFO

    #     data_module = "ken_french_data_library"
    #     yield {
    #         "name": f"pull:{data_module}",
    #         "actions": [
    #             f"python ./src/{data_module}/pull_fama_french_25_portfolios.py --DATA_DIR={DATA_DIR / data_module}"
    #         ],
    #         "targets": [
    #             DATA_DIR / "ken_french_data_library" / info["parquet"]
    #             for info in DATA_INFO.values()
    #         ],
    #         "file_dep": [f"./src/{data_module}/pull_fama_french_25_portfolios.py"],
    #         "clean": [],
    #     }

    data_module = "nyu_call_report"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "ftsfr_nyu_call_report_leverage.parquet",
                DATA_DIR
                / data_module
                / "ftsfr_nyu_call_report_holding_company_leverage.parquet",
                DATA_DIR / data_module / "ftsfr_nyu_call_report_cash_liquidity.parquet",
                DATA_DIR
                / data_module
                / "ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/pull_nyu_call_report.py",
                f"./src/{data_module}/create_ftsfr_datasets.py",
            ],
            "clean": [],
        }

    # TODO
    data_module = "options"
    if module_requirements[data_module]:
        yield from notebook_subtask(
            {
                "name": "combined_filters",
                "notebook_path": "./src/options/combined_filters.ipynb",
                "file_dep": [
                    "./src/options/level_1_filters.py",
                    "./src/options/level_2_filters.py",
                    "./src/options/level_3_filters.py",
                ],
                "targets": [],
            },
        )
        yield from notebook_subtask(
            {
                "name": "portfolios",
                "notebook_path": "./src/options/portfolios.ipynb",
                "file_dep": [
                    "./src/options/level_1_filters.py",
                    "./src/options/level_2_filters.py",
                    "./src/options/level_3_filters.py",
                ],
                "targets": [
                    DATA_DIR / data_module / "hkm_portfolio_returns_1996-01_2019-12.parquet",
                    DATA_DIR / data_module / "cjs_portfolio_returns_1996-01_2019-12.parquet",
                ],
            },
        )
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "ftsfr_hkm_option_returns.parquet",
                DATA_DIR / data_module / "ftsfr_cjs_option_returns.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/create_ftsfr_datasets.py",
            ],
            "clean": [],
        }

    data_module = "us_treasury_returns"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/calc_treasury_run_status.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "issue_dates.parquet",
                DATA_DIR / data_module / "treasuries_with_run_status.parquet",
                DATA_DIR / data_module / "ftsfr_treas_bond_returns.parquet",
                DATA_DIR / data_module / "ftsfr_treas_bond_portfolio_returns.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/calc_treasury_run_status.py",
                f"./src/{data_module}/create_ftsfr_datasets.py",
            ],
            "clean": [],
        }
        yield from notebook_subtask(
            {
                "name": "summary_treasury_bond_returns_ipynb",
                "notebook_path": "./src/us_treasury_returns/summary_treasury_bond_returns_ipynb.py",
                "file_dep": [
                    "./src/us_treasury_returns/calc_treasury_bond_returns.py",
                ],
                "targets": [],
            }
        )

    # if data_sources["wrds_bank_premium"]:
    #     data_module = "wrds_bank_premium"
    #     yield {
    #         "name": f"pull:{data_module}",
    #         "actions": [
    #             f"python ./src/{data_module}/pull_wrds_bank_premium.py --DATA_DIR={DATA_DIR / data_module}"
    #         ],
    #         "targets": [
    #             DATA_DIR / data_module / "wrds_struct_rel_ultimate.parquet",
    #             DATA_DIR / data_module / "wrds_call_research.parquet",
    #             DATA_DIR / data_module / "wrds_bank_crsp_link.parquet",
    #             DATA_DIR / data_module / "idrssd_to_lei.parquet",
    #             DATA_DIR / data_module / "lei_main.parquet",
    #             DATA_DIR / data_module / "lei_legalevents.parquet",
    #             DATA_DIR / data_module / "lei_otherentnames.parquet",
    #             DATA_DIR / data_module / "lei_successorentity.parquet",
    #         ],
    #         "file_dep": [f"./src/{data_module}/pull_wrds_bank_premium.py"],
    #         "clean": [],
    #     }

    data_module = "wrds_crsp_compustat"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "ftsfr_CRSP_monthly_stock_ret.parquet",
                DATA_DIR / data_module / "ftsfr_CRSP_monthly_stock_retx.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/create_ftsfr_datasets.py",
                f"./src/{data_module}/pull_CRSP_Compustat.py",
                f"./src/{data_module}/calc_Fama_French_1993.py",
            ],
            "clean": [],
        }


models = config_toml["models"]
models_activated = [model for model in models if models[model]]


def task_forecast():
    """Generate forecast tasks for each combination of model and dataset."""

    available_datasets = get_available_datasets(module_requirements, DATA_DIR)

    for model in models_activated:
        for dataset_name, dataset_info in available_datasets.items():
            # For debugging purposes, print the full command line action here:
            # print(f"DATASET_PATH={dataset_info['path']} FTSFR_IS_BALANCED={dataset_info['is_balanced']} FREQUENCY={dataset_info['frequency']} DATA_DIR={DATA_DIR} OUTPUT_DIR={OUTPUT_DIR} pixi run main")
            yield {
                "name": f"{model}:{dataset_name}",
                "actions": [
                    CmdAction(
                        f"{PIXI_EXECUTABLE} run main",
                        cwd=f"./models/{model}",
                        env={
                            "DATASET_PATH": str(dataset_info["path"]),
                            "FREQUENCY": dataset_info["frequency"],
                            "SEASONALITY": str(dataset_info["seasonality"]),
                            "OUTPUT_DIR": str(OUTPUT_DIR),
                        },
                    )
                ],
                "targets": [
                    OUTPUT_DIR / "raw_results" / f"{model}_{dataset_name}_results.csv"
                ],
                "file_dep": [
                    f"./models/{model}/main.py",
                    f"./models/{model}/pixi.toml",
                ],
                "task_dep": [
                    f"format:{get_format_task_name(dataset_info['module'])}",
                ],
                "clean": [],
                "verbosity": 0,
            }


def task_assemble_results():
    """Assemble results from all model-dataset combinations."""

    available_datasets = get_available_datasets(module_requirements, DATA_DIR)

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
        "task_dep": [
            f"forecast:{model}:{dataset_name}"
            for model in models_activated
            for dataset_name in available_datasets
        ],
        "clean": [],
    }


def task_create_data_glimpses():
    """Create data glimpses"""
    # Get all files in the src directory recursively
    src_files = list(Path("./src").rglob("*"))
    # Filter to only include actual files (not directories) and exclude .ipynb files
    src_files = [str(f) for f in src_files if f.is_file() and f.suffix != ".ipynb"]

    return {
        "actions": [
            # "python ./src/create_data_glimpses.py --max-columns=20",
            "python ./src/create_data_glimpses.py --no-samples"  # --max-columns=20",
            # "python ./src/create_data_glimpses.py --no-samples --no-stats --max-columns=20",
        ],
        "targets": [
            "./docs_src/data_glimpses.md",
        ],
        "file_dep": src_files,
    }


def task_compile_sphinx_docs():
    """Compile Sphinx Docs"""

    # Get all files in the src directory recursively
    src_files = list(Path("./src").rglob("*"))
    # Filter to only include actual files (not directories) and exclude .ipynb files
    src_files = [str(f) for f in src_files if f.is_file() and f.suffix != ".ipynb"]

    def touch_file():
        """Touch a file"""
        Path("./docs/.nojekyll").touch()

    # Task dependencies on the format tasks that now contain the notebooks
    task_deps = []
    if module_requirements.get("cds_bond_basis", False):
        task_deps.append("format:summary_cds_bond_basis_ipynb")
    if module_requirements.get("cds_returns", False):
        task_deps.append("format:summary_cds_returns_ipynb")
    if module_requirements.get("cip", False):
        task_deps.append("format:summary_cip_ipynb")
    if module_requirements.get("corp_bond_returns", False):
        task_deps.append("format:summary_corp_bond_returns_ipynb")
    if module_requirements.get("us_treasury_returns", False):
        task_deps.append("format:summary_treasury_bond_returns_ipynb")

    return {
        "actions": [
            copy_dir_contents_to_folder("./docs_src", "./_docs"),
            copy_dir_contents_to_folder(
                OUTPUT_DIR / "_notebook_build", "./_docs/_notebook_build"
            ),
            "sphinx-build -M html ./_docs/ ./_docs/_build",
            copy_dir_contents_to_folder("./_docs/_build/html", "./docs"),
            touch_file,
        ],  # Use docs as build destination
        # "actions": ["sphinx-build -M html ./docs/ ./docs/_build"], # Previous standard organization
        "targets": [
            "./docs/index.html",
            "./docs/myst_markdown_demos.html",
            "./docs/.nojekyll",
        ],
        "file_dep": [
            "./docs_src/logo.png",
            "./docs_src/conf.py",
            "./docs_src/index.md",
            "./docs_src/data_sources_and_modules.md",
            "./docs_src/myst_markdown_demos.md",
            "./docs_src/data_glimpses.md",
            *src_files,
        ],
        "task_dep": task_deps,
        "clean": True,
    }


def task_compile_latex_docs():
    """Compile the LaTeX documents to PDFs"""
    if config_toml["reports"]["is_latex_installed"]:
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
