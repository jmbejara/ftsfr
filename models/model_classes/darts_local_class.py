"""
The DartsLocal class is specifically designed for Global forecasting models 
implemented using darts. Examples include ARIMA, TBATS, ETS, and Theta.
"""
import statistics
import traceback

import numpy as np
import pandas as pd
from darts.utils.missing_values import fill_missing_values
from tabulate import tabulate
from tqdm import tqdm
import logging

# from warnings import filterwarnings
# filterwarnings("ignore")

from .darts_main_class import DartsMain
from .helper_func import common_error_catch

dl_logger = logging.getLogger("DartsLocal")

class DartsLocal(DartsMain):
    def __init__(self,
                 estimator,
                 model_name,
                 test_split,
                 frequency,
                 seasonality,
                 data_path,
                 output_path,
                 scaling = False,
                 interpolation = False):
        
        dl_logger.info("DartsLocal object initialized.")

        super().__init__(estimator,
                         model_name,
                         test_split,
                         frequency,
                         seasonality,
                         data_path,
                         output_path,
                         scaling,
                         interpolation)
        
        dl_logger.info("DartsLocal super().__init__() complete.")

        self.median_mase = np.nan
        self.mase_list = []
        self.model_path += ".pkl"

        dl_logger.info("DartsLocal internal variables set.")
    
    @common_error_catch
    def forecast_workflow(self):
        """
        This workflow function follows the procedure below:

        Step 1
        ------
        For each entity in raw_series:
            1. Extract and process entity data
            2. If entity data is too small, move to next
            3. Update internal variables and split into train and test
            4. Train -> Forecast -> Calculate error
            5. Update internal model to untrained version
        
        Step 2
        ------
        Calculates mean and median MASE, and updates internal variables.
        """
        dl_logger.info("forecast_workflow called. Predictions made for each "+\
                       "entity separately.")
        raw_series = self.raw_series.copy()
        auto_mode = False
        # Training on each entity and calculating MASE
        self.print_sep()
        dl_logger.info("Starting loop for the workflow on each entity.")
        for id in tqdm(raw_series.columns):
            dl_logger.info("Processing id: " + id + ".")
            # Select the date and the column for current id
            entity_data = raw_series[[id]].copy()
            # Removing leading/trailing NaNs which show up due to different 
            # start times of different series
            entity_data = entity_data.strip()
            entity_data = fill_missing_values(entity_data)

            dl_logger.info("Pre-processed entity data.")

            if len(entity_data) <= 10:
                dl_logger.info("Data too small, so skipped.")
                continue
            
            self.raw_series = entity_data

            # Updates internal train and test series
            self._train_test_split(entity_data)
            self.train()
            self.forecast()
            id_mase = self.calculate_error()
            dl_logger.info("MASE: " + str(id_mase) + ".")
            # Resets the model
            self.model = self.model.untrained_model()

            if id_mase is not None:
                self.mase_list.append(id_mase)

        self.print_sep()
        self.save_forecast()
        self.raw_series = raw_series

        if self.mase_list:
            self.errors["MASE"] = sum(self.mase_list) / len(self.mase_list)
            self.median_mase = statistics.median(self.mase_list)
        else:
            self.errors["MASE"] = np.nan
            self.median_mase = np.nan
        
        dl_logger.info(f"Mean MASE: {self.errors['MASE']} | "+\
                        "Median MASE: {self.median_mase}")
    
    def main_workflow(self):
        dl_logger.info("main_workflow called.")
        self.forecast_workflow()
        self.print_summary()
        self.save_results()
    
    def print_summary(self):
        dl_logger.info("print_summary called.")
        print(tabulate([
            ["Model", self.model_name],
            ["Dataset", self.dataset_name],
            ["Entities", len(self.mase_list)],
            ["Frequency", self.frequency],
            ["Seasonality", self.seasonality],
            ["Median MASE", self.median_mase],
            ["Mean MASE", self.errors["MASE"]]
            ], tablefmt="fancy_grid"))
    
    @common_error_catch
    def save_results(self):
        forecast_res = pd.DataFrame(
            {
                "Model" : [self.model_name],
                "Dataset" : [self.dataset_name],
                "Entities" : [len(self.mase_list)],
                "Seasonality" : [self.seasonality],
                "Median_MASE" : [self.median_mase],
                "Mean_MASE" : [self.errors["MASE"]]
            }
        )

        forecast_res.to_csv(self.result_path)
        dl_logger.info("Results saved to " + str(self.result_path))