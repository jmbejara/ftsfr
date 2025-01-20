from typing import Union, List
import datetime
import pandas as pd


class TimeSeriesModel:
    def __init__(
        self,
        y: Union[pd.DataFrame, pd.Series],
        X: pd.DataFrame,
        step_size: int,
        start_date: Union[datetime.date, datetime.datetime],
        filter_start_date: Union[datetime.date, datetime.datetime] = None,
        filter_end_date: Union[datetime.date, datetime.datetime] = None,
        forecasting_start_date: Union[datetime.date, datetime.datetime] = None,
        n_forecasting=None,
        intersect_forecasting: bool = False,
        rolling: bool = False,
        time_frequency="M",
    ):
        if n_forecasting is not None and forecasting_start_date is not None:
            raise ValueError(
                "Only one of 'n_forecasting' and 'forecasting_start_date' should be provided."
            )
        self.y = self.organize_time_series(
            y, filter_start_date, filter_end_date, enforce_not_none=True
        )
        self.X = self.organize_time_series(X, filter_start_date, filter_end_date)
        self.start_date = start_date
        self.n_forecasting = n_forecasting
        self.forecasting_start_date = forecasting_start_date
        self.step_size = step_size
        self.intersect_forecasting = intersect_forecasting
        self.time_frequency = time_frequency
        self.rolling = rolling
        self.divisions = {}

    @staticmethod
    def organize_time_series(
        time_series, filter_start_date, filter_end_date, enforce_not_none=False
    ):
        if time_series is None:
            if enforce_not_none:
                raise ValueError("Time series cannot be None.")
            return None
        if isinstance(time_series, pd.Series):
            time_series = time_series.to_frame()
        if "date" in list(time_series.columns.str.lower()):
            time_series = time_series.set_index("date")
        time_series.index = pd.to_datetime(time_series.index)
        time_series = time_series.sort_index()
        if filter_end_date is not None:
            time_series = time_series.loc[:filter_end_date]
        if filter_start_date is not None:
            time_series = time_series.loc[filter_start_date:]
        return time_series

    def build_divisions(self):
        end_index = len(self.y) - 1
        start_index = end_index - self.step_size + 1
        n_forecasting_left = self.n_forecasting if self.n_forecasting is not None else 0
        forecasting_start_date = (
            self.forecasting_start_date
            if self.forecasting_start_date is not None
            else self.y.index[end_index]
        )
        delta_index = 1 if self.intersect_forecasting else self.step_size
        idx = 0

        while (
            n_forecasting_left > 0
            or forecasting_start_date <= self.y.index[start_index]
        ):
            self.divisions[idx] = self.build_new_forecasting_division(
                self.y, self.X, start_index, end_index
            )
            end_index = end_index - delta_index
            start_index = end_index - self.step_size + 1
            n_forecasting_left -= 1
            idx += 1

    @staticmethod
    def build_new_division(y, X, start_index, end_index):
        y = y.copy()
        forecasting = {"forecasting": {"y": y.iloc[start_index:end_index], "X": None}}
        if X is not None:
            X = X.copy()
            forecasting = forecasting["forecasting"]["X"] = X.iloc[
                start_index:end_index
            ]
        training = {"training": {"y": y.iloc[:start_index], "X": None}}
        if X is not None:
            training["training"]["X"] = X.iloc[:start_index]
        return {**training, **forecasting}
