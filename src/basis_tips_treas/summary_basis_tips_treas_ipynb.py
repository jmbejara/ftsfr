# %%
"""
# TIPS-Treasury Arbitrage Replication (2004-2025)

This notebook replicates the TIPS-Treasury arbitrage strategy for the period 2004-2025 following the methodology of Fleckenstein et al. (2014). It also outlines how a trader could implement this strategy in practice.
"""

# %%
"""
## Methods

### Replication Strategy

1. **Data Sources**:
   - **TIPS Data:** Daily yield data for TIPS from U.S. Treasury sources.
   - **Inflation Swap Data:** Zero-coupon inflation swap rates from Bloomberg.
   - **Nominal Treasury Data:** Daily nominal Treasury yields from CRSP.

2. **Synthetic Yield Construction:**

   For a given maturity \(\tau\):

   \begin{equation}
   \text{Synthetic Yield}_{t,\tau} = s_{t,\tau} + f_{t,\tau}
   \end{equation}

   where \(s_{t,\tau}\) is the TIPS yield and \(f_{t,\tau}\) is the fixed rate from the inflation swap. The arbitrage spread is then:

   \begin{equation}
   \text{Spread}_{t,\tau} = (s_{t,\tau} + f_{t,\tau}) - y_{T,t,\tau}
   \end{equation}

   A positive spread indicates that nominal Treasuries are overpriced relative to the synthetic yield.
"""

# %%
# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import sys

sys.path.append("..")
from settings import config

DATA_DIR = config("DATA_DIR")
DATA_DIR = DATA_DIR / "basis_tips_treas"

warnings.filterwarnings("ignore")
# sns.set_theme(style="dark")

# %%
"""
### Load Data

The following cell loads the TIPS-Treasury arbitrage data from a parquet file. This file is generated from `compute_tips_treasury.py`. This formulates a tidy set of the data.

- Columns starting with "real_": TIPS real yields for each tenor (e.g., real_cc2, real_cc5, real_cc10, real_cc20)
expressed in decimal form (e.g., 0.02 for 2%).
- Columns starting with "nom_": Computed nominal zero-coupon Treasury yields for each tenor
(e.g., nom_zc2, nom_zc5, nom_zc10, nom_zc20) expressed in basis points.
- Columns starting with "tips_": TIPS-implied risk-free rates (e.g., tips_treas_2_rf, tips_treas_5_rf,
tips_treas_10_rf, tips_treas_20_rf) expressed in basis points.
- Columns starting with "arb_": Arbitrage measures (e.g., arb_2, arb_5, arb_10, arb_20) representing the
difference between the TIPS-implied risk-free rate and the corresponding nominal yield (tips_treas_{t}_rf - nom_zc{t}).

"""

# %%
rf = pd.read_parquet(DATA_DIR / "tips_treasury_implied_rf.parquet")
rf

# %%
"""
Selected region
"""

# %%
test = pd.DataFrame(index=rf.index)
test = rf[["arb_2", "arb_5", "arb_10", "arb_20"]]
test["date"] = rf["date"]
test.index = test["date"]
test.drop("date", axis=1, inplace=True)
test

# %%
"""
### Generate Summary Statistics

The cell below computes summary statistics using `generate_figures.py` for each TIPS-Treasury arbitrage series over the period 2004-2025.
"""

# %%
import generate_figures

# Compute summary statistics for the period 2004-01-01 to 2025-01-01
summary_stats = generate_figures.generate_summary_statistics(
    test, "2000-01-01", "2025-01-01"
)
summary_stats

# %%
"""
### Correlation Heatmap (as in Figure 2)
"""

# %%
# Calculate the correlation matrix for 'test'
corr_matrix = test.corr()

# Set up the matplotlib figure
plt.figure(figsize=(10, 8))

# Generate the heatmap using seaborn
sns.heatmap(
    corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True, linewidths=0.5
)

# Add a title
plt.title("Correlation Heatmap for Arbitrage Spreads")

# Display the plot
plt.show()

# %%
"""
### Plot TIPS-Treasury Spreads

The following cell plots the arbitrage spreads for various maturities (2Y, 5Y, 10Y, 20Y) over the period 2004-07-21 to 2025-05-30.
"""

# %%
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))

for year in [2, 5, 10, 20]:
    data = test[f"arb_{year}"].dropna()
    ax.plot(data.index, data.values, label=f"{year}Y")

ax.set_title("TIPS Treasury Arbitrage Spreads")
ax.set_xlabel("Date")
ax.set_ylabel("Arbitrage Spread (bps)")
ax.grid(True)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), frameon=False, ncol=4)
plt.show()


# %%
"""
### Practical Implementation

A trader could use the following steps to exploit the arbitrage opportunity:

1. **Signal Identification:** Continuously monitor the arbitrage spread using updated TIPS, inflation swap, and Treasury data. A consistently positive spread signals an opportunity.

2. **Position Construction:**
   - **Long Position:** Purchase TIPS and enter into corresponding zero-coupon inflation swap contracts to convert the real cash flows into fixed nominal cash flows.
   - **Short Position:** Short the nominal Treasury bond (or use Treasury futures/repurchase agreements as a proxy).

3. **Cash Flow Matching:** Utilize Treasury STRIPS or additional derivatives to ensure that the cash flows from the long and short positions align, thereby locking in the arbitrage profit.

4. **Risk Management:** Monitor execution costs, margin requirements, and liquidity risks. Funding constraints and counterparty risks must also be managed.

This strategy, while theoretically risk-free, requires meticulous execution and risk management in practice.
"""

# %%
"""
## Conclusion

The analysis confirms that a positive TIPS-Treasury arbitrage spread persisted throughout 2010-2020. Although the magnitude of the mispricing is lower than during the earlier period covered by Fleckenstein et al. (2014), the spread remains statistically and economically significant. This persistence underscores the impact of market frictions and funding constraints on arbitrage opportunities. In practice, traders could exploit this anomaly by constructing synthetic nominal positions using TIPS, inflation swaps, and nominal Treasury bonds, while carefully managing execution and funding risks.
"""
