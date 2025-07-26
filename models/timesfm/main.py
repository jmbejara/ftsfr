"""
TimesFM using the official timesfm package.

Performs both local and global forecasting using a TimesFM. Reports both mean and
median MASE for local forecasts and a single global MASE.

NOTE: Loading the TimesFM 500m checkpoint needs about 2GB of space.
"""

import os
import traceback
from collections import defaultdict
from pathlib import Path
import numpy as np
import pandas as pd
from tabulate import tabulate
from darts import TimeSeries
import subprocess
import timesfm
import sys
sys.path.append('../')

from model_classes.forecasting_model import forecasting_model
from model_classes.helper_func import calculate_darts_MASE

# TODO: Need to add logging
# TODO: Make a decorator for error handling

class TimesFMForecasting(forecasting_model):
    def __init__(self,
                 model_version,
                 test_split,
                 frequency,
                 seasonality,
                 data_path,
                 output_path):
        
        dataset_name = str(os.path.basename(data_path)).split(".")[0]
        dataset_name = dataset_name.removeprefix("ftsfr_")

        model_name = "timesfm"

        # Path to save forecasts
        forecast_path = output_path / "forecasts" / model_name / dataset_name
        Path(forecast_path).mkdir(parents = True, exist_ok = True)
        forecast_path = forecast_path / "forecasts.parquet"

        result_path = output_path / "raw_results" / model_name
        result_path.mkdir(parents = True, exist_ok = True)
        result_path = result_path / str(dataset_name + ".csv")

        df = pd.read_parquet(data_path).rename(columns = {"id" : 'unique_id'})
        df = df.interpolate()
        df = df.sort_values(["unique_id", "ds"])
        df = df.reset_index(drop = True)

        test_length = int(test_split * len(df.ds.unique()))
        unique_dates = sorted(np.unique(df["ds"].values))

        # Names
        self.dataset_name = dataset_name
        self.model_name = model_name

        # Paths
        self.forecast_path = forecast_path
        self.dataset_path = data_path
        self.result_path = result_path

        # Dataframes
        self.raw_series = df
        self.pred_series = None
        self.train_series = df[df.ds < unique_dates[-test_length]]
        self.test_series = df[df.ds >= unique_dates[-test_length]]

        # Important variables
        self.seasonality = seasonality
        self.frequency = frequency
        self.test_length_by_date = test_length

        if model_version == "500m" or model_version == "200m":
            self.model_version = model_version
        else:
            self.model_version = "500m"
        
        self.tfm = None

        # Error metrics
        self.errors = defaultdict(float)

        print("Object Initialized:")
        print(tabulate([["Model", model_name],
                        ["Dataset", dataset_name],
                        ["Total Entities", len(df["unique_id"].unique())]],
                        tablefmt="fancy_grid"))

    def train(self):
        # Might repurpose to fine-tuning later
        pass

    def load_model(self):
        # Check for an NVIDIA GPU
        try:
            subprocess.check_output("nvidia-smi")
            device = "gpu"
        except Exception:
            device = "cpu"
        # Code below adapted from https://pypi.org/project/timesfm/
        # and https://github.com/google-research/timesfm
        try:
            if self.model_version == "200m":
                repo_id = "google/timesfm-1.0-200m-pytorch"
            else:
                repo_id = "google/timesfm-2.0-500m-pytorch"
            # Loading the timesfm-2.0 checkpoint:
            self.tfm = timesfm.TimesFm(
            hparams=timesfm.TimesFmHparams(
                backend=device,
                per_core_batch_size=32,
                horizon_len=128,
                num_layers=50,
                use_positional_embedding=False,
                context_len=2048,
            ),
            checkpoint=timesfm.TimesFmCheckpoint(
                huggingface_repo_id = repo_id
            ),
        )
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in loading {self.model_name}. " +
                  "Full traceback above \u2191")
            self.print_sep()
            return None

    def forecast(self):
        try:
            df = self.raw_series
            tfm = self.tfm
            result = pd.DataFrame(columns = df.columns)
            for i in range(self.test_length_by_date, 0, -1):
                curr_date = sorted(np.unique(df["ds"].values))[-i]
                train_data = df[df.ds < curr_date]
                forecast_df = tfm.forecast_on_df(
                            inputs=train_data,
                            freq=self.frequency,
                            value_name="y",
                            num_jobs=-1,
                        )
                forecast_df = forecast_df[["unique_id", "ds", "timesfm"]]
                forecast_df = forecast_df[forecast_df.ds == forecast_df.ds.min()]
                forecast_df["ds"] = curr_date
                result = pd.concat([result, forecast_df], ignore_index = True)
            result = result.drop(["y"], axis = 1)
            result = result.rename(columns = {"timesfm" : "y"})
            self.pred_series = result
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
                                                           self.seasonality)
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
            ["Entities", len(self.raw_series["unique_id"].unique())],
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
                    "Entities" : [len(self.raw_series["unique_id"].unique())],
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


if __name__ == "__main__":
    
    dataset_path = Path(os.environ["DATASET_PATH"])
    frequency = os.environ["FREQUENCY"]
    seasonality = int(os.environ["SEASONALITY"])
    if os.environ.get("OUTPUT_DIR", None) is not None:
        OUTPUT_DIR = Path(os.environ["OUTPUT_DIR"])
    else:
        OUTPUT_DIR = Path().resolve().parent.parent / "_output"
    timesfm_obj = TimesFMForecasting("500m", # can use "200m" if needed
                                        0.2,
                                        frequency,
                                        seasonality,
                                        dataset_path,
                                        OUTPUT_DIR)

    timesfm_obj.inference_workflow()