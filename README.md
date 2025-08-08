# Financial Time-Series Forecasting Repository

You can view the current version of the website here: https://jeremybejarano.com/ftsfr/

## Overview

This repository contains a collection of financial time-series forecasting models. It produces testing benchmarks for practitioners. One key feature is that users can specify which data sources (i.e., subscriptions) they have access to in `subscriptions.toml`, and the system will automatically determine which modules can be run based on the user's available data sources.

### Architecture: Data Sources, Data Modules, and Datasets

This repository is organized around three key concepts:

1. **Data Sources**: External data providers that may require subscriptions or API access. Examples include:
   - Bloomberg Terminal
   - WRDS (Wharton Research Data Services) subscriptions (Markit, CRSP, Compustat, etc.)
   - Public data sources (Federal Reserve, Ken French Data Library, etc.)
   
   Users specify which data sources (subscriptions) they have access to in `subscriptions.toml`.

2. **Data Modules**: Self-contained units of code organized in subdirectories under `src/`. Each data module:
   - Contains all related code for a specific financial data domain
   - May depend on one or more _data sources_
   - Produces one or more related _datasets_
   - Examples: `cds_returns`, `corp_bond_returns`, `us_treasury_returns`

3. **Datasets**: The actual data files produced by data modules, saved as parquet files. These follow a consistent format:
   - Named as `ftsfr_<dataset_name>.parquet`
   - Contain standardized columns: `id` (entity), `ds` (date/timestamp), `y` (value)
   - Metadata (frequency, balance status, etc.) is stored in `datasets.toml`

The dependency relationships between data modules and data sources are defined in `datasets.toml` and tracked by `dependency_tracker.py`. This allows the system to automatically determine which modules can be run based on the user's available data sources.

## Agenda

Kausthub
 - Once I give data, need to do various treasury basis trades

Yangge
 - Needs to create ftsfr_futures_returns.parquet
 - Needs to clean up and consolidate various notebooks in futures_returns folder
 - Needs to consolidate futures_returns and commodities folders


## Configuration Files

This repository uses two main configuration files:

### subscriptions.toml
Controls which data sources and models are enabled. Key sections:
- `[cache]` - Whether to use cached data or pull fresh data
- `[data_sources]` - Enable/disable various data providers (Bloomberg, WRDS, public sources)
- `[models]` - Enable/disable different forecasting models
- `[reports]` - Configuration for report generation

### datasets.toml
Defines metadata for all datasets produced by the pipeline:
- Maps data modules to their required data sources
- Specifies dataset properties (frequency, seasonality)
- Documents dataset descriptions
- Controls which datasets are available for forecasting

## Task Organization

The build pipeline is split into three separate dodo files for modularity:

1. **dodo_01_pull.py** - Data acquisition and processing
   - Pulls data from various sources
   - Formats data into standardized datasets
   - Creates data documentation
   - Builds the documentation website

2. **dodo_02_forecast.py** - Model forecasting
   - Runs enabled models on available datasets
   - Can be run on different machines (e.g., GPU servers)
   - Checks for required data files

3. **dodo_03_paper.py** - Results and reporting
   - Assembles forecast results
   - Compiles LaTeX documents
   - Generates final reports

## Quickstart

Please install the following:

- TeX Live: <https://www.tug.org/texlive/>
- Pixi: <https://pixi.sh/latest/>
- Conda: Perhaps move everything over to Pixi soon.

Install TeX Live using the instructions here: <https://www.tug.org/texlive/quick-installation-guide.html> .

To install Pixi, please follow the instructions here: <https://docs.pixi.com/getting-started/installation> . In short, on MacOS or Linux, you can run this:

```bash
curl -fsSL https://pixi.sh/install.sh | zsh
```

and on Windows, you can run this:

```bash
winget install prefix-dev.pixi
```

Then, install Conda using the instructions here: <https://docs.conda.io/en/latest/miniconda.html> .

Then, create a virtual environment and activate it:

```bash
conda create -n ftsfr python=3.12.6
```

Activate virtual environment:

```bash
conda activate ftsfr
```

Install packages:

```bash
pip install -r requirements.txt
```
If you have a Bloomberg Terminal, you can install the Bloomberg API using the following command:
```bash
blpapi --index-url https://blpapi.bloomberg.com/repository/releases/python/simple/
```

Then, follow the pattern in the `.env.example` file to set your environment variables in a `.env` file.

Then, set the values in `subscriptions.toml` to your desired values. This file is used to configure the datasets that will be downloaded, based of the subscriptions that you have, and the benchmarks that will be run.

Finally, run the pipeline (which is broken down into three major parts):

```bash
# Step 1: Pull and format data (default when you run `doit`)
doit -f dodo_01_pull.py
# Or, simply, just run this: doit 

# Step 2: Run forecasting models (optional, requires step 1)
doit -f dodo_02_forecast.py

# Step 3: Generate reports and papers (optional, requires step 2)
doit -f dodo_03_paper.py
```

**Note:** Running `doit` without any arguments will execute the pull tasks (Step 1) by default. This is the most common use case for most users.

Or run specific tasks:
```bash
# Just pull data from a specific source
doit pull:fed_yield_curve

# Just format data for a specific module
doit format:cds_returns

# Run a specific model on specific datasets (requires specifying the file)
doit -f dodo_02_forecast.py forecast:arima:ftsfr_treas_yield_curve_zero_coupon
```

Note: Each step can be run on different machines. For example:
- Run `dodo_01_pull.py` on a machine with data access
- Run `dodo_02_forecast.py` on a GPU server
- Run `dodo_03_paper.py` on your local machine

### Tips for Running on LambdaLabs

We provide a setup script that automates the entire LambdaLabs GPU instance setup process:

```bash
./setup_lambdalabs.sh
```

This script will:
1. Install Miniconda and initialize it for all shells
2. Download VS Code CLI for remote development
3. Create a conda environment named "ftsfr" with Python 3.12.6
4. Install all required Python packages from requirements.txt
5. Install Pixi package manager
6. Optionally start the VS Code tunnel for remote development

**Note**: The script handles the shell restart requirement automatically. You'll need to run it twice - once for the initial setup, and once after restarting your shell (the script will guide you through this process).

## Data Format
Final, cleaned and formatted datasets have the following format: `ftsfr_<dataset_name>.parquet`
and have the following columns:
- `unique_id`: the entity id
- `ds`: the date/timestamp column
- `y`: the value

This follows the convention used by `nixtla` and other time series libraries (see, e.g., https://www.nixtla.io/docs/data_requirements/data_requirements).

The list of available datasets is given in `datasets.toml`, along with metadata such as the frequency of the time series, whether the panel is balanced, etc.

## Tips

For local development on forecasting scripts, you can activate a pixi environment and open a new shell with that environment activated using the following command:

```bash
pixi shell
```

# Data Modules

Overview of data modules:

**Misc**

- [x] CRSP Returns (with and without dividends)
- [ ] Compustat Panel Data
- [x] Fama-French Portfolio Returns
- [x] Treasury Yield Curve
- [x] Bank Call Report Data

**He, Kelly, Manela Test Portfolios**

We can just use the test portfolios as downloaded from their website, though it
would be nice to use data up until the present day.

- [x] Equity CLOSE
- [.] Treasury Securities
- [.] Corporate Bonds
- [.] Sovereign Bonds
- [.] Options
- [.] Foreign Exchange
- [.] Commodities CLOSE
- [.] CDS CLOSE

**He, Kelly, Manela Disaggregated Data**

- [.] Equity
- [.] Treasury Securities
- [.] Corporate Bonds
- [ ] Sovereign Bonds
- [.] Options
- [ ] Foreign Exchange
- [ ] Commodities
- [.] CDS

**Segmented Arbitrage, Arbitrage Spreads**

- [ ] CIP
- [.] Box Spread
- [.] Equity Spot-Futures
- [.] Treasury Spot-Futures
- [.] Treasury Swap
- [.] TIPS-Treasury
- [.] CDS-Bond Basis

## Equity Options Arbitrage

From the main Segmented Arbitrage paper, 

> Equity Options Arbitrage (Box Arbitrage) We infer riskless rates and arbitrage spreads from
> S&P 500 (SPX) equity options based on the put-call parity relationship. As discussed in Ronn and
> Ronn (1989) and van Binsbergen et al. (2019), implied riskless rates from put-call parity are often
> called box rates in practice. We adopt this naming convention and refer to this arbitrage as the box
> trade for the remainder of the paper. We take box rates for six, twelve, and eighteen month tenors
> directly from van Binsbergen et al. (2019), who estimate them using minute-by-minute pricing
> data for SPX options through 2018. We then follow van Binsbergen et al. (2019)’s methodology
> to extend the data to 2020 using SPX option data purchased directly from the CBOE. Arbitrage
> spreads are then computed by subtracting off a maturity-matched OIS rate.

And in the appendix, they provide the following description:

```
Put-call parity is a no-arbitrage condition relating the difference between the price of European put
and call options. For time t, tenor τ, and strike price Ki, let pi,t,τ denote the price of a put option
and ci,t,τ denote the price of call option. Put-call parity states the difference between two equals the
discounted strike price Ki and spot price (st ) and an adjustment for any dividend cash flows (Ct,τ ):
pi,t,τ −ci,t,τ = (Ct,τ −st)+exp(−r f
t,ττ)Ki, (A.3)
where r f
t,τ is the implied riskless rate from the option pair. van Binsbergen et al. (2019) compute the
r f
t,τ using a cross-section of call and put options via the following regression:
pi−ci = α +βKi+εi (A.4)
This cross-sectional regression is estimated over all strikes for each time t and tenor τ, and avoids
the need to estimate cash flows Ct,τ . The estimated β can then be used to back out the implied
riskless rate. van Binsbergen et al. (2019) estimate minute-by-minute implied riskless rates from
SPX options and then aggregate to the daily level by taking medians. The equity box arbitrage
spread equals the difference between the option implied and maturity-matched OIS riskless rates.
We combine estimates from van Binsbergen et al. (2019), which are available on their websites,
with OIS rates from Bloomberg. The data from van Binsbergen et al. (2019) ends in March 2018.
To better match the rest of our sample, we have also updated their series by applying their same
methodology to minute-level SPX options data that runs through the end of our sample. These data
were purchased directly through the CBOE. To verify the accuracy of our extended series, we have
compared our option-implied riskless rates to those in van Binsbergen et al. (2019) for the period in
which the two series overlap. When regressing their implied riskless rates on ours, the regression
constants for the 6,12, and 18m series are -0.68, 0.27, and 0.37 bps, respectively. The estimated
slopes are 1.01 in all cases and the R2s all exceed 0.9996.
Figure A1b plots daily raw values for 6, 12, and 18 month equity box arbitrage spreads. When
the equity box arbitrage spread is positive, the asset implied risk-free rate from put-call parity is
greater than the OIS dollar risk-free rate.
```

Do we have access to the data to get this up to the present day?

## Datasets I've Already Included

- CRSP Returns (with and without dividends)

## Potential Datasets to Include in the Future (Notes, Work in Progress)

The paper would reference data from a few papers. The datasets would mostly be organized by the paper in which they are references.

- He, Kelly, Manela Test portfolios. You would run the time series algorithms on the test portfolios all together in a single go. Just use the test portfolios as downloaded from their website. This would just reference their paper.

  - Equity: the Fama and French (1993) **25 size and value sorted portfolios** (from Ken French's website).
  - For **US bonds**, we include government and corporate bond portfolios in the same class. (Our choice to combine US government and corporate bonds into a single asset class is driven by our desire to estimate prices of intermediary capital risk separately for each asset class. Treating US government bonds as its own asset class is not statistically sensible due to the very high correlation in the returns on these portfolios.)

    - We use ten maturity-sorted **government bond** portfolios from CRSP's "Fama Bond Portfolios" file with maturities in six month intervals up to five years.
    - For **corporate bonds**, we use ten portfolios sorted on yield spreads from Nozawa (2017). These portfolios are based on a comprehensive bond data set combining TRACE, the Lehman bond database, and others, starting in 1973.

  - For **sovereign bonds** we use six portfolios from Borri and Verdelhan (2012). These portfolios are based on a twoway sort on a bond's covariance with the US equity market return and the bond's Standard & Poor's credit rating.
  

  
  - For **foreign exchange**, we combine two datasets of currency portfolios to arrive at a total of 12 portfolios. First is the set of six currency portfolios sorted on the interest rate differential from Lettau et al. (2014). Second is the set of six currency portfolios sorted on momentum from Menkhoff, Sarno, Schmeling and Schrimpf (2012).
  - For **commodities**, we use returns to commodity futures from the Commodities Research Bureau. We begin from the list of 31 commodities in Table 1 of Yang (2013). For each commodity, we form an equal-weighted portfolio of all futures contracts with maturities up to four months. These 31 commodities differ in their availability, with some samples only available for a few years. To balance the benefits of a long sample and many commodities, we include in our dataset 23 commodity portfolios with at least 25 years of returns data.
  - For **CDS**, we construct 20 portfolios sorted by spreads using individual name 5-year contracts. The data are from Markit and begin in 2001\. We focus on 5-year CDS for the well known reason that these are the most liquid contracts. Our definition of CDS returns follows Palhares (2013).

- Disaggregated Data from various asset classes (references)

  - Equity returns. This one wouldn't really reference Fama and French (1993), but I would let the readers know that the cleaning method is similar (very small stocks excluded, common shares, US exchanges, no ADRs, etc.) <https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/stock-version-2/>
  - CRSP Daily Treasury Prices: <https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/treasuries/daily-time-series/>
  - Corporate Bonds from TRACE: <https://wrds-www.wharton.upenn.edu/pages/get-data/otc-corporate-bond-and-agency-debt-bond-transaction-data/>
  - Options, from Constantinides, Jackwerth and Savov (2013)
  - Foreign Exchange, US to other major currencies
  - Commodity futures. list of 31 commodities in Table 1 of Yang (2013)
  - CDS returns, following Palhares (2013)

- Open Source Asset Pricing Data

  - Monthly and Daily long-short returns of 212 predictors following OPs (wide csv) (See here: <https://www.openassetpricing.com/data/>)
  - 209 predictive firm-level characteristics in wide format, signed so future mean returns increase in characteristics (1.6 GB zipped csv)

- Include basis trades data from Siriwardane et al.

  - This include basis spread data from Treasury Cash-Futures basis trade, CDS-Bond Basis, Treasury Swap basis, Options Spread bases, etc

- Bank Call Report data. Include bank call report series of interest from NYU call report archive (schnabl). This will be important for publishing on OFR website
- [Industrial Production](https://www.federalreserve.gov/releases/g17/download.htm) over the period 1972-2007 obtained from the Board of Governors, and Benchmark Input-Output tables provided by the Bureau of Economic Analysis (BEA)

  - E.g., following Foerster, Andrew T., Pierre-Daniel Sarte, and Marianna Kudlyak. "Sectoral vs. Aggregate Shocks: A Structural Factor Analysis of Industrial Production, Working Paper 08-07." (2008).

- Include Compustat series (do a bank only one versus everyone else. Maybe do that with CRSP too)
- Redo FRED-MD since it's applicable here, even though it's in the other one

Other options. It's probably best to stick to those above for simplicity

- Include various test portfolios from Ken French Data Library
- Various repo series from OFR short-term funding monitor
- Include estimates of mark-to-market losses from "Monetary Tightening" paper. This will also bolster the case for publishing on OFR website
- Include CRSP panel of stock returns, cash flows (with and without buybacks)
- Include all of the signals from the Open Source Asset Pricing website
- Dividend futures, dividends, S&P 500 returns
- Average within-firm predictability

  - Match asset returns and Compustat financials within firms. That is, for a given company (e.g., via PERCMO), find the stock return, dividend payment, bond returns, associated single name CDS, options connected with that firms stocks, and various Compustat financials all associated with that company. Calculate the predictability within this firm. Then, do this for all firms. Measure the average predictability among firms.

# Useful Commands

(We can delete this later. I'm putting these here as they're useful for me while I'm developing)

To run pre-commit hooks on all files:

```bash
pre-commit run --all-files
```

to format all files and fix linting errors:

```bash
ruff format . && ruff check --fix --show-fixes .
```
