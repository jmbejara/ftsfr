from pathlib import Path
import sys
sys.path.append("../")
import polars as pl

from settings import config
import calc_basis_treas_sf

DATA_DIR = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "basis_treas_sf"

df = calc_basis_treas_sf.load_treasury_sf_output(data_dir=DATA_DIR)
df = df.set_index("Date").dropna(how="all").reset_index()
df = pl.from_pandas(df)

df_long = (
    df.select(
        ["Date", "Treasury_SF_2Y", "Treasury_SF_5Y", "Treasury_SF_10Y", "Treasury_SF_20Y", "Treasury_SF_30Y"]
    )
    .with_columns(
        pl.col("Date").cast(pl.Datetime)
    )
    .unpivot(
        index=["Date"],
        variable_name="unique_id",
        value_name="y"
    )
).rename({"Date": "ds"}).select(
    ["unique_id", "ds", "y"]
)

df_long.write_parquet(
    Path(DATA_DIR) / "ftsfr_treasury_sf_basis.parquet"
)





