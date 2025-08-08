"""
Pulls data from Bloomberg or local files. Cleans if required.
"""

import pandas as pd
from xbbg import blp
from datetime import timedelta
import os
from pathlib import Path
from settings import config

data_dir = Path(config("DATA_DIR"))

def pull_raw_tyields(override_download = False):
    """Pull raw treasury yield data

    :param override_download: If set to True, downloaded data is ignored
    :type override_download: bool, default = False

    :return: Raw treasury yield data
    :rtype: pd.DataFrame
    """
    file_dir = os.path.join(data_dir, 'bbg')
    file = os.path.join(file_dir, 'raw_tyields.pkl')
    if os.path.exists(file) and not override_download:
        print('Loading local treasury yield data.')
        df = pd.read_pickle(file)
    else:
        print('Fetching treasury yield data from Bloomberg')
        TODAY = pd.to_datetime('today').normalize() - timedelta(days=1)
        months = [1, 2, 3, 4, 6, 12]
        years = [2, 3, 5, 7, 10, 20, 30]
        t_list = [f'GB{x} Govt' for x in months] + [f'GT{x} Govt' for x in years]
        try:
            df = blp.bdh(
                tickers = t_list,
                flds = ['PX_LAST',],
                start_date = '2000-01-01',
                end_date = TODAY
            )
        except Exception as e:
            print(f'Failed Bloomberg data pull.  See error below.')
            raise e
        df = df.rename(columns = {'GB12 Govt': 'GT1 Govt'})
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        df.to_pickle(file)
    return df

def pull_raw_syields(override_download = False):
    """Pull raw swap yield data

    :param override_download: If set to True, downloaded data is ignored
    :type override_download: bool, default = False
    
    :return: Raw swap yield data
    :rtype: pd.DataFrame
    """
    file_dir = os.path.join(data_dir, 'bbg')
    file = os.path.join(file_dir, 'raw_syields.pkl')
    if os.path.exists(file) and not override_download:
        print('Loading local swap yield data.')
        df = pd.read_pickle(file)
    else:
        print('Fetching swap yield data from Bloomberg')
        TODAY = pd.to_datetime('today').normalize() - timedelta(days=1)
        years = [1, 2, 3, 5, 10, 20, 30]
        swap_list = [f'USSO{x} CMPN Curncy' for x in years]
        try:
            df = blp.bdh(
                tickers = swap_list,
                flds = ['PX_LAST',],
                start_date = '2000-01-01',
                end_date = TODAY
            )
        except Exception as e:
            print(f'Failed Bloomberg data pull. See error below.')
            raise e
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        df.to_pickle(file)
    return df

def clean_raw_tyields(raw_df, override = False, save_data = True):
    """Cleans treasury yield data

    :param raw_df: Data Frame to clean
    :type raw_df: pd.DataFrame
    :param override: If set to True, downloaded data is ignored
    :type override: bool, default = False
    :type save_data: bool, default = True

    :return: Cleaned treasury yield data frame
    :rtype: pd.DataFrame
    """
    if save_data:
        file_dir = os.path.join(data_dir, 'bbg')
        file = os.path.join(file_dir, 'tyields.pkl')
        if os.path.exists(file) and not override:
            print('Loading local cleaned treasury yield data.')
            df = pd.read_pickle(file)
        else:
            df = raw_df.apply(pd.to_numeric, errors = 'coerce')
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            df.to_pickle(file)
    else:
        df = raw_df.apply(pd.to_numeric, errors = 'coerce')
    return df

def clean_raw_syields(raw_df, override = False, save_data = True):
    """Cleans swap yield data

    :param raw_df: Data Frame to clean
    :type raw_df: pd.DataFrame
    :param override: If set to True, downloaded data is ignored
    :type override: bool, default = False
    :type save_data: bool, default = True

    :return: Cleaned swap yield data frame
    :rtype: pd.DataFrame
    """
    if save_data:
        file_dir = os.path.join(data_dir, 'bbg')
        file = os.path.join(file_dir, 'syields.pkl')
        if os.path.exists(file) and not override:
            print('Loading local cleaned swap yield data.')
            df = pd.read_pickle(file)
        else:
            df = raw_df.apply(pd.to_numeric, errors = 'coerce')
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            
            df.to_pickle(file)
    else:
        df = raw_df.apply(pd.to_numeric, errors = 'coerce')
    return df

def bloom_main():
    """Main function which pulls data and cleans it
    
    :return: Cleaned treasury yield and swap yield data frame
    :rtype: pd.DataFrame
    """
    
    tyields = clean_raw_tyields(pull_raw_tyields())

    syields = clean_raw_syields(pull_raw_syields())

    return tyields, syields

if __name__ == '__main__':
    bloom_main()