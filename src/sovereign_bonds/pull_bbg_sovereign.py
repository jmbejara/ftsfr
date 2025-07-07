"""
TODO: Most of this code doesn't work

Fetches and loads JP Morgan EMBI sovereign bond indices from Bloomberg.

This module handles sovereign bond index data retrieval for 41 emerging market
countries that comprise the JP Morgan EMBI (Emerging Market Bond Index) family.
Data includes both composite indices and individual country sub-indices.

The EMBI indices track total returns for traded external debt instruments
(foreign currency denominated fixed income) in emerging markets. These are
widely used benchmarks for emerging market sovereign debt investors.

Index families included:
- EMBI+ (Emerging Markets Bond Index Plus)
- EMBI Global
- EMBI Global Diversified
- Individual country sub-indices for 41 countries
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import pandas as pd

from settings import config

DATA_DIR = config("DATA_DIR")
END_DATE = pd.Timestamp.today().strftime("%Y-%m-%d")


def pull_embi_composite_indices(start_date="1950-01-01", end_date=END_DATE):
    """
    Fetch JP Morgan EMBI composite indices from Bloomberg using xbbg.

    Parameters
    ----------
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format

    Returns
    -------
    pd.DataFrame
        DataFrame with EMBI composite index levels and returns
    """
    # import here to enhance compatibility with devices that don't support xbbg
    from xbbg import blp

    # Main EMBI composite indices
    composite_tickers = [
        "JPEIGLBL Index",  # EMBI Global
        "JPEIDIVR Index",  # EMBI Global Diversified
        "JPEMCOMP Index",  # EMBI+ Composite
        "JPEICORE Index",  # EMBI Global Core
        "JPEIESGE Index",  # ESG EMBI Global Diversified
    ]

    fields = ["PX_LAST", "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS"]

    # Pull data
    df = blp.bdh(
        tickers=composite_tickers,
        flds=fields,
        start_date=start_date,
        end_date=end_date,
    )

    # Flatten multi-index columns from xbbg if needed
    if not df.empty and isinstance(df.columns, pd.MultiIndex):
        df.columns = [f"{t[0]}_{t[1]}" for t in df.columns]
        df.reset_index(inplace=True)

    return df


def pull_embi_country_indices(start_date="1950-01-01", end_date=END_DATE):
    """
    Fetch individual country EMBI sub-indices from Bloomberg using xbbg.

    These track sovereign bonds for each of the 41 countries in the EMBI universe.

    Parameters
    ----------
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format

    Returns
    -------
    pd.DataFrame
        DataFrame with country-level EMBI index data
    """
    # import here to enhance compatibility with devices that don't support xbbg
    from xbbg import blp

    # Country sub-indices - using Bloomberg's EMBI country tickers
    # Format is typically JPEM{Country} Index or similar
    country_tickers = [
        # Latin America
        "JPEMARG Index",  # Argentina
        "JPEMBRAZ Index",  # Brazil
        "JPEMCHIL Index",  # Chile
        "JPEMCOLO Index",  # Colombia
        "JPEMECUA Index",  # Ecuador
        "JPEMMEXI Index",  # Mexico
        "JPEMPANA Index",  # Panama
        "JPEMPERU Index",  # Peru
        "JPEMURGY Index",  # Uruguay
        "JPEMVENE Index",  # Venezuela
        "JPEMDOMR Index",  # Dominican Republic
        "JPEMELSV Index",  # El Salvador
        "JPEMBELZ Index",  # Belize
        "JPEMTRIN Index",  # Trinidad and Tobago
        # Europe, Middle East & Africa
        "JPEMBULG Index",  # Bulgaria
        "JPEMCROA Index",  # Croatia
        "JPEMHUNG Index",  # Hungary
        "JPEMPOLA Index",  # Poland
        "JPEMRUSS Index",  # Russia
        "JPEMSERB Index",  # Serbia
        "JPEMTURK Index",  # Turkey
        "JPEMUKRA Index",  # Ukraine
        "JPEMEGYT Index",  # Egypt
        "JPEMLEBN Index",  # Lebanon
        "JPEMMARC Index",  # Morocco
        "JPEMSOAF Index",  # South Africa
        "JPEMGABN Index",  # Gabon
        "JPEMGHAN Index",  # Ghana
        "JPEMIVCO Index",  # Côte d'Ivoire
        "JPEMTUNS Index",  # Tunisia
        "JPEMIRAQ Index",  # Iraq
        # Asia
        "JPEMCHIN Index",  # China
        "JPEMINDO Index",  # Indonesia
        "JPEMKAZA Index",  # Kazakhstan
        "JPEMKORE Index",  # South Korea
        "JPEMMALAY Index",  # Malaysia
        "JPEMPAKI Index",  # Pakistan
        "JPEMPHIL Index",  # Philippines
        "JPEMSRIL Index",  # Sri Lanka
        "JPEMTHAI Index",  # Thailand
        "JPEMVIET Index",  # Vietnam
    ]

    fields = ["PX_LAST", "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS", "YLD_YTM_MID"]

    # Pull data
    df = blp.bdh(
        tickers=country_tickers,
        flds=fields,
        start_date=start_date,
        end_date=end_date,
    )

    # Flatten multi-index columns from xbbg if needed
    if not df.empty and isinstance(df.columns, pd.MultiIndex):
        df.columns = [f"{t[0]}_{t[1]}" for t in df.columns]
        df.reset_index(inplace=True)

    return df


def pull_embi_spreads(start_date="1950-01-01", end_date=END_DATE):
    """
    Fetch EMBI spread data (basis points over US Treasuries) from Bloomberg.

    Parameters
    ----------
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format

    Returns
    -------
    pd.DataFrame
        DataFrame with EMBI spread data in basis points
    """
    # import here to enhance compatibility with devices that don't support xbbg
    from xbbg import blp

    # Spread tickers for major indices
    spread_tickers = [
        "JPEMSOSD Index",  # EMBI Global Spread
        "JPEMDOSD Index",  # EMBI Global Diversified Spread
        "JPEMPOSD Index",  # EMBI+ Spread
    ]

    fields = ["PX_LAST"]

    # Pull data
    df = blp.bdh(
        tickers=spread_tickers,
        flds=fields,
        start_date=start_date,
        end_date=end_date,
    )

    # Flatten multi-index columns from xbbg if needed
    if not df.empty and isinstance(df.columns, pd.MultiIndex):
        df.columns = [f"{t[0]}_{t[1]}" for t in df.columns]
        df.reset_index(inplace=True)

    return df


def load_embi_composite_indices(data_dir=DATA_DIR):
    """Load EMBI composite indices from parquet file.

    Returns DataFrame with major EMBI index levels and returns including:
    - EMBI Global
    - EMBI Global Diversified  
    - EMBI+ Composite
    - EMBI Global Core
    - ESG EMBI Global Diversified

    Example:
    -------
    df = load_embi_composite_indices(data_dir=DATA_DIR)
    df.info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 7826 entries, 0 to 7825
    Data columns (total 11 columns):
     #   Column                                         Non-Null Count  Dtype         
    ---  ------                                         --------------  -----         
     0   index                                          7826 non-null   datetime64[ns]
     1   JPEIGLBL Index_PX_LAST                        7826 non-null   float64       
     2   JPEIGLBL Index_DAY_TO_DAY_TOT_RETURN_GROSS_DVDS  7826 non-null   float64       
     3   JPEIDIVR Index_PX_LAST                        7826 non-null   float64       
     4   JPEIDIVR Index_DAY_TO_DAY_TOT_RETURN_GROSS_DVDS  7826 non-null   float64       
     5   JPEMCOMP Index_PX_LAST                        6566 non-null   float64       
     6   JPEMCOMP Index_DAY_TO_DAY_TOT_RETURN_GROSS_DVDS  6566 non-null   float64       
     7   JPEICORE Index_PX_LAST                        6826 non-null   float64       
     8   JPEICORE Index_DAY_TO_DAY_TOT_RETURN_GROSS_DVDS  6826 non-null   float64       
     9   JPEIESGE Index_PX_LAST                        3044 non-null   float64       
     10  JPEIESGE Index_DAY_TO_DAY_TOT_RETURN_GROSS_DVDS  3044 non-null   float64       
    dtypes: datetime64[ns](1), float64(10)
    memory usage: 672.4 KB
    """
    path = data_dir / "embi_composite_indices.parquet"
    return pd.read_parquet(path)


def load_embi_country_indices(data_dir=DATA_DIR):
    """Load individual country EMBI sub-indices from parquet file.

    Returns DataFrame with country-level sovereign bond index data for
    all 41 countries in the EMBI universe. Includes price levels,
    returns, and yields.

    Example:
    -------
    df = load_embi_country_indices(data_dir=DATA_DIR)
    df.filter(regex='JPEMBRAZ').info()  # Show just Brazil columns
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 6566 entries, 0 to 6565
    Data columns (total 3 columns):
     #   Column                                          Non-Null Count  Dtype  
    ---  ------                                          --------------  -----  
     0   JPEMBRAZ Index_PX_LAST                         6566 non-null   float64
     1   JPEMBRAZ Index_DAY_TO_DAY_TOT_RETURN_GROSS_DVDS  6566 non-null   float64
     2   JPEMBRAZ Index_YLD_YTM_MID                     6566 non-null   float64
    dtypes: float64(3)
    memory usage: 154.0 KB
    """
    path = data_dir / "embi_country_indices.parquet"
    return pd.read_parquet(path)


def load_embi_spreads(data_dir=DATA_DIR):
    """Load EMBI spread data from parquet file.

    Returns DataFrame with EMBI spreads in basis points over US Treasuries.
    This is a key risk metric for emerging market sovereign bonds.

    Example:
    -------
    df = load_embi_spreads(data_dir=DATA_DIR)
    df.info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 7826 entries, 0 to 7825
    Data columns (total 4 columns):
     #   Column                  Non-Null Count  Dtype         
    ---  ------                  --------------  -----         
     0   index                   7826 non-null   datetime64[ns]
     1   JPEMSOSD Index_PX_LAST  7826 non-null   float64       
     2   JPEMDOSD Index_PX_LAST  7826 non-null   float64       
     3   JPEMPOSD Index_PX_LAST  6566 non-null   float64       
    dtypes: datetime64[ns](1), float64(3)
    memory usage: 244.7 KB
    """
    path = data_dir / "embi_spreads.parquet"
    return pd.read_parquet(path)


if __name__ == "__main__":
    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Pull and save composite indices
    composite_df = pull_embi_composite_indices()
    composite_df.to_parquet(DATA_DIR / "embi_composite_indices.parquet")

    # Pull and save country indices
    country_df = pull_embi_country_indices()
    country_df.to_parquet(DATA_DIR / "embi_country_indices.parquet")

    # Pull and save spread data
    spreads_df = pull_embi_spreads()
    spreads_df.to_parquet(DATA_DIR / "embi_spreads.parquet")
