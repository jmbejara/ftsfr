# %%
"""
# Cleaning Summary: Covered Interest Parity (CIP) Arbitrage Spreads

<small> **Source:**
Du, W., & Schreger, J. (2023). *Covered Interest Parity Deviations: Macro Risks and Market Frictions*. Harvard Business School.
[Link to paper](https://www.hbs.edu/ris/Publication%20Files/24-030_1506d32b-3190-4144-8c75-a2326b87f81e.pdf)

## Load and Format Data
"""

# %%
import sys
from pathlib import Path

sys.path.insert(0, "../../src")
sys.path.insert(0, "./src")

import calc_cip
import cip_analysis
import pandas as pd
from IPython.display import display

from settings import config

DATA_DIR = Path(config("DATA_DIR")) / "cip"

# %%
"""
<small> For our analysis of Covered Interest Rate Parity (CIP) deviations in G10 currencies against the USD, we collect data from January 2010 onwards using Excel as our secondary data source, orginally from bloomberg. The dataset incorporates spot exchange rates, 3-month forward rates, and Overnight Index Swap (OIS) rates for eight major currencies: AUD, CAD, CHF, EUR, GBP, JPY, NZD, and SEK. We use OIS as our benchmark risk-free rate to ensure consistency with other arbitrage spread analyses. Our implementation handles the different quotation conventions, with appropriate scaling of forward points and conversion to reciprocal rates for currencies conventionally quoted in USD-per-foreign-currency terms (EUR, GBP, AUD, NZD). This comprehensive dataset allows us to calculate CIP deviations according to the formula.


"""

# %%
"""
<small>

First, we will load the raw data. If you are utilizing a Bloomberg Terminal, set:

```python
input_excel = False

and the function will pull from bloomberg itself rather than a loaded excel file
"""

# %%
spot_rates = pd.read_parquet(f"{DATA_DIR}/fx_spot_rates.parquet")
fwd_pts = pd.read_parquet(f"{DATA_DIR}/fx_forward_points.parquet")
int_rates = pd.read_parquet(f"{DATA_DIR}/fx_interest_rates.parquet")

# %%
hmm = calc_cip.prepare_fx_data(spot_rates, fwd_pts, int_rates)
hmm

# %%
cip_table = calc_cip.calculate_cip(data_dir=DATA_DIR)
cip_table

# %%
cip_table.describe()

# %%
cip_table.isna().sum()

# %%
"""
<small>
Process in cleaning raw data:

- Converted forward points to actual forward rates
- Applied scaling factors: per 10,000 for most currencies, per 100 for JPY
- Standardized EUR, GBP, AUD, and NZD to USD-per-foreign-currency format
- Performed reciprocal conversion using 1.0 / original rate
- Applied conversion to both spot and forward values
"""

# %%
"""
<small> Next we will calculate the CIP arbitrage spreads
"""

# %%
print(f"Max CIP Deviation: {cip_table.max().idxmax()}")

# %%
"""
---
"""

# %%
cip_table_replicate = calc_cip.calculate_cip(end_date="2020-01-01", data_dir=DATA_DIR)
display(cip_table_replicate)

# %%
print(f"Max CIP Deviation: {cip_table_replicate.max().idxmax()}")

# %%
calc_cip.plot_cip_from_data(cip_table_replicate, end_date="2020-01-01", output_suffix="replicate")

# %%
"""
<small>
Process to calculate the CIP and clean the data:

- Calculated logarithmic CIP deviations in basis points
- Multiplied deviations by 10,000
- Incorporated interest rates and annualized forward premium
- Applied 360/90 day count convention for 3-month forward premium
- Implemented 45-day rolling window outlier detection
- Removed extreme values exceeding 10× rolling mean absolute deviation
- Renamed and reorganized columns for clarity
"""

# %%
"""
## Load data to 2025
"""

# %%
cip_table_2025 = calc_cip.calculate_cip(end_date="2025-01-01", data_dir=DATA_DIR)
display(cip_table_2025)

# %%
calc_cip.plot_cip_from_data(cip_table_2025, end_date="2025-01-01", output_suffix="2025")

# %%
"""
### Summary Statistics
"""

# %%
cip_table_2025.describe()

# %%
"""
<small> Our analysis revealed that the COVID period produced the most extreme spread variations in our sample, ranging from -50 to over 200 basis points. This extraordinary divergence created unique opportunities: currencies like NZD exhibited deeply negative spreads, making synthetic funding through government bonds particularly profitable. Conversely, EUR and CHF displayed strongly positive spreads, creating exploitable differences between actual risk-free rates.
It's worth noting that CHF demonstrated multiple volatility spikes throughout the sample period, attributable to the 2015 Swiss National Bank policy shock, persistent negative interest rate conditions, and its relatively thinner liquidity profile compared to other G10 currencies.
"""

# %%
# Create a version with the column names that cip_analysis expects
cip_table_2025_for_analysis = cip_table_2025.copy()
cip_table_2025_for_analysis.columns = [f"CIP_{col}_ln" for col in cip_table_2025_for_analysis.columns]
stats = cip_analysis.compute_cip_statistics(cip_table_2025_for_analysis)

# %%
cip_analysis.display_cip_summary(stats)

# %%
cip_analysis.display_cip_corr(stats)

# %%
cip_analysis.display_cip_max_min(stats)
