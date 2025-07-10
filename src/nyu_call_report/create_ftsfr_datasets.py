"""
This module contains functions to load the datasets.
It is used to load the datasets into memory.

List of datasets:

- nyu_call_report_leverage: Total assets / Total equity
- nyu_call_report_holding_company_leverage: Total assets / Total equity
- nyu_call_report_cash_liquidity: Cash / Total assets
- nyu_call_report_holding_company_cash_liquidty: Cash flow / Total assets
"""

import pull_nyu_call_report

from settings import config

DATA_DIR = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "nyu_call_report"


## nyu_call_report_leverage
df_all = pull_nyu_call_report.load_nyu_call_report(data_dir=DATA_DIR)
# df_all.info(verbose=True)
df_all["leverage"] = df_all["assets"] / df_all["equity"]

df = (
    df_all[["rssdid", "date", "leverage"]]
    .sort_values(by=["rssdid", "date"])
    .reset_index(drop=True)
)
# reshape to wide
# df_wide = df.pivot(index="date", columns="rssdid", values="leverage")
# df_wide.to_parquet(DATA_DIR / "ftsfr_nyu_call_report_leverage.parquet")
df = df.rename(columns={"rssdid": "entity", "date": "date", "leverage": "value"})
df.to_parquet(DATA_DIR / "ftsfr_nyu_call_report_leverage.parquet")

## nyu_call_report_holding_company_leverage
# Group by bhcid, sum the assets, equity, and cash to create a dataset at the holding company level
df_bhc = (
    df_all[["bhcid", "date", "assets", "equity", "cash"]]
    .groupby(["bhcid", "date"])
    .sum()
)
df_bhc = df_bhc.reset_index()
df_bhc["leverage"] = df_bhc["assets"] / df_bhc["equity"]

df_bhc = df_bhc.rename(columns={"bhcid": "entity", "date": "date", "leverage": "value"})
# drop values where entity is 0
df_bhc = df_bhc[df_bhc["entity"] != "0"]
df_bhc = df_bhc[["entity", "date", "value"]].reset_index(drop=True)
df_bhc.to_parquet(DATA_DIR / "ftsfr_nyu_call_report_holding_company_leverage.parquet")
# df_wide = df_bhc.pivot(index="date", columns="bhcid", values="leverage")
# df_wide = df_wide.drop(columns=["0"])
# df_wide.to_parquet(DATA_DIR / "ftsfr_nyu_call_report_holding_company_leverage.parquet")

## nyu_call_report_cash_liquidity
df_all["cash_liquidity"] = df_all["cash"] / df_all["assets"]
df = (
    df_all[["rssdid", "date", "cash_liquidity"]]
    .sort_values(by=["rssdid", "date"])
    .reset_index(drop=True)
)
df = df.rename(columns={"rssdid": "entity", "date": "date", "cash_liquidity": "value"})
df.to_parquet(DATA_DIR / "ftsfr_nyu_call_report_cash_liquidity.parquet")
# df_wide = df.pivot(index="date", columns="rssdid", values="cash_liquidity")
# df_wide.to_parquet(DATA_DIR / "ftsfr_nyu_call_report_cash_liquidity.parquet")

## nyu_call_report_holding_company_cash_liquidity
df_bhc = (
    df_all[["bhcid", "date", "cash", "assets"]]
    .groupby(["bhcid", "date"])
    .sum()
    .sort_values(by=["bhcid", "date"])
    .reset_index()
)
df_bhc["cash_liquidity"] = df_bhc["cash"] / df_bhc["assets"]
df = df_bhc.rename(columns={"bhcid": "entity", "date": "date", "cash_liquidity": "value"})
df = df[df["entity"] != "0"]
df = df[["entity", "date", "value"]].reset_index(drop=True)
df.to_parquet(DATA_DIR / "ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet")

# df_wide = df_bhc.pivot(index="date", columns="bhcid", values="cash_liquidity")
# df_wide = df_wide.drop(columns=["0"])
# df_wide.to_parquet(
#     DATA_DIR / "ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet"
# )
