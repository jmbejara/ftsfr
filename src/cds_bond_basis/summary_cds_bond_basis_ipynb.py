# %%
"""
# Cleaning Summary: CDS Bond Basis

## Paper Introduction

This construction is based upon the structure proposed by Siriwardane, Sunderam, and Wallen in Segmented Arbitrage (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3960980). The original paper studies the concept of implied arbitrage returns in many different markets. If markets were truly frictionless, we would expect there to be perfect correlation between all of the arbitrage returns. This is because efficient capital allocation would dictate that capital be spent where the best opportunity is, thus dictating the arbitrage opportunites we calculate via different product would have correlating rates as capital would be allocated to a different source if the arbitrage opportunity looks more attractive.

## CDS Par Spread Returns

### Spread Construction

In the following notebook, we will walk through the steps to constructing the implied arbitrage found in the CDS and corporate bond market as specified in the Appendix of the paper (https://static1.squarespace.com/static/5e29e11bb83a3f5d75beb17d/t/654d74d916f20316049a0889/1699575002123/Appendix.pdf). The authors define the CDS basis ($CB$) as

$$
CB_{i, t, \tau} = CDS_{i, t, \tau} - FR_{i, t, \tau}
$$

where:
- $FR_{i, t, \tau}$ = time $t$ floating rate spread implied by a fixed-rate corporate bond issued by firm $i$ at tenor $\tau$
- $CDS_{i, t, \tau}$ = time $t$ Credit Default Swap (CDS) par spread for firm $i$ with tenor $\tau$

A negative basis implies an investor could earn a positive arbitrage profit by going long the bond and purchasing CDS protection. The investor would pay a lower par spread than the coupon of the bond itself and then receive value from the default.

The value of $FR$ is substituted by the paper with **Z-spread** which we also modify in our construction. We will go into the substitution in detail later.

The value of $CDS$ is interpolated by the authors using a cubic spline function.

### Implied Risk Free Return

Given the CDS spread from above, traditional construction of a risk free rate for implied arbitrage implied the following return.

$$
rfr^{CDS}_{i, t, \tau} = y_{t, \tau} - CB_{i , t, \tau}
$$

where:
- $y_{t, \tau}$ = maturity matched treasury yield at time $t$

The risk free rate then can be seen as the treasury yield in addition to the basis recieved when executing the CDS basis trade (investor benefits from negative basis).

## Key Filters when selecting viable data as specified in Segmented Arbitrage

1. Include only Senior Unsecured Debt issued in USD by US firms with valid ISIN
2. Include only fixed rate bonds with maturity between 1 and 10 years
3. Include only bonds with outstanding principle of at least 100,000 USD
4. Exclude putable and convertible bonds
5. Exclude bonds trading at less than half of face value
6. Include only assets on a certain date if a cubic spline of the CDS set is possible
- There must be 2 or more CDS products corresponding to a corporate bond on a certain day for parspread cubic spline to be possible

"""

# %%
import sys
from pathlib import Path

sys.path.insert(0, "../../src")
sys.path.insert(0, "./src")

import pandas as pd
import pull_open_source_bond
import pull_wrds_markit
from merge_cds_bond import *
from process_final_product import *

from settings import config

# %load_ext autoreload
# %autoreload 2

# %%
DATA_DIR = Path(config("DATA_DIR"))

# %%
"""
## Z-Spread (Zero-Volatility Spread)

**Mathematical definition**

For a bond with cash-flows $CF_t$ at times $t=1,\dots,N$ and Treasury spot rates $s_t$,

$$
P = \sum_{t=1}^{N} \frac{CF_t}{\bigl(1+s_t+Z\bigr)^t}.
$$

The constant $Z$ that solves this equation is the **Z-spread**.

**Intuition**

$Z$ is the uniform extra yield added to every point on the risk-free spot curve so that the discounted cash-flows equal the bond’s dirty price $P$. It compensates investors for credit and liquidity risk relative to Treasuries.


### Link to Yield-to-Maturity

Setting the Z-spread pricing equation equal to the standard YTM equation gives

$$

\sum_{t=1}^{N}\frac{CF_t}{(1+y)^t}
=\sum_{t=1}^{N}\frac{CF_t}{\bigl(1+s_t+Z\bigr)^t}
\tag{A1}
$$

where $y$ is the bond’s yield-to-maturity.  Except for the trivial flat-curve case ($s_t=s$), (A1) has no algebraic solution—$y$ or $Z$ must be found numerically.


### Continuous-Compounding Identity

Rewrite discounts as $e^{-r t}$.  With PV-weights

$$
w_t=\frac{CF_t\,e^{-(s_t+Z)t}}{P},\qquad\sum_{t}w_t=1,
$$

equation (A1) yields the convenient mean-value relationship

$$
y \;=\; \sum_{t=1}^{N} w_t\,(s_t+Z)\tag{A2}
$$

Thus YTM is the PV-weighted average of the spot rates plus the Z-spread.


### Practical Proxy: YTM Credit Spread

Analysts often approximate $Z$ with the **credit spread**

$$
\Delta y = y_{\text{bond}} - y_{\text{Treasury-DM}},
$$

where $y_{\text{Treasury-DM}}$ is the yield on a Treasury portfolio matched to the bond’s (modified) duration.

**Why it works**

1. A small parallel shift $Z$ applied to all discount rates changes price by $-D_{\text{mod}}\;Z$.  For modest spreads, this produces nearly the same price change as replacing the spot curve with a single rate shift $\Delta y$.  
2. Duration-matching the Treasury benchmark neutralises curve-shape effects, so $\Delta y$ isolates the average extra yield attributable to credit/liquidity risk.  
3. Empirically, $\Delta y$ tracks $Z$ closely for plain-vanilla, option-free bonds, making it a “good-enough” proxy when full spot-curve data or iterative Z-spread calculations are impractical.

**Note**

Z-spread is said to be populated by Markit in the CDS dataset but during the reconstruction process we found no proxy. Thus, we chose our own construction.

"""

# %%
"""
## Data Overview
"""

# %%


corp_bonds_data = pull_open_source_bond.load_corporate_bond_returns(
    data_dir=DATA_DIR / "cds_bond_basis"
)
red_data = pd.read_parquet(DATA_DIR / "cds_bond_basis" / "RED_and_ISIN_mapping.parquet")
cds_data = pull_wrds_markit.load_cds_data(data_dir=DATA_DIR / "cds_bond_basis")

# %%
corp_bonds_data.info()

# %%
"""
As a proxy for the Z-spread, we will use the credit spread between the bond's yield and the yield on a Treasury portfolio matched to the bond's (modified) duration. In this data,

 - "cs" is the market-microstructure-noise-biased credit spread
 - "CS" is the credit spread that has been adjusted for the market-microstructure noise. We will use this as our proxy for the Z-spread.
 - "BOND_YIELD" is the corporate bond yield that has been adjusted for market-microstructure noise. We will use "BOND_YIELD" - "CS" as our treasury yield during the period.
"""

# %%
corp_bonds_data.describe()

# %%
"""
# Step 1: Merge the Redcodes of firms on to the corporate bonds.

The code for it is in **merge_cds_bond.py** in the function **merge_redcode_into_bond_treas**. The more specific inputs are within the function itself.

Given CDS tables record issuers of the Credit Default Swaps using Redcode and the bond tables only had CUSIPs, we needed to conduct a merge using a redcode-CUSIP matching table to the end product of step 1.2 for CDS processing later on.

We will pull the results without processing for CDS implied arbitrage returns. 
"""

# %%
corp_red_data = merge_red_code_into_bond_treas(corp_bonds_data, red_data)

# %%
corp_red_data.head()

# %%
corp_red_data.describe()

# %%
"""
# Step 2: CDS data pull and CDS data processing

## Step 2.1: CDS data pull

The CDS data pull will be filtered using the redcodes from the above **bond_redcode_merged_data** dataframe, ensuring that only the firms that have corporate bond data are pulled from the CDS table. Daily CDS data is being pulled initially, 

resulting in a mismatch in amount compared to corporate bonds. The data will be reduced during the merge process as the corporate bonds are indicated by monthly data.

## Step 2.2: CDS data processing

Let's first observe the data to see what we are working with:

"""

# %%
cds_data.info()

# %%
cds_data.describe()

# %%
"""
The CDS data has a flaw: the **tenor** is displayed as opposed to **maturity date** which would allow for more accurate cubic splines of the par spread. To approximate the correct number of days, we use tenor as is and annualize. 

For example, if the tenor is $3Y$, the number of days that we use to annualize is $3 \times 365 = 1095$. 

In our processing function **merge_cds_bond**, we grab the **redcode, date** tuples for which we can generate a viable cubic spline function, filter the bond and treasury dataframe (output of step 1). 

Then, we use the days between the **maturity** and the **date** for each corporate bond as the input for the cubic spline function for par spread generation. Thus, our final product contains corporate bonds, duration matched treasury rates, and implied 

CDS par spreads as specified by the Segmented Arbitrage paper.
"""

# %%
final_data = merge_cds_into_bonds(corp_red_data, cds_data)

# %%
final_data.head()

# %%
"""
# Step 3: Processing

Revisiting the original model:

$$
CB_{i, t, \tau} = CDS_{i, t, \tau} - FR_{i, t, \tau}
$$

where:
- $FR_{i, t, \tau}$ = time $t$ floating rate spread implied by a fixed-rate corporate bond issued by firm $i$ at tenor $\tau$
    - We use "CS" from the original corporate bonds table for this
- $CDS_{i, t, \tau}$ = time $t$ Credit Default Swap (CDS) par spread for firm $i$ with tenor $\tau$
    - CDS parspread is constructed using a Cubic Spline

$$
rfr^{CDS}_{i, t, \tau} = y_{t, \tau} - CB_{i , t, \tau}
$$

where:
- $y_{t, \tau}$ = duration matched treasury yield at time $t$
    - this is constructed via the "BOND_YIELD" - "CS" in the original corporate bond table

**Note: Filtering**

We threw out some unreasonable data for the absolute rf values exceeding 1 (risk free annual return of 100%). 
"""

# %%
processed_final_data = process_cb_spread(final_data)

# %%
processed_final_data.head()

# %%
processed_final_data.info()

# %%
processed_final_data.describe()

# %%
"""
# Step 4: Results

Below is a graph of 3 categories of bonds where certain ETFs may include both IG and Junk (HY) bonds.

Rating 0: Only junk bonds (HY)

Rating 1: Only IG bonds

Rating 2: Both IG and Junk bonds (HY) in the product
"""

# %%
generate_graph(processed_final_data)
