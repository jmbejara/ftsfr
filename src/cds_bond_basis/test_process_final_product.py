import pandas as pd
import pytest
from settings import config
from merge_cds_bond import * 
from datetime import date, datetime
import datetime as datetime
import numpy as np
from process_final_product import *
import os

def test_process_cb_spread():
    """
    Unit test for calc_cb_spread() function.
    This test ensures that:
    - The function correctly calculates the FR, CB, and rfr columns.
    - The output DataFrame contains the expected additional columns.
    - The calculations follow the expected formulas.
    """

    # Create a mock dataframe
    test_df = pd.DataFrame({
        'cusip': ['001957AM1', '001957AM2'],
        'date': pd.to_datetime(['2024-01-01', '2024-01-01']),
        'maturity': pd.to_datetime(['2026-01-01', '2028-01-01']),
        'yield': [0.05, 0.06],
        'rating': [0, 1],
        'treas_yld': [0.02, 0.025],
        'par_spread': [0.03, 0.04],
        't_spread': [0.005, 0.007],
        'price_eom': [100.5, 98.3],
        'amount_outstanding': [5000000, 3000000]
    })

    # Apply the function
    result_df = process_cb_spread(test_df)

    # Expected calculations
    expected_FR = test_df['yield'] - test_df['treas_yld']
    expected_CB = test_df['par_spread'] - expected_FR
    expected_rfr = test_df['treas_yld'] - expected_CB

    # Check that the new columns exist
    assert 'FR' in result_df.columns, "FR column is missing!"
    assert 'CB' in result_df.columns, "CB column is missing!"
    assert 'rfr' in result_df.columns, "rfr column is missing!"

    # Validate calculations
    assert (result_df['FR'] == expected_FR).all(), "FR values are incorrect!"
    assert (result_df['CB'] == expected_CB).all(), "CB values are incorrect!"
    assert (result_df['rfr'] == expected_rfr).all(), "rfr values are incorrect!"

    print("All tests passed successfully!")
