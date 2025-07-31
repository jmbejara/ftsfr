"""
The NixtlaMain class can help quickly create the necessary objects for 
forecasting with Nixtla's neuralforecast models.

NOTE: Currently doesn't support training on MPS.
"""
import os
import traceback
from collections import defaultdict
from pathlib import Path
import logging

import numpy as np
import pandas as pd
from pandas.tseries.frequencies import to_offset
from tabulate import tabulate
import torch
from darts import TimeSeries
from neuralforecast import NeuralForecast

from .forecasting_model import forecasting_model
from .helper_func import *

nx_logger = logging.getLogger("NixtlaMain")

class NixtlaMain(forecasting_model):
    def __init__(self,
                 estimator,
                 model_name,
                 test_split,
                 frequency,
                 seasonality,
                 data_path,
                 output_path):
        
        nx_logger.info("NixtlaMain __init__ called.")

        # This helps with organising
        dataset_name = str(os.path.basename(data_path)).split(".")[0]
        dataset_name = dataset_name.removeprefix("ftsfr_")

        # Path to save model once trained
        model_path = output_path / "models" / model_name / dataset_name
        Path(model_path).mkdir(parents = True, exist_ok = True)

        nx_logger.info("Created model path and its +" + \
                       "folders if they were missing.")

        # Path to save forecasts generated after training the model
        forecast_path = output_path / "forecasts" / model_name / dataset_name
        Path(forecast_path).mkdir(parents = True, exist_ok = True)
        forecast_path = forecast_path / "forecasts.parquet"

        nx_logger.info("Created forecast_path and its "+\
                       "folders if they were missing.")

        # Path to save results which include the error metric
        result_path = output_path / "raw_results" / model_name
        result_path.mkdir(parents = True, exist_ok = True)
        result_path = result_path / str(dataset_name + ".csv")

        nx_logger.info("Created result_path and its "+\
                       "folders if they were missing.")

        # Data pre-processing
        df = pd.read_parquet(data_path).rename(columns = {"id" : 'unique_id'})
        df, test_split = process_df(df, frequency, seasonality, test_split) 
        df = custom_interpolate(df)

        nx_logger.info("Data read and pre-processed.")

        # Unique dates defines the number of entries per entity
        # makes calculating test_length and subsequent splits easier
        unique_dates = df['ds'].unique()
        test_length = int(test_split * len(unique_dates))
        test_data = df[df.ds >= unique_dates[-test_length]]
        train_data = df[df.ds < unique_dates[-test_length]]

        nx_logger.info("Data split into train and test.")

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
            nx_logger.info("MPS available, but will be ignored.")
            self.estimator = estimator(h = 1,
                                        input_size = seasonality * 4,
                                        accelerator = "cpu")
        else:
            # Auto detect if not on MPS
            nx_logger.info("MPS not available. Auto detection enabled.")
            self.estimator = estimator(h = 1, input_size = seasonality * 4)
        
        # Stores the nf object
        self.nf = NeuralForecast(models = [self.estimator], freq = frequency)
        # Error metrics
        self.errors = defaultdict(float)

        nx_logger.info("Internal variables set up.")

        print("Object Initialized:")
        print(tabulate([["Model", model_name],
                        ["Dataset", dataset_name],
                        ["Total Entities", len(df["unique_id"].unique())]],
                        tablefmt="fancy_grid"))
        
        nx_logger.info("Object initialized.")

    def train(self):
        nx_logger.info("Model training started.")
        self.nf.fit(df = self.train_series)
        nx_logger.info("Model trained.")
    
    @common_error_catch
    def save_model(self):
        self.nf.save(self.model_path,
                    model_index = None,
                    overwrite = True,
                    save_dataset = False)
        nx_logger.info("Model saved to \"" + str(self.model_path) + "\".")

    def load_model(self):
        self.nf = NeuralForecast.load(path = str(self.model_path))
        nx_logger.info("Model loaded from \"" + str(self.model_path) + "\".")

    @common_error_catch
    def forecast(self):
        nx_logger.info("Forecasting from model.")
        # The loop keeps concatenating forecasts to pred_series
        pred_series = self.nf.predict(self.train_series)
        first_date = self.test_series["ds"].unique()[0]
        pred_series["ds"] = first_date
        df = self.raw_series
        nx_logger.info("Got predictions for date: " + \
                       first_date.strftime("%Y-%m-%d, %r") + ".")

        # Sliding window forecasts
        # Predict 1 date right after the dataset in the arguments
        # After each prediction the next prediction uses the actual value in the
        # test dataset instead of relying on the previous predicted value.
        nx_logger.info("Starting for loop to get sliding window forecasts.")
        for i in self.test_series["ds"].unique()[1:]:
            # Get predictions for the next date
            temp_pred_series = self.nf.predict(df[df.ds < i])
            # Lining up the dates
            temp_pred_series['ds'] = i
            pred_series = pd.concat([pred_series, temp_pred_series],
                                    ignore_index = True)
            nx_logger.info("Got predictions for date: " + \
                           i.strftime("%Y-%m-%d, %r") + ".")
        
        self.pred_series = pred_series

        nx_logger.info("Forecasting complete. Internal variable updated.")

    @common_error_catch
    def save_forecast(self):
        self.pred_series.to_parquet(self.forecast_path, engine = "pyarrow")
        nx_logger.info("Saved forecasts to \"" + str(self.forecast_path) +"\".")

    def load_forecast(self):
        temp_df = pd.read_parquet(self.forecast_path)
        self.pred_series = TimeSeries.from_dataframe(temp_df, 
                                                     time_col = "ds")
        nx_logger.info("Loaded forecasts from \"" +\
                       str(self.forecast_path) +"\".")
    
    def calculate_error(self, metric = "MASE"):
        if metric == "MASE":
            self.errors["MASE"] = calculate_darts_MASE(self.test_series,
                                                        self.train_series,
                                                        self.pred_series,
                                                        self.seasonality,
                                                        self.model_name.title())
            
            nx_logger.info("MASE: " + str(self.errors["MASE"]) + ".")

            return self.errors["MASE"]
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
    
    @common_error_catch
    def save_results(self):
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

        nx_logger.info("Saved results to \"" + str(self.result_path) +"\".")