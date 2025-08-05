"""
The GluontsMain class can help quickly create the necessary objects for
forecasting with Gluonts models. Some code adapted from Monash.
"""

import os
from collections import defaultdict
from pathlib import Path

import pandas as pd
import numpy as np
from tabulate import tabulate
import logging

# Gluonts based imports
from gluonts.dataset.common import ListDataset
from gluonts.dataset.field_names import FieldName
from gluonts.model.predictor import Predictor
from gluonts.dataset.pandas import PandasDataset

from .forecasting_model import forecasting_model
from .helper_func import *
from .unified_one_step_ahead import (
    perform_one_step_ahead_gluonts,
    verify_one_step_ahead,
)

gt_logger = logging.getLogger()


class GluontsMain(forecasting_model):
    def __init__(
        self,
        estimator,
        model_name,
        test_split,
        frequency,
        seasonality,
        data_path,
        output_path,
    ):
        gt_logger.info("GluontsMain __init__ called.")

        # This helps with organising
        dataset_name = str(os.path.basename(data_path)).split(".")[0]
        dataset_name = dataset_name.removeprefix("ftsfr_")

        # Path to save model once trained
        model_path = output_path / "models" / model_name / dataset_name
        Path(model_path).mkdir(parents=True, exist_ok=True)

        gt_logger.info("Created model path and its +" + "folders if they were missing.")

        # Path to save forecasts generated after training the model
        forecast_path = output_path / "forecasts" / model_name / dataset_name
        Path(forecast_path).mkdir(parents=True, exist_ok=True)
        forecast_path = forecast_path / "forecasts.parquet"

        gt_logger.info(
            "Created forecast_path and its " + "folders if they were missing."
        )

        # Path to save results which include the error metric
        result_path = output_path / "raw_results" / model_name
        result_path.mkdir(parents=True, exist_ok=True)
        result_path = result_path / str(dataset_name + ".csv")

        gt_logger.info("Created result_path and its " + "folders if they were missing.")

        # Data pre-processing
        raw_df = pd.read_parquet(data_path)
        raw_df = raw_df.rename(columns={"id": "unique_id"})
        # Fills missing dates and extends if required
        raw_df, test_split = process_df(raw_df, frequency, seasonality, test_split)

        gt_logger.info("Data read and pre-processed.")

        # Fills all the np.nans
        raw_df = custom_interpolate(raw_df)
        gt_logger.info("Data interpolated.")
        # Sorting for consistency
        raw_df = raw_df.sort_values(["unique_id", "ds"])
        # Sorting makes the indices shuffled
        raw_df = raw_df.reset_index(drop=True)
        gt_logger.info("Sorted values along unique_id and then ds.")
        # Some float and double issues
        raw_df["y"] = raw_df["y"].astype(np.float32)
        gt_logger.info("Converted target values to np.float32.")

        # Unique dates defines the number of entries per entity
        # makes calculating test_length and subsequent splits easier
        unique_dates = raw_df["ds"].unique()
        test_length = int(test_split * len(unique_dates))

        # Splitting to train and test
        # Train data for GluonTS is the entire df - test entries
        train_data = raw_df[raw_df["ds"] < unique_dates[-test_length]]
        # Test data for GluonTS is the entire dataframe with the dates as index
        test_data = raw_df.set_index("ds")
        # Train data for GluonTS with dates as index
        train_data = train_data.set_index("ds")

        gt_logger.info("Created train and test series from DataFrame.")

        # Converts to GluonTS format
        test_ds = PandasDataset.from_long_dataframe(
            test_data, target="y", item_id="unique_id"
        )
        train_ds = PandasDataset.from_long_dataframe(
            train_data, target="y", item_id="unique_id"
        )

        gt_logger.info("Converted from DataFrame to PandasDataset.")

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

        gt_logger.info("Internal variables set.")

        print("Object Initialized:")
        print(
            tabulate(
                [
                    ["Model", model_name],
                    ["Dataset", dataset_name],
                    ["Total Entities", len(raw_df["unique_id"].unique())],
                ],
                tablefmt="fancy_grid",
            )
        )

        gt_logger.info("Object fully initialized.")

    def train(self):
        gt_logger.info("Model training started.")
        self.model = self.model.train(training_data=self.train_series)
        gt_logger.info("Model trained.")

    @common_error_catch
    def save_model(self):
        self.model.serialize(self.model_path)
        gt_logger.info('Model saved to "' + str(self.model_path) + '".')

    def load_model(self):
        self.model = Predictor.deserialize(self.model_path)
        gt_logger.info('Model loaded from "' + str(self.model_path) + '".')

    def forecast(self):
        gt_logger.info("Starting unified one-step-ahead forecasting for GluonTS model")

        # Use the unified one-step-ahead implementation
        self.pred_series = perform_one_step_ahead_gluonts(
            model=self.model, train_ds=self.train_series, test_ds=self.test_series
        )

        # For verification, we need the test data in DataFrame format
        # Extract test portion from raw_df
        unique_dates = self.raw_df["ds"].unique()
        test_length = int(self.test_split * len(unique_dates))
        test_df = self.raw_df[self.raw_df["ds"] >= unique_dates[-test_length]]

        # Verify that we're doing one-step-ahead
        is_valid = verify_one_step_ahead(
            predictions=self.pred_series, test_data=test_df, model_type="gluonts"
        )

        if is_valid:
            gt_logger.info("✓ One-step-ahead forecasting verified")
        else:
            gt_logger.warning("⚠ One-step-ahead forecasting verification failed")

        gt_logger.info("Forecasting complete. Internal variable updated.")

    @common_error_catch
    def save_forecast(self):
        self.pred_series.to_parquet(self.forecast_path)
        gt_logger.info('Saved forecasts to "' + str(self.forecast_path) + '".')

    def load_forecast(self):
        self.pred_series = pd.read_parquet(self.forecast_path)
        gt_logger.info('Loaded forecasts from "' + str(self.forecast_path) + '".')

    def calculate_error(self, metric="MASE"):
        if metric == "MASE":
            df = self.raw_df

            unique_dates = df.ds.unique()
            test_length = int(self.test_split * len(unique_dates))

            test_data = df[df.ds >= unique_dates[-test_length]]
            train_data = df[df.ds < unique_dates[-test_length]]

            self.errors["MASE"] = calculate_darts_MASE(
                test_data, train_data, self.pred_series, self.seasonality
            )

            gt_logger.info("MASE: " + str(self.errors["MASE"]) + ".")

            return self.errors["MASE"]
        else:
            gt_logger.error("Metric not supported.")
            raise ValueError("Metric not supported.")

    def print_summary(self):
        print(
            tabulate(
                [
                    ["Model", self.model_name],
                    ["Dataset", self.dataset_name],
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
                "Frequency": [self.frequency],
                "Seasonality": [self.seasonality],
                "Global MASE": [self.errors["MASE"]],
            }
        )

        forecast_res.to_csv(self.result_path)

        gt_logger.info('Saved results to "' + str(self.result_path) + '".')
