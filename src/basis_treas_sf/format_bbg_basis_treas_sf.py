"""
format_bbg_basis_treas_sf.py

Format and combine individual Bloomberg data files into consolidated datasets.

This script takes the individual parquet files created by pull_bbg_basis_treas_sf.py
and combines them into a single consolidated dataset with proper column naming
and additional derived fields.

Inputs (from DATA_DIR/basis_treas_sf):
- ois.parquet: USD OIS rates
- treasury_2y.parquet: 2Y Treasury futures data
- treasury_5y.parquet: 5Y Treasury futures data
- treasury_10y.parquet: 10Y Treasury futures data
- treasury_20y.parquet: 20Y Treasury futures data (Ultra 10Y proxy)
- treasury_30y.parquet: 30Y Treasury futures data

Outputs (saved under DATA_DIR/basis_treas_sf):
- treasury_df.parquet: Combined Treasury futures data with all tenors
- last_day.parquet: Mapping of (Mat_Year, Mat_Month) -> Mat_Day (last calendar day)
- treasury_df.csv: CSV version of combined data
- treasury_df.xlsx: Excel version of combined data

Process:
1. Load individual tenor files
2. Combine all tenors on Date column
3. Rename OIS columns to compact labels
4. Add derived Contract columns for quarter cycle
5. Build last day mapping for maturity calculations
6. Save in multiple formats (parquet, CSV, Excel)
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from functools import reduce

from settings import config


# Configuration via settings.py
DATA_DIR: Path = config("DATA_DIR")


def rename_ois_columns(df_ois: pd.DataFrame) -> pd.DataFrame:
    """Rename Bloomberg OIS tickers to compact labels expected downstream."""
    rename_map = {
        "USSO1Z CMPN Curncy": "OIS_1W",
        "USSOA CMPN Curncy": "OIS_1M",
        "USSOB CMPN Curncy": "OIS_2M",
        "USSOC CMPN Curncy": "OIS_3M",
        "USSOF CMPN Curncy": "OIS_6M",
        "USSO1 CMPN Curncy": "OIS_1Y",
    }
    df = df_ois.copy()
    df.columns = [c if c not in rename_map else rename_map[c] for c in df.columns]
    return df


def _quarter_contract_label(dt: pd.Timestamp, offset_quarters: int = 0) -> str:
    """Return a contract label like 'DEC 21' for the given date plus offset."""
    q_months = [3, 6, 9, 12]
    y, m = dt.year, dt.month
    next_month = next((qm for qm in q_months if qm > m), None)
    if next_month is None:
        next_month = 3
        y += 1
    total_quarters = q_months.index(next_month) + offset_quarters
    y += total_quarters // 4
    m_idx = total_quarters % 4
    month = q_months[m_idx]
    month_abbr = {3: "MAR", 6: "JUN", 9: "SEP", 12: "DEC"}[month]
    yy = y % 100
    return f"{month_abbr} {yy:02d}"


def build_last_day_mapping_from_dates(dates: pd.Series) -> pd.DataFrame:
    """Construct (Mat_Year, Mat_Month) -> Mat_Day mapping as last calendar day."""
    df_dates = pd.DataFrame({"Date": pd.to_datetime(dates)})
    df_dates["Mat_Month"] = df_dates["Date"].dt.month
    df_dates["Mat_Year"] = df_dates["Date"].dt.year
    df_dates = df_dates.sort_values("Date").drop_duplicates(
        ["Mat_Year", "Mat_Month"], keep="last"
    )
    df_dates["Mat_Day"] = df_dates["Date"].dt.day
    return df_dates[["Date", "Mat_Month", "Mat_Year", "Mat_Day"]].reset_index(drop=True)


def combine_treasury_futures_data(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Combine individual tenor files into a single consolidated DataFrame."""
    output_dir = Path(data_dir) / "basis_treas_sf"
    
    # Define tenors to combine
    tenors = [2, 5, 10, 20, 30]
    
    frames: List[pd.DataFrame] = []
    for tenor in tenors:
        filepath = output_dir / f"treasury_{tenor}y.parquet"
        if filepath.exists():
            try:
                df = pd.read_parquet(filepath)
                frames.append(df)
                print(f"Loaded {tenor}Y futures data: {len(df)} rows")
            except Exception as e:
                print(f"Error loading {tenor}Y futures data: {e}")
        else:
            print(f"Warning: {filepath} not found, skipping {tenor}Y tenor")
    
    if not frames:
        raise FileNotFoundError("No treasury futures files found to combine")
    
    print(f"Combining {len(frames)} tenor files...")
    
    # Combine all tenors on Date
    treasury_df = reduce(lambda a, b: a.merge(b, on="Date", how="outer"), frames)
    treasury_df.sort_values("Date", inplace=True)
    treasury_df.reset_index(drop=True, inplace=True)
    
    print(f"Combined data shape: {treasury_df.shape}")
    
    # Add Contract columns derived from Date (quarter cycle)
    for v, offset in [(1, 0), (2, 1)]:
        contracts = treasury_df["Date"].apply(
            lambda dt: _quarter_contract_label(
                pd.to_datetime(dt), offset_quarters=offset
            )
        )
        for tenor in tenors:
            treasury_df[f"Contract_{v}_{tenor}"] = contracts
    
    return treasury_df


def load_ois(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load OIS data from parquet file."""
    return pd.read_parquet(Path(data_dir) / "basis_treas_sf" / "ois.parquet")


def load_treasury_df(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load combined Treasury futures data from parquet file."""
    return pd.read_parquet(Path(data_dir) / "basis_treas_sf" / "treasury_df.parquet")


def load_last_day(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load last day mapping from parquet file."""
    return pd.read_parquet(Path(data_dir) / "basis_treas_sf" / "last_day.parquet")


if __name__ == "__main__":
    output_dir = DATA_DIR / "basis_treas_sf"
    print(f"Output directory: {output_dir}")
    
    print("Loading and formatting OIS data...")
    # Load and rename OIS data
    ois = load_ois()
    ois = rename_ois_columns(ois)
    ois.to_parquet(output_dir / "ois_formatted.parquet", index=False)
    print("Successfully saved formatted OIS data")
    
    print("Combining Treasury futures data...")
    # Combine Treasury futures data
    treasury_df = combine_treasury_futures_data()
    
    print("Saving combined data in multiple formats...")
    # Save combined data in multiple formats
    treasury_df.to_parquet(output_dir / "treasury_df.parquet", index=False)
    treasury_df.to_csv(output_dir / "treasury_df.csv", index=False)
    treasury_df.to_excel(output_dir / "treasury_df.xlsx", index=False)
    print("Successfully saved combined Treasury data")
    
    print("Building last day mapping...")
    # Build and save last day mapping
    last_day = build_last_day_mapping_from_dates(treasury_df["Date"])
    last_day.to_parquet(output_dir / "last_day.parquet", index=False)
    last_day.to_csv(output_dir / "last_day.csv", index=False)
    last_day.to_excel(output_dir / "last_day.xlsx", index=False)
    print("Successfully saved last day mapping")
    
    print("All formatting complete!")
