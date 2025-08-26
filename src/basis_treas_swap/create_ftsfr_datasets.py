from pathlib import Path
import sys

sys.path.append("../")
import polars as pl

from settings import config
import calc_swap_spreads

DATA_DIR = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "basis_treas_swap"

df = calc_swap_spreads.load_swap_spreads(data_dir=DATA_DIR)
df = df[
    [
        "Arb_Swap_1",
        "Arb_Swap_2",
        "Arb_Swap_3",
        "Arb_Swap_5",
        "Arb_Swap_10",
        "Arb_Swap_20",
        "Arb_Swap_30",
    ]
]

df = df.dropna(how="all").reset_index(names="Date")
# df = df.set_index("Date").plot()
df = pl.from_pandas(df)

df_long = (
    (
        df.select(
            [
                "Date",
                "Arb_Swap_1",
                "Arb_Swap_2",
                "Arb_Swap_3",
                "Arb_Swap_5",
                "Arb_Swap_10",
                "Arb_Swap_20",
                "Arb_Swap_30",
            ]
        )
        .with_columns(pl.col("Date").cast(pl.Date))
        .unpivot(index=["Date"], variable_name="unique_id", value_name="y")
    )
    .rename({"Date": "ds"})
    .select(["unique_id", "ds", "y"])
)

df_long.write_parquet(Path(DATA_DIR) / "ftsfr_treasury_swap_basis.parquet")
