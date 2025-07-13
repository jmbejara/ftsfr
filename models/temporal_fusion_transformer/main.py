"""
Temporal Fusion Transformer(TFT) using GluonTS.

Performs both local and global forecasting using TFT. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""

from pathlib import Path
from warnings import filterwarnings

filterwarnings("ignore")

import toml
from tqdm import tqdm
import numpy as np
from decouple import config

from gluonts.torch import TemporalFusionTransformerEstimator
from gluonts.dataset.common import ListDataset
from gluonts.dataset.field_names import FieldName
from gluonts.evaluation.backtest import make_evaluation_predictions
from gluonts.evaluation import Evaluator

import pandas as pd

# The name of the column containing time series values
VALUE_COL_NAME = "value"

# The name of the column containing timestamps
TIME_COL_NAME = "date"

SEASONALITY_MAP_ADAPT = {
    "1min": [1440, 10080, 525960],
    "10min": [144, 1008, 52596],
    "30min": [48, 336, 17532],
    "1H": [24, 168, 8766],
    "1D": 7,
    "1B": 5,
    "1W": 365.25 / 7,
    "1M": 12,
    "1ME": 12,
    "1Q": 4,
    "1Y": 1,
}


def get_tft_forecasts_global(
    lag, df, test_ratio=0.2, frequency=None, external_forecast_horizon=None
):
    """
    Takes processed DataFrame, runs the training for a TFT model, and returns MASE

    :param lag: the number of past lags that should be used when predicting the
    future value of time series
    :param df: the processed DataFrame for training and evaluating
    :param frequency: the frequency of the time series
    :param external_forecast_horizon: the required forecast horizon

    :returns MASE

    """

    train_series_list = []
    test_series_list = []
    train_series_full_list = []
    test_series_full_list = []

    # Automatic frequency inference
    if not frequency:
        _offset = pd.infer_freq(df[TIME_COL_NAME])
        if _offset == "min":
            freq = "10" + "min"
        # 1M makes FRED work
        else:
            freq = "1" + _offset if _offset else "1ME"
    else:
        freq = frequency

    seasonality = SEASONALITY_MAP_ADAPT[freq]

    if isinstance(seasonality, list):
        seasonality = min(seasonality)  # Use to calculate MASE

    if external_forecast_horizon is None:
        raise Exception("Please provide the required forecast horizon")
    else:
        forecast_horizon = external_forecast_horizon

    for index, row in df.iterrows():
        train_start_time = row[TIME_COL_NAME]
        series_data = row[VALUE_COL_NAME]

        # Creating training and test series. Test series will be only used during evaluation
        train_index = int(test_ratio * len(series_data))
        train_series_data = series_data[:train_index]
        test_series_data = series_data[train_index:]

        train_series_list.append(train_series_data)
        test_series_list.append(test_series_data)

        # We use full length training series to train the model as we do not tune hyperparameters
        # FieldName.START: pd.Timestamp(train_start_time, freq=freq)

        train_series_full_list.append(
            {
                FieldName.TARGET: train_series_data,
                FieldName.START: pd.Timestamp(train_start_time),
            }
        )

        test_series_full_list.append(
            {
                FieldName.TARGET: series_data,
                FieldName.START: pd.Timestamp(train_start_time),
            }
        )

    train_ds = ListDataset(train_series_full_list, freq=freq)
    test_ds = ListDataset(test_series_full_list, freq=freq)

    estimator = TemporalFusionTransformerEstimator(
        freq=freq, context_length=lag, prediction_length=forecast_horizon
    )

    predictor = estimator.train(training_data=train_ds)

    forecast_it, ts_it = make_evaluation_predictions(
        dataset=test_ds, predictor=predictor, num_samples=100
    )

    # Time series predictions
    forecasts = list(forecast_it)

    tss = list(ts_it)

    evaluator = Evaluator(quantiles=[0.1, 0.5, 0.9])
    agg_metrics, item_metrics = evaluator(tss, forecasts)

    return agg_metrics["MASE"]


def get_tft_forecasts_local(lag, df, frequency, external_forecast_horizon=None):
    """
    Takes processed DataFrame containing multiple or single time series, runs
    the training for a separate TFT model on each series, and returns MASE
    list for each entity

    :param lag: the number of past lags that should be used when predicting the
    next future value of time series
    :param df: the processed DataFrame for training and evaluating
    :param frequency: frequency of the series which needs to be the same for all
    the series in df
    :param external_forecast_horizon: the required forecast horizon

    """

    # Process each entity separately
    entities = df["entity"].unique()
    mase_values = []

    print(f"Running TFT forecasting for {len(entities)} entities...")

    for entity in tqdm(entities):
        # Filter data for the current entity
        entity_data = df[df["entity"] == entity]

        # Generate forecasts using ARIMA
        entity_mase = get_tft_forecasts_global(
            lag=lag,
            df=entity_data,
            test_ratio=test_ratio,
            frequency=frequency,
            external_forecast_horizon=external_forecast_horizon,
        )

        if not np.isnan(entity_mase):
            mase_values.append(entity_mase)

    return mase_values


if __name__ == "__main__":
    DATA_DIR = config(
        "DATA_DIR", cast=Path, default=Path(__file__).parent.parent.parent / "_data"
    )
    OUTPUT_DIR = config(
        "OUTPUT_DIR", cast=Path, default=Path(__file__).parent.parent.parent / "_output"
    )
    datasets_info = toml.load(DATA_DIR / "ftsfr_datasets_paths.toml")

    file_path = DATA_DIR / datasets_info["treas_yield_curve_zero_coupon"]
    raw_df = pd.read_parquet(file_path)

    proc_df = raw_df.groupby("entity").agg(lambda x: pd.array(x)).reset_index()
    proc_df["date"] = proc_df["date"].iloc[0][0]
    proc_df["value"] = proc_df["value"].apply(lambda x: x.to_numpy())

    # Define forecasting parameters
    test_ratio = 0.2  # Use last 20% of the data for testing
    forecast_horizon = 20  # 20 business days, 4 weeks, about a month
    seasonality = 5  # 5 for weekly patterns (business days)

    # Process each entity separately
    entities = proc_df["entity"].unique()
    mase_values = get_tft_forecasts_local(
        lag=50, df=proc_df, frequency="1B", external_forecast_horizon=forecast_horizon
    )

    # Calculate mean MASE across all entities
    mean_mase = np.mean(mase_values)
    median_mase = np.median(mase_values)

    # Global Forecasting

    global_mase = get_tft_forecasts_global(
        lag=50,
        df=proc_df,
        test_ratio=0.2,
        frequency="1B",
        external_forecast_horizon=forecast_horizon,
    )

    # Printing and saving results

    print("\nTFT Forecasting Results:")
    print(f"Number of entities successfully forecasted: {len(mase_values)}")
    print(f"Mean MASE: {mean_mase:.4f}")
    print(f"Median MASE: {median_mase:.4f}")
    print(f"Global MASE: {global_mase:.4f}")

    results_df = pd.DataFrame(
        {
            "model": ["TFT"],
            "seasonality": [seasonality],
            "mean_mase": [mean_mase],
            "median_mase": [median_mase],
            "entity_count": [len(mase_values)],
            "global_mase": [global_mase],
        }
    )

    results_df.to_csv(OUTPUT_DIR / "raw_results" / "tft_results.csv", index=False)
