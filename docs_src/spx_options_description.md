
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


