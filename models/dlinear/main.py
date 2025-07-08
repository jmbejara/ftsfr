"""
D-Linear using darts

Performs both local and global forecasting using a D-Linear. Reports both mean and
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

from darts.models import DLinearModel
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from darts.utils.missing_values import fill_missing_values
from darts.utils.model_selection import train_test_split

from darts.metrics import mase


def forecast_dlinear(df, test_split, seasonality):
    """
    Fit D-Linear model and return MASE

    Parameters:
    -----------
    df : array-like
        array-like object(e.g. pd.DataFrame), with a single or multiple series, 
        which is split into testing and training data.
    test_ratio : int
        fraction of df used for testing.
    seasonality : int
        Seasonality of the series.
    Returns:
    --------
    float
        MASE value
    """
    try:
        # Data Processing

        test_length = int(test_split * len(df))
        # TimeSeries object is important for darts
        raw_series = TimeSeries.from_dataframe(df, time_col = "date").astype(np.float32)
        # Replace NaNs
        raw_series = fill_missing_values(raw_series)
        # Autoscaling the data
        transformer = Scaler()
        transformed_series = transformer.fit_transform(raw_series)
        # Splitting into train and test
        series, test_series = train_test_split(transformed_series, 
                                               test_size = test_split)

        # Check for an NVIDIA GPU
        try:
            subprocess.check_output('nvidia-smi')
            device = "gpu"
        except Exception:
            device = "cpu"

        # Training the model and getting MASE

        estimator = DLinearModel(input_chunk_length = seasonality * 10,
                                 output_chunk_length = 1,
                                 pl_trainer_kwargs = {"accelerator": device})
        estimator.fit(series)
        pred_series = estimator.predict(test_length)
        return mase(test_series, pred_series, series, seasonality)
    except Exception as e:
        # In case of errors, return NaN
        print(f"Error in D-Linear forecasting: {e}")
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
    

    # This pivot adds all values for an entity as a TS in each column
    proc_df = df.pivot(index="date", columns="entity", values="value").reset_index()
    # Basic cleaning
    proc_df.rename_axis(None, axis = 1, inplace=True)

    # Define forecasting parameters
    test_ratio = 0.2            # Use last 20% of the data for testing
    forecast_horizon = 20       # 20 business days, 4 weeks, about a month
    seasonality = 5             # 5 for weekly patterns (business days)

    # Process each entity separately
    entities = df["entity"].unique()
    mase_values = []

    # Local forecasting

    print(f"Running D-Linear forecasting for {len(entities)} entities...")

    for entity in tqdm(entities):
        # Filter data for the current entity
        entity_data = proc_df[["date", entity]]

        # Removing leading NaNs which show up due to different start times
        # of different series
        entity_data = entity_data.iloc[entity_data[entity].first_valid_index():]

        if len(entity_data) <= 10:  # Skip entities with too few observations
            continue

        # Get MASE using D-Linear
        entity_mase = forecast_dlinear(entity_data, test_ratio, seasonality)

        if not np.isnan(entity_mase):
            mase_values.append(entity_mase)

    # Calculate mean MASE across all entities
    mean_mase = np.mean(mase_values)
    median_mase = np.median(mase_values)

    # Global Forecasting

    global_mase = forecast_dlinear(proc_df,
                                       test_ratio,
                                       seasonality)

    # Printing and saving results

    print("\nD-Linear Forecasting Results:")
    print(f"Number of entities successfully forecasted: {len(mase_values)}")
    print(f"Mean MASE: {mean_mase:.4f}")
    print(f"Median MASE: {median_mase:.4f}")
    print(f"Global MASE: {global_mase:.4f}")

    results_df = pd.DataFrame(
        {
            "model": ["D-Linear"],
            "seasonality": [seasonality],
            "mean_mase": [mean_mase],
            "median_mase": [median_mase],
            "entity_count": [len(mase_values)],
            "global_mase": [global_mase],
        }
    )

    results_df.to_csv(OUTPUT_DIR / "raw_results" / "dlinear_results.csv", index=False)
