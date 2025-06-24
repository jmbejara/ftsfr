# %%

'''
## Covered Interest Parity (CIP) Arbitrage Replication
This contains steps to replicate the arbitrage referencing below

<small> **Source:**
Du, W., & Schreger, J. (2023). *Covered Interest Parity Deviations: Macro Risks and Market Frictions*. Harvard Business School.
[Link to paper](https://www.hbs.edu/ris/Publication%20Files/24-030_1506d32b-3190-4144-8c75-a2326b87f81e.pdf)


## Load and Format Data (Replication)
'''

# %%

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import sys
import os
import calc_cip

project_root = Path().resolve().parent.parent
sys.path.insert(0, str(project_root))

from settings import config

DATA_DIR = project_root / "_data"
SRC_PATH = project_root / "src"


if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
import pull_bloomberg_cip_data
import cip_analysis
import importlib
import settings

# %%

'''
### Details of our Replication

<small> For our analysis of Covered Interest Rate Parity (CIP) deviations in G10 currencies against the USD, we collect data from January 2010 onwards using Bloomberg as our primary data source. The dataset incorporates spot exchange rates, 3-month forward rates, and Overnight Index Swap (OIS) rates for eight major currencies: AUD, CAD, CHF, EUR, GBP, JPY, NZD, and SEK. We use OIS as our benchmark risk-free rate to ensure consistency with other arbitrage spread analyses. Our implementation handles the different quotation conventions, with appropriate scaling of forward points and conversion to reciprocal rates for currencies conventionally quoted in USD-per-foreign-currency terms (EUR, GBP, AUD, NZD). This comprehensive dataset allows us to calculate CIP deviations according to the formula.

### Set up

<small>

First, we will load the raw data. If you are utilizing a Bloomberg Terminal, set:

```python
input_excel = False
```

The function will pull from bloomberg itself rather than a loaded excel file

'''

# %%

spot_rates = pd.read_parquet(f"{DATA_DIR}/cip/fx_spot_rates.parquet")
fwd_pts = pd.read_parquet(f"{DATA_DIR}/cip/fx_forward_points.parquet")
int_rates = pd.read_parquet(f"{DATA_DIR}/cip/fx_interest_rates.parquet")

# %%

hmm = calc_cip.prepare_fx_data(spot_rates, fwd_pts, int_rates)
hmm

# %%

cip_table = calc_cip.calculate_cip(plot = True)
cip_table

# %%

cip_table.describe()

# %%

cip_table.isna().sum()

# %%

from IPython.display import IFrame
#graph = calc_cip.plot_cip_spreads(cip_table)
IFrame("cip_spreads.pdf", width=800, height=600)