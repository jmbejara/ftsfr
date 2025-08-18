"""
format_bbg_basis_treas_sf.py

Format and combine individual Bloomberg data files into consolidated datasets.

This script takes the individual parquet files created by pull_bbg_basis_treas_sf.py
and combines them into a single consolidated dataset with proper column naming
and additional derived fields.

Inputs (from DATA_DIR/basis_treas_sf):
- ois.parquet: USD OIS rates
- treasury_2y_1.parquet, treasury_2y_2.parquet: 2Y Treasury futures data (near/deferred)
- treasury_5y_1.parquet, treasury_5y_2.parquet: 5Y Treasury futures data (near/deferred)
- treasury_10y_1.parquet, treasury_10y_2.parquet: 10Y Treasury futures data (near/deferred)
- treasury_20y_1.parquet, treasury_20y_2.parquet: 20Y Treasury futures data (near/deferred)
- treasury_30y_1.parquet, treasury_30y_2.parquet: 30Y Treasury futures data (near/deferred)

Outputs (saved under DATA_DIR/basis_treas_sf):
- treasury_df.parquet: Combined Treasury futures data with all tenors
- last_day.parquet: Mapping of (Mat_Year, Mat_Month) -> Mat_Day (last calendar day)
- treasury_df.csv: CSV version of combined data
- treasury_df.xlsx: Excel version of combined data

Process:
1. Load individual tenor files (both near and deferred contracts)
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
    
    # Start with an empty DataFrame
    treasury_df = None
    
    for tenor in tenors:
        # Load both near (1) and deferred (2) contracts for this tenor
        filepath_1 = output_dir / f"treasury_{tenor}y_1.parquet"
        filepath_2 = output_dir / f"treasury_{tenor}y_2.parquet"
        
        if filepath_1.exists() and filepath_2.exists():
            try:
                df1 = pd.read_parquet(filepath_1)
                df2 = pd.read_parquet(filepath_2)
                
                # Rename columns to match expected names in calc function
                # Key fields: FUT_IMPLIED_REPO_RT -> Implied_Repo, FUT_AGGTE_VOL -> Vol, PX_LAST -> Price
                df1_renamed = df1.rename(columns={
                    'FUT_IMPLIED_REPO_RT': 'Implied_Repo_1',
                    'FUT_AGGTE_VOL': 'Vol_1', 
                    'PX_LAST': 'Price_1',
                    'CURRENT_CONTRACT_MONTH_YR': 'Contract_1'
                })
                df2_renamed = df2.rename(columns={
                    'FUT_IMPLIED_REPO_RT': 'Implied_Repo_2',
                    'FUT_AGGTE_VOL': 'Vol_2',
                    'PX_LAST': 'Price_2', 
                    'CURRENT_CONTRACT_MONTH_YR': 'Contract_2'
                })
                
                # Select only the columns needed for the calc function
                df1_selected = df1_renamed[['Date', 'Implied_Repo_1', 'Vol_1', 'Price_1', 'Contract_1']]
                df2_selected = df2_renamed[['Date', 'Implied_Repo_2', 'Vol_2', 'Price_2', 'Contract_2']]
                
                # Merge near and deferred contracts for this tenor
                df_tenor = df1_selected.merge(df2_selected, on="Date", how="outer")
                
                # Add tenor information
                df_tenor['Tenor'] = tenor
                
                # Append to the main DataFrame
                if treasury_df is None:
                    treasury_df = df_tenor
                else:
                    treasury_df = pd.concat([treasury_df, df_tenor], ignore_index=True)
                    
            except Exception as e:
                raise RuntimeError(f"Error loading {tenor}Y futures data: {e}")
        else:
            raise FileNotFoundError(f"Missing files for {tenor}Y tenor: {filepath_1} or {filepath_2}")
    
    if treasury_df is None:
        raise FileNotFoundError("No treasury futures files found to combine")
    
    # Sort by Date and Tenor
    treasury_df.sort_values(["Date", "Tenor"], inplace=True)
    treasury_df.reset_index(drop=True, inplace=True)
    
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
    
    # Load and rename OIS data
    ois = load_ois()
    ois = rename_ois_columns(ois)
    ois.to_parquet(output_dir / "ois.parquet", index=False)
    
    # Combine Treasury futures data
    treasury_df = combine_treasury_futures_data()
    
    # Save combined data in multiple formats
    treasury_df.to_parquet(output_dir / "treasury_df.parquet", index=False)
    treasury_df.to_csv(output_dir / "treasury_df.csv", index=False)
    treasury_df.to_excel(output_dir / "treasury_df.xlsx", index=False)
    
    # Build and save last day mapping
    last_day = build_last_day_mapping_from_dates(treasury_df["Date"])
    last_day.to_parquet(output_dir / "last_day.parquet", index=False)
    last_day.to_csv(output_dir / "last_day.csv", index=False)
    last_day.to_excel(output_dir / "last_day.xlsx", index=False)
