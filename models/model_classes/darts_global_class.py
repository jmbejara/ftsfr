"""
The DartsGlobal class is specifically designed for Global forecasting models
implemented using darts. Examples include CatBoost, Pooled Regression, and the
Transformer.
"""

import traceback
import pandas as pd
from tabulate import tabulate
import logging

# from warnings import filterwarnings
# filterwarnings("ignore")

from .darts_main_class import DartsMain
from .helper_func import common_error_catch

dg_logger = logging.getLogger("DartsGlobal")


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
        dg_logger.info("DartsGlobal object initialized.")

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

        dg_logger.info("DartsGlobal super().__init__() complete.")

        # self.model_path += ".pt"

    @common_error_catch
    def forecast(self):
        start_time = self.test_series.start_time()
        pred_series = self.model.historical_forecasts(
            series=self.raw_series, start=start_time, retrain=False
        )
        self.pred_series = pred_series

        dg_logger.info(
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

        dg_logger.info('Results saved to "' + str(self.result_path) + '".')
