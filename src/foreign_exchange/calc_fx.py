"""
Calculate foreign exchange daily returns for USD invested in foreign currencies.

This module implements a strategy where USD is converted to a foreign currency at the
end of day t-1, invested in that currency's overnight repo market, and then converted
back to USD on day t.

The methodology calculates returns as:
    ret_{t,i} = (spot_{t-1,i} / spot_{t,i}) * fret_{t,i}

Where:
    - i is the foreign currency
    - t is the date of the implied foreign currency return
    - ret is the return of USD invested in the foreign currency
    - fret is the return of the foreign currency when invested in their overnight repo market
    - spot is the spot price of the currency (how much 1 USD is worth in the foreign currency)

Data Sources:
    - Bloomberg FX spot rates
    - Bloomberg interest rates (OIS)

Note: The implementation in implied_daily_fx_returns() appears to have the spot ratio
inverted compared to the documented formula. This should be verified and corrected if needed.

Code adapted with permission from https://github.com/Kunj121/CIP
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from settings import config
import pull_bbg_foreign_exchange

DATA_DIR = config("DATA_DIR")
OUTPUT_DIR = config("OUTPUT_DIR")

CURRENCIES = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "SEK", "USD"]


def prepare_fx_data(spot_rates, interest_rates):
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
    interest_rates : pd.DataFrame
        Interest rates (OIS) with Date column

    Returns
    -------
    pd.DataFrame
        Merged DataFrame with all prepared data
    """
    # NOTE: removed forward points from original function
    # Set Date as index

    spot_rates = (
        spot_rates.set_index("index") if "index" in spot_rates.columns else spot_rates
    )
    interest_rates = (
        interest_rates.set_index("index")
        if "index" in interest_rates.columns
        else interest_rates
    )

    # Standard column names for currencies
    cols = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "SEK", "USD"]
    int_cols = ["ADS", "CDS", "SFS", "EUS", "BPS", "JYS", "NDS", "SKS", "USS"]

    # Clean up column names - extract currency codes from Bloomberg tickers if needed
    def clean_columns(df, suffix="", interest_rate=False):
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
        # if interest_rate == True:
        #     available_cols = [c for c in int_cols if c in df.columns]
        #     df = df[available_cols]
        # else:
        #     available_cols = [c for c in cols if c in df.columns]
        #     df = df[available_cols]

        # # Add suffix if provided
        # if suffix:
        #     df.columns = [f"{c}{suffix}" for c in df.columns]

        ## I've commented this out because it was dropping the index of all
        ## three dataframes --- Alex
        return df

    # Clean and rename columns
    spot_rates = clean_columns(spot_rates)
    interest_rates = clean_columns(interest_rates, interest_rate=True)

    # Map interest rate columns from int_cols to cols
    ir_mapping = dict(zip(int_cols, cols))
    interest_rates = interest_rates.rename(columns=ir_mapping)

    # Convert forward points to forward rates

    # Rename columns to keep track
    spot_rates.columns = [f"{name}_spot" for name in spot_rates.columns]
    interest_rates.columns = [f"{name}_ir" for name in interest_rates.columns]

    # Merge all dataframes
    df_merged = spot_rates.merge(
        interest_rates, left_index=True, right_index=True, how="inner"
    )

    # Convert to reciprocal for these currencies (quoted as foreign/USD instead of USD/foreign)
    reciprocal_currencies = ["EUR", "GBP", "AUD", "NZD"]
    for ccy in reciprocal_currencies:
        if f"{ccy}_spot" in df_merged.columns:
            df_merged[f"{ccy}_spot"] = 1.0 / df_merged[f"{ccy}_spot"]

    return df_merged


def implied_daily_fx_returns(fx_data, currency_list):
    """
    Calculate implied daily return time series for USD invested in foreign currencies.

    This function implements the investment strategy where USD is converted to a foreign
    currency, invested in that currency's overnight market, then converted back to USD.

    WARNING: The current implementation appears to have issues:
    1. The spot ratio is inverted (using spot_t/spot_{t-1} instead of spot_{t-1}/spot_t)
    2. Interest rates are used directly without converting from annual percentage to daily returns

    Parameters
    ----------
    fx_data : pd.DataFrame
        Foreign currency data containing:
        - CUR_spot: Spot exchange rate (how much 1 USD is worth in currency CUR)
        - CUR_ir: Annualized interest rate of CUR in percent space (7.0 = 7%)
    currency_list : list
        List of currency codes to generate returns for

    Returns
    -------
    pd.DataFrame
        Daily return time series with columns:
        - CUR_return: Daily return of USD invested in currency CUR (not in % space)
    """
    fx_df = fx_data.copy()
    fx_df = fx_df.fillna(method="ffill")

    # tracking returns columns
    ret_cols = ["USD_return"]

    for curr_name in currency_list:
        int_col = f"{curr_name}_ir"

        if curr_name == "USD":
            fx_df["USD_return"] = fx_df[
                int_col
            ]  # change to daily annualized returns in % space

            continue

        spot_col = f"{curr_name}_spot"
        fx_df[f"{spot_col}_ratio"] = fx_df[spot_col] / fx_df[spot_col].shift(
            1
        )  # change in spot price ratio
        curr_ret_col = f"{curr_name}_return"

        # keep interest conversion consistent with US
        fx_df[curr_ret_col] = (
            fx_df[f"{spot_col}_ratio"] * fx_df[int_col]
        )  # combine spot change and interest
        ret_cols.append(curr_ret_col)

    # filter just for returns
    fx_df = fx_df[ret_cols]
    return fx_df


def graph_fx_returns(fx_df, currency_list, region_name):
    """
    Graphs the FX returns for a set of currencies in a given region.
    Legend is placed to the side for clarity.

    Parameters:
    fx_df: DataFrame containing foreign currency implied daily return time series.
           CUR_return is the daily return of CUR (not in %).
    currency_list: List of currency codes to graph.
    region_name: Name of the region or category.
    """
    ret_list = [f"{curr}_return" for curr in currency_list]

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    fx_df[ret_list].plot(ax=ax, title=f"Annualized Daily Returns of {region_name}")

    # Move legend to the right side
    ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))

    plt.tight_layout()
    plt.show()


def calculate_fx(end_date="2025-03-01", data_dir=DATA_DIR):
    """
    Calculate foreign exchange daily returns for USD invested in foreign currencies.

    Parameters
    ----------
    end_date : str
        End date for the data
    data_dir : Path, optional
        Directory containing the FX data files. If None, uses DATA_DIR from settings.

    Returns
    -------
    pd.DataFrame
        DataFrame with FX returns for each currency
    """
    data_dir = Path(data_dir)
    # Load data
    spot_rates = pull_bbg_foreign_exchange.load_fx_spot_rates(data_dir=data_dir)
    interest_rates = pull_bbg_foreign_exchange.load_fx_interest_rates(data_dir=data_dir)

    # Prepare data
    df_merged = prepare_fx_data(spot_rates, interest_rates)
    # Filter by end date
    if end_date:
        date = pd.Timestamp(end_date).date()
        df_merged = df_merged.loc[:date]

    # Compute CIP spreads
    df_merged = implied_daily_fx_returns(df_merged, CURRENCIES)

    # Shorten column names for display

    return df_merged


if __name__ == "__main__":
    # Calculate fx returns
    fx_returns = calculate_fx()

    # Save to parquet
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    fx_returns.to_parquet(DATA_DIR / "fx_returns.parquet")
