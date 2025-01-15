# tests/test_timeseries_saving.py

import pytest
import datetime
from sqlalchemy.exc import IntegrityError
from app.models import TimeSeries, DataPoint, Keyword, TimeSeriesType, SeriesGroup
from app import db


@pytest.fixture
def basic_tstype(app, request):
    with app.app_context():
        tstype = TimeSeriesType(
            name="BasicType", description="A basic time series type for testing."
        )
        db.session.add(tstype)
        db.session.commit()

    # Just remove the teardown code. The db.drop_all() in app fixture is enough.
    # request.addfinalizer(teardown)

    return tstype


@pytest.fixture
def create_timeseries(app, basic_tstype):
    """
    Creates and returns a TimeSeries with no DataPoints,
    so that we can test adding DataPoints separately.
    """
    ts = TimeSeries(name="TS_Basic", time_series_type=basic_tstype, code="TS001")
    ts.save()
    return ts


def test_create_unique_timeseries(app, basic_tstype):
    """
    Test creating a brand-new TimeSeries with a unique code and name.
    """
    with app.app_context():
        ts = TimeSeries(name="TS_Unique", time_series_type=basic_tstype, code="UNIQ001")
        ts.save()
        assert ts.id is not None, "TimeSeries ID should be set after saving."
        assert (
            TimeSeries.query.count() == 1
        ), "Exactly one TimeSeries should exist in the database."

        # Ensure no conflicts
        retrieved_ts = TimeSeries.query.first()
        assert retrieved_ts.name == "TS_Unique"
        assert retrieved_ts.time_series_code == "UNIQ001"


def test_timeseries_conflict_no_allow_update_same_name(app, basic_tstype):
    """
    Test that creating a TimeSeries with a duplicate name fails when allow_update=False.
    """
    with app.app_context():
        existing_ts = TimeSeries(
            name="TS_Conflict", time_series_type=basic_tstype, code="CONF001"
        )
        existing_ts.save()

        ts_conflict = TimeSeries(
            name="TS_Conflict", time_series_type=basic_tstype, code="NEWCODE"
        )
        with pytest.raises(ValueError) as exc_info:
            ts_conflict.save(allow_update=False)

        assert "TimeSeries with the same name" in str(
            exc_info.value
        ), "Should raise ValueError about duplicate name."


def test_timeseries_conflict_no_allow_update_same_code(app, basic_tstype):
    """
    Test that creating a TimeSeries with a duplicate code fails when allow_update=False.
    """
    with app.app_context():
        existing_ts = TimeSeries(
            name="TS_Other", time_series_type=basic_tstype, code="DUPLICATE"
        )
        existing_ts.save()

        ts_conflict = TimeSeries(
            name="TS_NewName", time_series_type=basic_tstype, code="DUPLICATE"
        )
        with pytest.raises(ValueError) as exc_info:
            ts_conflict.save(allow_update=False)

        assert "TimeSeries with the same code" in str(
            exc_info.value
        ), "Should raise ValueError about duplicate code."


def test_timeseries_conflict_with_allow_update_same_name(app, basic_tstype):
    """
    Test that creating a TimeSeries with a duplicate name merges with existing one if allow_update=True.
    """
    with app.app_context():
        existing_ts = TimeSeries(
            name="TS_Merge", time_series_type=basic_tstype, code="MERGE001"
        )
        existing_ts.description = "Original description"
        existing_ts.save()

        # Create a new one with the same name, different code
        ts_merge = TimeSeries(
            name="TS_Merge", time_series_type=basic_tstype, code="MERGEXXX"
        )
        ts_merge.description = "New description"
        ts_merge.save(
            allow_update=True, keep_old_description=False
        )  # We do NOT keep the old description

        # The existing record's ID should be reused
        assert ts_merge.id == existing_ts.id, "Should merge with the existing record."
        assert (
            ts_merge.description == "New description"
        ), "Should replace the old description."

        # Only one time series in the DB
        assert TimeSeries.query.count() == 1, "Merging should not create a new record."


def test_timeseries_conflict_with_allow_update_same_code(app, basic_tstype):
    """
    Test that creating a TimeSeries with a duplicate code merges with existing one if allow_update=True.
    """
    with app.app_context():
        existing_ts = TimeSeries(
            name="TS_MergeCode", time_series_type=basic_tstype, code="CODE001"
        )
        existing_ts.delta_type = "pct"
        existing_ts.save()

        # Create a new one with a different name, same code
        ts_merge_code = TimeSeries(
            name="TS_NewName", time_series_type=basic_tstype, code="CODE001"
        )
        ts_merge_code.delta_type = "abs"
        ts_merge_code.save(
            allow_update=True, keep_old_delta_type=False
        )  # We do NOT keep the old delta_type

        # The existing record's ID should be reused
        assert (
            ts_merge_code.id == existing_ts.id
        ), "Should merge with the existing record."
        assert ts_merge_code.delta_type == "abs", "Should replace the old delta_type."

        # Only one time series in the DB
        assert TimeSeries.query.count() == 1, "Merging should not create a new record."


def test_timeseries_integrity_error(app, basic_tstype):
    """
    Test that an IntegrityError is raised if something else
    (e.g., a unique constraint or a DB-level issue) fails.
    """
    with app.app_context():
        ts = TimeSeries(
            name="TS_Integrity", time_series_type=basic_tstype, code="INTG001"
        )
        ts.save()
        # Trying to create another with the exact same name and code,
        # but we do not set allow_update (should default to True).
        # Because it's the same name & code, the logic merges.
        # However, let's intentionally cause an IntegrityError by messing
        # with something in the session if possible.

        # The simplest way: Another "TimeSeries" object with the same code but
        # name also the same, which triggers ValueError first, not IntegrityError.
        # Instead let's create a conflict on the DB side:
        try:
            duplicate_ts = TimeSeries(
                name="TS_Integrity", time_series_type=basic_tstype, code="INTG001"
            )
            # Force a direct DB insertion ignoring the time_series logic
            db.session.add(duplicate_ts)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  # expected

        assert (
            TimeSeries.query.count() == 1
        ), "There should still be only one TimeSeries in the DB."


def test_join_data_points_no_duplicates(app, create_timeseries):
    """
    Test join_data_points ensures no duplicate DataPoints based on (date, value).
    """
    ts = create_timeseries  # Already saved with code="TS001"

    dp1 = DataPoint(date=datetime.date(2025, 5, 5), value=100.0)
    dp2 = DataPoint(
        date=datetime.date(2025, 5, 5), value=100.0
    )  # duplicate date & value
    dp3 = DataPoint(
        date=datetime.date(2025, 5, 6), value=100.0
    )  # same value, different date
    dp4 = DataPoint(
        date=datetime.date(2025, 5, 6), value=200.0
    )  # same date, different value

    ts.join_data_points([dp1, dp2, dp3, dp4])
    ts.save()

    # We should have 3 unique DataPoints:
    # (2025-05-05, 100.0), (2025-05-06, 100.0), (2025-05-06, 200.0)
    all_dp = DataPoint.query.filter_by(time_series_id=ts.id).all()
    assert len(all_dp) == 3, "Should only add 3 unique (date, value) pairs."
    dates_values = sorted([(dp.date, dp.value) for dp in all_dp])
    assert dates_values == [
        (datetime.date(2025, 5, 5), 100.0),
        (datetime.date(2025, 5, 6), 100.0),
        (datetime.date(2025, 5, 6), 200.0),
    ]


def test_join_keywords_no_duplicates(app, create_timeseries):
    """
    Test join_keywords ensures no duplicate Keywords.
    """
    ts = create_timeseries  # name="TS_Basic", code="TS001"

    # Suppose we add these new keywords
    ts.join_keywords(["Finance", "Finance", "Investment"])
    ts.save()

    # We expect only two distinct keywords
    all_kws = [kw.word for kw in ts.keywords]
    assert len(all_kws) == 2, "Should only add distinct keywords."
    assert set(all_kws) == {"Finance", "Investment"}

    # Attempt to add the same keywords again
    ts.join_keywords(["Finance"])
    ts.save()

    # Should not have changed the total count
    all_kws_again = [kw.word for kw in ts.keywords]
    assert len(all_kws_again) == 2, "No new duplicates should be added."


def test_merge_existing_data_points_on_update(app, basic_tstype):
    """
    Test that data points from the old TimeSeries are merged if join_data_points=True
    on update, and no duplicates are introduced.
    """
    with app.app_context():
        old_ts = TimeSeries(
            name="TS_MergeDP", time_series_type=basic_tstype, code="MERGEDP"
        )
        old_ts.save()
        # Add data points to the old TimeSeries
        dp1 = DataPoint(date=datetime.date(2025, 1, 1), value=50.0, time_series=old_ts)
        dp2 = DataPoint(date=datetime.date(2025, 1, 2), value=60.0, time_series=old_ts)
        db.session.add_all([dp1, dp2])
        db.session.commit()

        # Create new TimeSeries with the same name or code, so it merges
        new_ts = TimeSeries(
            name="TS_MergeDP", time_series_type=basic_tstype, code="NEWMERGE"
        )
        dp3 = DataPoint(date=datetime.date(2025, 1, 2), value=60.0)  # duplicate
        dp4 = DataPoint(date=datetime.date(2025, 1, 3), value=70.0)  # unique
        new_ts.join_data_points([dp3, dp4])
        new_ts.save(allow_update=True, join_data_points=True)

        # Should have replaced the old TimeSeries but kept the old dp1, dp2
        assert new_ts.id == old_ts.id, "Should merge with the existing record."

        # Check that we have exactly 3 unique points
        all_dp = DataPoint.query.filter_by(time_series_id=new_ts.id).all()
        assert len(all_dp) == 3, "Should keep old DPs and add new unique DP."
        date_val_set = {(dp.date, dp.value) for dp in all_dp}
        expected_set = {
            (datetime.date(2025, 1, 1), 50.0),
            (datetime.date(2025, 1, 2), 60.0),
            (datetime.date(2025, 1, 3), 70.0),
        }
        assert (
            date_val_set == expected_set
        ), "Merged set of DataPoints should match expected."
