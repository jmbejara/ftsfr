"""
dodo_00_pull_bloomberg.py - Bloomberg Terminal data pulling tasks

This file contains all Bloomberg Terminal-specific data pulling tasks.
Run this file only when the Bloomberg Terminal is open and available.
"""

# Import common utilities
from dodo_common import (
    DATA_DIR,
    load_subscriptions,
    load_all_module_requirements,
)

DOIT_CONFIG = {
    "backend": "sqlite3",
    "dep_file": "./.doit-db.sqlite",
}

# Load configuration
subscriptions_toml = load_subscriptions()
data_sources = subscriptions_toml["data_sources"].copy()

# Load module requirements from datasets.toml
module_requirements_dict = load_all_module_requirements()

# Check which modules are available based on data sources
module_requirements = {}
for module_name, required_sources in module_requirements_dict.items():
    module_requirements[module_name] = all(
        data_sources.get(source, False) for source in required_sources
    )

use_cache = subscriptions_toml["cache"]["use_cache"]


def task_pull():
    """Pull Bloomberg Terminal data sources"""

    data_module = "basis_tips_treas"
    if module_requirements.get(data_module, False) and not use_cache:
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
    if module_requirements.get(data_module, False) and not use_cache:
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

    data_module = "basis_treas_swap"
    if module_requirements.get(data_module, False) and not use_cache:
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

    data_module = "commodities"
    if module_requirements[data_module] and not use_cache:
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
    if module_requirements[data_module] and not use_cache:
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

    data_module = "foreign_exchange"
    if module_requirements[data_module] and not use_cache:
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
