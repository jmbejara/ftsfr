"""
Nelson-Siegel-Svensson yield-curve fitting following Gurkaynak, Sack, and
Wright (2006). Adapted for ftsfr from the student replication of
Siriwardane, Sunderam, Wallen (2021).

The CRSP Treasury panel and Fed GSW yield-curve files are already produced
elsewhere in this repo, so this module only contains fitting code; data
pulls live in:

- src/us_treasury_returns/pull_CRSP_treasury.py  -> CRSP_TFZ_with_runness.parquet
- src/fed_yield_curve/pull_fed_yield_curve.py     -> fed_yield_curve.parquet
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd

from finm.fixedincome import (
    spot,
    discount,
    calc_cashflows,
    fit,
    gurkaynak_sack_wright_filters,
)

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
CRSP_TREASURY_PATH = DATA_DIR / "us_treasury_returns" / "CRSP_TFZ_with_runness.parquet"

PARAM_NAMES = ("tau1", "tau2", "beta1", "beta2", "beta3", "beta4")
PARAMS0 = np.array([1.0, 10.0, 3.0, 3.0, 3.0, 3.0])


def load_crsp_treasury_for_fitting() -> pd.DataFrame:
    """Load the ftsfr CRSP Treasury panel and apply GSW filters."""
    df = pd.read_parquet(CRSP_TREASURY_PATH)
    df = gurkaynak_sack_wright_filters(df)
    return df


def fit_curve_for_quote_date(quote_date, df_all: pd.DataFrame, params0=PARAMS0):
    """Fit NSS parameters on a single quote date."""
    params_star, error = fit(pd.Timestamp(quote_date), df_all, params0)
    return params_star, error


def _resolve_quote_date(target_date, available_dates: pd.DatetimeIndex):
    """
    Map a target date to an available CRSP quote date.

    Priority:
    1) exact date
    2) latest prior date in the same month
    """
    target_date = pd.Timestamp(target_date)
    if target_date in available_dates:
        return target_date, "exact"

    prior = available_dates[available_dates <= target_date]
    if len(prior) == 0:
        return pd.NaT, "no_prior_date"

    candidate = prior[-1]
    if candidate.to_period("M") == target_date.to_period("M"):
        return candidate, "prior_same_month"
    return pd.NaT, "no_date_in_month"
