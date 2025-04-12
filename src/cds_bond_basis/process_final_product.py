from pathlib import Path
from settings import config
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import CubicSpline

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

OUTPUT_DIR = config("OUTPUT_DIR")
DATA_DIR = config("DATA_DIR")

FINAL_ANALYSIS_FILE_NAME = "final_data.parquet"


def process_cb_spread(df):
    '''
    INPUT WAS PREVIOUS FINAL PRODUCT
    df: dataframe with par spread values merged into all values where there was a possible cubic spline
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

    output:
        additional columns:
        FR: Z-spread of the bond
            FR = yield - treas_yld
        CB: implied return on CDS-bond spread
            CB = par_spread - FR
        rfr: implied risk free rate
            rfr = treas_yld - CB
    '''
    df['FR'] = df['yield'] - df['treas_yld']
    df['CB'] = df['par_spread'] - df['FR']
    df['rfr'] = df['treas_yld'] - df['CB']

    df = df[df['rfr'] < 1] # remove unreasonable data, rfr is in absolute space

    return df


def generate_graph(df, col='rfr', col2=None, two=False):
    '''
    Generates a time series plot for given columns based on bond ratings.
    
    Parameters:
    - df: DataFrame containing financial data.
    - col: Primary column to graph (default is 'rfr').
    - col2: Secondary column to graph if two=True.
    - two: Boolean flag indicating whether to plot a second column with a secondary axis.
    '''
    df['date'] = pd.to_datetime(df['date'])

    # Compute the mean of the specified column(s) per (date, rating) pair
    df_grouped = df.groupby(['date', 'rating'])[col].mean().reset_index()

    if two and col2 is not None:
        df_grouped[col2] = df.groupby(['date', 'rating'])[col2].mean().reset_index()[col2]

    # Create the figure and primary axis
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot for Investment Grade (IG) (rating = 0) on primary axis
    df_ig = df_grouped[df_grouped['rating'] == 0]
    ax1.plot(df_ig['date'], df_ig[col], label=f"IG - {col}", linestyle='-', marker='o', color='tab:blue')

    # Plot for High Yield (HY) (rating = 1) on primary axis
    df_hy = df_grouped[df_grouped['rating'] == 1]
    ax1.plot(df_hy['date'], df_hy[col], label=f"HY - {col}", linestyle='-', marker='s', color='tab:orange')

    # Configure primary axis
    ax1.set_xlabel("Date")
    ax1.set_ylabel(f"{col} (Primary Axis)", color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # Add secondary axis if two=True and col2 is provided
    if two and col2 is not None:
        ax2 = ax1.twinx()  # Create secondary y-axis
        
        # Plot for Investment Grade (IG) (rating = 0) on secondary axis
        ax2.plot(df_ig['date'], df_ig[col2], label=f"IG - {col2}", linestyle='--', marker='x', color='tab:green')
        
        # Plot for High Yield (HY) (rating = 1) on secondary axis
        ax2.plot(df_hy['date'], df_hy[col2], label=f"HY - {col2}", linestyle='--', marker='d', color='tab:red')

        # Configure secondary axis
        ax2.set_ylabel(f"{col2} (Secondary Axis)", color='tab:green')
        ax2.tick_params(axis='y', labelcolor='tab:green')
        ax2.legend(loc='upper right')

    # Set title
    title = f"Time Series Plot of {col}" + (f" and {col2}" if two and col2 is not None else "")
    plt.title(title)
    
    plt.savefig(OUTPUT_DIR / title)

    # Show the plot
    plt.show()

    




                


