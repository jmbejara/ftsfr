"""
The NixtlaMain class can help quickly create the necessary objects for 
forecasting with Nixtla's neuralforecast models.

NOTE: Currently doesn't support training on MPS.
"""
import os
import traceback
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from tabulate import tabulate
import torch
from darts import TimeSeries
from darts.metrics import mase
from neuralforecast import NeuralForecast

from .forecasting_model import forecasting_model
from .helper_func import calculate_darts_MASE

# TODO: Need to add logging
# TODO: Make a decorator for error handling

class NixtlaMain(forecasting_model):
    def __init__(self,
                 estimator,
                 model_name,
                 test_split,
                 frequency,
                 seasonality,
                 data_path,
                 output_path):
        
        dataset_name = str(os.path.basename(data_path)).split(".")[0]
        dataset_name = dataset_name.removeprefix("ftsfr_")

        # Path to save model
        model_path = output_path / "models" / model_name / dataset_name
        Path(model_path).mkdir(parents = True, exist_ok = True)

        # Path to save forecasts
        forecast_path = output_path / "forecasts" / model_name / dataset_name
        Path(forecast_path).mkdir(parents = True, exist_ok = True)
        forecast_path = forecast_path / "forecasts.parquet"

        result_path = output_path / "raw_results" / model_name
        result_path.mkdir(parents = True, exist_ok = True)
        result_path = result_path / str(dataset_name + ".csv")

        df = pd.read_parquet(data_path).rename(columns = {"id" : 'unique_id'})
        df = df.interpolate()

        unique_dates = np.unique(df["ds"].values)
        test_length = int(test_split * len(unique_dates))
        test_data = df[df.ds >= unique_dates[-test_length]]
        train_data = df[df.ds < unique_dates[-test_length]]

        # Names
        self.dataset_name = dataset_name
        self.model_name = model_name

        # Paths
        self.forecast_path = forecast_path
        self.dataset_path = data_path
        self.model_path = str(model_path)
        self.result_path = result_path

        # Dataframes
        self.raw_series = df
        self.train_series = train_data
        self.test_series = test_data
        self.pred_series = None

        # Important variables
        self.seasonality = seasonality
        self.frequency = frequency
        
        # Model related variables
        # Stores base class
        # MPS is causing buffer errors
        if torch.backends.mps.is_available():
            if torch.cuda.is_available():
                self.estimator = estimator(h = 1, 
                                           input_size = seasonality * 4, 
                                           accelerator = "gpu")
            else:
                self.estimator = estimator(h = 1, 
                                           input_size = seasonality * 4, 
                                           accelerator = "cpu")
        else:
            self.estimator = estimator(h = 1, input_size = seasonality * 4)
        # Stores the nf object
        self.nf = NeuralForecast(models = [self.estimator], freq = frequency)

        # Error metrics
        self.errors = defaultdict(float)

        print("Object Initialized:")
        print(tabulate([["Model", model_name],
                        ["Dataset", dataset_name],
                        ["Total Entities", len(df["unique_id"].unique())]],
                        tablefmt="fancy_grid"))

    def train(self):
        try:
            self.nf.fit(df = self.train_series)
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in {self.model_name} training." +
                  "Full traceback above \u2191")
            self.print_sep()
            return None
    
    def save_model(self):
        try:
            self.nf.save(self.model_path,
                        model_index = None,
                        overwrite = True,
                        save_dataset = False)
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in saving {self.model_name}. " +
                  "Full traceback above \u2191")
            self.print_sep()
            return None

    def load_model(self):
        try:
            self.nf = NeuralForecast.load(path = str(self.model_path))
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in loading {self.model_name}. " +
                  "Full traceback above \u2191")
            self.print_sep()
            return None

    def forecast(self):
        try:
            pred_series = self.nf.predict(self.train_series)
            pred_series["ds"] = self.test_series["ds"].unique()[0]
            df = self.raw_series

            for i in self.test_series["ds"].unique()[1:]:
                # Get predictions
                temp_pred_series = self.nf.predict(df[df.ds < i])
                # Lining up the dates
                temp_pred_series['ds'] = i
                pred_series = pd.concat([pred_series, temp_pred_series], 
                                        ignore_index = True)
            
            self.pred_series = pred_series
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in {self.model_name} forecasting." +
                  " Full traceback above \u2191")
            self.print_sep()
            return None

    
    def save_forecast(self):
        try:
            self.pred_series.to_parquet(self.forecast_path, engine = "pyarrow")
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in saving {self.model_name} forecasts. " +
                  "Full traceback above \u2191")
            self.print_sep()
            return None

    def load_forecast(self):
        try:
            temp_df = pd.read_parquet(self.forecast_path)
            self.pred_series = TimeSeries.from_dataframe(temp_df, 
                                                         time_col = "ds")
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in saving {self.model_name} forecasts. " +
                  "Full traceback above \u2191")
            self.print_sep()
            return None
    
    def calculate_error(self, metric = "MASE"):
        if metric == "MASE":
            try:
                self.errors["MASE"] = calculate_darts_MASE(self.test_series,
                                                           self.train_series,
                                                           self.pred_series,
                                                           self.seasonality,
                                                           self.model_name.title())
                return self.errors["MASE"]
            except Exception:
                self.print_sep()
                print(traceback.format_exc())
                print(f"\nError in {self.model_name} MASE calculation. " +
                      "Full traceback above \u2191")
                self.print_sep()
                return None
        else:
            raise ValueError('Metric not supported.')
    
    def print_summary(self):
        print(tabulate([
            ["Model", self.model_name],
            ["Dataset", self.dataset_name],
            ["Entities", len(self.train_series["unique_id"].unique())],
            ["Frequency", self.frequency],
            ["Seasonality", self.seasonality],
            ["Global MASE", self.errors["MASE"]]
            ], tablefmt="fancy_grid"))
    
    def save_results(self):
        try:
            forecast_res = pd.DataFrame(
                {
                    "Model" : [self.model_name],
                    "Dataset" : [self.dataset_name],
                    "Entities" : [len(self.train_series["unique_id"].unique())],
                    "Frequency" : [self.frequency],
                    "Seasonality" : [self.seasonality],
                    "Global MASE" : [self.errors["MASE"]]
                }
            )
            forecast_res.to_csv(self.result_path)
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in saving {self.model_name} results." +
                  "Full traceback above \u2191")
            self.print_sep()
            return None