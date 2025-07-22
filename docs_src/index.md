# Financial Time Series Forecasting Repository (FTSFR)

**A standardized macro-finance data repository for global time series forecasting research**

## Overview

The Financial Time Series Forecasting Repository (FTSFR) addresses a critical gap in quantitative finance research: the lack of standardized datasets for evaluating and comparing time series forecasting models. When researchers evaluate their own forecasting models on their own arbitrarily chosen datasets, apples-to-apples comparisons across forecasting algorithms are not possible. This repository provides a comprehensive collection of financial and macroeconomic datasets that have been cleaned, formatted, and standardized according to academic best practices. We hope that this repository will serve as a useful time series forecasting benchmark.

## Why FTSFR?

### The Problem
When comparing different time series forecasting algorithms, researchers need **apples-to-apples comparisons**. Each forecasting model must be evaluated on identical datasets that have been:
- Prepared using the same methodology
- Cleaned with consistent standards  
- Sampled over the same time periods
- Formatted in the same way

We are inspired by the work of the Monash Time Series Data Repository (MTSDR), which provides a collection offreely available datasets for benchmarking  time series forecasting models. However, we are motivated by the desire to provide datasets from topics in finance and economics, which are often not freely available (e.g., require a subscription to access).

### Our Solution
We provide researchers with easy access to a ready-to-use repository of financial and macroeconomic datasets that have been cleaned, formatted, and standardized according to academic best practices. Although most of the data in this repository requires a subscription to access, we provide what we think is the next-best thing: a codebase that automates the end-to-end process for assembling various financial and macroeconomic data, from the data pull step to the final cleaning and transformation step. Most of our code pulls from the Wharton Research Data Services (WRDS), which is a subscription-based service commonly available at most universities. Our quickstart guide provides a short and simple guide to get you started.

## Key Features

- 📡 Streamlined data collection from multiple sources (e.g., WRDS, FRED, etc.)
- 🎯 Academic Standards: Replicates cleaning procedures for each datasetfrom academic literature
- 🤖 Fully reproducible data preparation workflows
- 📈 Spans multiple financial domains:
    - Equity Markets: Returns, portfolios, and characteristics
    - Fixed Income: Treasury, corporate, and sovereign bonds
    - Credit Markets: CDS spreads and bond-CDS basis
    - Derivatives: Options and futures data
    - Foreign Exchange: Currency portfolios and rates
    - Commodities: Futures and spot prices
    - Banking: Call report data and bank-specific metrics

## Replications of Studies from Academic Literature

Each of the cleaned datasets that we provide follow the procedures outlined in a published academic paper. We feel that these benchmarks are most useful when they follow the same procedures commonly used in the literature. We replicate the procedures outlined in or use the data provided via the following papers:

 
 - Barth, Daniel, and R. Jay Kahn. "Hedge funds and the Treasury cash-futures disconnect." OFR WP (2021): 21-01.
 - Borri, Nicola, and Adrien Verdelhan. "Sovereign risk premia." (2011).
 - Constantinides, George M., Jens Carsten Jackwerth, and Alexi Savov. "The puzzle of index option returns." Review of Asset Pricing Studies 3, no. 2 (2013): 229-257.
 - Drechsler, Itamar, Alexi Savov, and Philipp Schnabl. "The deposits channel of monetary policy." The Quarterly Journal of Economics 132, no. 4 (2017): 1819-1876.
 - Du, Wenxin, Alexander Tepper, and Adrien Verdelhan. "Deviations from covered interest rate parity." The Journal of Finance 73, no. 3 (2018): 915-957.
 - Du, Wenxin, Benjamin Hébert, and Wenhao Li. "Intermediary balance sheets and the treasury yield curve." Journal of Financial Economics 150, no. 3 (2023): 103722.
 - Duffie, Darrell. "Credit swap valuation." Financial Analysts Journal 55, no. 1 (1999): 73-87.
 - Fama, Eugene F., and Kenneth R. French. "Common risk factors in the returns on stocks and bonds." Journal of financial economics 33, no. 1 (1993): 3-56.
 - Fleckenstein, Matthias, Francis A. Longstaff, and Hanno Lustig. "The TIPS‐treasury bond puzzle." the Journal of Finance 69, no. 5 (2014): 2151-2197.
 - Gürkaynak, Refet S., Brian Sack, and Jonathan H. Wright. "The TIPS yield curve and inflation compensation." American Economic Journal: Macroeconomics 2, no. 1 (2010): 70-92.
 - Gürkaynak, Refet S., Brian Sack, and Jonathan H. Wright. "The US Treasury yield curve: 1961 to the present." Journal of monetary Economics 54, no. 8 (2007): 2291-2304.
 - He, Zhiguo, Bryan Kelly, and Asaf Manela. "Intermediary asset pricing: New evidence from many asset classes." Journal of Financial Economics 126, no. 1 (2017): 1-35.
 - J Jermann, Urban. "Negative swap spreads and limited arbitrage." The Review of Financial Studies 33, no. 1 (2020): 212-238.
 - Lettau, Martin, Matteo Maggiori, and Michael Weber. "Conditional risk premia in currency markets and other asset classes." Journal of Financial Economics 114, no. 2 (2014): 197-225.
 - Menkhoff, Lukas, Lucio Sarno, Maik Schmeling, and Andreas Schrimpf. "Carry trades and global foreign exchange volatility." The Journal of Finance 67, no. 2 (2012): 681-718.
 - Nozawa, Yoshio. "What drives the cross‐section of credit spreads?: A variance decomposition approach." The Journal of Finance 72, no. 5 (2017): 2045-2072.
 - Palhares, Diogo. Cash-flow maturity and risk premia in CDS markets. The University of Chicago, 2013.
 - Ronn, Aimee Gerbarg, and Ehud I. Ronn. "The box spread arbitrage conditions: theory, tests, and investment strategies." Review of Financial Studies 2, no. 1 (1989): 91-108.
 - Siriwardane, Emil, Adi Sunderam, and Jonathan L. Wallen. Segmented arbitrage. No. w30561. National Bureau of Economic Research, 2022.
 - Van Binsbergen, Jules H., William F. Diamond, and Marco Grotteria. "Risk-free interest rates." Journal of Financial Economics 143, no. 1 (2022): 1-29.
 - Yang, Fan. "Investment shocks and the commodity basis spread." Journal of Financial Economics 110, no. 1 (2013): 164-184.

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
- WRDS Bank Premium
- Bloomberg Terminal

```{note}
While some datasets require paid subscriptions, they are commonly available through academic institutions. Our code automates the data retrieval process once you have the appropriate access credentials. If you don't have access to any of the above data sources, you can still use our code to pull from only the data sources that you have subscriptions for. The code will automatically skip the data sources that you don't have access to. However, in that case, you won't be able to assemble the full suite of benchmark datasets.
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
:caption: 📊 Data Cleaning Procedure Summaries

_notebook_build/summary_cds_bond_basis_ipynb.ipynb
_notebook_build/summary_cds_returns_ipynb.ipynb
_notebook_build/summary_cip_ipynb.ipynb
_notebook_build/summary_corp_bond_returns_ipynb.ipynb
cleaning_options.md
_notebook_build/summary_treasury_bond_returns_ipynb.ipynb
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

## Acknowledgments

We would like to thank the following individuals. With their permission, we have adapted and used pieces oftheir code in this repository.

- Om Mehta and Kunj Shah, for their replication of the Covered Interest Rate Parity (CIP) arbitrage spreads that appear in _Siriwardane, Sunderam, and Wallen. "Segmented arbitrage", 2022._ and _Rime, Schrimpf, and Syrstad. "Segmented money markets and covered interest parity arbitrage", 2017_, available at https://github.com/Kunj121/CIP
- Kyle Parran and Duncan Park, for their replication of the construction of the commodity futures returns that appear in and _He, Kelly, and Manela. "Intermediary asset pricing: New evidence from many asset classes." Journal of Financial Economics, 2017_ and _Yang, Fan. “Investment shocks and the commodity basis spread.” (2013)_, available at https://github.com/kyleparran/final_project_group_09


---

```{note}
**Academic Collaboration**: This project represents a collaborative effort among researchers to advance the state of financial time series forecasting. We encourage academic partnerships and welcome contributors who are interested in pushing the boundaries of empirical finance research.
```

## Indices and Tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`

