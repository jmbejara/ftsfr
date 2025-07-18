"""
The NixtlaMain class can help quickly create the necessary objects for 
forecasting with Nixtla's neuralforecast models.
"""
from pathlib import Path
import os
import tabulate
from collections import defaultdict
import pandas as pd
import numpy as np
from .forecasting_model import forecasting_model
from darts import TimeSeries
from darts.metrics import mase
from neuralforecast import NeuralForecast

class NixtlaMain(forecasting_model):
    def __init__(self,
                 estimator,
                 model_name,
                 test_split,
                 frequency,
                 seasonality,
                 data_path,
                 output_path):
        
        dataset_name = str(os.path.basename(data_path)).split(".")[0].removeprefix("ftsfr_")

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

        # Data-related variables

        self.dataset_path = data_path
        self.dataset_name = dataset_name
        self.forecast_path = forecast_path
        self.result_path = result_path
        self.train_series = test_data
        self.test_series = train_data
        self.test_length = test_length
        self.pred_series = None

        self.seasonality = seasonality
        self.frequency = frequency
        
        # Model related variables
        # Stores base class
        self.estimator = estimator(h = test_length, input_size = seasonality * 4)
        # Stores the actual model
        self.nf = NeuralForecast(models = [self.estimator], freq = frequency)
        self.model_path = str(model_path)
        self.model_name = model_name
        # Error metrics
        self.errors = defaultdict(float)

    def train(self):
        self.nf.fit(df = self.train_series)
        self.nf.save(self.model_path,
                     model_index = None,
                     overwrite = True,
                     save_dataset = False)
    
    def load_model(self):
        self.nf = NeuralForecast.load(path = str(self.model_path))

    def forecast(self):
        # Get predictions
        self.pred_series = self.nf.predict(self.train_series)

        # Save to parquet
        pred_series = pred_series.sort_values(["unique_id", "ds"]).reset_index(
            drop=True
        )
        test_data = test_data.sort_values(["unique_id", "ds"]).reset_index(drop=True)
        # make the ds columns same
        pred_series["ds"] = test_data["ds"]

        pred_series.to_parquet(self.forecast_path, engine = "pyarrow")
    
    def load_forecast(self):
        temp_df = pd.read_parquet(self.forecast_path)
        self.pred_series = TimeSeries.from_dataframe(temp_df, time_col = "ds")
    
    def calculate_error(self, metric = "MASE"):
        
        if metric == "MASE":
            pred_series = pd.read_parquet(self.forecast_path)
        
            test_series = (
                self.test_series.pivot(index="ds", columns="unique_id", values="y")
                .reset_index()
                .rename_axis(None, axis=1)
                .rename(columns={"ds": "date"})
            )
            series = (
                self.train_series.pivot(index="ds", columns="unique_id", values="y")
                .reset_index()
                .rename_axis(None, axis=1)
                .rename(columns={"ds": "date"})
            )
            pred_series = (
                pred_series.pivot(index="ds", columns="unique_id", values="Autoformer")
                .reset_index()
                .rename_axis(None, axis=1)
                .rename(columns={"ds": "date"})
            )

            test_series = TimeSeries.from_dataframe(test_series, time_col="date")
            series = TimeSeries.from_dataframe(series, time_col="date")
            pred_series = TimeSeries.from_dataframe(pred_series, time_col="date")

            self.errors["MASE"] = mase(test_series, pred_series, series, self.seasonality)
            return self.errors["MASE"]
        else:
            raise ValueError('Metric not supported.')
    
    def print_summary(self):
        print(tabulate([
            ["Model", self.model_name],
            ["Dataset", self.dataset_name],
            ["Entities", len(self.train_series["id"].unique())],
            ["Frequency", self.frequency],
            ["Seasonality", self.seasonality],
            ["Global MASE", self.errors["MASE"]]
            ], tablefmt="fancy_grid"))
    
    def save_results(self):
        forecast_res = pd.DataFrame(
            {
                "Model" : [self.model_name],
                "Dataset" : [self.dataset_name],
                "Entities" : [len(self.train_series["id"].unique())],
                "Global MASE" : [self.errors["MASE"]]
            }
        )

        forecast_res.to_csv(self.result_path)
    
    def main_workflow(self):
        self.train()
        self.forecast()
        self.calculate_error()
        self.print_summary()
        self.save_results()