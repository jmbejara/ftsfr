# %%
"""
# CDS-Bond Basis: Construction and Comparison to Siriwardane, Sunderam, Wallen (2021)

This notebook documents the construction of the CDS-bond basis used in the
ftsfr panel and compares the resulting time series to Figure A1g of
Siriwardane, Sunderam, and Wallen (2021),
[*Segmented Arbitrage*](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3960980).

## Definition

The CDS-bond basis (or arbitrage spread) for firm $i$ at date $t$ and tenor
$\\tau$ is

$$
CB_{i,t,\\tau} = CDS_{i,t,\\tau} - FR_{i,t,\\tau}
$$

where $CDS_{i,t,\\tau}$ is the maturity-matched par CDS spread and
$FR_{i,t,\\tau}$ is the floating-rate spread implied by the bond, proxied by
its Z-spread relative to the fitted Treasury NSS curve.

We construct $FR_{i,t,\\tau}$ as a true Z-spread by solving the no-arbitrage
pricing equation against the Nelson-Siegel-Svensson Treasury curve fitted on
the CRSP daily Treasury panel
([Gurkaynak, Sack, Wright, 2007](https://doi.org/10.1016/j.jmoneco.2007.06.029)).
This replaces the earlier ftsfr implementation, which used a duration-matched
credit spread as a stand-in for the Z-spread.

## Sample filters (matching the paper)

1. Senior unsecured USD-denominated debt with non-missing ISIN
2. Fixed-rate bonds with maturity between 1 and 10 years
3. Outstanding principal >= USD 100,000 (`amount_outstanding > 100` in `wrdsapps_bondret.bondret`)
4. Excludes convertible bonds (`conv = 0`)
5. Excludes bonds priced below 50 cents on the dollar (`price_eom >= 50`)
6. CDS curve must have at least two tenors on the same date as the bond
   observation (otherwise the cubic-spline interpolation is unidentified).

## Data flow

```
pull_wrds_bond_ret.py    -> wrds_bondret_project.parquet
pull_markit_mapping.py   -> RED_and_ISIN_mapping.parquet
pull_wrds_markit.py      -> markit_cds.parquet
                           |
merge_cds_bond.py        -> Final_data.parquet           (bond + interpolated par CDS spread)
merge_z_spread_bond.py   -> final_data_with_z_spread.parquet
process_final_product.py -> cds_basis_aggregated.parquet (IG / HY monthly means in bps)
```
"""

# %%
import sys
from pathlib import Path

sys.path.insert(0, "../../src")
sys.path.insert(0, "./src")

import pandas as pd
from matplotlib import pyplot as plt

from settings import config

DATA_DIR = Path(config("DATA_DIR")) / "cds_bond_basis"

# %%
"""
## Aggregated panel: IG vs HY CDS-bond basis (bps)

The aggregated parquet is one row per (c_rating, date) and analysis period.
We focus on the full-sample series here; the paper's replication window is
shown as a separate slice for direct comparison to Figure A1g.
"""

# %%
agg_df = pd.read_parquet(DATA_DIR / "cds_basis_aggregated.parquet")
agg_df.head()

# %%
stats_df = pd.read_csv(DATA_DIR / "cds_basis_summary_stats.csv")
stats_df

# %%
"""
## Full-sample plot
"""

# %%
full = agg_df[agg_df["analysis_period"] == "full_period"].copy()
full["date"] = pd.to_datetime(full["date"])

fig, ax = plt.subplots(figsize=(12, 6))
for rating in ["Investment Grade", "High Yield"]:
    s = (
        full[full["c_rating"] == rating]
        .groupby(pd.Grouper(key="date", freq="ME"))["cds_basis_spread_bps"]
        .mean()
    )
    ax.plot(s.index, s.values, label=rating, linewidth=1.2)
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.set_title("CDS-Bond Basis (full sample)")
ax.set_xlabel("Date")
ax.set_ylabel("Basis (bps)")
ax.grid(True, linewidth=0.3, alpha=0.7)
ax.legend()
plt.tight_layout()
plt.show()

# %%
"""
## Paper replication window (2010-01 to 2020-02) — Figure A1g comparison
"""

# %%
rep = agg_df[agg_df["analysis_period"] == "replication_2010_2020"].copy()
rep["date"] = pd.to_datetime(rep["date"])

fig, ax = plt.subplots(figsize=(12, 6))
for rating in ["Investment Grade", "High Yield"]:
    s = (
        rep[rep["c_rating"] == rating]
        .groupby(pd.Grouper(key="date", freq="ME"))["cds_basis_spread_bps"]
        .mean()
    )
    ax.plot(s.index, s.values, label=rating, linewidth=1.2)
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.set_title("CDS-Bond Basis (replication window, paper Figure A1g)")
ax.set_xlabel("Date")
ax.set_ylabel("Basis (bps)")
ax.grid(True, linewidth=0.3, alpha=0.7)
ax.legend()
plt.tight_layout()
plt.show()
