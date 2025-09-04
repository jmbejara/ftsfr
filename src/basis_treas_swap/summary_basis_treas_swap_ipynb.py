# %%
from pathlib import Path
import os
import sys
import asyncio
import pandas as pd
import sys
sys.path.append("..")

from settings import config
import pull_bbg_treas_swap
from calc_swap_spreads import calc_swap_spreads
from plot_figure import (
    plot_figure,
    plot_supplementary,
    DEFAULT_START_DATE,
    REPLICATION_END_DATE,
)
from supplementary import replication_df

DATA_DIR = config("DATA_DIR")
DATA_DIR = DATA_DIR / "basis_treas_swap"

# Ensure Windows uses a selector event loop to avoid ZMQ RuntimeWarning during nbconvert
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

# %%
"""
# Recreating the Treasury Swap Arbitrage Analysis from "Segmented Arbitrage"

This notebook summarizes the process of recreating the Treasury-Swap arbitrage spread plot from Siriwardane, Sunderam, and Wallen (2023), "Segmented Arbitrage."
"""

# %%
"""
## Treasury Swap Arbitrage Concept
"""

# %%
"""
Treasury Swap arbitrage measures the difference between the fixed rate on overnight indexed swaps (OIS) and Treasury yields of matching maturities. This spread captures violations of the law of one price in fixed income markets. As the paper shows, these arbitrage opportunities persist due to funding and balance sheet segmentation among financial intermediaries.
"""

# %%
"""
The core logic of this arbitrage opportunity is that when the treasury yield and the swap rates are the same at identical tenors, holding the treasury on a repo super replicates receiving fixed in the swap. This is because the securitized floating repo rate is assumed to be less than the floating rate paid in a swap. Hence, if one were to hold a treasury on repo and pay fixed in a swap when the treasury yields exceeded the swap rates, they would be receiving a higher fixed rate than they are paying, and would receive a higher floating rate than they are paying also, implying an arbitrage.
"""

# %%
"""
### Data Loading
"""

# %%
"""
In accordance with the project rules, this notebook only loads data from disk.
The raw pull from Bloomberg happens once in the pull step; the cleaned files are
saved to disk and loaded here for analysis and plotting.
"""

# %%
"""
### Calculating Arbitrage Spreads
"""

# %%
"""
Load cleaned Treasury and Swap yields from disk and compute the arbitrage spreads.
"""

# %%
tyields = pull_bbg_treas_swap.load_tyields(data_dir=DATA_DIR)
syields = pull_bbg_treas_swap.load_syields(data_dir=DATA_DIR)
calc_df = calc_swap_spreads(tyields, syields)

# %%
"""
### Recreating the Paper's Plot
"""

# %%
"""
Once we have the spreads, we plot the replicated and updated figures and save them in the output directory.
"""

# %%
output_dir = Path(config("OUTPUT_DIR"))
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))

for year in [1, 20, 2, 30, 3, 5, 10]:
    data = calc_df[f"Arb_Swap_{year}"].dropna()
    ax.plot(data.index, data.values, label=f"{year}Y")

ax.set_title("Treasury-Swap Arbitrage Spreads")
ax.set_xlabel("Date")
ax.set_ylabel("Arbitrage Spread (bps)")
ax.grid(True)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), frameon=False, ncol=7)

plt.savefig(os.path.join(output_dir, "treasury_swap_arbitrage_spreads.png"))
plt.show()

# %%
"""
### Extending the Plot with Recent Data

Ever since the paper's publishing, more data has been added to Bloomberg which can be used to extend the plot recreated.
"""
# %%
"""
### Supplementary
"""

# %%
"""
#### Plots
"""

# %%
"""
Generate supplementary plots of Treasury versus Swap rates over time.
"""

# %%
replicated_df = replication_df(tyields, syields)
plot_supplementary(
    replicated_df,
    os.path.join(output_dir, "replication_figure.png"),
    start_date=DEFAULT_START_DATE,
    end_date=None,
)

# %%
"""
#### Table
"""

# %%
"""
We generate a small summary table of the mean arbitrage spread by tenor.
"""

# %%
years = [1, 2, 3, 5, 10, 20, 30]
means = calc_df[[f"Arb_Swap_{y}" for y in years]].mean()
means.index = [f"Arb Swap {y}" for y in years]
pd.DataFrame(means, columns=["Mean(bps)"])

# %%
"""
## Conclusion

This code has been able to approximately recreate the figure in the paper and also create an extended plot. We supplement these plots with a table of the means of the spreads, and a plot displaying how the curves(treasury and swap yields) follow each other for different treasury time periods.
"""
