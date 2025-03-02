import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from models.time_series_model import TimeSeriesModel
from typing import Union, Dict, Any, List
from models.dataset import Dataset
import datetime
import itertools


PARAM_GRID_DEFAULT = {
    "hidden_size": [32, 64],
    "num_layers": [1, 2, 3, 5],
    "epochs": [100, 200],
    "learning_rate": [0.001, 0.01, 0.05],
    "batch_size": [16],
}


class LstmForecasting(TimeSeriesModel):
    name = "Long Short Term Memory"
    code = "LST"

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
        n_splits: int = 3,
        param_grid: Dict[str, List[Any]] = None,
    ):
        """
        A minimal LSTM-based model that uses time-series cross-validation to tune hyperparameters.

        :param n_splits: Number of time-series cross-validation splits.
        :param param_grid: A dictionary specifying the hyperparameter grid to search.
        """
        super().__init__(
            y,
            X,
            step_size,
            filter_start_date,
            filter_end_date,
            forecasting_start_date,
            n_forecasting,
            intersect_forecasting,
            only_consider_last_of_each_intersection,
            rolling,
            time_frequency,
        )
        self.n_splits = n_splits
        self.param_grid = PARAM_GRID_DEFAULT if param_grid is None else param_grid
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.best_params = None
        self.model = None

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
        n_splits: int = 3,
        param_grid: Dict[str, List[Any]] = None,
    ):
        self = super().from_dataset(
            dataset,
            step_size,
            forecasting_start_date,
            n_forecasting,
            intersect_forecasting,
            only_consider_last_of_each_intersection,
            rolling,
        )
        self.param_grid = PARAM_GRID_DEFAULT if param_grid is None else param_grid
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.best_params = None
        self.model = None
        return self

    def _time_series_splits(self, series_length: int, n_splits: int):
        """
        Generate time-series splits (train, val) indices for cross-validation.
        """
        # We'll keep it straightforward: each fold will be train up to (fold_end) and val for next chunk
        fold_size = series_length // (n_splits + 1)
        for i in range(n_splits):
            # training from 0 to fold_end_i
            fold_end = (i + 1) * fold_size
            train_end = fold_end
            # validation from fold_end_i to fold_end_{i+1}
            val_end = (
                (i + 2) * fold_size if (i + 2) <= (n_splits + 1) else series_length
            )
            yield (0, train_end), (train_end, val_end)

    def _build_lstm_model(self, input_size, hidden_size, num_layers):
        class LSTM(nn.Module):
            def __init__(self, input_size, hidden_size, num_layers):
                super(LSTM, self).__init__()
                self.hidden_size = hidden_size
                self.num_layers = num_layers
                self.lstm = nn.LSTM(
                    input_size, hidden_size, num_layers, batch_first=True
                )
                self.fc = nn.Linear(hidden_size, 1)

            def forward(self, x):
                h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(
                    x.device
                )
                c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(
                    x.device
                )
                out, _ = self.lstm(x, (h0, c0))
                out = self.fc(out[:, -1, :])
                return out

        return LSTM(input_size, hidden_size, num_layers).to(self.device)

    def _train_one_epoch(self, model, train_loader, optimizer, criterion):
        model.train()
        for batch in train_loader:
            inputs = batch[0].to(self.device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, inputs[:, -1, :])
            loss.backward()
            optimizer.step()

    def _evaluate(self, model, val_data):
        model.eval()
        with torch.no_grad():
            outputs = model(val_data)
            mse = nn.MSELoss()(outputs, val_data[:, -1, :])
        return mse.item()

    def _train_model_cv(
        self, y_tensor, hidden_size, num_layers, epochs, lr, batch_size
    ):
        # Perform time-series CV
        series_len = y_tensor.shape[0]
        mses = []
        for (train_start, train_end), (val_start, val_end) in self._time_series_splits(
            series_len, self.n_splits
        ):
            # Build new model each fold
            model = self._build_lstm_model(1, hidden_size, num_layers)
            optimizer = torch.optim.Adam(model.parameters(), lr=lr)
            criterion = nn.MSELoss()

            # Split train, val
            y_train = y_tensor[train_start:train_end]
            y_val = y_tensor[val_start:val_end]

            # Create DataLoader for train
            train_loader = DataLoader(
                TensorDataset(y_train), batch_size=batch_size, shuffle=False
            )

            for _ in range(epochs):
                self._train_one_epoch(model, train_loader, optimizer, criterion)

            # Evaluate on val
            if len(y_val) > 0:
                mse = self._evaluate(model, y_val)
                mses.append(mse)
            else:
                # If no validation data is left, skip
                pass

        return np.mean(mses) if len(mses) > 0 else np.inf

    def _select_best_params(self, y_tensor):
        # Grid search over self.param_grid
        best_score = np.inf
        best_combo = None
        keys = list(self.param_grid.keys())
        for values in itertools.product(*(self.param_grid[k] for k in keys)):
            combo = dict(zip(keys, values))
            hidden_size = combo.get("hidden_size")
            num_layers = combo.get("num_layers")
            epochs = combo.get("epochs")
            lr = combo.get("learning_rate")
            batch_size = combo.get("batch_size")

            score = self._train_model_cv(
                y_tensor,
                hidden_size=hidden_size,
                num_layers=num_layers,
                epochs=epochs,
                lr=lr,
                batch_size=batch_size,
            )

            if score < best_score:
                best_score = score
                best_combo = combo
        return best_combo, best_score

    @TimeSeriesModel._fitted
    def fit(self, y, X=None):
        # Convert y to torch
        y_tensor = (
            torch.tensor(y.values, dtype=torch.float32).view(-1, 1, 1).to(self.device)
        )
        # Find best params
        self.best_params, best_score = self._select_best_params(y_tensor)
        # Now train final model on entire training set
        hidden_size = self.best_params.get("hidden_size")
        num_layers = self.best_params.get("num_layers")
        epochs = self.best_params.get("epochs")
        lr = self.best_params.get("learning_rate")
        batch_size = self.best_params.get("batch_size")

        self.model = self._build_lstm_model(1, hidden_size, num_layers)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        criterion = nn.MSELoss()

        train_loader = DataLoader(
            TensorDataset(y_tensor), batch_size=batch_size, shuffle=False
        )
        for _ in range(epochs):
            self._train_one_epoch(self.model, train_loader, optimizer, criterion)

    def forecast(self, y, X=None):
        if self.model is None:
            raise ValueError("Model must be fitted before forecasting.")
        y_test = (
            torch.tensor(y.values, dtype=torch.float32).view(-1, 1, 1).to(self.device)
        )
        self.model.eval()
        with torch.no_grad():
            forecast_values = self.model(y_test).cpu().numpy()
        return pd.DataFrame(forecast_values, index=y.index, columns=y.columns)
