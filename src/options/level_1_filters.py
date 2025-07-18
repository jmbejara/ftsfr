import pandas as pd
import numpy as np
import config
from pathlib import Path 

import load_option_data_01 
import time 

import bsm_pricer as bsm 
import datetime 
OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)
WRDS_USERNAME = config.WRDS_USERNAME

START_DATE_01 =config.START_DATE_01
END_DATE_01 = config.END_DATE_01

START_DATE_02 =config.START_DATE_02
END_DATE_02 = config.END_DATE_02

"""
This script contains the relevant functions for executing the lvl1 filters in appendix B. 
"""

def getLengths(df): 
	""" Helper function to get the lengths of the dataframe and the number of calls and puts
	"""
	test1 = df['cp_flag'].value_counts().to_dict()
	test1C = test1['C']
	test1P = test1['P'] 
	test1L = len(df)
	return np.array([test1L, test1C, test1P])


def getSecPrice(df): 
	""" Helper function to get the security price from the dataframe
	"""
	df['sec_price'] =  df['close']
	return df

def calc_moneyness(df):
	""" Helper function to calculate the moneyness of the options
	"""
	df['moneyness'] = df['strike_price']/df['close']
	return df

def identical_filter(df):
	""" Helper function to delete identical options from the dataframe
		Remove identical options (type, strike, expiration date, price). Filter is applied to the buyside/offer/ask side of the market
		to minimize risk of entering a position and not being able to exit. 
	"""
	columns_to_check = ['secid', 'cp_flag', 'strike_price','date', 'exdate', 'best_offer']
	df = df.drop_duplicates(subset=columns_to_check, keep='first')
	return df	


def identical_but_price_filter(df):
    """
    Vectorized version of identical_but_price_filter.
    Removes duplicate options (same secid, date, cp_flag, strike_price, exdate) but different prices.
    Keeps the quote whose IV is closest to the implied volatility of the moneyness-nearest neighbor.
    """

    keys = ['secid', 'date', 'cp_flag', 'strike_price', 'exdate']
    group_keys = ['secid', 'cp_flag', 'date', 'exdate']

    # Identify duplicate entries
    is_dup = df.duplicated(subset=keys, keep=False)
    df_unique = df[~is_dup]
    df_dupes = df[is_dup].copy()

    # Identify moneyness neighbors
    is_neighbor = df.set_index(group_keys).index.isin(df_dupes.set_index(group_keys).index)
    neighbors = df[is_neighbor].copy()

    # Compute absolute distance from moneyness = 1
    neighbors['moneyness_dist'] = (neighbors['moneyness'] - 1).abs()

    # Get index of nearest neighbor by minimum moneyness distance
    idx_neighbors = neighbors.groupby(group_keys)['moneyness_dist'].idxmin()
    nearest = df.loc[idx_neighbors].copy()
    nearest['mon_IV'] = nearest['IV'].fillna(0)

    # Merge reference IV into duplicate set
    df_joined = pd.merge(df_dupes, nearest[group_keys + ['mon_IV']], on=group_keys, how='inner')
    df_joined['IV_adj'] = df_joined['IV'].fillna(0)

    # Compute distance from neighbor IV
    df_joined['vola_dist'] = (df_joined['IV_adj'] - df_joined['mon_IV']).abs()

    # Find idx of rows with minimum vola distance per group
    idx_keep = df_joined.groupby(group_keys)['vola_dist'].idxmin()
    kept = df_joined.loc[idx_keep].drop(columns=['IV_adj', 'mon_IV', 'vola_dist'])

    # Combine with unique entries
    df_final = pd.concat([df_unique, kept], ignore_index=True)
    df_final = df_final.sort_values(by=['cp_flag', 'date']).reset_index(drop=True)

    return df_final


def delete_zero_bid_filter(df): 
	""" Helper function to delete options with zero bid from the dataframe
	"""
	df = df[df['best_bid'] != 0.0]
	return df 

def delete_zero_volume_filter(df): 
	""" Helper function to delete options with zero volume from the dataframe
		We do not implement this filter in the current version of the code
	"""
	df = df[df['volume'] != 0.0]
	#df = df[df['open_interest'] != 0.0]
	return df 

def delete_open_interest_filter(df): 
	""" Helper function to delete options with zero open interest from the dataframe
		We do not implement this filter in the current version of the code
	"""
	df = df[df['open_interest'] != 0.0]
	return df 

def keep_volume(df):
	""" Helper function to do nothing
	
	"""
	return df

def appendixBfilter_level1(df): 
	""" Function to apply the filters from Appendix B of the paper
	"""
	df = getSecPrice(df)
	df = calc_moneyness(df)

	rows = ["Total", "Calls", "Puts"]
	df_sum = pd.DataFrame(index = rows)

	L0 = getLengths(df)
	df_sum['Starting'] = L0


	df = identical_filter(df)
	L1 = getLengths(df)
	df_sum['Identical'] =  L0-L1


	df = identical_but_price_filter(df)
	L2 = getLengths(df)
	df_sum['Identical but Price'] = L1-L2


	df = delete_zero_bid_filter(df)
	L3 = getLengths(df)
	df_sum['Bid = 0'] =  L2-L3

	df = delete_zero_volume_filter(df)
	L4 = getLengths(df)
	df_sum['Volume = 0'] =   L3-L4
	df_sum['Final'] =  L4
	

	rows_B = ['Step', 'Deleted', 'Remaining']
	df_B1 = pd.DataFrame(index = rows_B)
	df_B1['Calls0'] = ['Starting', float('nan'), L0[1]]
	df_B1['Puts0'] = ['Starting', float('nan'), L0[2]]
	df_B1['All0'] = ['Starting', float('nan'), L0[0]]

	df_B1['Identical'] = ['Level 1 filters', (L0-L1)[0],float('nan')]
	df_B1['Identical except price'] = ['Level 1 filters', (L1-L2)[0],float('nan')]
	df_B1['Bid = 0'] = ['Level 1 filters', (L2-L3)[0],float('nan')]
	df_B1['Volume = 0'] = ['Level 1 filters', (L3-L4)[0],float('nan')]
	df_B1['All1'] = ['Level 1 filters', float('nan'), L4[0]]

	df_B1 = df_B1.T
	df_sum = df_sum.T
	return df, df_sum, df_B1


def execute_appendixBfilter_level1(start=START_DATE_01, end=END_DATE_01): 
	""" Function to execute the filters from Appendix B of the paper
	"""
	df = load_option_data_01.load_all_optm_data(data_dir=DATA_DIR,
											wrds_username=WRDS_USERNAME, 
											startDate=start,
											endDate=end)

	dfB1, df_sum, df_tableB1 = appendixBfilter_level1(df)
	startYearMonth = dfB1['date'].min().year*100 + dfB1['date'].min().month
	endYearMonth = dfB1['date'].max().year*100 + dfB1['date'].max().month
	
	save_path = DATA_DIR.joinpath( f"intermediate/data_{start[:7]}_{end[:7]}_L1filter.parquet")
	dfB1.to_parquet(save_path)
	print(f"\nData {start}-{end}, Filtered Level B1 saved to: {save_path}")
	 # @ihammock try this: df_tableB1 = df_tableB1.reset_index().rename(columns={'index': 'Substep'}).set_index(['Step', 'Substep'])
	b1path = OUTPUT_DIR.joinpath(f"tableB1_{start[:7]}_{end[:7]}.parquet")
	df_tableB1.to_parquet(b1path)

	print(f"Table B1 {start}-{end}, Level 1 saved to: {b1path}")
	return dfB1, df_tableB1

	
if __name__ == "__main__": 
	t0 = time.time()
	df01, tB01 = execute_appendixBfilter_level1(start=START_DATE_01, end=END_DATE_01)
	t1 = time.time()-t0
	print(f"Took {t1} to complete Level B1 Analysis on {START_DATE_01} -> {END_DATE_01} \n")


	t0 = time.time()
	df02, tB02 = execute_appendixBfilter_level1(start=START_DATE_02, end=END_DATE_02)
	t1 = time.time()-t0
	print(f"Took {t1} to complete Level B1 Analysis on {START_DATE_02} -> {END_DATE_02} \n")

	