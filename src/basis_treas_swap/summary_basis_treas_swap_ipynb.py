# %%
"""
# Recreating the Treasury Swap Arbitrage Analysis from "Segmented Arbitrage"

This notebook briefly summarises our process of recreating the Treasury-Swap arbitrage spread plot from the Siriwardane, Sunderam, and Wallen (2023) paper "Segmented Arbitrage."


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
### Data Collection from Bloomberg
"""

# %%
"""
We first pull the required data from Bloomberg using xbbg and other libraries. We also perform a small preprocessing step.
"""

# %%
from pull_bloomberg import *

raw_df_t = pull_raw_tyields()
raw_df_s = pull_raw_syields()
clean_df_t = clean_raw_tyields(raw_df_t)
clean_df_s = clean_raw_syields(raw_df_s)

# %%
"""
### Calculating Arbitrage Spreads
"""

# %%
"""
Now that we have the data, we calculate the arbitrage spread. The assumption here is that if this value goes negative, then this is an arb. We pay fixed in the swap agreement and receive the floating rate. Then, we purchase a treasury on repo, meaning that we are receiving the treasury rate and paying a floating repo rate. Thus, we get paid T_rate - Swap_rate + Swap_floating - Repo_Floating. Hence, this is not a true arbitrage unless you are guaranteed that you can secure 3mo treasury repos at a lower floating rate than you would receive in the swap (most likely SOFR).
"""

# %%
from calc_swap_spreads import *

calc_df = calc_swap_spreads(clean_df_t, clean_df_s)

# %%
"""
### Recreating the Paper's Plot
"""

# %%
"""
Once we have the data, we use a simple plotting function to plot the data and save it in "\\..\\_output". This plot measures the arbitrage opportunity, as anywhere the series is negative, the treasury super replicates the swap.
"""

# %%
from settings import config
from pathlib import Path
from plot_figure import *

output_dir = Path(config("OUTPUT_DIR"))
end_date = pd.Timestamp(config("END_DATE")).date()

plot_figure(
    calc_df, os.path.join(output_dir, "replicated_swap_spread_arb_figure.png"), end_date
)

# %%
"""
### Extending the Plot with Recent Data

Ever since the paper's publishing, more data has been added to Bloomberg which can be used to extend the plot recreated.
"""

# %%
plot_figure(calc_df, os.path.join(output_dir, "updated_swap_spread_arb_figure.png"))

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
We also generate a set of plots that shows the two rates over the extended period. In theory, since the treasury super replicates the swap, the treasury rate should be lower than the swap rate across these periods.
"""

# %%
replicated_df = supplementary_main()
plot_supplementary(replicated_df, os.path.join(output_dir, "replication_figure.png"))

# %%
"""
#### Table
"""

# %%
"""
We generate a table the represents the average swap-treasury spread over the extended period. Again, negative values represent arbitrage opportunities.
"""

# %%
print(sup_table(replicated_df).to_markdown())

# %%
"""
## Conclusion

This code has been able to approximately recreate the figure in the paper and also create an extended plot. We supplement these plots with a table of the means of the spreads, and a plot displaying how the curves(treasury and swap yields) follow each other for different treasury time periods.
"""