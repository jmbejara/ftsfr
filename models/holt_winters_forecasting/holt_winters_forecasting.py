# holt_winters_forecasting.py

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from models.time_series_model import TimeSeriesModel
from dataset import FREQUENCY_SEASONAL_MAP


class HoltWintersForecasting(TimeSeriesModel):
    def __init__(
        self,
        y: pd.DataFrame,
        X: pd.DataFrame = None,
        step_size: int = 1,
        filter_start_date=None,
        filter_end_date=None,
        forecasting_start_date=None,
        n_forecasting=None,
        intersect_forecasting: bool = False,
        only_consider_last_of_each_intersection: bool = False,
        rolling: bool = False,
        time_frequency: str = None,
        seasonal: str = "add",
        trend: str = "add",
        damped_trend: bool = False,
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
        self.seasonal = seasonal
        self.trend = trend
        self.damped_trend = damped_trend
        self.model = None
        self.fitted_model = None

    def fit(self, y, X=None):
        seasonal_periods = self._get_seasonal_periods()
        self.model = ExponentialSmoothing(
            y.iloc[:, 0].values,
            seasonal=self.seasonal,
            trend=self.trend,
            damped_trend=self.damped_trend,
            seasonal_periods=seasonal_periods,
        )
        self.fitted_model = self.model.fit()

    def forecast(self, y, X=None):
        if not self.fitted_model:
            raise ValueError("The model must be fitted before forecasting.")
        forecast_length = len(y)
        forecast_values = self.fitted_model.forecast(forecast_length)
        return pd.DataFrame(
            forecast_values,
            index=y.index,
            columns=["forecast"],
        )

    def _get_seasonal_periods(self):
        seasonal_periods_list = FREQUENCY_SEASONAL_MAP.get(
            self.dataset.time_frequency, []
        )
        if not seasonal_periods_list:
            raise ValueError(
                f"Unsupported time frequency '{self.dataset.time_frequency}'."
            )
        return max(seasonal_periods_list)
