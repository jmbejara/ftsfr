# tests/test_save_models.py

import pytest
import datetime
from app import db
from app.models import SeriesGroup, TimeSeriesType, TimeSeries, DataPoint


def test_save_seriesgroup(app):
    """
    Test saving a standalone SeriesGroup to the database using the `save` method.
    """
    seriesgroup = SeriesGroup(name="SG1", description="Test SeriesGroup", code="SG001")
    seriesgroup.save()  # or db.session.add(seriesgroup); db.session.commit()

    assert (
        seriesgroup.id is not None
    ), "SeriesGroup ID should be generated after saving."
    assert (
        SeriesGroup.query.count() == 1
    ), "Exactly one SeriesGroup should exist in the database."

    retrieved = SeriesGroup.query.first()
    assert retrieved.name == "SG1", "Retrieved SeriesGroup name should match 'SG1'."
    assert (
        retrieved.description == "Test SeriesGroup"
    ), "SeriesGroup description should match."
    assert (
        retrieved.series_group_code == "SG001"
    ), "SeriesGroup series_group_code should match 'SG001'."


def test_save_time_series_type(app):
    """
    Test saving a TimeSeriesType to the database using the `save` method.
    """
    tst = TimeSeriesType(name="Price", description="Price Time Series")
    tst.save()

    assert tst.id is not None, "TimeSeriesType ID should be set after saving."
    assert TimeSeriesType.query.count() == 1, "Exactly one TimeSeriesType should exist."

    retrieved = TimeSeriesType.query.first()
    assert retrieved.name == "Price", "Retrieved name should be 'Price'."
    assert (
        retrieved.description == "Price Time Series"
    ), "TimeSeriesType description mismatch."


def test_save_time_series_with_dependencies(app):
    """
    Test saving a TimeSeries that depends on a SeriesGroup and a TimeSeriesType.
    Verifies the parent objects can be saved together if they're new.
    """
    seriesgroup = SeriesGroup(
        name="SG2", description="Second SeriesGroup", series_group_code="SG002"
    )
    tstype = TimeSeriesType(name="Volume", description="Volume Time Series")

    ts = TimeSeries(
        name="TS-Test",
        time_series_type=tstype,  # Correct: Assign the object, not the ID
        code="TST",
    )
    ts.series_groups.append(seriesgroup)

    ts.save()  # Should save ts, seriesgroup & tstype, too.

    # Verify TimeSeries
    assert ts.id is not None, "TimeSeries ID should be set after saving."
    assert TimeSeries.query.count() == 1, "One TimeSeries should exist."

    # Verify SeriesGroup
    assert (
        seriesgroup.id is not None
    ), "SeriesGroup ID should be set after saving TimeSeries."
    assert SeriesGroup.query.count() == 1, "One SeriesGroup should exist."

    # Verify TimeSeriesType
    assert (
        tstype.id is not None
    ), "TimeSeriesType ID should be set after saving TimeSeries."
    assert TimeSeriesType.query.count() == 1, "One TimeSeriesType should exist."

    # Additionally, check that the association is correct
    retrieved_ts = TimeSeries.query.first()
    associated_sgs = retrieved_ts.series_groups.all()
    assert (
        len(associated_sgs) == 1
    ), "TimeSeries should be associated with one SeriesGroup."
    assert (
        associated_sgs[0].id == seriesgroup.id
    ), "Associated SeriesGroup should match the created one."


def test_save_data_points_with_timeseries(app):
    """
    Test saving a TimeSeries along with multiple DataPoints.
    Ensures child DataPoints are also saved.
    """
    seriesgroup = SeriesGroup(
        name="SG3", description="Third SeriesGroup", series_group_code="SG003"
    )
    tstype = TimeSeriesType(name="Price", description="Price Time Series")

    ts = TimeSeries(
        name="TS-DataPoints", time_series_type=tstype, code="109"
    )  # Correct assignment
    ts.series_groups.append(seriesgroup)

    dp1 = DataPoint(date=datetime.date(2025, 1, 10), value=4000.0)
    dp2 = DataPoint(date=datetime.date(2025, 1, 11), value=4050.5)
    ts.data_points.extend([dp1, dp2])

    ts.save()  # Should save ts, seriesgroup, tstype, and dp1/dp2

    # Verify
    assert TimeSeries.query.count() == 1, "One TimeSeries should be saved."
    assert DataPoint.query.count() == 2, "Two DataPoints should be saved."

    retrieved_ts = TimeSeries.query.first()
    assert (
        len(retrieved_ts.data_points) == 2
    ), "Retrieved TimeSeries should have 2 DataPoints."

    # Verify SeriesGroup association
    associated_sgs = retrieved_ts.series_groups.all()
    assert (
        len(associated_sgs) == 1
    ), "TimeSeries should be associated with one SeriesGroup."
    assert (
        associated_sgs[0].id == seriesgroup.id
    ), "Associated SeriesGroup should match the created one."


def test_save_datapoint_alone_with_parents(app):
    """
    Test saving a single DataPoint that has a reference to a new TimeSeries,
    which references a new SeriesGroup and TimeSeriesType. All should be saved.
    """
    seriesgroup = SeriesGroup(
        name="SG4", description="Fourth SeriesGroup", series_group_code="SG004"
    )
    tstype = TimeSeriesType(name="Bids", description="Bid Time Series")
    ts = TimeSeries(
        name="TS-Bids", time_series_type=tstype, code="1291"
    )  # Correct assignment
    ts.series_groups.append(seriesgroup)

    dp = DataPoint(date=datetime.date(2025, 1, 12), value=5001.5, time_series=ts)
    dp.save()  # Should cascade and save dp, ts, seriesgroup, tstype

    assert dp.id is not None, "DataPoint should have an ID after saving."
    assert seriesgroup.id is not None, "SeriesGroup should be saved."
    assert tstype.id is not None, "TimeSeriesType should be saved."
    assert ts.id is not None, "TimeSeries should be saved."

    # Verify counts
    assert SeriesGroup.query.count() == 1, "Exactly one SeriesGroup should be in DB."
    assert (
        TimeSeriesType.query.count() == 1
    ), "Exactly one TimeSeriesType should be in DB."
    assert TimeSeries.query.count() == 1, "Exactly one TimeSeries should be in DB."
    assert DataPoint.query.count() == 1, "Exactly one DataPoint should be in DB."

    # Optionally, verify the association
    retrieved_ts = TimeSeries.query.first()
    associated_sgs = retrieved_ts.series_groups.all()
    assert (
        len(associated_sgs) == 1
    ), "TimeSeries should be associated with one SeriesGroup."
    assert (
        associated_sgs[0].id == seriesgroup.id
    ), "Associated SeriesGroup should match the created one."


def test_save_multiple_objects_in_one_session(app):
    """
    Test saving multiple objects in one transaction without committing until the end.
    """
    seriesgroup = SeriesGroup(
        name="SG5", description="Fifth SeriesGroup", series_group_code="SG005"
    )
    tstype = TimeSeriesType(name="Spread", description="Spread Time Series")
    ts = TimeSeries(
        name="TS-Spread", time_series_type=tstype, code="183"
    )  # Correct assignment
    ts.series_groups.append(seriesgroup)
    dp = DataPoint(date=datetime.date(2025, 1, 13), value=3999.9, time_series=ts)

    # Manually pass commit=False to gather them in the session, then commit once
    seriesgroup.save(commit=False)
    tstype.save(commit=False)
    ts.save(commit=False)
    dp.save(commit=False)

    # Now commit explicitly
    db.session.commit()

    # Verify
    assert SeriesGroup.query.count() == 1, "Exactly one SeriesGroup should be saved."
    assert (
        TimeSeriesType.query.count() == 1
    ), "Exactly one TimeSeriesType should be saved."
    assert TimeSeries.query.count() == 1, "Exactly one TimeSeries should be saved."
    assert DataPoint.query.count() == 1, "Exactly one DataPoint should be saved."

    retrieved_dp = DataPoint.query.first()
    assert retrieved_dp.value == 3999.9, "DataPoint value should be as assigned."
    assert (
        retrieved_dp.time_series.name == "TS-Spread"
    ), "DataPoint should link to the correct TimeSeries."
