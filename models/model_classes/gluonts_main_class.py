"""
The GluontsMain class can help quickly create the necessary objects for 
forecasting with Gluonts models.
"""

import os
from collections import defaultdict
from pathlib import Path

import pandas as pd
import numpy as np
from tabulate import tabulate

# Gluonts based imports
from gluonts.dataset.common import ListDataset
from gluonts.dataset.field_names import FieldName
from gluonts.model.predictor import Predictor
from gluonts.dataset.pandas import PandasDataset

from .forecasting_model import forecasting_model
from .helper_func import *

class GluontsMain(forecasting_model):
    def __init__(self,
                 estimator,
                 model_name,
                 test_split,
                 frequency,
                 seasonality,
                 data_path,
                 output_path):
        
        # This helps with organising
        dataset_name = str(os.path.basename(data_path)).split(".")[0]
        dataset_name = dataset_name.removeprefix("ftsfr_")

        # Path to save model once trained
        model_path = output_path / "models" / model_name / dataset_name
        Path(model_path).mkdir(parents = True, exist_ok = True)

        # Path to save forecasts generated after training the model
        forecast_path = output_path / "forecasts" / model_name / dataset_name
        Path(forecast_path).mkdir(parents = True, exist_ok = True)
        forecast_path = forecast_path / "forecasts.parquet"

        # Path to save results which include the error metric
        result_path = output_path / "raw_results" / model_name
        result_path.mkdir(parents = True, exist_ok = True)
        result_path = result_path / str(dataset_name + ".csv")

        # Data pre-processing
        raw_df = pd.read_parquet(data_path)
        raw_df = raw_df.rename(columns = {"id" : "unique_id"})
        # Fills missing dates and extends if required
        raw_df, test_split = process_df(raw_df,
                                        frequency,
                                        seasonality,
                                        test_split)
        # Fills all the np.nans
        raw_df = custom_interpolate(raw_df)
        # Sorting for consistency
        raw_df = raw_df.sort_values(["unique_id", "ds"])
        # Sorting makes the indices shuffled
        raw_df = raw_df.reset_index(drop = True)
        # Some float and double issues
        raw_df['y'] = raw_df['y'].astype(np.float32)

        # Unique dates defines the number of entries per entity
        # makes calculating test_length and subsequent splits easier
        unique_dates = raw_df["ds"].unique()
        test_length = int(test_split * len(unique_dates))
        
        # Splitting to train and test
        # Train data for GluonTS is the entire df - test entries
        train_data = raw_df[raw_df['ds'] < unique_dates[-test_length]]
        # Test data for GluonTS is the entire dataframe with the dates as index
        test_data = raw_df.set_index("ds")
        # Train data for GluonTS with dates as index
        train_data = train_data.set_index("ds")
        # Converts to GluonTS format
        test_ds = PandasDataset.from_long_dataframe(test_data,
                                                    target="y",
                                                    item_id="unique_id")
        train_ds = PandasDataset.from_long_dataframe(train_data, 
                                                     target="y", 
                                                     item_id="unique_id")
        
        # Names
        self.model_name = model_name
        self.dataset_name = dataset_name

        # Paths
        self.model_path = model_path
        self.dataset_path = data_path
        self.forecast_path = forecast_path
        self.result_path = result_path

        # Series
        self.test_series = test_ds
        self.train_series = train_ds
        self.pred_series = None
        self.raw_df = raw_df

        # Important variables
        self.seasonality = seasonality
        self.frequency = frequency
        self.test_split = test_split
        
        # Model related variables
        # Stores the actual model
        self.model = estimator
        # Error metrics
        self.errors = defaultdict(float)

        print("Object Initialized:")
        print(tabulate([["Model", model_name],
                        ["Dataset", dataset_name],
                        ["Total Entities", len(raw_df["unique_id"].unique())]],
                        tablefmt="fancy_grid"))

    def train(self):
        self.model = self.model.train(training_data=self.train_series)
    
    @common_error_catch
    def save_model(self):
        self.model.serialize(self.model_path)

    def load_model(self):
        self.model = Predictor.deserialize(self.model_path)

    def forecast(self):
        model = self.model
        test_series = list(self.test_series)
        train_series = list(self.train_series)
        result = []

        for i in range(len(train_series[0]['target']), 
                       len(test_series[0]['target'])):
            
            # A temp dataset to store the current window of values
            temp_dataset = []
            for m in test_series:
                temp_dataset.append(m.copy())
                temp_dataset[-1]['target'] = temp_dataset[-1]['target'][:i]
            
            # Get model predictions for the next timestamp
            temp_pred = list(model.predict(temp_dataset, num_samples = 1))

            # Some models(e.g. wavenet) give SampleForecasts directly 
            # while others(e.g. ffnn) need conversion
            if temp_pred[0].__class__.__name__ != "SampleForecast":
                res = map(lambda x: x.to_sample_forecast(1),
                        temp_pred)
                res = list(res)
            else:
                res = temp_pred

            # Each SampleForecast has three values that we're interested in.
            # Each list in temp is a row in a dataframe.
            temp = []
            for j in res:
                temp.append([])
                temp[-1].append(j.start_date.to_timestamp())
                temp[-1].append(j.item_id)
                temp[-1].append(j.samples.item())
            
            # Stores all the rows
            result += temp
        
        self.pred_series = pd.DataFrame(result, 
                                        columns = ['ds', 'unique_id', 'y'])
    
    @common_error_catch
    def save_forecast(self):
        self.pred_series.to_parquet(self.forecast_path)

    def load_forecast(self):
        self.pred_series = pd.read_parquet(self.forecast_path)
    
    def calculate_error(self, metric = "MASE"):
        if metric == "MASE":
            df = self.raw_df

            unique_dates = df.ds.unique()
            test_length = int(self.test_split * len(unique_dates))

            test_data = df[df.ds >= unique_dates[-test_length]]
            train_data = df[df.ds < unique_dates[-test_length]]
            
            self.errors["MASE"] = calculate_darts_MASE(test_data,
                                                       train_data,
                                                       self.pred_series,
                                                       self.seasonality)

            return self.errors["MASE"]
        else:
            raise ValueError('Metric not supported.')
    
    def print_summary(self):
        print(tabulate([
            ["Model", self.model_name],
            ["Dataset", self.dataset_name],
            ["Frequency", self.frequency],
            ["Seasonality", self.seasonality],
            ["Global MASE", self.errors["MASE"]]
            ], tablefmt="fancy_grid"))
    
    @common_error_catch
    def save_results(self):
        forecast_res = pd.DataFrame(
            {
                "Model" : [self.model_name],
                "Dataset" : [self.dataset_name],
                "Frequency" : [self.frequency],
                "Seasonality" : [self.seasonality],
                "Global MASE" : [self.errors["MASE"]]
            }
        )

        forecast_res.to_csv(self.result_path)