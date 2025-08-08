"""
I use the data provided by Siriwardane et al on their website.

Notes from their paper:
"Our analysis starts from the observation that equity spot-futures, equity
options, and CIP arbitrage face relatively higher margin requirements than other strategies.
Because they require more unsecured funding, we refer to these high-margin strategies as
“unsecured” arbitrages, while we call the remaining ones “secured” arbitrages. Unsecured
arbitrages are more correlated with each other than they are with secured arbitrages"

OLD:
----

Here I collect and clean data from unofficial sources. These
are data that can be shared outside the OFR.

Includes:

  - fx swap basis data for the JPY USD swap basis trade
  - Treasury cash-futures basis.
  - swap_spreads_panel.csv


"""

import numpy as np
import pandas as pd
from pathlib import Path
import compute_tips_treasury
import unittest
from settings import config

# config.switch_to_alt() # Use data stored on local VDI
DATA_DIR = config("DATA_DIR")
OUTPUT_DIR = config("OUTPUT_DIR")


############################################################
## Code to load old bases data, which was manually collected
############################################################


# def read_usdjpyfxswap(dirpath=DATA_DIR):
#     """Read fx swap basis file from Quentin. Returns
#     the cleaned main file and also the final basis rate.

#     The basis is stitched together from two sources: Wenxin's
#     data, which is then extended by the other calculation.
#     I use the extension data as a fallback (rather than averaging
#     overlaps).
#     """
#     filename = "fwswaprate_data.xlsx"
#     dirpath = Path(dirpath) 
#     fxswap = pd.read_excel(dirpath / filename, skiprows=[0, 1, 2]).set_index("date")
#     # fxswap.head()
#     # fxswap.info()
#     basis = fxswap["fxbasisONjpy"].copy()
#     missing = basis.isna()
#     basis[missing] = fxswap.loc[missing, "fxswaprate_LA"]
#     # basis.isna().sum()
#     basis = basis.dropna()
#     # TODO: I'm not sure on the units repoted.
#     basis = basis / 100
#     return fxswap, basis


def read_treasury_cash_futures_bases(dirpath=DATA_DIR):
    filename = "irr_panel_b.csv"
    dirpath = Path(dirpath) 
    df = pd.read_csv(dirpath / filename, parse_dates=["date"]).set_index("date")
    # The PL column was manually created by Jay to match FV, with a fallback
    # of TU when FV was missing. This column should not be used in any
    # circumstance.
    df = df.drop(columns=["PL"])
    return df


def read_interest_swap_spread_bases(dirpath=DATA_DIR):
    filename = "swap_spreads_panel.csv"
    dirpath = Path(dirpath) 
    df = pd.read_csv(dirpath / filename, parse_dates=["date"]).set_index("date")
    # TODO: I'm not sure on the units repoted.
    df = df / 100
    return df


def read_adrien_bases_replication(dirpath=DATA_DIR):
    """Load bases data replicated by Adrien"""
    df = pd.read_stata(dirpath  / "Final_Spreads.dta")
    df = df.rename(columns={"data": "date"}).set_index("date")

    sa_ordering = [  # Missing Treasury SF bases
        "TreasurySwap1Y",
        "TreasurySwap2Y",
        "TreasurySwap3Y",
        "TreasurySwap5Y",
        "TreasurySwap10Y",
        "TreasurySwap20Y",
        "TreasurySwap30Y",  # Missing TIPS-Treasury, CDS-Bond
        "AUD_diff_ois",
        "CAD_diff_ois",
        # 'DKK_diff_ois', # Danish Krone not included in siri et al # Needs CHF Swiss Franc
        "EUR_diff_ois",
        "GBP_diff_ois",
        "JPY_diff_ois",
        "NZD_diff_ois",
        "SEK_diff_ois",  # Swedish Krona
        "BoxSpread6m",
        "BoxSpread12m",
        "BoxSpread18m",
        "Eq_SF_Dow",
        "Eq_SF_NDAQ",
        "Eq_SF_SPX",
    ]
    df = df[sa_ordering]
    return df


def _read_old_combined_basis_file(data_dir=DATA_DIR, rename=True):
    data_dir = Path(data_dir)
    fxswap, fxbasis = read_usdjpyfxswap(data_dir)
    treasury_cash_futures_bases = read_treasury_cash_futures_bases(data_dir)
    interest_swap_spread_bases = read_interest_swap_spread_bases(data_dir)

    df = pd.DataFrame()
    df["fxswap_jpy"] = fxbasis

    tcf = treasury_cash_futures_bases.rename(columns=lambda name: "tcf_" + name)
    df = pd.concat([df, tcf], axis=1)

    interest_swap_spread_bases = read_interest_swap_spread_bases(data_dir)
    iss = interest_swap_spread_bases.rename(columns=lambda name: "iss_" + name)
    df = pd.concat([df, iss], axis=1)

    if rename:
        columns = {
            "tcf_TU": "Treasury_SF_02Y",
            "tcf_FV": "Treasury_SF_05Y",
            "tcf_TY": "Treasury_SF_10Y",
            # '':'Treasury 20Y SF', # Missing
            "tcf_US": "Treasury_SF_30Y",
            # '':'Treasury-Swap 1Y', # Missing
            "iss_2": "Treasury_Swap_02Y",
            # '':'Treasury-Swap 3Y', # Missing
            "iss_5": "Treasury_Swap_05Y",
            "iss_10": "Treasury_Swap_10Y",  # Have data from Adrien
            # '':'Treasury-Swap 20Y', # Have data from Adrien
            "iss_30": "Treasury_Swap_30Y",  # Have data from Adrien
            "fxswap_jpy": "CIP_JPY",  # Have data from Adrien
        }
        df = df.rename(columns=columns)
    # df.mean()
    # df.to_csv('mytemp.csv')
    return df


def read_combined_basis_file_OLD(
    dirpath=DATA_DIR, rename=True, guess_resize=True, flip_to_pos_signs=True
):
    dirpath = Path(dirpath)
    treasury_cash_futures_bases = read_treasury_cash_futures_bases(config.DATA_DIR)
    adrien_rep = read_adrien_bases_replication(dirpath=DATA_DIR)
    tcf = treasury_cash_futures_bases.rename(columns=lambda name: "tcf_" + name)
    df = pd.concat([tcf, adrien_rep], axis=1)

    rescale_list = [
        "AUD_diff_ois",
        "CAD_diff_ois",
        "EUR_diff_ois",
        "GBP_diff_ois",
        "JPY_diff_ois",
        "NZD_diff_ois",
        "SEK_diff_ois",
        "Eq_SF_Dow",
        "Eq_SF_NDAQ",
        "Eq_SF_SPX",
    ]
    for col in rescale_list:
        df[col] = df[col] / 100

    if rename:
        columns = {
            "tcf_TU": "Treasury_SF_02Y",
            "tcf_FV": "Treasury_SF_05Y",
            "tcf_TY": "Treasury_SF_10Y",
            # '':'Treasury_20Y_SF', # Missing
            "tcf_US": "Treasury_SF_30Y",
            "TreasurySwap1Y": "Treasury_Swap_01Y",
            "TreasurySwap2Y": "Treasury_Swap_02Y",
            "TreasurySwap3Y": "Treasury_Swap_03Y",
            "TreasurySwap5Y": "Treasury_Swap_05Y",
            "TreasurySwap10Y": "Treasury_Swap_10Y",
            "TreasurySwap20Y": "Treasury_Swap_20Y",
            "TreasurySwap30Y": "Treasury_Swap_30Y",  # Missing TIPS-Treasury, CDS-Bond
            "AUD_diff_ois": "CIP_AUD",
            "CAD_diff_ois": "CIP_CAD",  # Needs CHF Swiss Franc
            "EUR_diff_ois": "CIP_EUR",
            "GBP_diff_ois": "CIP_GBP",
            "JPY_diff_ois": "CIP_JPY",
            "NZD_diff_ois": "CIP_NZD",
            "SEK_diff_ois": "CIP_SEK",  # Swedish Krona
            "BoxSpread6m": "Box_06m",
            "BoxSpread12m": "Box_12m",
            "BoxSpread18m": "Box_18m",
            "Eq_SF_Dow": "Eq_SF_Dow",
            "Eq_SF_NDAQ": "Eq_SF_NDAQ",
            "Eq_SF_SPX": "Eq_SF_SPX",
        }
        df = df.rename(columns=columns)

    means = df.mean()
    if flip_to_pos_signs:
        for trade in means.index:
            if means[trade] < 0:
                df[trade] = -df[trade]

    # df.mean()
    # df.to_csv('mytemp.csv')
    return df


################################################################################
## Code to load new bases data, which was collected from Siriwardane et al code.
## The process of collecting this data is not fully automated, so I have run the
## code in their GitHub repo and placed the result here.
################################################################################


def load_box(
    data_dir=DATA_DIR,
    raw=False,
):
    """Box Implied Rf - OIS, for 6m, 12m, and 18m
    Reported in basis points
    """
    raise NotImplementedError
    import load_bloomberg
    bl = load_bloomberg.load_selected(data_dir=data_dir)
    ds = load_datastream.load_selected(data_dir=data_dir)
    ds = ds[["USD_6m_OIS", "USD_1y_OIS"]]
    df_ois = pd.concat([ds, bl], axis=1)
    df_ois = df_ois.rename(
        columns={
            "USD_6m_OIS": "USD_06m_OIS",
            "USD_1y_OIS": "USD_12m_OIS",
            "USD_OIS_18m": "USD_18m_OIS",
        }
    )
    filepath = (
        data_dir  / "box" / "box_spreads.dta"
    )
    df_box = pd.read_stata(filepath).set_index("date")
    df = pd.concat([df_box, df_ois], axis=1)
    df = df.dropna(subset=df_box.columns, how="all")

    if raw:
        ret = df
    else:
        ret = pd.DataFrame(index=df.index)
        ret["Box_06m"] = df["box_6m_rf"] - 100 * df["USD_06m_OIS"]
        ret["Box_12m"] = df["box_12m_rf"] - 100 * df["USD_12m_OIS"]
        ret["Box_18m"] = df["box_18m_rf"] - 100 * df["USD_18m_OIS"]
        # ret.plot()
    return ret


def load_cds_bond(
    data_dir=DATA_DIR,
    raw=False,
):
    """
    Arbitrage spreads are reported in basis points. Reported
    as CDS-Bond implied Rf - Maturity Matched Treasury Yield

    In the raw Stata data, there are labels associated with each variable:
    "cds_bond_hy": "HY cds_bond_basis", # Difference of implied Rf and Maturity Matched Treasury
    "cds_bond_hy_treas": "CDS-Bond HY MM Treasury", # Maturity matched treasury?
    "cds_bond_hy_rf": "CDS-Bond HY-Implied Rf",
    "cds_bond_ig": "IG cds_bond_basis",
    "cds_bond_ig_treas": "CDS-Bond IG MM-Treasury",
    "cds_bond_ig_r": "CDS-Bond IG-Implied Rf",
    """
    filepath = (
        data_dir
        
        / "from_siriwardane_et_al"
        / "cds-bond"
        / "cds_bond_implied_rf.dta"
    )
    df = pd.read_stata(filepath).set_index("date")
    # (10000 * df["cds_bond_hy"]).plot()
    # (df["cds_bond_hy_treas"] - df["cds_bond_hy_rf"]).plot()
    # (df["cds_bond_hy_treas"] - df["cds_bond_hy_rf"]).equals(10000 * df["cds_bond_hy"])
    # (df["cds_bond_hy_treas"] - df["cds_bond_hy_rf"] - 10000 * df["cds_bond_hy"]).plot() # Very small average differences. mean(abs(diff)) close to 1e-5
    # df["cds_bond_hy_treas"].plot() # in basis points.
    if raw:
        ret = df
    else:
        df["CDS_Bond_HY"] = df["cds_bond_hy_rf"] - df["cds_bond_hy_treas"]
        df["CDS_Bond_IG"] = df["cds_bond_ig_rf"] - df["cds_bond_ig_treas"]
        # df["CDS_Bond_HY"].plot()
        ret = df[["CDS_Bond_HY", "CDS_Bond_IG"]].copy()
        ret.plot()
    return ret


def load_CIP(
    data_dir=DATA_DIR,
    raw=False,
):
    """
    Arbitrage spreads are reported in basis points.

    Reported as CIP implied Rf minus OIS

    Each provides 3M CURRENCY_XYZ Synthetic Dollar OIS.
    Spreads for AUD, CAD, CHF, EUR, GBP, JPY, NZD, SEK

    """
    raise NotImplementedError
    import load_datastream
    filepath = (
        data_dir  / "cip" / "cip_implied_rf.dta"
    )
    df_cip = pd.read_stata(filepath).set_index("date")

    ds = load_datastream.load_selected(data_dir=data_dir)
    ds = 100 * ds[["USD_3m_OIS"]]

    df = pd.concat([df_cip, ds], axis=1).dropna(subset=df_cip.columns, how="all")
    # df.plot()
    if raw:
        ret = df
    else:
        ret = pd.DataFrame(index=df.index)
        ret["CIP_AUD"] = df["cip_aud_rf"] - df["USD_3m_OIS"]
        ret["CIP_CAD"] = df["cip_cad_rf"] - df["USD_3m_OIS"]
        ret["CIP_CHF"] = df["cip_chf_rf"] - df["USD_3m_OIS"]
        ret["CIP_EUR"] = df["cip_eur_rf"] - df["USD_3m_OIS"]
        ret["CIP_GBP"] = df["cip_gbp_rf"] - df["USD_3m_OIS"]
        ret["CIP_JPY"] = df["cip_jpy_rf"] - df["USD_3m_OIS"]
        ret["CIP_NZD"] = df["cip_nzd_rf"] - df["USD_3m_OIS"]
        ret["CIP_SEK"] = df["cip_sek_rf"] - df["USD_3m_OIS"]
        # ret.plot()

    return ret


def load_equity_sf(
    data_dir=DATA_DIR,
    raw=False,
):
    """
    Arbitrage spreads are reported in basis points.

    Reported as the Equity futures's implied forward rate minus OIS
    (here the OIS FWD calendar spread).

    Note that the 3m OIS can be used here and the results will be very similar.
    See the internet appendix of "Segmented Arbitrage" for a discussion of this.
    Note also that the paper doesn't use the Equity futures' implied risk-free rate
    because of a market timing issue (spot market closes at 4 pm ET and the futures
    market closes at 4:15 pm ET). Since this would introduce measurement
    error, they just use the futures implied forward rate. They can then
    use the OIS-implied forward, which they do here, but it's very similar
    to the 3m OIS anyway.

    From "compute_calendar_spread.do":
    *Label and output
    label var cal_spx_rf "SPX Equity-SF Implied Rf"
    label var cal_dow_rf "DJX Equity-SF Implied Rf"
    label var cal_ndaq_rf "NDAQ Equity-SF Implied Rf"
    label var ois_fwd_cal "Forward OIS Rate for Calendar Spread"

    """
    raise NotImplementedError
    filepath = (
        data_dir
        
        / "from_siriwardane_et_al"
        / "equity-sf"
        / "equity_sf_implied_rf.dta"
    )
    df_equity = pd.read_stata(filepath).set_index("date")

    ds = load_datastream.load_selected(data_dir=data_dir)
    ds = 100 * ds[["USD_3m_OIS"]]

    df = pd.concat([df_equity, ds], axis=1).dropna(subset=df_equity.columns, how="all")
    # df.plot()
    if raw:
        ret = df
    else:
        ret = pd.DataFrame(index=df.index)
        ret["Eq_SF_Dow"] = df["cal_dow_rf"] - df["ois_fwd_cal"]
        ret["Eq_SF_NDAQ"] = df["cal_ndaq_rf"] - df["ois_fwd_cal"]
        ret["Eq_SF_SPX"] = df["cal_spx_rf"] - df["ois_fwd_cal"]
        # ret.plot()
        # ret["2010":"2020"].plot()

    return ret


def load_tips_treasury(
    data_dir=DATA_DIR,
    raw=False,
):
    """Box Implied Rf - OIS, for 6m, 12m, and 18m
    Reported in basis points
    """
    raise NotImplementedError(
        "This isn't working right yet. Doesn't match plots from paper."
    )
    filepath = (
        data_dir
        
        / "from_siriwardane_et_al"
        / "tip-treasury"
        / "tips_treasury_implied_rf.dta"
    )
    df_tips = pd.read_stata(filepath).set_index("date")
    # df_tips[['tips_treas_2_rf', 'tips_treas_5_rf','tips_treas_10_rf', 'tips_treas_20_rf']].plot()
    df_tips.columns

    if raw:
        ret = df_tips
    else:
        ret = pd.DataFrame(index=df.index)
        ret["TIPS_Treasury_02y"] = df_tips["tips_treas_2_rf"] - df_tips["nom_zc2"]
        ret["TIPS_Treasury_05y"] = df_tips["tips_treas_5_rf"] - df_tips["nom_zc5"]
        ret["TIPS_Treasury_10y"] = df_tips["tips_treas_10_rf"] - df_tips["nom_zc10"]
        ret["TIPS_Treasury_20y"] = df_tips["tips_treas_20_rf"] - df_tips["nom_zc20"]
        # ret.plot()
        ret["2010":"2020"].plot()
    return ret


def load_treasury_sf(
    data_dir=DATA_DIR,
    raw=False,
):
    """
    Reported as Treasury Futures implied risk free rate minus the OIS rate
    """
    raise NotImplementedError("This doesn't match the paper's plot very well.")
    filepath = (
        data_dir
        
        / "from_siriwardane_et_al"
        / "treasury-sf"
        / "treasury_sf_implied_rf.dta"
    )
    df = pd.read_stata(filepath).set_index("date")
    if raw:
        ret = df
    else:
        maturities = [2, 5, 10, 20, 30]
        all_bases = []
        for maturity in maturities:
            df[f"Treasury_{maturity:02}Y_SF"] = (
                df[f"tfut_{maturity}_rf"] - df[f"tfut_ois_{maturity}"]
            )
            all_bases.append(f"Treasury_{maturity:02}Y_SF")
            # E.g., Treasury_02Y_SF
        ret = df[all_bases]
        # ret["2010":"2020"].plot()
    return ret


def load_treasury_swap():
    raise NotImplementedError
    filepath = (
        data_dir
        
        / "from_siriwardane_et_al"
        / "treasury-swap"
        / "tswap_implied_rf.dta"
    )
    df = pd.read_stata(filepath).set_index("date")
    df.info()


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
    Wide include extra variables.
    In the raw data, variables labeled "raw" are the raw spreads.
    Without raw means the absolute value has been applied.
    """
    data_dir = Path(data_dir)
    # filepath = (
    #     data_dir / "arbitrage_spread_wide.dta"
    # )
    filepath = "https://www.dropbox.com/scl/fi/81jm3dbe856i7p17rjy87/arbitrage_spread_wide.dta?rlkey=ke78u464vucmn43zt27nzkxya&st=59g2n7dt&dl=1"
    df = pd.read_stata(filepath).set_index("date")
    if raw:
        ret = df.copy()
    else:
        ret = df[list(name_map.keys())]
        if rename:
            ret = ret.rename(columns=name_map)
        ret = ret.reindex(sorted(ret.columns), axis=1)
    return ret


def load_combined_spreads_long(data_dir=DATA_DIR, rename=True):
    """
    Wide include extra variables.
    In the raw data, variables labeled "raw" are the raw spreads.
    Without raw means the absolute value has been applied.
    """
    #data_dir = Path(data_dir)
    # filepath = (
    #     data_dir
    #     / "arbitrage_spread_panel.dta"
    # )
    filepath = "https://www.dropbox.com/scl/fi/mv2oodkibhzli5ywdgxv7/arbitrage_spread_panel.dta?rlkey=ctzelvfie1nztlp7o24gvnzff&st=nnzdxv78&dl=1"
    df = pd.read_stata(filepath)
    df = df.rename()
    if rename:
        non_raw_name_map = {key.split("raw_")[1]:value for key, value in name_map.items()}
        df["full_trade"] = df["full_trade"].replace(non_raw_name_map)
    return df


def demo():
    # fxswap, fxbasis = read_usdjpyfxswap(DATA_DIR)
    # treasury_cash_futures_bases = read_treasury_cash_futures_bases(DATA_DIR)
    # interest_swap_spread_bases = read_interest_swap_spread_bases(DATA_DIR)
    # df_old = read_combined_basis_file_OLD(DATA_DIR)
    # df_old.plot()
    # df_old.columns
    # df_old.loc["2010":"2020", ['Treasury_SF_02Y', 'Treasury_SF_05Y', 'Treasury_SF_10Y', 'Treasury_SF_30Y']].plot()
    df = load_combined_spreads_wide(data_dir=DATA_DIR)
    df.columns
    df.loc["2010":"2020", ['Treasury_SF_10Y', 'Treasury_SF_02Y', 'Treasury_SF_20Y', 'Treasury_SF_30Y']].plot()
    
class TestDataCloseness(unittest.TestCase):

    def test_data_closeness(self):
        # Load the expected DataFrame using the function
        df_expected = load_combined_spreads_wide()
        # For demonstration, we'll assume df_bloomberg should be very close to df_expected.
        # In a real test, df_bloomberg would be produced by the code under test.
        df_bloomberg = compute_tips_treasury.import_inflation_swap_data()

        #Data cleaning
        df_expected = df_expected[[
            "Treasury_Swap_01Y",
            "Treasury_Swap_02Y",
            "Treasury_Swap_03Y",
            "Treasury_Swap_05Y",
            "Treasury_Swap_10Y",
            "Treasury_Swap_20Y",
            "Treasury_Swap_30Y",
        ]]
        df_bloomberg = df_bloomberg.rename(columns={
            "inf_swap_1y": "Treasury_Swap_01Y",
            "inf_swap_2y": "Treasury_Swap_02Y",
            "inf_swap_3y": "Treasury_Swap_03Y",
            "inf_swap_5y": "Treasury_Swap_05Y",
            "inf_swap_10y": "Treasury_Swap_10Y",
            "inf_swap_20y": "Treasury_Swap_20Y",
            "inf_swap_30y": "Treasury_Swap_30Y",
        })

        # Align the two DataFrames on their common dates
        common_dates = df_bloomberg.index.intersection(df_expected.index)
        df_bloomberg_aligned = df_bloomberg.loc[common_dates]
        df_expected_aligned = df_expected.loc[common_dates]

        # Convert all columns to numeric (non-convertible entries become NaN)
        df_bloomberg_aligned = df_bloomberg_aligned.apply(pd.to_numeric, errors='coerce')
        df_expected_aligned = df_expected_aligned.apply(pd.to_numeric, errors='coerce')

        # Select only numeric columns
        df_bloomberg_numeric = df_bloomberg_aligned.select_dtypes(include=[np.number])
        df_expected_numeric = df_expected_aligned.select_dtypes(include=[np.number])

        # Restrict to the common columns across both DataFrames
        common_cols = df_bloomberg_numeric.columns.intersection(df_expected_numeric.columns)
        df_bloomberg_numeric = df_bloomberg_numeric[common_cols]
        df_expected_numeric = df_expected_numeric[common_cols]

        # Test equality with a 0.1% tolerance
        are_equal = np.allclose(
            df_bloomberg_numeric.values,
            df_expected_numeric.values,
            rtol=0.001,
            equal_nan=True
        )

        self.assertTrue(are_equal, "DataFrames are not equal within 2% tolerance")

if __name__ == "__main__":
    unittest.main()
    #df = load_combined_spreads_wide(data_dir=OUTPUT_DIR)
    #path = config.OUTPUT_DIR / "pulled"
    # path.mkdir(parents=True, exist_ok=True)
    #df.to_parquet(path / "arbitrage_spread_wide.parquet")
    # df.dropna().to_parquet(path / "basis_data_combined_balanced.parquet")
    #pass
