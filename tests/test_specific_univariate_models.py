import pytest
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from models.utils import create_simulated_X, create_simulated_y
from models.time_series_model import TimeSeriesModel
from models.univariate_local import (
    HoltWintersForecasting,
    MeanForecasting,
    NaiveForecasting,
    SarimaForecasting,
)


UNIVARIATE_LOCAL = [
    HoltWintersForecasting,
    MeanForecasting,
    NaiveForecasting,
    SarimaForecasting,
]


def test_error_metrics_frame():
    y = create_simulated_y()
    um = HoltWintersForecasting(y=y, n_forecasting=12, time_frequency="D")
    um.build_divisions()
    um.run()
    um.assess_error()
    error_metrics_frame = um.get_error_metrics_frame()
    assert isinstance(error_metrics_frame, pd.DataFrame)
    assert "model" in list(error_metrics_frame.columns) and "y" in list(
        error_metrics_frame.columns
    )
    assert len(error_metrics_frame.index) == 1
    assert error_metrics_frame.drop(["model", "y"], axis=1).isnull().sum().sum() == 0
    assert all(
        isinstance(e, (int, float))
        for e in error_metrics_frame.drop(["model", "y"], axis=1).iloc[0, :].values
    )
