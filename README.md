# Financial Time-Series Forecasting Repository

You can view the current version of the website here: https://jeremybejarano.com/ftsfr/

## Overview

This repository contains a collection of financial time-series forecasting models. It produces testing benchmarks for practitioners. One key feature is that users can specify which data sources (i.e., subscriptions) they have access to in `config.toml`, and the system will automatically determine which modules can be run based on the user's available data sources.

### Architecture: Data Sources, Data Modules, and Datasets

This repository is organized around three key concepts:

1. **Data Sources**: External data providers that may require subscriptions or API access. Examples include:
   - Bloomberg Terminal
   - WRDS (Wharton Research Data Services) subscriptions (Markit, CRSP, Compustat, etc.)
   - Public data sources (Federal Reserve, Ken French Data Library, etc.)
   
   Users specify which data sources (subscriptions) they have access to in `config.toml`.

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

All
 - Timeline (finish by end of July)
 - GitHub Contributions
 - Interactive work, using DATA_DIR
 - How to incorporate Bloomberg: Done https://github.com/jmbejara/ftsfr/issues/14

Alex and Vincent
 - Bloomberg data now available in foreign_exchange/pull_bbg_foreign_exchange.py https://github.com/jmbejara/ftsfr/issues/18
 - Foreign Exchange returns (returns on individual currencies, not the portfolios of He, Kelly, Manela) 


Kausthub
 - Sovereign bond data: https://github.com/jmbejara/ftsfr/issues/26
 - Treasuries and Corporate Bonds done? Sovereign Bonds next?

Yangge
 - Present issues raised in https://github.com/jmbejara/ftsfr/issues/21
 - Commodity returns? https://github.com/kyleparran/final_project_group_09 (I received permission)
 - Compare against: https://github.com/Raafayuqaily/DS-Commodities-Final-Project

Jeremy
 - Check this again? https://github.com/jmbejara/ftsfr/issues/2
 - Bloomberg sovereign bond data: https://github.com/jmbejara/ftsfr/issues/26


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

Then, set the values in `config.toml` to your desired values. This file is used to configure the datasets that will be downloaded, based of the subscriptions that you have, and the benchmarks that will be run.

Finally, download the data using the following command:

```bash
doit
```

### Tips for Running on LambdaLabs

Install Miniconda, using these [instructions](https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions):
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```
After installing, close and reopen your terminal application or refresh it by running the following command:

```
source ~/miniconda3/bin/activate
```

Then, initialize conda on all available shells by running the following command:

```
conda init --all
```
Also, to get VS Code code server
```
curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz

tar -xf vscode_cli.tar.gz
```
then run it with this:
```
./code tunnel
```
Then,
```
conda create -n ftsfr python=3.12.6
conda activate ftsfr
pip install -r requirements.txt
curl -fsSL https://pixi.sh/install.sh | zsh
```

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

Do have access to the data to get this up to the present day?

## He, Kelly, Manela (HKM) Test Portfolios: Options

From the HKM 2017 paper on intermediary asset pricing:
> For options, we use 54 portfolios of S&P 500 index options sorted on moneyness and maturity from Constantinides, Jackwerth and Savov (2013), 
> split by contract type (27 call and 27 put portfolios), and starting in 1986. Portfolio returns are leverage-adjusted, meaning that each option 
> portfolio is combined with the risk-free rate to achieve a targeted market beta of one. According to Constantinides et al. (2013),
> *The major advantage of this construction is to lower the variance and skewness of the monthly portfolio returns and render the returns close to
> normal (about as close to normal as the index return), thereby making applicable the standard linear factor pricing methodology*. To keep 
> the number of portfolios used in our tests similar across asset classes, we reduce the 54 portfolios to 18 portfolios by constructing equal-weighted
> averages of portfolios that have the same moneyness but different maturity (though our results are essentially unchanged if we use all 54 portfolios separately). 


In order to replicate the HKM options portfolio returns, we necessarily needed to construct the 54 portfolios of S&P 500 index options sorted on 9 tiers of moneyness and 3 maturities from Constantinides, Jackwerth and Savov (2013), split by contract type (9 moneyness x 3 maturities = 27 call portfolios, and similarly, 27 put portfolios). HKM take an equal-weighted average over the 3 maturities in CJS 2013, and obtain **54 / 3 = 18 portfolios for the HKM analysis**. 

The original CJS 2013 paper used data from 1986 through 2012 (26 years of data). Due to unavailability of SPX option data from 1985 to 1995, we replicated the data cleaning and portfolio construction process for the 54 portfolios in CJS using data from **January 1996 to December 2019** (23 years). Our dataset (from 1996 to 2019) comprises over 19.2 million rows of SPX options data, and, due to increasing liquidity in the SPX options market over time, our dataset contains significantly more options than the original paper. Portfolio returns are leverage-adjusted, meaning that each option portfolio is combined with the risk-free rate to achieve a targeted market beta of one, as described broadly in CJS 2013. *The spirit of this project is to replicate with the highest practical fidelity the ***process*** of data filtration and portfolio construction in the original CJS and HKM papers, without commenting on the effectiveness or appropriateness of the process and parameters. The idea here is that we provide the logic so the user can apply the same data cleaning and portfolio construction process to any date range of SPX options data.*  

### Data Filtration and Cleaning

We replicate the Level 1, 2, and 3 data filters outlined in *CJS 2013 Appendix B* as follows: 

***Level 1 Filters***

* **Identical Filter:** Retain only one instance of quotes with the same **option type**, **strike price**, **expiration date/maturity**, and **price**. 

* **Identical Except Price Filter:** There are a few sets of quotes with identical terms (**type**, **strike**, and **maturity**) but different prices. Keep the quote whose **T-bill-based implied volatility** is closest to that of its **moneyness neighbors**, and delete the others.  

* **Bid = 0 Filter:** Drop quotes with a **bid price** of zero, thereby avoiding low-valued options. Also, a zero bid may indicate censoring as negative bids cannot be recorded.

* **Volume = 0 Filter:** Drop quotes of zero for volumes. *Note: Appendix B of CJS does not explicitly detail this filter, but we include it here since it is included in *Table B.1. Filters* of CJS.*  


***Level 2 Filters***


* **Days to Maturity <7 or >180 Filter:** Drop options with fewer than seven or more than 180 calendar days to expiration. 


* **IV<5% or >100% Filter:** We remove all option quotes with implied volatilities lower than 5% or higher than 100%, computed using T-bill interest rates.

* **Moneyness <0.8 or >1.2 Filter:** We remove all option quotes with moneyness, the ratio of strike price to index price, below 0.8 or above 1.2. These options have little value beyond their intrinsic value and are also very thinly traded.

* **Implied Interest Rate <0 Filter:** When filtering outliers, we use T-bill interest rates to compute implied volatilities. T-bill interest rates are obtained from the Federal Reserve’s H.15 release. We assign a T-bill rate to each observation by assuming that we can use the next shortest rate if the time to expiration of the option is shorter than the shortest constant maturity rate. Our goal is to obtain an interest rate that is as close as possible to the one faced by investors in the options market. It appears that the T-bill rates are not the relevant ones when pricing these options. Specifically, when the T-bill rates are used, put and call implied volatilities do not line up very well; for
example, the T-bill rate tends to be too high for short maturity options, perhaps because no T-bill has maturity of less than a month. To address these issues, we compute a put-call parity-implied interest rate. Since we believe that put-call parity holds reasonably well in this deep and liquid European options market, we use the put-call parity-implied interest rate as our interest rate in the remainder of the paper and for further filters. To construct this rate, we take all put-call pairs of a given maturity and impose put-call parity using the bid-ask midpoint as the price, and allowing the interest rate to adjust. We then take the median-implied interest rate across all remaining pairs of the same maturity with moneyness between 0.95 and 1.05 and assign it to all quotes with that maturity. We fill in the gaps by interpolating across maturities and if necessary, across days. 

* **Unable to Compute IV Filter:** We remove quotes that imply negative time
value.

***Level 3 Filters***


* **IV Filter:** The IV filter removes volatility outliers to reduce the prevalence of apparent butterfly arbitrage. 

* **Put-Call Parity Filter:** The puts and calls need to be matched up based on trading date, expiry date, and option type.


### Construction of Monthly Leverage-Adjusted Portfolio Returns in CJS 2013 and HKM 2017

The construction of the 27 call and 27 put portfolios in CJS is a multi-step process, with the objective of developing portfolio returns series that are stationary and only moderately skewed. Note that the discrete bucketing of moneyness and days to maturity lead to multiple candidate options for each portfolio on each trading day. These options  are given weights according to a **bivariate Gaussian weighting kernel** in moneyness and maturity (bandwidths: *0.0125 in moneyness* and *10 days to maturity*).

Each portfolio's daily returns are initially calculated as simple arithmetic return, assuming the option is bought and sold at its bid-ask midpoint at each rebalancing. The one-day arithmetic return is then converted to a **leverage-adjusted return**. This procedure is achieved by calculating the one-day return of a hypothetical portfolio with $\omega_{BSM}^{-1}$ dollars invested in the option, and $(1 - \omega^{-1})$ dollars invested in the risk-free rate, where $\omega_{BSM}$ is the BSM elasticity based on the implied volatility of the option. 

$$
\begin{aligned}
\omega_{\text{BSM, Call}} &= \frac{\partial C_{\text{BSM}}}{\partial S} \cdot \frac{S}{C_{\text{BSM}}} > 1 \\
\omega_{\text{BSM, Put}}  &= \frac{\partial P_{\text{BSM}}}{\partial S} \cdot \frac{S}{P_{\text{BSM}}} < -1
\end{aligned}
$$

Each **leverage-adjusted call portfolio** comprises of a long position in a fraction of a call, and some investment in the risk-free rate. 

Each **leverage-adjusted put portfolio** comprises of a short position in a fraction of a put, and >100% investment in the risk-free rate. 

<font color="blue">*While the original paper did not provide this level of detail, for clarity, we present below the mathematics we utilized to implement CJS' portfolio construction process. The following applies for a single trading day <i>t</i>, for a set of candidate call or put options. Portfolios in CJS are identified by 3 characteristics: option type (call or put), moneyness (9 discrete targets), and time to maturity (3 discrete targets). On any given day, it is rare to find options that exactly match the moneyness and maturity targets. Instead, there may be multiple options that are "close to" the target moneyness / maturity (each a **"candidate option"**). Furthermore, each candidate option has its own price and price sensitivity to changes in the underlying SPX index level. In order to arrive at a "price" for an option portfolio, CJS applies a **Gaussian weighting kernel** in moneyness and maturity, as described below. This kernel-weighted price across the candidate options on a given day is used as the price of the **option component** of the portfolio (the other component being the risk-free rate). This portfolio is leverage-adjusted using the BSM elasticity, in order to standardize the sensitivity of OTM and ITM portfolios to changes in the underlying.*</font>

#### 1. Gaussian Kernel Weighting

Let:

* $m_{i}$ = moneyness of option $i$
* $\tau_{i}$ = days to maturity of option $i$
* $k_{s}$ = target moneyness
* $\tau$ = target maturity
* $h_{m}$, $h_{\tau}$ = bandwidths for moneyness and maturity
* $d_{i}^2 = \left( \frac{m_{i} - k_{s}}{h_{m}} \right)^2 + \left( \frac{\tau_{i} - \tau}{h_{\tau}} \right)^2$

Then the unnormalized Gaussian kernel weight for option $i$ is:

$$
\begin{aligned}
w_{i}^\ast &= \exp\left( -\frac{1}{2} d_{i}^2 \right) \\
\end{aligned}
$$

And the normalized Gaussian kernel weight for option $i$ is:

$$
\begin{aligned}
w_{i} &= \frac{w_{i}^\ast}{\sum_{j} w_{j}^\ast} \\
\end{aligned}
$$

#### 2. Option Elasticity

Let:

* $S_{t}$ = underlying index level at time $t$
* $P_{i}$ = price of option $i$
* $\Delta_{i}$ = option delta

Then:

$$
\varepsilon_{i} = \frac{S_t \cdot \Delta_{i}}{P_{i}}
$$


#### 3. Arithmetic Return of Option $i$

Let:

* $P_{i,t-1}$ = price of option $i$ at time $t-1$
* $P_{i,t}$ = price of option $i$ at time $t$

Then:

$$
r_{i} = \frac{P_{i,t} - P_{i,t-1}}{P_{i,t-1}}
$$


#### 4. Leverage-Adjusted Portfolio Construction

Let:

* $r_{f}$ = risk-free rate on day $t$

The leverage-adjusted return of the call portfolio is:

$$
R_t^{call} = \sum_{i} w_{i} \cdot \frac{1}{\varepsilon_{i}} \cdot r_{i} + \left(1 - \sum_{i} w_{i} \cdot \frac{1}{\varepsilon_{i}} \right) \cdot r_f
$$

The leverage-adjusted return of the put portfolio is:

$$
R_t^{put} = -\sum_{i} w_{i} \cdot \frac{1}{\varepsilon_{i}} \cdot r_{i} + \left(1 + \sum_{i} w_{i} \cdot \frac{1}{\varepsilon_{i}} \right) \cdot r_f
$$

On each trading day, the return of a portfolio is calculated as the <u>weighted average return of the set of candidate options that comprise a single day's option portfolio</u>. The weighting used is the Gaussian kernel weight calculated earlier. Thus the daily return from period $t$ to $t+1$ represents the return from holding a set of candidate options, weighted using the kernel weights as of $t$, from period $t$ to $t+1$. 

#### 5. (to be implemented) Filling NaNs
CJS implement an multi-step process to deal with options with missing prices (detailed in section **1.3 Portfolio Formation** of the paper). We reserve the implementation this NaN-filling process for a future version of this dataset. For the current version, we compound the daily portfolio returns into monthly returns, which is the final form of the data utilized in the paper.  

#### 6. Compound Daily Portfolio Returns to Monthly (final 54 portfolios in CJS)

#### 7. Construction of 18 Portfolio Return Series in He, Kelly, Manela (HKM 2017)

HKM 2017 reduces the 54 portfolio return series constructed in CJS to 18 by taking an equal-weight average across the 3 maturities for the CJS portfolios with the same moneyness. We implement that procedure to obtain the final return series for the FTSFR. 
<br>
<p align="center">* * *</p>

#### Final FTFSR Data Series

The final FTFSR data series comprise the monthly leverage-adjusted returns for call and put portfolios for **both CJS 2013 (54 portfolios) and HKM 2017 (18 portfolios)** for the period from Jan 1996 - Dec 2019. The format for the unique id for each portfolio is as follows: <br><p align="center"><b>{Call C or Put P flag}\_{moneyness * 1000}\_{maturity in days}</b></p>
    
So if we want to retrieve the monthly return series of the Call (<b>C</b>) portfolio with moneyness ($\frac{K}{S}$) of 0.90 (x1000 = <b>900</b>), and maturity of <b>30</b> days, the unique id would be the string <b>'C_900_30'</b>. 





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

# Interesting Packages to Use

## Darts

Darts offers a consistent fit() and predict() interface across various forecasting models (from ARIMA to deep learning models). Easy to understand, compare and switch.

<https://github.com/unit8co/darts>

## Prophet

Prophet is specifically designed for users with limited statistical knowledge.

<https://github.com/facebook/prophet>

## SKTime

SKtime provides a scikit-learn-compatible framework for time series analysis. Allows for easy model tuning, validation, and deployment. You can also use embedded scikit-learn data transformers for feature generation.

<https://github.com/sktime/sktime>

<https://www.sktime.net/en/stable/>

## GluonTS

GluonTS is focused on probabilistic forecasting, allowing users to generate confidence intervals.

<https://github.com/awslabs/gluonts>

<https://ts.gluon.ai/stable/>

# Useful Commands

(We can delete this later. I'm putting these here as they're useful for me while I'm developing)

To run pre-commit hooks on all files:

```bash
pre-commit run --all-files
```

to format all files and fix linting errors:

```bash
ruff format . && ruff check --select I --fix . && ruff check --fix .
```
