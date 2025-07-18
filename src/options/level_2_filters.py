"""
This module contains functions to filter options data based on time to maturity, implied volatility, moneyness, and implied interest rate.
"""

import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import bsm_pricer as bsm
import load_option_data_01 as l1
import level_1_filters as f1
import level_3_filters as f3
from pathlib import Path
import config

DATA_DIR = Path(config.DATA_DIR)


def calc_days_to_maturity(df):
    # calc days to maturity
    df = df.assign(days_to_maturity = df['exdate'].subtract(df['date']))
    return df

def days_to_maturity_filter(df, min_days=7, max_days=180):
    df = calc_days_to_maturity(df)
    df = df[(df['days_to_maturity'] >= pd.Timedelta(days=min_days)) & (df['days_to_maturity'] <= pd.Timedelta(days=max_days))]
    return df

def iv_range_filter(df, min_iv=0.05, max_iv=1.00):
    """Filter options based on implied volatility range.
       Default is 5% to 100% (0.05 to 1.00).
    """
    df = df[(df['IV'] >= min_iv) & (df['IV'] <= max_iv)]
    return df


def moneyness_filter(df, min_moneyness=0.8, max_moneyness=1.2):
    """Filter options based on moneyness range.
       Default is 0.8 to 1.2.
       Moneyness is defined as the ratio of the option's strike price to the stock underlying price.
    """
    if 'moneyness' not in df.columns:
        df = f1.calc_moneyness(df)
    df = df[(df['moneyness'] > min_moneyness) & (df['moneyness'] < max_moneyness)].reset_index(drop=True)
    return df


def implied_interest_rate_filter(df):
    """
    Filters out options implying a negative interest rate based on put-call parity.
    Imputes missing rates using ATM options by maturity.
    """

    df['mid_price'] = (df['best_bid'] + df['best_offer']) / 2

    # Split calls and puts
    calls = df[df['cp_flag'] == 'C'].copy()
    puts = df[df['cp_flag'] == 'P'].copy()

    # Match by date, exdate, moneyness
    calls.set_index(['date', 'exdate', 'moneyness'], inplace=True)
    puts.set_index(['date', 'exdate', 'moneyness'], inplace=True)
    common = calls.index.intersection(puts.index)
    c, p = calls.loc[common].reset_index(), puts.loc[common].reset_index()

    # Merge and compute implied interest rate
    matched = pd.merge(c, p, on=['date', 'exdate', 'moneyness'], suffixes=('_C', '_P'))
    matched = f3.calc_implied_interest_rate(matched)

    # Remove rows with negative implied rate
    neg = matched[matched['pc_parity_int_rate'] < 0][['date', 'exdate', 'strike_price_C', 'close_C']].drop_duplicates()
    df = df.merge(neg, left_on=['date', 'exdate', 'strike_price', 'close'], 
                       right_on=['date', 'exdate', 'strike_price_C', 'close_C'], 
                       how='outer', indicator=True)
    df = df[df['_merge'] == 'left_only'].drop(columns=['_merge', 'strike_price_C', 'close_C'])

    # Impute missing rates using median from ATM calls
    atm = matched[
        (matched['moneyness'].between(0.95, 1.05)) &
        (matched['pc_parity_int_rate'] >= 0)
    ]
    med = atm.groupby('days_to_maturity_C')['pc_parity_int_rate'].median().reset_index()
    df = df.merge(med, left_on='days_to_maturity', right_on='days_to_maturity_C', how='left')
    df['pc_parity_int_rate'] = df['pc_parity_int_rate'].ffill()
    df.drop(columns='days_to_maturity_C', inplace=True)

    return df


def unable_to_compute_iv_filter(df):
    """
    Removes options where the time value is negative and IV cannot be computed.
    Time value = market price - intrinsic value.
    For calls: intrinsic = max(S - K, 0)
    For puts:  intrinsic = max(K - S, 0)
    """
    # df = df.loc[df['IV'].notna()]
    df['mid_price'] = (df['best_bid'] + df['best_offer']) / 2

    # Calculate intrinsic value
    df['intrinsic'] = 0
    call_mask = df['cp_flag'] == 'C'
    put_mask = df['cp_flag'] == 'P'
    df.loc[call_mask, 'intrinsic'] = (df.loc[call_mask, 'close'] - df.loc[call_mask, 'strike_price']).clip(lower=0)
    df.loc[put_mask,  'intrinsic'] = (df.loc[put_mask,  'strike_price'] - df.loc[put_mask,  'close']).clip(lower=0)

    # Filter out rows where time value is negative
    df = df[df['mid_price'] >= df['intrinsic']]

    return df




def apply_l2_filters(df):
    """Apply all level 2 filters to the dataframe.
    """
    df = filter_days_to_maturity(df)
    df = filter_iv(df)
    df = filter_moneyness(df)
    df = filter_implied_interest_rate(df)
    df = filter_unable_compute_iv(df)
    return df

# if __name__ == "__main__": 