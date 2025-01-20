import numpy as np


METRICS = {
    "MSE": lambda y_true, y_pred: np.mean((y_true - y_pred) ** 2),
    "RMSE": lambda y_true, y_pred: np.sqrt(np.mean((y_true - y_pred) ** 2)),
    "MAE": lambda y_true, y_pred: np.mean(np.abs(y_true - y_pred)),
    "MASE": lambda y_true, y_pred: np.mean(np.abs(y_true - y_pred))
    / np.mean(np.abs(y_true - np.roll(y_true, 1))),
    "SMAPE": lambda y_true, y_pred: 2
    * np.mean(np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))),
}


class ErrorMetrics:
    def __init__(self):
        self.error_metrics = dict(zip(METRICS.keys(), [None for _ in METRICS.keys()]))

    def calculate_error_metrics(self, y_true, y_pred):
        organized_y_true = np.squeeze(y_true.iloc[:, 0].values)
        organized_y_pred = np.squeeze(y_pred.iloc[:, 0].values)
        self.error_metrics = {
            name: metric(organized_y_true, organized_y_pred)
            for name, metric in METRICS.items()
        }
