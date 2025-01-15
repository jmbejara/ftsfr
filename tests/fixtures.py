# tests/fixtures.py

import pytest
import random
import string
from app.models import SeriesGroup, TimeSeriesType, TimeSeries, DataPoint
import datetime
import pandas as pd
from app import db
import numpy as np


@pytest.fixture
def create_seriesgroup_and_type(app):
    """
    Fixture to create a SeriesGroup and a TimeSeriesType.
    Returns the objects themselves.
    """
    seriesgroup = SeriesGroup(
        name="SG_Test", description="Test SeriesGroup", series_group_code="SG999"
    )
    tstype = TimeSeriesType(name="TestType", description="Test TimeSeriesType")
    db.session.add_all([seriesgroup, tstype])
    db.session.commit()
    return seriesgroup, tstype


@pytest.fixture
def populate_test_db(app):
    """
    Fixture to populate the test database with initial data.
    Accepts parameters for the number of series groups and data points per time series.
    """

    def _populate_test_db(
        num_seriesgroups=3, num_data_points=5, start_date=datetime.date(2024, 1, 1)
    ):
        """
        Internal function to populate the test database.

        Args:
            num_seriesgroups (int): Number of SeriesGroups to create.
            num_data_points (int): Number of data points per time series.
            start_date (date or str): Start date for generating data points.
        """

        # Convert `start_date` to a `datetime.date` object if it's a string
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

        def generate_random_name(length=3):
            """Generate a random name with the specified length."""
            return "".join(random.choices(string.ascii_uppercase, k=length))

        def create_data_points(time_series_id, num_points, start_date):
            """Create random data points for a given time series."""
            data_points = []
            for i in range(num_points):
                date = start_date + datetime.timedelta(days=i)
                value = round(
                    random.uniform(1000.0, 5000.0), 2
                )  # Random value between 1000 and 5000

                # Randomly decide whether to assign a `date_release` or leave it as None
                if random.choice([True, False]):
                    date_release = date + datetime.timedelta(days=1)
                else:
                    date_release = None

                data_point = DataPoint(
                    date=date,
                    value=value,
                    date_release=date_release,
                    time_series_id=time_series_id,
                )
                data_points.append(data_point)
            return data_points

        with app.app_context():
            # Set a fixed random seed for reproducibility
            random.seed(42)

            # Create a TimeSeriesType
            time_series_type = TimeSeriesType(
                name="Price", description="Price Time Series"
            )
            db.session.add(time_series_type)
            db.session.commit()

            # Generate the specified number of SeriesGroups and time series
            for _ in range(num_seriesgroups):
                # Create a random SeriesGroup
                seriesgroup_name = generate_random_name()
                series_group_code = "".join(
                    random.choices(string.ascii_uppercase + string.digits, k=5)
                )
                seriesgroup = SeriesGroup(
                    name=seriesgroup_name,
                    description=f"{seriesgroup_name} Description",
                    series_group_code=series_group_code,
                )
                db.session.add(seriesgroup)
                db.session.commit()

                # Create a random TimeSeries for the SeriesGroup
                time_series_name = generate_random_name()
                time_series = TimeSeries(
                    name=f"{seriesgroup_name} {time_series_name}",
                    type_id=time_series_type.id,
                    delta_type="pct",  # Assuming default or desired value
                    code=series_group_code + time_series_name[0].upper(),
                )
                db.session.add(time_series)
                db.session.commit()

                # Associate TimeSeries with SeriesGroup
                seriesgroup.series.append(time_series)
                db.session.commit()

                # Create random data points for the time series
                data_points = create_data_points(
                    time_series.id, num_data_points, start_date
                )
                db.session.add_all(data_points)
                db.session.commit()

    return _populate_test_db


@pytest.fixture
def sample_df_single_column():
    """
    Returns a single-column DataFrame (with a DateTimeIndex).
    """
    rng = np.random.default_rng(seed=42)
    returns = rng.normal(0.0001, 0.01, 252)
    prices = 100 * (1 + np.cumsum(returns))
    dates = pd.date_range("2025-01-01", periods=252, freq="D")
    return pd.DataFrame({"price": prices}, index=dates)


@pytest.fixture
def sample_df_multiple_columns():
    """
    Returns a multi-column DataFrame (with a DateTimeIndex).
    """
    rng = np.random.default_rng(seed=42)
    returns = rng.normal(0.0001, 0.01, 252)
    prices = 100 * (1 + np.cumsum(returns))
    volumes = rng.integers(1000, 10000, 252)
    dates = pd.date_range("2025-01-01", periods=252, freq="D")
    return pd.DataFrame({"price": prices, "volume": volumes}, index=dates)


@pytest.fixture
def basic_tstype(app):
    """
    Fixture to create a basic TimeSeriesType for testing.
    """
    with app.app_context():
        tstype = TimeSeriesType(
            name="BasicType", description="A basic time series type for testing."
        )
        db.session.add(tstype)
        db.session.commit()
    return tstype
