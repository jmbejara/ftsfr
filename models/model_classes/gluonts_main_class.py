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

from .forecasting_model import forecasting_model
from .helper_func import calculate_darts_MASE

class GluontsMain(forecasting_model):
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

        raw_df = pd.read_parquet(data_path)
        raw_df = raw_df.rename(columns = {"id" : "unique_id"})

        raw_df = raw_df.sort_values(["unique_id", "ds"])
        raw_df = raw_df.reset_index(drop = True)

        proc_df = raw_df.groupby("unique_id").agg(lambda x: pd.array(x))
        proc_df = proc_df.reset_index()
        proc_df["ds"] = proc_df["ds"].iloc[0][0]
        proc_df["y"] = proc_df["y"].apply(lambda x: x.to_numpy())

        train_series_list = []
        test_series_list = []
        train_series_full_list = []
        test_series_full_list = []

        for index, row in proc_df.iterrows():
            train_start_time = row["ds"]
            series_data = row["y"]

            test_index = int(test_split * len(series_data))
            train_elements = len(series_data) - test_index
            train_series_data = series_data[:-test_index]
            # if train_elements < 4 * seasonality:
            #     curr_mean = train_series_data.mean()
            #     difference = 4 * seasonality - train_elements
            #     for _ in range(difference):
            #         train_series_data = np.insert(train_series_data, 0, curr_mean)
            
            test_series_data = series_data[-test_index:]

            train_series_list.append(train_series_data)
            test_series_list.append(test_series_data)

            train_series_full_list.append(
                {
                    FieldName.TARGET: train_series_data,
                    FieldName.START: pd.Timestamp(train_start_time),
                }
            )

            test_series_full_list.append(
                {
                    FieldName.TARGET: series_data,
                    FieldName.START: pd.Timestamp(train_start_time),
                }
            )

        train_ds = ListDataset(train_series_full_list, freq=frequency)
        test_ds = ListDataset(test_series_full_list, freq=frequency)

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
        # Stores base class
        self.estimator = estimator
        # Stores the actual model
        self.model = estimator
        # Error metrics
        self.errors = defaultdict(float)

    def train(self):
        self.model = self.estimator.train(training_data=self.train_series)
    
    def save_model(self):
        self.model.serialize(self.model_path)

    def load_model(self):
        self.model = Predictor.deserialize(self.model_path)

    def forecast(self):
        model = self.model
        test_series = self.test_series
        result = []
        for i in range(len(self.train_series[0]['target']), 
                       len(test_series[0]['target'])):
            temp_dataset = []
            for m in test_series:
                temp_dataset.append(m.copy())
                temp_dataset[-1]['target'] = temp_dataset[-1]['target'][:i]
            res = map(lambda x: x.to_sample_forecast(1), 
                    list(model.predict(temp_dataset)))
            res = list(res)
            temp = []
            for j in res:
                temp.append(j.samples.item())
            result.append(temp)
        
        df = self.raw_df.copy(deep = True)
        dates_unique = df.ds.unique()[len(self.train_series[0]['target']):]
        entities = sorted(df.unique_id.unique())
        i = 0
        for date in dates_unique:
            j = 0
            for id in entities:
                df.loc[(df['ds'] == date) & (df['unique_id'] == id), 'y'] = result[i][j]
                j += 1
            i += 1
        
        self.pred_series = df
    
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

            pred_series = self.pred_series
            pred_series = pred_series[pred_series.ds >= 
                                      unique_dates[-test_length]]
            
            self.errors["MASE"] = calculate_darts_MASE(test_data,
                                                       train_data,
                                                       pred_series,
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
    
    def save_results(self):
        forecast_res = pd.DataFrame(
            {
                "Model" : [self.model_name],
                "Dataset" : [self.dataset_name],
                "Global MASE" : [self.errors["MASE"]]
            }
        )

        forecast_res.to_csv(self.result_path)