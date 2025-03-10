import pytest
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from models.utils import create_simulated_X, create_simulated_y
from models.univariate_local import SarimaForecasting
from models.error_metrics import EXTRA_COLUMNS

# def test_one_step_sarima():
#     y = create_simulated_y()
#     model = SarimaForecasting(
#         y,
#         filter_start_date="2022-01-01",
#         n_forecasting=3,
#         rolling=False,
#         step_size=1,
#         intersect_forecasting=False,
#         max_p=1,
#         max_q=0,
#         max_d=0,
#         max_seasonal_p=1,
#         max_seasonal_q=0,
#         max_seasonal_d=0,
#     )
#     model.build_divisions()
#     model.run()
#     model.assess_error()
#     error_metrics = model.error_metrics.to_pandas()
#     error_metrics = error_metrics.drop(EXTRA_COLUMNS, axis=1)
#     error_metrics = error_metrics.iloc[0, :].values
#     assert all([isinstance(x, (int, float)) for x in error_metrics])
    


def test_multiple_steps_sarima():
    y = create_simulated_y()
    model = SarimaForecasting(
        y,
        filter_start_date="2022-01-01",
        n_forecasting=3,
        rolling=False,
        step_size=3,
        intersect_forecasting=False,
        max_p=1,
        max_q=0,
        max_d=0,
        max_seasonal_p=1,
        max_seasonal_q=0,
        max_seasonal_d=0,
    )
    model.build_divisions()
    model.run()
    model.assess_error()
    model.save(test_path=True)




