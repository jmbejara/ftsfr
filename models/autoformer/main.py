# """
# Autoformer using Nixtla's neuralforecast

# Performs both local and global forecasting using a Autoformer. Reports both mean and
# median MASE for local forecasts and a single global MASE.
# """

# from pathlib import Path
# from warnings import filterwarnings
# import numpy as np
# import pandas as pd
# import os
# import traceback
# import platform
# # Using darts for now for MASE
# from darts import TimeSeries
# from darts.metrics import mase
# from neuralforecast import NeuralForecast
# from neuralforecast.models import Autoformer

# # Ignoring warnings
# filterwarnings("ignore")

# def train_autoformer(train_data, test_length, freq, seasonality, path_to_save):
#     """
#     Fit Autoformer model and save it to specificed path

#     Parameters:
#     -----------
#     train_data : array-like
#         array-like object(e.g. pd.DataFrame), with a single or multiple series,
#         used for training the Autoformer.
#     test_ratio : int
#         fraction of df used for testing.
#     freq: str
#         pandas or polars frequency of the data
#     seasonality : int
#         seasonality of the dataset
#     path_to_save : str | Path
#         Path to save model
#     Returns:
#     --------
#     None
#     """
#     try:
#         estimator = Autoformer(h = test_length,
#                                 input_size = seasonality * 4)
        
#         nf = NeuralForecast(models=[estimator], freq=freq)

#         # fit model
#         nf.fit(df=train_data)

#         # Save model
#         nf.save(path = str(path_to_save),
#                 model_index = None,
#                 overwrite = True,
#                 save_dataset = False)
        
#     except Exception as e:
#         # In case of errors, return NaN
#         print(f"Error in Autoformer training: {e}")
#         print(traceback.format_exc())
#         return np.nan

# def forecast_autoformer(train_data, test_data, path_to_load, path_to_save):
#     """
#     Loads Autoformer from the path specified and saves predicted series.

#     Parameters:
#     -----------
#     train_data : array-like
#         array-like object(e.g. pd.DataFrame), with a single or multiple series,
#         which was used to train the loaded Autoformer.
#     test_data : array-like
#         array-like object used to match up the time indices of the test dataset 
#         with the predictions.
#     path_to_load : str | Path
#         Path to load model.
#     path_to_save : str
#         Path to save predicted series.
#     Returns:
#     --------
#         None
#     """
#     try:
#         nf = NeuralForecast.load(path = str(path_to_load))

#         # get predictions
#         pred_series = nf.predict(train_data)

#         # There is a possibility that the timestamps for pred_series wouldn't
#         # line up with test_data.
#         # Sort their values first on id then on timestamps
#         pred_series = pred_series.sort_values(["unique_id", "ds"]).reset_index(
#             drop=True
#         )
#         test_data = test_data.sort_values(["unique_id", "ds"]).reset_index(drop=True)
#         # make the ds columns same
#         pred_series["ds"] = test_data["ds"]

#         pred_series.to_parquet(path_to_save, engine = "pyarrow")

#     except Exception as e:
#         # In case of errors, return NaN
#         print(f"Error in Autoformer forecasting: {e}")
#         return np.nan

# def calculate_MASE(train_data, test_data, seasonality, path_to_load_pred):
#     """
#     Loads predicted values and returns mase

#     Parameters:
#     -----------
#     test_data : array-like
#         array-like object(e.g. pd.DataFrame), with a single or multiple series,
#         which is split into testing and training data.
#     train_data : array-like
#         Training dataset used to train the model.
#     path_to_load : str
#         Path to load model.
#     path_to_save : str
#         Path to save predicted series.
#     Returns:
#     --------
#     float
#         MASE value
#     """
#     try:
#         # Converting into TimeSeries objects to calculate darts mase
#         pred_series = pd.read_parquet(path_to_load_pred)
        
#         test_series = (
#             test_data.pivot(index="ds", columns="unique_id", values="y")
#             .reset_index()
#             .rename_axis(None, axis=1)
#             .rename(columns={"ds": "date"})
#         )
#         series = (
#             train_data.pivot(index="ds", columns="unique_id", values="y")
#             .reset_index()
#             .rename_axis(None, axis=1)
#             .rename(columns={"ds": "date"})
#         )
#         pred_series = (
#             pred_series.pivot(index="ds", columns="unique_id", values="Autoformer")
#             .reset_index()
#             .rename_axis(None, axis=1)
#             .rename(columns={"ds": "date"})
#         )

#         test_series = TimeSeries.from_dataframe(test_series, time_col="date")
#         series = TimeSeries.from_dataframe(series, time_col="date")
#         pred_series = TimeSeries.from_dataframe(pred_series, time_col="date")

#         calculated_MASE = mase(test_series, pred_series, series, seasonality)

#         return calculated_MASE
#     except Exception as e:
#         # In case of errors, return NaN
#         print(f"Error in Autoformer forecasting: {e}")
#         return np.nan


# if __name__ == "__main__":

#    # Read environment variables
#     dataset_path = Path(os.environ["FTSFR_DATASET_PATH"])
#     frequency = os.environ["FTSFR_FREQUENCY"]
#     OUTPUT_DIR = Path(
#         os.environ.get("OUTPUT_DIR", 
#                        Path(__file__).parent.parent.parent / "_output")
#     )
#     seasonality = int(os.environ["SEASONALITY"])

#     # Extract dataset name from path for results filename
#     dataset_name = dataset_path.stem.replace("ftsfr_", "")

#     # Path to save model
#     model_path = OUTPUT_DIR / "models" / "Autoformer" / dataset_name
#     Path(model_path).mkdir(parents = True, exist_ok = True)

#     # Path to save forecasts
#     forecast_path = OUTPUT_DIR / "forecasts" / "Autoformer" / dataset_name
#     Path(forecast_path).mkdir(parents = True, exist_ok = True)
#     forecast_path = forecast_path / "forecasts.parquet"

#     # Load data
#     df = pd.read_parquet(dataset_path).rename(columns={"id" : "unique_id"})

#     # Check if data follows the expected format (id, ds, y)
#     expected_columns = {"unique_id", "ds", "y"}
#     if not expected_columns.issubset(df.columns):
#         raise ValueError(
#             f"Dataset must contain columns: {expected_columns}. Found: {df.columns}"
#         )

#     unique_dates = np.unique(df["ds"].values)

#     # Define forecasting parameters
#     test_ratio = 15 / len(unique_dates)  # Use last 15 entries of the data for testing

#     # No data scaling required because neuralforecast does it automatically
#     test_length = int(test_ratio * len(unique_dates))
#     # Filling NaN values with interpolated values

#     df = df.interpolate()

#     test_data = df[df.ds >= unique_dates[-test_length]]
#     train_data = df[df.ds < unique_dates[-test_length]]

#     # Global Forecasting
#     train_autoformer(train_data, test_length, frequency, seasonality, model_path)
#     forecast_autoformer(train_data, test_data, model_path, forecast_path)
#     global_mase = calculate_MASE(train_data, test_data, seasonality, forecast_path)

#     # Printing and saving results

#     print("\nAutoformer Forecasting Results:")
#     print(f"Global MASE: {global_mase:.4f}")

#     results_df = pd.DataFrame(
#         {
#             "model": ["Autoformer"],
#             "global_mase": [global_mase],
#         }
#     )

#     results_path = OUTPUT_DIR / "raw_results" / "Autoformer"
#     file_name = "autoformer_" + dataset_name + ".csv"
#     Path(results_path).mkdir(parents = True, exist_ok = True)
#     results_df.to_csv(results_path / file_name, index = False)

import sys
sys.path.append('../')
from model_classes.nixtla_main_class import NixtlaMain
from neuralforecast.models import Autoformer
import os
from pathlib import Path

if __name__ == "__main__":

   # Read environment variables
    dataset_path = Path(os.environ["FTSFR_DATASET_PATH"])
    frequency = os.environ["FTSFR_FREQUENCY"]
    OUTPUT_DIR = Path(
        os.environ.get("OUTPUT_DIR", 
                       Path(__file__).parent.parent.parent / "_output")
    )
    seasonality = int(os.environ["SEASONALITY"])

    autoformer = NixtlaMain(estimator=Autoformer, 
                            model_name="autoformer", 
                            test_split=0.2, 
                            frequency=frequency,
                            seasonality=seasonality,
                            data_path=dataset_path,
                            output_path=OUTPUT_DIR)
    autoformer.main_workflow()