from pathlib import Path
import sys

sys.path.append("../")
import polars as pl

from settings import config
import compute_tips_treasury

DATA_DIR = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "basis_tips_treas"

df = compute_tips_treasury.load_tips_treasury(data_dir=DATA_DIR)

# # Plot
# df = df.select(["date", "arb_2", "arb_5", "arb_10", "arb_20"])
# df.to_pandas().set_index("date").plot()

df_long = (
    (
        df.select(["date", "arb_2", "arb_5", "arb_10", "arb_20"])
        .with_columns(pl.col("date").cast(pl.Datetime))
        .unpivot(index=["date"], variable_name="unique_id", value_name="y")
    )
    .rename({"date": "ds"})
    .select(["unique_id", "ds", "y"])
)

df_long.write_parquet(Path(DATA_DIR) / "ftsfr_tips_treasury_basis.parquet")
