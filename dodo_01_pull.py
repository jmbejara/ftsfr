"""
dodo_01_pull.py - Data pulling, formatting, and documentation tasks

This file contains all tasks related to:
- Pulling data from various sources
- Formatting and processing data
- Creating data glimpses
- Building documentation
"""

import sys
from pathlib import Path

# Import common utilities
from dodo_common import (
    DATA_DIR,
    OUTPUT_DIR,
    notebook_subtask,
    copy_dir_contents_to_folder,
    load_subscriptions,
    load_all_module_requirements,
)

from dependency_tracker import get_docs_task_dependencies

DOIT_CONFIG = {
    "backend": "sqlite3",
    "dep_file": "./.doit-db.sqlite",
}

# Load configuration
subscriptions_toml = load_subscriptions()
data_sources = subscriptions_toml["data_sources"].copy()

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
        if response in ["yes"]:
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
module_requirements_dict = load_all_module_requirements()

# Check which modules are available based on data sources
module_requirements = {}
for module_name, required_sources in module_requirements_dict.items():
    module_requirements[module_name] = all(
        data_sources.get(source, False) for source in required_sources
    )

use_cache = subscriptions_toml["cache"]["use_cache"]


def task_config():
    """Create empty directories for data and output if they don't exist"""

    return {
        "actions": [
            "python ./src/settings.py",
        ],
        "targets": [DATA_DIR, OUTPUT_DIR],
        "file_dep": ["./src/settings.py", "./subscriptions.toml"],
        "clean": [],
    }


def task_pull():
    """Pull selected data_sources based on subscriptions.toml configuration"""

    data_module = "basis_tips_treas"
    if module_requirements.get(data_module, False) and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/pull_fed_yield_curve.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/pull_fed_tips_yield_curve.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "fed_yield_curve_all.parquet",
                DATA_DIR / data_module / "fed_yield_curve.parquet",
                DATA_DIR / data_module / "fed_tips_yield_curve.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/pull_fed_yield_curve.py",
                f"./src/{data_module}/pull_fed_tips_yield_curve.py",
            ],
            "clean": [],
        }
    if module_requirements.get(data_module, False) and not use_cache and not bbg_skip:
        yield {
            "name": f"bbg:{data_module}",
            "actions": [
                f"python ./src/{data_module}/pull_bbg_treasury_inflation_swaps.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "treasury_inflation_swaps.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/pull_bbg_treasury_inflation_swaps.py",
            ],
            "clean": [],
        }

    data_module = "basis_treas_sf"
    if module_requirements.get(data_module, False) and not use_cache and not bbg_skip:
        yield {
            "name": f"bbg:{data_module}",
            "actions": [
                f"python ./src/{data_module}/pull_bbg_basis_treas_sf.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "treasury_2y_1.parquet",
                DATA_DIR / data_module / "treasury_2y_2.parquet",
                DATA_DIR / data_module / "treasury_5y_1.parquet",
                DATA_DIR / data_module / "treasury_5y_2.parquet",
                DATA_DIR / data_module / "treasury_10y_1.parquet",
                DATA_DIR / data_module / "treasury_10y_2.parquet",
                DATA_DIR / data_module / "treasury_20y_1.parquet",
                DATA_DIR / data_module / "treasury_20y_2.parquet",
                DATA_DIR / data_module / "treasury_30y_1.parquet",
                DATA_DIR / data_module / "treasury_30y_2.parquet",
                DATA_DIR / data_module / "ois.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/pull_bbg_basis_treas_sf.py",
            ],
            "clean": [],
        }
    if module_requirements.get(data_module, False) and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/format_bbg_basis_treas_sf.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "treasury_df.parquet",
                DATA_DIR / data_module / "last_day.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/format_bbg_basis_treas_sf.py",
            ],
            "clean": [],
        }

    data_module = "basis_treas_swap"
    if module_requirements.get(data_module, False) and not use_cache and not bbg_skip:
        yield {
            "name": f"bbg:{data_module}",
            "actions": [
                f"python ./src/{data_module}/pull_bbg_treas_swap.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "raw_tyields.parquet",
                DATA_DIR / data_module / "raw_syields.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/pull_bbg_treas_swap.py",
            ],
            "clean": [],
        }

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
                f"python ./src/{data_module}/pull_bbg_commodities_basis.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/pull_bbg_active_commodities.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "commodity_futures.parquet",
                DATA_DIR / data_module / "lme_metals.parquet",
                DATA_DIR / data_module / "gsci_indices.parquet",
                DATA_DIR / data_module / "commodity_futures_active.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/pull_bbg_commodities_basis.py",
                f"./src/{data_module}/pull_bbg_active_commodities.py",
            ],
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
                f"python ./src/{data_module}/pull_wrds_fx.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "fx_daily_data.parquet",
                DATA_DIR / data_module / "fx_monthly_data.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/pull_wrds_fx.py",
            ],
        }

    if module_requirements[data_module] and not use_cache and not bbg_skip:
        yield {
            "name": f"bbg:{data_module}",
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
    """Format and process pulled data into standardized datasets"""

    data_module = "basis_tips_treas"
    if module_requirements.get(data_module, False):
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/compute_tips_treasury.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/generate_figures.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/generate_latex_table.py --OUTPUT_DIR={OUTPUT_DIR}",
            ],
            "targets": [
                DATA_DIR / data_module / "tips_treasury_implied_rf.parquet",
                OUTPUT_DIR / "tips_treasury_spreads.png",
                OUTPUT_DIR / "tips_treasury_summary.csv",
                OUTPUT_DIR / "tips_treasury_summary_table.tex",
            ],
            "file_dep": [
                f"./src/{data_module}/compute_tips_treasury.py",
                f"./src/{data_module}/generate_figures.py",
                f"./src/{data_module}/generate_latex_table.py",
            ],
            "clean": [],
        }

        yield from notebook_subtask(
            {
                "name": "summary_basis_tips_treas_ipynb",
                "notebook_path": "./src/basis_tips_treas/summary_basis_tips_treas_ipynb.py",
                "file_dep": [
                    DATA_DIR / data_module / "tips_treasury_implied_rf.parquet",
                    f"./src/{data_module}/generate_figures.py",
                ],
                "targets": [],
            }
        )

    data_module = "basis_treas_sf"
    if module_requirements.get(data_module, False):
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/calc_basis_treas_sf.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "treasury_sf_output.parquet",
            ],
            "file_dep": [
                DATA_DIR / data_module / "treasury_df.parquet",
                DATA_DIR / data_module / "ois.parquet",
                DATA_DIR / data_module / "last_day.parquet",
                f"./src/{data_module}/calc_basis_treas_sf.py",
            ],
            "clean": [],
        }
        yield from notebook_subtask(
            {
                "name": "summary_basis_treas_sf_ipynb",
                "notebook_path": f"./src/{data_module}/summary_basis_treas_sf_ipynb.py",
                "file_dep": [
                    f"./src/{data_module}/calc_basis_treas_sf.py",
                    DATA_DIR / data_module / "treasury_sf_output.parquet",
                ],
                "targets": [],
            }
        )

    data_module = "basis_treas_swap"
    if module_requirements.get(data_module, False):
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/calc_swap_spreads.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/supplementary.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/plot_figure.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "calc_merged.parquet",
                DATA_DIR / data_module / "replicated_swap_spread_arb_figure.png",
                DATA_DIR / data_module / "updated_swap_spread_arb_figure.png",
                DATA_DIR / data_module / "table.txt",
            ],
            "file_dep": [
                f"./src/{data_module}/calc_swap_spreads.py",
                f"./src/{data_module}/supplementary.py",
                f"./src/{data_module}/plot_figure.py",
            ],
            "clean": [],
        }
        yield from notebook_subtask(
            {
                "name": "summary_basis_treas_swap_ipynb",
                "notebook_path": f"./src/{data_module}/summary_basis_treas_swap_ipynb.py",
                "file_dep": [
                    f"./src/{data_module}/pull_bbg_treas_swap.py",
                    f"./src/{data_module}/calc_swap_spreads.py",
                    f"./src/{data_module}/plot_figure.py",
                    f"./src/{data_module}/supplementary.py",
                ],
                "targets": [],
            }
        )

    data_module = "cds_bond_basis"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/merge_cds_bond.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "Red_Data.parquet",
                DATA_DIR / data_module / "Final_data.parquet",
                DATA_DIR / data_module / "ftsfr_CDS_bond_basis_aggregated.parquet",
                DATA_DIR / data_module / "ftsfr_CDS_bond_basis_non_aggregated.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/merge_cds_bond.py",
                f"./src/{data_module}/create_ftsfr_datasets.py",
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
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/calc_cds_returns.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "markit_cds_returns.parquet",
                DATA_DIR / data_module / "markit_cds_contract_returns.parquet",
                DATA_DIR / data_module / "ftsfr_CDS_contract_returns.parquet",
                DATA_DIR / data_module / "ftsfr_CDS_portfolio_returns.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/calc_cds_returns.py",
                f"./src/{data_module}/create_ftsfr_datasets.py",
            ],
            "clean": [],
            "verbosity": 2,
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
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}",
            ],
            "targets": [
                DATA_DIR / data_module / "cip_spreads.parquet",
                DATA_DIR / data_module / "ftsfr_CIP_spreads.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/calc_cip.py",
                # f"./src/{data_module}/cip_analysis.py",
                f"./src/{data_module}/create_ftsfr_datasets.py",
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
    if module_requirements[data_module] and not use_cache:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/calc_commodities_returns.py --DATA_DIR={DATA_DIR / data_module}"
            ],
            "targets": [
                DATA_DIR / data_module / "commodities_returns.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/calc_commodities_returns.py",
                f"./src/{data_module}/replicate_cmdty.py",
            ],
        }

    data_module = "corp_bond_returns"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/calc_corp_bond_returns.py --DATA_DIR={DATA_DIR / data_module}",
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}",
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

    data_module = "foreign_exchange"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}"
            ],
            "file_dep": [
                f"./src/{data_module}/create_ftsfr_datasets.py",
            ],
            "targets": [
                DATA_DIR / data_module / "ftsfr_FX_returns.parquet",
            ],
        }

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

    data_module = "he_kelly_manela"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}"
            ],
            "targets": [
                DATA_DIR
                / data_module
                / "ftsfr_he_kelly_manela_factors_monthly.parquet",
                DATA_DIR / data_module / "ftsfr_he_kelly_manela_factors_daily.parquet",
                DATA_DIR / data_module / "ftsfr_he_kelly_manela_all.parquet",
            ],
            "file_dep": [
                f"./src/{data_module}/create_ftsfr_datasets.py",
            ],
            "clean": [],
        }

    data_module = "ken_french_data_library"
    if module_requirements[data_module]:
        yield {
            "name": data_module,
            "actions": [
                f"python ./src/{data_module}/create_ftsfr_datasets.py --DATA_DIR={DATA_DIR / data_module}"
            ],
            "targets": [
                DATA_DIR
                / data_module
                / "ftsfr_french_portfolios_25_daily_size_and_bm.parquet",
                DATA_DIR
                / data_module
                / "ftsfr_french_portfolios_25_daily_size_and_op.parquet",
                DATA_DIR
                / data_module
                / "ftsfr_french_portfolios_25_daily_size_and_inv.parquet",
            ],
            "file_dep": [f"./src/{data_module}/create_ftsfr_datasets.py"],
            "clean": [],
        }

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
                    DATA_DIR
                    / data_module
                    / "hkm_portfolio_returns_1996-01_2019-12.parquet",
                    DATA_DIR
                    / data_module
                    / "cjs_portfolio_returns_1996-01_2019-12.parquet",
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

    task_deps = get_docs_task_dependencies(module_requirements)

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
