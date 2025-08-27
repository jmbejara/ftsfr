"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

- corp_bond_portfolio_returns: corporate bond portfolio returns
"""

import merge_cds_bond
import process_final_product
import pandas as pd
from settings import config

DATA_DIR = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "cds_bond_basis"
RED_CODE_FILE_NAME = "RED_and_ISIN_mapping.parquet"
CORPORATES_MONTHLY_FILE_NAME = "corporate_bond_returns.parquet"
CDS_FILE_NAME = (
    "markit_cds.parquet"  # Assuming this is the file name from Kaustaub's script
)


## Calculate cds_basis


corp_bonds_data = pd.read_parquet(f"{DATA_DIR}/{CORPORATES_MONTHLY_FILE_NAME}")
red_data = pd.read_parquet(f"{DATA_DIR}/{RED_CODE_FILE_NAME}")
cds_data = pd.read_parquet(f"{DATA_DIR}/{CDS_FILE_NAME}")

corp_red_data = merge_cds_bond.merge_red_code_into_bond_treas(corp_bonds_data, red_data)
final_data = merge_cds_bond.merge_cds_into_bonds(corp_red_data, cds_data)
# Missing a step of "process final data" from the ipynb

df_all = process_final_product.process_cb_spread(final_data)

agg_df, non_agg_df = process_final_product.output_cb_final_products(df_all)

# Set date as index before stacking to avoid mixing date and numeric values
agg_df_indexed = agg_df.set_index(["c_rating", "date"])
df_stacked = agg_df_indexed.stack().reset_index()
df_stacked.columns = ["c_rating", "date", "variable", "value"]
# Create a unique ID from c_rating
df_stacked["unique_id"] = df_stacked["c_rating"].astype(str)
df_stacked = df_stacked[["unique_id", "date", "value"]].rename(
    columns={"date": "ds", "value": "y"}
)

# For non-aggregated data, set cusip and date as index
non_agg_df_indexed = non_agg_df.set_index(["cusip", "date"])
df_stacked2 = non_agg_df_indexed.stack().reset_index()
df_stacked2.columns = ["cusip", "date", "variable", "value"]
# Use cusip as unique_id
df_stacked2["unique_id"] = df_stacked2["cusip"]
df_stacked2 = df_stacked2[["unique_id", "date", "value"]].rename(
    columns={"date": "ds", "value": "y"}
)

df_stacked.to_parquet(DATA_DIR / "ftsfr_CDS_bond_basis_aggregated.parquet")
df_stacked2.to_parquet(DATA_DIR / "ftsfr_CDS_bond_basis_non_aggregated.parquet")
