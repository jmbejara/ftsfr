# tests/test_series_search.py

import pytest
import datetime
import pandas as pd
from sqlalchemy.exc import IntegrityError
from app.models import TimeSeries, SeriesGroup, Keyword, TimeSeriesType
from app.series import SeriesSearcher
from app import db


@pytest.fixture
def populate_series_for_search(app, basic_tstype):
    """
    Fixture to populate the database with TimeSeries and SeriesGroup objects
    for testing the SeriesSearcher.

    Returns:
        tuple: (list_of_timeseries, list_of_seriesgroups)
    """
    with app.app_context():
        # Create TimeSeries instances
        ts1 = TimeSeries(name="TS_First", code="ABC123")
        ts1.add_keyword("Finance")
        ts1.add_keyword("Investment")

        ts2 = TimeSeries(name="TS_Second", code="DEF456")
        ts2.add_keyword("Economics")

        ts3 = TimeSeries(name="My Timeseries", code="MYCODE")
        ts3.add_keyword("Investment")
        ts3.add_keyword("Strategy")

        # Create SeriesGroup instances
        sg1 = SeriesGroup(name="SG_Beta", series_group_code="SG001")
        sg1.add_keyword("Finance")

        sg2 = SeriesGroup(name="SG_Alpha", series_group_code="SG002")
        sg2.add_keyword("Investment")

        sg3 = SeriesGroup(name="Alpha Finance Group", series_group_code="SG003")
        sg3.add_keyword("Finance")
        sg3.add_keyword("Alpha")

        # Add all to the session
        db.session.add_all([ts1, ts2, ts3, sg1, sg2, sg3])
        db.session.commit()

        return [ts1, ts2, ts3], [sg1, sg2, sg3]


def test_search_by_name_exact(app, populate_series_for_search):
    """
    Test searching by exact name match for TimeSeries and SeriesGroup.
    """
    with app.app_context():
        # Exact match for TimeSeries name
        df_ts = SeriesSearcher.search(
            search_text="TS_First",
            search_by_name=True,
            search_by_code=False,
            search_by_keyword=False,
            partial=False,
            search_time_series=True,
            search_series_group=False,
        )
        assert df_ts is not None, "Search should return a DataFrame, not None."
        assert len(df_ts) == 1, "Should return exactly one TimeSeries."
        assert df_ts.iloc[0]["type"] == "TimeSeries"
        assert df_ts.iloc[0]["name"] == "TS_First"
        assert df_ts.iloc[0]["code"] == "ABC123"

        # Exact match for SeriesGroup name
        df_sg = SeriesSearcher.search(
            search_text="SG_Alpha",
            search_by_name=True,
            search_by_code=False,
            search_by_keyword=False,
            partial=False,
            search_time_series=False,
            search_series_group=True,
        )
        assert df_sg is not None, "Search should return a DataFrame, not None."
        assert len(df_sg) == 1, "Should return exactly one SeriesGroup."
        assert df_sg.iloc[0]["type"] == "SeriesGroup"
        assert df_sg.iloc[0]["name"] == "SG_Alpha"
        assert df_sg.iloc[0]["code"] == "SG002"


def test_search_by_code_partial(app, populate_series_for_search):
    """
    Test searching by partial code match for TimeSeries and SeriesGroup.
    """
    with app.app_context():
        # Partial match for TimeSeries code
        df_ts = SeriesSearcher.search(
            search_text="ABC",
            search_by_name=False,
            search_by_code=True,
            search_by_keyword=False,
            partial=True,
            search_time_series=True,
            search_series_group=False,
        )
        assert df_ts is not None, "Search should return a DataFrame, not None."
        assert (
            len(df_ts) == 1
        ), "Should return exactly one TimeSeries matching partial code."
        assert df_ts.iloc[0]["type"] == "TimeSeries"
        assert df_ts.iloc[0]["code"] == "ABC123"

        # Partial match for SeriesGroup code
        df_sg = SeriesSearcher.search(
            search_text="SG00",
            search_by_name=False,
            search_by_code=True,
            search_by_keyword=False,
            partial=True,
            search_time_series=False,
            search_series_group=True,
        )
        assert df_sg is not None, "Search should return a DataFrame, not None."
        assert (
            len(df_sg) == 3
        ), "Should return all SeriesGroups with codes starting with 'SG00'."
        expected_codes = {"SG001", "SG002", "SG003"}
        assert set(df_sg["code"]) == expected_codes


def test_search_by_keyword_exact(app, populate_series_for_search):
    """
    Test searching by exact keyword match.
    """
    with app.app_context():
        # Exact keyword "Finance"
        df = SeriesSearcher.search(
            search_text="Finance",
            search_by_name=False,
            search_by_code=False,
            search_by_keyword=True,
            partial=False,
            search_time_series=True,
            search_series_group=True,
        )
        assert df is not None, "Search should return a DataFrame, not None."
        # Finance is associated with ts1, sg1, sg3
        assert (
            len(df) == 3
        ), "Should return three records associated with 'Finance' keyword."
        expected_types = {"TimeSeries", "SeriesGroup"}
        assert set(df["type"]) == expected_types
        expected_names = {"TS_First", "SG_Beta", "Alpha Finance Group"}
        assert set(df["name"]) == expected_names


def test_search_by_keyword_partial(app, populate_series_for_search):
    """
    Test searching by partial keyword match.
    """
    with app.app_context():
        # Partial keyword "Invest" should match "Investment"
        df = SeriesSearcher.search(
            search_text="Invest",
            search_by_name=False,
            search_by_code=False,
            search_by_keyword=True,
            partial=True,
            search_time_series=True,
            search_series_group=True,
        )
        assert df is not None, "Search should return a DataFrame, not None."
        # "Investment" is associated with ts1, ts3, sg2
        assert (
            len(df) == 3
        ), "Should return three records associated with partial 'Invest' keyword."
        expected_types = {"TimeSeries", "SeriesGroup"}
        assert set(df["type"]) == expected_types
        expected_names = {"TS_First", "My Timeseries", "SG_Alpha"}
        assert set(df["name"]) == expected_names


def test_search_combined_fields(app, populate_series_for_search):
    """
    Test searching by multiple fields simultaneously.
    """
    with app.app_context():
        # Search for 'Alpha' in name and keyword
        df = SeriesSearcher.search(
            search_text="Alpha",
            search_by_name=True,
            search_by_code=False,
            search_by_keyword=True,
            partial=True,
            search_time_series=True,
            search_series_group=True,
        )
        assert df is not None, "Search should return a DataFrame, not None."
        # 'Alpha' appears in sg2 name ("SG_Alpha") and sg3 keyword ("Alpha")
        assert (
            len(df) == 2
        ), "Should return two records matching 'Alpha' in name or keyword."
        expected_types = {"SeriesGroup"}
        assert set(df["type"]) == expected_types
        expected_names = {"SG_Alpha", "Alpha Finance Group"}
        assert set(df["name"]) == expected_names


def test_search_no_results(app, populate_series_for_search):
    """
    Test that searching for a non-existent string returns None.
    """
    with app.app_context():
        df = SeriesSearcher.search(
            search_text="NonExistent",
            search_by_name=True,
            search_by_code=True,
            search_by_keyword=True,
            partial=True,
            search_time_series=True,
            search_series_group=True,
        )
        assert df is None, "Search should return None when no matches are found."


def test_search_limit_rows(app, populate_series_for_search):
    """
    Test that the search respects the limit_rows parameter.
    """
    with app.app_context():
        # Add more SeriesGroup to exceed the limit
        for i in range(4, 110):
            sg = SeriesGroup(name=f"SG_Test_{i}", series_group_code=f"SG{100+i}")
            sg.add_keyword("TestKeyword")
            sg.save(commit=False)
        db.session.commit()

        # Search by keyword "TestKeyword" with limit_rows=10
        df = SeriesSearcher.search(
            search_text="TestKeyword",
            search_by_name=False,
            search_by_code=False,
            search_by_keyword=True,
            partial=False,
            search_time_series=False,
            search_series_group=True,
            limit_rows=10,
        )
        assert df is not None, "Search should return a DataFrame, not None."
        assert len(df) == 10, "Search should return at most 10 rows as per limit_rows."

        # Verify that only SeriesGroup types are returned
        assert set(df["type"]) == {
            "SeriesGroup"
        }, "Only SeriesGroup records should be returned."


def test_search_multiple_timeseries_and_seriesgroup(app, populate_series_for_search):
    """
    Test searching that returns multiple TimeSeries and SeriesGroup records.
    """
    with app.app_context():
        # Search for keyword "Investment" which is associated with ts1, ts3, sg2
        df = SeriesSearcher.search(
            search_text="Investment",
            search_by_name=False,
            search_by_code=False,
            search_by_keyword=True,
            partial=False,
            search_time_series=True,
            search_series_group=True,
        )
        assert df is not None, "Search should return a DataFrame, not None."
        assert (
            len(df) == 3
        ), "Should return three records associated with 'Investment' keyword."
        expected_types = {"TimeSeries", "SeriesGroup"}
        assert set(df["type"]) == expected_types
        expected_names = {"TS_First", "My Timeseries", "SG_Alpha"}
        assert set(df["name"]) == expected_names


def test_search_partial_and_exact(app, populate_series_for_search):
    """
    Test searching with partial=False and partial=True in different scenarios.
    """
    with app.app_context():
        # Partial=False: exact match for "Strategy"
        df_exact = SeriesSearcher.search(
            search_text="Strategy",
            search_by_name=False,
            search_by_code=False,
            search_by_keyword=True,
            partial=False,
            search_time_series=True,
            search_series_group=False,
        )
        assert df_exact is not None, "Search should return a DataFrame, not None."
        assert (
            len(df_exact) == 1
        ), "Should return exactly one TimeSeries with keyword 'Strategy'."
        assert df_exact.iloc[0]["type"] == "TimeSeries"
        assert df_exact.iloc[0]["name"] == "My Timeseries"

        # Partial=True: partial match for "Strat" should also find "Strategy"
        df_partial = SeriesSearcher.search(
            search_text="Strat",
            search_by_name=False,
            search_by_code=False,
            search_by_keyword=True,
            partial=True,
            search_time_series=True,
            search_series_group=False,
        )
        assert df_partial is not None, "Search should return a DataFrame, not None."
        assert (
            len(df_partial) == 1
        ), "Should return one TimeSeries matching partial keyword 'Strat'."
        assert df_partial.iloc[0]["type"] == "TimeSeries"
        assert df_partial.iloc[0]["name"] == "My Timeseries"


def test_search_by_name_partial(app, populate_series_for_search):
    """
    Test searching by partial name match.
    """
    with app.app_context():
        # Partial match for "TS" should match "TS_First" and "TS_Second"
        df = SeriesSearcher.search(
            search_text="TS",
            search_by_name=True,
            search_by_code=False,
            search_by_keyword=False,
            partial=True,
            search_time_series=True,
            search_series_group=False,
        )
        assert df is not None, "Search should return a DataFrame, not None."
        assert len(df) == 2, "Should return two TimeSeries matching partial name 'TS'."
        expected_names = {"TS_First", "TS_Second"}
        assert set(df["name"]) == expected_names


def test_search_only_seriesgroup_by_keyword(app, populate_series_for_search):
    """
    Test searching only within SeriesGroup by keyword.
    """
    with app.app_context():
        # Search for keyword "Alpha"
        df = SeriesSearcher.search(
            search_text="Alpha",
            search_by_name=False,
            search_by_code=False,
            search_by_keyword=True,
            partial=False,
            search_time_series=False,
            search_series_group=True,
        )
        assert df is not None, "Search should return a DataFrame, not None."
        # "Alpha" keyword is associated with sg3
        assert len(df) == 1, "Should return one SeriesGroup with 'Alpha' keyword."
        assert df.iloc[0]["type"] == "SeriesGroup"
        assert df.iloc[0]["name"] == "Alpha Finance Group"


def test_search_with_empty_search_text(app, populate_series_for_search):
    """
    Test searching with empty search_text should return an empty DataFrame.
    """
    with app.app_context():
        df = SeriesSearcher.search(
            search_text="",
            search_by_name=True,
            search_by_code=True,
            search_by_keyword=True,
            partial=True,
            search_time_series=True,
            search_series_group=True,
        )
        assert isinstance(df, pd.DataFrame), "Search should return a DataFrame."
        assert (
            df.empty
        ), "Search with empty search_text should return an empty DataFrame."


def test_search_multiple_keywords(app, populate_series_for_search):
    """
    Test that searching with a keyword returns all associated records.
    """
    with app.app_context():
        # Search for keyword "Investment" which is associated with ts1, ts3, sg2
        df = SeriesSearcher.search(
            search_text="Investment",
            search_by_name=False,
            search_by_code=False,
            search_by_keyword=True,
            partial=False,
            search_time_series=True,
            search_series_group=True,
        )
        assert df is not None, "Search should return a DataFrame, not None."
        assert (
            len(df) == 3
        ), "Should return three records associated with 'Investment' keyword."
        expected_names = {"TS_First", "My Timeseries", "SG_Alpha"}
        assert set(df["name"]) == expected_names
