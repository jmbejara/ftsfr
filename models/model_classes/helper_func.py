"""
Helper functions for multiple independent classes.
"""
from darts import TimeSeries
from darts.metrics import mase

def calculate_darts_MASE(test_series, train_series, pred_series, 
                         seasonality, value_column = "y"):
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