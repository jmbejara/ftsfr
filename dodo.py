import sys
from pathlib import Path

import toml
from doit.action import CmdAction

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

def task_source():
    """Pull selected data_sources based on benchmarks.toml configuration"""

    if data_sources["fed_yield_curve"]:
        subfolder = "fed_yield_curve"
        yield {
            "name": f"{subfolder}:pull",
            "actions": [
                f"python ./src/{subfolder}/pull_fed_yield_curve.py --DATA_DIR={DATA_DIR / subfolder}",
            ],
            "targets": [DATA_DIR / subfolder / "fed_yield_curve.parquet"],
            "file_dep": [f"./src/{subfolder}/pull_fed_yield_curve.py"],
            "clean": [],
        }
        yield {
            "name": f"{subfolder}:format",
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
            "name": f"{subfolder}:pull",
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
            "name": f"{subfolder}:pull",
            "actions": [
                f"python ./src/{subfolder}/pull_nyu_call_report.py --DATA_DIR={DATA_DIR / subfolder}"
            ],
            "targets": [DATA_DIR / subfolder / "nyu_call_report.parquet"],
            "file_dep": [f"./src/{subfolder}/pull_nyu_call_report.py"],
            "clean": [],
        }
        yield {
            "name": f"{subfolder}:format",
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
            "name": f"{subfolder}:pull",
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
            "name": f"{subfolder}:pull",
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
            "name": "CRSP_stock:pull",
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
            "name": "CRSP_treasury:pull",
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
            "name": f"{subfolder}:pull",
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
            "name": f"{subfolder}:pull",
            "actions": [
                f"python ./src/{subfolder}/pull_fed_yield_curve.py --DATA_DIR={DATA_DIR / subfolder}",
                f"python ./src/{subfolder}/pull_markit_cds.py --DATA_DIR={DATA_DIR / subfolder}",
                # f"ipython ./src/{subfolder}/calc_cds_returns.py", # TODO
            ],
            "targets": [
                DATA_DIR / subfolder / "markit_cds.parquet",
                # DATA_DIR / subfolder / "markit_cds_returns.parquet", # TODO
                DATA_DIR / subfolder / "fed_yield_curve.parquet",
            ],
            "file_dep": [
                f"./src/{subfolder}/pull_fed_yield_curve.py",
                f"./src/{subfolder}/pull_markit_cds.py",
            ],
            "clean": [],
        }


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
                CmdAction(
                    "pixi run main", cwd="./models/simple_exponential_smoothing"
                )
            ],
            "targets": [OUTPUT_DIR / "raw_results" / "ses_results.csv"],
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
