import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import polars as pl

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
# DATA_DIR = DATA_DIR / "options"

df_hkm = pl.read_parquet(DATA_DIR / "hkm_portfolio_returns_1996-01_2019-12.parquet")
# rename columns
df_hkm = df_hkm.rename({"ftfsa_id": "unique_id", "return": "y", "date": "ds"})
df_hkm = df_hkm.select(["unique_id", "ds", "y"])
# cast ds to date
# df_hkm = df_hkm.with_columns(pl.col('ds').cast(pl.Date))

df_cjs = pl.read_parquet(DATA_DIR / "cjs_portfolio_returns_1996-01_2019-12.parquet")
# rename columns
df_cjs = df_cjs.rename({"ftfsa_id": "unique_id", "return": "y", "date": "ds"})
df_cjs = df_cjs.select(["unique_id", "ds", "y"])
# cast ds to date
# df_cjs = df_cjs.with_columns(pl.col('ds').cast(pl.Date))

# save to data directory
df_hkm.write_parquet(DATA_DIR / "ftsfr_hkm_option_returns.parquet")
df_cjs.write_parquet(DATA_DIR / "ftsfr_cjs_option_returns.parquet")
