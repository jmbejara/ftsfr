"""
The GluontsMain class can help quickly create the necessary objects for
forecasting with GluonTS models. Some code adapted from Monash.
"""

import os
from collections import defaultdict
from pathlib import Path

import pandas as pd
import numpy as np
from tabulate import tabulate
import logging

GluontsMain_logger = logging.getLogger("GluontsMain")

from .forecasting_model import forecasting_model
from .helper_func import process_df, common_error_catch

# GluonTS-specific imports are moved inside methods

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
        # GluonTS-specific imports only when needed
        from gluonts.dataset.pandas import PandasDataset

        GluontsMain_logger.info("GluontsMain __init__ called.")

        # This helps with organising
        dataset_name = str(os.path.basename(data_path)).split(".")[0]
        dataset_name = dataset_name.removeprefix("ftsfr_")

        # Path to save model once trained
        model_path = output_path / "models" / model_name / dataset_name
        Path(model_path).mkdir(parents=True, exist_ok=True)

        GluontsMain_logger.info(
            "Created model path and its folders that were missing."
        )

        # Path to save forecasts generated after training the model
        forecast_path = output_path / "forecasts" / model_name / dataset_name
        Path(forecast_path).mkdir(parents=True, exist_ok=True)
        forecast_path = forecast_path / "forecasts.parquet"

        GluontsMain_logger.info(
            "Created forecast_path and its folders that were missing."
        )

        # Path to save results which include the error metric
        result_path = output_path / "raw_results" / model_name
        result_path.mkdir(parents=True, exist_ok=True)
        result_path = result_path / str(dataset_name + ".csv")

        GluontsMain_logger.info(
            "Created result_path and its folders that were missing."
        )

        # Data pre-processing
        raw_df = pd.read_parquet(data_path)
        raw_df = raw_df.rename(columns={"id": "unique_id"})
        # Fills missing dates and extends if required
        train_data, test_data, test_split = process_df(raw_df,
                                                           frequency,
                                                           seasonality,
                                                           test_split)
        
        GluontsMain_logger.info("Completed pre-processing and received "+\
                                "train and test data")

        # Sorting for consistency
        train_data = train_data.sort_values(["unique_id", "ds"]).\
                                    reset_index(drop=True).\
                                    set_index("ds")
        
        GluontsMain_logger.info("Sorted train data.")

        raw_df = pd.concat([train_data, test_data]).\
                    sort_values(["unique_id", "ds"]).\
                    reset_index(drop = True)
        
        GluontsMain_logger.info("Created raw_df from train and test data.")

        # Test data for GluonTS is the entire dataframe with the dates as index
        test_data = raw_df.set_index("ds")

        GluontsMain_logger.info("Created train and test series from DataFrame.")

        # Convert frequency for GluonTS compatibility (ME -> M)
        def convert_frequency_for_gluonts(freq):
            """Convert frequency strings for GluonTS compatibility."""
            if freq == "ME":
                return "M"  # Month end -> Month
            return freq

        gluonts_frequency = convert_frequency_for_gluonts(frequency)

        # Converts to GluonTS format
        test_ds = PandasDataset.from_long_dataframe(
            test_data, target="y", item_id="unique_id", freq=gluonts_frequency
        )
        train_ds = PandasDataset.from_long_dataframe(
            train_data, target="y", item_id="unique_id", freq=gluonts_frequency
        )

        GluontsMain_logger.info("Converted from DataFrame to PandasDataset.")

        # Names
        self.model_name = model_name
        self.dataset_name = dataset_name

        # Paths
        self.model_path = model_path
        self.dataset_path = data_path
        self.forecast_path = forecast_path
        self.result_path = result_path

        # Series
        self.test_data = test_ds
        self.train_data = train_ds
        self.pred_data = None
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

        GluontsMain_logger.info("Internal variables set.")

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

        GluontsMain_logger.info("Object fully initialized.")

    def train(self):
        GluontsMain_logger.info("Model training started.")
        self.model = self.model.train(training_data=self.train_data)
        GluontsMain_logger.info("Model trained.")

    @common_error_catch
    def save_model(self):
        self.model.serialize(self.model_path)
        GluontsMain_logger.info('Model saved to "' + str(self.model_path) + '".')

    def load_model(self):
        from gluonts.model.predictor import Predictor

        self.model = Predictor.deserialize(self.model_path)
        GluontsMain_logger.info('Model loaded from "' + str(self.model_path) + '".')

    def forecast(self):
        from .unified_one_step_ahead import (
            perform_one_step_ahead_gluonts,
            verify_one_step_ahead,
        )

        GluontsMain_logger.info(
            "Starting unified one-step-ahead forecasting for GluonTS model"
        )

        # Use the unified one-step-ahead implementation
        self.pred_data = perform_one_step_ahead_gluonts(
            model=self.model, train_ds=self.train_data, test_ds=self.test_data
        )

        # For verification, we need the test data in DataFrame format
        # Extract test portion from raw_df
        unique_dates = self.raw_df["ds"].unique()
        test_length = int(self.test_split * len(unique_dates))
        test_df = self.raw_df[self.raw_df["ds"] >= unique_dates[-test_length]]

        # Verify that we're doing one-step-ahead
        is_valid = verify_one_step_ahead(
            predictions=self.pred_data, test_data=test_df, model_type="gluonts"
        )

        if is_valid:
            GluontsMain_logger.info("✓ One-step-ahead forecasting verified")
        else:
            GluontsMain_logger.warning(
                "⚠ One-step-ahead forecasting verification failed"
            )

        GluontsMain_logger.info("Forecasting complete. Internal variable updated.")

    @common_error_catch
    def save_forecast(self):
        self.pred_data.to_parquet(self.forecast_path)
        GluontsMain_logger.info('Saved forecasts to "' + str(self.forecast_path) + '".')

    def load_forecast(self):
        self.pred_data = pd.read_parquet(self.forecast_path)
        GluontsMain_logger.info(
            'Loaded forecasts from "' + str(self.forecast_path) + '".'
        )

    def calculate_gluonts_mase(self, test_data, train_data, pred_data, seasonality):
        """
        Calculate MASE for GluonTS models without depending on darts.

        Args:
            test_data: DataFrame with test data
            train_data: DataFrame with training data
            pred_data: DataFrame with predictions
            seasonality: Seasonality period

        Returns:
            float: MASE score
        """
        GluontsMain_logger.info("Calculating MASE for GluonTS model")

        # Calculate mean absolute error of predictions
        # Merge test data with predictions on ds and unique_id
        merged = test_data.merge(
            pred_data, on=["ds", "unique_id"], suffixes=("_actual", "_pred")
        )

        # Calculate absolute errors
        merged["abs_error"] = np.abs(merged["y_actual"] - merged["y_pred"])
        mae_forecast = merged["abs_error"].mean()

        # Calculate mean absolute error of naive forecast on training data
        # For each series, calculate the naive forecast error
        naive_errors = []

        for series_id in train_data["unique_id"].unique():
            series_data = train_data[train_data["unique_id"] == series_id].sort_values(
                "ds"
            )

            if len(series_data) > seasonality:
                # Calculate naive forecast (value from seasonality periods ago)
                series_data = series_data.reset_index(drop=True)
                naive_forecast = series_data["y"].shift(seasonality)
                actual_values = series_data["y"]

                # Calculate absolute errors for naive forecast
                naive_abs_errors = np.abs(actual_values - naive_forecast)
                # Remove NaN values (first seasonality periods)
                naive_abs_errors = naive_abs_errors.dropna()

                if len(naive_abs_errors) > 0:
                    naive_errors.extend(naive_abs_errors.tolist())

        if len(naive_errors) == 0:
            GluontsMain_logger.warning(
                "No naive forecast errors calculated, using fallback"
            )
            mae_naive = 1.0  # Fallback value
        else:
            mae_naive = np.mean(naive_errors)

        # Calculate MASE
        mase = mae_forecast / mae_naive if mae_naive > 0 else float("inf")

        GluontsMain_logger.info(
            f"MASE calculated: {mase:.4f} (MAE_forecast: {mae_forecast:.4f}, MAE_naive: {mae_naive:.4f})"
        )

        return mase

    def calculate_error(self, metric="MASE"):
        if metric == "MASE":
            df = self.raw_df

            unique_dates = df.ds.unique()
            test_length = int(self.test_split * len(unique_dates))

            test_data = df[df.ds >= unique_dates[-test_length]]
            train_data = df[df.ds < unique_dates[-test_length]]

            self.errors["MASE"] = self.calculate_gluonts_mase(
                test_data, train_data, self.pred_data, self.seasonality
            )

            GluontsMain_logger.info("MASE: " + str(self.errors["MASE"]) + ".")

            return self.errors["MASE"]
        else:
            GluontsMain_logger.error("Metric not supported.")
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

        GluontsMain_logger.info('Saved results to "' + str(self.result_path) + '".')
