"""
Catboost using darts

Performs both local and global forecasting using Catboost. Reports both mean and
median MASE for local forecasts and a single global MASE.

NOTE: training this model, especially on data which is considered large either
due to the number of series, the number of values in a single series, or both
requires large amounts of computation power.
"""

from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") # This should be here to suppress warnings on import
import os
import pandas as pd
from tabulate import tabulate
import traceback
import subprocess
# Darts-based imports
from darts.models import CatBoostModel

from darts.metrics import mase


def train_catboost(train_series, seasonality, path_to_save):
    """
    Fit CatBoost model and return Mean Absolute Scaled Error(MASE).

    Parameters:
    -----------
    df : pd.DataFrame or pl.DataFrame
        DataFrame containing the training and test series in the long format.
    test_ratio : float
        Ratio of the number of test samples and the total number of samples.
    seasonality : int
        Seasonality of the dataset.
    
    Returns:
    --------
    mase : float
        MASE value from the testing, predicted, and training series.
    """
    try:
        # Check for an NVIDIA GPU
        try:
            subprocess.check_output("nvidia-smi")
            task_type = "GPU"
        except Exception:
            task_type = "CPU"
        
        estimator = CatBoostModel(
            lags=seasonality * 4,
            output_chunk_length=test_length,
            # Training a single global model for global forecasting
            multi_models=False,
            task_type=task_type,
        )

        estimator.fit(series)
        estimator.save(path_to_save)
        # Model predictions
        pred_series = estimator.predict(test_length)

        calculated_MASE = mase(test_series, pred_series, series, seasonality)

        return calculated_MASE
    
    except Exception:
        print("---------------------------------------------------------------")
        print(traceback.format_exc())
        print("\nError in CatBoost forecasting. Full traceback above \u2191")
        print("---------------------------------------------------------------")
        return None

def forecast_catboost(train_series, seasonality, model_path, pred_series_path):
    """
    Fit CatBoost model and return Mean Absolute Scaled Error(MASE).

    Parameters:
    -----------
    df : pd.DataFrame or pl.DataFrame
        DataFrame containing the training and test series in the long format.
    test_ratio : float
        Ratio of the number of test samples and the total number of samples.
    seasonality : int
        Seasonality of the dataset.
    
    Returns:
    --------
    mase : float
        MASE value from the testing, predicted, and training series.
    """
    try:
        estimator = CatBoostModel.load(model_path)
        pred_series = estimator.predict(test_length)

        pred_series = pred_series.to_dataframe(time_as_index = False)

        pred_series.to_parquet(pred_series_path)
    
    except Exception:
        print("---------------------------------------------------------------")
        print(traceback.format_exc())
        print("\nError in CatBoost forecasting. Full traceback above \u2191")
        print("---------------------------------------------------------------")
        return None

def calculate_MASE(train_series, seasonality, model_path, pred_series_path):
    """
    Fit CatBoost model and return Mean Absolute Scaled Error(MASE).

    Parameters:
    -----------
    df : pd.DataFrame or pl.DataFrame
        DataFrame containing the training and test series in the long format.
    test_ratio : float
        Ratio of the number of test samples and the total number of samples.
    seasonality : int
        Seasonality of the dataset.
    
    Returns:
    --------
    mase : float
        MASE value from the testing, predicted, and training series.
    """
    try:
        estimator = CatBoostModel.load(model_path)
        pred_series = estimator.predict(test_length)

        pred_series = pred_series.to_dataframe(time_as_index = False)

        pred_series = pd.read_parquet(pred_series_path)

        pred_series = TimeSeries.from_dataframe(pred_series, time_col = "ds")

        calculated_MASE = mase(test_series, pred_series, series, seasonality)

        return calculated_MASE
    
    except Exception:
        print("---------------------------------------------------------------")
        print(traceback.format_exc())
        print("\nError in CatBoost forecasting. Full traceback above \u2191")
        print("---------------------------------------------------------------")
        return None
    



if __name__ == "__main__":

    # Read env variables
    dataset_path = Path(os.environ["FTSFR_DATASET_PATH"])
    frequency = os.environ["FTSFR_FREQUENCY"]
    seasonality = int(os.environ["SEASONALITY"])
    if os.environ.get("OUTPUT_DIR", None) is not None:
        OUTPUT_DIR = Path(os.environ["OUTPUT_DIR"])
    else:
        OUTPUT_DIR = Path().resolve().parent.parent / "_output"

    dataset_name = str(os.path.basename(dataset_path)).split(".")[0].removeprefix("ftsfr_")

    # Path to save model
    model_path = OUTPUT_DIR / "models" / "CatBoost" / dataset_name
    Path(model_path).mkdir(parents = True, exist_ok = True)
    model_path = model_path / "saved_model.pkl"

    # Path to save forecasts
    forecast_path = OUTPUT_DIR / "forecasts" / "CatBoost" / dataset_name
    Path(forecast_path).mkdir(parents = True, exist_ok = True)
    forecast_path = forecast_path / "forecasts.parquet"

    # Read dataset as a DataFrame
    df = pd.read_parquet(dataset_path).rename(columns = {"id" : 'unique_id'})

    # This pivot adds all values for an entity as a TS in each column
    proc_df = df.pivot(index="ds", columns="unique_id", values="y").reset_index()
    # Basic cleaning
    proc_df.rename_axis(None, axis=1, inplace=True)

    # Some variables
    test_split = 0.2
    ids = df["unique_id"].unique()

    # Splitting and TimeSeries conversion
    test_length = int(test_split * len(df))
    # TimeSeries object is important for darts
    raw_series = TimeSeries.from_dataframe(df, time_col = "ds")
    # Replace NaNs automatically
    raw_series = fill_missing_values(raw_series)
    # Splitting into train and test
    series, test_series = train_test_split(raw_series, test_size = test_split)


    # Training on each entity and calculating MASE

    train_catboost()
    forecast_catboost()
    calculate_MASE()
    global_mase = forecast_catboost(proc_df, test_split, seasonality)

    # Printing a table with the results
    print(tabulate([["Model", "CatBoost"],
                    ["Dataset", dataset_name],
                    ["Entities", len(ids)],
                    ["Global MASE", global_mase]], tablefmt="fancy_grid"))
    
    # Saving the results

    forecast_res = pd.DataFrame(
        {
            "Model" : ["CatBoost"],
            "Dataset" : [dataset_name],
            "Entities" : [len(ids)],
            "Global MASE" : [global_mase]
        }
    )

    result_path = OUTPUT_DIR / "raw_results" / "catboost"
    result_path.mkdir(parents = True, exist_ok = True)
    result_path = result_path / str(dataset_name + ".csv")
    forecast_res.to_csv(result_path)