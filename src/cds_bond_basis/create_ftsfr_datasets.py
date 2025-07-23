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
# DATA_DIR = DATA_DIR / "wrds_crsp_compustat"
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

df_stacked = agg_df.stack().reset_index()
df_stacked.columns = ['unique_id', 'ds', 'y']

df_stacked2 = non_agg_df.stack().reset_index()
df_stacked2.columns = ['unique_id', 'ds', 'y']

df_stacked.to_parquet(DATA_DIR / "ftsfr_CDS_bond_basis_aggregated.parquet")
df_stacked2.to_parquet(DATA_DIR / "ftsfr_CDS_bond_basis_non_aggregated.parquet")

