# %%

"""

# Foreign Exchange Daily Returns Series

We are generating a Daily Returns Time Series for FX investing.

## Data Sources

Bloomberg is used to pull all of the data necessary for building this returns series. We will be using FX spot rates and interest rates (get specific pull data for this later).

## Methodology

$$
ret_{t, i} = \frac{spot_{t - 1, i}}{spot_{t, i}}  \times fret_{t, i}
$$
where
- $i$ is the foreign currency
- $t$ is the date of the implied foreign currency return
- $ret$ is the return of USD invested in the foreign currency
- $fret$ is the return of the foreign currency when invested in their overnight repo market
- $spot$ is the spot price of the currency (**how much 1 USD is worth in the foreign currency**)

We are replicating a process where we convert our USD into the foreign currency $i$ at end of day $t - 1$, invest it in the repo market, then switch the currency back to USD on day $t$.

"""

# %%
import pandas as pd

from calc_fx import *

# %%

# DATA_DIR = config("DATA_DIR")

DATA_DIR = r"../../../FS-project_files/FX-files"

# Initial Pull and analysis

FX_SPOT_RATES = r"fx_spot_rates.parquet"
FX_INTEREST_RATES = r"fx_interest_rates.parquet"

# %%

fx_spot = pd.read_parquet(f"{DATA_DIR}/{FX_SPOT_RATES}")
fx_interest = pd.read_parquet(f"{DATA_DIR}/{FX_INTEREST_RATES}")

# %%

fx_data = prepare_fx_data(fx_spot, fx_interest)
currency_list = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "SEK", "USD"]

# %%

"""
## FX raw data

The FX data we see is pulled from Bloomberg, then aggregated for consistent naming.
- CUR_spot is the spot price of the currency (how much 1 USD is worth in the foreign currency CUR)
- CUR_ir is the interest rate of CUR
"""

# %%

fx_data.head()

# %%

fx_data.tail()

# %%

fx_data.describe()

# %%

fx_data.info()

# %%

"""
# Implied Daily Returns Time Series

Through the *methodology* described above, we then calculate the implied daily returns on foreign currency invesment.
"""

# %%

impl_fx_ret = implied_daily_fx_returns(fx_data, currency_list)

# %%

impl_fx_ret.head()

# %%

impl_fx_ret.tail()

# %%

impl_fx_ret.describe()

# %%

impl_fx_ret.info()

# %%

"""
## Currency Groupings 

We will graph how certain currencies compare based upon regional breakdowns and other categories.
"""

# %%

liquid_currencies = ["USD", "EUR", "GBP", "JPY"]
world_currencies = ["USD", "AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "SEK"]
eur_currencies = ["USD", "EUR", "GBP", "CHF", "EUR", "SEK"]
oceania_currencies = ["USD", "NZD", "AUD"]
can_currencies = ["USD", "CAD"]

# %%

graph_fx_returns(impl_fx_ret, world_currencies, "All Currencies")

# %%

graph_fx_returns(impl_fx_ret, liquid_currencies, "Liquid Currencies")

# %%

graph_fx_returns(impl_fx_ret, eur_currencies, "European Currencies")

# %%

graph_fx_returns(impl_fx_ret, oceania_currencies, "Oceania Currencies")

# %%

graph_fx_returns(impl_fx_ret, can_currencies, "North American Currencies")
