"""
The DartsLocal class is specifically designed for Local forecasting models
implemented using darts. Examples include ARIMA, TBATS, ETS, and Theta.

These models train separately for each time series entity, so workflow
separation works differently - we save model configurations rather than
trained models.
"""

import statistics
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from tabulate import tabulate
from tqdm import tqdm
import logging

DartsLocal_logger = logging.getLogger("DartsLocal")

from .darts_main_class import DartsMain
from .helper_func import common_error_catch


class DartsLocal(DartsMain):
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
        # Import Darts-specific utilities only when needed

        DartsLocal_logger.info("DartsLocal object initialized.")

        super().__init__(
            estimator,
            model_name,
            test_split,
            frequency,
            seasonality,
            data_path,
            output_path,
        )

        DartsLocal_logger.info("DartsLocal super().__init__() complete.")

        # Initialize metric tracking for all three metrics
        self.median_mase = np.nan
        self.median_mae = np.nan
        self.median_rmse = np.nan
        self.mase_list = []
        self.mae_list = []
        self.rmse_list = []
        self.model_path += ".pkl"

        # Store model configuration for workflow separation
        self.model_config = {
            "class": self.model.__class__,
            "params": self.model._model_params
            if hasattr(self.model, "_model_params")
            else {},
        }

        DartsLocal_logger.info("DartsLocal internal variables set.")

    @common_error_catch
    def forecast_workflow(self):
        DartsLocal_logger.info(
            "forecast_workflow called. Predictions made for each "
            + "entity separately."
        )

        raw_data = self.raw_data.copy()
        train_data = self.train_data.copy()
        test_data = self.test_data.copy()

        # Training on each entity and calculating MASE
        self.print_sep()
        DartsLocal_logger.info("Starting loop for the workflow on each entity.")
        for id in tqdm(train_data.columns):
            DartsLocal_logger.info("Processing id: " + id + ".")

            # Updating internal variables to only contain the current series
            self.train_data = train_data[[id]].copy()
            self.test_data = test_data[[id]].copy()
            self.raw_data = raw_data[[id]].copy()

            # Updates internal train and test series
            self.train()
            self.forecast()
            error_metrics = self.calculate_error()
            DartsLocal_logger.info(
                f"MASE: {error_metrics['MASE']}, MAE: {error_metrics['MAE']}, RMSE: {error_metrics['RMSE']}"
            )
            # Resets the model
            self.model = self.model.untrained_model()

            # Store all three metrics for this entity
            if error_metrics["MASE"] is not None and not np.isnan(
                error_metrics["MASE"]
            ):
                self.mase_list.append(error_metrics["MASE"])
            if error_metrics["MAE"] is not None and not np.isnan(error_metrics["MAE"]):
                self.mae_list.append(error_metrics["MAE"])
            if error_metrics["RMSE"] is not None and not np.isnan(
                error_metrics["RMSE"]
            ):
                self.rmse_list.append(error_metrics["RMSE"])

        self.print_sep()
        self.save_forecast()
        self.raw_data = raw_data
        self.train_data = train_data
        self.test_data = test_data

        # Calculate mean and median for all three metrics
        if self.mase_list:
            self.errors["MASE"] = sum(self.mase_list) / len(self.mase_list)
            self.median_mase = statistics.median(self.mase_list)
        else:
            self.errors["MASE"] = None
            self.median_mase = None

        if self.mae_list:
            self.errors["MAE"] = sum(self.mae_list) / len(self.mae_list)
            self.median_mae = statistics.median(self.mae_list)
        else:
            self.errors["MAE"] = None
            self.median_mae = None

        if self.rmse_list:
            self.errors["RMSE"] = sum(self.rmse_list) / len(self.rmse_list)
            self.median_rmse = statistics.median(self.rmse_list)
        else:
            self.errors["RMSE"] = None
            self.median_rmse = None

        DartsLocal_logger.info(
            f"Mean MASE: {self.errors['MASE']} | Median MASE: {self.median_mase} | "
            f"Mean MAE: {self.errors['MAE']} | Median MAE: {self.median_mae} | "
            f"Mean RMSE: {self.errors['RMSE']} | Median RMSE: {self.median_rmse}"
        )

    def main_workflow(self):
        DartsLocal_logger.info("main_workflow called.")
        self.forecast_workflow()
        self.print_summary()
        self.save_results()

    def print_summary(self):
        DartsLocal_logger.info("print_summary called.")
        print(
            tabulate(
                [
                    ["Model", self.model_name],
                    ["Dataset", self.dataset_name],
                    [
                        "Entities",
                        max(
                            len(self.mase_list), len(self.mae_list), len(self.rmse_list)
                        ),
                    ],
                    ["Frequency", self.frequency],
                    ["Seasonality", self.seasonality],
                    ["Mean MASE", self.errors["MASE"]],
                    ["Median MASE", self.median_mase],
                    ["Mean MAE", self.errors["MAE"]],
                    ["Median MAE", self.median_mae],
                    ["Mean RMSE", self.errors["RMSE"]],
                    ["Median RMSE", self.median_rmse],
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
                "Entities": [
                    max(len(self.mase_list), len(self.mae_list), len(self.rmse_list))
                ],
                "Seasonality": [self.seasonality],
                "Mean_MASE": [self.errors["MASE"]],
                "Median_MASE": [self.median_mase],
                "Mean_MAE": [self.errors["MAE"]],
                "Median_MAE": [self.median_mae],
                "Mean_RMSE": [self.errors["RMSE"]],
                "Median_RMSE": [self.median_rmse],
            }
        )

        forecast_res.to_csv(self.result_path)
        DartsLocal_logger.info("Results saved to " + str(self.result_path))

    def save_model(self):
        """Save model configuration (not trained models) for DartsLocal.

        Since DartsLocal trains separately for each time series,
        we only save the configuration to recreate models during inference.
        """
        config_path = Path(self.model_path).with_suffix(".config")
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "wb") as f:
            pickle.dump(
                {
                    "model_config": self.model_config,
                    "model_name": self.model_name,
                    "seasonality": self.seasonality,
                    "frequency": self.frequency,
                },
                f,
            )
        DartsLocal_logger.info(f'Model configuration saved to "{config_path}"')

    def load_model(self):
        """Load model configuration and recreate untrained model."""
        config_path = Path(self.model_path).with_suffix(".config")

        with open(config_path, "rb") as f:
            data = pickle.load(f)

        # Recreate untrained model
        model_class = data["model_config"]["class"]
        model_params = data["model_config"]["params"]
        self.model = model_class(**model_params)
        DartsLocal_logger.info(f'Model configuration loaded from "{config_path}"')

    def training_workflow(self):
        """Training workflow for DartsLocal - saves configuration only."""
        DartsLocal_logger.info("DartsLocal training_workflow called.")
        # For DartsLocal, we don't train in advance
        # Just save the model configuration
        self.save_model()
        print("Note: DartsLocal models train per-entity during inference.")

    def inference_workflow(self):
        """Inference workflow - loads config and trains per entity."""
        DartsLocal_logger.info("DartsLocal inference_workflow called.")
        # Load model configuration
        self.load_model()
        # Run the regular forecast workflow (which trains per entity)
        self.forecast_workflow()
        self.print_summary()
        self.save_results()
