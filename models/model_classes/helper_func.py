"""
Helper functions for multiple independent classes.
"""

from pandas.tseries.frequencies import to_offset
import traceback
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


def calculate_darts_MASE(
    test_series, train_series, pred_series, seasonality, value_column="y"
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
        test_series = (
            test_series.pivot(index="ds", columns="unique_id", values="y")
            .reset_index()
            .rename_axis(None, axis=1)
        )
        train_series = (
            train_series.pivot(index="ds", columns="unique_id", values="y")
            .reset_index()
            .rename_axis(None, axis=1)
        )

        pred_series = (
            pred_series.pivot(index="ds", columns="unique_id", values=value_column)
            .reset_index()
            .rename_axis(None, axis=1)
        )

        hf_logger.info(
            "Converted train, test, and pred series into"
            + " darts TimeSeries compatible format."
        )

        # Try to convert to TimeSeries with frequency inference
        try:
            test_series = TimeSeries.from_dataframe(
                test_series, time_col="ds", fill_missing_dates=True, freq=None
            )
            train_series = TimeSeries.from_dataframe(
                train_series, time_col="ds", fill_missing_dates=True, freq=None
            )
            pred_series = TimeSeries.from_dataframe(
                pred_series, time_col="ds", fill_missing_dates=True, freq=None
            )
        except ValueError:
            # Fallback to simple conversion without frequency inference
            hf_logger.warning("Frequency inference failed, using simple conversion")
            test_series = TimeSeries.from_dataframe(
                test_series, time_col="ds", fill_missing_dates=False
            )
            train_series = TimeSeries.from_dataframe(
                train_series, time_col="ds", fill_missing_dates=False
            )
            pred_series = TimeSeries.from_dataframe(
                pred_series, time_col="ds", fill_missing_dates=False
            )

        hf_logger.info("Converted all three series into TimeSeries objects.")

        return mase(test_series, pred_series, train_series, seasonality)

    except Exception as e:
        hf_logger.error(f"Error in MASE calculation: {e}")
        raise e


def extend_df(df, train_series_len, frequency, seasonality, interpolate=True):
    """
    Extends a df to fit seasonality * 4 lags. Doesn't interpolate, but
    adds np.nan as values in the extend rows.
    """
    hf_logger = logging.getLogger("hf.extend_df")

    difference = 4 * seasonality - train_series_len
    new_date = df["ds"].min()
    date_offset = difference * to_offset(frequency)
    new_date -= date_offset

    hf_logger.info(new_date.strftime("%Y-%m-%d, %r") + " is the" + " new start date")

    df = fill_gaps(df, freq=frequency, start=new_date, end="global")

    hf_logger.info("DataFrame extended to fit 4 * seasonality window.")

    return df


def process_df(df, frequency, seasonality, test_split):
    """
    Fills missing dates as per frequency. Extends if train_series is less than
    4 * seasonality.
    """
    hf_logger = logging.getLogger("hf.process_df")

    hf_logger.info("Filling missing dates and extending if needed.")

    df = fill_gaps(df, freq=frequency, start="global", end="global")

    hf_logger.info("Missing dates added.")

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
            raise ValueError(
                "Series too short. " + "Please select appropriate test split."
            )

    test_length = int(test_split * len_ud)
    train_series_len = len_ud - test_length

    if train_series_len < 4 * seasonality:
        hf_logger.info("Train series shorter than seasonality * 4.")
        df = extend_df(df, train_series_len, frequency, seasonality)

        unique_dates = df["ds"].unique()
        test_split = float(test_length / len(unique_dates))

    hf_logger.info("Processing complete.")

    return (df, test_split)


def custom_interpolate(df):
    """
    Entity-wise interpolation.
    """
    hf_logger = logging.getLogger("hf.custom_interpolate")

    hf_logger.info("Interpolating each series in the DataFrame.")

    # Pivots so that each column is an entity
    proc_df = df.pivot(index="ds", columns="unique_id", values="y")

    hf_logger.info("Pivot dataframe to have each entity as " + "a column(wide format).")
    # Interpolates per entity
    proc_df = proc_df.interpolate(limit_direction="both")

    hf_logger.info("Interpolated values in both directions.")

    # Melts back to original shape
    proc_df = proc_df.reset_index().melt(id_vars=["ds"])

    hf_logger.info("DataFrame reverted to original shape(long format).")

    # Reset the name
    proc_df = proc_df.rename(columns={"value": "y"})

    return proc_df


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
            print(traceback.format_exc())
            print(f"\nError in {f.__name__}." + " Full traceback above \u2191")
            hf_logger.exception(f"Error in {f.__name__}.")
            print_sep()
            return None

    return error_catcher
