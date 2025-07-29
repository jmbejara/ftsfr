"""
Helper functions for multiple independent classes.
"""
import pandas as pd
import numpy as np
from pandas.tseries.frequencies import to_offset
from darts import TimeSeries
from darts.metrics import mase
from utilsforecast.preprocessing import fill_gaps

def calculate_darts_MASE(test_series, train_series, pred_series, 
                         seasonality, value_column = "y"):
    """
    Calculates mase using darts.
    """
    test_series = (
        test_series.pivot(index = "ds", 
                                columns = "unique_id", 
                                values = "y")
        .reset_index()
        .rename_axis(None, axis=1)
    )
    train_series = (
        train_series.pivot(index = "ds", 
                                columns = "unique_id", 
                                values = "y")
        .reset_index()
        .rename_axis(None, axis=1)
    )

    pred_series = (
        pred_series.pivot(index = "ds",
                            columns = "unique_id",
                            values = value_column)
        .reset_index()
        .rename_axis(None, axis=1)
    )

    test_series = TimeSeries.from_dataframe(test_series, 
                                            time_col="ds")
    train_series = TimeSeries.from_dataframe(train_series, 
                                        time_col="ds")
    pred_series = TimeSeries.from_dataframe(pred_series, 
                                            time_col="ds")

    return mase(test_series, pred_series, train_series, seasonality)

def extend_df(df, train_series_len, frequency, seasonality, interpolate = True):
    """
    Extends a df to fit seasonality * 4 lags. Doesn't interpolate, but
    adds np.nan as values in the extend rows.
    """
    difference = 4 * seasonality - train_series_len
    new_date = df['ds'].min()
    date_offset = difference * to_offset(frequency)
    new_date -= date_offset

    df = fill_gaps(df,
                   freq = frequency,
                   start = new_date,
                   end = 'global')
    
    return df

def process_df(df, frequency, seasonality, test_split):
    """
    Fills missing dates as per frequency. Extends if train_series is less than
    4 * seasonality.
    """
    df = fill_gaps(df,
                   freq = frequency,
                   start = "global",
                   end = "global")

    unique_dates = df["ds"].unique()
    len_ud = len(unique_dates)

    if test_split == "seasonal":
        if seasonality < len_ud:
            test_split = float(seasonality / len_ud)
        else:
            raise ValueError("Series too short. " +
                             "Please select appropriate test split.")
    
    test_length = int(test_split * len_ud)
    train_series_len = len_ud - test_length

    if train_series_len < 4 * seasonality:
        df = extend_df(df, train_series_len, frequency, seasonality)
        
        unique_dates = df['ds'].unique()
        test_split = float(test_length / len(unique_dates))
    
    return (df, test_split)

def custom_interpolate(df):
    """
    Entity-wise interpolation.
    """
    # Pivots so that each column is an entity
    proc_df = df.pivot(index="ds",
                           columns="unique_id",
                           values="y")
    
    # Interpolates per entity
    proc_df = proc_df.interpolate(limit_direction = 'both')

    # Melts back to original shape
    proc_df = proc_df.reset_index().melt(id_vars = ['ds'])

    # Reset the name
    proc_df = proc_df.rename(columns = {"value" : "y"})

    return proc_df


def common_error_catch(f):
    """
    A decorator to add generic error catching in any function.
    """
    def error_catcher(*args):
        try:
            return f(*args)
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in {f.__name__} for {self.model_name}." +
                " Full traceback above \u2191")
            self.print_sep()
            return None
    return error_catcher