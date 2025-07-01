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
# Ignoring warnings
filterwarnings("ignore")

import numpy as np
import pandas as pd
import toml
from decouple import config
from tqdm import tqdm

from darts.models import CatBoostModel
from darts import TimeSeries

from darts.metrics import mase


def forecast_catboost(train_data, test_data, seasonality, multi = False):
    """
    Fit Catboost model and return MASE

    Parameters:
    -----------
    train_data : array-like
        Training data
    test_length : int
        Number of periods to forecast
    test_data : array_like
        Testing data
    seasonality : int
        Seasonality of the series
    multi : bool
        indicates global forecasting if True
    
    Returns:
    --------
    int
        MASE value
    """
    try:
        test_length = len(test_data)
        series = TimeSeries.from_dataframe(train_data, time_col = "date")
        test_series = TimeSeries.from_dataframe(test_data, time_col = "date")
        if multi:
            estimator = CatBoostModel(lags = seasonality * 10,
                                      output_chunk_length = test_length,
                                      loss_function = "MultiRMSE")
        else:
            estimator = CatBoostModel(lags = seasonality * 10, 
                                      output_chunk_length = test_length)
        estimator.fit(series)
        pred_series = estimator.predict(test_length)
        return mase(test_series, pred_series, series, seasonality)
    except Exception as e:
        # In case of errors, return NaN
        print(f"Error in Catboost forecasting: {e}")
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
    # This step below is mportant for catboost since it can't handle nans
    # A large outlier value helps catboost treat it as a nan
    proc_df.fillna(-999, inplace=True)

    # Define forecasting parameters
    test_ratio = 0.2            # Use last 20% of the data for testing
    forecast_horizon = 20       # 20 business days, 4 weeks, about a month
    seasonality = 5             # 5 for weekly patterns (business days)

    # Process each entity separately
    entities = df["entity"].unique()
    mase_values = []

    # Local forecasting

    print(f"Running Catboost forecasting for {len(entities)} entities...")

    for entity in tqdm(entities):
        # Filter data for the current entity
        entity_data = proc_df[["date", entity]]

        if len(entity_data) <= 10:  # Skip entities with too few observations
            continue

        # Determine train/test split
        n = len(entity_data[entity])
        test_size = max(1, int(n * test_ratio))
        train_size = n - test_size

        train_data = entity_data.iloc[:train_size]
        test_data = entity_data.iloc[train_size:]

        # Get MASE using Catboost
        entity_mase = forecast_catboost(train_data, test_data, seasonality)

        if not np.isnan(entity_mase):
            mase_values.append(entity_mase)

    # Calculate mean MASE across all entities
    mean_mase = np.mean(mase_values)
    median_mase = np.median(mase_values)

    # Global Forecasting

    train_index = int((1 - test_ratio) * len(proc_df))
    global_mase = forecast_catboost(proc_df.iloc[:train_index],
                                    proc_df.iloc[train_index:],
                                    seasonality,
                                    True)

    # Printing and saving results

    print("\nCatboost Forecasting Results:")
    print(f"Number of entities successfully forecasted: {len(mase_values)}")
    print(f"Mean MASE: {mean_mase:.4f}")
    print(f"Median MASE: {median_mase:.4f}")


    results_df = pd.DataFrame(
        {
            "model": ["Catboost"],
            "seasonality": [seasonality],
            "mean_mase": [mean_mase],
            "median_mase": [median_mase],
            "entity_count": [len(mase_values)],
            "global_mase": [global_mase],
        }
    )

    results_df.to_csv(OUTPUT_DIR / "raw_results" / "catboost_results.csv", index=False)
