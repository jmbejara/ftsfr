"""
pull_bbg_treas_swap.py

Pull and load Bloomberg Treasury and Swap yield data.

- pull_ functions ALWAYS fetch from Bloomberg and never touch disk.
- load_ functions ALWAYS load from disk and never fetch from external sources.
- Cleaning functions are pure transformations with no side effects.

All files are saved as Parquet in DATA_DIR.
"""

from datetime import date
from pathlib import Path

import pandas as pd

from settings import config

DATA_DIR: Path = config("DATA_DIR")
START_DATE: str = config("START_DATE", default="2000-01-01")
END_DATE: str = config("END_DATE", default=str(date.today()))


def pull_raw_tyields(
    start_date: str = START_DATE, end_date: str = END_DATE
) -> pd.DataFrame:
    """
    Pull raw Treasury yields from Bloomberg.

    Returns
    - pd.DataFrame: MultiIndex columns by ticker with daily PX_LAST values.
    """
    from xbbg import blp
    months = [1, 2, 3, 4, 6, 12]
    years = [2, 3, 5, 7, 10, 20, 30]
    tickers = [f"GB{x} Govt" for x in months] + [f"GT{x} Govt" for x in years]
    df = blp.bdh(
        tickers=tickers, flds=["PX_LAST"], start_date=start_date, end_date=end_date
    )
    # Align the former 12M bill series name with 1Y convention
    df = df.rename(columns={"GB12 Govt": "GT1 Govt"})
    return df


def pull_raw_syields(
    start_date: str = START_DATE, end_date: str = END_DATE
) -> pd.DataFrame:
    """
    Pull raw Swap yields from Bloomberg.

    Returns
    - pd.DataFrame: MultiIndex columns by ticker with daily PX_LAST values.
    """
    from xbbg import blp
    years = [1, 2, 3, 5, 10, 20, 30]
    tickers = [f"USSO{x} CMPN Curncy" for x in years]
    df = blp.bdh(
        tickers=tickers, flds=["PX_LAST"], start_date=start_date, end_date=end_date
    )
    return df


def clean_raw_tyields(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Treasury yields by coercing numeric dtypes.

    Parameters
    - raw_df (pd.DataFrame): Raw Treasury yields.

    Returns
    - pd.DataFrame: Cleaned Treasury yields.
    """
    return raw_df.apply(pd.to_numeric, errors="coerce")


def clean_raw_syields(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Swap yields by coercing numeric dtypes.

    Parameters
    - raw_df (pd.DataFrame): Raw Swap yields.

    Returns
    - pd.DataFrame: Cleaned Swap yields.
    """
    return raw_df.apply(pd.to_numeric, errors="coerce")


def load_raw_tyields(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """
    Load raw Treasury yields from disk.

    Parameters
    - data_dir (Path): Base data directory.

    Returns
    - pd.DataFrame: Raw Treasury yields.
    """
    return pd.read_parquet(data_dir / "raw_tyields.parquet")


def load_raw_syields(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """
    Load raw Swap yields from disk.

    Parameters
    - data_dir (Path): Base data directory.

    Returns
    - pd.DataFrame: Raw Swap yields.
    """
    return pd.read_parquet(data_dir / "raw_syields.parquet")


def load_tyields(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """
    Load cleaned Treasury yields from disk.

    Parameters
    - data_dir (Path): Base data directory.

    Returns
    - pd.DataFrame: Cleaned Treasury yields.
    """
    return pd.read_parquet(data_dir / "tyields.parquet")


def load_syields(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """
    Load cleaned Swap yields from disk.

    Parameters
    - data_dir (Path): Base data directory.

    Returns
    - pd.DataFrame: Cleaned Swap yields.
    """
    return pd.read_parquet(data_dir / "syields.parquet")


if __name__ == "__main__":
    # Pull, clean, and save
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    raw_t = pull_raw_tyields()
    raw_s = pull_raw_syields()

    # Save raw as Parquet
    raw_t.to_parquet(DATA_DIR / "raw_tyields.parquet")
    raw_s.to_parquet(DATA_DIR / "raw_syields.parquet")

    # Clean and save as Parquet for downstream format step
    t_clean = clean_raw_tyields(raw_t)
    s_clean = clean_raw_syields(raw_s)
    t_clean.to_parquet(DATA_DIR / "tyields.parquet")
    s_clean.to_parquet(DATA_DIR / "syields.parquet")
