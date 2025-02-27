from abc import abstractmethod
import random
from typing import Union, List
import datetime
import pandas as pd
from models.dataset import Dataset
from models.error_metrics import ErrorMetrics
import os


MODELS_PATH = "models"
PATH_TIME_SERIES_MODELS_RESULTS = (
    "models/results/time_series_models/time_series_models.csv"
)
TEST_PATH_TIME_SERIES_MODELS_RESULTS = (
    "models/results/tests/time_series_models/time_series_models.csv"
)

DATE_COLUMNS = [
    "forecasting_start_date",
    "forecasting_last_date",
    "training_first_date",
]


class TimeSeriesModel:
    name = "Time Series Abstract Model"
    code = "TSA"
    virtual_env = "ftsf"
    python_version = "3.12.6"
    requirements_file = "requirements.txt"
    run_code = None

    @staticmethod
    def _fitted(fit_func):
        def wrapper(self, y, X=None):
            fit_func(self, y, X)
            self.is_fitted = True

        return wrapper

    def get_model_name(self):
        return self.name

    def get_model_code(self):
        return self.code

    @classmethod
    def get_virtual_env(cls):
        return cls.virtual_env

    @classmethod
    def get_requirements_file_path(cls):
        return cls.requirements_file

    def _get_run_code(self):
        if self.__class__.run_code is None:
            self.__class__.run_code = f"{random.randint(1, 9999):04d}"
        return self.__class__.run_code

    @classmethod
    def get_python_version(cls):
        return cls.python_version

    def _create_id(self):
        time = datetime.datetime.now(datetime.timezone(offset=datetime.timedelta(0)))
        run_code = self._get_run_code()
        code = self.get_model_code()
        if code is None or not isinstance(code, str):
            raise ValueError("Model code must be a string.")
        return f"R{run_code}M{code}D{time.strftime('%Y%m%d%H%M%S%f')}"

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
        self.base_model = None
        self.id = self._create_id()
        self.is_error_assessed = False
        self.is_div_built
        self.is_fitted = False
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
        self.error_metrics = ErrorMetrics(
            model_name=self.get_model_name(),
            y_name=self.dataset.y.columns[0],
            id=self.id,
        )
        self.divisions = {}

    @classmethod
    def from_dataset(
        cls,
        dataset: Dataset,
        step_size: int,
        forecasting_start_date: Union[datetime.date, datetime.datetime] = None,
        n_forecasting=None,
        intersect_forecasting: bool = False,
        only_consider_last_of_each_intersection: bool = False,
        rolling: bool = False,
    ):
        new_model = cls.__new__(cls)
        new_model.base_model = None
        new_model.id = new_model._create_id()
        new_model.is_error_assessed = False
        new_model.is_div_built = False
        new_model.is_fitted = False
        new_model.dataset = dataset
        new_model.step_size = step_size
        new_model.forecasting_start_date = forecasting_start_date
        new_model.n_forecasting = n_forecasting
        new_model.intersect_forecasting = intersect_forecasting
        new_model.only_consider_last_of_each_intersection = (
            only_consider_last_of_each_intersection
        )
        new_model.rolling = rolling
        new_model.error_metrics = ErrorMetrics(
            model_name=new_model.get_model_name(),
            y_name=new_model.dataset.y.columns[0],
            id=new_model.id,
            parquet_path=new_model.dataset.get_parquet_path(),
        )
        new_model.divisions = {}
        return new_model

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
        self.is_div_built = True

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
                division["forecasting"].get_y(), division["forecasting"].get_X()
            )
            division["forecasting"].set_y_pred(y_pred)
        self.y_pred = pd.DataFrame()
        for division in self.divisions.values():
            self.y_pred = pd.concat(
                [self.y_pred, division["forecasting"].get_y_pred()], axis=0
            )

    def assess_error(self):
        y_true = self.y
        y_pred = self.y_pred
        y_true = y_true.loc[lambda s: s.index.isin(y_pred.index)]
        self.error_metrics.calculate_error_metrics(y_true, y_pred)
        self.is_error_assessed = True

    def to_pandas(self):
        last_division = max(self.divisions.keys())
        info = {
            "model": self.get_model_name(),
            "id": self.id,
            "y": self.dataset.y.columns[0],
            "parquet_path": self.dataset.get_parquet_path(),
            "time_frequency": self.dataset.time_frequency,
            "step_size": self.step_size,
            "forecasting_start_date": self.divisions[0]["forecasting"].get_y().index[0],
            "forecasting_last_date": self.divisions[last_division]["forecasting"]
            .get_y()
            .index[-1],
            "training_first_date": self.divisions[0]["training"].get_y().index[0],
            "n_obs": len(self.dataset.get_y()),
            "n_forecasting": len(self.divisions.values()),
            "intersect_forecasting": self.intersect_forecasting,
            "only_consider_last_of_each_intersection": self.only_consider_last_of_each_intersection,
            "rolling": self.rolling,
        }
        return pd.DataFrame(info, index=[0])

    def is_it_already_in_results(self, test_path=False, not_check_cols=["id"]):
        if self.is_div_built is False:
            raise ValueError(
                "Divisions have not been built yet. Use 'build_divisions' method before assessing if results already exist."
            )
        if isinstance(not_check_cols, str):
            not_check_cols = [not_check_cols]
        if not os.path.exists(PATH_TIME_SERIES_MODELS_RESULTS):
            return False
        results = (
            pd.read_csv(TEST_PATH_TIME_SERIES_MODELS_RESULTS, parse_dates=DATE_COLUMNS)
            if test_path
            else pd.read_csv(PATH_TIME_SERIES_MODELS_RESULTS, parse_dates=DATE_COLUMNS)
        )
        if results.empty:
            return False
        current_result = self.to_pandas()
        for col in current_result.columns:
            if col in not_check_cols:
                continue
            if "date" == col[:4]:
                # convert to date
                results = results.loc[
                    lambda df: pd.to_datetime(df[col])
                    == pd.to_datetime(current_result[col].iloc[0]),
                    :,
                ]
            results = results.loc[lambda df: df[col] == current_result[col].iloc[0], :]
            if results.empty:
                return False
        return True

    def get_error_metrics(self):
        if not self.is_error_assessed:
            self.assess_error()
        return self.error_metrics.get()

    def get_error_metrics_frame(self):
        if not self.is_error_assessed:
            self.assess_error()
        return self.error_metrics.to_pandas()

    def save(self, save_error_metrics=True, test_path=False):
        self._create_results_file()
        self.to_pandas().to_csv(
            path_or_buf=(
                PATH_TIME_SERIES_MODELS_RESULTS
                if not test_path
                else TEST_PATH_TIME_SERIES_MODELS_RESULTS
            ),
            mode="a",
            header=False,
            index=False,
        )
        if save_error_metrics:
            self.error_metrics.set_parquet_path(self.dataset.get_parquet_path())
            self.error_metrics.save(test_path=test_path)

    @classmethod
    def get_results_file(cls, test_path=False):
        file = (
            TEST_PATH_TIME_SERIES_MODELS_RESULTS
            if test_path
            else PATH_TIME_SERIES_MODELS_RESULTS
        )
        if not os.path.exists(file):
            raise FileNotFoundError(f"File '{file}' not found.")
        return pd.read_csv(file, parse_dates=DATE_COLUMNS)

    @classmethod
    def get_error_metrics_file(cls, test_path=False):
        return ErrorMetrics.get_results_file(test_path=test_path)

    def _create_results_file(self):
        if not os.path.exists(PATH_TIME_SERIES_MODELS_RESULTS):
            columns = list(self.to_pandas().columns)
            pd.DataFrame(columns=columns).to_csv(
                PATH_TIME_SERIES_MODELS_RESULTS, index=False
            )
