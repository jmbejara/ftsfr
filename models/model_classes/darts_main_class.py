"""
This contains classes to directly inherit into a model class.

Expected behaviour is that each new object is created for a unique model
and data pair.
"""

import os
from collections import defaultdict
from pathlib import Path

import logging

dm_logger = logging.getLogger("DartsMain")

# from warnings import filterwarnings
# filterwarnings("ignore")

import numpy as np
import pandas as pd
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from darts.metrics import mase
from darts.utils.missing_values import fill_missing_values
from darts.utils.model_selection import train_test_split
from tabulate import tabulate

from .forecasting_model import forecasting_model
from .helper_func import process_df, common_error_catch
from .unified_one_step_ahead import perform_one_step_ahead_darts, verify_one_step_ahead


class DartsMain(forecasting_model):
    def __init__(
        self,
        estimator,
        model_name,
        test_split,
        frequency,
        seasonality,
        data_path,
        output_path,
        scaling=False,
        interpolation=True,
        f32=False,
    ):
        dm_logger.info("DartsMain __init__() called.")

        # This helps with organising
        dataset_name = str(os.path.basename(data_path)).split(".")[0]
        dataset_name = dataset_name.removeprefix("ftsfr_")

        # Read dataset to a pd.DataFrame
        df = pd.read_parquet(data_path).rename(columns={"id": "unique_id"})
        # Fills missing dates and extends if required
        df, test_split = process_df(df, frequency, seasonality, test_split)

        dm_logger.info("Read and processed dataframe.")

        # This pivot adds all values for an entity as a TS in each column
        proc_df = df.pivot(index="ds", columns="unique_id", values="y")

        # Removing column index
        proc_df.rename_axis(None, axis=1, inplace=True)

        # TimeSeries object is important for darts
        raw_series = TimeSeries.from_dataframe(proc_df)

        dm_logger.info("Created darts TimeSeries object.")

        if f32:
            raw_series = raw_series.astype(np.float32)
            dm_logger.info("Converted to np.float32.")

        # Replace NaNs automatically
        if interpolation:
            raw_series = fill_missing_values(raw_series)
            dm_logger.info("Replaced NaN values.")

        if scaling:
            transformer = Scaler()
            raw_series = transformer.fit_transform(raw_series)
            dm_logger.info("Performed scaling on the dataset.")

        # Splitting into train and test
        train_series, test_series = train_test_split(raw_series, test_size=test_split)
        dm_logger.info("Generated train and test series.")

        # Path to save model once trained
        model_path = output_path / "models" / model_name / dataset_name
        Path(model_path).mkdir(parents=True, exist_ok=True)
        model_path = model_path / "saved_model"  # Without an extension

        dm_logger.info(
            "Created model path and required folders if they " + "weren't present."
        )

        # Path to save forecasts generated after training the model
        forecast_path = output_path / "forecasts" / model_name / dataset_name
        Path(forecast_path).mkdir(parents=True, exist_ok=True)
        forecast_path = forecast_path / "forecasts.parquet"

        dm_logger.info(
            "Created forecast path and required folders if " + "they weren't present."
        )

        # Path to save results which include the error metric
        result_path = output_path / "raw_results" / model_name
        result_path.mkdir(parents=True, exist_ok=True)
        result_path = result_path / str(dataset_name + ".csv")

        dm_logger.info(
            "Created result path and required folders if they " + "weren't present."
        )

        # Names
        self.dataset_name = dataset_name
        self.model_name = model_name

        # Paths
        self.dataset_path = data_path
        self.forecast_path = forecast_path
        self.result_path = result_path
        self.model_path = str(model_path)

        # Series
        self.raw_series = raw_series  # Helps with predictions
        self.train_series = train_series
        self.test_series = test_series
        self.pred_series = None  # None to check if predictions have been made

        # Important variables
        # This is the ratio of test entries to total entries in the df
        self.test_split = test_split
        self.seasonality = seasonality
        self.frequency = frequency

        # Stores the actual model
        self.model = estimator

        # Error metrics
        self.errors = defaultdict(float)

        dm_logger.info("Set up internal variables.")

        print("Object Initialized:")
        print(
            tabulate(
                [
                    ["Model", model_name],
                    ["Dataset", dataset_name],
                    ["Total Entities", self.raw_series.n_components],
                ],
                tablefmt="fancy_grid",
            )
        )

        dm_logger.info("Object fully initialized.")

    @common_error_catch
    def _train_test_split(self, entity_data):
        self.train_series, self.test_series = train_test_split(
            entity_data, test_size=self.test_split
        )
        dm_logger.info("Internal train and test series updated")

    @common_error_catch
    def train(self):
        dm_logger.info("Model training started.")
        self.model.fit(self.train_series)
        dm_logger.info("Model trained.")

    @common_error_catch
    def save_model(self):
        self.model.save(self.model_path)
        dm_logger.info('Model saved to "' + str(self.model_path) + '".')

    def load_model(self):
        self.model = self.model.untrained_model().load(self.model_path)
        dm_logger.info('Model loaded from "' + str(self.model_path) + '".')

    @common_error_catch
    def forecast(self):
        dm_logger.info("Starting unified one-step-ahead forecasting")

        # Use the unified one-step-ahead implementation
        self.pred_series = perform_one_step_ahead_darts(
            model=self.model,
            train_series=self.train_series,
            test_series=self.test_series,
            raw_series=self.raw_series,
        )

        # Verify that we're doing one-step-ahead
        is_valid = verify_one_step_ahead(
            predictions=self.pred_series, test_data=self.test_series, model_type="darts"
        )

        if is_valid:
            dm_logger.info("✓ One-step-ahead forecasting verified")
        else:
            dm_logger.warning("⚠ One-step-ahead forecasting verification failed")

        dm_logger.info("Model inference complete. Internal variable updated.")

    @common_error_catch
    def save_forecast(self):
        # Save to parquet
        temp_df = self.pred_series.to_dataframe(time_as_index=False)
        temp_df.to_parquet(self.forecast_path)
        dm_logger.info('Predictions saved to "' + str(self.forecast_path) + '".')

    def load_forecast(self):
        temp_df = pd.read_parquet(self.forecast_path)
        self.pred_series = TimeSeries.from_dataframe(temp_df, time_col="ds")
        dm_logger.info(
            "Model forecasts loaded from "
            + self.forecast_path
            + ". Internal variable updated."
        )

    def calculate_error(self, metric="MASE"):
        if self.pred_series is None:
            dm_logger.error("calculate_error called without predictions.")
            raise ValueError("Please call self.forecast() first.")
        if metric == "MASE":
            self.errors["MASE"] = mase(
                self.test_series, self.pred_series, self.train_series, self.seasonality
            )
            dm_logger.info("MASE = " + str(self.errors["MASE"]) + ".")
            return self.errors["MASE"]
        else:
            dm_logger.error("calculate_error called for an unsupported metric.")
            raise ValueError("Metric not supported.")
