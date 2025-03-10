# sarima_forecasting.py

import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from models.time_series_model import TimeSeriesModel
from typing import Union
from models.dataset import FREQUENCY_SEASONAL_MAP, Dataset
import datetime
from joblib import Parallel, delayed
import warnings
import itertools


def _try_sarima(params, y, selection_criterion):
    p, d, q, P, D, Q, m = params
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = SARIMAX(
                endog=y,
                order=(p, d, q),
                seasonal_order=(P, D, Q, m),
                enforce_stationarity=False,
                enforce_invertibility=False,
            )
            results = model.fit(disp=False)
        score = results.aic if selection_criterion == "aic" else results.bic
        return (score, (p, d, q), (P, D, Q, m))
    except Exception:
        return None


class SarimaForecasting(TimeSeriesModel):
    name = "SARIMA Forecasting"
    code = "SAR"

    def __init__(
        self,
        y: Union[pd.DataFrame, pd.Series],
        X: pd.DataFrame = None,
        step_size: int = 1,
        filter_start_date: Union[datetime.date, datetime.datetime, str] = None,
        filter_end_date: Union[datetime.date, datetime.datetime, str] = None,
        forecasting_start_date: Union[datetime.date, datetime.datetime, str] = None,
        n_forecasting=None,
        intersect_forecasting: bool = False,
        only_consider_last_of_each_intersection: bool = False,
        rolling: bool = False,
        time_frequency: str = None,
        order=(1, 1, 1),
        seasonal_order=(0, 0, 0, 0),
        selection_criterion="aic",
        max_p=2,
        max_q=2,
        max_d=1,
        max_seasonal_p=1,
        max_seasonal_q=1,
        max_seasonal_d=1,
    ):
        super().__init__(
            y,
            X,
            step_size,
            filter_start_date,
            filter_end_date,
            forecasting_start_date,
            n_forecasting,
            intersect_forecasting,
            only_consider_last_of_each_intersection,
            rolling,
            time_frequency,
        )
        if self.time_frequency not in FREQUENCY_SEASONAL_MAP.keys():
            raise ValueError(
                f"'time_frequency' must be one of {list(FREQUENCY_SEASONAL_MAP.keys())}"
            )
        self.order = order
        self.seasonal_order = seasonal_order
        self.selection_criterion = selection_criterion
        self.max_p = max_p
        self.max_q = max_q
        self.max_d = max_d
        self.max_seasonal_p = max_seasonal_p
        self.max_seasonal_q = max_seasonal_q
        self.max_seasonal_d = max_seasonal_d
        self.model = None
        self.fitted_model = None

    @classmethod
    def from_dataset(
        cls,
        dataset: Dataset,
        step_size: int,
        forecasting_start_date: Union[datetime.date, datetime.datetime] = None,
        n_forecasting=None,
        intersect_forecasting: bool = False,
        only_consider_last_of_each_intersection: bool = False,
        rolling: bool = False,
        order=(1, 1, 1),
        seasonal_order=(0, 0, 0, 0),
        selection_criterion="aic",
        max_p=2,
        max_q=2,
        max_d=1,
        max_seasonal_p=1,
        max_seasonal_q=1,
        max_seasonal_d=1,
    ):
        self = super().from_dataset(
            dataset,
            step_size,
            forecasting_start_date,
            n_forecasting,
            intersect_forecasting,
            only_consider_last_of_each_intersection,
            rolling,
        )
        self.order = order
        self.seasonal_order = seasonal_order
        self.selection_criterion = selection_criterion
        self.max_p = max_p
        self.max_q = max_q
        self.max_d = max_d
        self.max_seasonal_p = max_seasonal_p
        self.max_seasonal_q = max_seasonal_q
        self.max_seasonal_d = max_seasonal_d
        self.model = None
        self.fitted_model = None
        return self

    @TimeSeriesModel._fitted
    def fit(self, y, X=None):
        best_score = np.inf
        best_order = None
        best_seasonal_order = None

        seasonal_frequencies = FREQUENCY_SEASONAL_MAP[self.time_frequency]

        param_combinations = list(
            itertools.product(
                range(self.max_p + 1),
                range(self.max_d + 1),
                range(self.max_q + 1),
                range(self.max_seasonal_p + 1),
                range(self.max_seasonal_d + 1),
                range(self.max_seasonal_q + 1),
                seasonal_frequencies,
            )
        )

        results = Parallel(n_jobs=-1)(
            delayed(_try_sarima)(params, y, self.selection_criterion)
            for params in param_combinations
        )

        valid_results = [res for res in results if res is not None]

        if not valid_results:
            raise Exception("No valid SARIMA model found with the given parameters.")

        best_score, best_order, best_seasonal_order = min(valid_results, key=lambda x: x[0])

        self.order = best_order
        self.seasonal_order = best_seasonal_order

        self.model = SARIMAX(
            y,
            order=self.order,
            seasonal_order=self.seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False,
        )
        self.fitted_model = self.model.fit(disp=False)

    def forecast(self, y, X=None):
        forecast_length = len(y)
        if not self.fitted_model:
            raise ValueError("The model must be fitted before forecasting.")
        forecast = self.fitted_model.get_forecast(steps=forecast_length)
        forecast_df = forecast.summary_frame()["mean"].iloc[-forecast_length:].values
        return pd.DataFrame(forecast_df, index=y.index, columns=["forecast"])
