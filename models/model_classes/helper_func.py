"""
Helper functions for multiple independent classes.
"""

import numpy as np
import pandas as pd
from pandas.tseries.frequencies import to_offset
from utilsforecast.preprocessing import fill_gaps

import logging

# Conditional imports to avoid dependency issues
try:
    from darts import TimeSeries
    from darts.metrics import mase

    DARTS_AVAILABLE = True
except ImportError:
    DARTS_AVAILABLE = False
    TimeSeries = None
    mase = None

MIN_SERIES_LEN = 30


def calculate_darts_MASE(
    test_data, train_data, pred_data, seasonality, value_column="y"
):
    """
    Calculates mase using darts.
    """
    if not DARTS_AVAILABLE:
        raise ImportError(
            "darts is required for MASE calculation but not available in this environment"
        )

    hf_logger = logging.getLogger("hf.calculate_darts_MASE")

    try:
        test_data = (
            test_data.pivot(index="ds", columns="unique_id", values="y")
            .reset_index()
            .rename_axis(None, axis=1)
        )
        train_data = (
            train_data.pivot(index="ds", columns="unique_id", values="y")
            .reset_index()
            .rename_axis(None, axis=1)
        )

        pred_data = (
            pred_data.pivot(index="ds", columns="unique_id", values=value_column)
            .reset_index()
            .rename_axis(None, axis=1)
        )

        hf_logger.info(
            "Converted train, test, and pred series into"
            + " darts TimeSeries compatible format."
        )

        # Try to convert to TimeSeries with frequency inference
        try:
            test_data = TimeSeries.from_dataframe(
                test_data, time_col="ds", fill_missing_dates=True, freq=None
            )
            train_data = TimeSeries.from_dataframe(
                train_data, time_col="ds", fill_missing_dates=True, freq=None
            )
            pred_data = TimeSeries.from_dataframe(
                pred_data, time_col="ds", fill_missing_dates=True, freq=None
            )
        except ValueError:
            # Fallback to simple conversion without frequency inference
            hf_logger.warning("Frequency inference failed, using simple conversion")
            test_data = TimeSeries.from_dataframe(
                test_data, time_col="ds", fill_missing_dates=False
            )
            train_data = TimeSeries.from_dataframe(
                train_data, time_col="ds", fill_missing_dates=False
            )
            pred_data = TimeSeries.from_dataframe(
                pred_data, time_col="ds", fill_missing_dates=False
            )

        hf_logger.info("Converted all three series into TimeSeries objects.")

        return mase(test_data, pred_data, train_data, seasonality)

    except Exception as e:
        hf_logger.error(f"Error in MASE calculation: {e}")
        raise e


def extend_df(df, train_data_len, frequency, seasonality, interpolate=True):
    """
    Extends a df to fit seasonality * 4 lags. Doesn't interpolate, but
    adds np.nan as values in the extend rows.
    """
    hf_logger = logging.getLogger("hf.extend_df")

    difference = max(4 * seasonality, MIN_SERIES_LEN) - train_data_len
    new_date = df["ds"].min()
    date_offset = difference * to_offset(frequency)
    new_date -= date_offset

    hf_logger.info(new_date.strftime("%Y-%m-%d, %r") + " is the" + " new start date")

    df = fill_gaps(df, freq=frequency, start=new_date, end="global")

    hf_logger.info("DataFrame extended to fit 4 * seasonality window.")

    return df


def scaled_data(train_data, test_data):

    # Using Sk-learns minmax scaling, scale both series
    # Reference: https://scikit-learn.org/stable/modules/preprocessing.html

    from sklearn import preprocessing

    # Pivots so that scaling is done entity-wise
    train_data = train_data.pivot(index="ds",
                                      columns="unique_id",
                                      values="y")
    
    test_data = test_data.pivot(index="ds",
                                    columns="unique_id",
                                    values="y")

    mmScaler = preprocessing.MinMaxScaler()
    # Trains on training data only
    scaled_train_data = mmScaler.fit_transform(train_data)
    scaled_train_data = pd.DataFrame(scaled_train_data,
                                       columns = train_data.columns,
                                       index = train_data.index)

    # Only transforms test data but doesn't "learn" from it
    scaled_test_data = mmScaler.transform(test_data)
    scaled_test_data = pd.DataFrame(scaled_test_data,
                                      columns = test_data.columns,
                                      index = test_data.index)

    # Undo pivot
    scaled_train_data = scaled_train_data.reset_index().melt(id_vars=["ds"])
    scaled_train_data = scaled_train_data.rename(columns={"value": "y"})
    scaled_test_data = scaled_test_data.reset_index().melt(id_vars=["ds"])
    scaled_test_data = scaled_test_data.rename(columns={"value": "y"})

    return (scaled_train_data, scaled_test_data)

def split_train_test(df, test_split):
    """
    Splits a dataframe using the cutoff date method
    """
    hf_logger = logging.getLogger("split_train_test")

    hf_logger.info("split_train_test called.")
    unique_dates = df['ds'].unique()
    test_length = test_split * len(unique_dates)

    cutoff_date = unique_dates[-test_length]
    hf_logger.debug(f"Cutoff date is {cutoff_date}")

    train_data = df[df['ds'] < cutoff_date]
    test_data = df[df['ds'] >= cutoff_date]
    hf_logger.debug(f"Train series length: {len(train_data)}." +\
                    f"Test series length: {len(test_data)}")

    return (train_data, test_data)

def custom_interpolate(df):
    """
    Entity-wise interpolation. Replaces all-nan columns with series mean.
    """
    hf_logger = logging.getLogger("hf.custom_interpolate")

    hf_logger.info("Interpolating each series in the DataFrame.")

    # Pivots so that each column is an entity
    proc_df = df.pivot(index="ds", columns="unique_id", values="y")

    hf_logger.info("Pivot dataframe to have each entity as " + "a column(wide format).")

    # Interpolates per entity
    proc_df = proc_df.interpolate(limit_direction="both")

    hf_logger.info("Interpolated values in both directions.")

    # Calculate date-wise mean and replace any series which is all NaNs
    date_wise_data_mean = proc_df.mean(axis = 1)

    for col in proc_df.columns:
        if proc_df[col].isna().all():
            proc_df[col] = date_wise_data_mean

    hf_logger.info("Replaced all-nan columns with means.")

    # Melts back to original shape
    proc_df = proc_df.reset_index().melt(id_vars=["ds"])

    hf_logger.info("DataFrame reverted to original shape(long format).")

    # Reset the name
    proc_df = proc_df.rename(columns={"value": "y"})

    return proc_df


def process_df(df, frequency, seasonality, test_split):
    """
    Fills missing dates as per frequency. Extends if train_data is less than
    4 * seasonality.
    """
    hf_logger = logging.getLogger("hf.process_df")

    hf_logger.info("Pre-processing data.")

    # This only adds NaNs as values for missing dates.
    df = fill_gaps(df, freq=frequency, start="global", end="global")

    hf_logger.info("Missing dates added.")

    unique_dates = df["ds"].unique()
    len_ud = len(unique_dates)

    if test_split == "seasonal":
        hf_logger.info("Got test_split as \"seasonal\". Converting to float.")
        if seasonality < len_ud:
            test_split = float(seasonality / len_ud)
            hf_logger.info('Converted test_split from "seasonal" to ' + 
                           f"{test_split}")
        else:
            hf_logger.error(
                'test_split = "seasonal" is not applicable.'
                + "Series is shorter than seasonality."
            )
            raise ValueError(
                "Series too short. " + "Please select appropriate test split."
            )

    test_length = int(test_split * len_ud)
    train_data_len = len_ud - test_length

    if (train_data_len < 4 * seasonality) or (train_data_len < 
                                                MIN_SERIES_LEN):
        hf_logger.info("Train series shorter than seasonality * 4.")
        df = extend_df(df, train_data_len, frequency, seasonality)

        test_split = float(test_length / len(unique_dates))
    
    train_data, test_data = split_train_test(df, test_split)
    hf_logger.info("Split into train and test.")

    train_data = custom_interpolate(train_data)
    hf_logger.info("Interpolation complete.")

    train_data, test_data = scaled_data(train_data, test_data)
    hf_logger.info("Scaling complete.")

    # float32 conversion is standardised accross implementations
    train_data['y'] = train_data['y'].astype(np.float32)
    test_data['y'] = test_data['y'].astype(np.float32)
    hf_logger.info("Converted y values to np.float32.")

    # The train series should now have all defined entries
    # The test series doesn't have any synthetic data

    hf_logger.info("Processing complete.")

    return (train_data, test_data, test_split)


def print_sep():
    sep = ""
    for i in range(67):
        sep += "-"
    print(sep)


def common_error_catch(f):
    """
    A decorator to add generic error catching in any function.
    """

    def error_catcher(*args):
        hf_logger = logging.getLogger("hf.common_error_catch")
        try:
            return f(*args)
        except Exception:
            print_sep()
            print(
                f"\nError in {f.__name__}. Please check logs. "
                + "There is a possibility that this error is insignificant "
                + "and can be ignored."
            )
            hf_logger.exception(f"Error in {f.__name__}.")
            print_sep()
            return None

    return error_catcher
