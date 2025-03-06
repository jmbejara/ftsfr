import sys
from pathlib import Path

import toml

sys.path.insert(1, "./src/")

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))

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


def task_pull_subscription_data():
    """Pull selected data_sources based on benchmarks.toml configuration"""

    if data_sources["wrds_bank_premium"]:
        subfolder = "wrds_bank_premium"
        yield {
            "name": "wrds_bank_premium",
            "actions": [f"ipython ./src/{subfolder}/pull_wrds_bank_premium.py"],
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
            "name": "wrds_crsp_compustat",
            "actions": [f"ipython ./src/{subfolder}/pull_CRSP_Compustat.py"],
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
            "name": "wrds_crsp_stock",
            "actions": [f"ipython ./src/{subfolder}/pull_CRSP_stock.py"],
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
            "name": "wrds_crsp_treasury",
            "actions": [
                f"ipython ./src/{subfolder}/pull_treasury_auction_stats.py",
                f"ipython ./src/{subfolder}/calculate_ontherun.py",
                f"ipython ./src/{subfolder}/pull_CRSP_treasury.py",
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
        from wrds_corp_bonds.pull_corp_bonds import SUBFOLDER as subfolder
        yield {
            "name": "wrds_corp_bonds",
            "actions": [f"ipython ./src/{subfolder}/pull_corp_bonds.py"],
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
            "name": "wrds_markit",
            "actions": [
                f"ipython ./src/{subfolder}/pull_fed_yield_curve.py",
                f"ipython ./src/{subfolder}/pull_markit_cds.py",
                # f"ipython ./src/{subfolder}/calc_cds_returns.py", # TODO
            ],
            "targets": [
                DATA_DIR / subfolder / "markit_cds.parquet",
                # DATA_DIR / subfolder / "markit_cds_returns.parquet", # TODO
                DATA_DIR / subfolder / "fed_yield_curve.parquet",
            ],
            "file_dep": [
                f"./src/{subfolder}/pull_markit_cds.py",
                f"./src/{subfolder}/pull_fed_yield_curve.py",
            ],
            "clean": [],
        }


def task_pull_public_data():
    """Pull selected data_sources based on benchmarks.toml configuration"""

    if data_sources["fed_yield_curve"]:
        subfolder = "fed_yield_curve"
        yield {
            "name": subfolder,
            "actions": [f"ipython ./src/{subfolder}/pull_fed_yield_curve.py"],
            "targets": [DATA_DIR / subfolder / "fed_yield_curve.parquet"],
            "file_dep": [f"./src/{subfolder}/pull_fed_yield_curve.py"],
            "clean": [],
        }

    if data_sources["ken_french_data_library"]:
        from ken_french_data_library.pull_fama_french_25_portfolios import DATA_INFO

        subfolder = "ken_french_data_library"
        yield {
            "name": "ken_french_data_library",
            "actions": [f"ipython ./src/{subfolder}/pull_fama_french_25_portfolios.py"],
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
            "name": subfolder,
            "actions": [f"ipython ./src/{subfolder}/pull_nyu_call_report.py"],
            "targets": [DATA_DIR / subfolder / "nyu_call_report.parquet"],
            "file_dep": [f"./src/{subfolder}/pull_nyu_call_report.py"],
            "clean": [],
        }


# def task_run_benchmarks():
#     """Run selected model benchmarks based on benchmarks.toml configuration"""
#     models = benchmarks_file['models']

#     if models["var"]:
#         yield {
#             "actions": ["ipython ./src/models/var_benchmark.py"],
#             "targets": [OUTPUT_DIR / "var_results.parquet"],
#             "file_dep": ["./src/models/var_benchmark.py"],
#             "clean": [],
#         }
