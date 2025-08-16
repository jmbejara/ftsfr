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
    ):
        # Darts-specific imports only when needed
        from darts import TimeSeries

        DartsMain_logger.info("DartsMain __init__() called.")

        # This helps with organising
        dataset_name = str(os.path.basename(data_path)).split(".")[0]
        dataset_name = dataset_name.removeprefix("ftsfr_")

        # Read dataset to a pd.DataFrame
        df = pd.read_parquet(data_path).rename(columns={"id": "unique_id"})

        # Fills missing dates and extends if required
        train_data, test_data, test_split = process_df(df,
                                                       frequency,
                                                       seasonality,
                                                       test_split)

        DartsMain_logger.info("Completed pre-processing and received "+\
                              "train and test data")

        raw_df = pd.concat([train_data, test_data])
        raw_df = raw_df.pivot(index="ds",
                              columns="unique_id",
                              values="y")

        raw_data = TimeSeries.from_dataframe(raw_df)

        DartsMain_logger.info("Made raw_df TimeSeries.")

        # This pivot adds all values for an entity as a TS in each column
        train_data = train_data.pivot(index="ds", columns="unique_id", values="y")
        # Removing column index
        train_data.rename_axis(None, axis=1, inplace=True)

        test_data = test_data.pivot(index="ds", columns="unique_id", values="y")
        # Removing column index
        test_data.rename_axis(None, axis=1, inplace=True)

        DartsMain_logger.info("Pivot both train and test data.")

        # Splitting into train and test
        train_data = TimeSeries.from_dataframe(train_data)
        test_data = TimeSeries.from_dataframe(test_data)

        DartsMain_logger.info("Made TimeSeries objects for train and test.")

        # Path to save model once trained
        model_path = output_path / "models" / model_name / dataset_name
        Path(model_path).mkdir(parents=True, exist_ok=True)
        model_path = model_path / "saved_model"  # Without an extension

        DartsMain_logger.info(
            "Created model path and required folders that weren't present."
        )

        # Path to save forecasts generated after training the model
        forecast_path = output_path / "forecasts" / model_name / dataset_name
        Path(forecast_path).mkdir(parents=True, exist_ok=True)
        forecast_path = forecast_path / "forecasts.parquet"

        DartsMain_logger.info(
            "Created forecast path and required folders that weren't present."
        )

        # Path to save results which include the error metric
        result_path = output_path / "raw_results" / model_name
        result_path.mkdir(parents=True, exist_ok=True)
        result_path = result_path / str(dataset_name + ".csv")

        DartsMain_logger.info(
            "Created result path and required folders that weren't present."
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
        self.raw_data = raw_data # Helps with predictions
        self.train_data = train_data
        self.test_data = test_data
        self.pred_data = None # None to check if predictions have been made

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
                    ["Total Entities", self.train_data.n_components],
                ],
                tablefmt="fancy_grid",
            )
        )

        DartsMain_logger.info("Object fully initialized.")

    @common_error_catch
    def train(self):
        DartsMain_logger.info("Model training started.")
        self.model.fit(self.train_data)
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
        self.pred_data = perform_one_step_ahead_darts(
            model = self.model,
            test_data = self.test_data,
            raw_data = self.raw_data,
        )

        # Verify that we're doing one-step-ahead
        is_valid = verify_one_step_ahead(
            predictions=self.pred_data, test_data=self.test_data, model_type="darts"
        )

        if is_valid:
            DartsMain_logger.info("✓ One-step-ahead forecasting verified")
        else:
            DartsMain_logger.warning("⚠ One-step-ahead forecasting verification failed")

        DartsMain_logger.info("Model inference complete. Internal variable updated.")

    @common_error_catch
    def save_forecast(self):
        # Add debugging to understand the type of pred_data
        DartsMain_logger.info(f"pred_data type: {type(self.pred_data)}")
        if hasattr(self.pred_data, "shape"):
            DartsMain_logger.info(f"pred_data shape: {self.pred_data.shape}")
        elif isinstance(self.pred_data, list):
            DartsMain_logger.info(
                f"pred_data is a list with {len(self.pred_data)} elements"
            )
            # If it's still a list, try to concatenate it
            if len(self.pred_data) > 0:
                from darts import TimeSeries

                self.pred_data = TimeSeries.concatenate(self.pred_data, axis=0)
                DartsMain_logger.info(
                    "Concatenated list of TimeSeries into single TimeSeries"
                )
            else:
                raise ValueError("pred_data is an empty list")

        # Save to parquet
        temp_df = self.pred_data.to_dataframe(time_as_index=False)
        temp_df.to_parquet(self.forecast_path)
        DartsMain_logger.info('Predictions saved to "' + str(self.forecast_path) + '".')

    def load_forecast(self):
        temp_df = pd.read_parquet(self.forecast_path).rename(columns = {"time": "ds"})
        self.pred_data = TimeSeries.from_dataframe(temp_df, time_col="ds")
        DartsMain_logger.info(
            "Model forecasts loaded from "
            + str(self.forecast_path)
            + ". Internal variable updated."
        )

    def calculate_error(self, metric="MASE"):
        if self.pred_data is None:
            DartsMain_logger.error("calculate_error called without predictions.")
            raise ValueError("Please call self.forecast() first.")

        # Add debugging information
        DartsMain_logger.info(
            f"test_data components: {self.test_data.n_components}"
        )
        DartsMain_logger.info(
            f"pred_data components: {self.pred_data.n_components}"
        )
        DartsMain_logger.info(f"test_data shape: {self.test_data.shape}")
        DartsMain_logger.info(f"pred_data shape: {self.pred_data.shape}")

        if metric == "MASE":
            from darts.metrics import mase

            try:
                # For MASE, the insample series needs to:
                # 1. Start before pred_data
                # 2. Extend until at least one time step before pred_data starts

                # Print debug info
                print(
                    f"DEBUG: train_data range: {self.train_data.start_time()} to {self.train_data.end_time()}"
                )
                print(
                    f"DEBUG: test_data range: {self.test_data.start_time()} to {self.test_data.end_time()}"
                )
                print(
                    f"DEBUG: pred_data range: {self.pred_data.start_time()} to {self.pred_data.end_time()}"
                )

                temp = mase(
                    self.test_data,
                    self.pred_data,
                    self.train_data,
                    self.seasonality,
                )

                if temp == np.nan:
                    temp = 0.0

                self.errors["MASE"] = temp

                DartsMain_logger.info("MASE = " + str(temp) + ".")
                return self.errors["MASE"]
            except ValueError as e:
                if "cannot use MASE with periodical signals" in str(e):
                    DartsMain_logger.warning(
                        "MASE failed due to periodical signals, falling back to MAE"
                    )
                    from darts.metrics import mae

                    self.errors["MAE"] = mae(self.test_data, self.pred_data)
                    DartsMain_logger.info("MAE = " + str(self.errors["MAE"]) + ".")
                    return self.errors["MAE"]
                else:
                    raise e
        elif metric == "MAE":
            from darts.metrics import mae

            self.errors["MAE"] = mae(self.test_data, self.pred_data)
            DartsMain_logger.info("MAE = " + str(self.errors["MAE"]) + ".")
            return self.errors["MAE"]
        else:
            DartsMain_logger.error("calculate_error called for an unsupported metric.")
            raise ValueError("Metric not supported.")
