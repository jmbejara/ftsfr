from typing import Union, List
import datetime
import pandas as pd


TIME_FREQUENCY_OPTIONS = ["D", "DU", "W", "M", "Q", "Y"]


class Dataset:
    def __init__(
        self,
        y,
        X,
        filter_start_date: Union[datetime.date, datetime.datetime] = None,
        filter_end_date: Union[datetime.date, datetime.datetime] = None,
        time_frequency=None,
    ):
        self.y = self.organize_time_series(
            y,
            self._validate_datetime(filter_start_date, "filter_start_date"),
            self._validate_datetime(filter_end_date, "filter_end_date"),
            enforce_not_none=True,
        )
        self.X = self.organize_time_series(X, filter_start_date, filter_end_date)
        self.time_frequency = self._validate_time_frequency(time_frequency)
        self.y_pred = None

    @staticmethod
    def _validate_time_frequency(time_frequency):
        if time_frequency is not None and time_frequency not in TIME_FREQUENCY_OPTIONS:
            raise ValueError(
                f"'time_frequency' must be one of {TIME_FREQUENCY_OPTIONS} or None"
            )
        return time_frequency

    def __len__(self):
        return len(self.y)

    @classmethod
    def from_organized_time_series(cls, y, X, time_frequency=None):
        # Not using __init__ to avoid reorganizing the time series
        new_dataset = cls.__new__(cls)
        new_dataset.y = y
        new_dataset.X = X
        new_dataset.time_frequency = time_frequency
        return new_dataset

    @staticmethod
    def _validate_datetime(date, date_name):
        if isinstance(date, str):
            return pd.to_datetime(date)
        elif (
            isinstance(date, datetime.date)
            or isinstance(date, datetime.datetime)
            or date is None
        ):
            return date
        else:
            raise ValueError(
                f"'{date_name}' must be a string, datetime.date, datetime.datetime, None"
            )

    @classmethod
    def create_from_y(cls, y, time_frequency=None):
        return cls.from_organized_time_series(y, None, time_frequency)

    def set_X(self, X):
        self.X = self.organize_time_series(
            X, filter_start_date=self.y.index[0], filter_end_date=self.y.index[-1]
        )

    def get_y(self):
        return self.y

    def get_X(self):
        return self.X

    def set_y_pred(self, y_pred, organize=False):
        if organize:
            self.y_pred = self.organize_time_series(
                y_pred,
                filter_start_date=self.y.index[0],
                filter_end_date=self.y.index[-1],
            )
        self.y_pred = y_pred

    def get_y_pred(self):
        return self.y_pred

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
        time_series.columns = time_series.columns.map(lambda x: str(x))
        if "date" in list(time_series.columns.str.lower()):
            time_series = time_series.set_index("date")
        time_series.index = pd.to_datetime(time_series.index)
        time_series = time_series.sort_index()
        if filter_end_date is not None:
            time_series = time_series.loc[:filter_end_date]
        if filter_start_date is not None:
            time_series = time_series.loc[filter_start_date:]
        return time_series
