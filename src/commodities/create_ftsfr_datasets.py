"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

"""

import calc_commodities_returns
from settings import config

DATA_DIR = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "commodities"


## Calculate commodities returns
df = calc_commodities_returns.load_commodities_returns(data_dir=DATA_DIR)
# df["unique_id"].unique()

# df.pivot(index="ds", columns="unique_id", values="y").plot()

# df.pivot(index="ds", columns="unique_id", values="y")["SPGCBRP Index_PX_LAST_Return"].plot()

df.reset_index(inplace=True, drop=True)
df.to_parquet(DATA_DIR / "ftsfr_commodities_returns.parquet")
