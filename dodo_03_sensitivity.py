"""
dodo_03_sensitivity.py - Data-cleaning sensitivity analysis

This file contains all tasks related to the "Sensitivity to cleaning method"
section of the paper. The work has three stages that interleave with
forecasting:

  1. Panel builders produce alternate-cleaning ftsfr_*.parquet files that
     are registered in datasets.toml. These must run BEFORE
     dodo_02_forecasting.py so the auto-generated jobs file picks them up.
  2. Replication tables (Dickerson-style long-short summaries) summarize
     the raw data and do not depend on forecasting.
  3. Sensitivity tables aggregate per-(dataset, model) forecasting metrics
     into LaTeX. These must run AFTER dodo_02_forecasting.py.

The numeric ordering dodo_01 -> dodo_02 -> dodo_03 -> dodo_04 groups files
by topic, not by execution order. A full rebuild is:

    doit -f dodo_01_pull.py
    doit -f dodo_03_sensitivity.py build_sensitivity_panels build_replication_tables
    doit -f dodo_02_forecasting.py
    doit -f dodo_03_sensitivity.py build_sensitivity_tables
    doit -f dodo_04_paper.py

build_str_dickerson_panels reads from an external `case_study_clean_trace`
repo (defaults to ~/GitRepositories/finm-32900-ALL/case_study_clean_trace,
override with CLEAN_TRACE_DIR). The subtask is skipped if the upstream
stage1_latest.parquet is not present.
"""

import os
from pathlib import Path

from dodo_common import (
    DATA_DIR,
    OUTPUT_DIR,
)


PAPER_DIR = OUTPUT_DIR / "forecasting" / "paper"
METRICS_DIR = OUTPUT_DIR / "forecasting" / "error_metrics"


def task_build_sensitivity_panels():
    """Build alternate-cleaning ftsfr_*.parquet panels for the sensitivity study.

    Each subtask produces one or more FTSFR long-format parquets registered in
    datasets.toml; dodo_02_forecasting.py auto-discovers and runs forecasting
    jobs on them.
    """

    data_module = "corp_bond_returns"
    yield {
        "name": "corp_bond_mmn_panels",
        "actions": [
            f"python ./src/{data_module}/build_mmn_comparison_panels.py",
        ],
        "targets": [
            DATA_DIR / data_module / "ftsfr_corp_bond_cs_deciles_mmn_biased.parquet",
            DATA_DIR / data_module / "ftsfr_corp_bond_cs_deciles_mmn_corrected.parquet",
        ],
        "file_dep": [
            f"./src/{data_module}/build_mmn_comparison_panels.py",
            f"./src/{data_module}/pull_open_source_bond.py",
        ],
        "clean": [],
        "verbosity": 2,
    }

    # build_str_dickerson_panels reads the case_study_clean_trace stage1 panel
    # from an external repo. Honor CLEAN_TRACE_DIR if set; otherwise default to
    # the location used during the original Dickerson replication. List the
    # external parquet as a file_dep so doit invalidates on upstream reruns;
    # if the path is missing the subtask is skipped (the build script would
    # error with a clear message).
    clean_trace_dir = Path(
        os.environ.get(
            "CLEAN_TRACE_DIR",
            Path.home()
            / "GitRepositories"
            / "finm-32900-ALL"
            / "case_study_clean_trace",
        )
    )
    clean_trace_stage1 = (
        clean_trace_dir / "_data" / "stage1" / "stage1_latest.parquet"
    )
    if clean_trace_stage1.exists():
        yield {
            "name": "corp_bond_str_panels",
            "actions": [
                f"python ./src/{data_module}/build_str_dickerson_panels.py",
            ],
            "targets": [
                DATA_DIR / data_module / "ftsfr_corp_bond_str_deciles_naive.parquet",
                DATA_DIR / data_module / "ftsfr_corp_bond_str_deciles_return_gap.parquet",
                PAPER_DIR / "str_dickerson_tabular.tex",
            ],
            "file_dep": [
                f"./src/{data_module}/build_str_dickerson_panels.py",
                str(clean_trace_stage1),
            ],
            "clean": [],
            "verbosity": 2,
        }

    data_module = "options"
    yield {
        "name": "options_filter_panels",
        "actions": [
            f"python ./src/{data_module}/build_filter_sensitivity_panels.py",
        ],
        "targets": [
            DATA_DIR / data_module / "ftsfr_cjs_option_returns_l1_filters.parquet",
            DATA_DIR / data_module / "ftsfr_cjs_option_returns_l3_filters.parquet",
        ],
        "file_dep": [
            f"./src/{data_module}/build_filter_sensitivity_panels.py",
            f"./src/{data_module}/build_cjs_portfolios.py",
            DATA_DIR / data_module / "L1_filtered_1996-01_2019-12.parquet",
            DATA_DIR / data_module / "spx_filtered_final_1996-01_2019-12.parquet",
        ],
        "clean": [],
        "verbosity": 2,
    }

    data_module = "us_treasury_returns"
    yield {
        "name": "treasury_gsw_panels",
        "actions": [
            f"python ./src/{data_module}/build_gsw_sensitivity_panels.py",
        ],
        "targets": [
            DATA_DIR / data_module / "ftsfr_treas_portfolios_permissive.parquet",
            DATA_DIR / data_module / "ftsfr_treas_portfolios_strict.parquet",
        ],
        "file_dep": [
            f"./src/{data_module}/build_gsw_sensitivity_panels.py",
            DATA_DIR / data_module / "CRSP_TFZ_with_runness_all_itypes.parquet",
        ],
        "clean": [],
        "verbosity": 2,
    }

    data_module = "wrds_crsp_compustat"
    yield {
        "name": "ff25_breakpoint_panels",
        "actions": [
            f"python ./src/{data_module}/build_ff25_breakpoint_panels.py",
        ],
        "targets": [
            DATA_DIR / data_module / "ftsfr_ff25_size_bm_nyse_breaks.parquet",
            DATA_DIR / data_module / "ftsfr_ff25_size_bm_crsp_breaks.parquet",
        ],
        "file_dep": [
            f"./src/{data_module}/build_ff25_breakpoint_panels.py",
            DATA_DIR / data_module / "Compustat.parquet",
            DATA_DIR / data_module / "CRSP_stock_ciz.parquet",
            DATA_DIR / data_module / "CRSP_Comp_Link_Table.parquet",
        ],
        "clean": [],
        "verbosity": 2,
    }


def task_build_replication_tables():
    """Build raw-data replication tables that do not depend on forecasting.

    `str_dickerson_tabular.tex` is emitted as a target of
    `build_sensitivity_panels:corp_bond_str_panels` (the same script writes
    both the parquets and the .tex), not as a separate replication subtask.
    """

    data_module = "corp_bond_returns"
    yield {
        "name": "mmn_dickerson",
        "actions": [
            f"python ./src/{data_module}/build_mmn_dickerson_replication.py",
        ],
        "targets": [
            DATA_DIR / data_module / "mmn_dickerson_replication.csv",
            PAPER_DIR / "mmn_dickerson_tabular.tex",
        ],
        "file_dep": [
            f"./src/{data_module}/build_mmn_dickerson_replication.py",
            f"./src/{data_module}/pull_open_source_bond.py",
        ],
        "clean": [],
        "verbosity": 2,
    }


def task_build_sensitivity_tables():
    """Aggregate forecasting metrics into the sensitivity LaTeX exhibits.

    file_dep is computed via glob over the error-metrics CSVs that
    dodo_02_forecasting.py emits per (dataset, model). The list may be empty
    before forecasting runs; doit will still list the task but won't be able
    to mark it up-to-date until at least the canonical metric files exist.
    """

    def _metric_files(*datasets):
        files = []
        for ds in datasets:
            ds_dir = METRICS_DIR / ds
            if ds_dir.exists():
                files.extend(sorted(str(p) for p in ds_dir.glob("*.csv")))
        return files

    mmn_datasets = (
        "ftsfr_corp_bond_cs_deciles_mmn_biased",
        "ftsfr_corp_bond_cs_deciles_mmn_corrected",
    )
    yield {
        "name": "mmn_sensitivity",
        "actions": [
            "python ./src/forecasting/build_mmn_sensitivity_table.py",
        ],
        "targets": [
            PAPER_DIR / "mmn_sensitivity_table.csv",
            PAPER_DIR / "mmn_sensitivity_tabular.tex",
        ],
        "file_dep": [
            "./src/forecasting/build_mmn_sensitivity_table.py",
            *_metric_files(*mmn_datasets),
        ],
        "clean": [],
        "verbosity": 2,
    }

    cleaning_datasets = (
        "ftsfr_cjs_option_returns_l1_filters",
        "ftsfr_cjs_option_returns_l3_filters",
        "ftsfr_ff25_size_bm_nyse_breaks",
        "ftsfr_ff25_size_bm_crsp_breaks",
        "ftsfr_treas_portfolios_permissive",
        "ftsfr_treas_portfolios_strict",
        "ftsfr_corp_bond_str_deciles_naive",
        "ftsfr_corp_bond_str_deciles_return_gap",
    )
    cleaning_panel_slugs = ("panel_a", "panel_b", "panel_c", "panel_d")
    yield {
        "name": "cleaning_sensitivity",
        "actions": [
            "python ./src/forecasting/build_cleaning_sensitivity_table.py",
        ],
        "targets": [
            *(PAPER_DIR / f"cleaning_sensitivity_{slug}.csv" for slug in cleaning_panel_slugs),
            PAPER_DIR / "cleaning_sensitivity_tabular.tex",
        ],
        "file_dep": [
            "./src/forecasting/build_cleaning_sensitivity_table.py",
            *_metric_files(*cleaning_datasets),
        ],
        "clean": [],
        "verbosity": 2,
    }
