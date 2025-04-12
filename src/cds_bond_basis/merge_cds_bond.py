import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from tqdm import tqdm
import ctypes
from scipy.interpolate import CubicSpline

from settings import config


DATA_DIR = config("DATA_DIR")
BOND_RED_CODE_FILE_NAME = "merged_bond_treasuries_redcode.parquet"
CDS_FILE_NAME = "cds_final.parquet"
FINAL_ANALYSIS_FILE_NAME = "final_data.parquet"



def merge_cds_into_bonds(bond_red_df, cds_df):
    '''
    bond_red_df: dataframe with the issuer cusip and red_code now added
        company_symbol, -- Company Symbol (issuer stock ticker).
        maturity, -- Date that the issue's principal is due for repayment.
        amount_outstanding, -- The amount of the issue remaining outstanding (sum of face values).
        date, -- Monthly Date (report date)
        yield, -- ytm at report date
        issuer_cusip, -- 6 character issuer cusip
        rating, -- Combined Rating Class: 0.IG or 1.HY
        price_eom, -- Price-End of Month (reported price)
        t_spread, -- Avg Bid/Ask Spread
        treas_yld, -- yield of similar treasury
        redcode -- redcode is issuer specific, used to merge CDS values later on
    cds_df: dataframe containing cds_data
        date, -- date of report 
        'ticker', -- ticker of issuer
        'redcode', -- redcode of issuer
        'parspread', -- parspread
        'tenor', -- tenor, how long
        'tier', -- tier of debt
        'country', -- country of issuer
        'year' -- year of date
    
    output: dataframe with par spread values merged into all values where there was a possible cubic spline
       'cusip', -- unique bond tag
       'date', -- reporting date
       'maturity', -- maturity date of bond
       'yield', -- corporate bond yield
       'rating', -- rating: 1 for HY, 0 for IG
       'treas_yld', -- treasury yield for similar maturity and same report date
       'par_spread', -- parspread of CDS, backed out by Cubic Spline
       't_spread', -- bid ask spread on bond
       'price_eom', -- End Of Month Price of bond
       'amount_outstanding' -- face value outstanding

    '''
    date_set = set(bond_red_df.date.unique())
    cds_df = cds_df[cds_df['date'].isin(date_set)].dropna(subset=['date', 'parspread', 'tenor', 'redcode'])

    # par spread values are roughly consistent for each tenor, make broad assumptions on true value on par spread
    c_df_avg = cds_df.groupby(cds_df.columns.difference(['parspread']).tolist(), as_index=False).agg({'parspread': 'median'})

    df_unique_count = c_df_avg.groupby(['redcode', 'date'])['tenor'].nunique().reset_index()
    df_unique_count.rename(columns={'tenor': 'unique_tenor_count'}, inplace=True)

    # need at least 2 for cubic spline
    df_unique_count = df_unique_count[df_unique_count['unique_tenor_count'] > 1]

    # grab the filtered_cds_df by using df_uni_count as a filter
    filtered_cds_df = c_df_avg.merge(df_unique_count[['redcode', 'date']], on=['redcode', 'date'], how='inner')

    # my mapping to convert tenor to days to get a rough approximation of a daily spline
    tenor_to_days = {
        "1Y": 365,
        "3Y": 3 * 365,
        "5Y": 5 * 365,
        "7Y": 7 * 365,
        "10Y": 10 * 365
    }

    filtered_cds_df['tenor_days'] = filtered_cds_df['tenor'].map(tenor_to_days)

    # Dictionary to store cubic splines for each (redcode, date) pair
    cubic_splines = {}

    # Group by (redcode, date) and create splines
    for (redcode, date), group in filtered_cds_df.groupby(['redcode', 'date']):
        x = group['tenor_days'].values
        y = group['parspread'].values
        
        sorted_indices = np.argsort(x)
        x_sorted, y_sorted = x[sorted_indices], y[sorted_indices]

        # Fit cubic spline
        try:
            cubic_splines[(redcode, date)] = CubicSpline(x_sorted, y_sorted)
        except:
            print(x_sorted)
            print(y_sorted)

    # START filtering the bond dataframe to make the merge easier
    red_set = set(filtered_cds_df['redcode'].unique())
    bond_red_df_df = bond_red_df[bond_red_df['redcode'].isin(red_set)]

    # add days for putting into cubic spline
    bond_red_df['days'] = (bond_red_df['maturity'] - bond_red_df['date']).dt.days

    # vectorized function to grab the par spread
    def add_par_spread_vectorized(df):
        mask = df.set_index(['redcode', 'date']).index.isin(cubic_splines.keys())

        # spline interpolation only for matching keys
        valid_rows = df.loc[mask]
        df.loc[mask, 'par_spread'] = valid_rows.apply(
            lambda row: cubic_splines[(row['redcode'], row['date'])](row['days']), axis=1
        )

        df['par_spread'] = df['par_spread'].fillna(np.nan)
        
        return df
    
    par_df = add_par_spread_vectorized(bond_red_df)
    par_df = par_df.dropna(subset=['par_spread'])

    # keep only the important columns
    par_df = par_df[['cusip', 'date', 'maturity', 'yield', 'rating', 'treas_yld', 'par_spread', 't_spread', 'price_eom', 'amount_outstanding']]

    # have had issues with a phantom array column
    def safe_convert(x):
        """Convert lists and arrays to tuples while keeping other data types unchanged."""
        if isinstance(x, list):
            return tuple(x)
        elif isinstance(x, np.ndarray):
            return tuple(x.tolist()) if x.ndim > 0 else x.item()  # Convert array to tuple if not scalar
        else:
            return x

    # Apply safe conversion
    par_df = par_df.applymap(safe_convert)
    par_df = par_df.drop_duplicates()

    return par_df




def main():
    """
    Main function to load data, process it, and merge Treasury data into Bonds.
    """
    print("Loading data...")
    CDS1 = pd.read_parquet(f"{DATA_DIR}/markit_cds_1.parquet")
    CDS2 = pd.read_parquet(f"{DATA_DIR}/markit_cds_2.parquet")
    CDSs = pd.concat([CDS1, CDS2], ignore_index=True)
    CDSs.to_parquet(f"{DATA_DIR}/{CDS_FILE_NAME}")

    # Load DataFrames
    bond_red_df = pd.read_parquet(f"{DATA_DIR}/{BOND_RED_CODE_FILE_NAME}")
    
    print("Merging CDS into Bonds...")
    fin_df = merge_cds_into_bonds(bond_red_df, CDSs)

    print("Saving processed data...")
    fin_df.to_parquet(f"{DATA_DIR}/{FINAL_ANALYSIS_FILE_NAME}")

    print("Processing complete. Data saved.")



if __name__ == "__main__":
    main()




        

    




    
