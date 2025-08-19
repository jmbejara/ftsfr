"""
format_bbg_basis_treas_sf.py

Format and combine individual Bloomberg data files into consolidated datasets.

This script takes the individual parquet files created by pull_bbg_basis_treas_sf.py
and combines them into a single consolidated dataset with proper column naming
and additional derived fields.

Inputs (from DATA_DIR):
- ois.parquet: USD OIS rates
- treasury_2y_1.parquet, treasury_2y_2.parquet: 2Y Treasury futures data (near/deferred)
- treasury_5y_1.parquet, treasury_5y_2.parquet: 5Y Treasury futures data (near/deferred)
- treasury_10y_1.parquet, treasury_10y_2.parquet: 10Y Treasury futures data (near/deferred)
- treasury_20y_1.parquet, treasury_20y_2.parquet: 20Y Treasury futures data (near/deferred)
- treasury_30y_1.parquet, treasury_30y_2.parquet: 30Y Treasury futures data (near/deferred)

Outputs (saved under DATA_DIR):
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

from pathlib import Path

import pandas as pd

from settings import config

# Configuration via settings.py
DATA_DIR: Path = config("DATA_DIR")
# DATA_DIR = DATA_DIR / "basis_treas_sf"


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


def _prepare_tenor_dataframes(
    df1_renamed: pd.DataFrame, 
    df2_renamed: pd.DataFrame, 
    tenor: int
) -> tuple[pd.DataFrame, pd.DataFrame] | None:
    """
    Prepare and validate tenor DataFrames for processing.
    
    Returns:
        Tuple of (df1_selected, df2_selected) if successful, None if tenor should be skipped
    """
    required_columns_1 = ["Date", "Implied_Repo_1", "Vol_1", "Price_1", "Contract_1"]
    required_columns_2 = ["Date", "Implied_Repo_2", "Vol_2", "Price_2", "Contract_2"]
    
    # Check which columns exist and create missing ones with empty values
    missing_columns_1 = []
    missing_columns_2 = []
    
    for col in required_columns_1:
        if col not in df1_renamed.columns:
            if col == "Date":
                # Date column is essential, skip this tenor if missing
                print(f"Warning: Date column missing for {tenor}Y tenor, skipping")
                return None
            else:
                missing_columns_1.append(col)
    
    for col in required_columns_2:
        if col not in df2_renamed.columns:
            if col == "Date":
                # Date column is essential, skip this tenor if missing
                print(f"Warning: Date column missing for {tenor}Y tenor, skipping")
                return None
            else:
                missing_columns_2.append(col)
    
    # Only create empty columns if we have some actual data to work with
    if not df1_renamed.empty and missing_columns_1:
        for col in missing_columns_1:
            df1_renamed[col] = None
    
    if not df2_renamed.empty and missing_columns_2:
        for col in missing_columns_2:
            df2_renamed[col] = None
    
    # Select columns (now guaranteed to exist)
    df1_selected = df1_renamed[required_columns_1]
    df2_selected = df2_renamed[required_columns_2]

    # Check if we have any meaningful data to work with
    # Don't process if both DataFrames are empty or have no non-null data
    if df1_selected.empty and df2_selected.empty:
        print(f"Warning: No data available for {tenor}Y tenor, skipping")
        return None
    
    # Check if we have any non-null data in key columns (excluding Date)
    key_columns_1 = ["Implied_Repo_1", "Vol_1", "Price_1", "Contract_1"]
    key_columns_2 = ["Implied_Repo_2", "Vol_2", "Price_2", "Contract_2"]
    
    has_data_1 = any(df1_selected[col].notna().any() for col in key_columns_1)
    has_data_2 = any(df2_selected[col].notna().any() for col in key_columns_2)
    
    if not has_data_1 and not has_data_2:
        print(f"Warning: No meaningful data (all key columns are null) for {tenor}Y tenor, skipping")
        return None
    
    return df1_selected, df2_selected


def combine_treasury_futures_data(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Combine individual tenor files into a single consolidated DataFrame."""

    # Define tenors to combine
    tenors = [2, 5, 10, 20, 30]

    # Start with an empty DataFrame
    treasury_df = None

    for tenor in tenors:
        # Load both near (1) and deferred (2) contracts for this tenor
        filepath_1 = data_dir / f"treasury_{tenor}y_1.parquet"
        filepath_2 = data_dir / f"treasury_{tenor}y_2.parquet"

        df1 = pd.read_parquet(filepath_1)
        df2 = pd.read_parquet(filepath_2)

        # Rename columns to match expected names in calc function
        # Key fields: FUT_IMPLIED_REPO_RT -> Implied_Repo, FUT_AGGTE_VOL -> Vol, PX_LAST -> Price
        df1_renamed = df1.rename(
            columns={
                "FUT_IMPLIED_REPO_RT": "Implied_Repo_1",
                "FUT_AGGTE_VOL": "Vol_1",
                "PX_LAST": "Price_1",
                "CURRENT_CONTRACT_MONTH_YR": "Contract_1",
            }
        )
        df2_renamed = df2.rename(
            columns={
                "FUT_IMPLIED_REPO_RT": "Implied_Repo_2",
                "FUT_AGGTE_VOL": "Vol_2",
                "PX_LAST": "Price_2",
                "CURRENT_CONTRACT_MONTH_YR": "Contract_2",
            }
        )

        # Prepare and validate the tenor DataFrames
        result = _prepare_tenor_dataframes(df1_renamed, df2_renamed, tenor)
        if result is None:
            continue
            
        df1_selected, df2_selected = result

        # Merge near and deferred contracts for this tenor
        df_tenor = df1_selected.merge(df2_selected, on="Date", how="outer")

        # Add tenor information
        df_tenor["Tenor"] = tenor

        # Debug info
        non_null_counts = df_tenor.drop("Tenor", axis=1).notna().sum()
        print(f"{tenor}Y tenor: {len(df_tenor)} rows, non-null counts: {dict(non_null_counts)}")

        # Append to the main DataFrame
        if treasury_df is None:
            treasury_df = df_tenor
        else:
            # Only concatenate if we have meaningful data
            if not df_tenor.empty and df_tenor.drop("Tenor", axis=1).notna().any().any():
                treasury_df = pd.concat([treasury_df, df_tenor], ignore_index=True)
            else:
                print(f"Warning: {tenor}Y tenor has no meaningful data after merge, skipping concatenation")


    if treasury_df is None:
        raise FileNotFoundError("No treasury futures files found to combine")

    # Sort by Date and Tenor
    treasury_df.sort_values(["Date", "Tenor"], inplace=True)
    treasury_df.reset_index(drop=True, inplace=True)

    # Print summary of processed tenors and data quality
    processed_tenors = sorted(treasury_df["Tenor"].unique())
    print(f"Successfully processed tenors: {processed_tenors}")
    
    # Data quality summary
    total_rows = len(treasury_df)
    non_null_counts = treasury_df.notna().sum()
    print(f"Total rows: {total_rows}")
    print(f"Non-null counts per column: {dict(non_null_counts)}")
    
    # Check for excessive null data
    null_percentage = (treasury_df.isnull().sum() / len(treasury_df)) * 100
    high_null_cols = null_percentage[null_percentage > 80].index.tolist()
    if high_null_cols:
        print(f"Warning: Columns with >80% null values: {high_null_cols}")

    return treasury_df


def load_ois(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load OIS data from parquet file."""
    df = pd.read_parquet(Path(data_dir) / "ois.parquet")
    df_renamed = rename_ois_columns(df)
    return df_renamed


def load_treasury_df(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load combined Treasury futures data from parquet file."""
    return pd.read_parquet(Path(data_dir) / "treasury_df.parquet")


def load_last_day(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load last day mapping from parquet file."""
    return pd.read_parquet(Path(data_dir) / "last_day.parquet")


if __name__ == "__main__":

    # Load and rename OIS data
    ois = load_ois(data_dir=DATA_DIR)

    # Combine Treasury futures data
    treasury_df = combine_treasury_futures_data(data_dir=DATA_DIR)

    # Save combined data in multiple formats
    treasury_df.to_parquet(DATA_DIR / "treasury_df.parquet", index=False)
    treasury_df.to_csv(DATA_DIR / "treasury_df.csv", index=False)

    # Build and save last day mapping
    last_day = build_last_day_mapping_from_dates(treasury_df["Date"])
    last_day.to_parquet(DATA_DIR / "last_day.parquet", index=False)
    last_day.to_csv(DATA_DIR / "last_day.csv", index=False)
