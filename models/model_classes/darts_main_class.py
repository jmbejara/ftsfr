"""
This contains classes to directly inherit into a model class.

Expected behaviour is that each new object is created for a unique model
and data pair.
"""
import os
import traceback
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from darts.metrics import mase
from darts.utils.missing_values import fill_missing_values
from darts.utils.model_selection import train_test_split
from tabulate import tabulate

from .forecasting_model import forecasting_model


class DartsMain(forecasting_model):
    def __init__(self,
                 estimator,
                 model_name,
                 test_split,
                 frequency,
                 seasonality,
                 data_path,
                 output_path,
                 scaling = False,
                 interpolation = True,
                 f32 = False):
        
        dataset_name = str(os.path.basename(data_path)).split(".")[0].removeprefix("ftsfr_")

        # Read dataset to a pd.DataFrame
        df = pd.read_parquet(data_path).rename(columns = {"id" : 'unique_id'})
        # This pivot adds all values for an entity as a TS in each column
        proc_df = df.pivot(index="ds", columns="unique_id", values="y").reset_index()
        # Basic cleaning
        proc_df.rename_axis(None, axis=1, inplace=True)
        # TimeSeries object is important for darts
        if f32:
            raw_series = TimeSeries.from_dataframe(proc_df, time_col = "ds").astype(np.float32)
        else:
            raw_series = TimeSeries.from_dataframe(proc_df, time_col = "ds")
        # Replace NaNs automatically
        # TODO: Replace with better method to deal with NaNs.
        # This uses linear interpolation
        # but that is most probably leading to reduced performance.
        if interpolation:
            raw_series = fill_missing_values(raw_series)

        if scaling:
            transformer = Scaler()
            transformed_series = transformer.fit_transform(raw_series)
            # Splitting into train and test
            train_series, test_series = train_test_split(transformed_series, test_size = test_split)
        else:
            train_series, test_series = train_test_split(raw_series, test_size = test_split)
        
        # TODO: Implement a filling mechanism which adds means to the dataset
        # if len(train_series) < 4 * seasonality:
        #     difference = 4 * seasonality - len(train_series)
        #     pd.date_range(end = train_series.start_time(), periods = difference + 1)


        # Path to save model
        model_path = output_path / "models" / model_name / dataset_name
        Path(model_path).mkdir(parents = True, exist_ok = True)
        model_path = model_path / "saved_model" # Without an extension

        # Path to save forecasts
        forecast_path = output_path / "forecasts" / model_name / dataset_name
        Path(forecast_path).mkdir(parents = True, exist_ok = True)
        forecast_path = forecast_path / "forecasts.parquet"

        result_path = output_path / "raw_results" / model_name
        result_path.mkdir(parents = True, exist_ok = True)
        result_path = result_path / str(dataset_name + ".csv")

        # Names

        self.dataset_name = dataset_name
        self.model_name = model_name

        # Paths
        self.dataset_path = data_path
        self.forecast_path = forecast_path
        self.result_path = result_path
        self.model_path = str(model_path)

        # Series
        self.raw_series = raw_series # Helps with predictions
        self.train_series = train_series
        self.test_series = test_series
        self.pred_series = None # None for checking if predictions have been made

        # Important variables
        # This is the ratio of test entries to total entries in the df
        self.test_split = test_split
        self.seasonality = seasonality
        self.frequency = frequency
        
        # Stores base class
        self.estimator = estimator
        # Stores the actual model
        self.model = estimator # Initially same as estimator

        # Error metrics
        self.errors = defaultdict(float)

        print("Object Initialized:")
        print(tabulate([["Model", model_name],
                        ["Dataset", dataset_name],
                        ["Total Entities", self.raw_series.n_components]],
                        tablefmt="fancy_grid"))

    def _train_test_split(self, entity_data):
        try:
            self.train_series, self.test_series = train_test_split(entity_data, test_size = self.test_split)
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in {self.model_name} dataset splitting. Full traceback above \u2191")
            self.print_sep()
            return None

    def train(self):
        try:
            self.model.fit(self.train_series)
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in {self.model_name} training. Full traceback above \u2191")
            self.print_sep()
            return None

    def save_model(self):
        try:
            self.model.save(self.model_path)
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in saving {self.model_name} model. Full traceback above \u2191")
            self.print_sep()
            return None
    
    def load_model(self):
        try:
            self.model = self.estimator.load(self.model_path)
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in {self.model_name} model loading. Full traceback above \u2191")
            self.print_sep()
            return None

    def forecast(self):
        try:
            pred_series = self.model.predict(1, 
                                series = self.raw_series.drop_after(
                                self.test_series.get_timestamp_at_point(0)))
            for i in range(1, len(self.test_series)):
                curr_time_stamp = self.test_series.get_timestamp_at_point(i)
                pred_dataset = self.raw_series.drop_after(curr_time_stamp)
                current_pred = self.model.predict(1, series = pred_dataset)
                pred_series = pred_series.concatenate(current_pred)
            self.pred_series = pred_series
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in {self.model_name} forecasting. Full traceback above \u2191")
            self.print_sep()
            return None

    def save_forecast(self):
        try:
            # Save to parquet
            temp_df = self.pred_series.to_dataframe(time_as_index = False)
            temp_df.to_parquet(self.forecast_path)
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in saving {self.model_name} forecasts. Full traceback above \u2191")
            self.print_sep()
            return None
    
    def load_forecast(self):
        try:
            temp_df = pd.read_parquet(self.forecast_path)
            self.pred_series = TimeSeries.from_dataframe(temp_df, time_col = "ds")
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in loading {self.model_name} forecasts. Full traceback above \u2191")
            self.print_sep()
            return None
    
    def calculate_error(self, metric = "MASE"):
        if self.pred_series is None:
            raise ValueError('Please call self.forecast() first.')
        if metric == "MASE":
            self.errors["MASE"] = mase(self.test_series,
                                       self.pred_series,
                                       self.train_series,
                                       self.seasonality)
            return self.errors["MASE"]
        else:
            raise ValueError('Metric not supported.')
