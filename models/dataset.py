from typing import Union, List
import datetime
import pandas as pd
from models.utils import _calc_periods_per_year


FREQUENCY_SEASONAL_MAP = {
    "DU": [5, 20, 21, 22, 42, 63],
    "D": [7, 30],
    "W": [4, 13, 26, 52],
    "ME": [3, 4, 6, 12],
    "BQ": [3, 4, 6, 12],
    "BA": [2, 4, 6, 10],
    "A": [1, 2, 3],
}


PATH_DATA_OUTPUT = "_data"


class Dataset:
    all_tables = {}

    @classmethod
    def get_in_memory_tables(cls):
        return cls.all_tables

    @classmethod
    def reset_tables_in_memory(cls):
        cls.all_tables = {}

    @classmethod
    def get_in_memory_tables_names(cls):
        return list(cls.all_tables.keys())

    @classmethod
    def get_table_from_memory(cls, table_name):
        if table_name.endswith(".parquet"):
            table_name = table_name[:-8]
        table = cls.all_tables.get(table_name)
        if table is None:
            table = cls.all_tables.get(PATH_DATA_OUTPUT + "/" + table_name)
        if table is None:
            raise ValueError(f"Table {table_name} not found in memory")
        return table

    @classmethod
    def from_parquet(
        cls,
        y,
        X=None,
        filter_start_date: Union[datetime.date, datetime.datetime] = None,
        filter_end_date: Union[datetime.date, datetime.datetime] = None,
        time_frequency=None,
        parquet_path=None,
    ):
        if parquet_path is not None:
            y = cls._get_variable(y, return_path=False)
        else:
            y, parquet_path = cls._get_variable(y, return_path=True)
        if X is None:
            X_frame = None
        else:
            if isinstance(X, str):
                X = [X]
            X_frame = pd.DataFrame()
            for x in X:
                X_frame = X_frame.join(cls._get_variable(x), how="outer")
        return cls(
            y, X_frame, filter_start_date, filter_end_date, time_frequency, parquet_path
        )

    @classmethod
    def from_parquet_all_from_table(
        cls,
        y_table,
        X=None,
        filter_start_date: Union[datetime.date, datetime.datetime] = None,
        filter_end_date: Union[datetime.date, datetime.datetime] = None,
        time_frequency=None,
        ignore_columns: List[str] = [],
    ):
        path_name = PATH_DATA_OUTPUT + "/" + y_table
        if cls.all_tables.get(path_name) is None:
            cls.all_tables[path_name] = pd.read_parquet(path_name + ".parquet")
        datasets_from_table = []
        for y in list(cls.all_tables[path_name].columns):
            if y.lower() in ignore_columns or y.lower() == "date":
                continue
            new_dataset = cls.from_parquet(
                y_table + "/" + y, X, filter_start_date, filter_end_date, time_frequency
            )
            new_dataset.parquet_path = path_name
            datasets_from_table.append(new_dataset)
        return datasets_from_table

    def get_parquet_path(self):
        return self.parquet_path

    def get_y_name(self):
        if isinstance(self.y, pd.DataFrame):
            return (
                '"["' + '", "'.join(list(self.y.columns)) + '"]"'
                if len(self.y.columns) > 1
                else '"' + self.y.columns[0] + '"'
            )
        else:
            return self.y.name

    @classmethod
    def _get_variable(cls, path, return_path=False):
        variable_name = path.split("/")[-1].split("\\")[-1]
        path_name = PATH_DATA_OUTPUT + "/" + "/".join(path.split("/")[:-1])
        if cls.all_tables.get(path_name) is None:
            cls.all_tables[path_name] = pd.read_parquet(path_name + ".parquet")
        if variable_name in cls.all_tables[path_name].columns:
            variable = cls.all_tables[path_name][variable_name]
            if "date" in list(cls.all_tables[path_name].columns.str.lower()):
                variable.index = cls.all_tables[path_name]["date"]
            if not return_path:
                return variable
            else:
                return variable, path_name
        else:
            raise ValueError(f"Variable {variable_name} not found in {path_name}")

    def __init__(
        self,
        y,
        X,
        filter_start_date: Union[datetime.date, datetime.datetime] = None,
        filter_end_date: Union[datetime.date, datetime.datetime] = None,
        time_frequency=None,
        parquet_path=None,
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
        self.parquet_path = parquet_path

    def _validate_time_frequency(self, time_frequency):
        if time_frequency == "M":
            return "ME"
        if time_frequency is not None and time_frequency not in list(
            FREQUENCY_SEASONAL_MAP.keys()
        ):
            raise ValueError(
                f"'time_frequency' must be one of {list(FREQUENCY_SEASONAL_MAP.keys())} or None"
            )
        elif time_frequency is None:
            time_frequency = _calc_periods_per_year(list(self.y.index))
        return time_frequency

    def __len__(self):
        return len(self.y)

    def __repr__(self):
        return f"Dataset(y={self.get_y_name()}, len={len(self.y.index)}, time_frequency={self.time_frequency})"

    def print(self):
        return pd.concat([self.y, self.X], axis=1).to_string()

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

    def get_last_y_date(self):
        return self.y.index[-1]

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
        index_counts = (
            time_series.index.value_counts()
            .sort_values(ascending=False)
            .loc[lambda df: df.values > 1]
        )
        if len(index_counts) > 0:
            not_unique_indexes = index_counts.index.to_list()
            if len(not_unique_indexes) > 10:
                not_unique_indexes = not_unique_indexes[:9] + ["..."]
            not_unique_indexes = ", ".join(not_unique_indexes)
            raise ValueError(
                f"Time series index contains non-unique values: {not_unique_indexes}"
            )
        time_series = time_series.sort_index()
        if filter_end_date is not None:
            time_series = time_series.loc[:filter_end_date]
        if filter_start_date is not None:
            time_series = time_series.loc[filter_start_date:]
        return time_series
