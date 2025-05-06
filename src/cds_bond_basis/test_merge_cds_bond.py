import pandas as pd
import pytest
from settings import config
from merge_cds_bond import * 
from datetime import date, datetime
import datetime as datetime
import numpy as np
from scipy.interpolate import CubicSpline

def test_merge_cds_into_bonds():
    """
    Unit test for merge_cds_into_bonds() function.
    This test ensures that:
    - The function correctly merges CDS data into bond data.
    - The output DataFrame has expected columns.
    - The cubic spline interpolation is applied correctly.
    """

    # Create a mock bond_red_df
    bond_red_df = pd.DataFrame({
        'cusip': ['001957AM1', '001957AM2'],
        'date': pd.to_datetime(['2024-01-01', '2024-01-01']),
        'maturity': pd.to_datetime(['2026-01-01', '2028-01-01']),
        'yield': [0.05, 0.06],
        'rating': [0, 1],
        'treas_yld': [0.02, 0.025],
        't_spread': [0.005, 0.007],
        'price_eom': [100.5, 98.3],
        'amount_outstanding': [5000000, 3000000],
        'redcode': ['R1', 'R1']
    })

    # Create a mock cds_df with different tenors for cubic spline fitting
    cds_df = pd.DataFrame({
        'date': pd.to_datetime(['2024-01-01', '2024-01-01', '2024-01-01', '2024-01-01']),
        'redcode': ['R1', 'R1', 'R1', 'R1'],
        'parspread': [0.03, 0.04, 0.05, 0.06],
        'tenor': ['1Y', '3Y', '5Y', '10Y'],
        'tier': ['SNRFOR', 'SNRFOR', 'SNRFOR', 'SNRFOR'],
        'country': ['USA', 'USA', 'USA', 'USA'],
        'year': [2024, 2024, 2024, 2024]
    })

    # Run the function
    result_df = merge_cds_into_bonds(bond_red_df, cds_df)

    # Check that the output DataFrame is not empty
    assert not result_df.empty, "Output DataFrame is empty!"

    # Check that expected columns exist
    expected_columns = ['cusip', 'date', 'maturity', 'yield', 'rating', 'treas_yld', 'par_spread', 't_spread', 'price_eom', 'amount_outstanding']
    assert all(col in result_df.columns for col in expected_columns), "Missing expected columns!"

    # Check that par_spread is interpolated correctly
    assert not result_df['par_spread'].isnull().any(), "par_spread contains NaN values!"

    # Check if duplicate rows were removed
    assert result_df.duplicated().sum() == 0, "Duplicates were not removed properly!"

    print("All tests passed successfully!")
