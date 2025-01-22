from abc import abstractmethod
from typing import Union, List
import datetime
import pandas as pd
from models.dataset import Dataset
from models.error_metrics import ErrorMetrics


MODELS_PATH = "models"


class TimeSeriesModel:
    virtual_env = "ftsf"
    python_version = "3.12.6"
    requirements_file = "requirements.txt"

    @classmethod
    def get_virtual_env(cls):
        return cls.virtual_env

    @classmethod
    def get_requirements_file_path(cls):
        return cls.requirements_file

    @classmethod
    def get_python_version(cls):
        return cls.python_version

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
    ):
        if n_forecasting is not None and forecasting_start_date is not None:
            raise ValueError(
                "Only one of 'n_forecasting' and 'forecasting_start_date' should be provided."
            )
        if only_consider_last_of_each_intersection and not intersect_forecasting:
            raise ValueError(
                "'only_consider_last_of_each_intersection' can only be True if 'intersect_forecasting' is True."
            )
        self.dataset = Dataset(y, X, filter_start_date, filter_end_date, time_frequency)
        self.n_forecasting = n_forecasting
        self.forecasting_start_date = Dataset._validate_datetime(
            forecasting_start_date, "forecasting_start_date"
        )
        self.step_size = step_size
        self.intersect_forecasting = intersect_forecasting
        self.only_consider_last_of_each_intersection = (
            only_consider_last_of_each_intersection
        )
        self.rolling = rolling
        self.error_metrics = ErrorMetrics()
        self.divisions = {}

    @classmethod
    def from_dataset(
        cls,
        dataset: Dataset,
        step_size: int,
        forecasting_start_date: Union[datetime.date, datetime.datetime] = None,
        n_forecasting=None,
        intersect_forecasting: bool = False,
        rolling: bool = False,
    ):
        new_model = cls.__new__(cls)
        new_model.dataset = dataset
        new_model.step_size = step_size
        new_model.forecasting_start_date = forecasting_start_date
        new_model.n_forecasting = n_forecasting
        new_model.intersect_forecasting = intersect_forecasting
        new_model.rolling = rolling
        new_model.error_metrics = ErrorMetrics()
        new_model.divisions = {}

    @property
    def y(self):
        return self.dataset.y

    @property
    def X(self):
        return self.dataset.X

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
            self.divisions[idx] = self.build_new_division(
                self.y, self.X, start_index, end_index
            )
            end_index = end_index - delta_index
            start_index = end_index - self.step_size + 1
            n_forecasting_left -= 1
            idx += 1
        self._reindex_divisions()

    def _reindex_divisions(self):
        max_idx = max(self.divisions.keys())
        divisions_copy = self.divisions.copy()
        for idx, division in self.divisions.items():
            new_idx = idx - max_idx
            divisions_copy[abs(new_idx)] = division
        self.divisions = dict(sorted(divisions_copy.items()))

    def get_training_div(self, idx):
        if self.divisions is None:
            raise ValueError("Divisions have not been built yet.")
        return self.divisions[idx]["training"]

    def get_forecasting_div(self, idx):
        if self.divisions is None:
            raise ValueError("Divisions have not been built yet.")
        return self.divisions[idx]["forecasting"]

    @staticmethod
    def build_new_division(y, X, start_index, end_index):
        y = y.copy()
        forecasting = {
            "forecasting": {"y": y.iloc[start_index : end_index + 1], "X": None}
        }
        forecasting = {
            "forecasting": Dataset.create_from_y(y.iloc[start_index : end_index + 1])
        }
        if X is not None:
            X = X.copy()
            forecasting = forecasting["forecasting"].set_X(
                X.iloc[start_index : end_index + 1]
            )

        training = {"training": Dataset.create_from_y(y.iloc[:start_index])}
        if X is not None:
            training["training"].set_X(X.iloc[:start_index])
        return {**training, **forecasting}

    @abstractmethod
    def fit(self, y, X):
        pass

    @abstractmethod
    def forecast(self, y, X):
        pass

    def _join_predictions(self):
        all_y_true = pd.DataFrame()
        all_y_pred = pd.DataFrame()
        for division in self.divisions.values():
            new_y_true = division["forecasting"].get_y()
            if (
                self.only_consider_last_of_each_intersection
                and self.intersect_forecasting
            ):
                new_y_true = new_y_true.iloc[-1, :]
            all_y_true = pd.concat([all_y_true, new_y_true], axis=0)

            new_y_pred = division["forecasting"].get_y_pred()
            if (
                self.only_consider_last_of_each_intersection
                and self.intersect_forecasting
            ):
                new_y_pred = new_y_pred.iloc[-1, :]
            all_y_pred = pd.concat([all_y_pred, new_y_pred], axis=0)
        return all_y_true, all_y_pred

    def assess_error(self):
        all_y_true, all_y_pred = self._join_predictions()
        self.error_metrics.calculate_error_metrics(all_y_true, all_y_pred)

    def run(self):
        for division in self.divisions.values():
            self.fit(division["training"].get_y(), division["training"].get_X())
            y_pred = self.forecast(
                division["training"].get_y(), division["forecasting"].get_X()
            )
            division["forecasting"].set_y_pred(y_pred)

    def assess_error(self):
        y_true = self.y
        y_pred = self.y_pred
        return self.error_metrics.calculate_error_metrics(y_true, y_pred)
