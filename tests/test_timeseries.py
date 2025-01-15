# tests/test_timeseries.py

import random
import string
import pytest
import datetime
import pandas as pd
from app.models import TimeSeries, DataPoint, SeriesGroup, TimeSeriesType
from app import db  # Import db for database operations


def test_from_dataframe_single_column(
    app, sample_df_single_column, create_seriesgroup_and_type  # Updated fixture name
):
    """
    Test that from_dataframe handles a single-column DataFrame and returns one TimeSeries.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    with app.app_context():
        ts_obj = TimeSeries.from_dataframe(
            df=sample_df_single_column,
            code="AAPL",  # Add a code for the TimeSeries
            series_groups=[seriesgroup],  # Pass as a list of objects
            time_series_type=tstype,  # Assign the object directly
        )

        # Expect a single TimeSeries (not a list)
        assert isinstance(
            ts_obj, TimeSeries
        ), "Should return a single TimeSeries object."
        assert (
            ts_obj.name == "price"
        ), "TimeSeries name should match the DataFrame column name."
        assert len(ts_obj.data_points) == 252, "TimeSeries should have 252 DataPoints."

        # Check the data points
        for i, dp in enumerate(ts_obj.data_points):
            expected_date = sample_df_single_column.index[i].date()
            expected_value = sample_df_single_column["price"].iloc[i]
            assert (
                dp.date.date() == expected_date
            ), f"Expected date {expected_date}, got {dp.date}"
            assert (
                dp.value == expected_value
            ), f"Expected value {expected_value}, got {dp.value}"


def test_from_dataframe_single_column_with_seriesgroup_and_tstype(
    app, sample_df_single_column, create_seriesgroup_and_type  # Updated fixture name
):
    """
    Test that from_dataframe handles a single-column DataFrame and returns one TimeSeries.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    with app.app_context():
        ts_obj = TimeSeries.from_dataframe(
            df=sample_df_single_column,
            code="AAPL",
            series_groups=[seriesgroup],  # Pass as a list of objects
            time_series_type=tstype,  # Assign the object directly
        )

        # Expect a single TimeSeries (not a list)
        assert isinstance(
            ts_obj, TimeSeries
        ), "Should return a single TimeSeries object."
        assert (
            ts_obj.name == "price"
        ), "TimeSeries name should match the DataFrame column name."
        assert len(ts_obj.data_points) == 252, "TimeSeries should have 252 DataPoints."

        # Check the data points
        for i, dp in enumerate(ts_obj.data_points):
            expected_date = sample_df_single_column.index[i].date()
            expected_value = sample_df_single_column["price"].iloc[i]
            assert (
                dp.date.date() == expected_date
            ), f"Expected date {expected_date}, got {dp.date}"
            assert (
                dp.value == expected_value
            ), f"Expected value {expected_value}, got {dp.value}"


def test_from_dataframe_single_column_with_date_as_column(
    app, sample_df_single_column, create_seriesgroup_and_type  # Updated fixture name
):
    """
    Test that from_dataframe handles a single-column DataFrame and returns one TimeSeries with a specified date column.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    sample_df = sample_df_single_column.copy()
    sample_df["Datetime"] = sample_df.index
    sample_df = sample_df.reset_index(drop=True)

    with app.app_context():
        ts_obj = TimeSeries.from_dataframe(
            df=sample_df,
            series_groups=[seriesgroup],  # Pass as a list of objects
            time_series_type=tstype,  # Assign the object directly
            code="AAPL",
            date_column="Datetime",
        )

        # Expect a single TimeSeries (not a list)
        assert isinstance(
            ts_obj, TimeSeries
        ), "Should return a single TimeSeries object."
        assert (
            ts_obj.name == "price"
        ), "TimeSeries name should match the DataFrame column name."
        assert len(ts_obj.data_points) == 252, "TimeSeries should have 252 DataPoints."

        # Check the data points
        for i, dp in enumerate(ts_obj.data_points):
            expected_date = sample_df["Datetime"][i].date()
            expected_value = sample_df["price"].iloc[i]
            assert (
                dp.date.date() == expected_date
            ), f"Expected date {expected_date}, got {dp.date}"
            assert (
                dp.value == expected_value
            ), f"Expected value {expected_value}, got {dp.value}"


def test_from_dataframe_multi_column(
    app, sample_df_multiple_columns, create_seriesgroup_and_type  # Updated fixture name
):
    """
    Test that from_dataframe handles a multi-column DataFrame and returns multiple TimeSeries.
    """
    seriesgroup, tstype = create_seriesgroup_and_type
    num_columns = len(sample_df_multiple_columns.columns)

    with app.app_context():
        # Since there are multiple columns, provide a list of SeriesGroup objects
        # For simplicity, using the same SeriesGroup for all columns
        series_groups = [seriesgroup for _ in range(num_columns)]
        codes = [
            "".join(random.choices(string.ascii_uppercase, k=3))
            for _ in range(num_columns)
        ]

        ts_objs = TimeSeries.from_dataframe(
            df=sample_df_multiple_columns,
            series_groups=series_groups,  # Pass as a list of objects
            time_series_type=tstype,  # Assign the object directly
            code=codes,  # Add a code for all TimeSeries
        )

        # Expect a list of TimeSeries objects
        assert isinstance(ts_objs, list), "Should return a list of TimeSeries objects."
        assert len(ts_objs) == num_columns, "Should return one TimeSeries per column."
        assert all(
            isinstance(ts, TimeSeries) for ts in ts_objs
        ), "All elements should be TimeSeries objects."
        assert (
            ts_objs[0].name == "price"
        ), "First TimeSeries name should match the first DataFrame column name."


def test_to_dataframe_multi_column(
    app, sample_df_multiple_columns, create_seriesgroup_and_type  # Updated fixture name
):
    """
    Test that from_dataframe handles a multi-column DataFrame and the resulting TimeSeries can be converted back to DataFrame.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    with app.app_context():
        # Provide a list of SeriesGroup objects matching the number of columns
        num_columns = len(sample_df_multiple_columns.columns)
        series_groups = [seriesgroup for _ in range(num_columns)]
        codes = [
            "".join(random.choices(string.ascii_uppercase, k=3))
            for _ in range(num_columns)
        ]

        ts_objs = TimeSeries.from_dataframe(
            df=sample_df_multiple_columns,
            series_groups=series_groups,  # Pass as a list of objects
            time_series_type=tstype,  # Assign the object directly
            code=codes,  # Add a code for all TimeSeries
        )
        for ts_obj in ts_objs:
            ts_dataframe = ts_obj.to_dataframe()
            assert isinstance(ts_dataframe, pd.DataFrame), "Should return a DataFrame."
            assert len(ts_dataframe.index) == len(
                sample_df_multiple_columns.index
            ), "DataFrame index length should match input length."


def test_to_dataframe_single_column(
    app, sample_df_single_column, create_seriesgroup_and_type  # Updated fixture name
):
    """
    Test that from_dataframe handles a single-column DataFrame and returns one TimeSeries, which can be converted back to DataFrame.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    with app.app_context():
        ts_obj = TimeSeries.from_dataframe(
            df=sample_df_single_column,
            series_groups=[seriesgroup],  # Pass as a list of objects
            time_series_type=tstype,  # Assign the object directly
            code="AAPL",
        )

        ts_dataframe = ts_obj.to_dataframe()
        assert isinstance(ts_dataframe, pd.DataFrame), "Should return a DataFrame."
        assert len(ts_dataframe.index) == len(
            sample_df_single_column.index
        ), "DataFrame index length should match input length."
        assert list(ts_dataframe.columns) == [
            "price"
        ], "DataFrame columns should match the input DataFrame."
        for i in range(5):
            assert (
                ts_dataframe.iloc[i, 0] == sample_df_single_column.iloc[i, 0]
            ), "DataFrame values should match the input DataFrame."
