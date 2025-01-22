import pandas as pd
import numpy as np
from models.time_series_model import TimeSeriesModel


class NaiveForecasting(TimeSeriesModel):

    def fit(self, y, X=None):
        self._prediction = y.iloc[:, -1].values

    def forecast(self, y, X=None):
        return pd.DataFrame(
            np.repeat(self._prediction, len(y.index)), index=y.index, columns=y.columns
        )
