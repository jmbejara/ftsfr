"""
Fetches and loads commodity futures data from Bloomberg.

This module handles futures price data retrieval for commodities including
energy, agriculture, livestock, and metals. It also pulls GSCI excess return
indices and LME metals spot/forward data.

Data includes:
- First, second, and third nearest futures contracts for 19 commodities
- LME metals spot and 3-month forward prices
- Goldman Sachs Commodity Index (GSCI) excess return indices
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import pandas as pd
import polars as pl
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
        "CO1 Comdty", "CO2 Comdty", "CO3 Comdty",  # Brent Crude
        "QS1 Comdty", "QS2 Comdty", "QS3 Comdty",  # Gasoil
        "CL1 Comdty", "CL2 Comdty", "CL3 Comdty",  # WTI Crude
        "XB1 Comdty", "XB2 Comdty", "XB3 Comdty",  # RBOB Gasoline
        "HO1 Comdty", "HO2 Comdty", "HO3 Comdty",  # Heating Oil
        "NG1 Comdty", "NG2 Comdty", "NG3 Comdty",  # Natural Gas
        # Agriculture
        "CT1 Comdty", "CT2 Comdty", "CT3 Comdty",  # Cotton
        "KC1 Comdty", "KC2 Comdty", "KC3 Comdty",  # Coffee
        "CC1 Comdty", "CC2 Comdty", "CC3 Comdty",  # Cocoa
        "SB1 Comdty", "SB2 Comdty", "SB3 Comdty",  # Sugar
        "S1 Comdty", "S2 Comdty", "S3 Comdty",     # Soybeans
        "KW1 Comdty", "KW2 Comdty", "KW3 Comdty",  # Kansas Wheat
        "C1 Comdty", "C2 Comdty", "C3 Comdty",     # Corn
        "W1 Comdty", "W2 Comdty", "W3 Comdty",     # Wheat
        # Livestock
        "LH1 Comdty", "LH2 Comdty", "LH3 Comdty",  # Lean Hogs
        "FC1 Comdty", "FC2 Comdty", "FC3 Comdty",  # Feeder Cattle
        "LC1 Comdty", "LC2 Comdty", "LC3 Comdty",  # Live Cattle
        # Metals
        "GC1 Comdty", "GC2 Comdty", "GC3 Comdty",  # Gold
        "SI1 Comdty", "SI2 Comdty", "SI3 Comdty",  # Silver
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
        "LMAHDY", "LMAHDS03",     # Aluminum spot and 3mo
        "LMNIDY", "LMNIDS03",     # Nickel spot and 3mo
        "LMPBDY", "LMPBDS03",     # Lead spot and 3mo
        "LMZSDY", "LMZSDS03",     # Zinc spot and 3mo
        "LMCADY", "LMCADS03",     # Copper spot and 3mo
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
        "SPGCBRP Index",   # Brent Crude Oil
        "SPGCGOP Index",   # Gasoil
        "SPGCCLP Index",   # WTI Crude
        "SPGCHUP Index",   # Unleaded Gasoline
        "SPGCHOP Index",   # Heating Oil
        "SPGCNGP Index",   # Natural Gas
        "SPGCCTP Index",   # Cotton
        "SPGCKCP Index",   # Coffee
        "SPGCCCP Index",   # Cocoa
        "SPGCSBP Index",   # Sugar
        "SPGCSOP Index",   # Soybeans
        "SPGCKWP Index",   # Kansas Wheat
        "SPGCCNP Index",   # Corn
        "SPGCWHP Index",   # Wheat
        "SPGCLHP Index",   # Lean Hogs
        "SPGCFCP Index",   # Feeder Cattle
        "SPGCLCP Index",   # Live Cattle
        "SPGCGCP Index",   # Gold
        "SPGCSIP Index",   # Silver
        "SPGCIAP Index",   # Aluminum
        "SPGCIKP Index",   # Nickel
        "SPGCILP Index",   # Lead
        "SPGCIZP Index",   # Zinc
        "SPGCICP Index",   # Copper
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
    df = pl.from_pandas(df)
    df.select(["index", "CO1 Comdty_PX_LAST", "CO2 Comdty_PX_LAST", "CO3 Comdty_PX_LAST"]).glimpse()
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
    df = pl.from_pandas(df)
    df.select(["index", "LMAHDY_PX_LAST", "LMAHDS03_PX_LAST"]).glimpse()
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
    df = pl.from_pandas(df)
    df.select(["index", "SPGCBRP Index_PX_LAST", "SPGCCLP Index_PX_LAST"]).glimpse()
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
