"""
Autoformer using Nixtla's neuralforecast

Performs both local and global forecasting using a Autoformer. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""

from pathlib import Path
from warnings import filterwarnings
import numpy as np
import pandas as pd
import os
from tqdm import tqdm
import subprocess
# Using darts for now for MASE
from darts import TimeSeries
from darts.metrics import mase
from neuralforecast import NeuralForecast
from neuralforecast.models import Autoformer

# Ignoring warnings
filterwarnings("ignore")

def train_autoformer(df, test_split, freq, seasonality, path_to_save):
    """
    Fit Autoformer model and save it to specificed path

    Parameters:
    -----------
    df : array-like
        array-like object(e.g. pd.DataFrame), with a single or multiple series,
        which is split into testing and training data.
    test_ratio : int
        fraction of df used for testing.
    freq: str
        pandas or polars frequency of the data
    seasonality : int
        Seasonality of the series.
    path_to_save : str
        Path to save model
    Returns:
    --------
    None
    """
    try:
        # Data Processing
        # No data scaling required because neuralforecast does it automatically
        test_length = int(test_split * len(df))
        # Filling NaN values with interpolated values
        df = df.interpolate()

        # Following Monash style testing
        forecast_horizon = test_length

        train_data = df[df.ds < np.unique(df["ds"].values)[-test_length]]

        # TODO: Need to test if code runs fine if model is trained on GPU
        # but saved to cpu
        # Check for an NVIDIA GPU
        try:
            subprocess.check_output("nvidia-smi")
            device = "gpu"
        except Exception:
            device = "cpu"

        # Having this horizon as the forecast_horizon means that predict will
        # return only these amount of values
        estimator = Autoformer(h = forecast_horizon,
                               input_size = seasonality * 4,
                               accelerator = device)

        nf = NeuralForecast(models=[estimator], freq=freq)
        # fit model
        nf.fit(df=train_data)

        # Save model
        nf.save(path = path_to_save,
                model_index = None,
                overwrite = True,
                save_dataset = False)
        
    except Exception as e:
        # In case of errors, return NaN
        print(f"Error in Autoformer training: {e}")
        return np.nan

def forecast_autoformer(df, test_split, freq, seasonality, path_to_load):
    """
    Fit Autoformer model and return MASE

    Parameters:
    -----------
    df : array-like
        array-like object(e.g. pd.DataFrame), with a single or multiple series,
        which is split into testing and training data.
    test_ratio : int
        fraction of df used for testing.
    freq: str
        pandas or polars frequency of the data
    seasonality : int
        Seasonality of the series.
    path_to_load : str
        Path to load model
    Returns:
    --------
    float
        MASE value
    """
    try:
        # Data Processing
        # No data scaling required because neuralforecast does it automatically
        test_length = int(test_split * len(df))
        # Filling NaN values with interpolated values
        df = df.interpolate()

        # Following Monash style testing
        forecast_horizon = test_length

        test_data = df[df.ds >= np.unique(df["ds"].values)[-test_length]]
        train_data = df[df.ds < np.unique(df["ds"].values)[-test_length]]

        # Check for an NVIDIA GPU
        try:
            subprocess.check_output("nvidia-smi")
            device = "gpu"
        except Exception:
            device = "cpu"

        # Having this horizon as the forecast_horizon means that predict will
        # return only these amount of values
        estimator = Autoformer(
            h=forecast_horizon, input_size=seasonality * 4, accelerator=device
        )

        nf = NeuralForecast(models=[estimator], freq=freq)
        # fit model
        nf.fit(df=train_data)

        nf = NeuralForecast.load(path = path_to_load)

        # get predictions
        pred_series = nf.predict()

        # Converting into TimeSeries objects to calculate darts mase
        # There is a possibility that the timestamps for pred_series wouldn't
        # line up with test_data.
        # Sort their values first on id then on timestamps
        pred_series = pred_series.sort_values(["unique_id", "ds"]).reset_index(
            drop=True
        )
        test_data = test_data.sort_values(["unique_id", "ds"]).reset_index(drop=True)
        # make the ds columns same
        pred_series["ds"] = test_data["ds"]

        test_series = (
            test_data.pivot(index="ds", columns="unique_id", values="y")
            .reset_index()
            .rename_axis(None, axis=1)
            .rename(columns={"ds": "date"})
        )
        series = (
            train_data.pivot(index="ds", columns="unique_id", values="y")
            .reset_index()
            .rename_axis(None, axis=1)
            .rename(columns={"ds": "date"})
        )
        pred_series = (
            pred_series.pivot(index="ds", columns="unique_id", values="Autoformer")
            .reset_index()
            .rename_axis(None, axis=1)
            .rename(columns={"ds": "date"})
        )

        test_series = TimeSeries.from_dataframe(test_series, time_col="date")
        series = TimeSeries.from_dataframe(series, time_col="date")
        pred_series = TimeSeries.from_dataframe(pred_series, time_col="date")

        return mase(test_series, pred_series, series, seasonality)
    except Exception as e:
        # In case of errors, return NaN
        print(f"Error in Autoformer forecasting: {e}")
        return np.nan


if __name__ == "__main__":
   # Read environment variables
    dataset_path = Path(os.environ["FTSFR_DATASET_PATH"])
    frequency = os.environ["FTSFR_FREQUENCY"]
    OUTPUT_DIR = Path(
        os.environ.get("OUTPUT_DIR", 
                       Path(__file__).parent.parent.parent / "_output")
    )
    seasonality = int(os.environ["SEASONALITY"])

    # Extract dataset name from path for results filename
    dataset_name = dataset_path.stem.replace("ftsfr_", "")

    # Path to save model to
    model_path_to_save = OUTPUT_DIR / "models" / "Autoformer" / dataset_name
    Path(model_path_to_save).mkdir(parents = True, exist_ok = True)

    # Load data
    df = pd.read_parquet(dataset_path)

    # Check if data follows the expected format (id, ds, y)
    expected_columns = {"unique_id", "ds", "y"}
    if not expected_columns.issubset(df.columns):
        raise ValueError(
            f"Dataset must contain columns: {expected_columns}. Found: {df.columns}"
        )

    # Define forecasting parameters
    test_ratio = 0.2  # Use last 20% of the data for testing
    forecast_horizon = 20  # 20 business days, 4 weeks, about a month

    # Global Forecasting

    global_mase = forecast_autoformer(
        df, test_ratio, frequency, seasonality, forecast_horizon
    )

    # Printing and saving results

    print("\nAutoformer Forecasting Results:")
    print(f"Global MASE: {global_mase:.4f}")

    results_df = pd.DataFrame(
        {
            "model": ["Autoformer"],
            "seasonality": [seasonality],
            "global_mase": [global_mase],
        }
    )

    results_path = OUTPUT_DIR / "raw_results" / "Autoformer"
    file_name = "autoformer_" + dataset_name + ".csv"
    Path(results_path).mkdir(parents = True, exist_ok = True)
    results_df.to_csv(results_path / file_name, index = False)