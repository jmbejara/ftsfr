import numpy as np
import pandas as pd
import csv
import os


PATH_ERROR_METRICS_RESULTS = "models/results/error_metrics/error_metrics.csv"
TEST_PATH_ERROR_METRICS_RESULTS = "models/results/tests/error_metrics/error_metrics.csv"
EXTRA_COLUMNS = ["model", "y", "id", "parquet_path"]


METRICS = {
    "MSE": lambda y_true, y_pred: np.mean((y_true - y_pred) ** 2),
    "RMSE": lambda y_true, y_pred: np.sqrt(np.mean((y_true - y_pred) ** 2)),
    "MAE": lambda y_true, y_pred: np.mean(np.abs(y_true - y_pred)),
    "MASE": (
        lambda y_true, y_pred: np.mean(np.abs(y_true - y_pred))
        / np.mean(np.abs(y_true - np.roll(y_true, 1)))
    ),
    "SMAPE": (
        lambda y_true, y_pred: 2
        * np.mean(np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred)))
    ),
}


class ErrorMetrics:
    def __init__(self, y_name=None, model_name=None, id=None, parquet_path=None):
        self.error_metrics = dict(zip(METRICS.keys(), [None for _ in METRICS.keys()]))
        self.id = id
        self.y_name = y_name
        self.model_name = model_name
        self.parquet_path = parquet_path

    def set_parquet_path(self, parquet_path):
        self.parquet_path = parquet_path

    def calculate_error_metrics(self, y_true, y_pred):
        organized_y_true = np.squeeze(y_true.iloc[:, 0].values)
        organized_y_pred = np.squeeze(y_pred.iloc[:, 0].values)
        self.error_metrics = {
            name: metric(organized_y_true, organized_y_pred)
            for name, metric in METRICS.items()
        }

    def get_results_file(self, test_path=False):
        file = (
            TEST_PATH_ERROR_METRICS_RESULTS if test_path else PATH_ERROR_METRICS_RESULTS
        )
        if not os.path.exists(file):
            raise FileNotFoundError(f"File '{file}' not found.")
        return pd.read_csv(file)

    def get(self):
        return self.error_metrics

    def __repr__(self):
        return str(self.to_pandas())

    def to_pandas(self):
        error_metrics_plus_info = self.error_metrics
        error_metrics_plus_info["model"] = self.model_name
        error_metrics_plus_info["y"] = self.y_name
        error_metrics_plus_info["id"] = self.id
        error_metrics_plus_info["parquet_path"] = self.parquet_path
        error_metrics_frame = pd.DataFrame(error_metrics_plus_info, index=[0])
        return error_metrics_frame[EXTRA_COLUMNS + list(METRICS.keys())]

    @classmethod
    def multiple_to_pandas(cls, list_error_metrics, reset_index: bool = True):
        if isinstance(list_error_metrics, cls):
            list_error_metrics = [list_error_metrics]
        mult_error_metrics = pd.concat(
            [error_metrics.to_pandas() for error_metrics in list_error_metrics], axis=0
        )
        if reset_index:
            mult_error_metrics.reset_index(drop=True, inplace=True)
        return mult_error_metrics

    def save(self, test_path=False):
        self._create_results_file()
        self.to_pandas().to_csv(
            path_or_buf=(
                PATH_ERROR_METRICS_RESULTS
                if not test_path
                else TEST_PATH_ERROR_METRICS_RESULTS
            ),
            mode="a",
            header=False,
            index=False,
        )

    @staticmethod
    def _create_results_file():
        if not os.path.exists(PATH_ERROR_METRICS_RESULTS):
            pd.DataFrame(columns=EXTRA_COLUMNS + list(METRICS.keys())).to_csv(
                PATH_ERROR_METRICS_RESULTS, index=False
            )
