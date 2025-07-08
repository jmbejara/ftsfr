"""
Autoformer using Nixtla's neuralforecast

Performs both local and global forecasting using a Autoformer. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""
from pathlib import Path
from warnings import filterwarnings
# Ignoring warnings
filterwarnings("ignore")

import numpy as np
import pandas as pd
import toml
from decouple import config
from tqdm import tqdm
import subprocess

# Using darts for now for MASE
from darts import TimeSeries
from darts.metrics import mase

from neuralforecast import NeuralForecast
from neuralforecast.models import Autoformer


def forecast_autoformer(df, test_split, freq, seasonality, forecast_horizon):
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
    forecast_horizon: int
        Forecast horizon
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

        test_data = df[df.ds>=np.unique(df['ds'].values)[-test_length]]
        train_data = df[df.ds<np.unique(df['ds'].values)[-test_length]]

        # Check for an NVIDIA GPU
        try:
            subprocess.check_output('nvidia-smi')
            device = "gpu"
        except Exception:
            device = "cpu"

        # Having this horizon as the forecast_horizon means that predict will
        # return only these amount of values
        estimator = Autoformer(h = forecast_horizon, input_size = seasonality * 10, accelerator = device)

        nf = NeuralForecast(
            models=[estimator],
            freq=freq
        )
        # fit model
        nf.fit(df = train_data)
        # get predictions
        pred_series = nf.predict()

        # Converting into TimeSeries objects to calculate darts mase
        # There is a possibility that the timestamps for pred_series wouldn't
        # line up with test_data.
        # Sort their values first on id then on timestamps
        pred_series = pred_series.sort_values(["unique_id", "ds"]).reset_index(drop = True)
        test_data = test_data.sort_values(["unique_id", "ds"]).reset_index(drop = True)
        # make the ds columns same
        pred_series["ds"] = test_data["ds"]

        test_series = test_data.pivot(index="ds", columns="unique_id", values="y").reset_index().rename_axis(None, axis = 1).rename(columns = {"ds":"date"})
        series = train_data.pivot(index="ds", columns="unique_id", values="y").reset_index().rename_axis(None, axis = 1).rename(columns = {"ds":"date"})
        pred_series = pred_series.pivot(index="ds", columns="unique_id", values="Autoformer").reset_index().rename_axis(None, axis = 1).rename(columns = {"ds":"date"})

        test_series = TimeSeries.from_dataframe(test_series, time_col = "date" )
        series = TimeSeries.from_dataframe(series, time_col = "date" )
        pred_series = TimeSeries.from_dataframe(pred_series, time_col = "date" )

        return mase(test_series, pred_series, series, seasonality)
    except Exception as e:
        # In case of errors, return NaN
        print(f"Error in Autoformer forecasting: {e}")
        return np.nan

if __name__ == "__main__":

    # Data loading and processing

    DATA_DIR = config(
        "DATA_DIR", cast=Path, default=Path(__file__).parent.parent.parent / "_data"
    )
    OUTPUT_DIR = config(
        "OUTPUT_DIR", cast=Path, default=Path(__file__).parent.parent.parent / "_output"
    )
    datasets_info = toml.load(DATA_DIR / "ftsfr_datasets_paths.toml")

    file_path = DATA_DIR / datasets_info["treas_yield_curve_zero_coupon"]
    df = pd.read_parquet(file_path)
    
    # neuralforecast naming conventions
    proc_df = df.rename(columns = {"entity": "unique_id", "date":"ds", "value":"y"})

    # Define forecasting parameters
    test_ratio = 0.2            # Use last 20% of the data for testing
    forecast_horizon = 20       # 20 business days, 4 weeks, about a month
    seasonality = 5             # 5 for weekly patterns (business days)
    freq = "B"
    # Process each entity separately
    entities = df["entity"].unique()
    mase_values = []

    # Local forecasting

    print(f"Running Autoformer forecasting for {len(entities)} entities...")

    for entity in tqdm(entities):
        # Filter data for the current entity
        entity_data = proc_df[proc_df["unique_id"] == entity]

        # Sort entity_data values by ds
        entity_data = entity_data.sort_values(["ds"]).reset_index(drop = True)
        # Removing leading NaNs which show up due to different start times
        # of different series
        entity_data = entity_data.iloc[entity_data["y"].first_valid_index():]

        if len(entity_data) <= 10:  # Skip entities with too few observations
            continue

        # Get MASE using Autoformer
        entity_mase = forecast_autoformer(entity_data, 
                                        test_ratio, 
                                        freq, 
                                        seasonality, 
                                        forecast_horizon)

        if not np.isnan(entity_mase):
            mase_values.append(entity_mase)

    # Calculate mean MASE across all entities
    mean_mase = np.mean(mase_values)
    median_mase = np.median(mase_values)

    # Global Forecasting

    global_mase = forecast_autoformer(proc_df,
                                    test_ratio,
                                    freq,
                                    seasonality,
                                    forecast_horizon)

    # Printing and saving results

    print("\nAutoformer Forecasting Results:")
    print(f"Number of entities successfully forecasted: {len(mase_values)}")
    print(f"Mean MASE: {mean_mase:.4f}")
    print(f"Median MASE: {median_mase:.4f}")
    print(f"Global MASE: {global_mase:.4f}")

    results_df = pd.DataFrame(
        {
            "model": ["Autoformer"],
            "seasonality": [seasonality],
            "mean_mase": [mean_mase],
            "median_mase": [median_mase],
            "entity_count": [len(mase_values)],
            "global_mase": [global_mase],
        }
    )

    results_df.to_csv(OUTPUT_DIR / "raw_results" / "autoformer_results.csv", index=False)
