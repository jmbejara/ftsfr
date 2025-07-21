"""
The DartsGlobal class is specifically designed for Global forecasting models 
implemented using darts. Examples include CatBoost, Pooled Regression, and the
Transformer.
"""
import traceback

import pandas as pd
from tabulate import tabulate

from .darts_main_class import DartsMain

class DartsGlobal(DartsMain):
    def __init__(self,
                 estimator,
                 model_name,
                 test_split,
                 frequency,
                 seasonality,
                 data_path,
                 output_path,
                 scaling = False,
                 interpolation = True,
                 f32 = False):
        
        super().__init__(estimator,
                         model_name,
                         test_split,
                         frequency,
                         seasonality,
                         data_path,
                         output_path,
                         scaling,
                         interpolation,
                         f32)
    
    def print_summary(self):
        print(tabulate([
            ["Model", self.model_name],
            ["Dataset", self.dataset_name],
            ["Entities", self.train_series.n_components],
            ["Frequency", self.frequency],
            ["Seasonality", self.seasonality],
            ["Global MASE", self.errors["MASE"]]
            ], tablefmt="fancy_grid"))
    
    def save_results(self):
        try:
            forecast_res = pd.DataFrame(
                {
                    "Model" : [self.model_name],
                    "Dataset" : [self.dataset_name],
                    "Entities" : [self.train_series.n_components],
                    "Global MASE" : [self.errors["MASE"]]
                }
            )

            forecast_res.to_csv(self.result_path)
        except Exception:

            self.print_sep()

            print(traceback.format_exc())
            print(f"\nError in saving {self.model_name} results. Full traceback above \u2191")

            self.print_sep()