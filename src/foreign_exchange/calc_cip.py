"""
Calculate Covered Interest Parity (CIP) spreads from foreign exchange data.

Code adapted with permission from https://github.com/Kunj121/CIP
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from settings import config
import pull_bbg_foreign_exchange

DATA_DIR = config("DATA_DIR")


def prepare_fx_data(spot_rates, forward_points, interest_rates):
    """
    Prepare foreign exchange data for CIP calculations.
    
    This function:
    1. Sets Date as index for all dataframes
    2. Standardizes column names
    3. Converts forward points to forward rates
    4. Converts certain currencies to reciprocals (EUR, GBP, AUD, NZD)
    5. Merges all data into a single DataFrame
    
    Parameters
    ----------
    spot_rates : pd.DataFrame
        Spot exchange rates with Date column
    forward_points : pd.DataFrame
        3M forward points with Date column
    interest_rates : pd.DataFrame
        Interest rates (OIS) with Date column
    
    Returns
    -------
    pd.DataFrame
        Merged DataFrame with all prepared data
    """
    # Set Date as index
    spot_rates = spot_rates.set_index("Date") if "Date" in spot_rates.columns else spot_rates
    forward_points = forward_points.set_index("Date") if "Date" in forward_points.columns else forward_points
    interest_rates = interest_rates.set_index("Date") if "Date" in interest_rates.columns else interest_rates
    
    # Standard column names for currencies
    cols = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "SEK"]
    
    # Clean up column names - extract currency codes from Bloomberg tickers if needed
    def clean_columns(df, suffix=""):
        new_cols = []
        for col in df.columns:
            # Extract currency code from Bloomberg ticker format
            if "_PX_LAST" in col:
                currency = col.split()[0][:3]
                new_cols.append(currency)
            else:
                new_cols.append(col)
        df.columns = new_cols
        
        # Keep only our standard currencies
        available_cols = [c for c in cols if c in df.columns]
        df = df[available_cols]
        
        # Add suffix if provided
        if suffix:
            df.columns = [f"{c}{suffix}" for c in df.columns]
        
        return df
    
    # Clean and rename columns
    spot_rates = clean_columns(spot_rates)
    forward_points = clean_columns(forward_points)
    interest_rates = clean_columns(interest_rates)
    
    # Also include USD in interest rates if available
    if "USD" in interest_rates.columns:
        cols_ir = cols + ["USD"]
    else:
        cols_ir = cols
    
    # Convert forward points to forward rates
    # Non-JPY: forward points are per 10,000; JPY: per 100
    forward_rates = forward_points.copy()
    non_jpy_cols = [c for c in forward_rates.columns if c != "JPY"]
    if non_jpy_cols:
        forward_rates[non_jpy_cols] = forward_rates[non_jpy_cols] / 10000
    if "JPY" in forward_rates.columns:
        forward_rates["JPY"] = forward_rates["JPY"] / 100
    
    # Add forward points to spot rates to get forward rates
    forward_rates = spot_rates + forward_rates
    
    # Rename columns to keep track
    spot_rates.columns = [f"{name}_CURNCY" for name in spot_rates.columns]
    forward_rates.columns = [f"{name}_CURNCY3M" for name in forward_rates.columns]
    interest_rates.columns = [f"{name}_IR" for name in interest_rates.columns]
    
    # Merge all dataframes
    df_merged = spot_rates.merge(
        forward_rates, left_index=True, right_index=True, how="inner"
    ).merge(interest_rates, left_index=True, right_index=True, how="inner")
    
    # Convert to reciprocal for these currencies (quoted as foreign/USD instead of USD/foreign)
    reciprocal_currencies = ["EUR", "GBP", "AUD", "NZD"]
    for ccy in reciprocal_currencies:
        if f"{ccy}_CURNCY" in df_merged.columns:
            df_merged[f"{ccy}_CURNCY"] = 1.0 / df_merged[f"{ccy}_CURNCY"]
        if f"{ccy}_CURNCY3M" in df_merged.columns:
            df_merged[f"{ccy}_CURNCY3M"] = 1.0 / df_merged[f"{ccy}_CURNCY3M"]
    
    return df_merged


def compute_cip_spreads(df_merged):
    """
    Compute CIP spreads in basis points for all currencies.
    
    CIP in log terms (bps) = 10000 × [domestic_i - (logF - logS)×(360/90) - foreign_i]
    
    Parameters
    ----------
    df_merged : pd.DataFrame
        DataFrame with spot rates, forward rates, and interest rates
    
    Returns
    -------
    pd.DataFrame
        DataFrame with CIP spreads for each currency
    """
    currencies = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "SEK"]
    
    # Compute the log CIP basis in basis points
    for ccy in currencies:
        fwd_col = f"{ccy}_CURNCY3M"
        spot_col = f"{ccy}_CURNCY"
        ir_col = f"{ccy}_IR"
        usd_ir_col = "USD_IR"
        
        if all(col in df_merged.columns for col in [fwd_col, spot_col, ir_col, usd_ir_col]):
            # CIP in log terms (bps) = 10000 × [domestic_i - (logF - logS)×(360/90) - foreign_i]
            cip_col = f"CIP_{ccy}_ln"
            df_merged[cip_col] = 10000 * (
                (df_merged[ir_col] / 100.0)  # domestic interest rate
                - (360.0 / 90.0) * (
                    np.log(df_merged[fwd_col]) - np.log(df_merged[spot_col])
                )
                - (df_merged[usd_ir_col] / 100.0)  # foreign interest rate (USD)
            )
    
    return df_merged


def clean_outliers(df_merged, window_size=45, threshold=10):
    """
    Clean outliers using rolling median absolute deviation.
    
    Parameters
    ----------
    df_merged : pd.DataFrame
        DataFrame with CIP spreads
    window_size : int
        Window size for rolling calculations
    threshold : float
        Threshold for outlier detection (number of MADs)
    
    Returns
    -------
    pd.DataFrame
        DataFrame with outliers replaced by NaN
    """
    currencies = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "SEK"]
    
    for ccy in currencies:
        cip_col = f"CIP_{ccy}_ln"
        if cip_col not in df_merged.columns:
            continue
        
        # Rolling median over window
        rolling_median = df_merged[cip_col].rolling(window_size).median()
        
        # Absolute deviation from median
        abs_dev = (df_merged[cip_col] - rolling_median).abs()
        
        # Rolling mean of abs_dev (proxy for MAD)
        rolling_mad = abs_dev.rolling(window_size).mean()
        
        # Mark outliers and replace with NaN
        outlier_mask = (abs_dev / rolling_mad) >= threshold
        df_merged.loc[outlier_mask, cip_col] = np.nan
    
    return df_merged


def plot_cip_spreads(spreads, output_filename="cip_spreads"):
    """
    Plot CIP spreads in basis points.
    
    Parameters
    ----------
    spreads : pd.DataFrame
        DataFrame with CIP spreads (columns should be currency codes)
    output_filename : str
        Base filename for output (without extension)
    """
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    
    # Plot each column
    for column in spreads.columns:
        ax.plot(spreads.index, spreads[column], label=column, linewidth=1, antialiased=True)
    
    ax.set_xlabel("Dates", fontsize=14)
    ax.set_ylabel("Arbitrage Spread (bps)", fontsize=14)
    
    # Format the x-axis for years
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_minor_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=0)
    
    # Horizontal grid lines only
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.xaxis.grid(False)
    
    # Hard limit the y-axis
    ax.set_ylim([-50, 210])
    
    # Legend below the plot
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=4, fontsize=12, frameon=True)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout(rect=[0, 0.15, 1, 1])  # ensure legend fits
    
    plt.savefig(f"{output_filename}.pdf", format="pdf", bbox_inches='tight')
    plt.savefig(f"{output_filename}.png", dpi=300, bbox_inches='tight')
    plt.close()


def calculate_cip(end_date='2025-03-01', plot=False):
    """
    Calculate CIP spreads from foreign exchange data.
    
    Parameters
    ----------
    end_date : str
        End date for the data
    plot : bool
        Whether to generate plots
    
    Returns
    -------
    pd.DataFrame
        DataFrame with CIP spreads
    """
    # Load data
    spot_rates = pull_bbg_foreign_exchange.load_fx_spot_rates(data_dir=DATA_DIR)
    forward_points = pull_bbg_foreign_exchange.load_fx_forward_points(data_dir=DATA_DIR)
    interest_rates = pull_bbg_foreign_exchange.load_fx_interest_rates(data_dir=DATA_DIR)
    
    # Prepare data
    df_merged = prepare_fx_data(spot_rates, forward_points, interest_rates)
    
    # Filter by end date
    if end_date:
        df_merged = df_merged.loc[:end_date]
    
    # Compute CIP spreads
    df_merged = compute_cip_spreads(df_merged)
    
    # Clean outliers
    df_merged = clean_outliers(df_merged)
    
    # Extract just the CIP columns
    currencies = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "SEK"]
    cip_cols = [f"CIP_{c}_ln" for c in currencies if f"CIP_{c}_ln" in df_merged.columns]
    spreads = df_merged[cip_cols].copy()
    
    # Shorten column names for display
    spreads.columns = [c[4:7] for c in spreads.columns]  # e.g., CIP_AUD_ln -> AUD
    
    if plot:
        plot_cip_spreads(spreads)
    
    return spreads


def load_cip_spreads(data_dir=DATA_DIR):
    """Load calculated CIP spreads from parquet file."""
    path = data_dir / "cip_spreads.parquet"
    return pd.read_parquet(path)


if __name__ == "__main__":
    # DATA_DIR = DATA_DIR / "foreign_exchange"
    df = pull_bbg_foreign_exchange.load_fx_spot_rates(data_dir=DATA_DIR)
    # Calculate CIP spreads
    cip_spreads = calculate_cip(end_date='2025-03-01', plot=True)
    
    # Save to parquet
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cip_spreads.to_parquet(DATA_DIR / "cip_spreads.parquet")
