"""
Gather and preprocess data from Siriwardane et al. (and related sources).

Summary:
- We collect various arbitrage spread data that Siriwardane et al. have made
  publicly available on their website.
- They differentiate "unsecured" arbitrages, which require more unsecured
  funding, from "secured" arbitrages, which are more collateralized. The
  paper documents that unsecured strategies (e.g., equity spot-futures,
  options, CIP arbitrage) typically have higher margin requirements.

Coverage:
- JPY/USD FX swap basis data
- Treasury cash-futures bases
- Interest rate swap spreads
- Other data sets, such as CIP and equity spot-futures, are also available in
  the Siriwardane data repository.

Notes:
- Certain functionality here is partially automated. In some places, the data
  is manually extracted or stitched together.
- The final output is typically combined into a single wide or long format
  dataset for convenience.
"""

import pandas as pd

from settings import config

# Points to the directory where data is stored
DATA_DIR = config("DATA_DIR")
MANUAL_DATA_DIR = config("MANUAL_DATA_DIR")

###############################################################################
# Functions below read older datasets, which are not from the official sources
# provided by OFR but from personal or external collections. They were manually
# compiled and may not be fully consistent with the official version.
###############################################################################


# def load_treasury_sf(data_dir=DATA_DIR, raw=False):
#     """
#     Placeholder for Treasury futures implied risk-free rate minus OIS from Siriwardane et al.
#     Currently raises NotImplementedError.
#     """
#     raise NotImplementedError


name_map = {
    "raw_box_12m": "Box_06m",
    "raw_box_18m": "Box_12m",
    "raw_box_6m": "Box_18m",
    "raw_cal_dow": "Eq_SF_Dow",
    "raw_cal_ndaq": "Eq_SF_NDAQ",
    "raw_cal_spx": "Eq_SF_SPX",
    "raw_cds_bond_hy": "CDS_Bond_HY",
    "raw_cds_bond_ig": "CDS_Bond_IG",
    "raw_cip_aud": "CIP_AUD",
    "raw_cip_cad": "CIP_CAD",
    "raw_cip_chf": "CIP_CHF",
    "raw_cip_eur": "CIP_EUR",
    "raw_cip_gbp": "CIP_GBP",
    "raw_cip_jpy": "CIP_JPY",
    "raw_cip_nzd": "CIP_NZD",
    "raw_cip_sek": "CIP_SEK",
    "raw_tfut_10": "Treasury_SF_10Y",
    "raw_tfut_2": "Treasury_SF_02Y",
    "raw_tfut_20": "Treasury_SF_20Y",
    "raw_tfut_30": "Treasury_SF_30Y",
    "raw_tfut_5": "Treasury_SF_05Y",
    "raw_tips_treas_10": "TIPS_Treasury_10Y",
    "raw_tips_treas_2": "TIPS_Treasury_02Y",
    "raw_tips_treas_20": "TIPS_Treasury_20Y",
    "raw_tips_treas_5": "TIPS_Treasury_05Y",
    "raw_tswap_1": "Treasury_Swap_01Y",
    "raw_tswap_10": "Treasury_Swap_10Y",
    "raw_tswap_2": "Treasury_Swap_02Y",
    "raw_tswap_20": "Treasury_Swap_20Y",
    "raw_tswap_3": "Treasury_Swap_03Y",
    "raw_tswap_30": "Treasury_Swap_30Y",
    "raw_tswap_5": "Treasury_Swap_05Y",
}


def load_combined_spreads_wide(data_dir=DATA_DIR, raw=False, rename=True):
    """
    Load the wide-format arbitrage spreads from Siriwardane et al.
    If not raw, only keeps the columns labeled 'raw_*' in the original dataset
    and optionally renames them.

    Returns:
    --------
    DataFrame with a date index and a variety of spread columns (CIP, CDS-Bond,
    Box, Equity SF, TIPS, Treasury-Futures, etc.).
    """
    # The code references an external link for the .dta file
    # Reference data here: U:\GitRepositories\final_projects_2025\p12_treasury_sf_arb\data_manual\reference
    url = "https://www.dropbox.com/scl/fi/81jm3dbe856i7p17rjy87/arbitrage_spread_wide.dta?rlkey=ke78u464vucmn43zt27nzkxya&st=59g2n7dt&dl=1"
    # url = MANUAL_DATA_DIR / "reference" / "arbitrage_spread_wide.dta"
    df = pd.read_stata(url).set_index("date")

    if raw:
        return df.copy()
    else:
        columns_to_keep = list(name_map.keys())
        subset_df = df[columns_to_keep].copy()
        if rename:
            subset_df = subset_df.rename(columns=name_map)
        return subset_df.reindex(sorted(subset_df.columns), axis=1)


# def demo():
#     """
#     Demonstrates usage of some old vs. new data loading routines.
#     """
#     fxswap, fxbasis = read_usdjpyfxswap(config.DATA_DIR)
#     tcf = read_treasury_cash_futures_bases(config.DATA_DIR)
#     iss = read_interest_swap_spread_bases(config.DATA_DIR)
#     df_old = read_combined_basis_file_OLD(config.DATA_DIR)
#     df_new = load_combined_spreads_wide(data_dir=DATA_DIR)

#     df_old.plot()
#     df_new.columns
#     # Example slice for TCF spreads in old data
#     df_old.loc["2010":"2020", ["Treasury_SF_02Y", "Treasury_SF_05Y", "Treasury_SF_10Y", "Treasury_SF_30Y"]].plot()
#     # Example slice in new data
#     df_new.loc["2010":"2020", ["Treasury_SF_10Y", "Treasury_SF_02Y", "Treasury_SF_20Y", "Treasury_SF_30Y"]].plot()


if __name__ == "__main__":
    # As a placeholder, we do not run anything by default.
    # You can invoke the code by calling 'demo()' or other relevant functions.
    pass
