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
        scaling=False,
        interpolation=False,
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
            scaling,
            interpolation,
        )

        DartsLocal_logger.info("DartsLocal super().__init__() complete.")

        self.median_mase = np.nan
        self.mase_list = []
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
        # Import Darts-specific utilities only when needed
        from darts.utils.missing_values import fill_missing_values

        DartsLocal_logger.info(
            "forecast_workflow called. Predictions made for each "
            + "entity separately."
        )
        raw_data = self.raw_data.copy()
        auto_mode = False
        # Training on each entity and calculating MASE
        self.print_sep()
        DartsLocal_logger.info("Starting loop for the workflow on each entity.")
        for id in tqdm(raw_data.columns):
            DartsLocal_logger.info("Processing id: " + id + ".")
            # Select the date and the column for current id
            entity_data = raw_data[[id]].copy()
            # Removing leading/trailing NaNs which show up due to different
            # start times of different series
            entity_data = entity_data.strip()
            entity_data = fill_missing_values(entity_data)

            DartsLocal_logger.info("Pre-processed entity data.")

            if len(entity_data) <= 10:
                DartsLocal_logger.info("Data too small, so skipped.")
                continue

            self.raw_data = entity_data

            # Updates internal train and test series
            self._train_test_split(entity_data)
            self.train()
            self.forecast()
            id_mase = self.calculate_error()
            DartsLocal_logger.info("MASE: " + str(id_mase) + ".")
            # Resets the model
            self.model = self.model.untrained_model()

            if id_mase is not None:
                self.mase_list.append(id_mase)

        self.print_sep()
        self.save_forecast()
        self.raw_data = raw_data

        if self.mase_list:
            self.errors["MASE"] = sum(self.mase_list) / len(self.mase_list)
            self.median_mase = statistics.median(self.mase_list)
        else:
            self.errors["MASE"] = np.nan
            self.median_mase = np.nan

        DartsLocal_logger.info(
            f"Mean MASE: {self.errors['MASE']} | " + "Median MASE: {self.median_mase}"
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
                    ["Entities", len(self.mase_list)],
                    ["Frequency", self.frequency],
                    ["Seasonality", self.seasonality],
                    ["Median MASE", self.median_mase],
                    ["Mean MASE", self.errors["MASE"]],
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
                "Entities": [len(self.mase_list)],
                "Seasonality": [self.seasonality],
                "Median_MASE": [self.median_mase],
                "Mean_MASE": [self.errors["MASE"]],
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
