"""
The NixtlaMain class can help quickly create the necessary objects for
forecasting with Nixtla's neuralforecast models.

NOTE: Currently doesn't support training on MPS.
"""

import os
from collections import defaultdict
from pathlib import Path

import pandas as pd
from tabulate import tabulate
import logging

from .forecasting_model import forecasting_model
from .helper_func import common_error_catch, calculate_darts_MASE, process_df, custom_interpolate

NixtlaMain_logger = logging.getLogger("Nixtla")

class NixtlaMain(forecasting_model):
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

        NixtlaMain_logger.info("NixtlaMain __init__ called.")

        # This helps with organising
        dataset_name = str(os.path.basename(data_path)).split(".")[0]
        dataset_name = dataset_name.removeprefix("ftsfr_")

        # Path to save model once trained
        model_path = output_path / "models" / model_name / dataset_name
        Path(model_path).mkdir(parents=True, exist_ok=True)

        NixtlaMain_logger.info(
            "Created model path and its folders that were missing."
        )

        # Path to save forecasts generated after training the model
        forecast_path = output_path / "forecasts" / model_name / dataset_name
        Path(forecast_path).mkdir(parents=True, exist_ok=True)
        forecast_path = forecast_path / "forecasts.parquet"

        NixtlaMain_logger.info(
            "Created forecast_path and its folders that were missing."
        )

        # Path to save results which include the error metric
        result_path = output_path / "raw_results" / model_name
        result_path.mkdir(parents=True, exist_ok=True)
        result_path = result_path / str(dataset_name + ".csv")

        NixtlaMain_logger.info(
            "Created result_path and its folders that were missing."
        )

        # Data pre-processing
        df = pd.read_parquet(data_path).rename(columns={"id": "unique_id"})
        train_data, test_data, test_split = process_df(df,
                                                       frequency,
                                                       seasonality,
                                                       test_split)

        NixtlaMain_logger.info("Completed pre-processing and received "+\
                                "train and test data")

        # Names
        self.dataset_name = dataset_name
        self.model_name = model_name

        # Paths
        self.forecast_path = forecast_path
        self.dataset_path = data_path
        self.model_path = str(model_path)
        self.result_path = result_path

        # Dataframes
        self.raw_data = custom_interpolate(pd.concat([train_data, test_data]))
        self.train_data = train_data
        self.test_data = test_data
        self.pred_data = None

        # Important variables
        self.seasonality = seasonality
        self.frequency = frequency


        self.estimator = estimator

        # Stores the nf object
        self.nf = None  # Initialize to None, will be set in train()
        # Error metrics
        self.errors = defaultdict(float)

        NixtlaMain_logger.info("Internal variables set up.")

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

        NixtlaMain_logger.info("Object initialized.")

    def train(self):
        NixtlaMain_logger.info("Model training started.")
        from neuralforecast import NeuralForecast

        self.nf = NeuralForecast(models=[self.estimator],
                                 freq=self.frequency,
                                 local_scaler_type = None)
        self.nf.fit(df=self.train_data)
        NixtlaMain_logger.info("Model trained.")

    @common_error_catch
    def save_model(self):
        self.nf.save(
            self.model_path, model_index=None, overwrite=True, save_dataset=False
        )
        NixtlaMain_logger.info('Model saved to "' + str(self.model_path) + '".')

    def load_model(self):
        from neuralforecast import NeuralForecast

        self.nf = NeuralForecast.load(path=str(self.model_path))
        NixtlaMain_logger.info('Model loaded from "' + str(self.model_path) + '".')

    @common_error_catch
    def forecast(self):
        NixtlaMain_logger.info(
            "Starting unified one-step-ahead forecasting for Nixtla model"
        )
        from .unified_one_step_ahead import (
            perform_one_step_ahead_nixtla,
            verify_one_step_ahead,
        )

        temp_df = perform_one_step_ahead_nixtla(
            nf_model = self.nf,
            train_data = self.train_data,
            test_data = self.test_data,
            raw_data = self.raw_data,
        )

        for col in temp_df.columns:
            if (col != "unique_id") and (col != "ds"):
                break

        self.pred_data = temp_df.rename(columns = {col : "y"})

        # Verify that we're doing one-step-ahead (only if darts is available)
        try:
            # Import for checking if darts is available
            from darts import TimeSeries

            is_valid = verify_one_step_ahead(
                predictions = self.pred_data,
                test_data = self.test_data,
                model_type = "nixtla",
            )

            if is_valid:
                NixtlaMain_logger.info("✓ One-step-ahead forecasting verified")
            else:
                NixtlaMain_logger.warning(
                    "⚠ One-step-ahead forecasting verification failed"
                )
        except ImportError:
            NixtlaMain_logger.warning(
                "⚠ Darts not available - skipping one-step-ahead verification"
            )

        NixtlaMain_logger.info("Forecasting complete. Internal variable updated.")

    @common_error_catch
    def save_forecast(self):
        if self.pred_data is None:
            NixtlaMain_logger.error(
                "No forecasts to save - forecast() must be called first"
            )
            raise ValueError("No forecasts available to save")
        self.pred_data.to_parquet(self.forecast_path, engine="pyarrow")
        NixtlaMain_logger.info('Saved forecasts to "' + str(self.forecast_path) + '".')

    def load_forecast(self):
        temp_df = pd.read_parquet(self.forecast_path)
        # For Nixtla models, we work with pandas DataFrames, not darts TimeSeries
        self.pred_data = temp_df
        NixtlaMain_logger.info(
            'Loaded forecasts from "' + str(self.forecast_path) + '".'
        )

    def calculate_error(self, metric="MASE"):
        if metric == "MASE":
            try:
                self.errors["MASE"] = calculate_darts_MASE(
                    self.test_data,
                    self.train_data,
                    self.pred_data,
                    self.seasonality,
                )
                NixtlaMain_logger.info("MASE: " + str(self.errors["MASE"]) + ".")
                return self.errors["MASE"]
            except (ImportError, ValueError, TypeError) as e:
                NixtlaMain_logger.warning(f"⚠ Cannot calculate MASE: {e}")
                self.errors["MASE"] = float("nan")
                return self.errors["MASE"]
        else:
            raise ValueError("Metric not supported.")

    def print_summary(self):
        print(
            tabulate(
                [
                    ["Model", self.model_name],
                    ["Dataset", self.dataset_name],
                    ["Entities", len(self.train_data["unique_id"].unique())],
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
                "Entities": [len(self.train_data["unique_id"].unique())],
                "Frequency": [self.frequency],
                "Seasonality": [self.seasonality],
                "Global MASE": [self.errors["MASE"]],
            }
        )
        forecast_res.to_csv(self.result_path)

        NixtlaMain_logger.info('Saved results to "' + str(self.result_path) + '".')
