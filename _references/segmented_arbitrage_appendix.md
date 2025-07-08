### Page 1
# Segmented Arbitrage 

Internet Appendix

Emil Siriwardane* ${ }^{*}$ Adi Sunderam ${ }^{\dagger}$ Jonathan Wallen ${ }^{\ddagger}$

October 2023

[^0]
[^0]:    *Siriwardane: Harvard Business School and NBER. E-mail: esiriwardane@hbs.edu
    ${ }^{\dagger}$ Sunderam: Harvard Business School and NBER. E-mail: asunderam@hbs.edu
    ${ }^{\ddagger}$ Wallen: Harvard Business School E-mail: jwallen@hbs.edu

### Page 2
# A. 1 Arbitrage Definitions 

In Appendix A.1, we provide definitions, data sources, and references for each arbitrage spread. The arbitrage spreads span equity, corporate bond, FX, and Treasury markets. For the U.S. equity market, we estimate spreads from spot-futures and put-call parity no-arbitrage conditions. For the corporate bond market, we estimate the CDS-bond spread. For FX markets, we estimate arbitrage spreads implied by covered interest rate parity. For Treasury markets, we estimate arbitrage spreads from spot-futures, Treasury-swap, and TIPS-Treasury no-arbitrage conditions.

## A.1.1 FX CIP Spread

For the FX market, we estimate deviations from covered interest rate parity (CIP). A CIP deviation is a spread between a cash riskless rate and a synthetic riskless rate. The synthetic rate is local currency borrowing swapped into a foreign denominated rate using cross-currency derivatives. With frictionless arbitrage, the cash riskless rate should be equivalent to the synthetic riskless rate. Du et al. (2018) document large arbitrage spreads among G10 currencies against the USD that persisted after the 2008-09 financial crisis. The CIP deviation at time $t$ for currency $c$ against the USD may be expressed as:

$$
\operatorname{CIP}_{t, \tau}^{c} \equiv y_{t, \tau}^{\$}-\left(y_{t, \tau}^{c}-\rho_{t, \tau}^{c}\right)
$$

where $\tau$ is tenor, $y_{t, \tau}^{\$}$ is the continuously compounded dollar riskless rate between $t$ and $t+\tau$, and $\left(y_{t, \tau}^{c}-\rho_{t, \tau}^{c}\right)$ is the synthetic dollar risk-free rate, which is comprised of the foreign currency riskless rate $\left(y_{t, \tau}^{c}\right)$ and the forward premium $\left(\rho_{t, \tau}^{c}\right)$. The forward premium is the annualized difference between the $\log \tau$-period forward $\left(f_{t, \tau}^{c}\right)$ and spot exchange rates $\left(s_{t}^{c}\right)$, both expressed in units of foreign currency per US dollar:

$$
\rho_{t, \tau}^{c} \equiv \frac{1}{\tau}\left(f_{t, \tau}^{c}-s_{t}^{c}\right)
$$

The relevant data is available through Bloomberg. Following Rime et al. (2017) and to be consistent with other arbitrage spreads, we use OIS as the benchmark risk-free rate. We use mid-

### Page 3
prices for spot and forward exchange rates from Bloomberg. We use 3-month tenors to avoid the impact of quarter-end effects on measured correlations. Figure A1a plots daily raw CIP spreads for each currency. When the CIP arbitrage spread is negative, the synthetic dollar funding rate is greater than the OIS dollar risk-free rate.

# A.1.2 Equity Box Spread 

Put-call parity is a no-arbitrage condition relating the difference between the price of European put and call options. For time $t$, tenor $\tau$, and strike price $K_{i}$, let $p_{i, t, \tau}$ denote the price of a put option and $c_{i, t, \tau}$ denote the price of call option. Put-call parity states the difference between two equals the discounted strike price $K_{i}$ and spot price $\left(s_{t}\right)$ and an adjustment for any dividend cash flows $\left(\mathscr{C}_{t, \tau}\right)$ :

$$
p_{i, t, \tau}-c_{i, t, \tau}=\left(\mathscr{C}_{t, \tau}-s_{t}\right)+\exp \left(-r_{t, \tau}^{f} \tau\right) K_{i}
$$

where $r_{t, \tau}^{f}$ is the implied riskless rate from the option pair. van Binsbergen et al. (2019) compute the $r_{t, \tau}^{f}$ using a cross-section of call and put options via the following regression:

$$
p_{i}-c_{i}=\alpha+\beta K_{i}+\varepsilon_{i}
$$

This cross-sectional regression is estimated over all strikes for each time $t$ and tenor $\tau$, and avoids the need to estimate cash flows $\mathscr{C}_{t, \tau}$. The estimated $\beta$ can then be used to back out the implied riskless rate. van Binsbergen et al. (2019) estimate minute-by-minute implied riskless rates from SPX options and then aggregate to the daily level by taking medians. The equity box arbitrage spread equals the difference between the option implied and maturity-matched OIS riskless rates.

We combine estimates from van Binsbergen et al. (2019), which are available on their websites, with OIS rates from Bloomberg. The data from van Binsbergen et al. (2019) ends in March 2018. To better match the rest of our sample, we have also updated their series by applying their same methodology to minute-level SPX options data that runs through the end of our sample. These data were purchased directly through the CBOE. To verify the accuracy of our extended series, we have

### Page 4
compared our option-implied riskless rates to those in van Binsbergen et al. (2019) for the period in which the two series overlap. When regressing their implied riskless rates on ours, the regression constants for the 6,12 , and 18 m series are $-0.68,0.27$, and 0.37 bps , respectively. The estimated slopes are 1.01 in all cases and the $R^{2} \mathrm{~s}$ all exceed 0.9996 .

Figure A1b plots daily raw values for 6, 12, and 18 month equity box arbitrage spreads. When the equity box arbitrage spread is positive, the asset implied risk-free rate from put-call parity is greater than the OIS dollar risk-free rate.

# A.1.3 Equity Spot-Futures 

Following Hazelkorn et al. (2021), we express the no-arbitrage futures price as:

$$
F_{t, \tau}=S_{t}\left(1+r_{t, \tau}^{f}\right)-\mathbb{E}_{t}^{Q}\left[D_{t, \tau}\right]
$$

where $r_{t, \tau}^{f}$ is the riskless rate and $\mathbb{E}_{t}^{Q}\left[D_{t, \tau}\right]$ is the risk-neutral expectation of dividends, both from $t$ to $t+\tau$.

The no-arbitrage condition in Equation (A.5) can also be used to infer implied forward rates. To see why, consider two futures contracts with tenors $\tau_{1}<\tau_{2}$ and let $f_{t}^{\tau_{1}, \tau_{2}}$ denote the time- $t$ forward rate for loans between $\tau_{1}$ and $\tau_{2}$. Rearranging Equation (A.5) and solving for the implied forward rate yields:

$$
1+f_{t}^{\tau_{1}, \tau_{2}}=\frac{1+r_{t, \tau_{2}}^{f}}{1+r_{t, \tau_{1}}^{f}}=\frac{F_{t, \tau_{2}}+\mathbb{E}_{t}^{Q}\left[D_{t, \tau_{2}}\right]}{F_{t, \tau_{1}}+\mathbb{E}_{t}^{Q}\left[D_{t, \tau_{1}}\right]}
$$

We construct arbitrage implied forward rates using the nearby and first deferred futures contracts for the S\&P 500, Dow Jones, and Nasdaq 100 indices. We construct implied forward rates $f_{t}^{\tau_{1}, \tau_{2}}$ rather than raw riskless rates (i.e., $r_{t, \tau_{1}}^{f}$ ) spot rates because spot markets for the equity indices close at 4 pm EST and futures markets close at $4: 15 \mathrm{pm}$ EST. ${ }^{1}$ Because we have only closing prices for both markets, using Equation (A.5) to construct $r_{t, \tau_{1}}^{f}$ will necessarily introduce measurement error

[^0]
[^0]:    ${ }^{1}$ See contract specification for S\&P500 index futures from the CME group at URL: https://www.cmegroup. com/trading/equity-index/us-index/sandp-500_contract_specifications.html

### Page 5
due to the timing mismatch between spot and futures prices. In contrast, implied forward rates in Equation (A.6) rely only on futures prices across different tenors, thereby mitigating any issues with asynchronous closing times. For all three indices, we proxy for expected dividends using realized dividends, an approach that is supported by Hazelkorn et al. (2021). We obtain realized dividends from Bloomberg. We also assume that dividends are paid uniformly between time $t$ and $\tau$. These assumptions have a small impact on the level of implied forward rates, but do not affect their dynamics, which are the focus of our study.

OIS forward rates are a natural benchmark to use when computing arbitrage spreads from implied forward rates $f_{t}^{\tau_{1}, \tau_{2}}$. Ideally, we would obtain OIS forward curves by bootstrapping the OIS swap curve. A computationally simpler alternative is to infer forward rates based on a linearly interpolated OIS swap curve, denoted by $f_{L O I S, t}^{\tau_{1}, \tau_{2}}$. The resulting linearly-interpolated OIS forward rate is over $99 \%$ correlated with the 3-month OIS swap rate, denoted by $O I S_{t}^{3 M}$. We use the latter series when computing equity spot-futures arbitrage spreads because the linearly-interpolated OIS forward rate has mechanical discontinuities around futures roll dates. Formally, we define the equity spot-futures arbitrage spread as:

$$
E S F_{t}=f_{t}^{\tau_{1}, \tau_{2}}-O I S_{t}^{3 M}
$$

We have confirmed that all of our results are robust to subtracting $f_{L O I S, t}^{\tau_{1}, \tau_{2}}$. Again, the main reason is that the benchmark rate used to compute equity spot-futures arbitrage spreads mainly affects their average level, not their correlation with other spreads. Figure A1c plots daily raw arbitrage spreads for the equity spot-futures arbitrage in the three different equity indices. When the equity spot-futures arbitrage spread is positive, the futures implied risk-free rate is greater than the OIS dollar risk-free rate.

# A.1.4 Treasury Spot-Futures 

The no-arbitrage condition in Equation (A.5) can also be used to infer implied riskless rates from Treasury futures prices. In practice, implementing the analogue of Equation (A.5) for Treasury

### Page 6
futures is complicated by the fact that, unlike equity futures, they are settled with physical delivery, as opposed to cash. For a given contract, the futures exchange predetermines the set of eligible deliverable Treasuries and the futures-implied riskless rate is typically computed based on the cheapest-to-deliver security on each date. These issues and other nuances associated with extracting implied riskless rates are discussed in detail by Fleckenstein and Longstaff (2020) and Barth and Kahn (2021). We follow Fleckenstein and Longstaff (2020) and use futures-implied riskless rates that are computed directly by Bloomberg. We do so for futures for 2-year, 5-year, 10-year, 20-year, and 30-year Treasuries. In all cases, we use implied riskless rates from the first deferred futures contract and only include observations with positive trading volume. ${ }^{2}$ This means that within a quarter, the tenor of the implied riskless rate starts at six months and declines to three months over the quarter. We do not use the nearby contract because the seller of Treasury futures has several delivery options during the delivery month, and it is well-known that these options confound prices of the nearby contract in the delivery month (Burghardt and Belton, 2005). For these reasons, most volume in the nearby contract is rolled into the first deferred contract by the beginning of the delivery month (Barth and Kahn, 2021). Finally, to compute arbitrage spreads, we subtract a maturity-matched OIS rate from the futures-implied riskless rate. ${ }^{3}$ Figure A1d plots the raw arbitrage spreads for the different Treasury futures contracts. When the Treasury spot-futures arbitrage spread is positive, the futures implied risk-free rate is greater than the OIS dollar risk-free rate.

# A.1.5 Treasury Swap 

In an interest rate swap, one counterparty agrees to pay a series of predetermined payments based on the so-called fixed rate (or swap rate) prevailing at the swap's inception. In return, the counterparty receives a series of stochastic floating payments that is determined based on the future realization of

[^0]
[^0]:    ${ }^{2}$ The filter on positive trading volume primarily affects the futures contract for 30-year Treasuries.
    ${ }^{3}$ Since the Treasury contract we use has an average tenor of 4.5 months, we use the average of 3 - and 6 -month OIS. Our results are virtual identical if we linearly-interpolate OIS rates to exactly match the remaining tenor of the Treasury contract. However, as discussed above, such linear interpolation introduces mechanical discontinuities around contract roll dates.

### Page 7
a short-term reference rate. For USD-denominated swaps, common reference rates for the floating leg are 3-month LIBOR (LIBOR swaps), the effective Federal Funds rate (overnight index swaps, or OIS), and more recently, the Secured Overnight Financing Rate (SOFR swaps). To understand no-arbitrage restrictions for interest rate swaps, consider an OIS with tenor $\tau$ that pays a fixed rate of $f_{t, \tau}^{\text {OIS }}$ and let $O I S_{t}$ equal the overnight reference rate. Following common practice, we define the Treasury-swap arbitrage spread ("swap spread") as:

$$
S S_{t, \tau}=f_{t, \tau}^{\text {OIS }}-\text { Treas }_{t, \tau}
$$

where Treas $_{t, \tau}$ is the yield of a maturity-matched Treasury. Since the 2008 Global Financial Crisis, it has been well-documented that swap spreads have been negative for several floating reference rates and tenors (Jermann, 2020; Du et al., 2022; Hanson et al., 2022). Negative swap spreads represent an arbitrage because an investor could purchase a Treasury via repo at prevailing secured financing rates (denoted $s_{t}$ ), and simultaneously pay fixed and receive floating in the interest rate swap. This transaction would net the investor:

$$
\begin{aligned}
\text { Profit } & =\left(\text { Treas }_{t, \tau}-s_{t}\right)+\left(\text { OIS }_{t}-f_{t, \tau}^{\text {OIS }}\right) \\
& =\underbrace{\left(\text { Treas }_{t, \tau}-f_{t, \tau}^{\text {OIS }}\right)}_{-S S_{t, \tau}}+\left(\text { OIS }_{t}-s_{t}\right)
\end{aligned}
$$

Here, the first term is positive by assumption and the second term equals the difference between the OIS rate (an unsecured rate) and the overnight secured borrowing rate for Treasuries, $s_{t}$. Under the natural assumption that unsecured rates are higher than secured ones in every state of the world, the investor will therefore earn a positive arbitrage profit if swap spreads are negative. As Hanson et al. (2022) and others have argued, this logic also implies that positive swap spreads are only an arbitrage when the underlying reference rate is the secured overnight borrowing rate (i.e., for SOFR swaps).

The preceding discussion suggests that SOFR swaps are the ideal derivative for our analysis.

### Page 8
However, because SOFR swaps began trading only in 2018, we instead focus on OIS and obtain their swap rates from Bloomberg for maturities of $1,2,3,5,10,20$, and 30 years. We compute swap spreads $S S_{t, \tau}$ for each tenor by subtracting out maturity-matched Treasury yields. We chose OIS over LIBOR swaps to minimize any mechanical variation in swap spreads that is driven by bank credit risk.

Figure A1e plots daily raw arbitrage spreads for swap contracts of different tenors. The 1, 2, $3,5,10,20$, and 30-year swap spreads are negative for $65 \%, 81 \%, 89 \%, 97 \%, 100 \%, 100 \%$, and $100 \%$ of our analysis sample, respectively.

# A.1.6 TIPS Treasury 

In the market for US sovereign debt, there is a no-arbitrage condition between inflation-swapped Treasury Inflation-Protected Securities (TIPS) and Treasuries (Fleckenstein et al., 2014). TIPS are US Treasury obligations for which the principal amount (and coupons) are adjusted for the Consumer Price Index (CPI). These inflation adjustments may be undone using an inflation swap, yielding fixed cash flows. The arbitrage spread is the difference in yield between this synthetic nominal Treasury constructed from TIPS and inflation swaps and a nominal Treasury. Define $y_{T, t, \tau}$ to be the Treasury yield, $s_{t, \tau}$ to be the TIPS yield, and $f_{t, \tau}$ to be the fixed inflation swap rate. The TIPS-Treasury spread $\left(\mathrm{TT}_{t, \tau}\right)$ is

$$
\mathrm{TT}_{t, \tau}=\left(s_{t, \tau}+f_{t, \tau}\right)-y_{T, t, \tau}
$$

To build the arbitrage, we use zero-coupon constant-maturity TIPS and Treasury yields, as well as constant-maturity inflation swaps. ${ }^{4}$ We focus on 2, 5, 10, and 20 year maturities to ensure the underlying TIPS securities used to construct the arbitrage are sufficiently liquid. Fleckenstein et al. (2014) instead build the TIPS-Treasury arbitrage based on the prices of individual Treasury and TIPS securities. We have verified that the two approaches deliver very similar arbitrage series (over

[^0]
[^0]:    ${ }^{4}$ Zero-coupon yields are taken directly from the Federal Reserve's Yield Curve Model https://www.federalreserve.gov/data/yield-curve-models.htm and inflation swap data is from Bloomberg.

### Page 9
$90 \%$ correlated) and we favor ours due to its simplicity.

# A.1.7 Corporate CDS-Bond Spread 

We build arbitrage spreads and implied riskless rates based on the relative pricing of corporate credit default swaps (CDS) and risky bonds. Corporate CDS are essentially an insurance contract against the default of an underlying corporate debt security. The buyer of CDS protection pays a fixed annuity premium (the CDS spread) to the seller for a pre-specified horizon $\tau$. In return, if there is a default event before $\tau$, the seller pays the buyer the difference between the par value of the security and its market value. Duffie (1999) formally shows that the cash flows from purchasing CDS protection on firm $i$ are equivalent to a portfolio that is long a default-free float rate note and short the floating rate debt of firm $i$. Consequently, the CDS spread should equal the floating rate spread, defined as the spread of par floating rate debt for firm $i$ over the riskless rate. Intuitively, an investor who simultaneously purchases the debt of a risky issuer and CDS protection on that same issuer faces no credit risk, and should therefore earn the riskless rate.

Because most corporate entities do not issue floating rate debt, it common practice to use so-called Z-spreads or asset swap spreads to infer the floating rate spread from the price of fixed rate corporate debt (Choudhry, 2018). Let $F R_{i, t, \tau}$ denote the time- $t$ floating rate spread implied by a fixed-rate bond issued by firm $i$ with tenor $\tau$. Motivated by the no-arbitrage logic above, we define the CDS-bond arbitrage spread (or basis) for debt issued by firm $i$ with tenor $\tau$ as follows: ${ }^{5}$

$$
C B_{i, t, \tau}=C D S_{i, t, \tau}-F R_{i, t, \tau}
$$

where $C D S_{i, t, \tau}$ is the maturity-matched CDS spread for firm $i$. This object can be bootstrapped based on the market values of CDS contracts trading on firm $i$ at each point in time. A negative basis implies that the bond is trading a low price relative to the CDS, and an investor could earn a

[^0]
[^0]:    ${ }^{5}$ There are several alternative methodologies for defining the CDS-bond basis that account for the fact that most corporate debt is fixed, not floating rate (see Bai and Collin-Dufresne, 2019 for a complete discussion). Z-spreads and asset swap spreads are readily available to us from our data provider (Markit) and so we use them for simplicity.

### Page 10
positive arbitrage profit by going long the bond and purchasing CDS protection.
We build individual bond bases using data from Markit. Markit's bond pricing platform contains daily prices for a wide range of globally issued bonds, with pricing information sourced from market-makers, TRACE, and FINRA. ${ }^{6}$ For each bond issue, Markit also computes the Z-spread and the implied par asset-swap spread. Z-spreads are more populated in Markit and so we use them to proxy for $F R_{i, t, \tau}$ in Equation (A.8). We use par asset-swap spreads when Z-spreads are not available. In addition, Markit uses daily CDS pricing to bootstrap the CDS spread $C D S_{i, t, \tau}$ associated with the maturity of each bond. When Markit's bootstrapped value is unavailable, we compute it ourselves by interpolating using cubic spline over constant-maturity CDS spreads that are also sourced from Markit. For each bond, we also compute a maturity-matched Treasury yield (denoted $y_{t, \tau}$ ) using a cubic spline interpolation and define the arbitrage-implied riskless rate as $r f_{i, t, \tau}^{C D S}=y_{t, \tau}-C B_{i, t, \tau}$. Finally, we create aggregate indices by taking the equal-weighted average of individual bond bases $C B_{i, t, \tau}$ and implied riskless rates $r f_{i, t, \tau}^{C D S}$ for both investment grade (IG) and high-yield rated firms (HY).

We apply several filters to the Markit bond database, mainly to ensure we only use liquid and reliable bond prices in our IG and HY indices. Specifically, we: (i) include only senior unsecured debt that is issued in USD by U.S. firms and has a non-missing ISIN; (ii) include fixed rate bonds with maturity between 1 and 10 years; (iii) include only bonds with an outstanding principle of at least $\$ 100,000$, where principal values are sourced from Mergent and matched to Markit using ISINs; (iv) exclude putable and convertible bonds; and (v) exclude bonds whose composite price is less than fifty cents on the dollar. To further ensure we use reliable bond pricing, in a given month we only include bonds whose ISINs are included in the WRDS Bond Return dataset. The WRDS Bond Return data is based on a cleaned set of bond transactions sourced from TRACE and TRACE enhanced.

Figure A1g plots daily raw average arbitrage spreads for investment grade (IG) and high yield (HY) bonds. Over our sample period, the IG CDS-Bond arbitrage index reflects an average of 1,690

[^0]
[^0]:    ${ }^{6}$ See the Markit pricing brochure for more information.

### Page 11
bonds per day issued by 358 firms. Over the same period, the HY index reflects an average of 307 bonds per day issued by 108 unique firms.

# A.1.8 Synchronicity of Prices 

For the computation of each arbitrage spread, we use New York closing prices (5PM Eastern Time) when available. We have synchronously measured arbitrage spreads at New York closing prices for the following trades: CIP, Treasury spot-futures, TIPS-Treasury, and Treasury-swap. For the equity spot-futures trade, the closing price is at 4:15 pm Eastern Time. For the Equity-Box asset implied risk-free rate, van Binsbergen et al. (2019) reports the median of minute-level estimates over the day. All arbitrage spreads are measured from mid-prices of composite quotes by multiple dealers. CDS and asset swaps spreads are based on both transactions and quotes that are aggregated by Markit.

## A.1.9 Outliers

Some short-tenor arbitrages (CIP, equity spot-futures, and Treasury spot-futures) have clear outliers in their arbitrage spreads. Following Barndorff-Nielsen et al. (2009), we drop observations for which the arbitrage spread deviated more than 10 mean absolute deviations from a rolling centered median (excluding the observation under consideration) of 90 days ( 45 days after and 45 days before).

## A. 2 Additional Results and Discussion

## A.2.1 The Impact of Measurement Error

The analysis in Section 3.2.2 is designed to address concerns that the arbitrage spread correlations are biased down by measurement error. Eq. 8 shows that any such attenuation bias can be directly addressed with knowledge of the adjustment factors, $\lambda_{i}$. These factors reflect how much of the total observed spread variance is driven by the true spread. If arbitrage spreads follow a one-factor model,

### Page 12
the adjustment factors can be estimated using instrumental variables (IV) regressions (Hausman, 2001). Specifically, for each spread $i$ we first run the following OLS regression:

$$
s_{j t}=\alpha_{i}+\beta_{i}^{O L S} s_{i t}+\varepsilon_{i t}
$$

where we pool all observations for which $j \neq i$. We then run an analogous IV regression with two instruments for $s_{i t}$ : (i) the observed arbitrage spread on the last day of the previous quarter, and (ii) the average observed arbitrage spread in the previous quarter. The idea behind these instruments is that any error induced by execution details of individual trades in the current quarter should be uncorrelated with errors from the previous quarter. Concretely, consider the Treasury spot-futures trade and suppose the contract we use to compute $s_{i, t}$ expires in September. Our instruments instead reflect an entirely different futures contract (i.e., the June contract).

Let $\beta_{i}^{J V}$ denote the IV estimate from regression (A.9). Under the null of a one-factor model for arbitrage spreads and assuming our instruments are valid, the ratio of the IV and OLS estimates reveals the measurement error variance relative to true variance (Hausman, 2001):

$$
\lambda_{i}=\sqrt{\frac{\beta_{i}^{I V}}{\beta_{i}^{O L S}}}
$$

We estimate the $\lambda_{i} \mathrm{~s}$ individually and use them to adjust the measured correlations up according to Eq. 8 To be maximally conservative, we focus on trades with short tenors for which convergence risk should be relatively unimportant (see Section 3.2.3). The average adjusted correlation equals 0.20 , similar to the overall average measured correlation and the average for short-tenor trades. The distributions of adjusted and unadjusted correlations are also comparable: the 25th and 75th percentile of adjusted correlations are -0.08 and 0.45 , respectively. These results cut against the idea that true spreads follow a one-factor structure but their measured correlation is biased toward zero by noise.

### Page 13
# A.2.2 Arbitrage Spreads Prior to the Dodd-Frank Era 

It is also interesting to compare the comovement of arbitrage spreads during the Covid-19 pandemic to the Global Financial Crisis (GFC). Table A1a shows the average pairwise correlations of spreads for the period of June 2007 through June 2009. For this analysis, we cannot include the Treasury spot-futures and swap arbitrages due to data limitations. The average correlation during the GFC was 0.66 , materially higher than during Covid-19.

One interpretation of this finding is that post-GFC regulation has raised the cost of conducting arbitrage activity (Du et al., 2018), thereby making it more difficult for integrated arbitrageurs to enter markets. However, a few additional patterns in the data suggest some caution in drawing this conclusion. For instance, Table A1b indicates that correlations were also low prior to the GFC. In addition, Figure A2 provides evidence of both balance sheet and funding segmentation prior to the passage of the Dodd-Frank Act in 2010. Consistent with the presence of balance sheet segmentation, Figure A2a shows that equity spot-futures spreads rose sharply relative to other unsecured trades after two Bear Stearns hedge funds took heavy losses due to margin calls (Khandani and Lo, 2011). Consistent with the presence of funding segmentation, Figure A2b shows that both the TED spread and unsecured arbitrage spreads rose sharply after Lehman Brothers declared bankruptcy. In contrast, secured arbitrage spreads did not rise for several weeks.

## A.2.3 Covariance Decomposition

In Section 3.3, we use sign-restricted SVARs to separate supply and demand shocks to arbitrage spreads. For a given trade $i$, the SVAR assumes the following dynamics for spreads $s_{i t}$ and quantities $q_{i t}$ :

$$
B_{i} Y_{i, t}=A_{i, 0}+A_{i, 1} Y_{i, t-1}+\varepsilon_{i, t}
$$

where $Y_{i t}=\left[\begin{array}{ll}s_{i t} & q_{i t}\end{array}\right]^{\prime}$. The reduced-form representation of the SVAR is given by:

$$
Y_{i, t}=\Phi_{i, 0}+\Phi_{i, 1} Y_{i, t-1}+u_{i, t}
$$

### Page 14
where $\Phi_{i, 0}=B_{i}^{-1} A_{i, 0}$ and $\Phi_{i, 1}=B_{i}^{-1} A_{i, 1}$. The covariance matrix of the reduced-form residuals $u_{i, t}=B_{i}^{-1} \varepsilon_{i, t}=\left[\begin{array}{ll}u_{i, s, t} & u_{i, q, t}\end{array}\right]^{\prime}$ is given by $\Sigma_{i, u}$ and depends only on the matrix $B_{i}$. This dynamic system makes it possible to decompose the covariance between two arbitrage spreads $s_{i, t}$ and $s_{j, t}$ into comovement that arises between supply shocks, demand shocks, and the intersection of the two. To see this more formally, let:

$$
X_{t}=\left[\begin{array}{l}
Y_{i t} \\
Y_{j t}
\end{array}\right], A=\left[\begin{array}{l}
\Phi_{i, 0} \\
\Phi_{j, 0}
\end{array}\right], \varepsilon_{t}=\left[\begin{array}{l}
\varepsilon_{i, t} \\
\varepsilon_{j, t}
\end{array}\right]
$$

be the stacked $(4 \times 1)$ vectors of price-quantity pairs, constants from the reduced form SVAR, and structural shocks. With some abuse of notation, further define define the $4 x 4$ matrix $\Phi$ as:

$$
\Phi=\left[\begin{array}{cc}
\Phi_{i} & 0_{2 \times 2} \\
0_{2 \times 2} & \Phi_{j}
\end{array}\right]
$$

and the $4 x 4$ matrix $B$ as:

$$
B=\left[\begin{array}{cc}
B_{i} & 0_{2 \times 2} \\
0_{2 \times 2} & B_{j}
\end{array}\right]
$$

Then, in reduced form, the SVAR system can be written as:

$$
X_{t}=A+\Phi X_{t-1}+B \varepsilon_{t}
$$

Assuming that $X_{t}$ is covariance stationary, then its covariance matrix $\Sigma_{X}$ is given by:

$$
\Sigma_{x}=\Phi \Sigma_{x} \Phi^{\prime}+B \Sigma_{\varepsilon} B^{\prime}
$$

where $\Sigma_{\varepsilon}$ is the variance-covariance matrix of $\varepsilon_{t}$. This equation implies that:

$$
\operatorname{vec}\left(\Sigma_{x}\right)=\underbrace{\left(I_{16 \times 16}-\Phi \otimes \Phi\right)^{-1}(B \otimes B)}_{\Gamma} \cdot \operatorname{vec}\left(\Sigma_{\varepsilon}\right)
$$

### Page 15
where we use the fact that $\operatorname{vec}(D E F)=\left(F^{T} \otimes D\right) \operatorname{vec}(E)$, for a $k \times l$ matrix $D$, a $l \times m$ matrix $E$, and an $m \times n$ matrix $F$. To finish the decomposition, focus on the third element of $\operatorname{vec}\left(\Sigma_{x}\right)=\operatorname{cov}\left(s_{1, t}, s_{2, t}\right)$ and let $\gamma$ be the third row of $\Gamma$. Then, the covariance between two spreads is given by:

$$
\operatorname{cov}\left(s_{i, t}, s_{j, t}\right)=\gamma \operatorname{vec}\left(\Sigma_{\varepsilon}\right)
$$

or, dividing through by $\operatorname{cov}\left(s_{i, t}, s_{j, t}\right)$ yields the following covariance decomposition (in vector form):

$$
1=\frac{\gamma \operatorname{vec}\left(\Sigma_{\varepsilon}\right)}{\operatorname{cov}\left(s_{i, t}, s_{j, t}\right)}
$$

If $\gamma_{k}$ denotes the $k$-th element of $\gamma$, then Equation (A.11) can be written as:

$$
\begin{aligned}
1= & \frac{\left(\gamma_{1}+\gamma_{6}+\gamma_{11}+\gamma_{16}\right)}{\mathbb{C}\left(s_{i, t}, s_{j, t}\right)} \\
& +\left(\gamma_{3}+\gamma_{9}\right) \frac{\mathbb{C}\left(\varepsilon_{s t}^{i}, \varepsilon_{s t}^{j}\right)}{\mathbb{C}\left(s_{i, t}, s_{j, t}\right)} \\
& +\left(\gamma_{4}+\gamma_{13}\right) \frac{\mathbb{C}\left(\varepsilon_{s t}^{i}, \varepsilon_{d t}^{j}\right)}{\mathbb{C}\left(s_{i, t}, s_{j, t}\right)} \\
& +\left(\gamma_{7}+\gamma_{10}\right) \frac{\mathbb{C}\left(\varepsilon_{d t}^{i}, \varepsilon_{s t}^{j}\right)}{\mathbb{C}\left(s_{i, t}, s_{j, t}\right)} \\
& \left(\gamma_{8}+\gamma_{14}\right) \frac{\mathbb{C}\left(\varepsilon_{d t}^{i}, \varepsilon_{d t}^{j}\right)}{\mathbb{C}\left(s_{i, t}, s_{j, t}\right)}
\end{aligned}
$$

The second and fifth term in the decomposition capture the portion of spread covariance driven by comovement in supply and demand shocks, respectively. The third and forth terms reflect covariance arising due to comovement between $i$ 's supply and $j$ 's demand shock (and vice versa). These quantities are straightforward to compute using the estimated SVAR parameters and structural shocks. ${ }^{7}$

[^0]
[^0]:    ${ }^{7}$ In all cases, decomposition is implemented for the median structural parameter vector (and associated shock series) from the identified SVAR parameter set $\Theta_{i}$.

### Page 16
# A.2.4 Balance Sheet vs Funding Shocks 

Our analysis in Section 4.2 uses the 2016 MMF Reform to study how a funding shock differentially impacts the cross section of arbitrage. The key assumption in that analysis is that the reform was not a balance sheet shock for banks. To understand why this is a plausible assumption, it is helpful to first consider how the distinction between funding and balance sheet shocks appears in the model of Section 2. Within the model, balance sheet shocks can arise for two reasons. The first is a change in balance sheet requirements, $V_{t}$. For example, under Basel III, the supplementary leverage ratio (SLR) requires the largest U.S. banks to hold 5\% of common equity relative to their assets. A change in the minimum required equity under the SLR would therefore constitute a balance sheet shock.

The second reason for a balance sheet shock within the model is a change in frictional adjustment costs, $c_{t}$. These costs can be thought of as the wedge between the rate of return that must be paid to raise outside equity and the rate that would arise in the absence of informational asymmetries between managers and outside investors, i.e., $c_{t}$ is zero in Modigliani and Miller (1958). A shock to $c_{t}$ could occur if outside equity holders became worried about the quality of assets held by an arbitrager, as was the case for banks with large holdings in special purpose vehicles during the 2008 financial crisis.

In contrast to balance sheet shocks, funding shocks in the model represent changes in the rate $f_{t}$ at which a specific arbitrage trade can be financed (in excess of the riskless rate). These costs are assumed to be non-zero due to violations of Modigliani and Miller (1958) in funding markets arbitragers cannot finance a riskless portfolio at the riskless rate.

In the language of our model, the 2016 MMF reform did not change balance sheet requirements for arbitragers $\left(V_{t}\right)$. It is also unlikely that frictional adjustment costs $c_{t}$ were materially affected by the reform. The reason why is that the reform forced prime MMFs to switch from reporting a stable to floating net asset values, which presumably did not impact any informational asymmetries that exist between banks (or other arbitragers) and their outside investors. We therefore find it most natural to view the reform as a shock to funding $f_{t}$ for unsecured arbitrages because prime money

### Page 17
funds were large lenders of commercial paper to banks.
Consistent with this interpretation, Figure A3 shows that the balance sheet strength of dealers was not negatively affected by the reform. The measure of balance sheet strength in the plot comes directly from He et al. (2017) and is defined as the ratio of market capitalization to market capitalization plus book debt for the New York Federal Reserve's primary dealers' publicly-traded holding companies. If anything, the balance sheet strength of dealers improved through the MMF Reform compliance date, driven mostly by positive stock market returns. The fact that unsecured arbitrage spreads nonetheless rose during this period therefore supports our interpretation of the reform as a funding shock. Anderson et al. (2019) also argue that the reform was a funding shock that caused banks to subsequently withdraw from CIP and central bank reserve arbitrage. We instead use the shock to trace out funding segmentation in the cross section or arbitrage.

It is also worth clarifying whether banks finance arbitrage or participate directly as arbitragers. In reality, they do both, depending on the type of trade. For unsecured arbitrages, banks likely participate as arbitragers and our analysis of the JP Morgan London Whale in Section 5.2 is consistent with this view. In addition, banks also appear to be active participants in CIP arbitrage (Du et al., 2018). For secured arbitrages, banks likely finance arbitrage trading through their role in the repo market (and as prime brokers). However, this is not a perfect delineation, as banks may also participate in longer-dated secured trades like the 30-year Treasury swap arbitrage (Du et al., 2022).

We also want to note that our analysis in Section 4 does not imply that banks simply finance arbitrage. In fact, as noted above, banks likely participate in unsecured arbitrages precisely because they can more easily raise unsecured funding relative to other institutions. For example, banks can borrow unsecured via the commercial paper market whereas hedge funds cannot. Thus, funding and balance sheet segmentation likely interact in equilibrium.

# A.2.5 Event Study Analysis and the Persistence of Arbitrage Spreads 

In Sections 4.2, 5.2, and 5.3 we use event studies to analyze the impact of various events on arbitrage spreads (e.g., the 2016 MMF Reform). These analyses are all structured around regressions of the

### Page 18
following form:

$$
s_{i, t}=\alpha_{i}+\alpha_{t}+\sum_{j=-L}^{F} \beta_{j} 1[i \in G] \times 1[t=j]+\varepsilon_{i, t}
$$

where $s_{i, t}$ is the arbitrage spread of trade $i$ at date $t, \alpha_{i}$ is a fixed effect for trade, and $\alpha_{t}$ is a fixed effect for time. $1[i \in G]$ is an indicator for whether trade $i$ is in group $G$ and $1[t=j]$ is an indicator for whether time $t$ equals $j$. All dates are in event time and centered around $t=0$. For example, in our analysis of the 2016 MMF reform in Section 4.2, $G$ is the set of unsecured arbitrages and $t=0$ corresponds to days in October 2016, the month in which compliance of the reform was required.

A natural concern with regression (A.12) is that the persistence of spreads $s_{i, t}$ distorts our inference of the $\beta_{j}$ 's. We address this concern by computing standard errors in two different ways. First, we cluster by time and trade, the latter of which allows for arbitrary correlations within trades. Second, we cluster by time and use Driscoll and Kraay (1998) standard errors within each trade. Driscoll and Kraay (1998) develop the panel analogue of the heteroskedasticity-and-autocorrelationrobust (HAR) standard errors from Newey and West (1987). As in Newey and West (1987), the Driscoll and Kraay (1998) estimator requires a choice of a lag length over which to compute the parameter covariance matrix. Our baseline lag length of 8 is based on the rules of thumb proposed in Newey and West (1987) and Andrews (1991). ${ }^{8}$

Figure A4 shows the estimates of $\beta_{j}$ for our analysis of the money market reform of 2016. These estimates correspond exactly to those found in column (2) of Table 7. Recall that the goal of this analysis is to test whether the reform differentially impacted unsecured versus secured arbitrage. The blue dots show standard error bands based on clustering by time and trade. The orange dots show the same bands based on clustering by time and using Driscoll and Kraay (1998) with 8 lags. The main takeaway is that the two approaches deliver similar standard errors, though clustering by time and trade appears to be slightly more conservative. For this reason, we cluster by time and trade in all of our event-study analyses.

[^0]
[^0]:    ${ }^{8}$ More recently, Lazarus et al. (2018) analyze the popular rules of thumb for lag length selection and suggest modifications that improve the coverage rates of HAR standard errors. In our setting, their suggestion implies a lag selection of around 60, though we find that a lag length of 8 generally delivers more conservative standard errors.

### Page 19
# A.2.6 Marginal Financing of Unsecured Trades 

In Section 4.2 (Table 6), we find that the sensitivity of unsecured arbitrage spreads to the TED spread generally exceeds the margin requirements listed in Table 5. Our interpretation is that the marginal dollar of financing for these trades requires more unsecured funding than on average. We would ideally confirm this interpretation with data on how arbitragers using unsecured strategies (CIP, Box, and Equity spot-futures) finance their trading activity. Because this data is difficult to obtain, we instead present suggestive evidence by comparing the value of equity securities held by dealers to the size of the equity repo market. We calculate the former based on Y-9C regulatory filings by all U.S. bank holding companies, and we calculate the latter based on public data provided by the New York Federal Reserve. Figure A5 plots the two series starting in 2010Q2, which is when equity repo market data first becomes available. The key takeaway is that the U.S. equity repo market does not appear large enough to fully finance the holdings of equities by U.S. bank holding companies. On average, the collateral value in the equity repo market is $41 \%$ of the value of equities held by U.S. bank holding companies. Thus, to the extent that U.S. bank holding companies are active in equity spot-futures arbitrage, it seems unlikely that their marginal dollar of arbitrage financing comes from the equity repo market. ${ }^{9}$

## A.2.7 First-Stage IV for Analysis of Fidelity Flows

In Section 4.3, we illustrate funding segmentation by showing that supply shocks from Fidelity MMFs uniquely impact equity-spot futures arbitrage. We isolate supply shocks using an IV strategy in which we instrument for Fidelity flows using what we call "passive Fidelity flows,"defined as flows to the aggregate MMF sector in month $t$ interacted with Fidelity's share of MMF assets measured at $t-6$. Table A2 shows the first-stage regression results for the IVs reported in columns (4)-(6) of Table 8. The only thing that differs across the columns is the estimation sample. The first column corresponds to the sample used when the outcome variable in the IV regression is the

[^0]
[^0]:    ${ }^{9}$ The sensitivity of equity spot-futures arbitrages to the TED spread (Section 4.2) and the event study of the JPMorgan London Whale (Section 5.2) both suggest that U.S. dealers are indeed active in equity spot-futures arbitrage.

### Page 20
implied riskless rate in the equity-spot futures arbitrage. The second corresponds to the sample used when the outcome is the implied riskless rate in other secured arbitrages (CIP and Box), and the third corresponds the sample using secured arbitrages. In all cases, the sign of the coefficient on passive Fidelity flows is positive as expected and highly significant. Thus, our IV does not suffer from a weak instruments problem.

# A.2.8 Futures Roll Dates and the JPM London Whale 

In Section 5.2 we study the behavior of equity spot-futures arbitrage around the JP Morgan London Whale episode in 2012. Our analysis focuses on two key dates through this period, March 1, 2012 and June 13, 2012. There is a particularly large and sudden spike around the latter date, which was the day that Jamie Dimon testified before Congress and announced that significant additional losses were to be expected at the firm's next conference call with shareholders. We interpret this spike as being driven by a tightening of JPM's balance sheet. However, a potential confounding factor with this interpretation is that the June 2012 futures contract expired on June 15, 2012. Because most equity futures trading rolls out of the nearby contract in the week prior to expiration, the spike in arbitrage spreads could be mechanically driven by futures rolling as opposed to changes JPM's balance sheet capacity.

To rule this potential alternative out, we compute the change $\Delta s_{i, m}$ for arbitrage $i$ around the third Friday in each month $m$. Specifically, in each month, we construct the change in spreads between the eight days prior to the third Friday in the month and the first business day after the third Friday. The logic of this window size is that it should bookend the period during which futures contracts roll during expiration months. We then run the following panel regression using only equity-spot futures arbitrages:

$$
\Delta s_{i, m}=c+\beta 1[m \in \text { Expiration Month, except June 2012 }]+\theta 1[m=\text { June 2012 }]+\varepsilon_{i, t}
$$

where $1[m \in$ Expiration Month, except June 2012] is an indicator variable if $m$ is a futures expiration

### Page 21
month (March, June, September, and December) excluding June of 2012. The indicator $1 \mid m=$ June 2012] equals one if the month is June 2012.

Figure A6 plots the estimated coefficients from regression (A.13) and their $95 \%$ confidence intervals based on robust standard errors. The plot shows that equity-spot futures spreads do not materially increase during roll periods outside of June 2012, as the estimated $\beta$ is small and not statistically different from zero. In contrast, the spike that occurred in June 2012 was an order of magnitude larger than the one that typically occurs during roll periods (roughly 30 bps vs 3 bps ). The estimated $\theta$ is also statistically different than zero and is such that we can reject the null that the June 2012 change is equal to the change during other roll months. We therefore conclude that futures contract rolling is not the primary driver of the spike in equity spot-futures arbitrage that occurred during June 2012.

# A.2.9 Arbitrage Returns 

In Section 6.1, we use the sign-restricted SVARs from Section 3.3 to study the persistence of arbitrage segmentation. Here, we supplement that analysis by studying the returns to arbitrage, as opposed to the level of spreads. Specifically, we proceed as follows. First, let $s_{t}(m)$ denote the annualized arbitrage spread for a trade with tenor $m$ on date $t .{ }^{10}$ Then the return to the arbitrage between $t$ and $t+h$ is given by:

$$
r_{t, t+h}=\frac{\left[1+s_{t}(m)\right]^{m}}{\left[1+s_{t+h}(m-h)\right]^{m-h}}-1
$$

To understand the formula, note that on date $t$, the arbitrager essentially purchases a default-free zero-coupon bond with maturity $m$ and yield-to-maturity $s_{t}(m)$. The price of this bond equals $P_{t}=\left[1+s_{t}(m)\right]^{-m}$. At date $t+h$, the remaining maturity of the bond is $m-h$ and the arbitrager sells it at prevailing market yields, meaning the sale price equals $P_{t+h}=\left[1+s_{t+h}(m-h)\right]^{-(m-h)}$.

[^0]
[^0]:    ${ }^{10}$ For CIP, Equity spot-futures, and Treasury spot-futures we use $m=3$ months. For the CDS-Bond basis, we assume $m=5$ years, which is roughly based on the tenor of the underlying bonds and swaps in the arbitrage. The tenor of the remaining trades is based on the maturity of their underlying swap (e.g, $m=30$ years for the 30-year Treasury-swap trade).

### Page 22
The return to this trade equals $r_{t, t+h}=P_{t+h} / P_{t}-1$, which after some rearrangement delivers Equation (A.14). Intuitively, when $m=h$, the trade is held to maturity and its annualized return equals its initial spread $s_{t}(m)$.

For simplicity, we further assume that the term structure of arbitrage spreads is relatively flat, at least locally, so that $s_{t+h}(m-h) \approx s_{t+h}(m)$. For example, consider holding the 30-year Treasury swap spread for one quarter $(m=30, h=1 / 4)$. While the term structure of Treasury swap arbitrage spreads is not flat over tenors spanning years, the simpler and more plausible assumption we are making is that the 30-year and 29.75-year Treasury swap arbitrages are relatively similar in magnitude. The more complicated alternative would be to build term structures of arbitrage spreads for every strategy and then interpolate $s_{t+h}(m-h)$. It is also important to note that the arbitrage returns in Equation (A.14) do not reflect the actual rates of return earned by arbitrages because they ignore transaction costs and funding rates. Instead, and as mentioned in Section 2, returns reflect the shadow cost of funding and other frictions facing arbitrages, which is precisely what we seek to characterize.

Three main patterns emerge when analyzing the returns arbitrage over different horizons. First, the returns to different trades become more correlated as the horizon of the holding period increases. Figure A7 demonstrates this visually by showing the average pairwise correlation of trades for holding periods ranging from one day to one quarter. We do not consider holding periods of longer than one quarter because this would exceed the initial tenor of many trades (e.g., CIP). The figure shows that the average correlation of one-quarter returns is roughly triple that of one-day returns. The fact that the correlation increases with the holding period is consistent with the idea that arbitrage capital flows slowly across different strategies, as in theories of slow-moving capital (Duffie, 2010).

Second, and more importantly, the correlation of arbitrage returns is still very far from perfect ( $\sim 15 \%$ ) even for holding periods of one quarter. This finding accords with our analysis in Table 3a, which shows that spread levels of short-tenor trades are only weakly correlated. Recall that for these trades, the ex-post quarterly return to arbitrage essentially and the ex-ante observed spread

### Page 23
are roughly equal because the trades are essentially held to maturity. The fact that arbitrage returns remain relatively uncorrelated even over quarterly holding periods suggests a fairly persistent form of segmentation.

The third takeaway from studying arbitrage returns is that there are certain markets or trades that do appear more integrated over the long run (see our response to Point \#2 as well). For example, consider the 3-month GBP CIP and the 10-year Treasury swap trades. At a daily level, the return correlation between the two trades is only $6 \%$, yet their correlation increases to $24 \%$ and $45 \%$ for holding periods of one month and one quarter, respectively. This result accords with Du et al. (2022) and is consistent with the idea that large dealers are active in both trades.

# A. 3 Multiple Tenors 

We extend the model in the main text in two ways. First, we consider two time periods $t=1,2$. Second, we allow for two-period contracts in the first period. For simplicity assume an integrated intermediary facing a single balance sheet constraint. At time $t=1$, the arbitrageur's problem is:

$$
\max \sum_{n=1}^{N}\left(q_{n, 1} s_{n, 1}\right)-\frac{1}{2} c_{1,1} V_{1,1}^{2}+E\left[\sum_{n=1}^{N}\left(q_{n, 2} s_{n, 2}\right)-\frac{1}{2} c_{1,2} V_{1,2}^{2}\right]
$$

The first order condition for one-period trades is the same as in the main model:

$$
s_{n, 1}=v_{n, 1} c_{1,1} V_{1,1}=v_{n, 1} c_{1,1}\left(\sum_{n} a_{n, 1} v_{n, 1}\right)
$$

For these trades, only the marginal cost of balance sheet constraint at time 1 matters. In contrast, the first order condition for two-period contracts is given by:

$$
s_{n, 1}=v_{n, 1}\left(c_{1,1} V_{1,1}+E\left[c_{1,2} V_{1,2}\right]\right)=v_{n, 1}\left(c_{1,1}\left(\sum_{n} a_{n, 1} v_{n, 1}\right)+E\left[c_{1,2}\left(\sum_{n} a_{n, 2} v_{n, 2}\right)\right]\right)
$$

Two-period contracts follow a two-factor structure: they depend on the marginal cost of balance

### Page 24
sheet at time 1 and the expected marginal cost of balance sheet at time 2. Thus, all one-period contracts are perfectly correlated, all two-period contracts are perfectly correlated, but one-period contracts are imperfectly correlated with two-period contracts. While we have maintained risk-neutrality in this example, Du et al. (2022) and Hanson et al. (2022) show that similar intuitions hold when arbitrageurs are risk averse and have short horizons. Our analysis in the main text constructs correlations between trades with similar tenors, thus showing that the low correlation of arbitrage spreads is not simply due to comparing trades with different tenors.

### Page 25
# References 

Anderson, A., W. Du, and B. Schlusche (2019). Money market fund reform and arbitrage capital. 16

Andrews, D. W. K. (1991). Heteroskedasticity and autocorrelation consistent covariance matrix estimation. Econometrica 59(3), 817-858. 17

Bai, J. and P. Collin-Dufresne (2019). The cds-bond basis. Financial Management 48(2), 417-439. 8

Barndorff-Nielsen, O. E., P. R. Hansen, A. Lunde, and N. Shephard (2009). Realized kernels in practice: trades and quotes. The Econometrics Journal 12(3), C1-C32. 10

Barth, D. and R. J. Kahn (2021). Hedge funds and the treasury cash-futures disconnect. 5
Burghardt, G. and T. Belton (2005). The Treasury Bond Basis: An in-Depth Analysis for Hedgers, Speculators, and Arbitrageurs. McGraw-Hill Library of Investment and Finance. McGraw-Hill Education. 5

Choudhry, M. (2018). Derivative Instruments and Hedging, Chapter 2, pp. 120-270. John Wiley and Sons, Ltd. 8

Driscoll, J. C. and A. C. Kraay (1998, 11). Consistent Covariance Matrix Estimation with Spatially Dependent Panel Data. The Review of Economics and Statistics 80(4), 549-560. 17, 32

Du, W., B. M. Hébert, and W. Li (2022). Intermediary balance sheets and the treasury yield curve. Technical report, National Bureau of Economic Research. 6, 16, 22, 23

Du, W., A. Tepper, and A. Verdelhan (2018). Deviations from covered interest rate parity. The Journal of Finance 73(3), 915-957. 1, 12, 16

Duffie, D. (1999). Credit swap valuation. Financial Analysts Journal 55(1), 73-87. 8
Duffie, D. (2010). Presidential address: Asset price dynamics with slow-moving capital. The Journal of finance 65(4), 1237-1267. 21

Fleckenstein, M. and F. A. Longstaff (2020). Renting balance sheet space: Intermediary balance sheet rental costs and the valuation of derivatives. The Review of Financial Studies 33(11), $5051-5091.5$

Fleckenstein, M., F. A. Longstaff, and H. Lustig (2014). The tips-treasury bond puzzle. the Journal of Finance 69(5), 2151-2197. 7

Hanson, S. G., A. Malkhozov, and G. Venter (2022). Demand-supply imbalance risk and long-term swap spreads. SRC Discussion Paper No 118. 6, 23

Hausman, J. (2001, December). Mismeasured variables in econometric analysis: Problems from the right and problems from the left. Journal of Economic Perspectives 15(4), 57-67. 11

### Page 26
Hazelkorn, T., T. Moskowitz, and K. Vasudevan (2021). Beyond basis basics: Liquidity demand and deviations from the law of one price. The Journal of Finance forthcoming. 3, 4

He, Z., B. Kelly, and A. Manela (2017). Intermediary asset pricing: New evidence from many asset classes. Journal of Financial Economics 126(1), 1-35. 16, 31

Jermann, U. (2020). Negative swap spreads and limited arbitrage. The Review of Financial Studies 33(1), 212-238. 6

Khandani, A. E. and A. W. Lo (2011). What happened to the quants in august 2007? evidence from factors and transactions data. Journal of Financial Markets 14(1), 1-46. 12, 30

Lazarus, E., D. J. Lewis, J. H. Stock, and M. W. Watson (2018). Har inference: Recommendations for practice. Journal of Business \& Economic Statistics 36(4), 541-574. 17

Modigliani, F. and M. H. Miller (1958). The cost of capital, corporation finance and the theory of investment. American Economic Review 1, 3. 15

Newey, W. K. and K. D. West (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation. Econometrica 55(3), 703-708. 17

Rime, D., A. Schrimpf, and O. Syrstad (2017). Segmented money markets and covered interest parity arbitrage. 1
van Binsbergen, J. H., W. F. Diamond, and M. Grotteria (2019). Risk-free interest rates. Technical report, National Bureau of Economic Research. 2, 3, 10

### Page 27
Figure A1: Time-Series of Arbitrage Spreads
(a) CIP
![img-0.jpeg](img-0.jpeg)
(b) Box Spread
![img-1.jpeg](img-1.jpeg)

Notes: Each panel shows the daily-time series of individual arbitrage trades for a given strategy.

### Page 28
(c) Equity-Spot Futures
![img-2.jpeg](img-2.jpeg)
(d) Treasury-Spot Futures
![img-3.jpeg](img-3.jpeg)

### Page 29
(e) Treasury-Swap
![img-4.jpeg](img-4.jpeg)
(f) TIPS-Treasury
![img-5.jpeg](img-5.jpeg)

### Page 30
(g) CDS-Bond Basis (IG)
![img-6.jpeg](img-6.jpeg)

### Page 31
Figure A2: Segmentation Prior to the Dodd-Frank Era
![img-7.jpeg](img-7.jpeg)
(a) Collapse of Bear Stearns Hedge Funds
![img-8.jpeg](img-8.jpeg)
(b) Lehman Bankruptcy and Run on MMFs

Notes: Panel (a) plots the average absolute values of arbitrage spreads for unsecured trades (CIP, Equity spot-futures, and Box) around the period when two of Bear Stearns's hedge funds were unwound. The red dotted line corresponds to June 14, 2007, the day that Merrill Lynch reportedly issued a margin call to the distressed hedge funds (Khandani and Lo, 2011). Panel (b) plots the average spread of secured and unsecured trades (left axis) and the 3-month TED spread (right axis) around the time of the Lehman Brother's bankruptcy and the run on the Reserve Primary Money Market Fund. The red dotted line corresponds to September 15, 2008, the day that Lehman Brothers declared bankruptcy.

### Page 32
Figure A3: Intermediary Balance Sheet Strength Around the 2016 MMF Reform
![img-9.jpeg](img-9.jpeg)

Notes: This figure shows the intermediary capital ratio of He et al. (2017) around the 2016 Money Market Reform. The intermediary capital ratio equals the ratio of market capitalization to market capitalization plus book debt for New York Federal Reserve primary dealers' publicly traded holding companies. The monthly series was taken directly from He et al. (2017). The red vertical dashed line in the plot corresponds to October 2016, the month in which compliance with the 2016 Money Market Reform was required.

### Page 33
Figure A4: Standard Error Robustness and the Analysis of 2016 MMF Reform
![img-10.jpeg](img-10.jpeg)

Notes: This table shows estimates of the effect of the 2016 money market reform on the absolute values of arbitrage spreads. The figure plots the $\beta$ 's from the following regression: $s_{i t}=\alpha_{i}+\alpha_{t}+\sum_{j=-4}^{3} \beta_{j} 1[i \in$ Unsecured $] \times 1[t=$ October2016 + j] $+\beta_{j \geq 4} 1[i \in$ Unsecured $] \times 1[t \geq$ February2017] $+\varepsilon_{i t}$. Arbitrage spreads are expressed in basis points. The blue markers show $95 \%$ confidence bands based on standard errors that are clustered by time and use Driscoll and Kraay (1998) errors within each trade using eight lags. The orange markers show standard error bands that are clustered by time and trade. The estimation sample ends one year after the reform in October 2017.

### Page 34
Figure A5: Value of Equity Securities Held by Dealers vs Equity Repo Market
![img-11.jpeg](img-11.jpeg)

Notes: This figure shows the value of equity securities held by U.S. bank holding companies and the total value of equity collateral in the U.S. equity repo market. The first series is based on Y-9C filings and the second is based on publicly available data from the New York Federal Reserve.

### Page 35
Figure A6: Changes in the Equity Spot-Futures Around Futures Roll Dates
![img-12.jpeg](img-12.jpeg)

Notes: This figure shows coefficients from the following regression:

$$
\Delta s_{i, m}=c+\beta 1[m \in \text { Expiration Month, except June 2012 }]+\theta 1[m=\text { June 2012 }]+\varepsilon_{i, t}
$$

where $\Delta s_{i, t}$ is the change in arbitrage spread $i$ around the third Friday in month $m .1[m \in$ Expiration Month, except June 2012] is an indicator variable if $m$ is a futures expiration month (March, June, September, and December) excluding June of 2012. The indicator $1[m=$ June 2012] equals one if the month is June 2012. Changes within each month are computed between eight days prior to the third Friday in the month and the first business day after the third Friday. Robust standard errors are used to create $95 \%$ confidence bands in the plot.

### Page 36
Figure A7: Arbitrage Returns over Different Horizons
![img-13.jpeg](img-13.jpeg)

Notes: This figure shows average pairwise correlation of arbitrage returns over different horizon. For each of the 32 arbitrage trades in our analysis sample, we compute returns according to Equation (A.14) and assuming a locally flat term structure of arbitrage spreads. We vary the holding period of returns from one day to one quarter. The figures shows the average pairwise correlation of returns across all trades for each horizon. See Section XXX for more details.

### Page 37
Table A1: Correlations Before the Dodd-Frank Era
(a) During Global Financial Crisis

|  |  |  | $\rho_{i j}$ |  |  |  |  | $p$-value |  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| Mean | Sd | Min | p25 | p50 | p75 | Max | N | $\bar{\rho}>0.67$ | $\rho_{i j}=\rho$ |
| 0.66 | 0.24 | -0.04 | 0.56 | 0.72 | 0.83 | 0.99 | 190 | 0.20 | 0.00 |
| $28 \%$ of pairs reject $H_{0}: \rho_{i j}>0.67$ |  |  |  |  |  |  |  |  |  |

(b) Prior to Global Financial Crisis

|  |  |  | $\rho_{i j}$ |  |  |  |  | $p$-value |  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| Mean | Sd | Min | p25 | p50 | p75 | Max | N | $\bar{\rho}>0.67$ | $\rho_{i j}=\rho$ |
| 0.06 | 0.27 | -0.67 | -0.10 | 0.03 | 0.21 | 0.90 | 190 | 0.00 | 0.00 |
| $97 \%$ of pairs reject $H_{0}: \rho_{i j}>0.67$ |  |  |  |  |  |  |  |  |  |

Notes: This table summarizes the distribution of pairwise correlations for arbitrage strategies in different subsamples. In all cases, the columns under $p$-value are, respectively, based on tests of the null that average correlations are above 0.67 and the null that all pairwise correlations are zero. Panel A i is based on the period between June 1, 2007 through June 30, 2009. Panel B is based on the period between January 2, 2004 and June 1, 2007. Treasury spot-futures and Treasury swap arbitrage are not included in either panel due to data limitations.

### Page 38
Table A2: Arbitrage-Implied Riskless Rates and Funding Shocks to Fidelity (First-Stage IV)

|  | Dep Variable: Fidelity Flows |  |  |
| :-- | --: | --: | --: |
|  | (1) | (2) | (3) |
|  | Equity S-F | CIP/Box | Secured |
| Passive Fidelity Flows | $4.55^{* *}$ | $4.44^{* *}$ | $4.32^{* *}$ |
|  | $(2.94)$ | $(3.84)$ | $(5.45)$ |
| $\Delta$ Treasury | 0.01 | 0.00 | $-0.02^{*}$ |
|  | $(0.20)$ | $(0.05)$ | $(-1.89)$ |
| $\Delta$ TED | $-0.19^{* *}$ | $-0.18^{* *}$ | $-0.19^{* *}$ |
|  | $(-2.46)$ | $(-3.13)$ | $(-5.49)$ |
| $R^{2}$ | 0.13 | 0.12 | 0.11 |
| $N$ | 357 | 1,309 | 2,099 |

Notes: This table presents first-stage IV estimates where flows out of Fidelity IPrime money market funds (MMFs) are instrumented using net flows into all Fidelity MMFs interacted with the Fidelity IPrime share of assets, lagged by 3 months. Additional controls in the regression are the maturity-matched Treasury yield and the change in the maturity-matched TED spread. Define $l$ and $m$, respectively, as the maturities of the nearest-maturity LIBOR and Treasury for a given trade. The maturity-matched TED spread for the trade is then defined as $\operatorname{LIBOR}(l)-\operatorname{Treasury}(l)$ and the maturity-matched Treasury yield is defined as $\operatorname{Treasury}(m) . l$ does not equal $m$ for longer-tenor trades (e.g., 30-year Treasury swap) because the maximum maturity LIBOR rate we observe is one year. Column (1) is the first-stage when outcome variable in the IV regression is equity spot-futures implied riskless rate. Columns (2) and (3) show first-stage estimates for when the outcome variable in the IV regressions are implied riskless rates implied by, respectively, other unsecured trades (CIP and Box) and secured trades. All implied riskless rates are in basis points and flows are in percentage points. $t$-statistics are reported under point estimates and are based on standard errors clustered by strategy-month.