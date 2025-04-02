import pandas as pd
import numpy as np
from models.time_series_model import TimeSeriesModel


class MeanForecasting(TimeSeriesModel):
    name = "Mean Forecasting"
    code = "MEA"

    @TimeSeriesModel._fitted
    def fit(self, y, X=None):
        self.prediction = y.iloc[:, :].dropna().values.mean()

    def forecast(self, y, X=None):
        return pd.DataFrame(
            np.repeat(self.prediction, len(y.index)), index=y.index, columns=y.columns
        )
