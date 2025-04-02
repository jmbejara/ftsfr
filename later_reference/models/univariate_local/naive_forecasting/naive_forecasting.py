import numpy as np
import pandas as pd

from models.time_series_model import TimeSeriesModel


class NaiveForecasting(TimeSeriesModel):
    name = "Naive Forecasting"
    code = "NAI"

    @TimeSeriesModel._fitted
    def fit(self, y, X=None):
        self.prediction = y.iloc[-1, 0]

    def forecast(self, y, X=None):
        return pd.DataFrame(
            np.repeat(self.prediction, len(y.index)), index=y.index, columns=y.columns
        )
