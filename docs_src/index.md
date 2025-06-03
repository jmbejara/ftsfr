# Financial Time Series Forecasting Repository (FTSFR)

**A standardized macro-finance data repository for global time series forecasting research**

## Overview

The Financial Time Series Forecasting Repository (FTSFR) addresses a critical gap in quantitative finance research: the lack of standardized datasets for evaluating and comparing time series forecasting models. This repository provides a comprehensive collection of financial and macroeconomic datasets that have been cleaned, formatted, and standardized according to academic best practices.

## Why FTSFR?

### The Problem
When comparing different time series forecasting algorithms, researchers need **apples-to-apples comparisons**. Each forecasting model must be evaluated on identical datasets that have been:
- Prepared using the same methodology
- Cleaned with consistent standards  
- Sampled over the same time periods
- Formatted in the same way

### Our Solution
FTSFR provides a codebase that automates the extract-transform-load (ETL) process for financial and macroeconomic data from various sources. Our standardized approach ensures that researchers can focus on model development rather than data preparation.

## Key Features

### 🔧 **Automated ETL Pipeline**
- Streamlined data collection from multiple sources
- Consistent cleaning and formatting procedures
- Reproducible data preparation workflows

### 📊 **Comprehensive Coverage**
Our repository spans multiple financial domains:
- **Equity Markets**: Returns, portfolios, and characteristics
- **Fixed Income**: Treasury, corporate, and sovereign bonds
- **Credit Markets**: CDS spreads and bond-CDS basis
- **Derivatives**: Options and futures data
- **Foreign Exchange**: Currency portfolios and rates
- **Commodities**: Futures and spot prices
- **Banking**: Call report data and bank-specific metrics

### 🎯 **Academic Standards**
- Data cleaning follows established academic literature
- Consistent with peer-reviewed research methodologies
- Suitable for academic publication and peer review

### 📈 **Baseline Benchmarks**
- Pre-computed performance metrics for baseline forecasting methods
- Multiple error metrics for comprehensive evaluation
- Reference points for comparing new forecasting approaches

## Data Sources

Our repository leverages both **publicly available** and **subscription-based** data sources:

### Public Data Sources *(No subscription required)*
- He, Kelly, Manela test portfolios
- Ken French Data Library  
- Federal Reserve economic data
- NYU Call Report archive
- Open Source Bond Asset Pricing

### Academic Subscription Sources *(Commonly available via university subscriptions)*
- WRDS Compustat North America
- WRDS CRSP (Stocks, Bonds, Treasury)
- WRDS Markit CDS data
- WRDS Bond Returns
- WRDS Mergent FISD

```{note}
While some datasets require paid subscriptions, they are commonly available through academic institutions. Our code automates the data retrieval process once you have the appropriate access credentials.
```

## Getting Started

1. **Installation**: Follow our [quickstart guide](data_sources_and_modules.md#installation) to set up the environment
2. **Configuration**: Set up your data source credentials and specify available subscriptions
3. **Data Download**: Run the automated ETL pipeline to build your standardized datasets
4. **Benchmarking**: Use our baseline models to establish performance benchmarks

## Documentation Contents

```{toctree}
:maxdepth: 1
:caption: 📚 Documentation

data_sources_and_modules
ftsfr_datasets_info
data_glimpses
```

```{toctree}
:maxdepth: 1
:caption: 📊 Dataset Summaries

_notebook_build/corp_bond_returns_summary_ipynb.ipynb
_notebook_build/treasury_bond_returns_summary_ipynb.ipynb
_notebook_build/01_cds_returns_summary_ipynb.ipynb
```

```{toctree}
:maxdepth: 1
:caption: 🔧 Development

myst_markdown_demos
```

## Research Impact

This repository facilitates rigorous empirical research by providing:

- **Standardized benchmarks** for forecasting algorithm evaluation
- **Reproducible results** through consistent data preparation
- **Comprehensive coverage** across financial markets and instruments
- **Academic credibility** through literature-consistent methodologies

## Citation

If you use FTSFR in your research, please cite:

```
Bejarano, J. et al. (2024). Financial Time Series Forecasting Repository: 
A Standardized Macro-Finance Data Repository for Global Time Series Forecasting. 
[Working Paper]
```

## Contributing

We welcome contributions from the research community. Whether you're:
- Adding new data sources
- Improving cleaning methodologies  
- Implementing additional forecasting benchmarks
- Enhancing documentation

Please see our contribution guidelines for more information.

---

```{note}
**Academic Collaboration**: This project represents a collaborative effort among researchers to advance the state of financial time series forecasting. We encourage academic partnerships and welcome contributors who are interested in pushing the boundaries of empirical finance research.
```

## Indices and Tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`

