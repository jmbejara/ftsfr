"""
Exponential Smoothing(ETS) using darts.

Performs local forecasting using ETS. Reports both mean and
median MASE for local forecasts.
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

from darts.models import ExponentialSmoothing
from darts import TimeSeries
from darts.utils.missing_values import fill_missing_values
from darts.utils.model_selection import train_test_split
from darts.utils.utils import ModelMode, SeasonalityMode

from darts.metrics import mase


def forecast_ets(df, test_ratio, seasonality):
    """
    Fit ETS model and return MASE

    Parameters:
    -----------
    df : array-like
        array-like object(e.g. pd.DataFrame) with a single series which is split
        into testing and training data.
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
        test_length = int(test_ratio * len(df))
        # TimeSeries object is important for darts
        raw_series = TimeSeries.from_dataframe(df, time_col="date")
        # Replace NaNs automatically
        raw_series = fill_missing_values(raw_series)
        # Splitting into train and test
        series, test_series = train_test_split(raw_series, test_size=test_ratio)
        # Training the model and getting MASE
        estimator = ExponentialSmoothing(
            trend=ModelMode.ADDITIVE, damped=True, seasonal=SeasonalityMode.NONE
        )
        estimator.fit(series)
        pred_series = estimator.predict(test_length)
        return mase(test_series, pred_series, series, seasonality)
    except Exception as e:
        # In case of errors, return NaN
        print(f"Error in ETS forecasting: {e}")
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
    proc_df.rename_axis(None, axis=1, inplace=True)

    # Define forecasting parameters
    test_ratio = 0.2  # Use last 20% of the data for testing
    forecast_horizon = 20  # 20 business days, 4 weeks, about a month
    seasonality = 5  # 5 for weekly patterns (business days)

    # Process each entity separately
    entities = df["entity"].unique()
    mase_values = []

    # Local forecasting

    print(f"Running ETS forecasting for {len(entities)} entities...")

    for entity in tqdm(entities):
        # Filter data for the current entity
        entity_data = proc_df[["date", entity]]

        # Removing leading NaNs which show up due to different start times
        # of different series
        entity_data = entity_data.iloc[entity_data[entity].first_valid_index() :]

        if len(entity_data) <= 10:  # Skip entities with too few observations
            continue

        # Get MASE using ETS
        entity_mase = forecast_ets(entity_data, test_ratio, seasonality)

        if not np.isnan(entity_mase):
            mase_values.append(entity_mase)

    # Calculate mean MASE across all entities
    mean_mase = np.mean(mase_values)
    median_mase = np.median(mase_values)

    # Printing and saving results

    print("\nETS Forecasting Results:")
    print(f"Number of entities successfully forecasted: {len(mase_values)}")
    print(f"Mean MASE: {mean_mase:.4f}")
    print(f"Median MASE: {median_mase:.4f}")

    results_df = pd.DataFrame(
        {
            "model": ["ETS"],
            "seasonality": [seasonality],
            "mean_mase": [mean_mase],
            "median_mase": [median_mase],
            "entity_count": [len(mase_values)],
        }
    )

    results_df.to_csv(OUTPUT_DIR / "raw_results" / "ets_results.csv", index=False)
