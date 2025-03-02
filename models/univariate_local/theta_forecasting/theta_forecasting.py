import pandas as pd
import numpy as np
from models.time_series_model import TimeSeriesModel
from statsmodels.tsa.holtwinters import SimpleExpSmoothing


class ThetaForecasting(TimeSeriesModel):
    name = "Theta Forecasting"
    code = "THE"

    @TimeSeriesModel._fitted
    def fit(self, y, X=None):
        self.base_model = SimpleExpSmoothing(y.values).fit()

    def forecast(self, y, X=None):
        forecast_values = self.base_model.forecast(len(y))
        return pd.DataFrame(forecast_values, index=y.index, columns=y.columns)
