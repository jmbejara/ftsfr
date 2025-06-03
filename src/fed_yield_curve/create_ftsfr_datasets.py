"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

- treas_yield_curve_zero_coupon: Federal Reserve yield curve

"""

import pull_fed_yield_curve

from settings import config

DATA_DIR = config("DATA_DIR")


## treas_yield_curve_zero_coupon
df_all = pull_fed_yield_curve.load_fed_yield_curve(data_dir=DATA_DIR)
# df_all.info()
df = df_all.reset_index()
df = df.melt(id_vars=["Date"], var_name="tenor", value_name="value")
df = df[["tenor", "Date", "value"]].sort_values(by=["tenor", "Date"])
df = df.rename(columns={"Date": "date", "tenor": "entity"})
df.to_parquet(DATA_DIR / "ftsfr_treas_yield_curve_zero_coupon.parquet")
