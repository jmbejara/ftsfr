import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant
from decouple import config

DATA_DIR = config('DATA_DIR')
OUTPUT_DIR = config("OUTPUT_DIR")

def load_tips_treasury_data(file_path="/tips_treasury_implied_rf.parquet",
                           filter_columns=True
                            ):
    """
    Load TIPS-Treasury arbitrage data from parquet file.

    Parameters:
        file_path (str): Path to the parquet file
        filter_columns (bool): If True, return only arbitrage columns

    Returns:
        pd.DataFrame: DataFrame with the requested data
    """
    try:
        # Read the parquet file
        df = pd.read_parquet(file_path)

        # Set the date as index
        if 'date' in df.columns:
            df.index = df['date']

        # Extract only arbitrage columns if requested
        if filter_columns:
            arb_cols = [col for col in df.columns if col.startswith('arb_')]
            df = df[arb_cols]

        return df

    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Function to calculate AR(1) coefficient for an entire series
def ar1_coefficient(series):
    # Drop NaN values
    series = series.dropna()

    if len(series) <= 1:
        return np.nan

    y = series[1:].values
    X = add_constant(series[:-1].values)

    try:
        model = OLS(y, X).fit()
        return model.params[1]  # AR(1) coefficient
    except:
        return np.nan

def generate_summary_statistics(test_df, start_date=None, end_date=None, save_path=None):
    """
    Generate summary statistics for the TIPS-Treasury arbitrage data.

    Parameters:
        test_df (pd.DataFrame): DataFrame containing arbitrage data
        start_date (str): Start date in format 'YYYY-MM-DD' (optional)
        end_date (str): End date in format 'YYYY-MM-DD' (optional)
        save_path (str): Path to save the summary statistics as a CSV file

    Returns:
        pd.DataFrame: Summary statistics with renamed indices and formatted values
    """
    if start_date and end_date:
        df = test_df.loc[start_date:end_date].copy()
    elif start_date:
        df = test_df.loc[start_date:].copy()
    elif end_date:
        df = test_df.loc[:end_date].copy()
    else:
        df = test_df.copy()

    arb_cols = [col for col in df.columns if col.startswith('arb_') and not col.endswith('_AR1')]

    summary = pd.DataFrame()

    col_name_map = {
        'arb_2': 'TIPS-Treasury 2Y',
        'arb_5': 'TIPS-Treasury 5Y',
        'arb_10': 'TIPS-Treasury 10Y',
        'arb_20': 'TIPS-Treasury 20Y'
    }

    for col in arb_cols:
        series = df[col]

        ar1_val = ar1_coefficient(series)

        min_val = max(0, series.min())

        stats = {
            'Mean': round(series.mean()),
            'p50': round(series.median()),
            'Std. Dev': round(series.std()),
            'Min': round(min_val),
            'Max': round(series.max()),
            'AR1': round(ar1_val, 3),  # Keep AR1 to 2 decimal places
            'First': series.first_valid_index().strftime('%b-%Y') if not pd.isna(series.first_valid_index()) else 'N/A',
            'Last': series.last_valid_index().strftime('%b-%Y') if not pd.isna(series.last_valid_index()) else 'N/A',
            'N': int(series.count())
        }

        col_name = col_name_map.get(col, col)

        summary[col_name] = pd.Series(stats)

    if save_path:
        summary.to_csv(save_path)

    return summary.T


def plot_tips_treasury_spreads(data_df, start_date=None, end_date=None, figsize=(12, 6),
                              style="dark", save_path=None):
    """
    Plot TIPS-Treasury spreads over time.

    Parameters:
        data_df (pd.DataFrame): DataFrame containing arbitrage data
        start_date (str): Start date in format 'YYYY-MM-DD' (optional)
        end_date (str): End date in format 'YYYY-MM-DD' (optional)
        figsize (tuple): Figure size as (width, height)
        style (str): Seaborn style theme
        save_path (str): If provided, save figure to this path

    Returns:
        matplotlib.figure.Figure: The figure object
    """
    sns.set_theme(style=style)

    date_filter = slice(start_date, end_date)

    legend_name_map = {
        "arb_2": "2Y",
        "arb_5": "5Y",
        "arb_10": "10Y",
        "arb_20": "20Y"
    }

    fig, ax = plt.subplots(figsize=figsize)
    data_df.loc[date_filter].plot(ax=ax)

    title_dates = f"({start_date[:4] if start_date else ''}-{end_date[:4] if end_date else ''})"
    ax.set_title(f'TIPS Treasury Rates {title_dates}', fontsize=16)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Spread (bps)', fontsize=14)
    ax.grid(True, axis='y')

    ax.legend([legend_name_map.get(col, col) for col in data_df.columns],
              fontsize=12, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)

    plt.tight_layout()

    # Save if a path is provided
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)

    return fig

if __name__ == '__main__':
    data_path = f"{DATA_DIR}/tips_treasury_implied_rf.parquet"
    fig_path = f"{OUTPUT_DIR}/tips_treasury_spreads.png"
    summary_stats_path = f"{OUTPUT_DIR}/tips_treasury_summary.csv"

    arb_data = load_tips_treasury_data(file_path=data_path)
    summary_stats = generate_summary_statistics(arb_data, '2010-01-01', '2020-02-28', save_path=summary_stats_path)
    fig = plot_tips_treasury_spreads(arb_data, save_path=fig_path)

