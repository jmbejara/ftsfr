"""
The DartsGlobal class is specifically designed for Global forecasting models 
implemented using darts. Examples include CatBoost, Pooled Regression, and the
Transformer.
"""
import tabulate
import pandas as pd
from .darts_main_class import DartsMain
import traceback

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

    def forecast(self):
        # Get predictions
        self.pred_series = self.model.predict(self.test_length)

        # Save to parquet
        temp_df = self.pred_series.to_dataframe(time_as_index = False)
        temp_df.to_parquet(self.forecast_path)
    
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
        forecast_res = pd.DataFrame(
            {
                "Model" : [self.model_name],
                "Dataset" : [self.dataset_name],
                "Entities" : [self.train_series.n_components],
                "Global MASE" : [self.errors["MASE"]]
            }
        )

        forecast_res.to_csv(self.result_path)
    
    def main_workflow(self):
        try:
            self._train()
            self.save_model()
            self.forecast()
            self.save_forecast()
            self.calculate_error()
            self.print_summary()
            self.save_results()
        except Exception:
            print("---------------------------------------------------------------")
            print(traceback.format_exc())
            print(f"\nError in {self.model_name} training. Full traceback above \u2191")
            print("---------------------------------------------------------------")
            return None