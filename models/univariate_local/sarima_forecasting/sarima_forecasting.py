# sarima_forecasting.py

import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from models.time_series_model import TimeSeriesModel
from typing import Union
from dataset import FREQUENCY_SEASONAL_MAP
import datetime


class SarimaForecasting(TimeSeriesModel):
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
        if time_frequency not in FREQUENCY_SEASONAL_MAP.keys():
            raise ValueError(
                f"'time_frequency' must be one of {list(FREQUENCY_SEASONAL_MAP.keys())}"
            )
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

    @TimeSeriesModel._fitted
    def fit(self, y, X=None):
        best_score = np.inf
        best_order = None
        best_seasonal_order = None

        seasonal_frequencies = FREQUENCY_SEASONAL_MAP.get(
            self.dataset.time_frequency, [0]
        )

        for p in range(self.max_p + 1):
            for d in range(self.max_d + 1):
                for q in range(self.max_q + 1):
                    for P in range(self.max_seasonal_p + 1):
                        for D in range(self.max_seasonal_d + 1):
                            for Q in range(self.max_seasonal_q + 1):
                                for m in seasonal_frequencies:
                                    try:
                                        model = SARIMAX(
                                            y,
                                            order=(p, d, q),
                                            seasonal_order=(P, D, Q, m),
                                            enforce_stationarity=False,
                                            enforce_invertibility=False,
                                        )
                                        results = model.fit(disp=False)
                                        score = (
                                            results.aic
                                            if self.selection_criterion == "aic"
                                            else results.bic
                                        )
                                        if score < best_score:
                                            best_score = score
                                            best_order = (p, d, q)
                                            best_seasonal_order = (P, D, Q, m)
                                    except Exception as e:
                                        continue

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
        forecast_df = forecast.summary_frame()["mean"]
        return pd.DataFrame(forecast_df, index=y.index, columns=["forecast"])
