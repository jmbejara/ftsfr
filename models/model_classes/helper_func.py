"""
Helper functions to be used independent of classes.
"""

import numpy as np
import pandas as pd
from pandas.tseries.frequencies import to_offset
from utilsforecast.preprocessing import fill_gaps
from scipy.stats.mstats import winsorize
import traceback

import logging

# Conditional imports to avoid dependency issues
try:
    from darts import TimeSeries
    from darts.metrics import mase, mae, rmse

    DARTS_AVAILABLE = True
except ImportError:
    DARTS_AVAILABLE = False
    TimeSeries = None
    mase = None
    mae = None
    rmse = None

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
        test_data = test_data.pivot(
            index="ds", columns="unique_id", values="y"
        ).rename_axis(None, axis=1)
        train_data = train_data.pivot(
            index="ds", columns="unique_id", values="y"
        ).rename_axis(None, axis=1)

        pred_data = pred_data.pivot(
            index="ds", columns="unique_id", values=value_column
        ).rename_axis(None, axis=1)

        hf_logger.info(
            "Converted train, test, and pred series into"
            + " darts TimeSeries compatible format."
        )

        # Try to convert to TimeSeries with frequency inference
        try:
            test_data = TimeSeries.from_dataframe(test_data)
            train_data = TimeSeries.from_dataframe(train_data)
            pred_data = TimeSeries.from_dataframe(pred_data)
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


def calculate_darts_MAE(test_data, pred_data, value_column="y"):
    """
    Calculates MAE using darts by converting from Nixtla format.
    """
    if not DARTS_AVAILABLE:
        raise ImportError(
            "darts is required for MAE calculation but not available in this environment"
        )

    hf_logger = logging.getLogger("hf.calculate_darts_MAE")

    try:
        test_data = test_data.pivot(
            index="ds", columns="unique_id", values="y"
        ).rename_axis(None, axis=1)
        pred_data = pred_data.pivot(
            index="ds", columns="unique_id", values=value_column
        ).rename_axis(None, axis=1)

        hf_logger.info(
            "Converted test and pred series into darts TimeSeries compatible format."
        )

        # Try to convert to TimeSeries with frequency inference
        try:
            test_data = TimeSeries.from_dataframe(test_data)
            pred_data = TimeSeries.from_dataframe(pred_data)
        except ValueError:
            # Fallback to simple conversion without frequency inference
            hf_logger.warning("Frequency inference failed, using simple conversion")
            test_data = TimeSeries.from_dataframe(
                test_data, time_col="ds", fill_missing_dates=False
            )
            pred_data = TimeSeries.from_dataframe(
                pred_data, time_col="ds", fill_missing_dates=False
            )

        hf_logger.info("Converted series into TimeSeries objects.")

        return mae(test_data, pred_data)

    except Exception as e:
        hf_logger.error(f"Error in MAE calculation: {e}")
        raise e


def calculate_darts_RMSE(test_data, pred_data, value_column="y"):
    """
    Calculates RMSE using darts by converting from Nixtla format.
    """
    if not DARTS_AVAILABLE:
        raise ImportError(
            "darts is required for RMSE calculation but not available in this environment"
        )

    hf_logger = logging.getLogger("hf.calculate_darts_RMSE")

    try:
        test_data = test_data.pivot(
            index="ds", columns="unique_id", values="y"
        ).rename_axis(None, axis=1)
        pred_data = pred_data.pivot(
            index="ds", columns="unique_id", values=value_column
        ).rename_axis(None, axis=1)

        hf_logger.info(
            "Converted test and pred series into darts TimeSeries compatible format."
        )

        # Try to convert to TimeSeries with frequency inference
        try:
            test_data = TimeSeries.from_dataframe(test_data)
            pred_data = TimeSeries.from_dataframe(pred_data)
        except ValueError:
            # Fallback to simple conversion without frequency inference
            hf_logger.warning("Frequency inference failed, using simple conversion")
            test_data = TimeSeries.from_dataframe(
                test_data, time_col="ds", fill_missing_dates=False
            )
            pred_data = TimeSeries.from_dataframe(
                pred_data, time_col="ds", fill_missing_dates=False
            )

        hf_logger.info("Converted series into TimeSeries objects.")

        return rmse(test_data, pred_data)

    except Exception as e:
        hf_logger.error(f"Error in RMSE calculation: {e}")
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

    scaled_data_logger = logging.getLogger("hf.scaled_data")

    from sklearn import preprocessing

    # Pivots so that scaling is done entity-wise
    train_data = train_data.pivot(index="ds", columns="unique_id", values="y")

    test_data = test_data.pivot(index="ds", columns="unique_id", values="y")

    scaled_data_logger.info("Pivot train and test data to wide format.")

    mmScaler = preprocessing.MinMaxScaler()
    # Trains on training data only
    scaled_train_data = mmScaler.fit_transform(train_data)

    scaled_data_logger.info(
        "MinMaxScaler fit on train_data and the " + "latter transformed."
    )

    scaled_train_data = pd.DataFrame(
        scaled_train_data, columns=train_data.columns, index=train_data.index
    )

    scaled_data_logger.info("Converted scaled train_data to pd.DataFrame.")

    # Only transforms test data but doesn't "learn" from it
    scaled_test_data = mmScaler.transform(test_data)
    scaled_test_data = pd.DataFrame(
        scaled_test_data, columns=test_data.columns, index=test_data.index
    )

    scaled_data_logger.info("Scaled test data with same train data scaler.")

    # Undo pivot
    scaled_train_data = scaled_train_data.reset_index().melt(id_vars=["ds"])
    scaled_train_data = scaled_train_data.rename(columns={"value": "y"})
    scaled_test_data = scaled_test_data.reset_index().melt(id_vars=["ds"])
    scaled_test_data = scaled_test_data.rename(columns={"value": "y"})

    scaled_data_logger.info("Reverted train and test data to long format.")

    return (scaled_train_data, scaled_test_data)


def split_train_test(df, test_split):
    """
    Splits a dataframe using the cutoff date method
    """
    stt_logger = logging.getLogger("hf.split_train_test")

    stt_logger.info("split_train_test called.")

    unique_dates = df["ds"].unique()
    test_length = int(test_split * len(unique_dates))

    cutoff_date = unique_dates[-test_length]
    stt_logger.info(f"Cutoff date: {cutoff_date}")

    train_data = df[df["ds"] < cutoff_date]
    test_data = df[df["ds"] >= cutoff_date]

    return (train_data, test_data)


def custom_interpolate(df):
    """
    Entity-wise interpolation. Replaces all-nan columns with series mean.
    """
    hf_logger = logging.getLogger("hf.custom_interpolate")

    hf_logger.info("Interpolating each series in the DataFrame.")

    # Pivots so that each column is an entity
    proc_df = df.pivot(index="ds", columns="unique_id", values="y")

    hf_logger.info("Pivot dataframe to have each entity as a column.")

    # Interpolates per entity
    proc_df_int = proc_df.interpolate(method="linear", limit_direction="both")

    random_number_gen = np.random.default_rng()

    # Gaussian noise to add to interpolated values
    values_to_add = pd.Series(
        np.absolute(random_number_gen.normal(size=proc_df.shape[0])) / 100000,
        index=proc_df.index,
    )

    proc_df_replace_nan = proc_df_int.add(values_to_add, axis=0)

    proc_df = proc_df.fillna(proc_df_replace_nan)

    hf_logger.info("Forward and backward filling performed.")

    # Calculate date-wise mean and replace any series which is all NaNs
    date_wise_data_mean = proc_df.mean(axis=1)

    for col in proc_df.columns:
        if proc_df[col].isna().all():
            proc_df[col] = date_wise_data_mean

    hf_logger.info("Replaced all-nan columns with date-wise mean.")

    # Melts back to original shape
    proc_df = proc_df.reset_index().melt(id_vars=["ds"])

    hf_logger.info("DataFrame reverted to original shape(long format).")

    # Reset the name
    proc_df = proc_df.rename(columns={"value": "y"})

    return proc_df


def winsorize_data(df, winsorization_limits, value_column="y"):
    """
    Apply winsorization to the target variable in a long-format DataFrame.
    
    Args:
        df: DataFrame in long format with 'unique_id', 'ds', and target column
        winsorization_limits: List [lower_percentile, upper_percentile] e.g. [1.0, 99.0]
        value_column: Name of the column to winsorize (default: 'y')
        
    Returns:
        DataFrame with winsorized values
        
    Logs:
        Original and winsorized value ranges for monitoring
    """
    if winsorization_limits is None:
        return df
    
    hf_logger = logging.getLogger("hf.winsorize_data")
    
    # Convert percentiles to winsorization limits 
    # For [1.0, 99.0] percentiles, we winsorize 1% from each tail -> (0.01, 0.01)
    lower_perc, upper_perc = winsorization_limits
    lower_limit = lower_perc / 100.0  # 1.0 -> 0.01
    upper_limit = (100.0 - upper_perc) / 100.0  # 99.0 -> 0.01
    
    # Store original statistics
    original_min = df[value_column].min()
    original_max = df[value_column].max()
    original_count = df[value_column].count()
    
    df_winsorized = df.copy()
    
    # Apply winsorization globally across all entities
    # This is more appropriate for financial data where extreme values are often data errors
    non_null_mask = df_winsorized[value_column].notna()
    if non_null_mask.sum() > 0:
        df_winsorized.loc[non_null_mask, value_column] = winsorize(
            df_winsorized.loc[non_null_mask, value_column], 
            limits=(lower_limit, upper_limit)
        )
    
    # Log winsorization statistics
    winsorized_min = df_winsorized[value_column].min()
    winsorized_max = df_winsorized[value_column].max()
    
    # Count how many values were changed
    values_changed = (df[value_column] != df_winsorized[value_column]).sum()
    
    hf_logger.info(
        f"Applied winsorization [{lower_perc}%, {upper_perc}%]: "
        f"range [{original_min:.4f}, {original_max:.4f}] -> [{winsorized_min:.4f}, {winsorized_max:.4f}], "
        f"{values_changed}/{original_count} values changed ({100*values_changed/original_count:.1f}%)"
    )
    
    return df_winsorized


def process_df(df, frequency, seasonality, test_split, winsorization=None):
    """
    This function performs the following:
        1. Fill in missing dates based on the frequency provided
        2. Applies winsorization if specified
        3. Handles 'seasonal' test_split
        4. Extends the DataFrame backwards if training data is small
        5. Splits DataFrame into train and test using cutoff date method
        6. Interpolates train data based on custom strategy
        7. Scales both train and test using Min-Max scaling
        8. Converts both to np.float32
        
    Args:
        df: Long-format DataFrame with 'unique_id', 'ds', 'y' columns
        frequency: Frequency string (e.g. 'ME', 'D', 'Q')  
        seasonality: Seasonal period length
        test_split: Float fraction or 'seasonal'
        winsorization: Optional list [lower_perc, upper_perc] for winsorization
    """
    hf_logger = logging.getLogger("hf.process_df")

    hf_logger.info("process_df called.")

    df["y"] = df["y"].astype(np.float32)

    df.loc[(df["y"] == float("inf")) | (df["y"] == float("-inf")), "y"] = np.nan

    # This only adds NaNs as values for missing dates.
    df = fill_gaps(df, freq=frequency, start="global", end="global")

    hf_logger.info("Missing dates added.")
    
    # Apply winsorization if specified
    if winsorization is not None:
        df = winsorize_data(df, winsorization)
        hf_logger.info("Applied winsorization to data.")

    unique_dates = df["ds"].unique()
    len_ud = len(unique_dates)

    if test_split == "seasonal":
        if seasonality < len_ud:
            test_split = float(seasonality / len_ud)
            hf_logger.info('Converted test_split from "seasonal" to ' + f"{test_split}")
        else:
            hf_logger.error(
                'test_split = "seasonal" is not applicable.'
                + "Series is shorter than seasonality."
            )
            raise ValueError("Series too short. Please select appropriate test split.")

    test_length = int(test_split * len_ud)
    train_data_len = len_ud - test_length

    if (train_data_len < 4 * seasonality) or (train_data_len < MIN_SERIES_LEN):
        hf_logger.info("Train series shorter than seasonality * 4.")
        df = extend_df(df, train_data_len, frequency, seasonality)

        unique_dates = df["ds"].unique()
        test_split = float(test_length / len(unique_dates))

    # Split using the cutoff-date method
    train_data, test_data = split_train_test(df, test_split)
    hf_logger.info("Split data into train and test.")

    # Interpolate in both directions and then fill all-nan entities with
    # date-wise means
    train_data = custom_interpolate(train_data)
    hf_logger.info("Custom interpolation complete.")

    # MinMax Scaling
    train_data, test_data = scaled_data(train_data, test_data)
    hf_logger.info("Performed scaling on train and test.")

    train_data["y"] = train_data["y"].astype(np.float32)
    test_data["y"] = test_data["y"].astype(np.float32)
    hf_logger.info("Converted train and test to np.float32.")

    # The train series should now have all defined entries
    # The test series doesn't have any synthetic data

    train_data.reset_index(drop=True, inplace=True)
    test_data.reset_index(drop=True, inplace=True)

    hf_logger.info("Pre-processing complete.")

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
        except Exception as ex:
            print_sep()
            print(
                f"\nError in {f.__name__}. Please check logs. "
                + "There is a possibility that this error is insignificant "
                + "and can be ignored."
            )
            traceback.print_exception(ex)
            hf_logger.exception(f"Error in {f.__name__}.")
            print_sep()
            return None

    return error_catcher
