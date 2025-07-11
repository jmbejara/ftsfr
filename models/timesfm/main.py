"""
TimesFM using the official timesfm package.

Performs both local and global forecasting using a TimesFM. Reports both mean and
median MASE for local forecasts and a single global MASE.

NOTE: Loading the TimesFM 500m checkpoint needs about 2GB of space.
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

import timesfm


def forecast_timesfm(df, test_split, freq, seasonality):
    """
    Fit TimesFM model and return MASE

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

        test_data = df[df.ds >= np.unique(df["ds"].values)[-test_length]]
        train_data = df[df.ds < np.unique(df["ds"].values)[-test_length]]

        # Check for an NVIDIA GPU
        try:
            subprocess.check_output("nvidia-smi")
            device = "gpu"
        except Exception:
            device = "cpu"

        # Code below acquired from https://pypi.org/project/timesfm/

        # Loading the timesfm-2.0 checkpoint:

        # For Torch
        tfm = timesfm.TimesFm(
            hparams=timesfm.TimesFmHparams(
                backend=device,
                per_core_batch_size=32,
                horizon_len=128,
                num_layers=50,
                use_positional_embedding=False,
                context_len=2048,
            ),
            checkpoint=timesfm.TimesFmCheckpoint(
                huggingface_repo_id="google/timesfm-2.0-500m-pytorch"
            ),
        )

        # Don't need to fit the model
        len_forecast = 0
        temp_train_data = train_data
        pred_series = pd.DataFrame(columns=["unique_id", "ds", "timesfm"])
        # We directly run inference on the saved checkpoint
        # Keep forecasting till the length of the forecasts exceeds or is equal to
        # test_length
        while len_forecast < test_length:
            forecast_df = tfm.forecast_on_df(
                inputs=temp_train_data,
                freq=freq,  # monthly
                value_name="y",
                num_jobs=-1,
            )
            # Removing the quantiles from forecast_df
            pred_series = pd.concat(
                [pred_series, forecast_df[["unique_id", "ds", "timesfm"]]]
            )
            temp_train_data = pred_series
            len_forecast += len(temp_train_data)

        # Converting into TimeSeries objects to calculate darts mase
        # There is a possibility that the timestamps for pred_series wouldn't
        # line up with test_data.

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
            pred_series.pivot(index="ds", columns="unique_id", values="timesfm")
            .reset_index()
            .rename_axis(None, axis=1)
            .rename(columns={"ds": "date"})
        )

        # truncating pred_series to test_length
        pred_series = pred_series.iloc[:test_length]
        # Lining up their date columns
        pred_series["date"] = test_series["date"]

        test_series = TimeSeries.from_dataframe(test_series, time_col="date")
        series = TimeSeries.from_dataframe(series, time_col="date")
        pred_series = TimeSeries.from_dataframe(pred_series, time_col="date")

        return mase(test_series, pred_series, series, seasonality)
    except Exception as e:
        # In case of errors, return NaN
        print(f"Error in TimesFM forecasting: {e}")
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
    proc_df = df.rename(columns={"entity": "unique_id", "date": "ds", "value": "y"})

    # Define forecasting parameters
    test_ratio = 0.2  # Use last 20% of the data for testing
    forecast_horizon = 20  # 20 business days, 4 weeks, about a month
    seasonality = 5  # 5 for weekly patterns (business days)
    freq = "B"
    # Process each entity separately
    entities = df["entity"].unique()
    mase_values = []

    # Local forecasting

    print(f"Running TimesFM forecasting for {len(entities)} entities...")

    for entity in tqdm(entities):
        # Filter data for the current entity
        entity_data = proc_df[proc_df["unique_id"] == entity]

        # Sort entity_data values by ds
        entity_data = entity_data.sort_values(["ds"]).reset_index(drop=True)
        # Removing leading NaNs which show up due to different start times
        # of different series
        entity_data = entity_data.iloc[entity_data["y"].first_valid_index() :]

        if len(entity_data) <= 10:  # Skip entities with too few observations
            continue

        # Get MASE using TimesFM
        entity_mase = forecast_timesfm(
            entity_data, test_ratio, freq, seasonality, forecast_horizon
        )

        if not np.isnan(entity_mase):
            mase_values.append(entity_mase)

    # Calculate mean MASE across all entities
    mean_mase = np.mean(mase_values)
    median_mase = np.median(mase_values)

    # Global Forecasting

    global_mase = forecast_timesfm(
        proc_df, test_ratio, freq, seasonality, forecast_horizon
    )

    # Printing and saving results

    print("\nTimesFM Forecasting Results:")
    print(f"Number of entities successfully forecasted: {len(mase_values)}")
    print(f"Mean MASE: {mean_mase:.4f}")
    print(f"Median MASE: {median_mase:.4f}")
    print(f"Global MASE: {global_mase:.4f}")

    results_df = pd.DataFrame(
        {
            "model": ["TimesFM"],
            "seasonality": [seasonality],
            "mean_mase": [mean_mase],
            "median_mase": [median_mase],
            "entity_count": [len(mase_values)],
            "global_mase": [global_mase],
        }
    )

    results_df.to_csv(OUTPUT_DIR / "raw_results" / "timesfm_results.csv", index=False)
