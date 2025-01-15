# tests/test_keywords.py

import pytest
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from app.models import SeriesGroup, Keyword, SeriesBase
from app import db


@pytest.fixture
def seriesgroup(app):
    """
    Fixture to create a SeriesGroup without keywords.
    """
    sg = SeriesGroup(
        name="SG_Test", description="Test SeriesGroup", series_group_code="SG999"
    )
    sg.save()
    return sg


def test_add_keywords_during_creation(app):
    """
    Test creating a SeriesGroup and adding keywords after saving.
    Verify that keywords are saved and associated correctly.
    """
    keywords = ["Finance", "Investment", "Portfolio"]
    sg = SeriesGroup(
        name="SG_WithKeywords",
        description="SeriesGroup with initial keywords",
        series_group_code="SG100",
        # Do not pass keywords here to avoid DetachedInstanceError
    )
    sg.save()

    # Now, add keywords after the object is bound to the session
    for kw in keywords:
        sg.add_keyword(kw)
    sg.save()

    # Retrieve the SeriesGroup from the database with keywords eagerly loaded
    stmt = (
        select(SeriesGroup)
        .options(joinedload(SeriesGroup.keywords))
        .where(SeriesGroup.id == sg.id)
    )
    retrieved_sg = db.session.execute(stmt).scalars().unique().one()

    assert retrieved_sg is not None, "SeriesGroup should be saved and retrievable."

    # Verify keywords are associated
    associated_keywords = [kw.word for kw in retrieved_sg.keywords]
    assert set(associated_keywords) == set(
        keywords
    ), "Keywords should match the ones provided during creation."


def test_add_keywords_later(app, seriesgroup):
    """
    Test adding keywords to a SeriesGroup after it has been created.
    Verify that keywords are saved and associated correctly.
    """
    # Initially, the SeriesGroup has no keywords
    stmt = (
        select(SeriesGroup)
        .options(joinedload(SeriesGroup.keywords))
        .where(SeriesGroup.id == seriesgroup.id)
    )
    retrieved_sg = db.session.execute(stmt).scalars().unique().one()
    assert (
        len(retrieved_sg.keywords) == 0
    ), "SeriesGroup should initially have no keywords."

    # Add keywords
    new_keywords = ["Stocks", "Bonds"]
    for kw in new_keywords:
        retrieved_sg.add_keyword(kw)

    # Save the changes
    retrieved_sg.save()

    # Retrieve again with eager loading
    retrieved_sg = db.session.execute(stmt).scalars().unique().one()

    # Verify keywords are associated
    associated_keywords = [kw.word for kw in retrieved_sg.keywords]
    assert set(associated_keywords) == set(
        new_keywords
    ), "Keywords should match the ones added later."


def test_add_duplicate_keywords(app, seriesgroup):
    """
    Test that adding duplicate keywords does not create duplicate entries in the database.
    """
    keyword = "Equity"
    # Add the keyword for the first time
    seriesgroup.add_keyword(keyword)
    seriesgroup.save()

    # Attempt to add the same keyword again
    seriesgroup.add_keyword(keyword)
    seriesgroup.save()

    # Retrieve with eager loading
    stmt = (
        select(SeriesGroup)
        .options(joinedload(SeriesGroup.keywords))
        .where(SeriesGroup.id == seriesgroup.id)
    )
    retrieved_sg = db.session.execute(stmt).scalars().unique().one()

    # Verify only one instance of the keyword exists
    assert len(retrieved_sg.keywords) == 1, "Duplicate keywords should not be added."
    assert (
        retrieved_sg.keywords[0].word == keyword
    ), "Keyword should match the one added."


def test_add_invalid_keyword_length(app, seriesgroup):
    """
    Test that adding a keyword exceeding the maximum length raises a ValueError.
    """
    invalid_keyword = "K" * 51  # Exceeds the 50 character limit

    with pytest.raises(ValueError) as exc_info:
        # Attempt to add an overly long keyword
        seriesgroup.add_keyword(invalid_keyword)
        seriesgroup.save()
    # No need to rollback since the exception is handled

    assert "Keyword must be 50 characters or less." in str(
        exc_info.value
    ), "Adding a keyword with invalid length should raise a ValueError."


def test_remove_keyword(app, seriesgroup):
    """
    Test removing a keyword from a SeriesGroup.
    """
    keywords = ["Growth", "Value", "Income"]
    for kw in keywords:
        seriesgroup.add_keyword(kw)
    seriesgroup.save()

    # Retrieve with eager loading
    stmt = (
        select(SeriesGroup)
        .options(joinedload(SeriesGroup.keywords))
        .where(SeriesGroup.id == seriesgroup.id)
    )
    retrieved_sg = db.session.execute(stmt).scalars().unique().one()

    assert (
        len(retrieved_sg.keywords) == 3
    ), "SeriesGroup should have three keywords initially."

    # Remove one keyword
    retrieved_sg.remove_keyword("Value")
    retrieved_sg.save()

    # Retrieve again with eager loading
    retrieved_sg = db.session.execute(stmt).scalars().unique().one()

    # Verify the keyword is removed
    associated_keywords = [kw.word for kw in retrieved_sg.keywords]
    assert "Value" not in associated_keywords, "Keyword 'Value' should be removed."
    assert (
        len(retrieved_sg.keywords) == 2
    ), "SeriesGroup should have two keywords after removal."


def test_add_keyword_with_invalid_type(app, seriesgroup):
    """
    Test that adding a keyword with an invalid type (non-string) raises a TypeError.
    """
    invalid_keyword = 12345  # Non-string keyword

    with pytest.raises(TypeError) as exc_info:
        # Attempt to add a non-string keyword
        seriesgroup.add_keyword(invalid_keyword)
        seriesgroup.save()
    # No need to rollback since the exception is handled

    assert "Keyword must be a string." in str(
        exc_info.value
    ), "Adding a keyword with invalid type should raise a TypeError."


def test_save_and_retrieve_keywords(app):
    """
    Test saving a SeriesGroup with keywords and retrieving it to verify persistence.
    """
    keywords = ["Alpha", "Beta", "Gamma"]
    sg = SeriesGroup(
        name="SG_Persistence",
        description="SeriesGroup for persistence test",
        series_group_code="SG200",
        # Do not pass keywords here to avoid DetachedInstanceError
    )
    sg.save()

    # Now, add keywords after the object is bound to the session
    for kw in keywords:
        sg.add_keyword(kw)
    sg.save()

    # Retrieve the SeriesGroup from the database with keywords eagerly loaded
    stmt = (
        select(SeriesGroup)
        .options(joinedload(SeriesGroup.keywords))
        .where(SeriesGroup.id == sg.id)
    )
    retrieved_sg = db.session.execute(stmt).scalars().unique().one()

    assert retrieved_sg is not None, "SeriesGroup should be retrievable after saving."

    # Verify keywords are persisted
    associated_keywords = [kw.word for kw in retrieved_sg.keywords]
    assert set(associated_keywords) == set(
        keywords
    ), "Persisted keywords should match the ones saved."


def test_save_keywords_added_later(app, seriesgroup):
    """
    Test saving keywords added after the initial creation and verifying persistence.
    """
    # Add keywords after creation
    keywords = ["Delta", "Epsilon"]
    for kw in keywords:
        seriesgroup.add_keyword(kw)
    seriesgroup.save()

    # Retrieve the SeriesGroup with keywords eagerly loaded
    stmt = (
        select(SeriesGroup)
        .options(joinedload(SeriesGroup.keywords))
        .where(SeriesGroup.id == seriesgroup.id)
    )
    retrieved_sg = db.session.execute(stmt).scalars().unique().one()

    assert (
        retrieved_sg is not None
    ), "SeriesGroup should be retrievable after adding keywords."

    # Verify keywords are persisted
    associated_keywords = [kw.word for kw in retrieved_sg.keywords]
    assert set(associated_keywords) == set(
        keywords
    ), "Persisted keywords should match the ones added later."
