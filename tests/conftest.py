# tests/conftest.py

import pytest
import sys
import pandas as pd
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db


@pytest.fixture(scope="function")
def app():
    """
    Create and configure a new app instance for each test.
    """
    # Set the environment variable to 'testing'
    os.environ["FLASK_ENV"] = "testing"

    # Create the Flask app with testing configuration
    app = create_app("testing")

    # Establish an application context
    with app.app_context():
        # Create the database and the database tables
        db.create_all()
        yield app
        # Drop the database tables after the test
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """
    Create a test client for the app.
    """
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """
    Create a CLI runner for the app.
    """
    return app.test_cli_runner()


# Import fixtures from fixtures.py
from .fixtures import (
    populate_test_db,
    sample_df_single_column,
    sample_df_multiple_columns,
    create_seriesgroup_and_type,
    basic_tstype,
)
