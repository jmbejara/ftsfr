# tests/test_initial_database_population.py

import pytest
from app.models import SeriesGroup, TimeSeriesType, TimeSeries, DataPoint
import datetime


def test_initial_population(populate_test_db):
    """
    Test the initial population of the test database by verifying the created entries.
    """
    # Populate the database with 3 SeriesGroups and 5 data points per time series
    populate_test_db(num_seriesgroups=3, num_data_points=5, start_date="2024-01-01")

    # Verify the number of entries created
    assert SeriesGroup.query.count() == 3, "There should be exactly 3 SeriesGroups."
    assert (
        TimeSeriesType.query.count() == 1
    ), "There should be exactly one TimeSeriesType."
    assert TimeSeries.query.count() == 3, "There should be exactly three TimeSeries."
    assert DataPoint.query.count() == 15, "Each TimeSeries should have 5 DataPoints."

    # Retrieve and check the SeriesGroups
    for sg in SeriesGroup.query.all():
        assert (
            len(sg.name) == 3
        ), f"SeriesGroup name '{sg.name}' should have exactly three characters."
        assert sg.description.endswith(
            "Description"
        ), f"SeriesGroup description mismatch for '{sg.name}'."
        assert (
            sg.series_group_code is not None and len(sg.series_group_code) == 5
        ), f"SeriesGroup '{sg.name}' should have a valid series_group_code of length 5."

    # Retrieve and check the TimeSeriesType
    time_series_type = TimeSeriesType.query.first()
    assert time_series_type.name == "Price", "TimeSeriesType name should be 'Price'."
    assert (
        time_series_type.description == "Price Time Series"
    ), "TimeSeriesType description mismatch."

    # Retrieve and check the TimeSeries and their DataPoints
    for time_series in TimeSeries.query.all():
        assert len(time_series.name) > 0, "TimeSeries name should not be empty."
        assert (
            time_series.type_id == time_series_type.id
        ), "TimeSeries type_id mismatch."

        # Ensure each TimeSeries is associated with at least one SeriesGroup
        associated_sg_ids = [sg.id for sg in time_series.series_groups]
        assert (
            len(associated_sg_ids) >= 1
        ), f"TimeSeries '{time_series.name}' should be associated with at least one SeriesGroup."

        data_points = time_series.data_points
        assert (
            len(data_points) == 5
        ), f"TimeSeries '{time_series.name}' should have exactly 5 DataPoints."

        # Verify the DataPoints
        start_date = datetime.date(2024, 1, 1)
        for i, dp in enumerate(data_points):
            expected_date = start_date + datetime.timedelta(days=i)
            assert (
                dp.date == expected_date
            ), f"DataPoint date mismatch: expected {expected_date}, got {dp.date}."
            assert isinstance(dp.value, float), "DataPoint 'value' should be a float."
            assert (
                dp.time_series_id == time_series.id
            ), f"DataPoint time_series_id mismatch for DataPoint ID {dp.id}."

            # Check `date_release` conditionally
            if dp.date_release:
                expected_release_date = dp.date + datetime.timedelta(days=1)
                assert (
                    dp.date_release == expected_release_date
                ), f"DataPoint 'date_release' mismatch: expected {expected_release_date}, got {dp.date_release}."
