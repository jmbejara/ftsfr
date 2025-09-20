# %%
"""
### Treasury spot-futures basis: overview

- The basis is the difference between the futures-implied risk-free rate on the deferred Treasury futures contract and the corresponding USD OIS rate aligned to the contract's time-to-maturity.
- Positive basis means futures imply higher financing than OIS.

What follows:
- Plot of our computed basis for 2Y, 5Y, 10Y, 20Y, 30Y.
- Side-by-side overlay with Siriwardane et al.'s published series for an eyeball check.

"""

# %%
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
import sys
import asyncio

sys.path.append("..")
from settings import config
from calc_basis_treas_sf import load_treasury_sf_output
import load_bases_data

DATA_DIR = config("DATA_DIR")

# Ensure Windows uses a selector event loop to avoid ZMQ RuntimeWarning during nbconvert
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

DATA_DIR = DATA_DIR / "basis_treas_sf"

tenors = [
    "Treasury_SF_2Y",
    "Treasury_SF_5Y",
    "Treasury_SF_10Y",
    "Treasury_SF_20Y",
    "Treasury_SF_30Y",
]

# %%
df_mine = load_treasury_sf_output(data_dir=DATA_DIR).sort_values("Date")
tenors_plot_mine = [c for c in tenors if c in df_mine.columns]
fig, ax = plt.subplots(figsize=(12, 6))

for col in tenors_plot_mine:
    data = df_mine.set_index("Date")[col]
    ax.plot(
        data.index, data.values, label=col.replace("Treasury_SF_", "").replace("Y", "Y")
    )

ax.set_title("Treasury Spot-Futures Basis")
ax.set_xlabel("Date")
ax.set_ylabel("Basis (bps)")
ax.grid(True)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), frameon=False, ncol=5)

plt.tight_layout()
plt.show()

# %%
df_ref = load_bases_data.load_combined_spreads_wide(
    data_dir=DATA_DIR, raw=False, rename=True
)
df_ref = df_ref.reset_index().rename(columns={"date": "Date"})
df_ref["Date"] = pd.to_datetime(df_ref["Date"]).dt.tz_localize(None)
ref_map = {
    "Treasury_SF_02Y": "Treasury_SF_2Y",
    "Treasury_SF_05Y": "Treasury_SF_5Y",
    "Treasury_SF_10Y": "Treasury_SF_10Y",
    "Treasury_SF_20Y": "Treasury_SF_20Y",
    "Treasury_SF_30Y": "Treasury_SF_30Y",
}
df_ref = df_ref.rename(columns=ref_map)
tenors_overlay = [c for c in tenors if c in df_ref.columns and c in df_mine.columns]

fig, axes = plt.subplots(
    len(tenors_overlay), 1, figsize=(12, 2.6 * len(tenors_overlay)), sharex=True
)
if len(tenors_overlay) == 1:
    axes = [axes]

for i, col in enumerate(tenors_overlay):
    ax = axes[i]
    df_mine.set_index("Date")[col].plot(ax=ax, label="FTSFR Replication", color="C0")
    df_ref.set_index("Date")[col].plot(
        ax=ax, label="Siriwardane et al.", color="C1", alpha=0.7
    )
    ax.set_title(col)
    ax.set_ylabel("bps")
    ax.grid(True)

axes[0].legend()
plt.xlabel("")
plt.tight_layout()
plot_path = DATA_DIR / "treasury_sf_basis_overlay_siriwardane.png"
fig.savefig(plot_path, dpi=300, bbox_inches="tight")
# Provide accessible alt text for the overlay figure
display(
    fig,
    metadata={
        "image/alt": "Overlay of Treasury Spot-Futures Basis: FTSFR Replication vs. Siriwardane et al., by tenor (2Y, 5Y, 10Y, 20Y, 30Y)."
    },
)

# %%
"""
### How the Treasury spot-futures basis is computed (summary)

Inputs loaded in `calc_basis_treas_sf.py`:
- `treasury_df.parquet`: contract strings, implied repo rates, volumes, prices for near/deferred contracts.
- `ois.parquet`: USD OIS tenors (1W, 1M, 3M, 6M, 1Y).
- `last_day.parquet`: month/year → settlement day mapping for futures.

Computation outline:
- Parse contract strings (e.g., "DEC 21") to month/year; merge settlement day; build a maturity date and compute TTM in days for each contract.
- Interpolate OIS to the contract's TTM using a piecewise-linear rule across 1W/1M/3M/6M/1Y.
- Define basis for the deferred contract: `(Implied_Repo_2 − OIS_2) × 100` bps.
- Clean: flag outliers via a ±45-day rolling MAD by tenor; set flagged values to NaN; require volume in the deferred contract.
- Pivot long → wide; produce series `Treasury_SF_2Y, 5Y, 10Y, 20Y, 30Y`; forward-fill small gaps.

See `calc_basis_treas_sf.py` functions for details: `parse_contract_date`, `interpolate_ois`, `rolling_outlier_flag`, `compute_treasury_long`, `compute_treasury_output`. 


"""

# %%


# %%
"""
### What is the Treasury spot-futures basis trade?

- **Idea**: Exploit deviations between the financing rate implied by deferred Treasury futures and the USD OIS curve for the same maturity horizon.
- **Mechanics (high level)**: Construct a hedged “cash-and-carry” or “reverse cash-and-carry” using the deliverable Treasury bond (or basket) versus the futures. Direction depends on the sign of the basis and carry considerations.
- **Signal**: Our series `Treasury_SF_2Y/5Y/10Y/20Y/30Y` measure `(futures-implied rf − OIS)` in bps for the deferred contract. Persistent positive values suggest futures-implied financing is rich to OIS; negative values suggest the opposite.
- **Caveats**: Delivery options, cheapest-to-deliver dynamics, funding frictions, margining, and liquidity constraints matter; the series is an indicator, not a PnL.


"""

# %%
