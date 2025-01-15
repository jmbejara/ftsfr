# tests/test_relationships.py

import pytest
import datetime
from app import db
from app.models import (
    SeriesGroup,
    TimeSeries,
    SeriesBase,
    TimeSeriesType,
    Keyword,
    DataPoint,
)


@pytest.fixture
def create_parent_child_seriesgroups(app):
    """
    Fixture to create a parent SeriesGroup with multiple child SeriesGroups.
    """
    parent = SeriesGroup(
        name="ParentSG", description="Parent SeriesGroup", series_group_code="PSG001"
    )
    child1 = SeriesGroup(
        name="ChildSG1",
        description="First Child SeriesGroup",
        series_group_code="CSG001",
        parent=parent,
    )
    child2 = SeriesGroup(
        name="ChildSG2",
        description="Second Child SeriesGroup",
        series_group_code="CSG002",
        parent=parent,
    )
    db.session.add_all([parent, child1, child2])
    db.session.commit()
    return parent, child1, child2


def test_seriesgroup_parent_child_relationship(app, create_parent_child_seriesgroups):
    """
    Test the self-referential parent-child relationship in SeriesGroup.
    """
    parent, child1, child2 = create_parent_child_seriesgroups

    # Verify parent has two children
    assert (
        len(parent.children.all()) == 2
    ), "Parent SeriesGroup should have two children."
    assert child1.parent == parent, "Child1's parent should be ParentSG."
    assert child2.parent == parent, "Child2's parent should be ParentSG."

    # Verify children are correctly linked
    assert child1 in parent.children.all(), "Child1 should be in ParentSG's children."
    assert child2 in parent.children.all(), "Child2 should be in ParentSG's children."


def test_polymorphic_querying(app):
    """
    Test that querying SeriesBase returns instances of the correct subclasses.
    """
    tstype = TimeSeriesType(
        name="Polymorphic", description="Polymorphic TimeSeriesType"
    )

    # Create a SeriesGroup
    sg = SeriesGroup(
        name="SG_Poly",
        description="Polymorphic SeriesGroup",
        series_group_code="SGP001",
    )
    db.session.add(sg)

    # Create a TimeSeries
    ts = TimeSeries(name="TS_Poly", time_series_type=tstype, code="TSP001")
    db.session.add(ts)

    db.session.commit()

    # Query SeriesBase
    all_seriesbase = SeriesBase.query.all()
    assert len(all_seriesbase) == 2, "There should be three SeriesBase instances."

    # Optionally, verify the types of each instance
    assert any(
        isinstance(sb, SeriesGroup) for sb in all_seriesbase
    ), "At least one SeriesGroup should be present."
    assert any(
        isinstance(sb, TimeSeries) for sb in all_seriesbase
    ), "At least one TimeSeries should be present."


def test_seriesgroup_seriesbase_association(app, create_seriesgroup_and_type):
    """
    Test the many-to-many relationship between SeriesGroup and SeriesBase.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    # Create additional SeriesBase instances
    ts1 = TimeSeries(name="TS_Assoc1", time_series_type=tstype, code="TSA001")
    ts2 = TimeSeries(name="TS_Assoc2", time_series_type=tstype, code="TSA002")
    db.session.add_all([ts1, ts2])
    db.session.commit()

    # Associate SeriesBase with SeriesGroup
    seriesgroup.series.append(ts1)
    seriesgroup.series.append(ts2)
    db.session.commit()

    # Verify associations
    assert (
        ts1 in seriesgroup.series.all()
    ), "TS_Assoc1 should be associated with SeriesGroup."
    assert (
        ts2 in seriesgroup.series.all()
    ), "TS_Assoc2 should be associated with SeriesGroup."
    assert (
        seriesgroup in ts1.series_groups.all()
    ), "SeriesGroup should be associated with TS_Assoc1."
    assert (
        seriesgroup in ts2.series_groups.all()
    ), "SeriesGroup should be associated with TS_Assoc2."


def test_keyword_uniqueness(app, create_seriesgroup_and_type):
    """
    Test that adding duplicate keywords raises an IntegrityError.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    # Add a keyword
    keyword = Keyword(word="Finance")
    db.session.add(keyword)
    db.session.commit()

    # Attempt to add the same keyword again
    duplicate_keyword = Keyword(word="Finance")
    db.session.add(duplicate_keyword)

    with pytest.raises(Exception) as exc_info:
        db.session.commit()

    db.session.rollback()
    assert "UNIQUE constraint failed" in str(
        exc_info.value
    ), "Adding duplicate keyword should fail due to unique constraint."


def test_seriesgroup_unique_code(app, create_seriesgroup_and_type):
    """
    Test that SeriesGroup's series_group_code is unique.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    # Create a SeriesGroup with a unique code
    sg_unique = SeriesGroup(
        name="UniqueSG",
        description="Unique Code SeriesGroup",
        series_group_code="USG001",
    )
    db.session.add(sg_unique)
    db.session.commit()

    # Attempt to create another SeriesGroup with the same code
    sg_duplicate = SeriesGroup(
        name="DuplicateSG",
        description="Duplicate Code SeriesGroup",
        series_group_code="USG001",
    )
    db.session.add(sg_duplicate)

    with pytest.raises(Exception) as exc_info:
        db.session.commit()

    db.session.rollback()
    assert "UNIQUE constraint failed" in str(
        exc_info.value
    ), "Adding SeriesGroup with duplicate code should fail due to unique constraint."


def test_time_series_unique_code(app, create_seriesgroup_and_type):
    """
    Test that TimeSeries's time_series_code is unique.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    # Create a TimeSeries with a unique code
    ts_unique = TimeSeries(name="UniqueTS", time_series_type=tstype, code="UTS001")
    db.session.add(ts_unique)
    db.session.commit()

    # Attempt to create another TimeSeries with the same code
    ts_duplicate = TimeSeries(
        name="DuplicateTS", time_series_type=tstype, code="UTS001"
    )
    db.session.add(ts_duplicate)

    with pytest.raises(Exception) as exc_info:
        db.session.commit()

    db.session.rollback()
    assert "UNIQUE constraint failed" in str(
        exc_info.value
    ), "Adding TimeSeries with duplicate code should fail due to unique constraint."


def test_seriesbase_deletion_cascade(app, create_seriesgroup_and_type):
    """
    Test that deleting a SeriesBase (TimeSeries) also deletes associated DataPoints if cascade is set.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    # Create a TimeSeries with DataPoints
    ts = TimeSeries(name="TS_DeleteCascade", time_series_type=tstype, code="TSC001")
    dp1 = DataPoint(date=datetime.date(2025, 1, 1), value=100.0, time_series=ts)
    dp2 = DataPoint(date=datetime.date(2025, 1, 2), value=110.0, time_series=ts)
    db.session.add_all([ts, dp1, dp2])
    db.session.commit()

    # Verify DataPoints exist
    assert (
        DataPoint.query.filter_by(time_series_id=ts.id).count() == 2
    ), "There should be two DataPoints associated with the TimeSeries."

    # Delete the TimeSeries
    db.session.delete(ts)
    db.session.commit()

    # Verify TimeSeries is deleted
    assert (
        TimeSeries.query.filter_by(id=ts.id).count() == 0
    ), "TimeSeries should be deleted."

    # Verify DataPoints are also deleted if cascade is set
    # Note: Ensure that cascade delete is configured in the relationship if expected
    assert (
        DataPoint.query.filter_by(time_series_id=ts.id).count() == 0
    ), "Associated DataPoints should be deleted with the TimeSeries."


def test_validate_code_len_decorator(app, create_seriesgroup_and_type):
    """
    Test that the validate_code_len decorator enforces code length constraints.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    # Attempt to create a SeriesGroup with a code exceeding CODE_MAX_LEN
    long_code = "A" * 13  # Assuming CODE_MAX_LEN is 12

    with pytest.raises(ValueError) as exc_info:
        sg = SeriesGroup(
            name="LongCodeSG",
            description="SeriesGroup with long code",
            series_group_code=long_code,
        )
        sg.save()

    db.session.rollback()
    assert "Code must be 12 characters or less." in str(
        exc_info.value
    ), "Code length validation should fail for codes longer than 12 characters."


def test_seriesgroup_nested_relationship(app, create_seriesgroup_and_type):
    """
    Test creating nested SeriesGroups (grandchildren).
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    # Create child SeriesGroups
    child1 = SeriesGroup(
        name="ChildSG1",
        description="First Child SeriesGroup",
        series_group_code="CSG001",
        parent=seriesgroup,
    )
    child2 = SeriesGroup(
        name="ChildSG2",
        description="Second Child SeriesGroup",
        series_group_code="CSG002",
        parent=seriesgroup,
    )
    db.session.add_all([child1, child2])
    db.session.commit()

    # Create grandchildren
    grandchild1 = SeriesGroup(
        name="GrandChildSG1",
        description="First Grandchild SeriesGroup",
        series_group_code="GCSG001",
        parent=child1,
    )
    grandchild2 = SeriesGroup(
        name="GrandChildSG2",
        description="Second Grandchild SeriesGroup",
        series_group_code="GCSG002",
        parent=child1,
    )
    db.session.add_all([grandchild1, grandchild2])
    db.session.commit()

    # Verify relationships
    assert grandchild1.parent == child1, "Grandchild1's parent should be ChildSG1."
    assert grandchild2.parent == child1, "Grandchild2's parent should be ChildSG1."
    assert (
        child1 in seriesgroup.children.all()
    ), "ChildSG1 should be a child of ParentSG."
    assert (
        grandchild1 in child1.children.all()
    ), "GrandChildSG1 should be a child of ChildSG1."
    assert (
        grandchild2 in child1.children.all()
    ), "GrandChildSG2 should be a child of ChildSG1."


def test_seriesbase_keywords_relationship(app, create_seriesgroup_and_type):
    """
    Test that SeriesBase (SeriesGroup and TimeSeries) can have multiple keywords associated.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    # Add keywords to SeriesGroup
    seriesgroup.add_keyword("Finance")
    seriesgroup.add_keyword("Investment")
    db.session.commit()

    # Verify keywords
    assert len(seriesgroup.keywords) == 2, "SeriesGroup should have two keywords."
    keywords = [kw.word for kw in seriesgroup.keywords]
    assert "Finance" in keywords, "SeriesGroup should have the 'Finance' keyword."
    assert "Investment" in keywords, "SeriesGroup should have the 'Investment' keyword."

    # Create a TimeSeries and add keywords
    ts = TimeSeries(name="TS_Keywords", time_series_type=tstype, code="TSK001")
    ts.add_keyword("Growth")
    ts.add_keyword("Value")
    db.session.add(ts)
    db.session.commit()

    # Verify keywords
    assert len(ts.keywords) == 2, "TimeSeries should have two keywords."
    ts_keywords = [kw.word for kw in ts.keywords]
    assert "Growth" in ts_keywords, "TimeSeries should have the 'Growth' keyword."
    assert "Value" in ts_keywords, "TimeSeries should have the 'Value' keyword."


def test_datapoint_date_release_logic(app, create_seriesgroup_and_type):
    """
    Test the conditional assignment of date_release in DataPoint.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    # Create a TimeSeries
    ts = TimeSeries(name="TS_DateRelease", time_series_type=tstype, code="TSD001")
    db.session.add(ts)
    db.session.commit()

    # Create DataPoints with and without date_release
    dp1 = DataPoint(
        date=datetime.date(2025, 1, 1),
        value=100.0,
        date_release=datetime.date(2025, 1, 2),
        time_series=ts,
    )
    dp2 = DataPoint(
        date=datetime.date(2025, 1, 3), value=110.0, time_series=ts
    )  # No date_release
    db.session.add_all([dp1, dp2])
    db.session.commit()

    # Verify date_release
    assert dp1.date_release == datetime.date(
        2025, 1, 2
    ), "DataPoint1's date_release should be set correctly."
    assert dp2.date_release is None, "DataPoint2's date_release should be None."


def test_seriesbase_unique_constraints(app, create_seriesgroup_and_type):
    """
    Test unique constraints on SeriesGroup and TimeSeries.
    """
    seriesgroup, tstype = create_seriesgroup_and_type

    # Create a SeriesGroup with a unique code
    sg1 = SeriesGroup(
        name="SG_Unique1",
        description="Unique SeriesGroup 1",
        series_group_code="SGU001",
    )
    db.session.add(sg1)
    db.session.commit()

    # Attempt to create another SeriesGroup with the same code
    sg2 = SeriesGroup(
        name="SG_Unique2",
        description="Unique SeriesGroup 2",
        series_group_code="SGU001",
    )
    db.session.add(sg2)

    with pytest.raises(Exception) as exc_info:
        db.session.commit()

    db.session.rollback()
    assert "UNIQUE constraint failed" in str(
        exc_info.value
    ), "Duplicate SeriesGroup codes should violate unique constraint."

    # Similarly, test TimeSeries unique code
    ts1 = TimeSeries(name="TS_Unique1", time_series_type=tstype, code="TSU001")
    db.session.add(ts1)
    db.session.commit()

    ts2 = TimeSeries(name="TS_Unique2", time_series_type=tstype, code="TSU001")
    db.session.add(ts2)

    with pytest.raises(Exception) as exc_info_ts:
        db.session.commit()

    db.session.rollback()
    assert "UNIQUE constraint failed" in str(
        exc_info_ts.value
    ), "Duplicate TimeSeries codes should violate unique constraint."
