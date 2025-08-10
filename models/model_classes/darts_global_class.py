"""
The DartsGlobal class is specifically designed for Global forecasting models
implemented using darts. Examples include CatBoost, Pooled Regression, and the
Transformer.
"""

import pandas as pd
from tabulate import tabulate
import logging

DartsGlobal_logger = logging.getLogger("DartsGlobal")

import torch

torch.set_float32_matmul_precision("medium")

# from warnings import filterwarnings
# filterwarnings("ignore")

from .darts_main_class import DartsMain
from .helper_func import common_error_catch

# Darts-specific imports are moved inside methods


class DartsGlobal(DartsMain):
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
        DartsGlobal_logger.info("DartsGlobal object initialized.")

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
            f32,
        )

        DartsGlobal_logger.info("DartsGlobal super().__init__() complete.")

        # self.model_path += ".pt"

    @common_error_catch
    def forecast(self):
        # Darts-specific imports only when needed
        from .unified_one_step_ahead import (
            perform_one_step_ahead_darts,
            verify_one_step_ahead,
        )

        DartsGlobal_logger.info(
            "Starting unified one-step-ahead forecasting for global model"
        )

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
            DartsGlobal_logger.info("✓ One-step-ahead forecasting verified")
        else:
            DartsGlobal_logger.warning(
                "⚠ One-step-ahead forecasting verification failed"
            )

        DartsGlobal_logger.info(
            "DartsGlobal forecast called. "
            + "Predicted series acquired. "
            + "Internal pred_series updated."
        )

    def print_summary(self):
        print(
            tabulate(
                [
                    ["Model", self.model_name],
                    ["Dataset", self.dataset_name],
                    ["Entities", self.train_series.n_components],
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
                "Entities": [self.train_series.n_components],
                "Global MASE": [self.errors["MASE"]],
            }
        )

        forecast_res.to_csv(self.result_path)

        DartsGlobal_logger.info('Results saved to "' + str(self.result_path) + '".')
