import pandas as pd
import numpy as np
import pytest
from settings import config
from merge_bond_treasury_redcode import * 
from datetime import date, datetime
import datetime as datetime


def test_merge_treasury_data():    
    issue_df = pd.DataFrame({
        'kycrspid': [1, 2, 3, 4, 6, np.NaN],
        'kycrspid': [1, 2, 3, 4, 6, np.NaN],
        'kytreasno': [1, 2, 3, 4, 6, np.NaN],
        'tmatdt': [date(2020, 1, 1), date(2020, 1, 1), np.NaN, date(2020, 1, 1), date(2020, 1, 1), date(2020, 1, 1)]
    })

    treas_df = pd.DataFrame({
        'kycrspid': [1, 2, 3, 4, 5, np.NaN],
        'kytreasno': [1, 2, 3, 4, 5, np.NaN],
        'mcaldt': [np.NaN, date(2000, 1, 1), date(2000, 1, 1), date(2000, 1, 1), date(2000, 1, 1), date(2000, 1, 1)],
        'tmpubout': [100] * 6,
        'tmyld': [0.0005, np.NaN, 0.0005, 0.0005, 0.0005, 0.0005]
    })

    res_df = merge_treasury_data(issue_df, treas_df)

    assert isinstance(res_df, pd.DataFrame)
    assert not res_df.empty, "res_df is empty, expected at least one row"
    treas_yld = res_df.iloc[0]['treas_yld']

    assert treas_yld == pytest.approx(0.2005, rel=1e-2) 
    
    res_df = res_df.drop(columns={'treas_yld'})

    expected_df = pd.DataFrame({
        'kycrspid': [4],
        'kytreasno': [4],
        'mcaldt': [date(2000, 1, 1)],
        'tmpubout': [100],
        'tmatdt': [date(2020, 1, 1)]
        })
    
    expected_df.index = [3]

    pd.testing.assert_frame_equal(res_df, expected_df, check_dtype=False)

def test_merge_treasuries_into_bonds():
    # Mock bond dataset
    bond_df = pd.DataFrame({
        'cusip': ['123456', '654321'],
        'company_symbol': ['AAPL', 'MSFT'],
        'date': [date(2025, 1, 31), date(2025, 2, 28)],
        'maturity': [date(2030, 1, 1), date(2030, 6, 1)],
        'amount_outstanding': [500000, 750000],
        'yield': [0.05, 0.045],
        'rating': [0, 1],
        'price_eom': [101, 99.5],
        't_spread': [1.5, 2.0]
    })

    # Mock treasury dataset
    treas_df = pd.DataFrame({
        'kycrspid': [1, 2],
        'kytreasno': [101, 102],
        'mcaldt': [date(2025, 1, 15), date(2025, 2, 15)],
        'tmpubout': [1000000, 2000000],
        'treas_yld': [0.03, 0.032],
        'tmatdt': [date(2030, 1, 1), date(2030, 6, 1)]
    })

    merged_df = merge_treasuries_into_bonds(bond_df, treas_df, day_window=3)

    assert isinstance(merged_df, pd.DataFrame), "Output should be a DataFrame"
    assert not merged_df.empty, "Merged DataFrame should not be empty"
    
    expected_cols = {'cusip', 'company_symbol', 'date', 'maturity', 'amount_outstanding', 'yield',
                     'rating', 'price_eom', 't_spread', 'treas_yld'}
    assert set(merged_df.columns) == expected_cols, f"Expected columns: {expected_cols}, but got {set(merged_df.columns)}"

    expected_ylds = {datetime.datetime(2030, 1, 1, 0, 0): 0.03, datetime.datetime(2030, 6, 1, 0, 0): 0.032}
    for _, row in merged_df.iterrows():
        expected_treas_yld = expected_ylds[row['maturity']]
        assert row['treas_yld'] == pytest.approx(expected_treas_yld, rel=1e-2), \
            f"Unexpected treasury yield: {row['treas_yld']} for maturity {row['maturity']}"
        

def test_merge_red_code_into_bond_treas():
    bond_treas_df = pd.DataFrame({
        'cusip': ['123456AB1', '654321XY2', '987654CD3'],
        'company_symbol': ['AAPL', 'MSFT', 'GOOGL'],
        'date': pd.to_datetime(['2025-01-31', '2025-02-28', '2025-03-31']),
        'maturity': pd.to_datetime(['2030-01-01', '2030-06-01', '2035-12-01']),
        'amount_outstanding': [500000, 750000, 1000000],
        'yield': [0.05, 0.045, 0.06],
        'rating': [0, 1, 0],  # IG (0) or HY (1)
        'price_eom': [101, 99.5, 105],
        't_spread': [1.5, 2.0, 1.2],
        'treas_yld': [0.03, 0.032, 0.028]
    })

    red_c_df = pd.DataFrame({
        'obl_cusip': ['123456XX9', '654321AA8', '999999ZZ7'],
        'redcode': ['RED123', 'RED654', 'RED999'],
        'ticker': ['AAPL', 'MSFT', 'TSLA'],
        'isin': ['US1234567890', 'US6543217890', 'US9999997890'],
        'tier': ['Senior', 'Subordinated', 'Senior']
    })

    merged_df = merge_red_code_into_bond_treas(bond_treas_df, red_c_df)

    # Assertions
    assert isinstance(merged_df, pd.DataFrame), "Output should be a DataFrame"
    assert not merged_df.empty, "Merged DataFrame should not be empty"
    
    expected_cols = {'cusip', 'yield', 't_spread', 'issuer_cusip', 'redcode', 'amount_outstanding', 
                     'rating', 'company_symbol', 'treas_yld', 'date', 'price_eom', 'maturity'}
    assert set(merged_df.columns) == expected_cols, f"Expected columns: {expected_cols}, but got {set(merged_df.columns)}"


    for _, row in merged_df.iterrows():
        assert row['issuer_cusip'] == row['cusip'][:6], f"Issuer CUSIP mismatch: {row['issuer_cusip']} != {row['cusip'][:6]}"
    
    expected_redcodes = {'123456': 'RED123', '654321': 'RED654'}
    for _, row in merged_df.iterrows():
        assert row['redcode'] == expected_redcodes[row['issuer_cusip']], \
            f"Unexpected redcode: {row['redcode']} for issuer_cusip {row['issuer_cusip']}"
