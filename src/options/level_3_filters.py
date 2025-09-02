"""
This file contains a collection of functions for filtering and processing option data according to the Level 3 Filters described in originalpaper.

Functions:
- functimer: A decorator function that measures the execution time of a given function.
- fit_and_store_curve: Fit a quadratic curve to a group of data points and store the fitted values.
- apply_quadratic_iv_fit: Apply quadratic curve fitting to the input data.
- calc_relative_distance: Calculate the relative distance between two series of data.
- mark_outliers: Determine if a data point is an outlier based on its moneyness_bin and relative distance from the fitted curve.
- build_put_call_pairs: Build pairs of call and put options based on the same date, expiration date, and moneyness.
- test_price_strike_match: Check if the strike prices and security prices of matching calls and puts are equal.
- calc_implied_interest_rate: Calculate the implied interest rate based on the given matched options data.
- pcp_filter_outliers: Filter out outliers based on the relative distance of interest rates and the outlier threshold.
- iv_filter_outliers: Filter out outliers based on the relative distance of implied volatility and the outlier threshold.
"""

# standard libraries
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
pd.set_option('display.max_columns', None)

import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

# system libraries
import os
import sys
from pathlib import Path
# Add the src directory to the path in order to import config
current_directory = Path.cwd()
src_path = current_directory.parent / "src"
sys.path.insert(0, str(src_path))

# project files
import config
import load_option_data_01 as l1
import level_1_filters as f1
import wrds
import bsm_pricer as bsm

from functools import partial
import time

# environment variables
WRDS_USERNAME = Path(config.WRDS_USERNAME)
DATA_DIR = Path(config.DATA_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)
START_DATE_01 =config.START_DATE_01
END_DATE_01 = config.END_DATE_01
START_DATE_02 =config.START_DATE_02
END_DATE_02 = config.END_DATE_02


# Helper functions
def functimer(func):
    """
    A decorator function that measures the execution time of a given function.

    Parameters:
    func (function): The function to be timed.

    Returns:
    function: The wrapped function.

    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f" |-- !! Execution time: {func.__name__} --> {execution_time:,.5f} seconds")
        return result
    return wrapper


def fit_and_store_curve(group):
    """
    Fit a quadratic curve to the given group of data points and store the fitted values.

    Args:
        group (pandas.DataFrame): The group of data points to fit the curve to.

    Returns:
        pandas.DataFrame: The group of data points with the fitted values stored in the 'fitted_iv' column.
    """
    try:
        # Fit the quadratic curve
        coefficients = np.polyfit(group['moneyness'], group['log_iv'], 2)
        # Calculate fitted values
        group['fitted_iv'] = np.polyval(coefficients, group['moneyness'])
    except np.RankWarning:
        print("Polyfit may be poorly conditioned")
    return group



@functimer
def apply_quadratic_iv_fit(l2_data):
    """
    Apply quadratic curve fitting to the input data.

    Parameters:
    l2_data (DataFrame): The input data to which the quadratic curve fitting function will be applied.

    Returns:
    DataFrame: The input data with the quadratic curve fitting applied.
    """
    # Apply the quadratic curve fitting function to the data
    l2_data = l2_data.dropna(subset=['moneyness', 'log_iv']).groupby(['date', 'exdate', 'cp_flag']).filter(lambda group: len(group) >= 3)
    
    l2_data = l2_data.groupby(['date', 'exdate', 'cp_flag']).apply(fit_and_store_curve)
    
    return l2_data



def calc_relative_distance(series1, series2, method='percent'):
    """
    Calculate the relative distance between the implied volatility and the fitted implied volatility.
    
    Parameters:
        method (str): The method to calculate the relative distance. Options are 'percent', 'manhattan', or 'euclidean'.
        
    Returns:
        numpy.ndarray: The relative distance calculated based on the specified method.
        
    Raises:
        ValueError: If the method is not one of 'percent', 'manhattan', or 'euclidean'.
    """
    
    if method == 'percent':
        result = (series1 - series2) / series2 * 100
    elif method == 'manhattan':
        result = abs(series1 - series2)
    elif method == 'euclidean':
        result = np.sqrt((series1 - series2)**2)
    else:
        raise ValueError("Method must be 'percent', 'manhattan', or 'euclidean'")
    
    result = np.where(np.isinf(result), np.nan, result)
    
    return result


@functimer  
def mark_outliers(row, std_devs, outlier_threshold):
    """
    Determines if a data point is an outlier based on its moneyness_bin and relative distance from the fitted curve.
    
    Args:
        row (pandas.Series): A row of data containing the moneyness_bin and rel_distance columns.
        std_devs (pandas.DataFrame): A DataFrame containing the standard deviations for each moneyness_bin.
    
    Returns:
        bool: True if the data point is an outlier, False otherwise.
    """
    
    # Attempt to retrieve the standard deviation for the row's moneyness_bin
    std_dev_row = std_devs.loc[std_devs['moneyness_bin'] == row['moneyness_bin'], 'std_dev']
    
    # Check if std_dev_row is empty (i.e., no matching moneyness_bin was found)
    if not std_dev_row.empty:
        std_dev = std_dev_row.values[0]
        # Calculate how many std_devs away from the fitted curve the IV is
        if abs(row['rel_distance']) > outlier_threshold * std_dev:  # Adjust this threshold as needed
            return True
    else:
        # Handle the case where no matching moneyness_bin was found
        return False
    return False


def build_put_call_pairs(call_options, put_options):
    """
    Builds pairs of call and put options based on the same date, expiration date, and moneyness.

    Args:
        call_options (DataFrame): DataFrame containing call options data.
        put_options (DataFrame): DataFrame containing put options data.

    Returns:
        tuple of (matching_calls: pd.DataFrame, matching_puts: pd.DataFrame)
    """
    call_options.set_index(['date', 'exdate', 'moneyness'], inplace=True)
    put_options.set_index(['date', 'exdate', 'moneyness'], inplace=True)
    
    # get common indices
    common_index = call_options.index.intersection(put_options.index)

    # Extract the matching entries
    matching_calls = call_options.loc[common_index]
    matching_puts = put_options.loc[common_index]
    
    result = (matching_calls, matching_puts)

    return result


def test_price_strike_match(matching_calls_puts):
    """
    Check if the strike prices and security prices of matching calls and puts are equal.

    Parameters:
    matching_calls_puts (DataFrame): DataFrame containing matching calls and puts data.

    Returns:
    bool: True if the strike prices and security prices of matching calls and puts are equal, False otherwise.
    """
    #print(matching_calls_puts)
    try:
        return (np.allclose(matching_calls_puts['strike_price_C'], matching_calls_puts['strike_price_P'])) and (np.allclose(matching_calls_puts['close_C'], matching_calls_puts['close_P']))# and (np.allclose(matching_calls_puts['tb_m3_C'], matching_calls_puts['tb_m3_P']))
    except KeyError:
        if 'strike_price' in matching_calls_puts.columns and 'close' in matching_calls_puts.columns:
            return True
        else:
            return False


def calc_implied_interest_rate(matched_options):
    """
    Calculates the implied interest rate assuming put-call parity, based on the given put/call matched option pairs.

    Parameters:
    matched_options (DataFrame): DataFrame containing the matched options data.

    Returns:
    DataFrame: DataFrame with an additional column 'pc_parity_int_rate' representing the implied interest rate.
    
    Raises:
    ValueError: If there is a mismatch between the price and strike price of the options.
    """
    
    # underlying price
    if test_price_strike_match(matched_options):
        print(" |-- PCP filter: Check ok --> Underlying prices, strike prices of put and call options match exactly.")
        try:
            S = matched_options['close_C']
        except KeyError:
            S = matched_options['close']
        
        try:
            K = matched_options['strike_price_C']  
        except KeyError:
            K = matched_options['strike_price']
        
        # 1/T = 1/time to expiration in years
        T_inv = np.power((matched_options.reset_index()['exdate']-matched_options.reset_index()['date'])/datetime.timedelta(days=365), -1)
        T_inv.index=matched_options.index
        
        C_mid = matched_options['mid_price_C']
        P_mid = matched_options['mid_price_P']
        # implied interest rate
        matched_options['pc_parity_int_rate'] = np.log((S-C_mid+P_mid)/K) * T_inv
        return matched_options
    else:
        raise ValueError("!! Price and strike price mismatch")


def pcp_filter_outliers(matched_options, int_rate_rel_distance_func, outlier_threshold):
    """
    Filters out outliers based on the relative distance of interest rates and the outlier threshold.

    Parameters:
    - matched_options (DataFrame): DataFrame containing the matched options data.
    - int_rate_rel_distance_func (str): Method to calculate the relative distance of interest rates.
    - outlier_threshold (float): Threshold for flagging outliers.

    Returns:
    - l3_filtered_options (DataFrame): DataFrame with outliers filtered out, structured in long-form (like the original L2 data).
    """
    matched_options['rel_distance_int_rate'] = calc_relative_distance(matched_options['pc_parity_int_rate'], matched_options['daily_median_rate'], method=int_rate_rel_distance_func)
    # fill 3905 nans...
    matched_options['rel_distance_int_rate'] = matched_options['rel_distance_int_rate'].fillna(0.0)

    # calculate the standard deviation of the relative distances
    stdev_int_rate_rel_distance = matched_options['rel_distance_int_rate'].std()

    # flag outliers based on the threshold
    matched_options['is_outlier_int_rate'] = matched_options['rel_distance_int_rate'].abs() > outlier_threshold * stdev_int_rate_rel_distance

    # filter out the outliers
    l3_filtered_options = matched_options[~matched_options['is_outlier_int_rate']]

    # make the dataframe long-form to compare to the level 2 data
    _calls = l3_filtered_options.filter(like='_C').rename(columns=lambda x: x.replace('_C', ''))
    _puts = l3_filtered_options.filter(like='_P').rename(columns=lambda x: x.replace('_P', ''))
    l3_filtered_options = pd.concat((_calls, _puts), axis=0)

    return l3_filtered_options


def iv_filter_outliers(l2_data, iv_distance_method, iv_outlier_threshold):
    """
    Filter out outliers based on the relative distance of log_iv and fitted_iv.

    Parameters:
    l2_data (DataFrame): Input data containing log_iv, fitted_iv, moneyness columns.
    iv_distance_method (str): Method to calculate relative distance of log_iv and fitted_iv.
    iv_outlier_threshold (float): Threshold value to flag outliers.

    Returns:
    DataFrame: Filtered data without outliers.

    """
    l2_data['rel_distance_iv'] = calc_relative_distance(l2_data['log_iv'], l2_data['fitted_iv'], method=iv_distance_method)

    # Define moneyness bins
    bins = np.arange(0.875, 1.125, 0.025)
    l2_data['moneyness_bin'] = pd.cut(l2_data['moneyness'], bins=bins)

    # Compute standard deviation of relative distances within each moneyness bin
    std_devs = l2_data.groupby('moneyness_bin')['rel_distance_iv'].std().reset_index(name='std_dev')
    
    l2_data['stdev_iv_moneyness_bin'] = l2_data['moneyness_bin'].map(std_devs.set_index('moneyness_bin')['std_dev'])
    l2_data['stdev_iv_moneyness_bin'].apply(lambda x: x*iv_outlier_threshold).astype(float)
    # flag outliers based on the threshold
    l2_data['is_outlier_iv'] = l2_data['rel_distance_iv'].abs() > l2_data['stdev_iv_moneyness_bin'].apply(lambda x: x*iv_outlier_threshold).astype(float)

    # filter out the outliers
    l3_data_iv_only = l2_data[~l2_data['is_outlier_iv']]
    
    return l3_data_iv_only



def build_check_results():
    """
    Builds and returns a DataFrame containing check results for level 3 filters.

    Returns:
        pandas.DataFrame: DataFrame with check results for level 3 filters.
    """
    check_results = pd.DataFrame(index=pd.MultiIndex.from_product([['Level 3 filters'], ['IV filter', 'Put-call parity filter', 'All']]),
                             columns=pd.MultiIndex.from_product([['Berkeley', 'OptionMetrics'], ['Deleted', 'Remaining']]))
    check_results.loc[['Level 3 filters'], ['Berkeley', 'OptionMetrics']] = [[10865, np.nan, 67850, np.nan], [10298, np.nan,46138, np.nan], [np.nan, 173500,np.nan, 962784]]

    return check_results.loc[:, 'OptionMetrics']



def nan_iv_in_l2_data(l2_data, date_range):
    """
    Calculate the summary of NaN IV (Implied Volatility) records in Level 2 filtered data.

    Parameters:
    l2_data (DataFrame): The Level 2 data containing option information.
    date_range (str): The date range for which the summary is calculated.

    Returns:
    DataFrame: The summary of NaN IV records, including the number of NaN IV records, total records, and percentage of NaN IV records for calls and puts.

    Example:
    nan_iv_in_l2_data(l2_data, '2021-01-01_2021-01-31')
    """
    nan_iv_calls = l2_data[(l2_data['cp_flag'] == 'C') & (l2_data['IV'].isna())]
    nan_iv_puts = l2_data[(l2_data['cp_flag'] == 'P') & (l2_data['IV'].isna())]
    nan_iv_summary = pd.DataFrame(index=['Calls', 'Puts'], columns = ['NaN IV Records', 'Total Records', '% NaN IV'])
    nan_iv_summary.loc['Calls'] = [len(nan_iv_calls), len(l2_data[l2_data['cp_flag'] == 'C']), len(nan_iv_calls)/len(l2_data[l2_data['cp_flag'] == 'C'])*100]
    nan_iv_summary.loc['Puts'] = [len(nan_iv_puts), len(l2_data[l2_data['cp_flag'] == 'P']), len(nan_iv_puts)/len(l2_data[l2_data['cp_flag'] == 'P'])*100]
    # nan_iv_summary.style.format({'NaN IV Records': '{:,.0f}', 'Total Records': '{:,.0f}', '% NaN IV': '{:.2f}%'}).set_caption(f'Summary of NaN IV Records in Level 2 Filtered Data: {date_range.replace("_", " to ")}')
    
    return nan_iv_summary



def calc_relative_distance_stats(l3_data_iv_only, date_range):
    """
    Calculate the statistics of the relative distance of options based on the given data and date range.

    Parameters:
    l3_data_iv_only (DataFrame): DataFrame containing the option data with 'rel_distance_iv', 'moneyness' columns.
    date_range (str): Date range for which the statistics are calculated.

    Returns:
    DataFrame: DataFrame containing the statistics of the relative distance of options.

    """
    ntm_rel_dist = l3_data_iv_only[(l3_data_iv_only['moneyness'] < 1.1) & (l3_data_iv_only['moneyness'] > 0.9)].describe()['rel_distance_iv'].to_frame().rename(columns={'rel_distance_iv': 'Near-The-Money'})
    fftm_rel_dist = l3_data_iv_only[(l3_data_iv_only['moneyness'] > 1.1) | (l3_data_iv_only['moneyness'] < 0.9)].describe()['rel_distance_iv'].to_frame().rename(columns={'rel_distance_iv': 'Far-From-The-Money Options'})
    rel_dist_stats = pd.concat([ntm_rel_dist, fftm_rel_dist], axis=1)
    
    rel_dist_stats.style.format('{:,.2f}').set_caption('Relative Distance Stats')
    rel_dist_stats.to_latex(OUTPUT_DIR / f'L3_rel_dist_stats_{date_range}.tex')
    
    return rel_dist_stats


###### CHARTS ######

def _get_col(df, col):
    if col in df.columns:
        return df[col]
    if isinstance(df.columns, pd.MultiIndex):
        if col in df.columns.get_level_values(-1):
            return df.xs(col, axis=1, level=-1)
    if col in df.index.names:
        return df.index.get_level_values(col)
    raise KeyError(f"{col} not found in DataFrame or index levels")

def _plot_distribution(ax, df, col, color, title):
    series = _get_col(df, col).dropna()
    ax.hist(series.values, bins=250, color=color)
    ax.set_title(title)
    ax.set_xlabel(col)
    ax.set_ylabel('Frequency')
    ax.grid()

def _plot_logiv_vs_moneyness(ax, df, sample_size):
    moneyness = _get_col(df, 'moneyness')
    log_iv = _get_col(df, 'log_iv')
    xy = pd.DataFrame({'moneyness': moneyness, 'log_iv': log_iv}).dropna()
    if len(xy) > sample_size:
        xy = xy.sample(sample_size, random_state=0)
    ax.scatter(xy['moneyness'], xy['log_iv'], alpha=0.1, color='purple')
    ax.set_title('log(IV) vs Moneyness')
    ax.set_xlabel('Moneyness')
    ax.set_ylabel('log(IV)')
    ax.grid()

def _plot_iv_vs_moneyness(ax, df, cp_flag, sample_size):
    moneyness = _get_col(df, 'moneyness')
    iv = _get_col(df, 'IV')
    cp = _get_col(df, 'cp_flag')
    mask = (cp == cp_flag) & iv.notna() & moneyness.notna()
    data = pd.DataFrame({'moneyness': moneyness[mask], 'IV': iv[mask]})
    if len(data) > sample_size:
        seed = 1 if cp_flag == 'C' else 2
        data = data.sample(sample_size, random_state=seed)
    color = 'blue' if cp_flag == 'C' else 'red'
    ax.scatter(data['moneyness'], data['IV'], alpha=0.1, color=color)
    ax.set_title(f"IV vs Moneyness ({'Calls' if cp_flag == 'C' else 'Puts'})")
    ax.set_xlabel('Moneyness')
    ax.set_ylabel('IV')
    ax.grid()

def _plot_fitted_vs_logiv(ax, df, sample_size):
    if 'fitted_iv' not in df.columns:
        ax.axis('off')
        return
    log_iv = _get_col(df, 'log_iv')
    fitted = _get_col(df, 'fitted_iv')
    xy = pd.DataFrame({'log_iv': log_iv, 'fitted_iv': fitted}).dropna()
    if len(xy) > sample_size:
        xy = xy.sample(sample_size, random_state=3)
    ax.scatter(xy['log_iv'], xy['fitted_iv'], alpha=0.1, color='darkgreen')
    min_val, max_val = xy['log_iv'].min(), xy['log_iv'].max()
    ax.plot([min_val, max_val], [min_val, max_val], linestyle='--', color='red')
    ax.set_title('Fitted log(IV) vs Observed log(IV)')
    ax.set_xlabel('log(IV)')
    ax.set_ylabel('Fitted log(IV)')
    ax.grid()

def _build_iv_chart(df, date_range, level_tag, title_prefix, sample_size=50000):
    df = df.copy()
    if 'log_iv' not in df.columns:
        iv = _get_col(df, 'IV')
        df['log_iv'] = np.log(iv.where(iv > 0))

    fig, ax = plt.subplots(2, 3, figsize=(12, 8))
    _plot_distribution(ax[0, 0], df, 'IV', 'darkblue', 'Distribution of IV')
    _plot_distribution(ax[0, 1], df, 'log_iv', 'grey', 'Distribution of log(IV)')
    _plot_logiv_vs_moneyness(ax[0, 2], df, sample_size)
    _plot_iv_vs_moneyness(ax[1, 0], df, 'C', sample_size)
    _plot_iv_vs_moneyness(ax[1, 1], df, 'P', sample_size)
    _plot_fitted_vs_logiv(ax[1, 2], df, sample_size)

    fig.suptitle(f'{title_prefix}: {date_range.replace("_", " to ")}')
    plt.tight_layout()
    filename = f'{level_tag}_{date_range}_iv_summary.png'
    try:
        fig.savefig(OUTPUT_DIR / filename)
    except FileNotFoundError:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        fig.savefig(OUTPUT_DIR / filename)

    plt.show()
    

# === Public Functions ===
def build_raw_iv_chart(df, date_range, sample_size=50000):
    _build_iv_chart(df, date_range, level_tag='RAW', title_prefix='Raw Options Data', sample_size=sample_size)

def build_l1_iv_chart(df, date_range, sample_size=50000):
    _build_iv_chart(df, date_range, level_tag='L1', title_prefix='Level 1 Filtered Data', sample_size=sample_size)

def build_l2_iv_chart(df, date_range, sample_size=50000):
    _build_iv_chart(df, date_range, level_tag='L2', title_prefix='Level 2 IV-Filtered Data', sample_size=sample_size)

def build_l3_iv_chart(df, date_range, sample_size=50000):
    _build_iv_chart(df, date_range, level_tag='L3_IV', title_prefix='Level 3 IV-Filtered Data', sample_size=sample_size)

def build_l3_iv_pcp_chart(df, date_range, sample_size=50000):
    _build_iv_chart(df, date_range, level_tag='L3_IV_PCP', title_prefix='Level 3 IV + PCP Filtered Data', sample_size=sample_size)





def get_filepaths(date_range):
    """
    Returns the filepaths for the input and output files based on the given date range.
    
    Parameters:
        date_range (str): The date range for which the filepaths are generated.
        
    Returns:
        tuple: A tuple containing the filepaths for the input and output files.
            - l2_input_file (str): The filepath for the L2 input file.
            - l3_iv_only_output_file (str): The filepath for the L3 IV-only output file.
            - l3_output_file (str): The filepath for the L3 output file.
    """
    
    l2_input_file = f"intermediate/data_{date_range}_L2filter.parquet"
    l3_iv_only_output_file = f"intermediate/data_{date_range}_L3filterIVonly.parquet"
    l3_output_file = f"intermediate/data_{date_range}_L3filter.parquet"
    
    return l2_input_file, l3_iv_only_output_file, l3_output_file


def run_filter(_df, date_range, iv_only=False):
    """
    Run the L3 filter on option data.

    Parameters:
    - _df: Dummy argument (not used) - included to make this module work with Table B doit.
    - date_range (tuple): A tuple containing the start and end dates of the date range.
    - iv_only (bool, optional): If True, only run the IV filter. If False, run both the IV filter and the put-call filter. Default is False.

    Returns:
    - l3_filtered_options (list): A list of filtered option data.

    """
    print('>> L3 filter running...')
    
    if iv_only:
        print(' >> Running IV filter only...')
        l3_data_iv_only = IV_filter(_df, date_range=date_range)
        l3_filtered_options = None
    else:
        l3_data_iv_only = IV_filter(_df, date_range=date_range)
        l3_filtered_options = put_call_filter(_df, date_range=date_range)
    
    return l3_data_iv_only, l3_filtered_options



def compare_to_optionmetrics(l2_data, l3_data_iv_only, l3_filtered_options, date_range):
    """
    Compare the data from different levels of filtering to OptionMetrics data (1996 - 2012 only).

    Parameters:
    - l2_data (DataFrame): Level 2 data.
    - l3_data_iv_only (DataFrame): Level 3 data after applying IV filter.
    - l3_filtered_options (DataFrame): Level 3 data after applying Put-call parity filter.
    - date_range (str): Date range for the comparison.

    Returns:
    - final_result_compare (DataFrame): Comparison results.

    """
    final_result_compare = build_check_results()
    final_result_compare.loc[('Level 3 filters', 'IV filter'), 'Deleted'] = len(l2_data)-len(l3_data_iv_only)  
    # final result
    final_result_compare.loc[('Level 3 filters', 'Put-call parity filter'), 'Deleted'] = len(l3_data_iv_only)-len(l3_filtered_options)
    final_result_compare.loc[('Level 3 filters', 'All'), 'Remaining'] = len(l3_filtered_options)    
    final_result_compare = pd.merge(final_result_compare, build_check_results(), left_index=True, right_index=True, suffixes=(f' - Implemented_{date_range.replace("-01", "").replace("-02", "").replace("-12","")}', ' - OptionMetrics_1996-2012'))
    final_result_compare.to_parquet(OUTPUT_DIR / f'L3_{date_range}_Final_vs_OptionMetrics.parquet')
    final_result_compare.to_latex(OUTPUT_DIR / f'L3_{date_range}_Final_vs_OptionMetrics.tex')
    print(' |-- Comparison to OptionMetrics complete, files saved.')
    
    return final_result_compare


def IV_filter(l2_data, date_range):
    """
    Applies log(IV), fits quadratic curve, filters IV outliers.
    Returns both intermediate (L2 with fitted IV) and final (L3) datasets.
    """
    print(' \n>> Running IV filter...')

    # Step 1: Ensure log(IV)
    l2_data['log_iv'] = np.log(l2_data['IV'])

    # Step 2: Fit quadratic IV model and append fitted IV
    print(' |-- IV filter: applying quadratic fit...')
    l2_data = apply_quadratic_iv_fit(l2_data)

    # Step 3: Filter outliers to produce Level 3
    print(' |-- IV filter: filtering outliers...')
    l3_data_iv_only = iv_filter_outliers(l2_data, 'percent', 2.0)
    l3_data_iv_only['moneyness_bin'] = l3_data_iv_only['moneyness_bin'].astype(str)

    # Step 4: Save filtered output
    print(' |-- IV filter: saving L3 IV-filtered data...')
    l3_data_iv_only.to_parquet(DATA_DIR / f'L3_IV_filter_only_{date_range}.parquet')

    return l2_data, l3_data_iv_only




def put_call_filter(df, date_range): 
    """
    Filters option data using the put-call parity filter.

    Args:
        _df: Placeholder parameter, not used in the function.
        date_range (str): The date range for which the option data is filtered.

    Returns:
        DataFrame: The final filtered result after applying the put-call parity filter.
    """
    
    print(' \n>> Running PCP filter...')
    
    # _, l3_iv_only_output_file, l3_output_file = get_filepaths(date_range)
    
    # try:
    #     l3_data_iv_only = pd.read_parquet(DATA_DIR / l3_iv_only_output_file)    
    #     print(' |-- PCP filter: L3 data (IV filter only) loaded...')
    # except FileNotFoundError:
    #     raise FileNotFoundError(f"File {l3_iv_only_output_file} not found. Please run the IV filter first.")
    
    # calculate bid-ask midpoint
    print(' |-- PCP filter: calculating bid-ask midpoint...')
    df['mid_price'] = (df['best_bid'] + df['best_offer']) / 2
    # extract all the call options
    call_options = df.xs('C', level='cp_flag')
    # extract all the put options
    put_options = df.xs('P', level='cp_flag')
    
    print(' |-- PCP filter: building put-call pairs...')
    matching_calls, matching_puts = build_put_call_pairs(call_options.reset_index(drop=True), put_options.reset_index(drop=True))
    # match the puts and calls
    matched_options = pd.merge(matching_calls, matching_puts, on=['date', 'exdate', 'moneyness'], suffixes=('_C', '_P'))
    
    # calculate the PCP implied interest rate 
    print(' |-- PCP filter: calculating PCP implied interest rate...')
    matched_options = calc_implied_interest_rate(matched_options)
    matched_options[matched_options['tb_m3_C'].eq(matched_options['tb_m3_P']) == False][['tb_m3_C', 'tb_m3_P']].isna().sum()
    
    # Calculate the daily median implied interest rate from the T-Bill data (same for calls and puts on a given day)
    daily_median_int_rate = matched_options.groupby('date')['tb_m3_C'].median().reset_index(name='daily_median_rate')
    matched_options = matched_options.join(daily_median_int_rate.set_index('date'), on='date')
    
    print(' |-- PCP filter: filtering outliers...')
    l3_filtered_options = pcp_filter_outliers(matched_options, 'percent', 2.0)
    
    # print(' |-- PCP filter: saving L3 IV- and PCP-filtered data...')
    # save to parquet and latex
    # l3_filtered_options.to_parquet(DATA_DIR / f'L3_filtered_{date_range}.parquet')
    # l3_filtered_options.to_latex(OUTPUT_DIR / l3_output_file.replace('.parquet', '.tex').replace('intermediate/', ''))
    
    # build chart
    print(' |-- PCP filter: building L3 final filtered options chart...')
    l3_filtered_options['log_iv'] = np.log(l3_filtered_options['IV'].where(l3_filtered_options['IV'] > 0))
    #build_l3_data_iv_pcp_chart(l3_filtered_options, date_range)
    print(' |-- PCP filter complete.')
    
    # # compare to optionmetrics
    # global final_result_compare
    # final_result_compare = final_result_compare(l3_filtered_options=l3_filtered_options)

    return l3_filtered_options


def common_iv_charts(data, date_range, fig_name, plot_nan_iv=False, has_fitted_iv=False, has_rel_dist=False, output_dir=OUTPUT_DIR):
    """
    Generalized function to plot IV-related charts.
    Parameters control which additional panels are drawn.
    """
    if plot_nan_iv:
        fig, ax = plt.subplots(2, 3, figsize=(12, 8))
    elif has_rel_dist:
        fig, ax = plt.subplots(3, 3, figsize=(12, 12))
    else:
        fig, ax = plt.subplots(2, 3, figsize=(12, 8))

    ax[0, 0].hist(data['IV'], bins=250, color='darkblue')
    ax[0, 0].set(xlabel='IV', ylabel='Frequency', title='Distribution of IV')
    ax[0, 0].grid()

    ax[0, 1].hist(data['log_iv'], bins=250, color='grey')
    ax[0, 1].set(xlabel='log(IV)', ylabel='Frequency', title='Distribution of log(IV)')
    ax[0, 1].grid()

    if has_fitted_iv:
        ax[0, 2].scatter(data['log_iv'], data['fitted_iv'], color='darkblue', alpha=0.1)
        ax[0, 2].plot([data['log_iv'].min(), data['log_iv'].max()],
                      [data['log_iv'].min(), data['log_iv'].max()],
                      color='red', linestyle='--')
        ax[0, 2].set(xlabel='log(IV)', ylabel='Fitted log(IV)', title='log(IV) vs Fitted log(IV)')
        ax[0, 2].grid()
    elif plot_nan_iv:
        nan_calls = data[(data['cp_flag'] == 'C') & (data['IV'].isna())]
        nan_puts = data[(data['cp_flag'] == 'P') & (data['IV'].isna())]
        if nan_calls.empty and nan_puts.empty:
            ax[0, 2].axis('off')
            ax[1, 2].axis('off')
        else:
            ax[0, 2].scatter(nan_calls['date'], nan_calls['moneyness'], color='blue', alpha=0.1, s=10, label='Calls')
            ax[0, 2].scatter(nan_puts['date'], nan_puts['moneyness'], color='red', alpha=0.1, s=10, label='Puts')
            ax[0, 2].set(xlabel='Trade Date', ylabel='Moneyness', title='Moneyness of NaN IV Options')
            ax[0, 2].legend()
            ax[0, 2].grid()

            pct_nan = data.groupby(['date', 'cp_flag'])['IV'].apply(lambda x: x.isna().mean() * 100)
            ax[1, 2].scatter(pct_nan[pct_nan.index.get_level_values(1) == 'C'].index.get_level_values(0),
                             pct_nan[pct_nan.index.get_level_values(1) == 'C'].values,
                             color='blue', alpha=0.1, s=10, label='Calls')
            ax[1, 2].scatter(pct_nan[pct_nan.index.get_level_values(1) == 'P'].index.get_level_values(0),
                             pct_nan[pct_nan.index.get_level_values(1) == 'P'].values,
                             color='red', alpha=0.1, s=10, label='Puts')
            ax[1, 2].set(xlabel='Trade Date', ylabel='% NaN IV', title='NaN IV % by Date')
            ax[1, 2].legend()
            ax[1, 2].grid()
    else:
        ax[0, 2].axis('off')

    grouped = data.set_index(['date', 'exdate', 'cp_flag'])

    for i, flag in enumerate(['C', 'P']):
        subset = grouped.xs(flag, level='cp_flag')
        ax[1, i].scatter(subset['moneyness'], np.exp(subset['log_iv']), alpha=0.1, label=flag,
                         color='blue' if flag == 'C' else 'red')
        ax[1, i].set(xlabel='Moneyness', ylabel='IV', title=f'IV vs Moneyness ({flag})')
        ax[1, i].grid()

        if has_rel_dist:
            ax[2, i].scatter(subset['moneyness'], subset['rel_distance_iv'], alpha=0.1,
                             color='blue' if flag == 'C' else 'red')
            ax[2, i].set(xlabel='Moneyness', ylabel='Relative Distance %',
                         title=f'Rel. Distance logIV-fitted IV ({flag})')
            ax[2, i].grid()

    if has_rel_dist:
        ax[1, 2].axis('off')
        ax[2, 2].axis('off')

    plt.suptitle(f'Options IV Chart: {date_range.replace("_", " to ")}')
    plt.tight_layout()

    output_file = os.path.join(output_dir, f'L3_{date_range}_{fig_name}.png')
    os.makedirs(output_dir, exist_ok=True)
    fig.savefig(output_file)
    plt.close(fig)


if __name__ == "__main__": 
    date_range = f'{START_DATE_01[:7]}_{END_DATE_01[:7]}'
    df = run_filter(_df=None, date_range=date_range, iv_only=False)