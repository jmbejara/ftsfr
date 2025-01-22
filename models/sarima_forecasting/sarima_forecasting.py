# sarima_forecasting.py

import datetime
from typing import Union
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from models.time_series_model import TimeSeriesModel


class SarimaForecasting(TimeSeriesModel):
    virtual_env = "ftsf"
    python_version = "3.12.6"
    requirements_file = "requirements.txt"

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
        order=(1, 1, 1),
        seasonal_order=(0, 0, 0, 0),
        selection_criterion="aic",
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
        )
        self.order = order
        self.seasonal_order = seasonal_order
        self.selection_criterion = selection_criterion
        self.model = None
        self.fitted_model = None

    def fit(self, y, X=None):
        best_score = np.inf
        best_order = None
        best_seasonal_order = None
        for p in range(3):
            for d in range(2):
                for q in range(3):
                    for P in range(2):
                        for D in range(2):
                            for Q in range(2):
                                for m in [0, 12]:  # Monthly seasonal order
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
