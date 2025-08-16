"""
TimesFM using the official timesfm package.

Performs both local and global forecasting using a TimesFM. Reports both mean and
median MASE for local forecasts and a single global MASE.

NOTE: Loading the TimesFM 500m checkpoint needs about 2GB of space.
"""

import os
from collections import defaultdict
from pathlib import Path
import logging
import numpy as np
import pandas as pd
from tabulate import tabulate
import sys

# Add parent directory to path for imports
parent_dir = os.path.join(os.path.dirname(__file__), "..")
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config_reader import get_model_config
from model_classes.forecasting_model import forecasting_model
from model_classes.helper_func import *

logger = logging.getLogger("main")


class TimesFMForecasting(forecasting_model):
    def __init__(
        self, model_version, test_split, frequency, seasonality, data_path, output_path
    ):
        # TimesFM-specific import only when needed
        logger.info("TimesFM __init__ called.")

        dataset_name = str(os.path.basename(data_path)).split(".")[0]
        dataset_name = dataset_name.removeprefix("ftsfr_")

        model_name = "timesfm"

        # Path to save forecasts
        forecast_path = output_path / "forecasts" / model_name / dataset_name
        Path(forecast_path).mkdir(parents=True, exist_ok=True)
        forecast_path = forecast_path / "forecasts.parquet"

        logger.info(
            "Created forecast path and required folders if " + "they weren't present."
        )

        result_path = output_path / "raw_results" / model_name
        result_path.mkdir(parents=True, exist_ok=True)
        result_path = result_path / str(dataset_name + ".csv")

        logger.info(
            "Created result path and required folders if they " + "weren't present."
        )

        df = pd.read_parquet(data_path).rename(columns={"id": "unique_id"})
        train_data, test_data, test_split = process_df(df, frequency, seasonality, test_split)
        df = pd.concat([train_data, test_data]).\
                       sort_values(["unique_id", "ds"]).\
                       reset_index(drop = True)

        logger.info("Read and processed dataframe.")

        test_length = int(test_split * len(df['ds'].unique()))

        # Names
        self.dataset_name = dataset_name
        self.model_name = model_name

        # Paths
        self.forecast_path = forecast_path
        self.dataset_path = data_path
        self.result_path = result_path

        # Dataframes
        self.raw_data = df
        self.pred_data = None
        self.train_data = train_data
        self.test_data = test_data

        logger.info("Generated train and test series.")

        # Important variables
        self.seasonality = seasonality
        self.frequency = frequency
        self.test_length_by_date = test_length

        if model_version == "500m" or model_version == "200m":
            self.model_version = model_version
        else:
            self.model_version = "500m"

        logger.info("Selected: " + self.model_version + ".")

        self.tfm = None

        # Error metrics
        self.errors = defaultdict(float)

        logger.info("Setup internal variables.")

        print("Object Initialized:")
        print(
            tabulate(
                [
                    ["Model", model_name],
                    ["Dataset", dataset_name],
                    ["Total Entities", len(df["unique_id"].unique())],
                ],
                tablefmt="fancy_grid",
            )
        )

        logger.info("Object fully initialized.")

    def train(self):
        # Might repurpose to fine-tuning later
        pass

    @common_error_catch
    def load_model(self):
        import subprocess
        import timesfm

        logger.info("Loading model.")
        # Check for an NVIDIA GPU
        try:
            subprocess.check_output("nvidia-smi")
            device = "gpu"
        except Exception:
            device = "cpu"

        logger.info("Selected device: " + device + ".")
        # Code below adapted from https://pypi.org/project/timesfm/
        # and https://github.com/google-research/timesfm
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
            checkpoint=timesfm.TimesFmCheckpoint(huggingface_repo_id=repo_id),
        )

        logger.info("Model loaded.")

    @common_error_catch
    def forecast(self):
        logger.info("Getting model predictions.")
        df = self.raw_data
        tfm = self.tfm
        result = pd.DataFrame(columns=df.columns)

        logger.info("Starting loop to get sliding window forecasts.")

        for i in range(self.test_length_by_date, 0, -1):
            curr_date = sorted(np.unique(df["ds"].values))[-i]
            logger.info(
                "Getting predictions for date: "
                + pd.to_datetime(curr_date).strftime("%Y-%m-%d, %r")
                + "."
            )
            train_data = df[df.ds < curr_date]
            forecast_df = tfm.forecast_on_df(
                inputs=train_data,
                freq=self.frequency,
                value_name="y",
                num_jobs=-1,
            )
            logger.info("Got predictions.")
            forecast_df = forecast_df[["unique_id", "ds", "timesfm"]]
            forecast_df = forecast_df[forecast_df.ds == forecast_df.ds.min()]
            forecast_df["ds"] = curr_date
            result = pd.concat([result, forecast_df], ignore_index=True)
            logger.info("Processed DataFrame and added to result.")
        result = result.drop(["y"], axis=1)
        result = result.rename(columns={"timesfm": "y"})
        self.pred_data = result

        logger.info(
            "Got all predictions. Processed result " + "and updated internal variable."
        )

    @common_error_catch
    def save_forecast(self):
        if self.pred_data is None:
            logger.error(
                "Cannot save forecast: pred_data is None. Forecast method may have failed."
            )
            raise ValueError(
                "pred_data is None - forecast method did not complete successfully"
            )
        self.pred_data.to_parquet(self.forecast_path, engine="pyarrow")
        logger.info('Predictions saved to "' + str(self.forecast_path) + '".')

    @common_error_catch
    def load_forecast(self):
        temp_df = pd.read_parquet(self.forecast_path)
        # Check if darts is available before using TimeSeries
        if not DARTS_AVAILABLE:
            logger.error(
                "Cannot load forecast: darts is required but not available in this environment"
            )
            raise ImportError(
                "darts is required for loading forecasts but not available in this environment"
            )
        self.pred_data = TimeSeries.from_dataframe(temp_df, time_col="ds")
        logger.info(
            "Model forecasts loaded from "
            + self.forecast_path
            + ". Internal variable updated."
        )

    def calculate_error(self, metric="MASE"):
        if self.pred_data is None:
            logger.error(
                "Cannot calculate error: pred_data is None. Forecast method may have failed."
            )
            raise ValueError(
                "pred_data is None - forecast method did not complete successfully"
            )

        if metric == "MASE":
            self.errors["MASE"] = calculate_darts_MASE(
                self.test_data, self.train_data, self.pred_data, self.seasonality
            )
            logger.info("MASE = " + str(self.errors["MASE"]) + ".")
            return self.errors["MASE"]
        else:
            logger.error("calculate_error called for an unsupported metric.")
            raise ValueError("Metric not supported.")

    def print_summary(self):
        print(
            tabulate(
                [
                    ["Model", self.model_name],
                    ["Dataset", self.dataset_name],
                    ["Entities", len(self.raw_data["unique_id"].unique())],
                    ["Frequency", self.frequency],
                    ["Seasonality", self.seasonality],
                    ["Global MASE", self.errors["MASE"]],
                ],
                tablefmt="fancy_grid",
            )
        )

    @common_error_catch
    def save_results(self):
        forecast_res = pd.DataFrame(
            {
                "Model": [self.model_name],
                "Dataset": [self.dataset_name],
                "Entities": [len(self.raw_data["unique_id"].unique())],
                "Frequency": [self.frequency],
                "Seasonality": [self.seasonality],
                "Global MASE": [self.errors["MASE"]],
            }
        )

        forecast_res.to_csv(self.result_path)
        logger.info('Saved results to "' + str(self.result_path) + '".')


if __name__ == "__main__":
    env_vars = get_model_config(os.environ)[
        :5
    ]  # Get first 5 elements for compatibility

    data_path = env_vars[3]

    dataset_name = str(os.path.basename(data_path)).split(".")[0]
    dataset_name = dataset_name.removeprefix("ftsfr_")

    log_path = Path().resolve().parent / "model_logs" / "timesfm"
    Path(log_path).mkdir(parents=True, exist_ok=True)
    log_path = log_path / (dataset_name + ".log")
    logging.basicConfig(
        filename=log_path,
        filemode="w",  # Overwrites previously existing logs
        format="%(asctime)s - timesfm - %(name)-12s" + " - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )

    logger.info("Running main. Environment variables read.")

    timesfm_obj = TimesFMForecasting("500m", *env_vars)  # can use "200m"

    timesfm_obj.inference_workflow()
