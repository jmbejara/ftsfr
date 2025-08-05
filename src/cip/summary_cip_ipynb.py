# %%
"""
# Cleaning Summary: Covered Interest Parity (CIP) Arbitrage Spreads

**Source:**
Du, W., & Schreger, J. (2023). *Covered Interest Parity Deviations: Macro Risks and Market Frictions*. Harvard Business School.
[Link to paper](https://www.hbs.edu/ris/Publication%20Files/24-030_1506d32b-3190-4144-8c75-a2326b87f81e.pdf)

## Data Collection and Processing Pipeline

This analysis examines Covered Interest Parity (CIP) deviations using a two-stage data processing pipeline:

1. **Data Retrieval (`pull_bbg_foreign_exchange.py`)**: Fetches raw foreign exchange data from Bloomberg Terminal, including spot exchange rates, 3-month forward points, and Overnight Index Swap (OIS) rates for eight G10 currencies versus USD.

2. **CIP Calculation (`calc_cip.py`)**: Processes the raw data to compute CIP arbitrage spreads, applying standardized transformations and outlier detection methods.
"""

# %%
import sys
from pathlib import Path

sys.path.insert(0, "../../src")
sys.path.insert(0, "./src")

import calc_cip
import cip_analysis
import pandas as pd

from settings import config

DATA_DIR = Path(config("DATA_DIR")) / "cip"

# %%
""" 
## Data Sources and Coverage

Our analysis examines Covered Interest Parity (CIP) deviations across eight G10 currencies against the USD, using data from 1999 onwards sourced through Bloomberg Terminal. The dataset includes:

- **Spot exchange rates**: Current market rates for currency pairs
- **3-month forward points**: Market-quoted forward premiums/discounts  
- **Overnight Index Swap (OIS) rates**: Risk-free benchmark rates for each currency

**Currency Coverage**: AUD, CAD, CHF, EUR, GBP, JPY, NZD, and SEK versus USD

**Data Standardization**: The analysis accounts for different market quotation conventions:
- Forward points are scaled appropriately (per 10,000 for most currencies, per 100 for JPY)
- Currencies conventionally quoted as USD-per-foreign-currency (EUR, GBP, AUD, NZD) are converted to reciprocal rates for consistency
- OIS rates serve as our risk-free benchmark to align with other arbitrage spread studies
"""

# %%
spot_rates = pd.read_parquet(DATA_DIR / "fx_spot_rates.parquet")
fwd_pts = pd.read_parquet(DATA_DIR / "fx_forward_points.parquet")
int_rates = pd.read_parquet(DATA_DIR / "fx_interest_rates.parquet")

# %%
cip_table = calc_cip.calculate_cip(data_dir=DATA_DIR)
cip_table.tail()

# %%
"""
## Data Processing Steps

The raw Bloomberg data undergoes several standardization steps in `pull_bbg_foreign_exchange.py`:

1. **Forward Rate Calculation**: Forward points are converted to actual forward rates by:
   - Scaling forward points (÷10,000 for most currencies, ÷100 for JPY)
   - Adding scaled points to corresponding spot rates

2. **Currency Convention Standardization**: To ensure consistent USD-per-foreign-currency quotation:
   - EUR, GBP, AUD, and NZD rates are converted to reciprocals (1.0 / original rate)
   - Applied to both spot and forward rates for these currencies

3. **Data Merging**: Spot rates, forward rates, and OIS rates are merged on date indices for comprehensive analysis
"""

# %%
"""
## CIP Spread Calculation

Using the prepared data, we calculate CIP arbitrage spreads using the log-linearized formula.
"""

# %%
print(f"Max CIP Deviation: {cip_table.max().idxmax()}")

# %%
cip_table_replicate = calc_cip.calculate_cip(end_date="2020-01-01", data_dir=DATA_DIR)
cip_table_replicate.tail()

# %%
print(f"Max CIP Deviation: {cip_table_replicate.max().idxmax()}")

# %%
calc_cip.plot_cip_from_data(
    cip_table_replicate, end_date="2020-01-01", output_suffix="replicate"
)

# %%
"""
## CIP Calculation and Data Cleaning Process

The CIP spread calculation in `calc_cip.py` follows these steps:

1. **CIP Formula Application**: 
   - Uses log-linearized CIP formula: CIP = 10,000 × [domestic_rate - (ln(F) - ln(S)) × (360/90) - foreign_rate]
   - Domestic rate: Currency-specific OIS rate
   - Foreign rate: USD OIS rate  
   - Forward premium: Annualized using 360/90 day convention

2. **Outlier Detection and Cleaning**:
   - Implements 45-day rolling window outlier detection
   - Calculates rolling median and mean absolute deviation (MAD)
   - Removes extreme values exceeding 10× rolling MAD threshold
   - Replaces outliers with NaN to preserve time series structure

3. **Output Formatting**: Final spreads are expressed in basis points with shortened currency labels for analysis
"""

# %%
"""
## Extended Analysis: 2025 Dataset

We extend our analysis to include more recent data through 2025 to examine contemporary CIP patterns.
"""

# %%
cip_table_2025 = calc_cip.calculate_cip(end_date="2025-01-01", data_dir=DATA_DIR)
cip_table_2025.tail()

# %%
calc_cip.plot_cip_from_data(cip_table_2025, end_date="2025-01-01", output_suffix="2025")

# %%
"""
## Summary Statistics and Cross-Currency Analysis

The following section provides comprehensive statistical analysis of CIP deviations across currencies and time periods.
"""

# %%
cip_table_2025.describe()


# %%
# Create a version with the column names that cip_analysis expects
cip_table_2025_for_analysis = cip_table_2025.copy()
cip_table_2025_for_analysis.columns = [
    f"CIP_{col}_ln" for col in cip_table_2025_for_analysis.columns
]
stats = cip_analysis.compute_cip_statistics(cip_table_2025_for_analysis)

# %%
cip_analysis.display_cip_summary(stats)

# %%
cip_analysis.display_cip_corr(stats)

# %%
cip_analysis.display_cip_max_min(stats)
