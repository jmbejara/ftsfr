import pandas as pd
import requests
from io import BytesIO
from pathlib import Path

from settings import config
DATA_DIR = config('DATA_DIR')


def pull_fed_yield_curve():
    """
    Download the latest yield curve from the Federal Reserve
    
    This is the published data using Gurkaynak, Sack, and Wright (2007) model
    
    load in as: 
    "Treasury_SF_10Y",
    "Treasury_SF_02Y",
    "Treasury_SF_20Y",
    "Treasury_SF_03Y",
    "Treasury_SF_30Y",
    "Treasury_SF_05Y",
    """
    
    url = "https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv"
    response = requests.get(url)
    pdf_stream = BytesIO(response.content)
    df_all = pd.read_csv(pdf_stream, skiprows=9, index_col=0, parse_dates=True)

    cols = ['SVENY' + str(i).zfill(2) for i in range(1, 31)]
    df = df_all[cols]
    return df_all, df

def load_fed_yield_curve_all(data_dir=DATA_DIR):
    path = data_dir / "fed_yield_curve_all.parquet"
    _df = pd.read_parquet(path)
    
    # Select the specific columns. Note: SVENY03 is included so that
    # we can rename to "Treasury_SF_03Y" as requested.
    selected_cols = ['SVENY02', 'SVENY03', 'SVENY05', 'SVENY10', 'SVENY20', 'SVENY30']
    _df = _df[selected_cols]
    
    # Rename the columns to the desired names.
    rename_mapping = {
        'SVENY10': 'Treasury_SF_10Y',
        'SVENY02': 'Treasury_SF_02Y',
        'SVENY20': 'Treasury_SF_20Y',
        'SVENY03': 'Treasury_SF_03Y',
        'SVENY30': 'Treasury_SF_30Y',
        'SVENY05': 'Treasury_SF_05Y'
    }
    _df = _df.rename(columns=rename_mapping)
    
    return _df

def load_fed_yield_curve(data_dir=DATA_DIR):
    path = data_dir / "fed_yield_curve.parquet"
    _df = pd.read_parquet(path)
    return _df

def _demo():
    _df = pull_fed_yield_curve(data_dir=DATA_DIR)
    

if __name__ == "__main__":
    df_all, df = pull_fed_yield_curve()
    path = Path(DATA_DIR) / "fed_yield_curve_all.parquet"
    df_all.to_parquet(path)
    path = Path(DATA_DIR) / "fed_yield_curve.parquet"
    df.to_parquet(path)