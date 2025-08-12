"""
pull_bbg_commodities_basis.py

Purpose
-------
Pulls both futures prices and spot (or spot-proxy) prices for a broad set of
commodities so basis can be computed consistently: Basis = Futures − Spot.

What this module pulls
----------------------
- Generic futures (1st/2nd/3rd nearby) for energy, agriculture, livestock, metals
  using Bloomberg `Comdty` tickers (e.g., "CL1 Comdty").
- LME metals spot and 3-month forward prices for base metals (Al, Ni, Pb, Zn, Cu)
  using Bloomberg `Comdty` tickers (e.g., "LMCADY Comdty", "LMCADS03 Comdty").
- GSCI Excess Return indices as supplemental series for many commodities
  (e.g., "SPGCCLP Index").
- Precious metals USD spot for Gold, Silver, Platinum, Palladium using
  Bloomberg `Curncy` tickers ("XAUUSD Curncy", "XAGUSD Curncy",
  "XPTUSD Curncy", "XPDUSD Curncy").
- Spot proxies for commodities lacking reliable Bloomberg spot series by
  extracting the 1st generic futures from the pulled futures panel.

Notes on basis construction
---------------------------
- For LME base metals: use LME spot vs 1st generic futures.
- For precious metals: use USD spot (XAU/XAG/XPT/XPD) vs 1st generic futures.
- For other commodities where no robust spot is available from Bloomberg in this
  module, we provide a transparent spot-proxy constructed from the 1st generic
  futures. This enables basis calculation but is a proxy rather than true cash.
  If true spot sources are required later (e.g., location-specific cash quotes),
  add a dedicated pull function and replace the proxy.
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
        "RB1 Comdty",
        "RB2 Comdty",
        "RB3 Comdty",  # Gasoline (RBOB)
        "XB1 Comdty",
        "XB2 Comdty",
        "XB3 Comdty",  # RBOB Gasoline
        "HO1 Comdty",
        "HO2 Comdty",
        "HO3 Comdty",  # Heating Oil
        "NG1 Comdty",
        "NG2 Comdty",
        "NG3 Comdty",  # Natural Gas
        "HU1 Comdty",
        "HU2 Comdty",
        "HU3 Comdty",  # Unleaded Gas
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
        "LB1 Comdty",
        "LB2 Comdty",
        "LB3 Comdty",  # Lumber
        "O 1 Comdty",
        "O 2 Comdty",
        "O 3 Comdty",  # Oats
        "JO1 Comdty",
        "JO2 Comdty",
        "JO3 Comdty",  # Orange Juice
        "RR1 Comdty",
        "RR2 Comdty",
        "RR3 Comdty",  # Rough Rice
        "SM1 Comdty",
        "SM2 Comdty",
        "SM3 Comdty",  # Soybean Meal
        "WC1 Comdty",
        "WC2 Comdty",
        "WC3 Comdty",  # Canola
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
        "AL1 Comdty",
        "AL2 Comdty",
        "AL3 Comdty",  # Aluminium
        "HG1 Comdty",
        "HG2 Comdty",
        "HG3 Comdty",  # Copper
        "GC1 Comdty",
        "GC2 Comdty",
        "GC3 Comdty",  # Gold
        "SI1 Comdty",
        "SI2 Comdty",
        "SI3 Comdty",  # Silver
        "PA1 Comdty",
        "PA2 Comdty",
        "PA3 Comdty",  # Palladium
        "PL1 Comdty",
        "PL2 Comdty",
        "PL3 Comdty",  # Platinum
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


def pull_precious_metals_spot(start_date="1950-01-01", end_date=END_DATE):
    """
    Fetch USD spot prices for precious metals using Bloomberg `Curncy` tickers.

    Includes Gold (XAU), Silver (XAG), Platinum (XPT), Palladium (XPD).

    Returns a wide DataFrame with PX_LAST columns and a date index reset to
    an "index" column.
    """
    from xbbg import blp

    tickers = [
        "XAUUSD Curncy",  # Gold spot USD
        "XAGUSD Curncy",  # Silver spot USD
        "XPTUSD Curncy",  # Platinum spot USD
        "XPDUSD Curncy",  # Palladium spot USD
    ]

    fields = ["PX_LAST"]

    df = blp.bdh(tickers=tickers, flds=fields, start_date=start_date, end_date=end_date)

    if not df.empty and isinstance(df.columns, pd.MultiIndex):
        df.columns = [f"{t[0]}_{t[1]}" for t in df.columns]
        df.reset_index(inplace=True)

    return df


def build_spot_proxies_from_futures_df(df_futures: pd.DataFrame) -> pd.DataFrame:
    """
    Construct spot proxies by extracting 1st generic futures series from the
    futures panel. This is a transparent proxy for commodities lacking a robust
    Bloomberg spot series.

    The function expects a wide DataFrame as returned by `pull_commodity_futures`.
    It selects columns that end with "1 Comdty_PX_LAST" and returns a new wide
    DataFrame (including the date column named "index").
    """
    if df_futures is None or df_futures.empty:
        return df_futures

    date_col = "index" if "index" in df_futures.columns else df_futures.columns[0]
    proxy_cols = [
        c for c in df_futures.columns if c != date_col and c.endswith("1 Comdty_PX_LAST")
    ]

    cols = [date_col] + proxy_cols
    return df_futures[cols].copy()


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


def load_precious_metals_spot(data_dir=DATA_DIR):
    """Load precious metals USD spot prices from parquet file."""
    path = data_dir / "precious_metals_spot.parquet"
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


def load_commodity_spot_proxies(data_dir=DATA_DIR):
    """Load spot proxies (1st generic futures) from parquet file."""
    path = data_dir / "commodity_spot_proxies.parquet"
    return pd.read_parquet(path)


def compute_basis_series(
    futures_df: pd.DataFrame,
    futures_col: str,
    spot_df: pd.DataFrame,
    spot_col: str,
    date_col: str = "index",
) -> pd.DataFrame:
    """Compute basis = futures − spot for a single pair of columns.

    Returns a DataFrame with columns: [date_col, futures_col, spot_col, "basis"].
    """
    merged = (
        futures_df[[date_col, futures_col]]
        .merge(spot_df[[date_col, spot_col]], on=date_col, how="inner")
        .copy()
    )
    merged["basis"] = merged[futures_col] - merged[spot_col]
    return merged


def compute_precious_metals_basis(
    futures_df: pd.DataFrame, precious_spot_df: pd.DataFrame, date_col: str = "index"
) -> dict[str, pd.DataFrame]:
    """Compute basis for precious metals using USD spot:

    - GC1 Comdty vs XAUUSD Curncy
    - SI1 Comdty vs XAGUSD Curncy
    - PL1 Comdty vs XPTUSD Curncy
    - PA1 Comdty vs XPDUSD Curncy

    Returns a dict mapping commodity roots to basis DataFrames.
    """
    mapping: list[tuple[str, str, str]] = [
        ("GC1 Comdty_PX_LAST", "XAUUSD Curncy_PX_LAST", "GC"),
        ("SI1 Comdty_PX_LAST", "XAGUSD Curncy_PX_LAST", "SI"),
        ("PL1 Comdty_PX_LAST", "XPTUSD Curncy_PX_LAST", "PL"),
        ("PA1 Comdty_PX_LAST", "XPDUSD Curncy_PX_LAST", "PA"),
    ]

    out: dict[str, pd.DataFrame] = {}
    for fut_col, spot_col, root in mapping:
        if fut_col in futures_df.columns and spot_col in precious_spot_df.columns:
            out[root] = compute_basis_series(
                futures_df, fut_col, precious_spot_df, spot_col, date_col=date_col
            )
    return out


def compute_lme_base_metals_basis(
    futures_df: pd.DataFrame, lme_df: pd.DataFrame, date_col: str = "index"
) -> dict[str, pd.DataFrame]:
    """Compute basis for LME base metals using LME spot series:

    - AL1 Comdty vs LMAHDY Comdty (Aluminum)
    - HG1 Comdty vs LMCADY Comdty (Copper)

    Returns a dict mapping commodity roots to basis DataFrames.
    """
    mapping: list[tuple[str, str, str]] = [
        ("AL1 Comdty_PX_LAST", "LMAHDY Comdty_PX_LAST", "AL"),
        ("HG1 Comdty_PX_LAST", "LMCADY Comdty_PX_LAST", "HG"),
    ]

    out: dict[str, pd.DataFrame] = {}
    for fut_col, spot_col, root in mapping:
        if fut_col in futures_df.columns and spot_col in lme_df.columns:
            out[root] = compute_basis_series(
                futures_df, fut_col, lme_df, spot_col, date_col=date_col
            )
    return out


if __name__ == "__main__":
    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Pull and save commodity futures data
    commodity_futures_df = pull_commodity_futures()
    commodity_futures_df.to_parquet(DATA_DIR / "commodity_futures.parquet")

    # Derive and save spot proxies from 1st generic futures
    spot_proxies_df = build_spot_proxies_from_futures_df(commodity_futures_df)
    spot_proxies_df.to_parquet(DATA_DIR / "commodity_spot_proxies.parquet")

    # Pull and save LME metals data
    lme_metals_df = pull_lme_metals()
    lme_metals_df.to_parquet(DATA_DIR / "lme_metals.parquet")

    # Pull and save precious metals USD spot data
    precious_spot_df = pull_precious_metals_spot()
    precious_spot_df.to_parquet(DATA_DIR / "precious_metals_spot.parquet")

    # Pull and save GSCI indices data
    gsci_indices_df = pull_gsci_indices()
    gsci_indices_df.to_parquet(DATA_DIR / "gsci_indices.parquet")
