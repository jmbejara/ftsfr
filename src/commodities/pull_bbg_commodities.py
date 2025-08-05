"""
Fetches and loads commodity futures data from Bloomberg.

This module handles futures price data retrieval for commodities including
energy, agriculture, livestock, and metals. It also pulls GSCI excess return
indices and LME metals spot/forward data.

Data includes:
- First, second, and third nearest futures contracts for 19 commodities
- LME metals spot and 3-month forward prices
- Goldman Sachs Commodity Index (GSCI) excess return indices


TODO: Yangge, check to see if the commodities in this table are all pulled in the code below.

Sector Commodity Symbol N Basis Freq. of bw. Excess returns Volatility Sharpe ratio (%)
Agriculture Canola WC 97 0.12 83.02 -0.73 19.37 -3.75
Cocoa CC 160 -0.01 25.43 4.52 30.19 14.98
Coffee KC 149 0.08 81.88 6.45 35.96 17.95
Corn C- 152 0.30 99.57 -1.10 24.09 -4.55
Cotton CT 170 0.07 78.21 2.07 23.17 8.93
Lumber LB 114 -0.01 31.50 3.71 24.88 14.90
Oats O- 119 -0.03 44.42 0.06 29.57 0.22
Orange juice JO 178 -0.05 23.50 1.55 30.54 5.09
Rough rice RR 119 0.35 97.08 -1.23 25.56 -4.82
Soybean meal SM 191 -0.19 0.43 6.81 30.71 22.18
Soybeans S- 182 -0.01 34.62 4.53 27.42 16.51
Wheat W- 133 0.45 98.72 1.75 24.18 7.25
Energy Crude Oil CL 241 0.13 85.48 12.54 32.41 38.68
Gasoline RB 251 -0.09 0.00 -11.35 40.52 -28.02
Heating Oil HO 246 -0.02 30.37 12.33 31.85 38.72
Natural gas NG 250 0.48 96.89 2.26 49.33 4.59
Unleaded gas HU 198 0.01 69.64 9.94 29.24 33.98
Livestock Feeder cattle FC 141 0.18 97.75 3.55 16.02 22.13
Lean hogs LH 175 0.34 97.07 5.81 20.93 27.78
Live cattle LC 136 0.08 85.47 5.52 15.81 34.93
Metals Aluminium AL 252 0.05 100.00 -2.76 18.04 -15.28
Copper HG 197 -0.03 31.12 8.92 24.94 35.78
Gold GC 229 -0.03 7.84 0.28 19.10 1.44
Palladium PA 69 0.19 77.29 6.98 30.56 22.85
Platinum PL 78 -0.17 17.95 5.66 21.53 26.30
Silver SI 198 0.12 99.51 1.56 30.79 5.07

"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import pandas as pd

from settings import config

DATA_DIR = config("DATA_DIR")
END_DATE = pd.Timestamp.today().strftime("%Y-%m-%d")


def pull_commodity_futures(start_date="1950-01-01", end_date=END_DATE):
    """
    Fetch historical commodity futures prices from Bloomberg using xbbg.

    Parameters
    ----------
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format

    Returns
    -------
    pd.DataFrame
        DataFrame with prices for 1st, 2nd, 3rd nearest contracts
    """
    # import here to enhance compatibility with devices that don't support xbbg
    from xbbg import blp

    # Commodity futures tickers (1st, 2nd, 3rd nearest contracts)
    commodity_futures_tickers = [
        # Energy
        "CO1 Comdty",
        "CO2 Comdty",
        "CO3 Comdty",  # Brent Crude
        "QS1 Comdty",
        "QS2 Comdty",
        "QS3 Comdty",  # Gasoil
        "CL1 Comdty",
        "CL2 Comdty",
        "CL3 Comdty",  # WTI Crude
        "XB1 Comdty",
        "XB2 Comdty",
        "XB3 Comdty",  # RBOB Gasoline
        "HO1 Comdty",
        "HO2 Comdty",
        "HO3 Comdty",  # Heating Oil
        "NG1 Comdty",
        "NG2 Comdty",
        "NG3 Comdty",  # Natural Gas
        # Agriculture
        "CT1 Comdty",
        "CT2 Comdty",
        "CT3 Comdty",  # Cotton
        "KC1 Comdty",
        "KC2 Comdty",
        "KC3 Comdty",  # Coffee
        "CC1 Comdty",
        "CC2 Comdty",
        "CC3 Comdty",  # Cocoa
        "SB1 Comdty",
        "SB2 Comdty",
        "SB3 Comdty",  # Sugar
        "S 1 Comdty",
        "S 2 Comdty",
        "S 3 Comdty",  # Soybeans
        "KW1 Comdty",
        "KW2 Comdty",
        "KW3 Comdty",  # Kansas Wheat
        "C 1 Comdty",
        "C 2 Comdty",
        "C 3 Comdty",  # Corn
        "W 1 Comdty",
        "W 2 Comdty",
        "W 3 Comdty",  # Wheat
        # Livestock
        "LH1 Comdty",
        "LH2 Comdty",
        "LH3 Comdty",  # Lean Hogs
        "FC1 Comdty",
        "FC2 Comdty",
        "FC3 Comdty",  # Feeder Cattle
        "LC1 Comdty",
        "LC2 Comdty",
        "LC3 Comdty",  # Live Cattle
        # Metals
        "GC1 Comdty",
        "GC2 Comdty",
        "GC3 Comdty",  # Gold
        "SI1 Comdty",
        "SI2 Comdty",
        "SI3 Comdty",  # Silver
    ]

    fields = ["PX_LAST"]

    # Pull data
    df = blp.bdh(
        tickers=commodity_futures_tickers,
        flds=fields,
        start_date=start_date,
        end_date=end_date,
    )

    # Flatten multi-index columns from xbbg if needed
    if not df.empty and isinstance(df.columns, pd.MultiIndex):
        df.columns = [f"{t[0]}_{t[1]}" for t in df.columns]
        df.reset_index(inplace=True)

    return df


def pull_lme_metals(start_date="1950-01-01", end_date=END_DATE):
    """
    Fetch LME metals spot and 3-month forward prices from Bloomberg using xbbg.

    Parameters
    ----------
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format

    Returns
    -------
    pd.DataFrame
        DataFrame with LME spot and 3-month forward prices
    """
    # import here to enhance compatibility with devices that don't support xbbg
    from xbbg import blp

    # LME metals tickers (spot and 3-month forward)
    lme_metals_tickers = [
        "LMAHDY Comdty",
        "LMAHDS03 Comdty",  # Aluminum spot and 3mo
        "LMNIDY Comdty",
        "LMNIDS03 Comdty",  # Nickel spot and 3mo
        "LMPBDY Comdty",
        "LMPBDS03 Comdty",  # Lead spot and 3mo
        "LMZSDY Comdty",
        "LMZSDS03 Comdty",  # Zinc spot and 3mo
        "LMCADY Comdty",
        "LMCADS03 Comdty",  # Copper spot and 3mo
    ]

    fields = ["PX_LAST"]

    # Pull data
    df = blp.bdh(
        tickers=lme_metals_tickers,
        flds=fields,
        start_date=start_date,
        end_date=end_date,
    )

    # Flatten multi-index columns from xbbg if needed
    if not df.empty and isinstance(df.columns, pd.MultiIndex):
        df.columns = [f"{t[0]}_{t[1]}" for t in df.columns]
        df.reset_index(inplace=True)

    return df


def pull_gsci_indices(start_date="1950-01-01", end_date=END_DATE):
    """
    Fetch Goldman Sachs Commodity Index excess returns from Bloomberg using xbbg.

    Parameters
    ----------
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format

    Returns
    -------
    pd.DataFrame
        DataFrame with GSCI excess return indices
    """
    # import here to enhance compatibility with devices that don't support xbbg
    from xbbg import blp

    # GSCI excess return indices
    gsci_indices_tickers = [
        "SPGCBRP Index",  # Brent Crude Oil
        "SPGCGOP Index",  # Gasoil
        "SPGCCLP Index",  # WTI Crude
        "SPGCHUP Index",  # Unleaded Gasoline
        "SPGCHOP Index",  # Heating Oil
        "SPGCNGP Index",  # Natural Gas
        "SPGCCTP Index",  # Cotton
        "SPGCKCP Index",  # Coffee
        "SPGCCCP Index",  # Cocoa
        "SPGCSBP Index",  # Sugar
        "SPGCSOP Index",  # Soybeans
        "SPGCKWP Index",  # Kansas Wheat
        "SPGCCNP Index",  # Corn
        "SPGCWHP Index",  # Wheat
        "SPGCLHP Index",  # Lean Hogs
        "SPGCFCP Index",  # Feeder Cattle
        "SPGCLCP Index",  # Live Cattle
        "SPGCGCP Index",  # Gold
        "SPGCSIP Index",  # Silver
        "SPGCIAP Index",  # Aluminum
        "SPGCIKP Index",  # Nickel
        "SPGCILP Index",  # Lead
        "SPGCIZP Index",  # Zinc
        "SPGCICP Index",  # Copper
    ]

    fields = ["PX_LAST"]

    # Pull data
    df = blp.bdh(
        tickers=gsci_indices_tickers,
        flds=fields,
        start_date=start_date,
        end_date=end_date,
    )

    # Flatten multi-index columns from xbbg if needed
    if not df.empty and isinstance(df.columns, pd.MultiIndex):
        df.columns = [f"{t[0]}_{t[1]}" for t in df.columns]
        df.reset_index(inplace=True)

    return df


def load_commodity_futures(data_dir=DATA_DIR):
    """Load commodity futures prices from parquet file.

    Returns DataFrame with columns for each commodity's 1st, 2nd, and 3rd
    nearest contracts. Column names follow pattern: {TICKER}_PX_LAST

    Example:
    -------
    df = load_commodity_futures(data_dir=DATA_DIR)
    df.info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 16858 entries, 0 to 16857
    Data columns (total 58 columns):
    #   Column              Non-Null Count  Dtype
    ---  ------              --------------  -----
    0   index               16858 non-null  object
    1   CO1 Comdty_PX_LAST  9465 non-null   float64
    2   CO2 Comdty_PX_LAST  9466 non-null   float64
    3   CO3 Comdty_PX_LAST  9346 non-null   float64
    4   QS1 Comdty_PX_LAST  9206 non-null   float64
    5   QS2 Comdty_PX_LAST  9205 non-null   float64
    6   QS3 Comdty_PX_LAST  9205 non-null   float64
    7   CL1 Comdty_PX_LAST  10598 non-null  float64
    8   CL2 Comdty_PX_LAST  10622 non-null  float64
    9   CL3 Comdty_PX_LAST  10621 non-null  float64
    10  XB1 Comdty_PX_LAST  4974 non-null   float64
    11  XB2 Comdty_PX_LAST  4974 non-null   float64
    12  XB3 Comdty_PX_LAST  4974 non-null   float64
    13  HO1 Comdty_PX_LAST  9804 non-null   float64
    14  HO2 Comdty_PX_LAST  9805 non-null   float64
    15  HO3 Comdty_PX_LAST  9805 non-null   float64
    16  NG1 Comdty_PX_LAST  8856 non-null   float64
    17  NG2 Comdty_PX_LAST  8860 non-null   float64
    18  NG3 Comdty_PX_LAST  8861 non-null   float64
    19  CT1 Comdty_PX_LAST  16564 non-null  float64
    20  CT2 Comdty_PX_LAST  16584 non-null  float64
    21  CT3 Comdty_PX_LAST  16521 non-null  float64
    22  KC1 Comdty_PX_LAST  13109 non-null  float64
    23  KC2 Comdty_PX_LAST  13246 non-null  float64
    24  KC3 Comdty_PX_LAST  13229 non-null  float64
    25  CC1 Comdty_PX_LAST  16361 non-null  float64
    26  CC2 Comdty_PX_LAST  16470 non-null  float64
    27  CC3 Comdty_PX_LAST  16462 non-null  float64
    28  SB1 Comdty_PX_LAST  16128 non-null  float64
    29  SB2 Comdty_PX_LAST  16127 non-null  float64
    30  SB3 Comdty_PX_LAST  16077 non-null  float64
    31  S 1 Comdty_PX_LAST  16630 non-null  float64
    32  S 2 Comdty_PX_LAST  16629 non-null  float64
    33  S 3 Comdty_PX_LAST  16630 non-null  float64
    34  KW1 Comdty_PX_LAST  13974 non-null  float64
    35  KW2 Comdty_PX_LAST  13980 non-null  float64
    36  KW3 Comdty_PX_LAST  13980 non-null  float64
    37  C 1 Comdty_PX_LAST  16629 non-null  float64
    38  C 2 Comdty_PX_LAST  16632 non-null  float64
    39  C 3 Comdty_PX_LAST  16632 non-null  float64
    40  W 1 Comdty_PX_LAST  16629 non-null  float64
    41  W 2 Comdty_PX_LAST  16633 non-null  float64
    42  W 3 Comdty_PX_LAST  16632 non-null  float64
    43  LH1 Comdty_PX_LAST  9899 non-null   float64
    44  LH2 Comdty_PX_LAST  9879 non-null   float64
    45  LH3 Comdty_PX_LAST  9860 non-null   float64
    46  FC1 Comdty_PX_LAST  13461 non-null  float64
    47  FC2 Comdty_PX_LAST  13508 non-null  float64
    48  FC3 Comdty_PX_LAST  13474 non-null  float64
    49  LC1 Comdty_PX_LAST  15272 non-null  float64
    50  LC2 Comdty_PX_LAST  15273 non-null  float64
    51  LC3 Comdty_PX_LAST  15270 non-null  float64
    52  GC1 Comdty_PX_LAST  12635 non-null  float64
    53  GC2 Comdty_PX_LAST  12696 non-null  float64
    54  GC3 Comdty_PX_LAST  12696 non-null  float64
    55  SI1 Comdty_PX_LAST  12654 non-null  float64
    56  SI2 Comdty_PX_LAST  12698 non-null  float64
    57  SI3 Comdty_PX_LAST  12697 non-null  float64
    dtypes: float64(57), object(1)
    memory usage: 7.5+ MB
    """
    path = data_dir / "commodity_futures.parquet"
    return pd.read_parquet(path)


def load_lme_metals(data_dir=DATA_DIR):
    """Load LME metals spot and 3-month forward prices from parquet file.

    Returns DataFrame with columns for each metal's spot and 3-month forward
    prices. LME uses different contract structure than other commodities.

    Example:
    -------
    df = load_lme_metals(data_dir=DATA_DIR)
    df.info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 9919 entries, 0 to 9918
    Data columns (total 11 columns):
    #   Column                   Non-Null Count  Dtype
    ---  ------                   --------------  -----
    0   index                    9919 non-null   object
    1   LMAHDY Comdty_PX_LAST    9538 non-null   float64
    2   LMAHDS03 Comdty_PX_LAST  9615 non-null   float64
    3   LMNIDY Comdty_PX_LAST    9704 non-null   float64
    4   LMNIDS03 Comdty_PX_LAST  9707 non-null   float64
    5   LMPBDY Comdty_PX_LAST    9709 non-null   float64
    6   LMPBDS03 Comdty_PX_LAST  9706 non-null   float64
    7   LMZSDY Comdty_PX_LAST    9212 non-null   float64
    8   LMZSDS03 Comdty_PX_LAST  9214 non-null   float64
    9   LMCADY Comdty_PX_LAST    9902 non-null   float64
    10  LMCADS03 Comdty_PX_LAST  9899 non-null   float64
    dtypes: float64(10), object(1)
    memory usage: 852.5+ KB
    """
    path = data_dir / "lme_metals.parquet"
    return pd.read_parquet(path)


def load_gsci_indices(data_dir=DATA_DIR):
    """Load Goldman Sachs Commodity Index excess returns from parquet file.

    Returns DataFrame with GSCI excess return indices for each commodity.
    These are total return indices excluding collateral interest.

    Example:
    -------
    df = load_gsci_indices(data_dir=DATA_DIR)
    df.info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 15272 entries, 0 to 15271
    Data columns (total 25 columns):
    #   Column                 Non-Null Count  Dtype
    ---  ------                 --------------  -----
    0   index                  15272 non-null  object
    1   SPGCBRP Index_PX_LAST  6660 non-null   float64
    2   SPGCGOP Index_PX_LAST  6660 non-null   float64
    3   SPGCCLP Index_PX_LAST  9695 non-null   float64
    4   SPGCHUP Index_PX_LAST  9442 non-null   float64
    5   SPGCHOP Index_PX_LAST  10705 non-null  float64
    6   SPGCNGP Index_PX_LAST  7924 non-null   float64
    7   SPGCCTP Index_PX_LAST  12217 non-null  float64
    8   SPGCKCP Index_PX_LAST  11212 non-null  float64
    9   SPGCCCP Index_PX_LAST  10454 non-null  float64
    10  SPGCSBP Index_PX_LAST  13224 non-null  float64
    11  SPGCSOP Index_PX_LAST  13982 non-null  float64
    12  SPGCKWP Index_PX_LAST  6660 non-null   float64
    13  SPGCCNP Index_PX_LAST  13982 non-null  float64
    14  SPGCWHP Index_PX_LAST  13982 non-null  float64
    15  SPGCLHP Index_PX_LAST  12470 non-null  float64
    16  SPGCFCP Index_PX_LAST  5907 non-null   float64
    17  SPGCLCP Index_PX_LAST  13982 non-null  float64
    18  SPGCGCP Index_PX_LAST  11966 non-null  float64
    19  SPGCSIP Index_PX_LAST  13225 non-null  float64
    20  SPGCIAP Index_PX_LAST  8685 non-null   float64
    21  SPGCIKP Index_PX_LAST  8177 non-null   float64
    22  SPGCILP Index_PX_LAST  7672 non-null   float64
    23  SPGCIZP Index_PX_LAST  8684 non-null   float64
    24  SPGCICP Index_PX_LAST  12217 non-null  float64
    dtypes: float64(24), object(1)
    memory usage: 2.9+ MB
    """
    path = data_dir / "gsci_indices.parquet"
    return pd.read_parquet(path)


if __name__ == "__main__":
    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Pull and save commodity futures data
    commodity_futures_df = pull_commodity_futures()
    commodity_futures_df.to_parquet(DATA_DIR / "commodity_futures.parquet")

    # Pull and save LME metals data
    lme_metals_df = pull_lme_metals()
    lme_metals_df.to_parquet(DATA_DIR / "lme_metals.parquet")

    # Pull and save GSCI indices data
    gsci_indices_df = pull_gsci_indices()
    gsci_indices_df.to_parquet(DATA_DIR / "gsci_indices.parquet")
