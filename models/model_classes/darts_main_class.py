"""
This contains classes to directly inherit into a model class.

Expected behaviour is that each new object is created for a unique model
and data pair.
"""

import os
from collections import defaultdict
from pathlib import Path

import logging

DartsMain_logger = logging.getLogger("DartsMain")

# from warnings import filterwarnings
# filterwarnings("ignore")

import numpy as np
import pandas as pd
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
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
        # Darts-specific imports only when needed
        from darts import TimeSeries
        from darts.utils.model_selection import train_test_split

        DartsMain_logger.info("DartsMain __init__() called.")

        # This helps with organising
        dataset_name = str(os.path.basename(data_path)).split(".")[0]
        dataset_name = dataset_name.removeprefix("ftsfr_")

        # Read dataset to a pd.DataFrame
        df = pd.read_parquet(data_path).rename(columns={"id": "unique_id"})
        # Fills missing dates and extends if required
        df, test_split = process_df(df, frequency, seasonality, test_split)

        DartsMain_logger.info("Read and processed dataframe.")

        # This pivot adds all values for an entity as a TS in each column
        proc_df = df.pivot(index="ds", columns="unique_id", values="y")

        # Removing column index
        proc_df.rename_axis(None, axis=1, inplace=True)

        # TimeSeries object is important for darts
        raw_series = TimeSeries.from_dataframe(proc_df)

        DartsMain_logger.info("Created darts TimeSeries object.")

        if f32:
            raw_series = raw_series.astype(np.float32)
            DartsMain_logger.info("Converted to np.float32.")

        # Replace NaNs automatically
        if interpolation:
            raw_series = fill_missing_values(raw_series)
            DartsMain_logger.info("Replaced NaN values.")

        if scaling:
            transformer = Scaler()
            raw_series = transformer.fit_transform(raw_series)
            DartsMain_logger.info("Performed scaling on the dataset.")

        # Splitting into train and test
        train_series, test_series = train_test_split(raw_series, test_size=test_split)
        DartsMain_logger.info("Generated train and test series.")

        # Path to save model once trained
        model_path = output_path / "models" / model_name / dataset_name
        Path(model_path).mkdir(parents=True, exist_ok=True)
        model_path = model_path / "saved_model"  # Without an extension

        DartsMain_logger.info(
            "Created model path and required folders if they " + "weren't present."
        )

        # Path to save forecasts generated after training the model
        forecast_path = output_path / "forecasts" / model_name / dataset_name
        Path(forecast_path).mkdir(parents=True, exist_ok=True)
        forecast_path = forecast_path / "forecasts.parquet"

        DartsMain_logger.info(
            "Created forecast path and required folders if " + "they weren't present."
        )

        # Path to save results which include the error metric
        result_path = output_path / "raw_results" / model_name
        result_path.mkdir(parents=True, exist_ok=True)
        result_path = result_path / str(dataset_name + ".csv")

        DartsMain_logger.info(
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

        DartsMain_logger.info("Set up internal variables.")

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

        DartsMain_logger.info("Object fully initialized.")

    @common_error_catch
    def _train_test_split(self, entity_data):
        self.train_series, self.test_series = train_test_split(
            entity_data, test_size=self.test_split
        )
        DartsMain_logger.info("Internal train and test series updated")

    @common_error_catch
    def train(self):
        DartsMain_logger.info("Model training started.")
        self.model.fit(self.train_series)
        DartsMain_logger.info("Model trained.")

    @common_error_catch
    def save_model(self):
        self.model.save(self.model_path)
        DartsMain_logger.info('Model saved to "' + str(self.model_path) + '".')

    def load_model(self):
        self.model = self.model.untrained_model().load(self.model_path)
        DartsMain_logger.info('Model loaded from "' + str(self.model_path) + '".')

    @common_error_catch
    def forecast(self):
        DartsMain_logger.info("Starting unified one-step-ahead forecasting")

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
            DartsMain_logger.info("✓ One-step-ahead forecasting verified")
        else:
            DartsMain_logger.warning("⚠ One-step-ahead forecasting verification failed")

        DartsMain_logger.info("Model inference complete. Internal variable updated.")

    @common_error_catch
    def save_forecast(self):
        # Add debugging to understand the type of pred_series
        DartsMain_logger.info(f"pred_series type: {type(self.pred_series)}")
        if hasattr(self.pred_series, "shape"):
            DartsMain_logger.info(f"pred_series shape: {self.pred_series.shape}")
        elif isinstance(self.pred_series, list):
            DartsMain_logger.info(
                f"pred_series is a list with {len(self.pred_series)} elements"
            )
            # If it's still a list, try to concatenate it
            if len(self.pred_series) > 0:
                from darts import TimeSeries

                self.pred_series = TimeSeries.concatenate(self.pred_series, axis=0)
                DartsMain_logger.info(
                    "Concatenated list of TimeSeries into single TimeSeries"
                )
            else:
                raise ValueError("pred_series is an empty list")

        # Save to parquet
        temp_df = self.pred_series.to_dataframe(time_as_index=False)
        temp_df.to_parquet(self.forecast_path)
        DartsMain_logger.info('Predictions saved to "' + str(self.forecast_path) + '".')

    def load_forecast(self):
        temp_df = pd.read_parquet(self.forecast_path)
        self.pred_series = TimeSeries.from_dataframe(temp_df, time_col="ds")
        DartsMain_logger.info(
            "Model forecasts loaded from "
            + self.forecast_path
            + ". Internal variable updated."
        )

    def calculate_error(self, metric="MASE"):
        if self.pred_series is None:
            DartsMain_logger.error("calculate_error called without predictions.")
            raise ValueError("Please call self.forecast() first.")

        # Add debugging information
        DartsMain_logger.info(
            f"test_series components: {self.test_series.n_components}"
        )
        DartsMain_logger.info(
            f"pred_series components: {self.pred_series.n_components}"
        )
        DartsMain_logger.info(f"test_series shape: {self.test_series.shape}")
        DartsMain_logger.info(f"pred_series shape: {self.pred_series.shape}")

        if metric == "MASE":
            from darts.metrics import mase

            try:
                # For MASE, the insample series needs to:
                # 1. Start before pred_series
                # 2. Extend until at least one time step before pred_series starts

                # Print debug info
                print(
                    f"DEBUG: train_series range: {self.train_series.start_time()} to {self.train_series.end_time()}"
                )
                print(
                    f"DEBUG: test_series range: {self.test_series.start_time()} to {self.test_series.end_time()}"
                )
                print(
                    f"DEBUG: pred_series range: {self.pred_series.start_time()} to {self.pred_series.end_time()}"
                )

                # Since we're doing one-step-ahead, predictions should align with test
                # But MASE needs historical data. Let's use the full series up to pred start
                pred_start = self.pred_series.start_time()

                # Get the full historical series up to the prediction start
                # We need to include data up to one step before predictions
                try:
                    # Get the index of pred_start in raw_series
                    pred_start_idx = self.raw_series.get_index_at_point(pred_start)
                    if pred_start_idx > 0:
                        # Slice raw_series to include everything before pred_start
                        historical_series = self.raw_series[:pred_start_idx]
                    else:
                        # Fallback to train_series
                        historical_series = self.train_series
                except:
                    # If any issues, fall back to train_series
                    print("DEBUG: Failed to slice raw_series, using train_series")
                    historical_series = self.train_series

                self.errors["MASE"] = mase(
                    self.test_series,
                    self.pred_series,
                    historical_series,
                    self.seasonality,
                )
                DartsMain_logger.info("MASE = " + str(self.errors["MASE"]) + ".")
                return self.errors["MASE"]
            except ValueError as e:
                if "cannot use MASE with periodical signals" in str(e):
                    DartsMain_logger.warning(
                        "MASE failed due to periodical signals, falling back to MAE"
                    )
                    from darts.metrics import mae

                    self.errors["MAE"] = mae(self.test_series, self.pred_series)
                    DartsMain_logger.info("MAE = " + str(self.errors["MAE"]) + ".")
                    return self.errors["MAE"]
                else:
                    raise e
        elif metric == "MAE":
            from darts.metrics import mae

            self.errors["MAE"] = mae(self.test_series, self.pred_series)
            DartsMain_logger.info("MAE = " + str(self.errors["MAE"]) + ".")
            return self.errors["MAE"]
        else:
            DartsMain_logger.error("calculate_error called for an unsupported metric.")
            raise ValueError("Metric not supported.")
