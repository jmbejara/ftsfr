from pathlib import Path
import sys
sys.path.append("../")
import polars as pl

from settings import config
import compute_tips_treasury

DATA_DIR = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "basis_tips_treas"

df = compute_tips_treasury.load_tips_treasury(data_dir=DATA_DIR)

df_long = (
    df.select(
        ["date", "tips_treas_2_rf", "tips_treas_5_rf", "tips_treas_10_rf", "tips_treas_20_rf"]
    )
    .with_columns(
        pl.col("date").cast(pl.Date)
    )
    .unpivot(
        index=["date"],
        variable_name="unique_id",
        value_name="y"
    )
).rename({"date": "ds"}).select(
    ["unique_id", "ds", "y"]
)

df_long.write_parquet(
    Path(DATA_DIR) / "ftsfr_tips_treasury_implied_rf.parquet"
)





