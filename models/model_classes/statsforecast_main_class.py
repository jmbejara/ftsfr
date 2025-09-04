"""
The StatsForecastMain class can help quickly create the necessary objects for
forecasting with Nixtla's statsforecast models.

Supports traditional statistical models like AutoARIMA, ETS, etc.
"""

import os
from collections import defaultdict
from pathlib import Path

import pandas as pd
from tabulate import tabulate
import logging

from .forecasting_model import forecasting_model
from .helper_func import (
    common_error_catch,
    calculate_darts_MASE,
    process_df,
    custom_interpolate,
)

StatsForecastMain_logger = logging.getLogger("StatsForecast")


class StatsForecastMain(forecasting_model):
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
        StatsForecastMain_logger.info("StatsForecastMain __init__ called.")

        # This helps with organizing
        dataset_name = str(os.path.basename(data_path)).split(".")[0]
        dataset_name = dataset_name.removeprefix("ftsfr_")

        # Path to save model checkpoints (though StatsForecast models are lightweight)
        model_path = (
            output_path
            / "forecasting"
            / "model_checkpoints"
            / model_name
            / dataset_name
        )
        Path(model_path).mkdir(parents=True, exist_ok=True)

        StatsForecastMain_logger.info(
            "Created model checkpoint path and its folders that were missing."
        )

        # Path to save forecasts generated after training the model
        forecast_path = (
            output_path / "forecasting" / "forecasts" / model_name / dataset_name
        )
        Path(forecast_path).mkdir(parents=True, exist_ok=True)
        forecast_path = forecast_path / "forecasts.parquet"

        StatsForecastMain_logger.info(
            "Created forecast_path and its folders that were missing."
        )

        # Path to save error metrics
        result_path = output_path / "forecasting" / "error_metrics" / model_name
        result_path.mkdir(parents=True, exist_ok=True)
        result_path = result_path / str(dataset_name + ".csv")

        StatsForecastMain_logger.info(
            "Created error metrics path and its folders that were missing."
        )

        # Data pre-processing
        df = pd.read_parquet(data_path).rename(columns={"id": "unique_id"})
        train_data, test_data, test_split = process_df(
            df, frequency, seasonality, test_split
        )

        StatsForecastMain_logger.info(
            "Completed pre-processing and received " + "train and test data"
        )

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

        # Stores the sf object
        self.sf = None  # Initialize to None, will be set in train()
        # Error metrics
        self.errors = defaultdict(float)

        StatsForecastMain_logger.info("Internal variables set up.")

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

        StatsForecastMain_logger.info("Object initialized.")

    def train(self):
        StatsForecastMain_logger.info("Model training started.")
        from statsforecast import StatsForecast

        # StatsForecast expects frequency as string
        self.sf = StatsForecast(
            models=[self.estimator], 
            freq=self.frequency,
            n_jobs=1
        )
        self.sf.fit(df=self.train_data)
        StatsForecastMain_logger.info("Model trained.")

    @common_error_catch
    def save_model(self):
        # StatsForecast models are typically lightweight and don't require explicit saving
        # We'll save the model configuration for consistency
        import pickle
        with open(Path(self.model_path) / "model.pkl", "wb") as f:
            pickle.dump(self.sf, f)
        StatsForecastMain_logger.info('Model saved to "' + str(self.model_path) + '".')

    def load_model(self):
        # Load the saved StatsForecast model
        import pickle
        with open(Path(self.model_path) / "model.pkl", "rb") as f:
            self.sf = pickle.load(f)
        StatsForecastMain_logger.info('Model loaded from "' + str(self.model_path) + '".')

    @common_error_catch
    def forecast(self):
        StatsForecastMain_logger.info(
            "Starting unified one-step-ahead forecasting for StatsForecast model"
        )
        from .unified_one_step_ahead import (
            perform_one_step_ahead_statsforecast,
            verify_one_step_ahead,
        )

        temp_df = perform_one_step_ahead_statsforecast(
            sf_model=self.sf,
            train_data=self.train_data,
            test_data=self.test_data,
            raw_data=self.raw_data,
        )

        for col in temp_df.columns:
            if (col != "unique_id") and (col != "ds"):
                break

        self.pred_data = temp_df.rename(columns={col: "y"})

        # Verify that we're doing one-step-ahead (only if darts is available)
        try:
            # Import for checking if darts is available
            from darts import TimeSeries

            is_valid = verify_one_step_ahead(
                predictions=self.pred_data,
                test_data=self.test_data,
                model_type="statsforecast",
            )

            if is_valid:
                StatsForecastMain_logger.info("✓ One-step-ahead forecasting verified")
            else:
                StatsForecastMain_logger.warning(
                    "⚠ One-step-ahead forecasting verification failed"
                )
        except ImportError:
            StatsForecastMain_logger.warning(
                "⚠ Darts not available - skipping one-step-ahead verification"
            )

        StatsForecastMain_logger.info("Forecasting complete. Internal variable updated.")

    @common_error_catch
    def save_forecast(self):
        if self.pred_data is None:
            StatsForecastMain_logger.error(
                "No forecasts to save - forecast() must be called first"
            )
            raise ValueError("No forecasts available to save")
        self.pred_data.to_parquet(self.forecast_path, engine="pyarrow")
        StatsForecastMain_logger.info('Saved forecasts to "' + str(self.forecast_path) + '".')

    def load_forecast(self):
        temp_df = pd.read_parquet(self.forecast_path)
        # For StatsForecast models, we work with pandas DataFrames
        self.pred_data = temp_df
        StatsForecastMain_logger.info(
            'Loaded forecasts from "' + str(self.forecast_path) + '".'
        )

    def calculate_error(self):
        """Calculate all error metrics (MASE, MAE, RMSE) for the forecasting results.

        Returns:
            dict: Dictionary containing all calculated error metrics
        """
        # Calculate MASE
        try:
            self.errors["MASE"] = calculate_darts_MASE(
                self.test_data,
                self.train_data,
                self.pred_data,
                self.seasonality,
            )
            StatsForecastMain_logger.info("MASE: " + str(self.errors["MASE"]) + ".")
        except (ImportError, ValueError, TypeError) as e:
            StatsForecastMain_logger.warning(f"⚠ Cannot calculate MASE: {e}")
            self.errors["MASE"] = 0.0

        # Calculate MAE and RMSE using the Darts conversion helper
        try:
            from .helper_func import calculate_darts_MAE, calculate_darts_RMSE

            self.errors["MAE"] = calculate_darts_MAE(
                self.test_data,
                self.pred_data,
            )
            StatsForecastMain_logger.info("MAE: " + str(self.errors["MAE"]) + ".")

            self.errors["RMSE"] = calculate_darts_RMSE(
                self.test_data,
                self.pred_data,
            )
            StatsForecastMain_logger.info("RMSE: " + str(self.errors["RMSE"]) + ".")

        except (ImportError, ValueError, TypeError) as e:
            StatsForecastMain_logger.warning(f"⚠ Cannot calculate MAE/RMSE: {e}")
            self.errors["MAE"] = 0.0
            self.errors["RMSE"] = 0.0

        return self.errors

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
                    ["Global MAE", self.errors["MAE"]],
                    ["Global RMSE", self.errors["RMSE"]],
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
                "Global_MASE": [self.errors["MASE"]],
                "Global_MAE": [self.errors["MAE"]],
                "Global_RMSE": [self.errors["RMSE"]],
            }
        )
        forecast_res.to_csv(self.result_path)

        StatsForecastMain_logger.info('Saved results to "' + str(self.result_path) + '".')