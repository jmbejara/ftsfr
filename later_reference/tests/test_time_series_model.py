import os
import sys

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from models.time_series_model import TimeSeriesModel
from models.utils import create_simulated_X, create_simulated_y


def test_instanciate_time_series_model():
    y = create_simulated_y()
    X = create_simulated_X()
    model = TimeSeriesModel(y, X, step_size=1)
    assert model.dataset.X.shape == model.X.shape
    assert model.dataset.X.equals(X)
    assert model.dataset.y.equals(model.y)
    assert model.step_size == 1
    assert model.forecasting_start_date is None
    assert model.n_forecasting is None
    assert model.intersect_forecasting is False
    assert model.rolling is False
    assert model.error_metrics is not None
    assert model.divisions == {}


def test_create_divisions():
    y = create_simulated_y()
    model = TimeSeriesModel(
        y, filter_start_date="2022-01-01", n_forecasting=12, rolling=False
    )
    model.build_divisions()
    old_idx = -1
    old_last_date = model.divisions[0]["training"].y.index[-2]
    for idx, division in model.divisions.items():
        assert idx > old_idx
        old_idx = idx
        assert (
            division["training"].y.index[-1] + pd.Timedelta(days=1)
            == division["forecasting"].y.index[0]
        )
        assert division["training"].y.index[-1] - pd.Timedelta(days=1) == old_last_date
        old_last_date = division["training"].y.index[-1]


def test_create_divisions_with_bigger_steps():
    y = create_simulated_y()
    model = TimeSeriesModel(
        y, filter_start_date="2022-01-01", n_forecasting=12, rolling=False, step_size=3
    )
    model.build_divisions()
    for idx in model.divisions.keys():
        for i in range(3):
            assert (
                model.divisions[idx]["training"].y.index[-1] + pd.Timedelta(days=i + 1)
                == model.divisions[idx]["forecasting"].y.index[i]
            )
        len(model.divisions[idx]["forecasting"].y.index) == 3


def test_different_n_forecasting():
    y = create_simulated_y(n_periods=1e4)
    for n_forecasting in range(100, 500, 100):
        model = TimeSeriesModel(y, n_forecasting=n_forecasting, rolling=False)
        model.build_divisions()
        assert len(model.divisions) == n_forecasting


def test_create_divisions_with_intersection():
    y = create_simulated_y()
    model = TimeSeriesModel(
        y,
        filter_start_date="2022-01-01",
        n_forecasting=12,
        rolling=False,
        step_size=3,
        intersect_forecasting=True,
    )
    model.build_divisions()
    model.divisions[0]


if __name__ == "__main__":
    test_different_n_forecasting()
    test_create_divisions()
    test_instanciate_time_series_model()
