"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

- treas_yield_curve_zero_coupon: Federal Reserve yield curve
- .. todo
- nyu_call_report_leverage: Total assets / Total equity
- nyu_call_report_holding_company_leverage: Total assets / Total equity
- nyu_call_report_cash_liquidity: Cash / Total assets
- nyu_call_report_holding_company_cash_liquidty: Cash flow / Total assets
- .. todo
- CRSP_monthly_stock_ret: CRSP stock returns
- CRSP_monthly_stock_retx: CRSP stock returns (without dividends)

TODO:

- SPX_option_ret: S&P 500 option returns
- CRSP_treasury_ret: CRSP treasury returns
- CRSP_treasury_ields: Cusip-level treasury yields
- fed_yield_curve: zero-coupon yields from the Federal Reserve, from Gurkaynak, Sack, and Wright (2007)
- fama_french_25_portfolios: Fama-French 25 portfolios, from Kenneth French's website
- nyu_call_report: NYU Call Report data
- wrds_bank_premium: Bank premium data from WRDS
- wrds_bank_premium_consolidated: Bank premium data from WRDS, consolidated
- wrds_bank_premium_consolidated_with_runness: Bank premium data from WRDS, consolidated with runness
- wrds_bank_premium_consolidated_with_runness: Bank premium data from WRDS, consolidated with runness

"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import polars as pl
import toml

from settings import config

BASE_DIR = config("BASE_DIR")
DATA_DIR = config("DATA_DIR")

# Read benchmarks.toml
with open(BASE_DIR / "benchmarks.toml", "r") as f:
    benchmarks = toml.load(f)

data_sources = benchmarks["data_sources"]

# data_sets_and_required_sources = {
#     "treas_yield_curve_zero_coupon": {
#         "fed_yield_curve",
#     },
#     "CRSP_monthly_stock_ret": {
#         "wrds_crsp_compustat",
#     },
#     "CRSP_monthly_stock_retx": {
#         "wrds_crsp_compustat",
#     },
#     "SPX_option_ret": {
#         "wrds_optionmetrics",
#     },
# }


# # available_datasets is the list of all datasets that can be loaded.
# # It is calculated by checking if the sources for each dataset are available,
# # as marked as "true" in the benchmarks.toml file.
# available_datasets = [
#     data_set
#     for data_set in data_sets_and_required_sources.keys()
#     if all(
#         source in data_sources and data_sources[source]
#         for source in data_sets_and_required_sources[data_set]
#     )
# ]


def load_dataset(dataset_name="nyu_call_report_leverage", dataframe_type="pandas"):
    # if dataset_name not in available_datasets:
    #     raise ValueError(
    #         f"Dataset {dataset_name} not found in available_datasets. Please check the benchmarks.toml file."
    #     )
    # fmt: off
    if dataset_name == "CRSP_monthly_stock_ret":
        file_path = DATA_DIR / "wrds_crsp_compustat" / "ftsfa_CRSP_monthly_stock_ret.parquet"
    elif dataset_name == "CRSP_monthly_stock_retx":
        file_path = DATA_DIR / "wrds_crsp_compustat" / "ftsfa_CRSP_monthly_stock_retx.parquet"
    elif dataset_name == "SPX_option_ret":
        file_path = DATA_DIR / "wrds_optionmetrics" / "ftsfa_SPX_option_ret.parquet"
    elif dataset_name == "nyu_call_report_leverage":
        file_path = DATA_DIR / "nyu_call_report" / "ftsfa_nyu_call_report_leverage.parquet"
    elif dataset_name == "nyu_call_report_holding_company_leverage":
        file_path = DATA_DIR / "nyu_call_report" / "ftsfa_nyu_call_report_holding_company_leverage.parquet"
    elif dataset_name == "nyu_call_report_cash_liquidity":
        file_path = DATA_DIR / "nyu_call_report" / "ftsfa_nyu_call_report_cash_liquidity.parquet"
    elif dataset_name == "nyu_call_report_holding_company_cash_liquidity":
        file_path = DATA_DIR / "nyu_call_report" / "ftsfa_nyu_call_report_holding_company_cash_liquidity.parquet"
    else:
        raise ValueError(
            f"Dataset {dataset_name} not found in available_datasets. Please check the benchmarks.toml file."
        )
    # fmt: on
    if dataframe_type == "pandas":
        df = pd.read_parquet(file_path)
    elif dataframe_type == "polars":
        df = pl.read_parquet(file_path)
    else:
        raise ValueError(
            f"Dataframe type {dataframe_type} not supported. Please choose 'pandas' or 'polars'."
        )

    return df
