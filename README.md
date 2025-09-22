# FTSFR: Financial Time-Series Forecasting Repository

FTSFR is an open benchmark for evaluating time-series forecasting methods across equity, credit, rates, currency, and real-asset markets. The repository automates data acquisition from both public and subscription-based sources, standardizes each dataset into a common panel format, and provides reproducible forecasting experiments and research outputs.

## Repository Highlights
- Modular data pipeline that mirrors the datasets described in `reports/draft_ftsfr.tex`
- Reproducible pulls for Bloomberg Terminal and WRDS feeds controlled through `subscriptions.toml`
- Standardized parquet datasets (`ftsfr_<name>.parquet`) with metadata defined in `datasets.toml`
- Forecasting jobs and evaluation utilities that benchmark classical and modern global models
- Documentation and LaTeX paper build scripts for publishing results

## Directory Guide
- `src/` – Data modules, forecasting code, and utilities (each asset class lives in its own subdirectory)
- `dodo_00_pull_bloomberg.py` – Bloomberg Terminal pulls (run only where Bloomberg Desktop API is available)
- `dodo_01_pull.py` – Core data pulls, formatting, and documentation tasks
- `dodo_02_forecasting.py` – Forecast generation pipeline
- `dodo_03_paper.py` – Report and website assembly
- `_data/` – Raw and processed data artifacts produced by the pipeline
- `_output/` – Forecasts, diagnostics, documentation assets, and timing logs
- `reports/` – LaTeX sources for the draft paper (`draft_ftsfr.tex` is the current manuscript)

## Environment Setup
1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or another Conda distribution.
2. Create the project environment and install core dependencies:
   ```bash
   conda create -n ftsfr python=3.12
   conda activate ftsfr
   pip install -r requirements.txt
   ```
3. To run the forecasting suite, install the additional dependencies:
   ```bash
   pip install -r requirements_forecasting.txt
   ```
4. (Optional) If you will pull Bloomberg data via the Bloomberg API, install their Python package (as noted here: https://www.bloomberg.com/professional/support/api-library/):
   ```bash
   python -m pip install --index-url=https://blpapi.bloomberg.com/repository/releases/python/simple/ blpapi
   ```
5. (Optional) Install TeX Live if you plan to compile the LaTeX paper or PDF documentation.
6. Confirm the tooling is available:
   ```bash
   doit --version
   ```

## Configure Credentials and Data Access
1. Create a `.env` file (see `.env.example`) containing identifiers such as WRDS usernames and any other secrets required by your subscriptions.
2. Edit `subscriptions.toml` to describe which data feeds and models you can access. The key sections are:
   ```toml
   [cache]
   use_cache = true          # set to false to force fresh pulls

   [data_sources]
   bloomberg = true          # enable when running on a Bloomberg terminal
   wrds = true               # enable for WRDS-sourced modules
   public = true             # toggle free/public datasets

   [models]
   darts_tcn = true
   prophet = false
   ```
   The `doit` tasks read this file to decide which modules to execute and whether cached extracts can be reused. Make sure the flags reflect the subscriptions and permissions available on the machine you are using.

## Data & Forecasting Workflow

### 1. Pull Bloomberg Terminal Data (optional)
`dodo_00_pull_bloomberg.py` contains every Bloomberg-only pull task. Launch it on a machine with the Bloomberg Desktop API running:
```bash
doit -f dodo_00_pull_bloomberg.py
```
Only the modules enabled in `subscriptions.toml` with `bloomberg = true` will execute. Targets are saved under `_data/<module>/`.

### 2. Pull and Format Core Datasets
`dodo_01_pull.py` is the main entry point for building the benchmark panel:
```bash
# Download and format data from all enabled sources
doit -f dodo_01_pull.py
```

### 3. Run Forecasts
Forecasting jobs live in `dodo_02_forecasting.py` and the `src/forecasting/` package. Typical usage:
```bash
doit -f dodo_02_forecasting.py
```
Job definitions are generated from `subscriptions.toml`, `datasets.toml`, and `src/forecasting/models_config.toml`. Results (error metrics, predictions, timing) land in `_output/forecasting/`.

### 4. Build Documentation and Paper (optional)
Use `dodo_03_paper.py` to rebuild the website and LaTeX report once data and forecasts are in place:
```bash
doit -f dodo_03_paper.py
```
This compiles the manuscript in `reports/draft_ftsfr.tex` and refreshes site assets under `docs/`.

## Working with Datasets and Modules
- Each data module under `src/` owns its extraction scripts (`pull_*`), formatting logic, and notebook utilities.
- `datasets.toml` documents every dataset, its frequency, and the data sources it depends on—use it to understand prerequisites before toggling modules in `subscriptions.toml`.
- Helper utilities in `src/determine_available_datasets.py` and `src/organize_ftsfr_datasets.py` ensure parquet outputs conform to the benchmark schema (`id`, `ds`, `y`, plus optional covariates).

## Forecast Outputs and Diagnostics
- Error metrics: `_output/forecasting/error_metrics/<dataset>/<model>.csv`
- Timing logs: `_output/forecasting/timing/<model>/<dataset>_timing.csv`
- Generated job list: `src/forecasting/forecasting_jobs.txt`

Check `_output/available_datasets.csv` and `_output/forecasting/summary/` (if present) to confirm coverage before writing up results.

## Reporting and Further Reading
- The full narrative, methodology, and empirical results are documented in `reports/draft_ftsfr.tex`.
- The static site under `docs/` mirrors the paper’s structure and is rebuilt through the dodo tasks above.

For questions or contributions, follow the structure outlined here to extend data modules, add forecasting models, or refine the documentation.
