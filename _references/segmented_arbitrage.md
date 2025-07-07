### Page 1
Working Paper 24-030

# Segmented Arbitrage 

Emil Siriwardane
Adi Sunderam
Jonathan Wallen

### Page 2
# Segmented Arbitrage 

Emil Siriwardane<br>Harvard Business School

Adi Sunderam
Harvard Business School
Jonathan Wallen
Harvard Business School

## Working Paper 24-030

Copyright (C) 2023 by Emil Siriwardane, Adi Sunderam, and Jonathan Wallen.
Working papers are in draft form. This working paper is distributed for purposes of comment and discussion only. It may not be reproduced without permission of the copyright holder. Copies of working papers are available from the author.

Funding for this research was provided in part by Harvard Business School.

### Page 3
# Segmented Arbitrage* 

Emil Siriwardane ${ }^{\dagger}$ Adi Sunderam ${ }^{\ddagger}$ Jonathan Wallen ${ }^{\S}$

October 2023

We use arbitrage activity in equity, fixed income, and foreign exchange markets to characterize the frictions and constraints facing intermediaries. The average pairwise correlation between the 32 arbitrage spreads that we study is $22 \%$. These low correlations are inconsistent with canonical intermediary asset pricing models. We show that at least two types of segmentation drive arbitrage dynamics. First, funding is segmented-certain trades rely on specific funding sources, making their arbitrage spreads sensitive to localized funding shocks. Second, balance sheets are segmentedintermediaries specialize in certain trades, so arbitrage spreads are sensitive to idiosyncratic balance sheet shocks.

[^0]
[^0]:    *We thank Matteo Benetton, John Campbell, Wenxin Du, Jonathan Goldberg, Sam Hanson, Zhiguo He, Anil Kashyap, Arvind Krishnamurthy, Stavros Panageas, Andrei Shleifer, Erik Stafford, Jeremy Stein, Fabrice Tourre, and seminar participants at Arrowstreet Capital, Boston College Carroll School of Management, Chicago Booth School of Business, Copenhagen Business School, New York Federal Reserve, Michigan Ross, the University of Houston Business School, UT Austin, the 2022 UCLA Conference on Financial Markets, the 2022 GSU-CEAR Finance Conference, the 2022 Napa/Sonoma Finance Conference, the 2022 Advances in Fixed Income and Macro-Finance Research Federal Reserve Bank of San Francisco and Bank of Canada, the 2022 Western Finance Association, and the 2022 Q Group Fall Seminar for helpful comments.
    ${ }^{\dagger}$ Siriwardane: Harvard Business School and NBER. E-mail: esiriwardane@hbs.edu
    ${ }^{\ddagger}$ Sunderam: Harvard Business School and NBER. E-mail: asunderam@hbs.edu
    §Wallen: Harvard Business School E-mail: jwallen@hbs.edu

### Page 4
# 1 Introduction 

There is growing recognition that financial intermediaries play a key role in determining asset prices. Much of the research on intermediaries treats them as a monolith, assuming that all financial institutions face the same, typically limited, set of constraints, fund homogeneously from the household sector, and perfectly share risk with each other. This view of intermediaries has several implications. It suggests that all risk premia should strongly comove with aggregate intermediary balance sheet strength, and conversely that all risk premia should be equally informative about the health of the intermediary sector. In addition, if intermediaries are strongly integrated, fire sales in any market have economy-wide effects on credit creation because intermediaries will reduce lending and instead provide that market with liquidity.

In this paper, we argue that the assumption of a representative intermediary, while helpful for many applications, understates the importance of frictions within the intermediary sector and their implications for prices. We provide empirical evidence that segmentation within the intermediary sector has a first-order impact on asset prices. We focus our analysis on arbitrage spreads—riskless returns in excess of riskless rates-that arise from violations of the law of one price in equity, fixed income, and foreign exchange markets. We take this approach for two reasons. First, arbitrage is intermediated by financial institutions such as broker-dealers and hedge funds and cannot be easily performed by households (Haddad and Muir, 2021). Second, arbitrage spreads are accurate measures of expected returns, the key objects in any asset pricing theory. Thus, arbitrages offer a high-power setting for understanding the frictions faced by intermediaries. In contrast, studies analyzing risky assets must work with average realized returns, a noisy proxy for expected returns (Merton, 1980).

To fix ideas, we begin with a stylized model in which intermediaries determine arbitrage spreads. In the model, a continuum of intermediaries participates in a set of fundamentally riskless arbitrage trades. Intermediaries potentially face two types of frictions that break the Modigliani and Miller (1958) theorem. First, they may face balance sheet constraints like regulatory capital requirements, which are costly to satisfy due to external financing frictions. Second, intermediaries

### Page 5
may face frictions that prevent them from raising financing to fund riskless assets at the riskless rate. Intermediaries may fund from different sources with different costs, and certain trades may require them to fund from a specific source. We model these frictions in reduced form to focus on their implications for arbitrage spreads.

In the model and throughout the paper, we distinguish between three assumptions typically embedded in theoretical and applied work using a representative intermediary. First, balance sheet integration means that the marginal balance sheet cost of holding a given riskless asset is equalized across intermediaries. Second, funding integration means intermediaries can fund all riskless assets from the same source. Third, the set of constraints intermediaries face is limited. These assumptions result in one- or two- factor structures for arbitrage spreads. ${ }^{1}$ For instance, if the representative intermediary faces a single constraint (e.g., a leverage constraint) and funding is frictionless, then all arbitrage spreads are determined by the shadow cost of the constraint. Thus, spreads are perfectly correlated and follow a single-factor structure.

We then use the model to illustrate how segmentation can reduce correlations between arbitrage spreads. Funding segmentation—violations of funding integration—can reduce correlations between trades that use different funding sources. Similarly, balance sheet segmentation—violations of balance sheet integration—implies that trades performed by the same arbitrageurs will be more correlated with each other than trades performed by different arbitrageurs.

We next turn to the data, focusing on the decade following the 2007-2009 financial crisis. We study 32 arbitrage trades that fall into seven broad strategies: (i) equity spot-futures arbitrage, (ii) equity options arbitrage, which enforces put-call parity, (iii) currency spot-futures arbitrage, which enforces covered interest parity (CIP), (iv) CDS-bond arbitrage, (v) Treasury spot-futures arbitrage, (vi) Treasury-interest rate swaps arbitrage, and (vii) Treasury-inflation swaps arbitrage. For each arbitrage trade, we define the spread as the difference between the riskless rate implied by no-arbitrage conditions (e.g., spot-futures parity) and a relevant benchmark rate.

Our first result is that the daily correlation of spreads is low on average. The average pairwise

[^0]
[^0]:    ${ }^{1}$ See, e.g., He et al. (2017); He and Krishnamurthy (2013); Adrian et al. (2014); Ivashina et al. (2015); Gromb and Vayanos (2018); Andersen et al. (2019).

### Page 6
correlation is 0.22 , and the 75 th percentile of pairwise correlations is 0.42 . While these low correlations could be driven by measurement error, this measurement error would have to be large to explain our results since observed correlations are far from one. Furthermore, we observe a similar factor structure if we smooth the data. For instance, after taking monthly moving averages, 10 principal components are required to explain $90 \%$ of the variation in arbitrage spreads. Correlations are also low among the subsample of arbitrage trades with short tenors (3-6 month horizons), suggesting that convergence or noise trader risk (Delong et al., 1993) is not the source of the high-dimensional factor structure. The data are therefore far from the one- or two-factor structure predicted by models in which balance sheet and funding integration hold in an intermediary sector facing few constraints.

Departures from the integrated intermediary benchmark imply that the correlations of arbitrage spreads are determined by both arbitrageur supply and end-user demand. One might therefore wonder whether the low correlations we document arise primarily from the supply side or the demand side. We use the sign-restricted structural VAR methodology of Uhlig (2005) to uncover separate supply and demand shocks for the subset of trades for which we have quantity data. Correlations of supply shocks across trades are low, consistent with the idea that intermediaries performing these arbitrages face significant frictions.

We then show that funding segmentation is one reason that correlations between arbitrage spreads are low. Our analysis starts from the observation that equity spot-futures, equity options, and CIP arbitrage face relatively higher margin requirements than other strategies. Because these high-margin strategies require more unsecured funding, we refer to them as "unsecured" arbitrages, while we call the remaining ones "secured" arbitrages. ${ }^{2}$ Unsecured arbitrages are more correlated with each other than they are with secured arbitrages. We provide evidence that this higher correlation reflects the higher exposure of unsecured arbitrages to conditions in unsecured funding markets, which we proxy for with the Treasury-Eurodollar (TED) spread. We find that unsecured arbitrage spreads are nearly seven times more sensitive to movements in the TED spread than are

[^0]
[^0]:    ${ }^{2}$ Secured arbitrages include Treasury spot-futures, Treasury-swap, TIPS-Treasury, and CDS-bond.

### Page 7
secured arbitrage spreads.
While the higher loading of unsecured arbitrage spreads on the TED spread is consistent with funding segmentation, it could also be driven by balance sheet segmentation. For example, if broker-dealers specialize in unsecured arbitrages, then a deterioration of their balance sheets could cause both the TED spread and unsecured arbitrage spreads to rise. To isolate the role of funding segmentation, it is therefore useful to trace out how shocks to the supply of unsecured funding differentially impact unsecured versus secured arbitrages. Following Anderson et al. (2019), we conduct an event study around the 2016 money market fund (MMF) reform, which resulted in a sharp contraction in unsecured lending by MMFs. During the reform, the TED spread and unsecured arbitrage spreads rise, while secured arbitrage spreads do not, demonstrating that segmentation in funding markets is an important driver of arbitrage spreads.

We then provide evidence that funding markets are more segmented than the simple divide between secured and unsecured trades because funding providers specialize (Chernenko and Sunderam, 2014; Li, 2021). Thus, shocks to individual funding sources move specific arbitrage spreads without moving others. We illustrate this idea by studying supply shocks to Fidelity MMFs, which Hu et al. (2021) show are especially active in funding holders of equity securities. These shocks move equity spot-futures arbitrage spreads, but not others.

We next show that balance sheet segmentation also contributes to the low overall correlation of arbitrage spreads. In other words, it is not the case that intermediary balance sheets are integrated and a representative intermediary facing segmented funding is marginal in all strategies. We first provide event study evidence that the balance sheet constraints of certain intermediaries affect some trades more than others. We study the "London Whale" episode, in which JP Morgan lost over \$6 billion through its credit derivatives hedging program in 2012. This event is useful for our purposes because it did not materially affect the firm's funding rates but did result in a tightening of the firm's risk limits (U.S. Senate, 2014). We show that the episode led equity spot-futures arbitrage spreads to rise relative to others.

Balance sheet segmentation is also evidenced by the fact that secured arbitrage spreads tend to

### Page 8
rise following losses at hedge funds that specialize in fixed income arbitrage, yet unsecured arbitrage spreads do not. These joint patterns suggest that hedge fund balance sheets are thus particularly important for secured arbitrages. Moreover, specific hedge funds appear to matter for specific trades. For example, the hedge funds with balance sheets important for CDS-Bond arbitrage are not the ones that are important for TIPS-Treasury arbitrage. Overall, our evidence suggests that arbitrage activity is segmented due to fragmented funding sources (e.g., unsecured vs secured) and specialization across financial institutions (e.g., dealers vs hedge funds).

Our paper belongs to the rapidly expanding literature on financial intermediaries and their role in capital markets. The theoretical literature in this area, including Shleifer and Vishny (1997), Gromb and Vayanos (2002), Brunnermeier and Pedersen (2009), Garleanu and Pedersen (2011), Adrian and Boyarchenko (2012), He and Krishnamurthy (2013), and Brunnermeier and Sannikov (2014), generally assumes a representative intermediary and theoretically studies how different constraints on its activity impact equilibrium asset prices or arbitrage spreads. Our results suggest that these theories most naturally describe market segments, rather than providing a uniform account of dynamics across all capital markets. ${ }^{3}$

The empirical literature can be divided into three categories. One strand studies law of one price violations in specific markets, including equity (van Binsbergen et al., 2019; Hazelkorn et al., 2021), foreign exchange (Du et al., 2018), Treasury (Fleckenstein et al., 2014; Jermann, 2020; Barth and Kahn, 2021), and corporate bond markets (Bai and Collin-Dufresne, 2019). Our paper departs from this research by simultaneously analyzing law of one price violations across many different markets, which enables us to characterize the frictions and constraints faced by different intermediaries sector. ${ }^{4}$ A second strand, including Pasquariello (2014), Adrian et al. (2014), He et al. (2017), and Du et al. (2019), aims to empirically link sector-level measures of intermediary constraints to risky asset prices. ${ }^{5}$ Our results suggest that accounting for which intermediaries are

[^0]
[^0]:    ${ }^{3} \mathrm{~A}$ recent theoretical literature has emphasized the importance of intermediary heterogeneity for macroeconomic outcomes and optimal macroprudential policy (Begenau and Landvoigt, 2021; Jamilov, 2021).
    ${ }^{4}$ There is also work documenting segmentation in short-term money markets (Bech and Klee, 2011; Duffie and Krishnamurthy, 2016). Our paper shows how that segmentation ultimately impacts risky asset prices.
    ${ }^{5}$ Adrian et al. (2014) and He et al. (2017) fail to reject the null of integration based on a test of whether the prices of risk for intermediary factors differ across markets. However, their tests use realized average returns to proxy for ex-ante

### Page 9
active in a market and how they fund themselves is likely to improve the performance of these kinds of intermediary-based asset pricing models. This conclusion accords with Siriwardane (2018), who shows how specialization by financial intermediaries affects the pricing of credit derivatives.

A third strand of the empirical literature, including Boyarchenko et al. (2016), Boyarchenko et al. (2020), and Liu (2020), studies large panels of arbitrage spreads like we do. These papers emphasize moments of the data that are consistent with the integrated intermediary model. For instance, Boyarchenko et al. (2016) and Boyarchenko et al. (2020) assume globally systemically important banks are all active in a wide range of arbitrages and study how spreads respond to the introduction of the supplementary leverage ratio requirement under this assumption. Similarly, Liu (2020) emphasizes the common variation in spreads by studying their first principal component and correlating it with the TED spread and hedge fund returns. In contrast, our analysis starts from moments that are inconsistent with the integrated intermediary model, the pairwise correlation matrix of arbitrage spreads. This difference in empirical focus leads us to conceptually different economic conclusions from the existing literature. We start from moments that suggest segmentation and then characterize the nature of that segmentation, emphasizing frictions in funding markets and the segmentation of balance sheets (i.e., arbitrageur equity capital) as two distinct drivers of low correlations between arbitrage spreads.

# 2 Motivating Model 

To fix ideas, we begin with a stylized model in which intermediaries face multiple frictions and determine arbitrage spreads. The model highlights how balance sheet constraints, balance sheet segmentation, and funding segmentation all impact arbitrage spreads. The key point is that the three assumptions typical of the intermediary asset pricing literature-(i) a small number of constraints, (ii) balance sheet and (iii) funding integration-result in highly correlated arbitrage spreads. Violating any of the three assumptions can result in the high-dimensional factor structure for arbitrage spreads risk premia, which lowers their power. Accordingly, Bryzgalova (2015) finds that the quarterly intermediary capital factor is weak in the sense that it has a small covariance with asset returns.

### Page 10
that we document below. Balance sheet and funding segmentation further predict that some spreads move with proxies for balance sheet and funding costs, but others do not.

# 2.1 Setup 

Formally, suppose there are $N$ arbitrage trades that are riskless. Normalize the riskless rate to zero and let $s_{n, t}$ denote the arbitrage spread on trade $n$ at time $t$. For simplicity, we assume arbitrageurs are always net long, so that all spreads in the model are positive. In the empirics, we will work with the absolute value of spreads since arbitrageurs can be net long or net short each trade.

A unit measure of competitive and atomistic arbitrageurs (i.e., intermediaries) engages in these trades, supplying $q_{n, t}$ of trade $n .{ }^{6}$ Arbitrageurs face two main frictions, both of which are modeled in reduced form. First, there are $K$ balance sheet requirements of the form $\sum_{n} q_{n, t} v_{n, k}=V_{k, t}$. These requirements capture equity capital and liquidity constraints, which may be set by regulators or by arbitrageurs themselves for internal risk-management purposes. We assume that the contribution of trade $n$ to constraint $k, v_{n, k}$, is fixed over time. Arbitrageurs can adjust their balance sheets to meet requirement $k$ at total cost $\frac{1}{2} c_{k, t} V_{k, t}^{2}$, which capture costs of external finance or other adjustment costs. For instance, a high value of $c_{k, t}$ could capture that the signaling problem associated with equity issuance is more severe. The existence of balance sheet requirements does not imply balance sheet segmentation. Even with multiple balance sheet requirements, all arbitrageurs can face the same marginal balance sheet cost for a given trade, which means that we can model a single, representative intermediary for all trades. We introduce balance sheet segmentation below.

Second, there are funding frictions. There are $L$ funding sources with associated cost $f_{1, t}, \ldots, f_{L, t}$ (in excess of the riskless rate of zero) per unit borrowed. One dollar of trade $n$ can be financed with $w_{n, l}$ dollars from funding source $l \in L$. This assumption captures violations of the Modigliani and Miller (1958) theorem in funding markets. Despite the fact that all $N$ trades are riskless, arbitrageurs may not be able to fund the basket of securities and derivatives that underlie each trade at the riskless

[^0]
[^0]:    ${ }^{6}$ As discussed in Wallen (2019), market power among intermediaries may be important in certain markets. The results here would be qualitatively unchanged in oligopolistic market structures if the elasticity of demand from outside investors is constant over time.

### Page 11
rate (Duarte et al., 2006). For instance, Treasury and equity repo rates differ even when both sources of funding are used in a fundamentally riskless futures-basis arbitrage. The assumption that $w_{n, l}$ does not vary over time corresponds to the empirical notion that rates on funding fluctuate more than haircuts (Copeland et al., 2010). If $L=0$, then funding is frictionless. If $L=1$, then funding is frictional but integrated, and if $L>1$ (and $w_{n, l}$ varies across trades and financing sources), then funding is segmented.

The arbitrageur's problem is:

$$
\max \sum_{n=1}^{N}\left(q_{n, t}\left(s_{n, t}-\sum_{l} w_{n, l} f_{l, t}\right)\right)-\frac{1}{2} \sum_{k=1}^{K} c_{k, t} V_{k, t}^{2}
$$

Since arbitrageurs are atomistic, they take $s_{n, t}$ as given. To close the model, we assume that outside demand for trade $n$ is inelastic and given by $a_{n, t}>0$. Market clearing then requires that $q_{n, t}=a_{n, t} .{ }^{7}$

# 2.2 Canonical Intermediary Asset Pricing Models 

Though it is stylized, the model allows us to nest common assumptions in the intermediary asset pricing literature. We discuss two typical structures here, both of which feature balance sheet and funding integration.

Balance sheet and funding integration with a single balance sheet constraint. Many models of intermediaries consider a single balance sheet constraint and frictionless funding (e.g., He and Krishnamurthy (2013)). This case can be captured by setting $f_{l, t}=0$ for all $l, c_{1, t} \neq 0$, and $c_{k, t}=0$ for all $k>1 .{ }^{8}$ The solution to Eq. (1) is then given by

$$
s_{n, t}=v_{n, 1} c_{1, t} V_{1, t}=v_{n, 1} c_{1, t}\left(\sum_{n} a_{n, t} v_{n, 1}\right)
$$

From this expression, it is clear that spreads will be perfectly correlated. There is a single factor-the

[^0]
[^0]:    ${ }^{7}$ We make the assumption that outside demand is completely inelastic for simplicity. Our key results would not qualitatively change if outside demand were elastic (e.g., given by $a_{n, t}-b_{n} s_{n, t}$ ).
    ${ }^{8}$ This is equivalent to setting $w_{n, l}=0$ for all $n, l$ and $v_{n, k}=0$ for all $k>1$, which can be interpreted as the ability to fully fund trades at the riskless rate with trades loading on a single balance sheet requirement $(k=1)$.

### Page 12
marginal cost of the balance sheet constraint, $c_{1, t} V_{1, t}$-that moves all trades proportionally. Trades that face a higher balance sheet requirement $v_{n, 1}$ load more heavily on this factor, but all spreads move linearly with the marginal cost of the constraint. This one-factor structure in spreads holds despite the fact that there are a large number of primitive shocks in the model. In particular, the balance sheet shocks $c_{1, t}$ and the outside demand shocks $a_{n, t}$ for each trade $n$ fluctuate independently, yet a one-factor structure still obtains. The intuition is that these independent shocks all move the marginal cost of balance sheet, which is ultimately all that matters for spreads.

Balance sheet and funding integration with a single funding factor. Another simple structure featuring both balance sheet and funding integration involves no constraints and a single frictional funding factor: $c_{k, t}=0, v_{n, k}=0, f_{n, 1}>0$, and $f_{n, l}=0$ for $l>1$. Then we simply have spreads driven by the funding factor: $s_{n, t}=w_{n, 1} f_{1, t}$. In this case, we again have perfect correlations across spreads. Spreads may load differentially on the funding factor, but they all move linearly with it. ${ }^{9}$

# 2.3 Integration with Many Constraints 

While much of the intermediary asset pricing literature features perfectly correlated arbitrage spreads, balance sheet and funding integration need not imply them. In particular, balance sheet and funding integration admit a single frictional funding source $(L=1)$ and arbitrarily many balance sheet constraints $(K>0)$. In this case, all riskless arbitrages are funded from the same source and marginal balance sheet costs are equated across arbitrageurs for each trade $n$. Spreads are given by:

$$
s_{n, t}=w_{n, 1} f_{1, t}+\sum_{k=1}^{K} v_{n, k} c_{k, t} V_{k, t}
$$

and feature a $K+1$ factor structure. Thus, a high-dimensional factor structure for arbitrage spreads rules out balance sheet and funding integration with a small number of constraints.

[^0]
[^0]:    ${ }^{9}$ Andersen et al. (2019) has this reduced form, though formally they obtain the result by microfounding the costs of external equity with a debt overhang problem. With this microfoundation, the marginal cost of external equity funding for a riskless asset, $w_{n, \text { equity }} f_{\text {equity,t }}$, is equal to the arbitrageur's credit spread.

### Page 13
# 2.4 Segmentation 

We next consider the impact of segmentation on spreads. We consider two types of segmentation: funding segmentation and balance sheet segmentation.

Segmented funding. By funding segmentation, we mean that certain trades can use certain funding sources while other trades cannot. For instance, Treasury repo financing can be used for Treasury spot-futures arbitrage but cannot be used for equity spot-futures arbitrage. To see the implications of this kind of segmentation, suppose that trades $n=1, \ldots, N_{1}<N$ can be funded only using source $l=1$ with corresponding cost $f_{1, t}$, while trades $n=N_{1}+1, \ldots, N$ can be funded only using source $l=2$ with corresponding cost $f_{2, t}$. If there are no further frictions, we have

$$
s_{n, t}=\left\{\begin{array}{l}
w_{n, 1} f_{1, t} \text { if } n \leq N_{1} \\
w_{n, 2} f_{2, t} \text { if } N_{1}<n
\end{array}\right.
$$

In this case, spreads have a two-factor structure. All trades that can be funded using source 1 are perfectly correlated, as are all trades that can be funded using source 2, but the correlation between the two groups is the correlation between $f_{1, t}$ and $f_{2, t}$ :

$$
\rho\left(s_{n_{1}, t}, s_{n_{2}, t}\right)=\left\{\begin{array}{c}
1 \text { if } n_{1}, n_{2} \leq N_{1} \text { or } N_{1}<n_{1}, n_{2} \\
\rho\left(f_{1, t}, f_{2, t}\right) \text { if } n_{1} \leq N_{1}, n_{2}>N_{1}
\end{array}\right.
$$

Extending the argument to more than two funding sources, segmented funding can create a highdimensional factor structure for arbitrage spreads. In this case, the outside demand shocks $a_{n, t}$ still do not impact the correlation of spreads because balance sheets are integrated and funding is elastically supplied.

Segmented balance sheets. Finally, we consider balance sheet segmentation with frictionless funding. We use balance sheet segmentation to describe environments in which certain trades are done by one set of intermediaries and are therefore subject to their balance sheet constraints, while other trades are done by another set of intermediaries and are subject to their balance sheet constraints. One could microfound this segmentation with a small amount of specialization

### Page 14
in different trades. For instance, suppose there are small marginal costs $\varepsilon_{n, i}$ associated with arbitrageur $i$ doing trade $n$ and there are two types of arbitrageurs. Arbitrageurs $i \in I$ have a marginal cost advantage $\varepsilon_{n, i}<\varepsilon_{n, j}$ for trades $n=1, \ldots, N_{1}$ over all other arbitrageurs $j \in \sim I$. Conversely, arbitrageurs $j \in \sim I$ have a marginal cost advantage $\varepsilon_{n, j}<\varepsilon_{n, i}$ for trades $n=N_{1}+1, \ldots, N$. In other words, one group of arbitrageurs has a cost advantage in one set of trades, while the other has a cost advantage in a different set of trades. There is a representative arbitrageur for each group.

Finally, suppose there is a single balance sheet constraint ( $f_{l, t}=0$ for all $l, c_{1, t} \neq 0$, and $c_{k, t}=0$ ). Further allow arbitrageurs $i \in I$ to face a different frictional cost of meeting the single balance sheet constraint, $\frac{1}{2} c_{1, t}^{I}\left(V_{1, t}^{I}\right)^{2}$, than arbitrageurs $j \notin I, \frac{1}{2} c_{1, t}^{\sim I}\left(V_{1, t}^{\sim I}\right)^{2}$. If the outside demand for each group of trades is similar, then by market clearing arbitrageurs $i \in I$ will absorb all demand for trades $n=1, \ldots, N_{1}$ and arbitrageurs $j \in \sim I$ will absorb all demand for trades $n=N_{1}+1, \ldots, N .{ }^{10}$ In other words, we have $V_{1, t}^{I}=\sum_{n=1}^{N_{1}} a_{n, t} v_{n, 1}$ and $V_{1, t}^{\sim I}=\sum_{n=N_{1}}^{N} a_{n, t} v_{n, 1}$, where $a_{n, t}$ is the outside demand for trade $n$.

In this case, then spreads are given by

$$
s_{n, t}=\left\{\begin{array}{l}
\varepsilon_{n, i}+v_{n, 1} c_{1, t}^{I} V_{1, t,}^{I} \text { if } n \leq N_{1} \\
\varepsilon_{n, j}+v_{n, 1} c_{1, t}^{\sim I} V_{1, t}^{\sim I} \text { if } N_{1}<n
\end{array}\right.
$$

In other words, spreads have a two-factor structure. Intuitively, spreads for the first group of trades $\left(n=1, \ldots, N_{1}\right)$ reflect the shadow cost of the balance sheet constraint for arbitrageurs in group $I$. For the second group of trades $\left(n=N_{1}+1, \ldots, N\right)$, spreads will reflect the shadow cost of the balance sheet constraint for arbitrageurs outside group $I$.

To get closed form expressions for the correlation structure in this case, assume that balance sheet costs $c_{1, t}^{I}$ and $c_{1, t}^{\sim I}$, as well as all outside demand shocks are jointly normally distributed with mean zero. For simplicity, also assume that there is a single trade in each group: group $I$ intermediates trade 1 and group $\sim I$ intermediates trade 2. Then we can use the results in Bohrnstedt

[^0]
[^0]:    ${ }^{10}$ Formally, we need an assumption ensuring that marginal cost advantages ( $\varepsilon$ 's) are not swamped by differences in adjustment costs ( $c$ 's) or outside demand (through the $V$ 's).

### Page 15
and Goldberger (1969) to compute the correlations of spreads

$$
\rho\left(s_{1, t}, s_{2, t}\right)=\rho\left(c_{1, t}^{I}, c_{1, t}^{\sim I}\right) \rho\left(a_{1, t}, a_{2, t}\right)+\rho\left(c_{1, t}^{I}, a_{2, t}\right) \rho\left(c_{1, t}^{\sim I}, a_{1, t}\right)
$$

In other words, the correlation between two spreads intermediated by different groups of arbitrageurs depends on: (i) the correlation of balance sheet shocks $\rho\left(c_{1, t}^{I}, c_{1, t}^{\sim I}\right)$, (ii) the correlation of demand shocks $\rho\left(a_{1, t}, a_{2, t}\right)$, and (ii) cross terms, i.e., the correlation of balance sheet shocks for one group of arbitrageurs with the demand shocks facing another group of arbitrageurs: $\rho\left(c_{1, t}^{I}, a_{2, t}\right)$ and $\rho\left(c_{1, t}^{\sim I}, a_{1, t}\right)$. This intuition extends to the case where each group of arbitrageurs intermediates many trades. In that case, the correlation of spreads intermediated by the same group of arbitrageurs is 1, while the correlation of spreads intermediated by different groups is determined by correlations of supply, demand, and cross terms.

This setup can also be used to explore the implications of slow-moving capital for the correlation of spreads. Suppose without loss of generality that the marginal cost of balance sheet is higher for arbitrageurs in group $I: c_{1, t}^{I} V_{1 t}^{I}>c_{1, t}^{\sim I} V_{1 t}^{\sim I}$. Further suppose that between times $t$ and $t+\Delta t$, flows equilibrate the marginal costs of capital between the two groups. For instance, suppose that the marginal cost advantages $\varepsilon_{n, i}$ between the two groups vanish between $t$ and $t+\Delta t$. Then arbitrageurs in group $I$ could sell some of their positions to other arbitrageurs, and we will have $c_{1, t+\Delta t}^{I} V_{1 t+\Delta t}^{I}=c_{1, t+\Delta t}^{\sim I} V_{1 t+\Delta t}^{\sim I}$. In other words, with such capital flows, we get back to the integrated intermediary model and spreads are again perfectly correlated. Extending the argument, if capital flows so that differences in marginal costs of balance sheet for group $I$ and $\sim I$ shrink but are not fully equated, the correlation of spreads will rise but not all the way to 1 . We further explore arbitrage dynamics within the model in Internet Appendix Section A.3.

# 2.5 Empirical Implications 

The model highlights what we can learn from spreads alone and what conclusions require ancillary data. For instance, a high-dimensional factor structure for spreads rejects simple models in which

### Page 16
both balance sheet and funding integration obtain and the representative intermediary is subject to a single constraint. As Eq. (3) shows, however, a high-dimensional factor structure by itself does not distinguish between situations in which (i) both balance sheet and funding integration obtain, but the representative intermediary is subject to many constraints and (ii) either balance sheets or funding markets are segmented. As Eq. (4) shows, the empirical signature of funding segmentation is a covariance between certain spreads and certain funding rates. Similarly, Eq. (6) shows that the empirical signature of balance sheet segmentation is a covariance between certain spreads and individual intermediary balance sheet costs. Our empirics below follow this outline. We begin by describing the factor structure of arbitrage spreads and then provide direct evidence of both types of segmentation. For instance, we will directly show that certain spreads comove with the costs of particular types of funding. And we will show that certain spreads directly respond to shocks to the balance sheets of specific intermediaries.

Finally, while we have discussed funding and balance sheet segmentation separately, it is worth noting that they are not mutually exclusive. We think of segmented funding and segmented balance sheets simultaneously driving individual arbitrage spreads. For instance, we will show below that equity spot-futures spreads depend both on the TED spread, which captures conditions in the market for unsecured funding, and JP Morgan's balance sheet constraints. In other words, JP Morgan is acting as an arbitrageur in these trades, so that its balance sheet conditions impact them, and raising financing from the frictional unsecured funding market to finance them. Moreover, the dealer banks sometimes finance arbitrage and sometimes participate directly as arbitragers, depending on the type of trade. Our results below broadly suggest that they likely participate as arbitrageurs for unsecured arbitrages. In contrast, for secured arbitrages, dealers likely finance arbitrage trading through their role in the repo market (and as prime brokers).

### Page 17
# 3 The Factor Structure of Arbitrage 

### 3.1 Data

Our main analysis sample covers 32 arbitrage trades over the period from January 1, 2010 to February 29, 2020. This period spans the post-financial crisis era and predates the Covid-19 pandemic. For each arbitrage trade, we construct an implied riskless rate based on observed asset prices and then subtract a maturity-matched benchmark riskless rate. For arbitrage trades that mature in less than two years, the benchmark is based on overnight indexed swap (OIS) rates; for longer-maturity trades, it is based on Treasury yields. Our choice of benchmark rates means that our arbitrage spreads do not represent true riskless profits that are available to unconstrained intermediaries, since they are not constructed using the exact funding rate that a trader implementing the arbitrage would face. Instead, our arbitrage spreads capture funding and other frictions faced by arbitragers, which are precisely what we seek to characterize. A detailed description of each arbitrage spread and its construction is contained in Internet Appendix A.1. Here, we provide a short description of the trades, which can be grouped into 7 broad categories or "strategies". The code for constructing arbitrage spreads is housed in a publicly available Github repository. ${ }^{11}$

### 3.1.1 Arbitrage Spreads

Foreign Exchange Arbitrage We follow Du et al. (2018) and measure arbitrage spreads in foreign exchange markets with deviations from covered interest parity (CIP). For each currency we study, we define the CIP arbitrage spread as the difference between the dollar OIS rate and a synthetic riskless rate that is implied by currency forwards, currency spot rates, and foreign OIS rates. We build CIP arbitrage spreads for all G-10 currencies except the Danish and Norwegian krones because OIS rates are not available for these two currencies. We use 3-month CIP violations to avoid any confounding effects that the quarter-end spikes documented in Du et al. (2018) may have on correlations. We obtain data on spot and forward exchange rates and OIS rates from

[^0]
[^0]:    ${ }^{11}$ https://github.com/esiriwardane/arbitrage-spreads-public.

### Page 18
Bloomberg. See Internet Appendix A.1.1 for more details.

Equity Options Arbitrage (Box Arbitrage) We infer riskless rates and arbitrage spreads from S\&P 500 (SPX) equity options based on the put-call parity relationship. As discussed in Ronn and Ronn (1989) and van Binsbergen et al. (2019), implied riskless rates from put-call parity are often called box rates in practice. We adopt this naming convention and refer to this arbitrage as the box trade for the remainder of the paper. We take box rates for six, twelve, and eighteen month tenors directly from van Binsbergen et al. (2019), who estimate them using minute-by-minute pricing data for SPX options through 2018. We then follow van Binsbergen et al. (2019)'s methodology to extend the data to 2020 using SPX option data purchased directly from the CBOE. Arbitrage spreads are then computed by subtracting off a maturity-matched OIS rate.

Equity Spot-Futures Arbitrage For equity futures markets, we measure arbitrage spreads based on violations of spot-futures parity. As we discuss in Internet Appendix A.1.3, the spot and futures markets for equities close at different times, which prevents us from using the spot-futures parity relationship to accurately compute implied riskless rates from closing prices alone. ${ }^{12}$ Instead, we compute implied forward rates based on the relative pricing of futures contracts with different tenors. To illustrate, consider a futures contract on an asset that does not pay a dividend. In this case, spot-futures parity implies that the current futures price $F_{T_{1}}$ for a contract with tenor $T_{1}$ and the spot price $S$ satisfy $F_{T_{1}}=S\left(1+r_{T_{1}}\right)$, where $r_{T_{1}}$ is the riskless rate between today and $T_{1}$. Next, consider another futures contract with tenor $T_{2}>T_{1}$. Under the parity condition, the ratio of the two futures prices $F_{T_{2}} / F_{T_{1}}$ equals the gross forward rate $1+f_{T_{1}, T_{2}}$ between $T_{1}$ and $T_{2}$.

We estimate implied forward rates using Bloomberg futures data on the S\&P 500, Dow Jones Industrial, and Nasdaq 100 indices. For each index, our analysis is based on the nearby and firstdeferred contracts, which are the most liquid. Internet Appendix A.1.3 provides more details about our implementation, including how we account for dividends and compute arbitrage spreads from implied forward rates.

[^0]
[^0]:    ${ }^{12}$ Hazelkorn et al. (2021) avoid this issue by using high-frequency data for both futures and spot markets.

### Page 19
Treasury Spot-Futures Arbitrage For Treasury futures markets, we measure arbitrage spreads based on violations of spot-futures parity, following Fleckenstein and Longstaff (2020) and Barth and Kahn (2021). We study five such trades, associated with the first-deferred futures contract on the 2-year, 5-year, 10-year, 20-year, and 30-year Treasury. We measure arbitrage spreads using the first-deferred contract to avoid complications with the nearby contract in the futures delivery month (Fleckenstein and Longstaff, 2020). We obtain futures-implied riskless rates directly from Bloomberg and define arbitrage spreads by subtracting off a maturity-matched OIS rate. See Internet Appendix A.1.4 for more details.

Treasury Swap Arbitrage For interest rate swap markets, we measure arbitrage spreads using OIS swap spreads, defined as the difference between the fixed rate on overnight indexed swaps and Treasury yields. We study seven such trades, associated with 1-year, 2-year, 3-year, 5-year, 10-year, 20-year, and 30-year Treasuries. OIS swap rates are from Bloomberg. As discussed in Jermann (2020), Du et al. (2022), and Hanson et al. (2022b), only negative OIS swap spreads indicate a guaranteed arbitrage. We show in Internet Appendix A.1.5 that this condition is satisfied for the large majority of observations in our analysis sample.

TIPS-Treasury Arbitrage We build on Fleckenstein et al. (2014) and construct the difference in yield between a synthetic nominal Treasury, constructed using Treasury Inflation Protected Securities (TIPS) and inflation swaps, and the true nominal Treasury yield. Unlike Fleckenstein et al. (2014), who construct the arbitrage at the security level, we use the zero-coupon constant-maturity TIPS and Treasury yields that are published by the Federal Reserve based on Gürkaynak et al. (2007) and Gürkaynak et al. (2010). ${ }^{13}$ Constant-maturity inflation swap data is taken from Bloomberg. In Internet Appendix A.1.6, we provide additional details and compare our series to the one constructed in Fleckenstein et al. (2014). We focus on 2, 5, 10, and 20 year maturities to ensure the underlying TIPS securities used to construct the arbitrages are sufficiently liquid.

[^0]
[^0]:    ${ }^{13}$ The yield curve models can be found here.

### Page 20
CDS-Bond Arbitrage For U.S. corporate bond and credit default swap (CDS) markets, we follow Duffie (1999) and measure arbitrage spreads based on the difference between cash-bond implied credit spreads and CDS spreads. Cash bond and CDS pricing data both come from Markit. We form CDS-bond bases for both investment-grade and high-yield bonds, aggregating over bonds in each ratings category. The average number of bonds used to compute the daily investment grade and high-yield bases is 1,690 and 307, respectively. Internet Appendix A.1.7 contains the full construction methodology.

Summary Statistics Table 1 provides summary statistics. The data is daily and spreads are reported in annualized basis points (bps). Unless otherwise noted, we work with absolute values of spreads since the sign of the spread depends on whether arbitrageurs are net long or short a particular leg of the trade. The number of observations varies slightly across trades, mainly due to availability from raw data providers (e.g., Bloomberg versus Markit) and differences in trading holidays across swaps and futures markets.

Table 1 shows that there is significant variation in spreads, both across trades on average and within trades over time. For many individual trades, the daily standard deviation of spreads is around half the mean spread. Figure 1 helps visualize this variation by plotting average spreads by broad strategy, both at the daily and monthly frequencies. Figure 2 plots average spreads across trades. Table 1 also indicates that spreads are highly persistent at the daily level, a fact that we are careful to account for when conducting statistical inference.

# 3.1.2 Quantity Data 

In addition to data on arbitrage spreads, we use data from the Commodity Futures Trading Commission (CFTC) on quantities. ${ }^{14}$ The CFTC publishes weekly "Traders in Financial Futures" reports, which break down open interest for futures markets in which 20 or more traders hold large positions. The position data is supplied by clearinghouses and other reporting firms. The reports break down positions into four trader types: dealers, asset managers, leveraged funds, and other reporting

[^0]
[^0]:    ${ }^{14}$ The data are available at this link.

### Page 21
entities. These classifications are based on the predominant business purpose self-reported by traders on the CFTC Form 40. This data is weekly and begins in July 2010.

# 3.1.3 Money Market Fund Holdings 

We obtain data on the holdings and total net assets (TNAs) of money market mutual funds (MMFs) from Crane data. The data is compiled from form N-MFP, which MMFs are required to file with the Securities and Exchange Commission (SEC) every month.

### 3.1.4 Hedge Fund Returns

We also use hedge fund returns from the Preqin Pro Hedge Fund Database. This database includes performance data on over 24,000 hedge funds. Importantly for our purposes, the database contains descriptive information on fund strategies, which allows us to focus on funds that self-report being involved in the arbitrage trades that we study.

### 3.2 Characterizing Arbitrage Comovement

### 3.2.1 Baseline Results

We now turn to our first main result: the correlation between arbitrage spreads is low. Figure 3 presents this result graphically, depicting a heat map of pairwise correlations between the absolute value of different spreads. Darker red indicates higher positive correlations. With the exception of the diagonal, little of the figure is dark red, indicating that correlations are generally low.

Table 2a provides formal statistical evidence on pairwise correlations. The average pairwise correlation is 0.22 , and the 75 th percentile of pairwise correlations is 0.42 . These results are at odds with simple structures for the intermediary sector, in which there is only a single balance sheet constraint or a single funding factor. As shown in Section 2, in these cases, arbitrage spreads should be perfectly correlated. In Figure 4, we conduct a principal components analysis of spreads. Consistent with the low correlations documented above, it takes 11 principal components

### Page 22
to cumulatively explain $90 \%$ of the variation in arbitrage spreads. Furthermore, the last column of Table 2a shows that we can reject the null of equal correlations across all arbitrage pairs. ${ }^{15}$ Thus, the data suggest a complex structure for the intermediary sector. Either balance sheet and funding integration hold, but the representative intermediary faces a large number of different constraints, or there is significant segmentation in arbitrage.

# 3.2.2 Measurement error 

Measurement error is an important issue to consider when interpreting low arbitrage correlations. To see why, suppose that the observed spread $s_{i, t}$ equals the true spread $s_{i, t}^{*}$ plus an error term that is independent across arbitrages:

$$
s_{i, t}=s_{i, t}^{*}+\varepsilon_{i, t}
$$

where the variance of the true spread is $\operatorname{Var}\left[s_{i, t}^{*}\right]=\sigma_{i}^{2}$ and the variance of the measurement error $\varepsilon_{i, t}$ is $\operatorname{Var}\left[\varepsilon_{i, t}\right]=\sigma_{i, \varepsilon}^{2}$. Let $\rho_{i j}^{*}$ denote the correlation between the true spreads and $\rho_{i j}$ denote the correlation between the observed spreads. In this setting, the true correlation $\rho_{i j}^{*}$ and measured correlation $\rho_{i j}$ are related as follows:

$$
\begin{aligned}
\rho_{i j} & =\rho_{i j}^{*} /\left(\lambda_{i} \lambda_{j}\right) \\
\lambda_{i} & =\sqrt{\frac{\sigma_{i}^{2}+\sigma_{i, \varepsilon}^{2}}{\sigma_{i}^{2}}}
\end{aligned}
$$

Because the adjustment factor $\lambda_{i}$ is above 1 for all $i$, observed correlations will be biased toward zero. Thus, if arbitrage is fully integrated and the representative intermediary faces a limited number of constraints $\left(\rho_{i j}^{*} \approx 1\right)$, measurement error may lead us to incorrectly conclude otherwise based on low measured correlations.

We address potential measurement error in a few complementary ways. To start, consider the simple case in which the variance of measurement error is a constant proportion $\theta$ of the variance

[^0]
[^0]:    ${ }^{15}$ The low daily correlation between arbitrage spreads is more striking given that the high daily persistence of spreads (Table 1) should, if anything, generate spurious relationships between arbitrages (Granger and Newbold, 1974). The average pairwise correlation of changes in arbitrage spreads is similarly low at $5 \%$.

### Page 23
of true spreads, $\sigma_{i, \varepsilon}^{2}=\theta \sigma_{i}^{2}$. In this case, Eq. (8) simplifies to $\rho_{i j}=\rho_{i j}^{*}(1+\theta)^{-1}$. If the variance of the measurement error is less than half that of true spreads $(\theta<0.5)$ and true spreads are perfectly correlated, measured pairwise correlations should be greater than 0.67 . However, in Table 2a we reject the null that the average pairwise correlation of all spreads is greater than 0.67 . Moreover, we reject the null that the individual pairwise correlation is above 0.67 for $90 \%$ (448/496) of pairs. One can also reverse the exercise and ask how large measurement error would need to be in order to generate the correlations that we observe. If $\sigma_{i, \varepsilon}^{2}=\theta \sigma_{i}^{2}$ and true spreads are perfectly correlated, $\theta \approx 4$ would be required to generate a measured correlation of $0.22 .{ }^{16}$

If true spreads more persistent than measurement errors, another approach is to smooth the data. Figure 4 shows that we obtain very similar results if we compute principal components after taking a five-day or one-month moving average of spreads. Averaging should increase the ratio of variation driven by true spreads as opposed to noise, but it has little effect on the principal components analysis. Even after taking one-month moving averages of spreads, it takes 10 principal components to cumulatively explain over $90 \%$ of the variation in our arbitrage spreads.

The final reason we think measurement error is unlikely to be driving our results is that the correlations are not uniformly low. While spreads are far from perfectly correlated, they still have an interesting structure. Figure 4 shows that there is important common variation in spreads as emphasized by the previous literature, including Pasquariello (2014) and Liu (2020). When considering all trades, the first three principal components of daily spreads cumulatively explain $59 \%$ of their variation. If spreads were completely uncorrelated, we would expect them to explain only $33 \% .{ }^{17}$ Thus, our principal components analysis reveals a meaningful underlying economic structure to arbitrage spreads.

Figure 3 and Table 2 b suggest two places to look for this structure. First, cross-strategy

[^0]
[^0]:    ${ }^{16}$ Eq. 8 also shows that any attenuation bias can be directly addressed with knowledge of the adjustment factors, $\lambda_{i}$. If arbitrage spreads follow a one-factor model, the adjustment factors can be estimated using instrumental variables (IV) regressions (Hausman, 2001). Section A.2.1 of the Internet Appendix develops this idea further and shows that arbitrage correlations remain low even after adjusting them for measurement error.
    ${ }^{17}$ If spreads were uncorrelated, then the first three principal components would simply be the three spreads with the largest variance, and the total variance of spreads would be the sum of individual spread variances. In our data, the ratio of the sum of the largest three variances to the sum of all variances is about $33 \%$.

### Page 24
correlations are relatively high for the box, CIP, and equity-spot futures spreads. Second, correlations are higher within strategy than across strategy. For instance, Table 2b shows the average pairwise correlation of the three box trades is 0.87 and the average pairwise correlation of CIP spreads is 0.35 . We explore these sources of correlation further in Sections 4 and 5 of the paper, arguing that they reflect funding and balance sheet segmentation.

# 3.2.3 The Term Structure of Arbitrage 

The term structure is another important consideration when interpreting the correlation of arbitrage spreads. This topic has been studied in recent work by Du et al. (2022) and Hanson et al. (2022b). In our setting, intertemporal considerations may change the correlation structure of arbitrage even with an integrated intermediary sector. For instance, trades that differ in tenor may not be perfectly correlated because long-tenor trades reflect expected future balance sheet costs while short-tenor trades reflect only current balance sheet costs. Internet Appendix A. 3 modifies our baseline model to formalize these considerations; for a fuller treatment, see Du et al. (2022) and Hanson et al. (2022b).

A simple way to mitigate these concerns is to compare trades with similar tenors. Table 3 implements this idea by grouping trades into one of three buckets based on their tenor. The shorttenor bucket contains all trades whose maturity is always less than six months, namely CIP, equity spot-futures, and Treasury-spot futures. Medium-tenor trades are those whose tenor is greater than or equal to 6 months but less than or equal to 3 years. Finally, long-tenor trades are those with a tenor exceeding 3 years. The CDS-Bond arbitrages are included with long-tenor trades based on the typical tenor of their underlying bonds.

Table 3 shows the distribution of pairwise correlations for short, medium, and long-tenor trades. The broad takeaway from the table is that correlations remain relatively low, even within trades of the same tenor. For example, in Table 3a, the average correlation among short-tenor trades is 0.19 and the 75 th percentile of correlations is 0.35 . Because short-tenor trades are less exposed to mark-to-market risk, the low correlation among these trades cuts strongly against conventional

### Page 25
models featuring an integrated intermediary sector. As a more extreme example, consider the correlation between two overnight arbitrages: (i) the spread between interest paid on required and excess reserves (IOER) and the effective federal funds rate (Banegas and Tase, 2020); and (ii) the spread between the general collateral repo rate and the tri-party repo rate (Correa et al., 2020). Though these trades have virtually no mark-to-market risk, their correlation during our analysis sample is $23 \%$, a clear indication of segmentation. ${ }^{18}$

Tables 3b and 3c summarize the distribution of correlations for medium and long-tenor trades, respectively. The degree of integration appears higher in these trades compared to those with shorttenors, at least as evidenced by their larger average pairwise correlation (roughly $40 \%$ vs $20 \%$ ). This could occur if some institutions specialize in longer-tenor trades, perhaps because they are better equipped to manage mark-to-market risk. For example, access to stable funding may allow larger dealers to mitigate noise-trader risk because they can more reliably roll over repo. Specialization could also arise because longer-tenor arbitrages use fixed-income derivatives like interest rate and credit default swaps. With that said, the more important point is that correlations within medium and long-tenor trades are still far from perfect. In both groups, the average correlation is below $40 \%$ and the 75 th percentile is around $50 \%$. These relatively low correlations further support our main argument that arbitrage is more segmented than previously acknowledged in the literature.

# 3.2.4 Zones of Arbitrageur Inaction 

Arbitrageurs may not find it profitable to enter a market unless the level of arbitrage is sufficiently high due to debt overhang issues-as argued by Andersen et al. (2019), an intermediary facing a debt overhang problem will only enter a riskless arbitrage if the return is higher than its credit spread. Consequently, small arbitrage spreads may appear uncorrelated because of this "zone of inaction" even if the intermediary sector is integrated. To address this concern, we first compute

[^0]
[^0]:    ${ }^{18}$ We thank Wenxin Du for pointing us to this example. To construct the IOER arbitrage, we use the first-percentile of the overnight federal funds rate from the New York Federal Reserve. This necessarily focuses on the depository institutions who can earn an arbitrage profit because they are able to borrow in the Federal Funds market at favorable rates, most likely large banks (Banegas and Tase, 2020). The correlation between the GCF-TPR and the volumeweighted IOER arbitrage spread (truncated at zero) is $21 \%$. Tri-party repo rates from BNY Mellon are available starting in 2016.

### Page 26
the cross-sectional average 6-month credit default swap (CDS) spread across all New York Federal Reserve primary dealers, denoted $d_{t} .{ }^{19}$ Next, we compute the pairwise correlation of each pair of trades, conditional on both exceeding $d_{t}$. The logic of Andersen et al. 2019 suggests that dealers should be active when arbitrage spreads exceed this threshold. Table 4a summarizes the distribution of pairwise correlations when arbitrage spreads exceed dealer credit spreads. The average correlation remains below $30 \%$ and the distribution is comparable to the one observed in the full sample (Table 2a).

The behavior of arbitrage spreads during the onset of the Covid-19 pandemic also cuts against the idea that arbitrager inaction is responsible for low spread correlations. From March through May 2020, the average level of spreads rose to 46 basis points, nearly double the average level in our main sample. Over the same period, Table 4 b shows that the average pairwise correlation of spreads rose to 0.29 , a modest increase from the average of 0.22 observed in our analysis sample. These low correlations are also readily apparent in Figure 5a, which plots strategy-level spreads starting in March 2020. The figure shows how different trades diverge at the onset of the pandemic, with the CDS-Bond and equity spot-futures arbitrages peaking several days after other arbitrages. This divergence is particularly stark within Treasury spot-futures arbitrage, as Figure 5b shows that arbitrage spreads based on futures for 20-year Treasuries remained elevated much longer than those based on shorter-maturity Treasuries. Overall, the fact that correlations remain low when arbitrage spreads are relatively elevated reinforces our argument that arbitrage activity is segmented. ${ }^{20}$

# 3.3 Supply versus Demand 

As shown in Section 2, once we depart from the integrated intermediary benchmark, the correlations of arbitrage spreads are determined by both arbitrageur supply and end-user demand. One might wonder whether the low correlations we document arise primarily from the supply side or the

[^0]
[^0]:    ${ }^{19}$ We include any dealer that has been listed as a primary dealer since 2010.
    ${ }^{20}$ We further study the behavior of arbitrage spreads before the Dodd-Frank era in Internet Appendix A.2.2, showing that correlations were low before the 2008-09 financial crisis and providing evidence of funding and balance sheet segmentation during the crisis.

### Page 27
demand side. To shed light on this question, we follow the large literature on sign-restricted SVARs (Uhlig, 2005; Arias et al., 2018). While this approach was originally developed for macroeconomic time-series analysis, it has been applied more recently in financial markets by Goldberg and Nozawa (2021) and Hanson et al. (2022a), among others.

Denote $Y_{t}=\left[\begin{array}{ll}s_{t} & q_{t}\end{array}\right]^{\prime}$ as the vector of arbitrage spreads and quantities for a given trade. Quantities are defined more precisely below, but for now it is sufficient to think of them as the size of the derivative market that supports a particular arbitrage trade (e.g., net outstanding futures). The dynamics of $Y_{t}$ are assumed to take the following form:

$$
B Y_{t}=A_{0}+A_{1} Y_{t-1}+\varepsilon_{t}
$$

where $\varepsilon_{t}=\left[\begin{array}{ll}\varepsilon_{s, t} & \varepsilon_{d, t}\end{array}\right]^{\prime}$ are primitive orthonormal shocks. For reasons discussed below, the structural shock $\varepsilon_{s, t}$ can be thought of as a supply shock that emanates from arbitrageurs, whereas $\varepsilon_{d, t}$ can be thought of as demand for the derivatives relative to cash securities arising from end users like insurance or pension funds. Assuming $B$ is invertible, the reduced-form VAR implied by the structural model in (9) is:

$$
Y_{t}=\Phi_{0}+\Phi_{1} Y_{t-1}+u_{t}
$$

where $\Phi_{0}=B^{-1} A_{0}$ and $\Phi_{1}=B^{-1} A_{1}$. The covariance matrix of the reduced-form residuals $u_{t}=$ $B^{-1} \varepsilon_{t}=\left[\begin{array}{ll}u_{s, t} & u_{q, t}\end{array}\right]^{\prime}$ is given by $\Sigma_{u}$ and depends only on the matrix $B$. While the reduced-form parameters $\left(\Phi_{0}, \Phi_{1}, \Sigma_{u}\right)$ can be estimated by OLS or Bayesian methods, the structural parameters $\left(A_{0}, A_{1}, B\right)$ cannot be identified without imposing additional restrictions. One solution to this problem is to impose restrictions on the sign of the impact of structural shocks on the reduced-form shocks. In our context, we assume the following sign restrictions:

$$
\left[\begin{array}{l}
u_{s, t} \\
u_{q, t}
\end{array}\right]=\underbrace{\left[\begin{array}{l}
-+ \\
++
\end{array}\right]}_{B^{-1}}\left[\begin{array}{l}
\varepsilon_{s, t} \\
\varepsilon_{d, t}
\end{array}\right]
$$

### Page 28
These restrictions make our labeling of the structural shocks more clear. $\varepsilon_{s, t}$ is interpreted as a supply shock because it lowers arbitrage spreads and raises quantities. Conversely, $\varepsilon_{d, t}$ is interpreted as a demand shock because it raises both arbitrage spreads and quantities.

We estimate the sign-restricted SVAR using weekly data separately for each futures-based arbitrage trade, as these are the only trades for which quantity data is publicly available. The quantity for a given trade is defined as the net amount of futures outstanding in the CFTC's weekly "Traders in Financial Futures," described in more detail in Section 3.1.2. Arbitrage spreads equal the absolute value of raw spreads because this is the most natural object on which to impose the sign restrictions. ${ }^{21}$

Our estimation strategy closely follows Arias et al. (2018), who develop an efficient algorithm to estimate sign-restricted SVARs with appropriately conservative confidence intervals. To start, Bayesian methods are employed to estimate the reduced-form VAR parameters under a Normal-Wishart prior. Next, we randomly draw from the posterior distribution of the reduced-form parameters and use the Cholesky decomposition of $\Sigma_{u}$ to obtain a $B$ that satisfies the sign restriction in (10). ${ }^{22}$ This process is repeated 1,000 times to generate a set of structural parameters that all satisfy the sign restriction, reflecting the well-known result that sign-restricted SVARs are generally only set-identified. With some abuse of notation, let $\Theta_{i}$ be the set of identified structural parameters when estimating the model for trade $i$. Each element of this set implies its own sequence of supply and demand shocks and we denote $\left(\tilde{\varepsilon}_{i, t}^{s}, \tilde{\varepsilon}_{i, t}^{d}\right)$ as the shocks associated with the median parameter draw from $\Theta_{i}$.

Note that since the model is estimated separately for each trade, there are no restrictions put on the covariance of supply and demand shocks across trades. Figure 6a visualizes the correlation of estimated supply shocks $\tilde{\varepsilon}_{i, t}^{s}$ across trades. The plot shows that supply shocks are far from perfectly correlated, as would be the case if arbitrage were perfectly integrated. The average pairwise correlation of $16 \%$ is low and supports our broad argument that supply-side frictions like

[^0]
[^0]:    ${ }^{21}$ The 30-year Treasury spot-futures arbitrage is excluded because it is more prone to missing arbitrage spread data (see Table 1).
    ${ }^{22}$ Our exact implementation is based on the open source VAR Matlab toolbox of Breitenlechner et al. (2019), found here.

### Page 29
balance sheet or funding segmentation have a first-order impact on asset prices. With that said, Figure 6a also reveals portions of the market where arbitrage appears more integrated. For example, perhaps unsurprisingly, the average correlation of supply shocks within equity-spot futures arbitrage is higher at $62 \%$.

Figure 6b visualizes the correlation of the demand shocks $\tilde{\varepsilon}_{i, t}^{d}$ from the SVAR. Again, these shocks are most naturally interpreted as the relative demand for futures versus spot contracts from end-users like insurance companies and pension funds. Consistent with the intuition that demand is also segmented, the average correlation of the demand shocks equals 16\%. However, there are again portions of the capital markets where demand shocks are more correlated. For instance, within equity spot-futures trades, the average correlation of demand shocks equals $64 \%$.

The preceding correlation analysis was based on the median structural shocks $\tilde{\varepsilon}_{i, t}^{s}$ and $\tilde{\varepsilon}_{i, t}^{d}$ from the SVAR. However, given they are set-identified, we can also use them to put confidence bands on the correlation of the structural shocks. To do so, we select 10,000 random draws from the identified set of structural parameters $\Theta_{i}$ for each trade and compute the implied supply shock series. For each draw $k$, we then compute the correlation matrix $R_{k}$ of the supply shocks across trades. Figure 7a shows the $99 \%$ percentile of each element of $R_{k}$. Akin to a traditional bootstrap, the elements of the figure can be interpreted as the $1 \%$ upper bound on the pairwise correlation of supply shocks. The average upper bound equals $24 \%$, suggesting that arbitrage is far from integrated for futures-based trades with $99 \%$ confidence.

In Internet Appendix A.2.3, we use the SVAR to further decompose the covariance between a pair of arbitrage spreads into three terms suggested by the model in Section 2: (i) covariance between supply shocks; (ii) covariance between demand shocks; and (iii) covariance between supply and demand shocks across two trades. For the average pair, comovement between supply shocks contributes $14 \%$ to the overall covariance and comovement between demand shocks contributes $26 \%$. Thus, according to the SVAR, comovement between supply and demand shocks contribute similarly to the overall observed covariance of arbitrage spreads. The remaining covariance is attributable to cross-market supply and demand terms.

### Page 30
# 4 Segmented Funding 

In this section, we focus on funding frictions as a key driver of the low correlations of supply shocks documented above. As discussed in Section 2, the underlying violation of the Modigliani and Miller (1958) theorem is that certain riskless portfolios cannot be funded at the riskless rate. For instance, the equity spot-futures arbitrage involves holding the underlying equities and selling equity futures. Taken together, this position is riskless, but it cannot be funded with (for instance) Treasury repo. As the cost of funding for certain arbitrage trades moves, spreads move as well.

We proceed in three steps. We start with suggestive evidence that there are differences in funding structures across the different arbitrage strategies we study. We then provide more formal empirical evidence that movements in funding costs affect arbitrage spreads. In particular, we show that they help explain the relatively high degree of comovement between the box, CIP, and equity-spot futures spreads in Table 2b, and the relatively low degree of comovement between those spreads and the others we study. Finally, we show that specialization in funding creates segmentation that goes beyond the divide between unsecured and secured funding markets.

### 4.1 Suggestive Evidence on Margins

Table 5 shows that there are meaningful differences in the availability of secured financing across arbitrage strategies. The data primarily come from the Federal Reserve Bank of New York's Triparty Repo Infrastructure Reform Task Force. ${ }^{23}$ The Treasury spot-futures, Treasury-swap, and TIPS-Treasury arbitrages can be largely financed with Treasury repo, requiring only a 2\% margin. In other words, intermediaries need little unsecured debt or equity funding to enter into these arbitrages. Conversely, the box, CIP, and equity spot-futures arbitrages require higher margins between 8\% and $12 \%$. For these arbitrages, unsecured funding conditions are much more important. We will therefore frequently group these trades together, labeling them "unsecured", while we label the

[^0]
[^0]:    ${ }^{23}$ For currencies, we report data from central bank lending operations by the Bank of England and the European Central Bank because the quantity of tri-party repo backed by international collateral is typically small (less than $0.5 \%$ of the total). Margin data from the NY Fed can be found here, Bank of England data can be found here, and ECB data can be found here.

### Page 31
remaining trades (Treasury spot-futures, Treasury-swap, TIPS-Treasury, and CDS-bond) "secured."

# 4.2 Shocks to Unsecured Funding and Arbitrage Activity 

In this section, we show that variation in unsecured funding conditions induces comovement in unsecured arbitrage spreads but not secured spreads. We start with OLS evidence in Table 6. We work with implied riskless rates from different arbitrages, as opposed to spreads that subtract out a benchmark riskless rate, to separate changes in secured and unsecured funding conditions. In the first two columns, we run the following monthly panel regression:

$$
\Delta r_{i, j, t}=\alpha_{i, j}+\beta_{1} \Delta y_{i, t}+\beta_{2} \Delta T E D_{t}+\varepsilon_{i, j, t}
$$

where $r_{i, j, t}$ is the implied riskless rate for individual trade $i$ in broad strategy $j$ in month $t$ and $y_{i, t}$ is the yield on a Treasury with the same maturity as the horizon of the trade-a proxy for the true riskless rate. $T E D_{t}$ is the maturity-matched Treasury-Eurodollar spread (i.e., LIBOR minus Treasury) and proxies for unsecured funding costs. ${ }^{24}$ Standard errors are clustered by strategy-month.

In the first column of Table 6, the sample consists of unsecured trades (equity spot-futures, CIP, and box). These trades load on the Treasury yield with a coefficient close to 1, but also have a high loading on the TED spread, consistent with the idea that these trades require a significant amount of unsecured funding. Indeed, the coefficient on the TED spread of 0.49 is higher than the margin requirements listed in Table 5, possibly because these trades require more unsecured funding on the margin than on average. ${ }^{25}$

The second column of Table 6 shows a stark contrast for secured trades. These trades also load on the Treasury yield with a coefficient close to 1 , but their loading on the TED spread is much

[^0]
[^0]:    ${ }^{24}$ ICE Benchmark Association does not publish LIBOR rates beyond one year. Thus, when the tenor of the trade exceeds one year, we construct the TED spread using the one-year LIBOR and Treasury yields.
    ${ }^{25}$ In Internet Appendix A.2.6, we provide suggestive evidence in favor of this interpretation for equity spot-futures arbitrage. We show that the value of equity securities held by dealers is nearly double the size of equity triparty repo, cutting against the idea that dealers fully finance their equity positions with equity repo.

### Page 32
lower ( 0.07 vs 0.49 ) and is not statistically distinguishable from zero. ${ }^{26}$ The remaining columns of Table 6 run the regression strategy-by-strategy. The coefficient on the TED spread is higher for all unsecured strategies than it is for any of the secured strategies. Moreover, we cannot reject the null that the TED spread loading is zero for each of the secured strategies, but we can for each of the unsecured ones.

Previous research has noted that arbitrage spreads are sensitive to the TED spread (e.g., Garleanu and Pedersen, 2011), particularly during stressed periods like the 2007-09 financial crisis. Our focus here is to highlight differences in the sensitivity of arbitrage strategies to the TED spread. We interpret these differences as showing that frictions in funding markets drive cross-sectional differences in arbitrage spreads.

While the results in Table 6 are consistent with funding segmentation, they could also reflect balance sheet segmentation. For instance, suppose broker dealers specialize in unsecured trades. Then a deterioration in their balance sheet health could lead to a simultaneous rise in the TED spread and unsecured arbitrage spreads. Formally, in the notation of the model, we are interpreting the results in Table 6 as differential loadings on a funding factor $f_{1, t}$, captured by the TED spread. However, they could also reflect variation in the marginal balance sheet costs $c_{1 t} V_{1 t}$ of arbitrageurs who specialize in unsecured trades.

To isolate the role of funding segmentation, we follow Anderson et al. (2019) and study the 2016 MMF reform. The reform modified SEC Rule 2a-7, which governs MMFs. It required institutional prime MMFs to switch from reporting stable to floating net asset values (NAVs), while allowing government MMFs to continue reporting stable NAVs. Thus, following the reform, many prime MMFs converted to government MMFs to accommodate client preferences for stable NAVs. Prior to the reform, prime MMFs were a significant source of unsecured funding for banks, so the reform plausibly represents a funding shock that is distinct from bank balance sheet shocks. ${ }^{27}$ Indeed, as

[^0]
[^0]:    ${ }^{26}$ Note that correlations with the Treasury yield are very high for some secured trades because these trades involve Treasuries.
    ${ }^{27}$ Consistent with this interpretation, Figure A3 shows that the balance sheet strength of dealers was not negatively affected by the reform. The measure of balance sheet strength in the plot comes directly from He et al. (2017) and is defined as the ratio of market capitalization to market capitalization plus book debt for the New York Federal Reserve's primary dealers' publicly-traded holding companies. We discuss the distinction between balance sheet and funding

### Page 33
shown in Figure 9a, unsecured MMF lending to banks fell approximately $\$ 550$ billion as a result of the reform. Anderson et al. (2019) study how global banks respond to this shock, arguing that they withdraw from CIP and central bank reserve arbitrage. In contrast, we use the shock to trace out funding segmentation in the cross section of arbitrage.

Figure 9b shows that the MMF reform shock generated a significant rise in the TED spread. As the reform was anticipated, spreads start rising before the reform is implemented. For example, five months before the reform, MMFs were more willing to lend to banks unsecured for four months than six months. Figure 9c shows that around the time of the reform, spreads on unsecured arbitrages rise relative to secured arbitrages. Thus, unsecured funding shocks induce comovement in arbitrage spreads for unsecured trades but result in low correlations between secured and unsecured trades.

Table 7 provides formal regression evidence corresponding to these figures. ${ }^{28}$ We first estimate the following OLS regression:

$$
s_{i, t}=\alpha_{i}+\alpha_{t}+\beta 1[i \in \text { Unsecured }] \times 1[t \geq \text { October2016 }]+\varepsilon_{i, t}
$$

where $s_{i, t}$ is the absolute value of the arbitrage spread for trade $i$ on date $t, \alpha_{i}$ is a trade fixed effect, and $\alpha_{t}$ is a time fixed effect. We estimate the regression using data through October 2017 to focus on the one-year impact of the reform on arbitrage spreads. Given the persistence of spreads at the daily level (Table 1), we cluster standard errors by trade and time. In Internet Appendix A.2.5, we show that our inference is also robust to using Driscoll and Kraay (1998) standard errors, which are explicitly designed to handle serial correlation and heteroskedasticity in panel settings. Column (1) shows that unsecured spreads rose by an average of 12 bps in the year following the reform. In column (2), we estimate a dynamic version of Eq. (12) to more carefully study the response of spreads to the reform over time. Unsecured spreads initially rise 18 bps relative to other arbitrage
shocks in the context of the MMF Reform in Internet Appendix A.2.4.
${ }^{28}$ While Figure 9c and Table 7 look similar to a differences-in-differences analysis, they are formally closer to a placebo test. In particular, the parallel trends assumption should hold under the null of integrated funding. However, under our preferred interpretation-that the unsecured arbitrages are segmented from the secured arbitrages-there is no reason for the parallel trends assumption to hold. That is, we do not think that the gap in spreads between unsecured and secured arbitrages would have remained fixed in the absence of the 2016 MMF reform. Instead, we simply interpret this evidence as showing that only unsecured arbitrages are affected by a shock to unsecured funding.

### Page 34
spreads in the October 2016 and remain elevated near that level for the subsequent three months, after which they only partially revert between February and October 2017. These findings indicate that the effect of the funding shock on arbitrage activity persisted for many months.

Furthermore, the passthrough of 0.59 implied by the 2016 MMF reform event study is similar to the OLS estimate of 0.49 in Table 6, and we cannot reject the null hypothesis that they are equal. ${ }^{29}$ This suggests that most of the comovement between the TED spread and unsecured trades in our sample is driven by funding shocks, as opposed to bank balance sheet shocks. Taken together, the analysis in Tables 6 and 7 shows that funding segmentation is one broad driver of low correlations among arbitrage spreads. Some trades-equity spot-futures, box spreads, and CIP—require more unsecured funding than others. These trades are therefore more exposed to broad conditions in unsecured funding markets, as measured by the TED spread. As a result, unsecured trades tend to comove more with each other than they do with secured trades. In other words, funding segmentation impacts asset prices.

# 4.3 Further Funding Segmentation 

We next provide evidence that funding markets are more segmented than the simple divide between secured and unsecured trades. In particular, we argue that additional funding segmentation helps to explain why the equity spot-futures, box, and CIP trades, while more correlated than other trades, are still not highly correlated with each other. Building on the MMF literature (e.g., Chernenko and Sunderam, 2014; Rime et al., 2017; Li, 2021; Hu et al., 2021), we document that specialization in certain types of funding by MMFs is reflected in arbitrage spreads.

Our analysis starts from the observation made by Hu et al. (2021), who show that Fidelity MMFs were the largest provider of equity-repo financing during the period of 2010 to 2013. In Table 8, we show that funding shocks to Fidelity move equity spot-futures arbitrage spreads over and above the effect of the TED spread. To do so, we augment Eq. (11) with flows into Fidelity's

[^0]
[^0]:    ${ }^{29}$ Around the reform, the TED spread and unsecured spreads increased by 31 and 18 bps, respectively. This implies that the passthrough of changes in the TED spread to unsecured spreads equals 0.59 .

### Page 35
Institutional Prime (IPrime) MMFs. ${ }^{30}$ Columns 1-3 report OLS results. Column 1 shows that equity spot-futures arbitrages spreads fall when funds flow into Fidelity MMFs, consistent with the idea that a positive Fidelity funding supply shock reduces the cost of funding equity holdings and hence equity spot-futures spreads. Columns 2 and 3 show that flows to Fidelity have no impact on either other unsecured trades (box and CIP) or secured trades, suggesting that Fidelity funding supply shocks do not affect these trades. These results also suggest that flows into Fidelity are not proxying for aggregate unsecured funding conditions or aggregate intermediary balance sheet health.

The OLS estimates in columns (1)-(3) are potentially biased because flows into Fidelity IPrime MMFs could be driven by supply or demand. On the one hand, when arbitrage spreads rise, arbitrageurs may demand funding from Fidelity IPrime MMFs to take advantage of the profit opportunity, thereby leading to a positive correlation between spread changes and MMF flows. On the other hand, exogenous outflows from Fidelity IPrime MMFs will contract the supply of repo funding for available for arbitrage and raise arbitrage spreads, resulting in a negative correlation between spread changes and flows. The opposing effects of supply and demand therefore work against finding any relationship between spread changes and Fidelity IPrime flows. Thus, the fact that there is still a negative relationship between changes in equity spot-futures arbitrage spreads and Fidelity IPrime MMF flows suggests funding supply shocks dominate for this trade. ${ }^{31}$

In columns 4-6, we try to address this potential endogeneity bias by instrumenting with "passive flows" into Fidelity IPrime funds, defined as:

$$
Z_{t}=F_{t} \times L_{t-3}^{I}
$$

where $F_{t}$ is the flow into all Fidelity MMFs and $L_{t-3}^{I}$ is the lagged share of Fidelity MMF assets that are in its Institutional Prime funds. The validity of $Z_{t}$ as an instrument for flows into Fidelity IPrime

[^0]
[^0]:    ${ }^{30}$ The data for this analysis is based on the SEC's Form N-MFP. According to these data, virtually all of Fidelity's equity repo lending is done by its prime MMFs.
    ${ }^{31}$ Another concern is that the OLS results reflect balance sheet segmentation. It could be that specific intermediaries are important for equity spot-futures arbitrage and flows to Fidelity reflect the health of those intermediaries' balance sheets. In this case, however, the most natural interpretation is that both balance sheet and funding segmentation are at work. Flows to Fidelity reflect the health of particular intermediaries over and above the TED spread because Fidelity has funding relationships with those intermediaries.

### Page 36
funds rests on two assumptions. The first is that the lagged share $L_{t-3}^{I}$ is exogenous to arbitrager demand for funding from Fidelity IPrime funds, which seems reasonable given the lag length of one quarter. The second is that demand for arbitrage funding is exogenous to flows into all Fidelity MMFs $\left(F_{t}\right)$. This assumption is likely to hold for equity-spot futures arbitrage because equity repo lending is a very small portion Fidelity's overall MMF portfolio. During our sample, equity repo lending accounts for less $1 \%$ of all lending by Fidelity MMFs and never exceeds $3.1 \%$. Thus, while Fidelity is large relative to the equity repo market (average lender share of 53\%), it is unlikely that demand for equity repo funding drives flows into all Fidelity MMFs.

Consistent with demand inducing bias into the OLS coefficients, column (4) shows that the relationship between equity spot-futures arbitrage spreads and Fidelity IPrime flows is stronger when we instrument. ${ }^{32}$ Importantly, the IV estimate is close to zero and is not statistically significant for other unsecured arbitrages (column 5) and secured arbitrages (column 6), further confirming that Fidelity IPrime funds play no special role for these trades. Overall, the evidence in Table 8 shows that funding is segmented even within the unsecured market - the cost of funding equity holdings moves independently of other funding costs.

Taken together, our results suggest that funding segmentation is an important driver of segmentation in asset prices. Unsecured trades are broadly segmented from secured trades because unsecured funding is segmented from secured funding, with the TED spread capturing these differences. Beyond the simple divide between secured and unsecured funding, there is additional segmentation, which appears to be driven by specialization among funding sources.

# 4.4 Factor Analysis 

To complement our analysis of unsecured and secured arbitrages, we now conduct a simple principal component analysis of the two groups. To start, we document that the first principal component of unsecured arbitrages explains $51 \%$ of the daily variation in the level of spreads. Reinforcing the results in Section 4.2, Figure 8a shows that it is natural to interpret this principal component

[^0]
[^0]:    ${ }^{32}$ In Internet Appendix Section A.2.7, we report the first stage.

### Page 37
as capturing common unsecured funding costs because the first PC closely tracks the TED spread, also shown in the figure. The correlation between the two series is $69 \%$ at the monthly level. The existence of a meaningful factor structure among unsecured arbitrages explains why they are more correlated with each other than secured arbitrages, yet it is also important to note that half of the total variation in unsecured spreads is not captured by common funding costs. As we argue in Sections 4.3 and 5, this remaining variation is likely driven by strategy-specific funding costs or balance sheet shocks to specialized intermediaries.

A similar analysis of secured arbitrages indicates the first principal component explains $40 \%$ of the daily variation in spread levels. Figure 8b plots the monthly version of this PC along with the TED spread for reference. Unlike unsecured arbitrages, the first PC of secured arbitrages is largely unrelated to the TED spread, as the two are only $36 \%$ correlated at the monthly level. This finding supports our argument that funding segmentation drives down the correlation between unsecured and secured arbitrages (Section 4.2). The next question is how to interpret the first PC of secured arbitrages. We explore three possibilities: (i) secured funding costs, (ii) balance sheet costs of dealers, and (iii) the balance sheet costs of non-dealer intermediaries.

A first possibility is that secured funding costs move independently from unsecured funding costs, but also have a strong factor structure. If this were the case, the first PC of secured arbitrage spreads would have a high correlation with common proxies for funding conditions in secured financing markets. We find little evidence consistent with this hypothesis. For example, Figure 8b also plots the spread between the GCF repo rate and the Interest on Excess Reserves (IOER) paid by the Federal Reserve. This proxy has been used to measure repo market conditions in several recent papers, including Correa et al. (2020) and Copeland et al. (2021). It is clear from the plot that the first PC of secured arbitrages and the GCF-IOER spread follow different time-series trends, as their monthly correlation is only $30 \%$.

Another possibility is that the first PC of secured arbitrage spreads reflects variation in the balance sheet costs of banks, which could matter for instance because dealers intermediate secured funding markets, namely repo. This conjecture follows from Correa et al. (2020) and He et al.

### Page 38
(2022), who show that overnight Treasury repo rates spike at the end of each quarter because banks reduce their intermediation activity to avoid regulatory capital charges. However, we think it is unlikely that the first PC of secured arbitrages reflects bank balance sheet costs because the magnitudes do not line up. The magnitude of quarter-end spikes in overnight repo rates implies relatively small spikes in one-week and one-month repo rates, which are the relevant tenors for the secured arbitrages that we study. For instance, He et al. (2022) find that the overnight spread between the General Collateral Finance Repo rate (GCF) and Tri-Party repo rate (TPR) spikes by roughly 20 bps at quarter end, implying one-week and one-month spikes of 3 and 0.7 bps , respectively. By comparison, the time-series volatility of secured arbitrages is roughly 22 bps. Thus, the variation in repo rates induced by bank balance sheet costs is likely too small to explain the observed variation in secured arbitrage spreads.

In light of these results, our preferred interpretation is that the first PC of secured arbitrages reflects common variation in the balance sheet costs of (non-dealer) arbitrageurs. Though such costs are inherently hard to measure without data on the exact institutions that are active in each trade, our analysis in Section 5.4 supports this interpretation. In particular, we show that when hedge funds who specialize in fixed income arbitrage experience poor returns in month $t$, spreads on secured arbitrages tend to increase in month $t+1$, whereas unsecured arbitrages are not affected.

To be clear, we are not claiming that secured financing conditions do not matter for secured arbitrages. Rather, variation in secured financing rates is likely too small to explain the observed variation in secured arbitrage spreads. To see this more formally within the model in Section 2, let $f_{t}^{\text {sec }}$ be the spread between the funding rate for secured arbitrages and the riskless rate. Further, denote $c_{t} V_{t}$ as the marginal balance sheet cost for arbitragers that are active in secured trades. Then the equilibrium arbitrage spread of secured arbitrages is a linear combination of funding and balance sheet costs:

$$
s_{n, t}=a f_{t}^{\text {sec }}+b c_{t} V_{t}
$$

Thus, while secured funding costs $f_{t}^{\text {sec }}$ clearly impact the level of spreads, they may not contribute meaningfully to the variation of spreads if balance sheet costs $c_{t} V_{t}$ are sufficiently volatile. Our

### Page 39
results essentially suggest that repo rates against fixed income collateral like Treasuries or corporate bonds (captured by $f_{t}^{\text {sec }}$ ) are much less volatile than the balance sheet costs (captured by $c_{t} V_{t}$ ) of arbitragers in secured trades, like hedge funds.

# 5 Segmented Balance Sheets 

We next provide evidence of a second driver of segmentation in asset prices: balance sheet segmentation across intermediaries. As discussed in Section 2, if different intermediaries specialize in different trades, then the tightness of their individual balance sheet constraints will affect some arbitrage spreads but not others.

We provide three complementary types of analysis. First, we provide suggestive evidence from CFTC quantity data that different intermediaries are more central for different trades. We then examine two event studies: JP Morgan's London Whale episode in 2012 and Deutsche Bank's exit from the CDS market in 2014. Finally, we show that the tightness of fixed income hedge fund balance sheet constraints are important for certain secured trades.

### 5.1 Suggestive Evidence from Quantities

Table 9 uses the CFTC data to provide suggestive evidence that different intermediaries play bigger roles in certain arbitrage trades. The CFTC summarizes positions in different futures of different types of intermediaries: dealers, hedge funds (labeled by the CFTC as "leveraged funds"), and asset managers. For each intermediary type and contract, the CFTC reports total gross positions long and short of the intermediary type in the contract, as well as total positions in the contract netted by intermediary type. The data is silent on the specific intermediaries that are active in a particular trade, and therefore does not perfectly reveal the marginal price setter for each contract. It does, however, give us a sense of which intermediaries are most active in which contract.

We compute three different measures of activity. First, we look at an intermediary type's gross share of activity in a contract-the sum of the intermediary type's long, short, and spread positions

### Page 40
in that contract, divided by the total long, short, and spread positions in the contract. Second, we net within each intermediary type, taking the difference between gross long and gross short positions for the intermediary type. We then report the intermediary type's net position as a fraction of the total net positions across intermediaries. Finally, we report the fraction of days the intermediary type's net position is in the direction that would earn the arbitrage spread. A high fraction of days earning the spread is suggestive evidence that the intermediary type is an important arbitrageur for the contract, accommodating demand from other sectors.

All three measures tell the same story. Dealers are the biggest players in equity futures, while hedge funds and asset managers play a more important role in Treasury futures. For instance, dealers are in a net position that earns the arbitrage spread in equity futures on $87 \%$ of days, while hedge funds are in a net position to earn the spread on $45 \%$ of days, and asset managers are in a net position to earn the spread on only $8 \%$ of days. Moreover, dealers have the largest share of equity futures in terms of gross and net positions. In contrast, hedge funds appear to be the most active in Treasury futures, as their net position earns the arbitrage spread on $58 \%$ of days. Dealers are in a net position to earn the arbitrage spread on $50 \%$ of days, though their shares of gross and net outstanding are relatively small compared to hedge funds and asset managers.

While certainly not definitive, these numbers suggest that dealer balance sheet constraints are likely to be particularly important for equity futures, while hedge fund balance sheets are more important for Treasury trades. The notion that hedge funds are particularly active in Treasury spot-futures arbitrage is also consistent with Barth and Kahn (2021). We next turn to event studies for more definitive evidence.

# 5.2 Event Study: the London Whale 

In this section, we first provide suggestive evidence that JP Morgan is a particularly important intermediary for equity spot-futures arbitrage. We then examine the impact of balance sheet shocks to JP Morgan on equity spot-futures arbitrage spreads. According to Coalition Greenwich, a subsidiary of S\&P that provides benchmarks for the financial services industry, JP Morgan has

### Page 41
had the largest share of the market for equity derivatives since 2015. ${ }^{33}$ This accords with data from bank regulatory filings, which provide further suggestive evidence. In particular, we use the Y-9C regulatory filings to examine the trading book securities holdings of all U.S. bank holding companies. JP Morgan had by far the largest holdings of equity securities in its trading book over our sample, accounting for $37 \%$ of the total. JP Morgan's dominance was greater earlier in the sample; for instance, it held $56 \%$ of all equities in trading books in 2010. This evidence suggests that JP Morgan could play an outsized role in equity spot-futures arbitrage.

We now turn to the impact of an exogenous balance sheet shock to JP Morgan-the so-called "London Whale" episode"-on equity spot-futures arbitrages spreads. The London Whale episode was a result of activities by JP Morgan's Chief Investment Office (CIO) designed to hedge credit risk in the bank's loan portfolio. The Senate Permanent Subcommittee on Investigations issued a detailed report on the episode, from which we draw the following background information. ${ }^{34}$ At the beginning of 2012, JP Morgan wished to reduce the size of its hedges in the credit derivatives market. Rather than simply exiting its existing positions, the CIO instead sought to offset the credit protection it had bought by selling credit protection. In doing so, it became one of the biggest players in credit derivatives markets, with other traders nicknaming it the London Whale. In addition, it incurred significant basis risk, in terms of both the credit quality and maturity of the credit protection it had bought versus sold.

As shown in Figure 10a, this risk taking resulted in significant losses, which reached over \$6 billion by the end of 2012. For context, the firm's market capitalization at the time was about $\$ 125$ billion. Figure 10a shows that losses began to accelerate in March 2012, with monthly losses totaling $\$ 550$ million and representing $75 \%$ of the firm's year-to-date losses. The Senate report also indicates that several internal risk limits were breached for the first time during the month. Another important event occurred on June 13, 2012, when JP Morgan CEO Jamie Dimon testified before Congress and announced that significant additional losses were to be expected at the firm's next conference call with shareholders. We therefore use March 1, 2012 and June 13, 2012 as the focal

[^0]
[^0]:    ${ }^{33}$ The full report can be found here.
    ${ }^{34}$ The report is available at the following link.

### Page 42
points of our event study.
Figure 10b shows that around these critical dates equity spot-futures arbitrage spreads increased relative to other spreads. These results are consistent with the idea that JP Morgan is a particularly important intermediary for equity spot-futures arbitrage. Losses incurred in the London Whale episode tightened JP Morgan's balance sheet constraints relative to other intermediaries, moving equity spot-futures spreads but not other arbitrage spreads.

Figure 10c provides formal regression evidence of the comparison between equity spot-futures arbitrage spreads and other unsecured-funding intensive trades. In a weekly panel of the absolute value of spreads on unsecured trades, we estimate the regression:

$$
s_{i, t}=\alpha_{i}+\alpha_{t}+\sum_{j=-4}^{24}+\beta_{j} 1\left[i \in \text { Equity Spot-Futures Arbitrage }\right] \times 1[t=j]+\varepsilon_{i, t}
$$

Figure 10c plots the coefficients $\beta_{j}$ as well as $95 \%$ confidence intervals and shows that the patterns observed in Figure 10b are statistically significant. Equity spot-futures arbitrage spreads significantly increased compared to other unsecured arbitrage spreads following the event dates (March 1, 2012 and June 13, 2012) and remained elevated for several months. ${ }^{35}$

Finally, to bolster the argument that these results are due to balance sheet constraints and not funding costs, Figure 10d shows the evolution of rates on JP Morgan's commercial paper over the same period. There is little indication that short-term funding costs move substantially, which we take as evidence that the London Whale was primarily a balance sheet shock. Taken together, this evidence suggests that JP Morgan is an important intermediary for equity spot-futures arbitrage and shocks to its balance sheet constraints disproportionately impact those trades. In other words, balance sheet segmentation helps to explain the low correlation of arbitrage spreads.

[^0]
[^0]:    ${ }^{35}$ A potential confounding factor for the second event date (June 13, 2012) is that it is near the futures roll date in June. We show Internet Appendix Section A.2.8 that the size of the increase in the calendar spread during this period is an order of magnitude larger than what is typically observed around futures roll dates, suggesting that the June 2012 increase is not mechanically related to contract rolling. Another potential concern with regression (A.12) is that the persistence of spreads $s_{i, t}$ distorts our inference of the $\beta_{j}$ 's. We explore this issue in Section A.2.5 of the Internet Appendix.

### Page 43
# 5.3 Event Study: Deutsche Bank's exit from CDS 

In our second event study, we examine Deutsche Bank's exit from the CDS market. As discussed in Wang et al. (2021), in late 2014 Deutsche Bank announced that it was exiting the single-name CDS market and sold a significant fraction of its CDS portfolio to Citigroup. Consistent with a substantial adjustment in Deutsche Bank's participation in the CDS market, the notional value of CDS contracts outstanding fell from 2 trillion euros in its 2013 annual report to 1.4 trillion in its 2014 annual report. The exact timing of Deutsche Bank's exit is unknown, but Bloomberg reported the sale to Citigroup in September 2014, and Deutsche Bank publicly announced the exit on November 17, 2014. Wang et al. (2021) study the effects of Deutsche Bank's exit on CDS market liquidity. In contrast, we are interested in its effect on CDS-bond arbitrage spreads, as compared to other arbitrage spreads.

Figure 11a depicts spreads around the exit event, which we center around the first week of October. Throughout late 2014, CDS-bond arbitrage spreads rise, but other arbitrage spreads do not. Figure 11b provides formal statistical evidence by running a regression analogous to (13) for the CDS-Bond basis relative to other secured trades. The plot shows that the differential impact of Deutsche Bank's exit on CDS-bond arbitrage spreads relative to other secured spreads is significant at the 5\% level. Furthermore, the relative widening of the CDS-bond arbitrage spread persisted for over 5 months. These results are consistent with the idea that Deutsche Bank was a particularly important intermediary for CDS-bond arbitrages. Its decision to exit the market is akin to a tightening of its balance sheet constraints, which moved CDS-bond arbitrage spreads but not other spreads.

### 5.4 Hedge Fund Balance Sheet Constraints

We next turn to the impact of hedge fund balance sheet constraints, which we proxy for using monthly hedge fund returns. The idea is that following negative returns, hedge funds face tighter balance sheet constraints. Arbitrage spreads should subsequently rise for trades in which hedge

### Page 44
funds are important intermediaries. The following monthly regression tests this idea:

$$
\Delta s_{i, t}=\alpha+\beta r_{t-1}^{H}+\varepsilon_{i, t}
$$

$\Delta s_{i, t}$ in the regression is the change in the absolute value of the spread on trade $i$ in month $t$ and $r_{t-1}^{H}$ is the monthly return of hedge funds that specialize in fixed income arbitrage at $t-1$. Hedge fund returns are measured using Barclay's fixed income arbitrage hedge fund index, which is based on the returns of funds aiming to profit from price anomalies between related fixed income securities, including interest rate swap arbitrage, US and non-US government bond arbitrage, and forward yield curve arbitrage. ${ }^{36}$ The monthly hedge fund return series is standardized to have mean zero and unit variance. Lagged returns are used in the regression to avoid any confounding issues with reverse causality, since returns should be negatively related to contemporaneous changes in spreads but not future changes.

The first column of Table 10 shows that lagged fixed income hedge fund returns do not predict future increases in unsecured arbitrage spreads. In contrast, the second column shows a negative forecasting relationship for future changes in secured arbitrage spreads. A one-standard deviation return loss for fixed income hedge funds forecasts a 0.7 basis point increase in future secured arbitrage spreads. The remaining columns of Table 10 reveal that the relationship is driven primarily by the link between fixed income hedge fund returns and the Treasury-swap and CDS-Bond arbitrages. Overall, these results support the idea that hedge fund balance sheet constraints are more relevant for secured trades than unsecured trades.

We explore more granular balance sheet segmentation using individual hedge fund returns. ${ }^{37}$ We start by estimating the forecasting regression in Eq. (14) for each strategy and each of the top ten largest fixed income arbitrage hedge funds according to Preqin. This means we run ten different regressions for each strategy. We adjust our approach to hypothesis testing by computing

[^0]
[^0]:    ${ }^{36}$ See this link for more information.
    ${ }^{37}$ These results do not imply that dealer banks are completely uninvolved in the secured trades. Indeed, the dealers often supply hedge funds with funding through repo and prime brokerage relationships Boyarchenko et al. (2020). However, our analysis suggests that frictions in this funding process contribute less to the variance of secured spreads than balance sheet frictions in hedge fund equity capital.

### Page 45
critical values using the Bonferroni adjustment. Figure 12 displays the resulting $t$-statistic from these forecasting regressions. In the plot, hedge funds are indexed from one to ten along the $x$-axis and plot markers correspond to different strategies. The figure shows that different hedge funds are important for different arbitrage strategies. For instance, returns for hedge fund 1 negatively forecast future changes for both the CDS-bond and Treasury-futures arbitrages, with the $t$-statistics just at the Bonferroni threshold. Hedge fund 6 appears to be relevant for Treasury-futures arbitrage, while hedge fund 8 appears relevant for the TIPS-Treasury arbitrage, and hedge fund 10's balance sheet is important for the Treasury-swap arbitrages. It is worth noting that these results do not imply that the hedge funds we study are the only intermediaries that are marginal in a particular trade. Rather, they are likely to be representative of a broader set of intermediaries all following similar strategies and hence subject to similar balance sheet constraints.

To summarize, the results from this section suggest that balance sheet segmentation is important for explaining the low correlations of arbitrage spreads. Intermediaries appear to specialize in certain arbitrage strategies. Furthermore, when an intermediary that is important for one arbitrage suffers a balance sheet shock, the spread for that arbitrage can move without significantly affecting other arbitrage spreads. The price effects of shocks to specialized arbitrageurs imply that intermediary balance sheets are segmented.

# 6 Discussion and Conclusion 

### 6.1 Persistence of Segmentation

While our empirical results have documented that both funding and balance sheet segmentation impact asset prices, they are less definitive on how long this segmentation persists. Following market dislocations, capital will ultimately flow to profitable arbitrage opportunities; the question is how quickly (Duffie, 2010; Duffie and Strulovici, 2012). The sign-restricted SVARs estimated in Section 3.3 provide some insight into this question. To see why, first recall that the SVARs deliver weekly supply shocks for each spot-futures arbitrage. These weekly supply shocks can be cumulated to

### Page 46
construct supply shocks that occur over longer horizons (e.g., one month). Next, suppose arbitragers that specializes in a trade $i$ experience an exogenous tightening of their balance sheet in week $t$. While arbitragers that specialize in trade $j \neq i$ may not react immediately to the shock, it seems natural to expect that they will eventually adjust their balance sheets to take advantage of elevated spreads in trade $i$. Over time then, the total supply shocks across the two markets should therefore appear more correlated.

Consistent with this intuition, Figures 7 b and 7 c show the pairwise correlation of supply shocks for spot-futures arbitrages over aggregation periods of one month and one quarter, respectively. As with Figure 7a, these plots show the $1 \%$ upper bound on the pairwise correlation between supply shocks over different horizons, at least as implied by the sign-restricted SVARs. ${ }^{38}$ When moving from the one-week horizon in Figure 7a to the one-quarter horizon in Figure 7c, the darker red shading clearly shows that the supply shocks become more correlated over longer horizons. Though this suggests some amount of arbitrage capital flows across trades, the average $1 \%$ upper bound of the quarterly supply shocks is only $37 \%$ and thus points to a relatively persistent form of segmentation in arbitrage. This persistence is also apparent from our event studies of the 2016 MMF reform (Section 4.2), the JP Morgan London Whale (Section 5.2), and Deutsche Bank's Exit from the CDS market (Section 5.3). In all three events, a subset of arbitrage spreads remained elevated for several months after the initial funding or balance sheet shock.

In Internet Appendix Section A.2.9, we supplement our analysis by studying how the returns to different arbitrage strategies comove over varying holding periods. While correlations do increase over longer holding periods, they remain very far from perfect ( 15\%) even for holding periods of one quarter. With that said, there are some parts of the market that appear more integrated than others over longer horizons, such as the 3-month GBP CIP and the 10-year Treasury swap trades.

[^0]
[^0]:    ${ }^{38}$ To construct each figure, we first draw a random set of identified supply shocks for each trade, cumulate them to the desired frequency (e.g, one month), and compute the resulting correlation matrix of shocks across trades. The figure shows the $99 \%$ percentile of each pairwise correlation across 10,000 draws.

### Page 47
# 6.2 Conclusion 

In this paper, we show that riskless arbitrage is segmented. The average correlation between arbitrage spreads is low. We show that this low correlation is due to both funding and balance sheet factors.

Overall, our results demonstrate the importance of both balance sheet and funding segmentation in financial intermediation. In this respect, we build on research that documents how shocks to specialized risk-bearing capacity can disconnect risk premia across markets. Our focus on fundamentally riskless arbitrage trades highlights the pervasiveness of these issues. The arbitrages we study are relatively straightforward to execute and have expected returns that are essentially observable. These characteristics should mitigate the typical agency problems thought to underlie segmentation, slow moving capital, and the limits of arbitrage, yet in practice arbitrage still appears fairly segmented. It seems natural to expect more segmentation in the intermediation of risky assets where agency problems are likely to be more severe. More broadly, our results suggest that exploring the boundaries of the firm for financial intermediaries - why certain trades are grouped together in a market segment - is a promising direction for future research.

### Page 48
# References 

Adrian, T. and N. Boyarchenko (2012). Intermediary leverage cycles and financial stability. FRB of New York Staff Report (567). 5

Adrian, T., E. Etula, and T. Muir (2014). Financial intermediaries and the cross-section of asset returns. The Journal of Finance 69(6), 2557-2596. 2, 5

Andersen, L., D. Duffie, and Y. Song (2019). Funding value adjustments. The Journal of Finance 74(1), 145-192. 2, 9, 22, 23

Anderson, A., W. Du, and B. Schlusche (2019). Money market fund reform and arbitrage capital. 4, 29, 30

Arias, J. E., J. F. Rubio-RamÃrez, and D. F. Waggoner (2018). Inference based on structural vector autoregressions identified with sign and zero restrictions: Theory and applications. Econometrica 86(2), 685-720. 24, 25, 54, 55

Bai, J. and P. Collin-Dufresne (2019). The cds-bond basis. Financial Management 48(2), 417-439. 5

Banegas, A. and M. Tase (2020). Reserve balances, the federal funds market and arbitrage in the new regulatory framework. Journal of Banking and Finance 118, 105893. 22

Barth, D. and R. J. Kahn (2021). Hedge funds and the treasury cash-futures disconnect. 5, 16, 37
Bech, M. L. and E. Klee (2011). The mechanics of a graceful exit: Interest on reserves and segmentation in the federal funds market. Journal of Monetary Economics 58(5), 415-431. 5

Begenau, J. and T. Landvoigt (2021). Financial regulation in a quantitative model of the modern banking system. NBER WOrking Paper. 5

Bohrnstedt, G. W. and A. S. Goldberger (1969). On the exact covariance of products of random variables. Journal of the American Statistical Association 64(328), 1439-1442. 11

Boyarchenko, N., T. M. Eisenbach, P. Gupta, O. Shachar, and P. Van Tassel (2020). Bankintermediated arbitrage. Federal Reserve Bank of New York Staff Reports 854. 6, 41

Boyarchenko, N., P. Gupta, N. Steele, and J. Yen (2016). Trends in credit market arbitrage. FRB of New York Staff Report (784). 6

Breitenlechner, M., M. Geiger, and F. Sindermann (2019). Zerosignvar: A zero and sign restriction algorithm implemented in matlab. Technical report, Matlab Documentation. 25

Brunnermeier, M. K. and L. H. Pedersen (2009). Market liquidity and funding liquidity. The review of financial studies 22(6), 2201-2238. 5

Brunnermeier, M. K. and Y. Sannikov (2014). A macroeconomic model with a financial sector. American Economic Review 104(2), 379-421. 5

### Page 49
Bryzgalova, S. (2015). Spurious factors in linear asset pricing models. LSE manuscript 1(3). 6
Chernenko, S. and A. Sunderam (2014). Frictions in shadow banking: Evidence from the lending behavior of money market funds. The Review of Financial Studies 27(6), 1717-1750. 4, 31

Copeland, A., D. Duffie, and Y. Yang (2021, July). Reserves were not so ample after all. Working Paper 29090, National Bureau of Economic Research. 34

Copeland, A. M., A. Martin, and M. Walker (2010). The tri-party repo market before the 2010 reforms. FRB of New York Staff Report (477). 8

Correa, R., W. Du, and L. Y. Gordon (2020). U.s. banks and global liquidity. Technical report, National Bureau of Economic Research. 22, 34

Delong, J. B., A. Shleifer, L. H. Summers, and R. J. Waldmann (1993). Noise trader risk in financial markets. Journal of Political Economy 98(4). 3

Driscoll, J. C. and A. C. Kraay (1998, 11). Consistent Covariance Matrix Estimation with Spatially Dependent Panel Data. The Review of Economics and Statistics 80(4), 549-560. 30

Du, W., B. M. Hébert, and A. W. Huber (2019). Are intermediary constraints priced? Technical report, National Bureau of Economic Research. 5

Du, W., B. M. Hébert, and W. Li (2022). Intermediary balance sheets and the treasury yield curve. Technical report, National Bureau of Economic Research. 16, 21

Du, W., A. Tepper, and A. Verdelhan (2018). Deviations from covered interest rate parity. The Journal of Finance 73(3), 915-957. 5, 14

Duarte, J., F. A. Longstaff, and F. Yu (2006, 07). Risk and Return in Fixed-Income Arbitrage: Nickels in Front of a Steamroller? The Review of Financial Studies 20(3), 769-811. 8

Duffie, D. (1999). Credit swap valuation. Financial Analysts Journal 55(1), 73-87. 17
Duffie, D. (2010). Presidential address: Asset price dynamics with slow-moving capital. The Journal of finance 65(4), 1237-1267. 42

Duffie, D. and A. Krishnamurthy (2016). Passthrough efficiency in the fed's new monetary policy setting. In Designing Resilient Monetary Policy Frameworks for the Future. Federal Reserve Bank of Kansas City, Jackson Hole Symposium, pp. 1815-1847. 5

Duffie, D. and B. Strulovici (2012). Capital mobility and asset pricing. Econometrica 80(6), 2469-2509. 42

Fleckenstein, M. and F. A. Longstaff (2020). Renting balance sheet space: Intermediary balance sheet rental costs and the valuation of derivatives. The Review of Financial Studies 33(11), 5051-5091. 16

Fleckenstein, M., F. A. Longstaff, and H. Lustig (2014). The tips-treasury bond puzzle. the Journal of Finance 69(5), 2151-2197. 5, 16

### Page 50
Garleanu, N. and L. H. Pedersen (2011). Margin-based asset pricing and deviations from the law of one price. The review of financial studies 24(6), 1980-2022. 5, 29

Goldberg, J. and Y. Nozawa (2021). Liquidity supply in the corporate bond market. The Journal of Finance 76(2), 755-796. 24

Granger, C. W. and P. Newbold (1974). Spurious regressions in econometrics. Journal of econometrics 2(2), 111-120. 19

Gromb, D. and D. Vayanos (2002). Equilibrium and welfare in markets with financially constrained arbitrageurs. Journal of financial Economics 66(2-3), 361-407. 5

Gromb, D. and D. Vayanos (2018). The dynamics of financially constrained arbitrage. The Journal of Finance 73(4), 1713-1750. 2

Gürkaynak, R. S., B. Sack, and J. H. Wright (2007). The u.s. treasury yield curve: 1961 to the present. Journal of Monetary Economics 54(8), 2291-2304. 16

Gürkaynak, R. S., B. Sack, and J. H. Wright (2010, January). The tips yield curve and inflation compensation. American Economic Journal: Macroeconomics 2(1), 70-92. 16

Haddad, V. and T. Muir (2021). Do intermediaries matter for aggregate asset prices. The Journal of Finance 76(6), 2557-2596. 1

Hanson, S. G., A. Malkhozov, and G. Venter (2022a). Demand-and-supply imbalance risk and long-term swap spreads. Harvard Business School Working Paper. 24

Hanson, S. G., A. Malkhozov, and G. Venter (2022b). Demand-supply imbalance risk and long-term swap spreads. SRC Discussion Paper No 118. 16, 21

Hausman, J. (2001, December). Mismeasured variables in econometric analysis: Problems from the right and problems from the left. Journal of Economic Perspectives 15(4), 57-67. 20

Hazelkorn, T., T. Moskowitz, and K. Vasudevan (2021). Beyond basis basics: Liquidity demand and deviations from the law of one price. The Journal of Finance forthcoming. 5, 15

He, Z., B. Kelly, and A. Manela (2017). Intermediary asset pricing: New evidence from many asset classes. Journal of Financial Economics 126(1), 1-35. 2, 5, 29

He, Z. and A. Krishnamurthy (2013). Intermediary asset pricing. American Economic Review 103(2), 732-70. 2, 5, 8

He, Z., S. Nagel, and Z. Song (2022). Treasury inconvenience yields during the covid-19 crisis. Journal of Financial Economics 143(1), 57-79. 34, 35

Hu, X., J. Pan, and J. Wang (2021). Triparty repo pricing. Journal of Financial and Quantitative Analysis 56(1), 337-371. 4, 31

Ivashina, V., D. S. Scharfstein, and J. C. Stein (2015). Dollar funding and the lending behavior of global banks. The Quarterly Journal of Economics 130(3), 1241-1281. 2

### Page 51
Jamilov, R. (2021). A macroeconomic model with heterogeneous banks. Available at SSRN 3732168.5

Jermann, U. (2020). Negative swap spreads and limited arbitrage. The Review of Financial Studies 33(1), 212-238. 5, 16

Li, Y. (2021). Reciprocal lending relationships in shadow banking. Journal of Financial Economics 141(2), 600-619. 4, 31

Liu, J. (2020). Comovement in arbitrage limits. Available at SSRN 3242862. 6, 20
Merton, R. C. (1980). On estimating the expected return on the market: An exploratory investigation. Journal of Financial Economics 8(4), 323-361. 1

Modigliani, F. and M. H. Miller (1958). The cost of capital, corporation finance and the theory of investment. American Economic Review 1, 3. 1, 7, 27

Pasquariello, P. (2014). Financial market dislocations. Review of Financial Studies 27(10), 18681914. 5, 20

Rime, D., A. Schrimpf, and O. Syrstad (2017). Segmented money markets and covered interest parity arbitrage. 31

Ronn, A. G. and E. I. Ronn (1989). The box spread arbitrage conditions: theory, tests, and investment strategies. Review of Financial Studies 2(1), 91-108. 15

Shleifer, A. and R. W. Vishny (1997). The limits of arbitrage. The Journal of finance 52(1), 35-55. 5

Siriwardane, E. N. (2018). Limited investment capital and credit spreads. The Journal of Finance. 6
Uhlig, H. (2005). What are the effects of monetary policy on output? results from an agnostic identification procedure. Journal of Monetary Economics 52(2), 381-419. 3, 24, 54, 55
U.S. Senate (2014). Jpmorgan chase whale trades: A case history of derivative risks and abuses. 4
van Binsbergen, J. H., W. F. Diamond, and M. Grotteria (2019). Risk-free interest rates. Technical report, National Bureau of Economic Research. 5, 15

Wallen, J. (2019). Markups to financial intermediation in foreign exchange markets. 7
Wang, X., Y. Wu, H. Yan, and Z. Zhong (2021). Funding liquidity shocks in a quasi-experiment: Evidence from the cds big bang. Journal of Financial Economics 139(2), 545-560. 40

### Page 52
Figure 1: Strategy-Level Average Arbitrage
(a) Daily Frequency
![img-0.jpeg](img-0.jpeg)
(b) Monthly Moving Average
![img-1.jpeg](img-1.jpeg)

Notes: Panel A shows the average arbitrage spread by strategy at the daily frequency. Panel B plots a monthly (22 trading days) moving average of the daily series for each strategy.

### Page 53
Figure 2: Arbitrage Spreads by Strategy
![img-2.jpeg](img-2.jpeg)

Notes: This figure shows average absolute values of arbitrage spreads by strategy. Data is daily and spans January 1, 2010 to February 29, 2020.

### Page 54
Figure 3: Correlation of Arbitrage Spreads

![img-3.jpeg](img-3.jpeg)

**Notes:** The figure shows the pairwise correlation matrix of the absolute value of arbitrage spreads across all trades in our sample. See Section 3.1 for details on each trade. Data is daily and spans January 1, 2010 to February 29, 2020.

### Page 55
Figure 4: The Factor Structure of Arbitrage Spreads
![img-4.jpeg](img-4.jpeg)

Notes: This figure summarizes principal component analysis for the absolute values of arbitrage spreads in our sample. Each line shows the results of principal component analysis after we smooth our arbitrage spreads over a different moving average window. The $x$-axis shows the number of components and the $y$-axis shows the cumulative proportion of variance captured by those components. The red horizontal line on the plot is at the $90 \%$ level. See Section 3.1 for details on each trade. Data is daily and spans January 1, 2010 to February 29, 2020.

### Page 56
Figure 5: Arbitrage Spreads at the Onset of Covid
![img-5.jpeg](img-5.jpeg)
(a) Average Strategy-Level Spreads
![img-6.jpeg](img-6.jpeg)
(b) Treasury Spot-Futures Arbitrage

Notes: Panel (a) of this figure shows the average level of the absolute values of arbitrage spreads by strategy at the onset of the Covid-19 pandemic. Panel (b) plots individual Treasury spot-futures arbitrage spreads over the same period.

### Page 57
Figure 6: Correlation of Arbitrage Supply and Demand Shocks
(a) Supply Shocks
![img-7.jpeg](img-7.jpeg)
(b) Demand Shocks
![img-8.jpeg](img-8.jpeg)

Notes: This figure shows the correlation of supply (panel a) and demand (panel b) shocks based on a sign-restricted SVAR that is estimated separately for each trade. For a given trade $i$, we first estimate a sign-restricted SVAR with one lag following Uhlig (2005) and Arias et al. (2018). Using the median estimated parameter set, we then construct the implied supply and demand shock series. The top and bottom panels then shows the correlation matrix of the respective supply and demand shock series across trades. Data is weekly from 2010 to 2020. See Section 3.3 for more details.

### Page 58
Figure 7: 99th Percentile of Arbitrage Supply Shock Correlations
![img-9.jpeg](img-9.jpeg)

Notes: This figure shows the correlation of supply shock (panel a) and demand shocks (panel b) based on a sign-restricted SVAR that is estimated separately for each trade. For a given trade $i$, we first estimate a sign-restricted SVAR with one lag following Uhlig (2005) and Arias et al. (2018). We then select 10,000 random draws from the identified set of structural parameters $\Theta_{i}$ for each trade and compute the implied supply shock series. For each draw $k$, we then compute the correlation matrix $R_{k}$ of the supply shocks across trades. Panels (a), (b), and (c) show the 99th percentile of the correlation matrix for weekly shocks, monthly, and quarterly shocks, respectively. Monthly and quarterly shocks series are computed by cumulating weekly shock series. See Section 3.3 for more details.

### Page 59
Figure 8: Funding Costs and Arbitrage Correlations
![img-10.jpeg](img-10.jpeg)
(a) First Principal Component of Unsecured Arbitrages
![img-11.jpeg](img-11.jpeg)
(b) First Principal Component of Secured Arbitrages

Notes: Panel (a) of this figure shows the first principal component (PC) of unsecured arbitrage spreads and the 3-month TED spread. Panel (b) shows the first principal component of secured arbitrages, the 1-day, 1-week, and 1-month tri-party general collateral repo rate relative to the interest rate on excess reserves (IOER), and the 3-month TED spread. All data is sampled monthly. Panel (b) begins in September 2011 due to the availability of the 10- and 20-year Treasury-swap rate.

### Page 60
Figure 9: Event Study of the 2016 Money Market Reform
![img-12.jpeg](img-12.jpeg)

Notes: This figure summarizes money market fund (MMF) behavior, funding costs, and the absolute values of arbitrage spreads around the 2016 MMF reform. Compliance with the reform was required by October 2016 and so we define the reform event as occurring in October 2016. Panel A of the figure shows the time series of bank commercial paper held by MMFs. Panel B shows the average maturity-matched TED spread (LIBOR - Treasury) for the arbitrages in our sample. Denote $l$ as the maturity of the nearest-maturity LIBOR for a given trade. The maturity-matched TED spread for the trade is then defined as $\operatorname{LIBOR}(l)-\operatorname{Treasury}(l)$. For trades with tenors longer than 1 year, we set $l=1$ year based on the availability of LIBOR rates. Panel C shows the average arbitrage spread of trades that rely heavily on unsecured funding (CIP, Box, and Equity spot-futures) and those that rely more on secured funding.

### Page 61
Figure 10: Event Study of the 2012 JPM London Whale
![img-13.jpeg](img-13.jpeg)

Notes: This figure summarizes JP Morgan's (JPM) losses, the absolute value of equity spot-futures arbitrage spreads, and JPM commercial paper (CP) borrowing rates around the 2012 JPM London Whale incident. Panel (a) of the figure shows the 2012 year-to-date losses on JPM's credit derivative portfolio, as reported by the U.S. Senate investigation into the incident. Panel (b) shows the daily average arbitrage spreads of equity spot-futures, other unsecured arbitrages (CIP and Box), and secured arbitrages in 2012. The first vertical line in the plot is March 1, 2012, which is when losses began to accelerate. The second dotted line is June 13, 2012, the first day that the CEO of JPM appeared before the U.S. Senate Committee on Banking, Housing, and Urban Affairs to testify about the Whale trades. Panel (c) shows the estimated impact on equity spot-futures arbitrage spreads, relative to other unsecured arbitrages (CIP and Box). The solid lines show the point estimates from a dynamic difference-in-difference model and the dotted lines show the associated $95 \%$ confidence intervals. Panel (d) shows the estimated impact on JPM's commercial paper (CP) rate, relative to the CP rates of other large global banks. See Section 5.2 for more details.

### Page 62
Figure 11: Event Study of the Deutsche Bank's 2014 Exit from CDS Trading
![img-14.jpeg](img-14.jpeg)
(b) Impact on CDS-Bond Basis

Notes: This figure summarizes the behavior of the absolute values of arbitrage spreads around the 2014 exit of Deutsche Bank (DB) from the CDS market. Panel (a) shows the daily average arbitrage spreads of CDS-Bond arbitrage, other secured arbitrages (Treasury Futures, Treasury Swap, and TIPS-Treasury), and unsecured arbitrages in the last half of 2014 and the beginning of 2015. The first vertical line in the plot is October 1, 2014. The exact timing of DB's exit is unknown, but there are reports that they sold a large portion of their CDS portfolio to Citibank in September 2014 and they publicly announced the exit on November 17, 2014. Panel (b) plots the point estimates from a dynamic difference-in-difference model and the associated $95 \%$ confidence intervals around the event. See Section 5.3 for more details.

### Page 63
Figure 12: Fixed Income Arbitrage Hedge Funds and Secured Arbitrages
![img-15.jpeg](img-15.jpeg)

Notes: This figure plots the $t$-statistics from regressing monthly changes in the absolute values of arbitrage spreads on the lagged return of ten different fixed income hedge funds. Each hedge fund is indexed along the $x$-axis, and the $y$-axis shows the $t$-statistic from the regression. The different plot markers correspond to different strategies. We obtain returns of the ten largest Fixed Income Arbitrage Hedge Funds from Preqin. The horizontal red line corresponds to the Bonferroni-adjusted $t$-statistic that corresponds to a $5 \%$ significance threshold, which accounts for the fact that we run ten separate regressions for each strategy. Within each regression, we cluster standard errors by month.

### Page 64
Table 1: Summary Statistics for Arbitrage Spreads

|  | Mean | p50 | Std. Dev | Min | Max | AR1 | First | Last | $N$ |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| Box 6 m | 35 | 35 | 11 | 0 | 82 | 0.897 | Jan-10 | Feb-20 | 2,534 |
| Box 12 m | 34 | 34 | 10 | 0 | 87 | 0.914 | Jan-10 | Feb-20 | 2,534 |
| Box 18 m | 33 | 32 | 9 | 2 | 64 | 0.943 | Jan-10 | Feb-20 | 2,534 |
| Dow SF | 45 | 45 | 24 | 0 | 139 | 0.976 | Jan-10 | Feb-20 | 2,497 |
| NDAQ SF | 38 | 39 | 22 | 0 | 123 | 0.978 | Jan-10 | Feb-20 | 2,496 |
| SPX SF | 42 | 41 | 20 | 0 | 116 | 0.982 | Jan-10 | Feb-20 | 2,495 |
| AUD CIP | 13 | 11 | 10 | 0 | 59 | 0.933 | Jan-10 | Feb-20 | 2,541 |
| CAD CIP | 12 | 9 | 10 | 0 | 62 | 0.983 | Jan-10 | Feb-20 | 2,539 |
| CHF CIP | 51 | 47 | 27 | 11 | 198 | 0.974 | Jan-10 | Feb-20 | 2,541 |
| EUR CIP | 35 | 33 | 21 | 0 | 118 | 0.986 | Jan-10 | Feb-20 | 2,540 |
| GPB CIP | 17 | 12 | 14 | 0 | 93 | 0.986 | Jan-10 | Feb-20 | 2,540 |
| JPY CIP | 45 | 41 | 24 | 10 | 125 | 0.986 | Jan-10 | Feb-20 | 2,541 |
| NZD CIP | 11 | 11 | 6 | 0 | 36 | 0.873 | Jan-10 | Feb-20 | 2,540 |
| SEK CIP | 27 | 21 | 22 | 0 | 99 | 0.985 | Jan-10 | Feb-20 | 2,541 |
| Treasury 2Y SF | 13 | 12 | 9 | 0 | 62 | 0.930 | Jan-10 | Feb-20 | 2,347 |
| Treasury 5Y SF | 12 | 9 | 11 | 0 | 58 | 0.953 | Jan-10 | Feb-20 | 2,388 |
| Treasury 10Y SF | 18 | 15 | 15 | 0 | 113 | 0.930 | Jan-10 | Feb-20 | 2,477 |
| Treasury 20Y SF | 17 | 13 | 14 | 0 | 79 | 0.898 | Jan-10 | Feb-20 | 2,494 |
| Treasury 30Y SF | 11 | 9 | 10 | 0 | 180 | 0.655 | Jan-10 | Feb-20 | 1,734 |
| Treasury-Swap 1Y | 6 | 5 | 5 | 0 | 32 | 0.964 | Jan-10 | Feb-20 | 2,541 |
| Treasury-Swap 2Y | 10 | 9 | 6 | 0 | 34 | 0.964 | Jan-10 | Feb-20 | 2,541 |
| Treasury-Swap 3Y | 12 | 10 | 8 | 0 | 36 | 0.982 | Jan-10 | Feb-20 | 2,541 |
| Treasury-Swap 5Y | 17 | 15 | 10 | 0 | 44 | 0.984 | Jan-10 | Feb-20 | 2,541 |
| Treasury-Swap 10Y | 26 | 25 | 12 | 0 | 59 | 0.986 | Jan-10 | Feb-20 | 2,541 |
| Treasury-Swap 20Y | 35 | 35 | 15 | 8 | 70 | 0.990 | Sep-11 | Feb-20 | 2,105 |
| Treasury-Swap 30Y | 54 | 51 | 19 | 23 | 100 | 0.995 | Sep-11 | Feb-20 | 2,105 |
| TIPS-Treasury 2Y | 21 | 23 | 12 | 0 | 54 | 0.968 | Jan-10 | Feb-20 | 2,541 |
| TIPS-Treasury 5Y | 19 | 20 | 8 | 0 | 56 | 0.981 | Jan-10 | Feb-20 | 2,541 |
| TIPS-Treasury 10Y | 25 | 25 | 7 | 1 | 40 | 0.976 | Jan-10 | Feb-20 | 2,541 |
| TIPS-Treasury 20Y | 26 | 26 | 8 | 1 | 47 | 0.974 | Jan-10 | Feb-20 | 2,541 |
| CDS-Bond IG | 22 | 20 | 13 | 0 | 79 | 0.973 | Jan-10 | Feb-20 | 2,540 |
| CDS-Bond HY | 65 | 59 | 36 | 1 | 188 | 0.989 | Jan-10 | Feb-20 | 2,540 |

Notes: This table presents summary statistics on the absolute values of different arbitrage spreads. Trades are grouped by strategy (e.g., CIP). All CIP trades are for 3 month tenors. SPX, DJX, and NDAQ SF are spot-futures arbitrages for the S\&P 500, Dow Jones, and Nasdaq indices, respectively. Treasury iY SF is the Treasury spot-futures arbitrage for $i$-year maturity Treasuries. CDS-Bond denotes the average CDS-Bond basis for investment grade (IG) and high-yield (HY) firms. See Section 3.1 and Internet Appendix A. 1 for details on the construction of arbitrage trades. The column AR1 is the coefficient from an AR(1) model estimated from daily data. The columns First and Last are the month and year of the first and last observation for each series.

### Page 65
Table 2: Correlations Within and Across Arbitrage Strategies
(a) Distribution of All Pairwise Correlations

|  |  |  | $\rho_{i j}$ |  |  |  |  | $p$-value |  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| Mean | Sd | Min | p25 | p50 | p75 | Max | N | $\bar{\rho}>0.67$ | $\rho_{i j}=\rho$ |
| 0.22 | 0.30 | -0.55 | 0.00 | 0.17 | 0.42 | 0.96 | 496 | 0.00 | 0.00 |
| $90 \%$ of pairs reject $H_{0}: \rho_{i j}>0.67$ |  |  |  |  |  |  |  |  |  |

(b) Average Within and Across-Strategy Correlations

|  | CIP | Box | Equity S-F | Treasury S-F | Treasury-Swap | TIPS-Treasury | CDS-Bond |
| :-- | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| CIP | 0.35 | 0.39 | 0.27 | 0.06 | 0.36 | 0.18 | -0.00 |
| Box | 0.39 | 0.87 | 0.42 | -0.04 | 0.36 | 0.16 | -0.18 |
| Equity S-F | 0.27 | 0.42 | 0.85 | -0.05 | 0.03 | 0.03 | -0.41 |
| Treasury S-F | 0.06 | -0.04 | -0.05 | 0.20 | 0.21 | 0.04 | 0.28 |
| Treasury-Swap | 0.36 | 0.36 | 0.03 | 0.21 | 0.62 | 0.16 | 0.30 |
| TIPS-Treasury | 0.18 | 0.16 | 0.03 | 0.04 | 0.16 | 0.37 | 0.10 |
| CDS-Bond | -0.00 | -0.18 | -0.41 | 0.28 | 0.30 | 0.10 | 0.70 |

Notes: Panel A summarizes the distribution of pairwise correlations for all arbitrage strategies. The columns under $p$ value report tests of the null that the average pairwise correlation is above 0.67 and the null that all pairwise correlations are equal, respectively. Panel B shows the average pairwise correlation within and across trades in each strategy.

### Page 66
Table 3: Correlations for Arbitrages of Similar Tenors
(a) Distribution of Pairwise Correlations for Short-Tenor Trades

|  |  |  | $\rho_{i j}$ |  |  |  |  | $p$-value |  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| Mean | Sd | Min | p25 | p50 | p75 | Max | N | $\bar{\rho}>0.67$ | $\rho_{i j}=\rho$ |
| 0.19 | 0.32 | -0.41 | -0.02 | 0.15 | 0.35 | 0.89 | 120 | 0.00 | 0.00 |
| $87 \%$ of pairs reject $H_{0}: \rho_{i j}>0.67$ |  |  |  |  |  |  |  |  |  |

(b) Distribution of Pairwise Correlations for Medium-Tenor Trades

|  |  |  | $\rho_{i j}$ |  |  |  |  | $p$-value |  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| Mean | Sd | Min | p25 | p50 | p75 | Max | N | $\bar{\rho}>0.67$ | $\rho_{i j}=\rho$ |
| 0.39 | 0.28 | 0.02 | 0.21 | 0.32 | 0.50 | 0.93 | 21 | 0.00 | 0.00 |
| $81 \%$ of pairs reject $H_{0}: \rho_{i j}>0.67$ |  |  |  |  |  |  |  |  |  |

(c) Distribution of Pairwise Correlations for Long-Tenor Trades

|  |  |  | $\rho_{i j}$ |  |  |  |  | $p$-value |  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| Mean | Sd | Min | p25 | p50 | p75 | Max | N | $\bar{\rho}>0.67$ | $\rho_{i j}=\rho$ |
| 0.37 | 0.30 | -0.22 | 0.13 | 0.32 | 0.53 | 0.96 | 36 | 0.00 | 0.00 |
| $81 \%$ of pairs reject $H_{0}: \rho_{i j}>0.67$ |  |  |  |  |  |  |  |  |  |

Notes: Panel A summarizes the distribution of pairwise correlations for all arbitrage strategies with tenors of less than six months. Panel B mirrors Panel A and summarizes the distribution of pairwise correlations for all arbitrage strategies with tenors greater than 6 months and less than or equal to 3 years. Panel C shows the distribution of correlations for trades with tenor greater than 3 years, including the CDS-Bond basis strategies. The columns under $p$-value report tests of the null that the average pairwise correlation is above 0.67 and the null that all pairwise correlations are equal, respectively.

### Page 67
Table 4: Correlations in Different Subsamples
(a) Conditional on Dealer Credit Spreads

|  |  | $\rho_{i j}$ |  |  |  |  |  | $p$-value |  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| Mean | Sd | Min | p25 | p50 | p75 | Max | N | $\bar{\rho}>0.67$ | $\rho_{i j}=\rho$ |
| 0.27 | 0.28 | -0.48 | 0.08 | 0.27 | 0.46 | 0.97 | 492 | 0.00 | 0.00 |
| $86 \%$ of pairs reject $H_{0}: \rho_{i j}>0.67$ |  |  |  |  |  |  |  |  |  |

(b) During the Onset of Covid

|  |  | $\rho_{i j}$ |  |  |  |  |  | $p$-value |  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| Mean | Sd | Min | p25 | p50 | p75 | Max | N | $\bar{\rho}>0.67$ | $\rho_{i j}=\rho$ |
| 0.29 | 0.36 | -0.68 | 0.02 | 0.31 | 0.57 | 0.99 | 496 | 0.00 | 0.00 |
| $62 \%$ of pairs reject $H_{0}: \rho_{i j}>0.67$ |  |  |  |  |  |  |  |  |  |

Notes: This table summarizes the distribution of pairwise correlations for arbitrage strategies in different subsamples. In all cases, the columns under $p$-value are, respectively, based on tests of the null that average correlations are above 0.67 and the null that all pairwise correlations are equal. Panel A is only for the subsample of dates on which each arbitrage in a given pair exceeds the average 6-month CDS spread for the set of dealers who have been designated as primary dealers by the New York Federal Reserve since 2010. Panel B is based on all arbitrage strategies between March 1, 2020 through May 31, 2020.

### Page 68
Table 5: Margin Requirements for Arbitrage Strategies

|  |  | Margin Requirement (\%) |  |  |
| :-- | :--: | :--: | :--: | :--: |
| Arbitrage | Collateral | p10 | Median | p90 |
| Treasury Spot-Futures | Treasuries | 2 | 2 | 2 |
| Treasury-Swap | Treasuries | 2 | 2 | 2 |
| TIPS-Treasury | Treasuries | 2 | 2 | 2 |
| IG CDS-Bond | IG Corporate Bond | 3 | 5 | 8 |
| HY CDS-Bond | HY Corporate Bond | 3 | 8 | 15 |
| Equity Box | Equities | 5 | 8 | 15 |
| Equity Spot-Futures | Equities | 5 | 8 | 15 |
| CIP | Foreign Currency | 6 | $6-12$ | 12 |
|  |  |  |  |  |

Notes: This table shows margin requirements for each strategy. Margin data primarily come from the Federal Reserve Bank of New York's Tri-party Repo Infrastructure Reform Task Force. For currencies, we report data from central bank lending operations by the Bank of England and the European Central Bank.

### Page 69
Table 6: Arbitrage-Implied Riskless Rates and Funding Conditions

|   | Dep Variable: $\Delta$ Implied RF |  |  |  |  |  |  |  |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   | Unsecured | Secured | CIP | Box | Equity S-F | TSwap | TFut | Tips-T | CDS-Bond  |
|  $\Delta$ Treasury | $0.88^{ }$ | $0.93^{ }$ | $0.85^{ }$ | $0.99^{ }$ | $0.78^{ }$ | $0.99^{ }$ | $0.80^{ }$ | $0.95^{ }$ | $0.71^{ }$  |
|   | $(9.34)$ | $(51.66)$ | $(5.66)$ | $(16.68)$ | $(2.85)$ | $(60.79)$ | $(8.74)$ | $(35.97)$ | $(9.81)$  |
|  $\Delta$ TED | $0.49^{ }$ | 0.07 | $0.35^{ }$ | $0.53^{ }$ | $0.78^{ }$ | 0.04 | 0.15 | 0.08 | $-0.24$  |
|   | $(4.58)$ | $(1.33)$ | $(2.24)$ | $(5.26)$ | $(3.81)$ | $(0.94)$ | $(1.35)$ | $(0.77)$ | $(-1.12)$  |
|  $R^{2}$ | 0.23 | 0.66 | 0.22 | 0.57 | 0.11 | 0.95 | 0.11 | 0.88 | 0.53  |
|  $N$ | 1,694 | 2,136 | 968 | 363 | 363 | 807 | 603 | 484 | 242  |

Notes: This table shows monthly OLS regressions of changes in arbitrage-implied riskless rates on changes in maturity-matched Treasury yields and TED spreads. All variables are expressed in basis points. Define $l$ and $m$, respectively, as the maturities of the nearest-maturity LIBOR and Treasury for a given trade. The maturity-matched TED spread for the trade is then defined as $L I B O R(l)-T r e a s u r y(l)$ and the maturity-matched Treasury yield is defined as $T r e a s u r y(m) . l$ does not equal $m$ for longer-tenor trades (e.g., 30-year Treasury swap) because the maximum maturity LIBOR rate we observe is one year. $t$-statistics are reported in parentheses under point estimates and are based on standard errors clustered by strategy-month.

### Page 70
Table 7: Analysis of 2016 MMF Reform

|  | Dep Variable: Arb. Spread (bps) |  |
| :-- | :--: | :--: |
|  | $(1)$ | $(2)$ |
| $\beta$ | $11.77^{* *}$ |  |
|  | $(2.47)$ |  |
| $\beta_{j=-4}$ |  | -4.01 |
| $\beta_{j=-3}$ |  | $(-0.59)$ |
| $\beta_{j=-2}$ |  | 0.80 |
| $\beta_{j=-1}$ |  | $(0.09)$ |
| $\beta_{j=0}$ |  | 7.23 |
| $\beta_{j=1}$ |  | $(1.64)$ |
| $\beta_{j=2}$ |  | $18.03^{* *}$ |
| $\beta_{j=3}$ |  | $(2.33)$ |
| $\beta_{j \geq 4}$ |  | $18.29^{* *}$ |
|  |  | $(2.21)$ |
| $p$ | $20.70^{* *}$ |  |
| $p:$ | $16.29^{* *}$ |  |
| $p:$ | $9.26^{* *}$ |  |
| $N$ | $(2.18)$ |  |
| $p:$ | 0.00 |  |
| $p:$ | 0.00 |  |
| Adjusted $R^{2}$ | 0.59 | 0.59 |
| $N$ | 60,691 | 60,691 |

Notes: This table shows estimates of the effect of the 2016 money market reform on the absolute values of arbitrage spreads. Column (1) presents estimates of the following daily regression: $s_{i t}=\alpha_{i}+\alpha_{t}+\beta 1[i \in$ Unsecured $] \times 1[t \geq$ October2016] $+\varepsilon_{i t}$, where $s_{i t}$ is the absolute value of the arbitrage spread for trade $i$ on date $t, 1[i \in$ Unsecured $]$ is a dummy variable that equals 1 if trade $i$ relies heavily on unsecured funding (CIP, Box, and Equity spot-futures), and $1[t \geq$ October2016] is a dummy variable that equals 1 on or after October 2016. Column (2) shows estimates of the regression: $s_{i t}=\alpha_{i}+\alpha_{t}+\sum_{j=-4}^{3} \beta_{j} 1[i \in$ Unsecured $] \times 1[t=$ October2016 $+j]+\beta_{j \geq 4} 1[i \in$ Unsecured $] \times 1[t \geq$ February2017] $+\varepsilon_{i t}$. Arbitrage spreads are expressed in basis points. In column 2, we also report $p$-values for the null hypothesis that the coefficients prior to October 2016 ( $\beta_{j}$ for $j<0$ ) are equal to zero, as well as the null hypothesis that the coefficients on or after October 2016 are equal to each other ( $\beta_{j}$ are equal for $j \geq 0$ ). All regressions include fixed effects for trade $\left(\alpha_{i}\right)$ and date $\left(\alpha_{t}\right) . t$-statistics are reported in parentheses under point estimates and are based on standard errors clustered by trade and date. The estimation sample ends one year after the reform in October 2017.

### Page 71
Table 8: Arbitrage-Implied Riskless Rates and Funding Shocks to Fidelity

|  | Dep Variable: $\Delta$ Implied RF |  |  |  |  |  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: |
|  | (1) | (2) | (3) | (4) | (5) | (6) |
|  | Equity S-F | CIP/Box | Secured | Equity S-F | CIP/Box | Secured |
| $\Delta$ Treasury | $0.79^{* *}$ | $0.91^{* *}$ | $0.93^{* *}$ | $0.81^{* *}$ | $0.91^{* *}$ | $0.94^{* *}$ |
|  | (2.94) | (9.65) | (51.57) | (3.01) | (9.45) | (50.11) |
| $\Delta$ TED | $0.70^{* *}$ | $0.39^{* *}$ | 0.07 | $0.62^{* *}$ | $0.41^{* *}$ | $0.12^{*}$ |
|  | (3.56) | (3.24) | (1.35) | (3.16) | (3.20) | (1.95) |
| Fidelity IPrime Flows | $-0.55^{* *}$ | $-0.14^{*}$ | 0.01 | $-1.09^{* *}$ | 0.04 | 0.27 |
|  | $(-3.86)$ | $(-1.84)$ | (0.34) | $(-2.25)$ | (0.12) | (1.38) |
| Estimation | OLS | OLS | OLS | IV | IV | IV |
| First-Stage $F$ |  |  |  | 9 | 15 | 30 |
| $R^{2}$ | 0.15 | 0.31 | 0.66 | 0.11 | 0.30 | 0.65 |
| $N$ | 363 | 1,331 | 2,136 | 357 | 1,309 | 2,099 |

Notes: This table presents regression estimates of monthly changes in arbitrage-implied riskless rates on flows out of Fidelity IPrime money market funds (MMFs). The first three columns show OLS estimates, and the last three columns show IV estimates, where the instrument is net flows into all Fidelity MMFs interacted with the Fidelity IPrime share of assets, lagged by 3 months. We also include the change in the maturity-matched Treasury yield and the change in the maturity-matched TED spread. Define $l$ and $m$, respectively, as the maturities of the nearest-maturity LIBOR and Treasury for a given trade. The maturity-matched TED spread for the trade is then defined as $\operatorname{LIBOR}(l)-\operatorname{Treasury}(l)$ and the maturity-matched Treasury yield is defined as $\operatorname{Treasury}(m) . l$ does not equal $m$ for longer-tenor trades (e.g., 30-year Treasury swap) because the maximum maturity LIBOR rate we observe is one year. See Section 4.3 for details on instrument construction. Columns (1) and (4) show estimates using only Equity spot-futures, columns (2) and (5) show estimates for other unsecured trades (CIP and Box), and columns (3) and (6) show estimates for all secured trades. All implied riskless rates are in basis points and flows are in percentage points. $t$-statistics are reported in parentheses under point estimates and are based on standard errors clustered by strategy-month. The $F$-statistic from the first-stage of the IV is reported at the bottom of the table.

### Page 72
Table 9: Trading Behavior in U.S. Futures Markets

|   | Gross Share (\%) |  |  | Position Size (\% of Net) |  |  | Earns Arbitrage (\% of days) |  |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   | Dealers | HFs | Asset Mgrs | Dealers | HFs | Asset Mgrs | Dealers | HFs | Asset Mgrs  |
|  2-Year Treasury Notes | 11 | 37 | 38 | 13 | 33 | 30 | 46 | 63 | 34  |
|  5-Year Treasury Notes | 12 | 30 | 48 | 14 | 32 | 38 | 62 | 66 | 26  |
|  10-Year Treasury Notes | 12 | 30 | 48 | 12 | 30 | 31 | 58 | 74 | 32  |
|  20-Year Treasury Bonds | 12 | 25 | 56 | 25 | 14 | 43 | 37 | 45 | 62  |
|  30-Year Treasury Bonds | 16 | 29 | 52 | 18 | 32 | 45 | 46 | 46 | 23  |
|  S\&P 500 Index | 21 | 30 | 41 | 27 | 18 | 45 | 88 | 98 | 1  |
|  Nasdaq Index | 35 | 31 | 29 | 41 | 19 | 29 | 80 | 29 | 14  |
|  Dow Jones Industrial Average | 52 | 32 | 11 | 45 | 29 | 15 | 94 | 8 | 9  |
|  Average Treasury | 13 | 30 | 48 | 16 | 28 | 37 | 50 | 58 | 35  |
|  Average Equity | 36 | 31 | 27 | 38 | 22 | 30 | 87 | 45 | 8  |

Notes: This table summarizes the weekly positions of dealers, hedge funds, and asset managers using weekly reports on the Commitments of Traders provided by the Commodity Futures Trading Commission (CFTC). We use hedge funds (HFs) to designate traders who classified by the CFTC as "leveraged funds". Gross positions by type are computed as the sum of long, short, and spread positions. Gross share is the percent of total gross positions outstanding across all reporting agents. The columns listed under Position Size (\% of Net) are computed as follows: (i) compute the net position of each type $i$ in week $t$ as $N e t_{i t}=$ Long $_{i t}-$ Short $_{i t}$; (ii) compute the total net outstanding of the market $N e t_{t}$ by summing $\left|N e t_{i t}\right|$ across all reporting agents; and (iii) Position Size (\% of Net) is then $\left|N e t_{i t}\right| / N e t_{t}$. We include the CFTC's "Other Reporting" agents in our calculation of gross and net outstanding, but do not report their share in the table. This means that shares in the table will not sum to 100. The Gross Share and Position Size are weekly averages for each contract. The columns under Earns Arbitrage shows the percent of days on which the net position of the type would earn the observed arbitrage spread.

### Page 73
Table 10: Fixed Income Arbitrage Hedge Fund Returns and Arbitrage Spreads

|  | Dep Variable: $\Delta$ Arbitrage Spread |  |  |  |  |  |  |  |  |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
|  | Unsecured | Secured | CIP | Box | Equity S-F | TSwap | TFut | Tips-T | CDS-Bond |
| FI Arb HF Return $_{t-1}$ | 0.00 | $-0.66^{ }$ | $-0.10$ | $-0.34$ | 0.64 | $-0.40^{ }$ | $-0.44$ | $-0.49$ | $-2.33^{ }$ |
|  | $(0.01)$ | $(-3.04)$ | $(-0.16)$ | $(-0.56)$ | $(0.65)$ | $(-2.45)$ | $(-0.89)$ | $(-1.09)$ | $(-2.72)$ |
| $R^{2}$ | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.02 | 0.00 | 0.01 | 0.06 |
| $N$ | 1,694 | 2,136 | 968 | 363 | 363 | 807 | 603 | 484 | 242 |

Notes: This table shows regressions of monthly changes in the absolute values of arbitrage spreads on the lagged aggregate return of hedge funds that specialize on fixed income arbitrage, as measured by Barclay's Aggregate Fixed Arbitrage Index. The aggregate return series is standardized to have mean zero and unit variance. The columns Unsecured and Secured pool strategies based on whether they rely on unsecured funding (CIP, Equity Spot-Futures, and Box). The remaining columns run the regression by strategy. Standard errors are clustered by strategy-month.