"""
Simple Exponential Smoothing(SES) using darts.

Performs local forecasting using SES. Reports both mean and
median MASE for local forecasts.
"""

from pathlib import Path
from warnings import filterwarnings
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
# Darts-based imports
from darts.models import ExponentialSmoothing
from darts import TimeSeries
from darts.utils.missing_values import fill_missing_values
from darts.utils.model_selection import train_test_split
from darts.utils.utils import ModelMode, SeasonalityMode
from darts.metrics import mase

filterwarnings("ignore")


def forecast_ses(df, test_ratio, seasonality):
    """
    Fit SES model and return MASE

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
        raw_series = TimeSeries.from_dataframe(df, time_col="ds")
        # Replace NaNs automatically
        raw_series = fill_missing_values(raw_series)
        # Splitting into train and test
        series, test_series = train_test_split(raw_series, test_size=test_ratio)
        # Training the model and getting MASE
        estimator = ExponentialSmoothing(trend = ModelMode.NONE, seasonal = SeasonalityMode.NONE)
        estimator.fit(series)
        pred_series = estimator.predict(test_length)
        return mase(test_series, pred_series, series, seasonality)
    except Exception as e:
        # In case of errors, return NaN
        print(f"Error in SES forecasting: {e}")
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

    # Load data
    df = pd.read_parquet(dataset_path)

    # Check if data follows the expected format (id, ds, y)
    expected_columns = {"unique_id", "ds", "y"}
    if not expected_columns.issubset(df.columns):
        raise ValueError(
            f"Dataset must contain columns: {expected_columns}. Found: {df.columns}"
        )

    # This pivot adds all values for an entity as a TS in each column
    proc_df = df.pivot(index="ds", columns="unique_id", values="y").reset_index()
    # Basic cleaning
    proc_df.rename_axis(None, axis=1, inplace=True)

    # Define forecasting parameters based on frequency
    test_ratio = 0.2  # Use last 20% of the data for testing

    # Process each entity separately
    entities = df["unique_id"].unique()
    mase_values = []

    # Local forecasting
    print(f"Running SES forecasting for {len(entities)} entities...")
    print(f"Dataset: {dataset_name}")
    print(f"Frequency: {frequency}, Seasonality: {seasonality}")

    for entity in tqdm(entities):
        # Filter data for the current entity
        entity_data = proc_df[["ds", entity]]

        # Removing leading/trailing NaNs which show up due to different start 
        # times of different series
        if entity_data[entity].first_valid_index() is None:
            continue
        entity_data = entity_data.iloc[entity_data[entity].first_valid_index():
                                       entity_data[entity].last_valid_index()+1]

        if len(entity_data) <= 10:  # Skip entities with too few observations
            continue

        # Get MASE using SES
        entity_mase = forecast_ses(entity_data, test_ratio, seasonality)

        if not np.isnan(entity_mase):
            mase_values.append(entity_mase)

    # Calculate mean MASE across all entities
    mean_mase = np.mean(mase_values) if mase_values else np.nan
    median_mase = np.median(mase_values) if mase_values else np.nan

    # Printing and saving results
    print("\nSES Forecasting Results:")
    print(f"Number of entities successfully forecasted: {len(mase_values)}")
    print(f"Mean MASE: {mean_mase:.4f}")
    print(f"Median MASE: {median_mase:.4f}")

    results_df = pd.DataFrame(
        {
            "model": ["ses"],
            "dataset": [dataset_name],
            "frequency": [frequency],
            "seasonality": [seasonality],
            "mean_mase": [mean_mase],
            "median_mase": [median_mase],
            "entity_count": [len(mase_values)],
        }
    )

    # Save with the expected filename pattern
    results_file = OUTPUT_DIR / "raw_results" / f"ses_{dataset_name}_results.csv"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(results_file, index=False)