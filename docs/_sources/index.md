# Financial Time Series Forecasting Repository (FTSFR)

**A standardized macro-finance data repository for global time series forecasting research**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/jmbejara/ftsfr/)

---

## Objectives

The Financial Time Series Forecasting Repository (FTSFR) addresses a critical gap in quantitative finance research: the lack of standardized datasets for evaluating and comparing time series forecasting models. When researchers evaluate their own forecasting models on their own arbitrarily chosen datasets, apples-to-apples comparisons across forecasting algorithms are not possible.

This repository provides a comprehensive collection of financial and macroeconomic datasets that have been cleaned, formatted, and standardized according to academic best practices. We hope that this repository will serve as a useful time series forecasting benchmark for the research community.

**Key objectives:**
- Provide **apples-to-apples comparisons** for time series forecasting algorithms
- Ensure datasets are prepared using consistent methodology
- Follow academic standards from published research
- Enable reproducible forecasting benchmarks across financial domains

We are inspired by the work of the [Monash Time Series Forecasting Repository](https://forecastingdata.org/), which provides freely available datasets for benchmarking time series forecasting models. However, we focus on datasets from finance and economics, which often require subscriptions to access but are commonly available at universities through services like WRDS (Wharton Research Data Services).

### Our Solution

Although most of the data in this repository requires a subscription to access, we provide a codebase that **automates the end-to-end process** for assembling various financial and macroeconomic data, from the data pull step to the final cleaning and transformation step. Our [quickstart guide](data_sources_and_modules.md#installation) provides a simple guide to get you started.

---

## Datasets

Our benchmark includes **25 datasets** spanning multiple financial domains. Each dataset follows cleaning procedures from published academic papers, ensuring that benchmarks reflect established best practices.

### Dataset Overview

| Dataset Name | Description | Citation |
|:-------------|:------------|:---------|
| **Returns Data** | | |
| CDS Contract | Monthly returns for individual CDS contracts (follows Palhares 2012) | Palhares (2012) |
| CDS Portfolio | 20 CDS portfolios by tenor and credit quality | He, Kelly, Manela (2017) |
| Commodity | Monthly returns for commodity futures | Yang (2013) |
| Corporate Bond | Monthly returns for individual corporate bonds from TRACE | Dickerson et al. (2024); Nozawa (2017) |
| Corporate Portfolio | Monthly returns for corporate bond portfolios by credit spread | Nozawa (2017) |
| CRSP Stock | Monthly stock returns from CRSP database | Fama & French (1993) |
| FF25 Size-BM | Daily Fama-French 25 portfolios: size and book-to-market | Fama & French (1993) |
| FX | Daily foreign exchange returns vs USD | Lettau et al. (2014) |
| SPX Options Portfolios | Monthly returns for individual SPX option contracts | Constantinides et al. (2013) |
| Treasury Bond | Monthly returns for individual Treasury bonds from CRSP | Gürkaynak et al. (2007) |
| Treasury Portfolio | Monthly returns for Treasury bond portfolios by maturity | Gürkaynak et al. (2007) |
| **Basis Spread Data** | | |
| CDS-Bond | Monthly CDS-bond basis spreads | Siriwardane et al. (2022) |
| CIP | Monthly covered interest parity deviations | Du et al. (2018) |
| TIPS-Treasury | Monthly TIPS-Treasury basis spreads | Fleckenstein et al. (2014) |
| Treasury-SF | Monthly Treasury-SF arbitrage spreads | Jermann (2020) |
| Treasury-Swap | Monthly Treasury-Swap arbitrage spreads | Siriwardane et al. (2022) |
| **Other Financial Data** | | |
| Bank Cash Liquidity | Quarterly cash liquidity from call report data | Drechsler et al. (2017) |
| Bank Leverage | Quarterly leverage ratios from call report data | Drechsler et al. (2017) |
| BHC Cash Liquidity | Quarterly bank holding company cash liquidity | Drechsler et al. (2017) |
| BHC Leverage | Quarterly bank holding company leverage ratios | Drechsler et al. (2017) |
| HKM Daily Factor | Intermediary risk factors (capital ratio, risk factor, returns, leverage) | He, Kelly, Manela (2017) |
| HKM Monthly Factor | Same as above, but monthly | He, Kelly, Manela (2017) |
| Treasury Yield Curve | Daily Nelson-Siegel-Svensson zero-coupon yields (1-30 years) | Gürkaynak et al. (2007) |

*Source: Authors' analysis*

### Dataset Statistics

The following table provides key statistics for each dataset after filtering and cleaning:

| Dataset | Frequency | Entities (Before) | Entities (After) | Retention | Median Length (After) | Date Range |
|:--------|:----------|------------------:|-----------------:|----------:|----------------------:|:-----------|
| **Basis Spreads** | | | | | | |
| CDS-Bond | Monthly | 3,402 | 1,516 | 44.6% | 57 | 2002-09 to 2022-09 |
| CIP | Monthly | 8 | 8 | 100.0% | 272 | 2001-12 to 2025-02 |
| TIPS-Treasury | Monthly | 4 | 4 | 100.0% | 251 | 2004-07 to 2025-05 |
| Treasury-SF | Monthly | 5 | 5 | 100.0% | 247 | 2004-06 to 2025-01 |
| Treasury-Swap | Monthly | 7 | 7 | 100.0% | 207 | 2001-12 to 2025-08 |
| **Returns (Portfolios)** | | | | | | |
| CDS Portfolio | Monthly | 20 | 4 | 20.0% | 276 | 2001-01 to 2023-12 |
| Corporate Portfolio | Monthly | 10 | 10 | 100.0% | 242 | 2002-08 to 2022-09 |
| FF25 Size-BM | Daily | 25 | 25 | 100.0% | 36,160 | 1926-07 to 2025-06 |
| SPX Options Portfolios | Monthly | 18 | 18 | 100.0% | 288 | 1996-01 to 2019-12 |
| Treasury Portfolio | Monthly | 10 | 10 | 100.0% | 668 | 1970-01 to 2025-08 |
| **Returns (Disaggregated)** | | | | | | |
| CDS Contract | Monthly | 6,552 | 234 | 3.6% | 54 | 2001-02 to 2023-12 |
| CRSP Stock | Monthly | 26,757 | 25,095 | 93.8% | 94 | 1926-01 to 2024-12 |
| CRSP Stock (ex-div) | Monthly | 26,757 | 25,095 | 93.8% | 94 | 1926-01 to 2024-12 |
| Commodity | Monthly | 23 | 23 | 100.0% | 511 | 1970-01 to 2025-08 |
| Corporate Bond | Monthly | 23,473 | 16,719 | 71.2% | 52 | 2002-08 to 2022-09 |
| FX | Monthly | 9 | 9 | 100.0% | 276 | 1999-02 to 2025-02 |
| Treasuries | Monthly | 2,054 | 1,912 | 93.1% | 49 | 1970-01 to 2025-08 |
| **Other** | | | | | | |
| BHC Cash Liquidity | Quarterly | 13,770 | 6,351 | 46.1% | 69 | 1976-03 to 2020-03 |
| BHC Leverage | Quarterly | 13,761 | 6,653 | 48.3% | 67 | 1976-03 to 2020-03 |
| Bank Cash Liquidity | Quarterly | 23,862 | 17,383 | 72.8% | 82 | 1976-03 to 2020-03 |
| Bank Leverage | Quarterly | 22,965 | 17,295 | 75.3% | 82 | 1976-03 to 2020-03 |
| HKM All Factor | Monthly | 4 | 4 | 100.0% | 516 | 1970-01 to 2012-12 |
| HKM Daily Factor | Daily | 4 | 4 | 100.0% | 6,918 | 2000-01 to 2018-12 |
| HKM Monthly Factor | Monthly | 4 | 4 | 100.0% | 587 | 1970-01 to 2018-11 |
| Treasury Yield Curve | Daily | 30 | 30 | 100.0% | 17,902 | 1961-06 to 2025-09 |

*Source: Generated automatically from dataset processing pipeline*

---

## Forecasting Results

We provide comprehensive baseline results across all datasets using a diverse set of forecasting models, from classical statistical methods to modern deep learning architectures. Results are evaluated using multiple metrics to provide complementary perspectives on forecasting performance.

### Overall Model Performance

The table below shows median and mean performance statistics across all 25 datasets. **MASE** (Mean Absolute Scaled Error) is the primary metric used in forecasting literature, with values < 1.0 indicating better performance than a seasonal naive benchmark. **Relative MASE** compares each model to the Historic Average baseline. **R²** (out-of-sample R²) measures the percentage reduction in mean squared error relative to predicting the historical average.

| Model | N | Med MASE | Mean MASE | Med Rel MASE | Mean Rel MASE | Med R² | Mean R² |
|:------|--:|---------:|----------:|-------------:|--------------:|-------:|--------:|
| **NBEATS** | 25 | **0.786** | 0.950 | **0.477** | 0.606 | 0.098 | -0.062 |
| NHITS | 25 | 0.806 | **0.912** | 0.488 | 0.611 | 0.333 | -0.077 |
| Theta | 25 | 0.814 | 0.927 | 0.505 | **0.599** | **0.379** | -0.019 |
| DLinear | 25 | 0.829 | 0.977 | 0.554 | 0.606 | 0.307 | 0.019 |
| NLinear | 25 | 0.837 | 0.944 | 0.518 | 0.612 | 0.353 | -1.755 |
| ARIMA | 25 | 0.841 | 0.933 | 0.498 | 0.622 | 0.359 | **0.278** |
| Transformer | 25 | 0.852 | 0.998 | 0.491 | 0.602 | 0.245 | 0.185 |
| KAN | 25 | 0.861 | 1.063 | 0.481 | 0.641 | -0.030 | 0.003 |
| TiDE | 25 | 0.875 | 0.969 | 0.586 | 0.634 | 0.234 | -0.200 |
| SES | 25 | 1.020 | 1.359 | 0.638 | 0.700 | 0.169 | -0.043 |
| DeepAR | 25 | 1.148 | 1.791 | 0.851 | 0.837 | -0.081 | -4.514 |
| HistAvg | 25 | 1.819 | 2.957 | — | — | 0.000 | 0.000 |

*Note: MASE shows absolute performance (lower is better), Relative MASE shows performance relative to Historic Average (lower is better), and R² shows out-of-sample predictive power (higher is better). Models are sorted by median MASE. Bold indicates best performance in each column.*

*Sources: Bloomberg, Board of Governors of the Federal Reserve System, Center for Research in Security Prices, U.S. Call Reports, WRDS TRACE, OptionMetrics, S&P Global, Authors' analysis*

### Performance by Dataset Category

Model rankings vary significantly across different types of financial data. The table below disaggregates performance by dataset category:

**Basis Spreads**

| Model | N | Med MASE | Mean MASE | Med Rel MASE | Mean Rel MASE | Med R² | Mean R² |
|:------|--:|---------:|----------:|-------------:|--------------:|-------:|--------:|
| **NLinear** | 5 | **0.395** | **0.637** | 0.299 | **0.407** | 0.514 | **0.651** |
| Theta | 5 | 0.411 | 0.672 | 0.297 | 0.449 | 0.544 | 0.529 |
| Transformer | 5 | 0.421 | 0.723 | 0.305 | 0.475 | 0.581 | 0.563 |
| ARIMA | 5 | 0.446 | 0.700 | 0.306 | 0.457 | 0.539 | 0.588 |
| DLinear | 5 | 0.455 | 0.836 | 0.495 | 0.466 | 0.431 | 0.562 |
| NHITS | 5 | 0.464 | 0.664 | **0.272** | 0.446 | 0.580 | 0.550 |
| KAN | 5 | 0.465 | 0.766 | 0.337 | 0.497 | 0.405 | 0.509 |
| TiDE | 5 | 0.491 | 0.862 | 0.311 | 0.627 | 0.517 | 0.185 |
| DeepAR | 5 | 0.567 | 1.147 | 0.693 | 0.615 | 0.186 | 0.102 |
| NBEATS | 5 | 0.587 | 0.685 | 0.329 | 0.441 | **0.706** | 0.552 |
| SES | 5 | 0.939 | 1.208 | 0.601 | 0.672 | 0.345 | 0.250 |
| HistAvg | 5 | 1.784 | 2.126 | — | — | 0.000 | 0.000 |

**Returns**

| Model | N | Med MASE | Mean MASE | Med Rel MASE | Mean Rel MASE | Med R² | Mean R² |
|:------|--:|---------:|----------:|-------------:|--------------:|-------:|--------:|
| **KAN** | 12 | **0.803** | 1.183 | 0.959 | 0.893 | -0.073 | -0.267 |
| Transformer | 12 | 0.815 | 1.119 | 0.948 | 0.840 | -0.043 | -0.099 |
| NBEATS | 12 | 0.825 | 1.024 | 0.955 | 0.858 | -0.059 | -0.513 |
| DLinear | 12 | 0.827 | 0.988 | 0.974 | 0.837 | -0.029 | -0.469 |
| NLinear | 12 | 0.845 | 1.015 | 0.992 | 0.876 | -0.184 | -4.149 |
| SES | 12 | 0.853 | 1.501 | 0.965 | 0.899 | -0.021 | -0.437 |
| TiDE | 12 | 0.859 | **0.975** | **0.913** | **0.833** | -0.077 | -0.742 |
| Theta | 12 | 0.860 | 1.045 | 0.965 | 0.862 | -0.015 | -0.614 |
| NHITS | 12 | 0.869 | 1.000 | 0.996 | 0.881 | -0.156 | -0.675 |
| ARIMA | 12 | 0.873 | 1.035 | 1.003 | 0.902 | -0.073 | -0.009 |
| HistAvg | 12 | 0.873 | 2.519 | — | — | **0.000** | **0.000** |
| DeepAR | 12 | 1.181 | 2.071 | 1.007 | 1.075 | -0.125 | -7.815 |

**Other (Bank Metrics, Factors, Yield Curve)**

| Model | N | Med MASE | Mean MASE | Med Rel MASE | Mean Rel MASE | Med R² | Mean R² |
|:------|--:|---------:|----------:|-------------:|--------------:|-------:|--------:|
| **NHITS** | 8 | **0.796** | 0.937 | 0.327 | 0.308 | 0.465 | 0.429 |
| Theta | 8 | 0.811 | **0.908** | **0.313** | **0.298** | 0.474 | **0.531** |
| ARIMA | 8 | 0.830 | 0.926 | 0.328 | 0.305 | **0.481** | 0.514 |
| DLinear | 8 | 0.839 | 1.049 | 0.378 | 0.346 | 0.380 | 0.411 |
| NBEATS | 8 | 0.867 | 1.004 | 0.380 | 0.331 | 0.459 | 0.232 |
| Transformer | 8 | 0.888 | 0.988 | 0.363 | 0.326 | 0.437 | 0.375 |
| KAN | 8 | 0.912 | 1.069 | 0.404 | 0.353 | 0.413 | 0.090 |
| TiDE | 8 | 0.918 | 1.028 | 0.362 | 0.341 | 0.414 | 0.372 |
| NLinear | 8 | 0.925 | 1.031 | 0.412 | 0.344 | 0.398 | 0.333 |
| SES | 8 | 1.118 | 1.242 | 0.491 | 0.421 | 0.292 | 0.364 |
| DeepAR | 8 | 1.359 | 1.773 | 0.473 | 0.619 | 0.043 | -2.446 |
| HistAvg | 8 | 2.653 | 4.132 | — | — | 0.000 | 0.000 |

*Note: Metrics are computed within each dataset category. Lower MASE/Relative MASE values indicate better performance; higher R² values indicate better performance. Bold indicates best performance in each column.*

### Key Findings

- **Basis spreads** exhibit pronounced seasonal structure and mean reversion, where models like **NLinear**, **NHITS**, and **NBEATS** excel by decomposing series into trend and seasonal components
- **Asset returns** are notoriously difficult to forecast, with nearly all models achieving R² values near zero—consistent with decades of empirical asset pricing research showing that the historical mean is hard to beat
- **Other datasets** (bank metrics, intermediary factors, yield curves) favor classical approaches like **Theta** and **ARIMA**, which balance flexibility with parsimony

---

## Important Links

- **GitHub Repository**: [https://github.com/jmbejara/ftsfr/](https://github.com/jmbejara/ftsfr/)
- **Documentation**: Browse the sections below for detailed information
- **Paper**: Bejarano, J. et al. (2024). Financial Time Series Forecasting Repository: A Standardized Macro-Finance Data Repository for Global Time Series Forecasting. *[Working Paper]*

### Data Sources

Our repository leverages both **publicly available** and **subscription-based** data sources:

**Public Data Sources** *(No subscription required)*
- He, Kelly, Manela test portfolios
- Ken French Data Library
- Federal Reserve economic data (FRED)
- NYU Call Report archive
- Open Source Bond Asset Pricing

**Academic Subscription Sources** *(Commonly available via university subscriptions)*
- WRDS Compustat North America
- WRDS CRSP (Stocks, Bonds, Treasury)
- WRDS Markit CDS data
- WRDS Bond Returns
- WRDS Mergent FISD
- WRDS Bank Premium
- Bloomberg Terminal
- OptionMetrics IvyDB

```{note}
While some datasets require paid subscriptions, they are commonly available through academic institutions. Our code automates the data retrieval process once you have the appropriate access credentials. If you don't have access to any of the above data sources, you can still use our code to pull from only the data sources that you have subscriptions for.
```

---

## Getting Started

1. **Installation**: Follow our [quickstart guide](data_sources_and_modules.md#installation) to set up the environment
2. **Configuration**: Set up your data source credentials and specify available subscriptions
3. **Data Download**: Run the automated ETL pipeline to build your standardized datasets
4. **Benchmarking**: Use our baseline models to establish performance benchmarks

---

## Documentation

```{toctree}
:maxdepth: 1
:caption: 📚 Documentation

data_sources_and_modules
ftsfr_datasets_info
data_glimpses
data_glimpses_ftsfr
```

```{toctree}
:maxdepth: 1
:caption: 📊 Data Cleaning Procedure Summaries

_notebook_build/summary_cds_bond_basis_ipynb.ipynb
_notebook_build/summary_cds_returns_ipynb.ipynb
_notebook_build/summary_cip_ipynb.ipynb
_notebook_build/summary_commodities.ipynb
_notebook_build/summary_corp_bond_returns_ipynb.ipynb
spx_options_description.md
cleaning_options.md
_notebook_build/summary_treasury_bond_returns_ipynb.ipynb
```

```{toctree}
:maxdepth: 1
:caption: 🔧 Development

myst_markdown_demos
```

---

## Key Features

- 📡 **Streamlined data collection** from multiple sources (WRDS, FRED, Bloomberg, etc.)
- 🎯 **Academic standards**: Replicates cleaning procedures from academic literature
- 🤖 **Fully reproducible** data preparation workflows
- 📈 **Spans multiple financial domains**:
    - Equity Markets: Returns, portfolios, and characteristics
    - Fixed Income: Treasury, corporate, and sovereign bonds
    - Credit Markets: CDS spreads and bond-CDS basis
    - Derivatives: Options and futures data
    - Foreign Exchange: Currency portfolios and rates
    - Commodities: Futures and spot prices
    - Banking: Call report data and bank-specific metrics

---

## Contributing

We welcome contributions from the research community. Whether you're:
- Adding new data sources
- Improving cleaning methodologies
- Implementing additional forecasting benchmarks
- Enhancing documentation

Please see our contribution guidelines for more information.

---

## Acknowledgments

We would like to thank the following individuals. With their permission, we have adapted and used pieces of their code in this repository:

- **Om Mehta and Kunj Shah**, for their replication of the Covered Interest Rate Parity (CIP) arbitrage spreads (Siriwardane et al. 2022; Rime et al. 2017), available at https://github.com/Kunj121/CIP

- **Kyle Parran and Duncan Park**, for their replication of the construction of commodity futures returns (He et al. 2017; Yang 2013), available at https://github.com/kyleparran/final_project_group_09

- **Haoshu Wang and Guanyu Chen**, for their replication of the Treasury Spot-Futures basis (Siriwardane et al. 2022)

- **Arsh Kumar and Raiden Egbert**, for their replication of the Treasury Swap basis (Siriwardane et al. 2022)

- **Bailey Meche and Raul Renteria**, for their replication of the TIPS-Treasury basis (Siriwardane et al. 2022)

---

## Project Team

**Project Lead:**
- [Jeremiah Bejarano](https://jeremybejarano.com/), Office of Financial Research, U.S. Department of the Treasury and Financial Mathematics Program, University of Chicago

**Project Collaborators:**
- Viren Desai
- Kausthub Keshava
- Arsh Kumar
- Zixiao Wang
- Vincent Hanyang Xu
- Yangge Xu

*Views and opinions expressed are those of the authors and do not necessarily represent official positions or policy of the Office of Financial Research (OFR) or the U.S. Department of the Treasury.*

---

## Citation

If you use FTSFR in your research, please cite:

```
Bejarano, J. et al. (2024). Financial Time Series Forecasting Repository:
A Standardized Macro-Finance Data Repository for Global Time Series Forecasting.
[Working Paper]
```

---

```{note}
**Academic Collaboration**: This project represents a collaborative effort among researchers to advance the state of financial time series forecasting. We encourage academic partnerships and welcome contributors who are interested in pushing the boundaries of empirical finance research.
```

---

## Indices and Tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
