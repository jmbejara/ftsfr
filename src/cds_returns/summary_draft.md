# Summary of CDS Return Replication

## 1. Introduction

This notebook replicates monthly CDS portfolio returns as constructed in He, Kelly, and Manela (2017) and Palhares (2013)'s paper *"Cash-Flow Maturity and Risk Premia in CDS Markets."*

> "For CDS, we construct 20 portfolios sorted by spreads using individual name 5-year contracts... Our definition of CDS returns follows Palhares (2013)."

While He, Kelly, and Manela (2017) construct CDS portfolios using data up to 2012, in this notebook we extend the sample period through 2024 for demonstration purposes.  
TODO: MAKE THIS AUTOMATION The underlying Python modules used for data retrieval and processing are designed to be modular and automated, allowing replication to dynamically incorporate the latest available data with minimal modification.

### Target Replication: Quarterly CDS Return Structure

The CDS return series consists of 20 portfolios, formed by sorting 5-year single-name CDS contracts into 4 quintiles based on credit spreads. Each month, returns are computed for portfolios within each quintile, producing 20 total portfolios.


## 2. Data Retrieval

We retrieve the datasets required to replicate the quarterly CDS returns. Retrieval scripts are modularized by source.

### 2.1 CDS Data from Markit

Following He et al. and Palhares, we use Markit as the source for CDS-related information. Specifically, we filter data by the following conditions:

- `currency = 'USD'`: USD-denominated CDS contracts only  
- `docclause LIKE 'XR%%'`: Only XR (no restructuring) contracts  
- `CompositeDepth5Y >= 3`: Minimum 3 dealer submissions for 5Y quotes  
- `tenor IN ('1Y', '3Y', '5Y', '7Y', '10Y')`: Focus on standard maturities

### 2.2 Federal Reserve Zero-Coupon Yields

We retrieve zero-coupon yield data directly from the Federal Reserve, labeled SVENY01 to SVENY30, representing 1-year to 30-year maturities.

### 2.3 Treasury Yield Data

To calculate risk-free rates at shorter maturities, we also retrieve 3-month and 6-month Treasury yields (DGS3MO and DGS6MO) from FRED.

---

## 3. Replication

We follow the return formula used in *He-Kelly-Manela (2017)*, referencing Palhares:

$$
\text{CDS}^{Ret}_t = \frac{\text{CDS}_{t-1}}{250} + \Delta \text{CDS}_t \cdot \text{RD}_{t-1}
$$

Where:

- $\frac{\text{CDS}_{t-1}}{250}$: **Carry return**, daily accrual from previous day’s spread (annualized over 250 days)  
- $\Delta \text{CDS}_t$: Daily change in spread  
- $\text{RD}_{t-1}$: **Risky duration**, proxy for PV of future spread payments

$$
\text{RD}_t = \frac{1}{4} \sum_{j=1}^{4M} e^{-j\lambda/4} \cdot e^{-jr_t^{(j/4)}/4}
$$

Where:

- $M$: CDS maturity (e.g., 5)  
- $r_t^{(j/4)}$: Quarterly risk-free rate  
- $\lambda$: Default intensity, computed as:

$$
\lambda = 4 \cdot \log \left(1 + \frac{\text{CDS}}{4L} \right), \quad L = 0.6
$$


### 3.1. Risk-Free Rate Calculation

We calculate the quarterly risk-free rates $r_t^{(j/4)}$ via interpolation, since the raw data is only available annually (plus 0.25Y and 0.5Y points). Cubic interpolation fills in missing quarterly maturities.

Even though returns are monthly, we retain quarterly rates under the assumption that CDS spreads are paid quarterly.

### 3.2. Monthly Return Computation

We compute monthly CDS returns by applying the above formula for each individual name and maturity. Spread data is first aligned and cleaned at the monthly frequency.


### 3.3. Portfolio Construction

We focus on U.S.-based 5Y CDS contracts and process spreads monthly. For each firm in each month, we keep only the **first observed 5Y par spread**, ensuring consistency in time series construction.

To sort firms into credit quality groups, we compute quintiles based on the cross-sectional distribution of 5Y spreads for each month. These breakpoints define five credit buckets (quantiles 1–5), from safest to riskiest.

We then assign each firm a quantile label based on their spread ranking. This quantile label is merged back into the full dataset, including other tenors (3Y, 7Y, 10Y), allowing us to analyze spread dynamics across maturities while controlling for credit quality.

Finally, we compute the **average par spread** for each combination of:

* Tenor ∈ {3Y, 5Y, 7Y, 10Y}
* Credit Quantile ∈ {1, 2, 3, 4, 5}

This results in 20 tenor–quantile portfolios, each with a monthly spread time series.

