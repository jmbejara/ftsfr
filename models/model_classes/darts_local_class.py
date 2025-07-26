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

# from warnings import filterwarnings
# filterwarnings("ignore")

from .darts_main_class import DartsMain

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
        
        super().__init__(estimator,
                         model_name,
                         test_split,
                         frequency,
                         seasonality,
                         data_path,
                         output_path,
                         scaling,
                         interpolation)

        self.median_mase = np.nan
        self.mase_list = []
        self.model_path += ".pkl"
    
    def forecast_workflow(self):
        try:
            raw_series = self.raw_series.copy()
            auto_mode = False
            # The check below is important because Auto models like AutoARIMA
            # need interpolation
            if self.model_name[:5] == "auto_":
                auto_mode = True
            # Training on each entity and calculating MASE
            self.print_sep()

            for id in tqdm(raw_series.columns):
                # Select the date and the column for current id
                entity_data = raw_series[[id]].copy()
                # Removing leading/trailing NaNs which show up due to different start 
                # times of different series
                entity_data = entity_data.strip()
                if auto_mode:
                    entity_data = fill_missing_values(entity_data)
                if len(entity_data) <= 10:
                    continue
                
                self.raw_series = entity_data

                # Updates internal train and test series
                self._train_test_split(entity_data)
                self.forecast()
                id_mase = self.calculate_error()

                # Resets the model
                self.model = self.estimator

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
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in {self.model_name} forecast workflow. Full traceback above \u2191")
            self.print_sep()
            return None
    
    def main_workflow(self):
        try:
            self.forecast_workflow()
            self.print_summary()
            self.save_results()
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in {self.model_name} workflow. Full traceback above \u2191")
            self.print_sep()
            return None
    
    def print_summary(self):
        print(tabulate([
            ["Model", self.model_name],
            ["Dataset", self.dataset_name],
            ["Entities", len(self.mase_list)],
            ["Frequency", self.frequency],
            ["Seasonality", self.seasonality],
            ["Median MASE", self.median_mase],
            ["Mean MASE", self.errors["MASE"]]
            ], tablefmt="fancy_grid"))
    
    def save_results(self):
        try:
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
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in saving {self.model_name} results. Full traceback above \u2191")
            self.print_sep()
            return None
    