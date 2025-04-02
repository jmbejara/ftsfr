import os
import sys

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from tests.utils import del_files

from models.time_series_model import (
    TEST_PATH_TIME_SERIES_MODELS_RESULTS,
)
from models.univariate_local import (
    HoltWintersForecasting,
)
from models.utils import create_simulated_y


@del_files
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


@del_files
def test_saving_time_series_models():
    y = create_simulated_y()
    um = HoltWintersForecasting(y=y, n_forecasting=12, time_frequency="D")
    um.build_divisions()
    um.run()
    um.assess_error()
    um.save(save_error_metrics=False, test_path=True)
    assert os.path.exists(TEST_PATH_TIME_SERIES_MODELS_RESULTS)
    ts_model_frame = pd.read_csv(TEST_PATH_TIME_SERIES_MODELS_RESULTS)
    assert len(ts_model_frame.index) == 1
    assert "y" in list(ts_model_frame.columns) and "model" in list(
        ts_model_frame.columns
    )


@del_files
def test_saving_error_metrics():
    y = create_simulated_y()
    um = HoltWintersForecasting(y=y, n_forecasting=12, time_frequency="D")
    um.build_divisions()
    um.run()
    um.assess_error()
    um.save(save_error_metrics=True, test_path=True)
    assert os.path.exists(TEST_PATH_TIME_SERIES_MODELS_RESULTS)
    error_metrics_frame = pd.read_csv(TEST_PATH_TIME_SERIES_MODELS_RESULTS)
    assert len(error_metrics_frame.index) == 1
    assert "y" in list(error_metrics_frame.columns) and "model" in list(
        error_metrics_frame.columns
    )
    ts_model_frame = pd.read_csv(TEST_PATH_TIME_SERIES_MODELS_RESULTS)
    assert ts_model_frame["id"].iloc[0] == error_metrics_frame["id"].iloc[0]
    assert ts_model_frame["model"].iloc[0] == error_metrics_frame["model"].iloc[0]
