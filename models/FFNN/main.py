from pathlib import Path
from warnings import filterwarnings

import toml
from decouple import config

from gluonts.mx.model.simple_feedforward import SimpleFeedForwardEstimator
from gluonts.dataset.common import ListDataset
from gluonts.dataset.field_names import FieldName
from gluonts.evaluation.backtest import make_evaluation_predictions
from gluonts.evaluation import Evaluator

import pandas as pd

filterwarnings("ignore")

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
   "1W": 365.25/7,
   "1M": 12,
   "1Q": 4,
   "1Y": 1
}

def get_deep_nn_forecasts(lag, proc_df, external_forecast_horizon = None):
    """
    Takes PKL file and writes the results into respective files

    :param dataset_name: the name of the dataset
    :param lag: the number of past lags that should be used when predicting the next future value of time series
    :param input_file_name: name of the .tsf file corresponding with the dataset
    :param method: name of the forecasting method that you want to evaluate
    :param external_forecast_horizon: the required forecast horizon, if it is not available in the .tsf file
    :param integer_conversion: whether the forecasts should be rounded or not
    
    """

    # raw_df = pd.read_parquet(input_file_name)
    # df = raw_df.groupby(TIME_COL_NAME).agg(lambda x: pd.array(x)).reset_index()

    df = proc_df

    train_series_list = []
    test_series_list = []
    train_series_full_list = []
    test_series_full_list = []

    # Automatic frequency inference
    _offset = pd.infer_freq(df[TIME_COL_NAME])
    if _offset == "min":
        freq = '10' + "min"
    # 1M makes FRED work
    else:
        freq = '1' + _offset if _offset else "1M"

    seasonality = SEASONALITY_MAP_ADAPT[freq]

    if isinstance(seasonality, list):
        seasonality = min(seasonality) # Use to calculate MASE

    if external_forecast_horizon is None:
        raise Exception("Please provide the required forecast horizon")
    else:
        forecast_horizon = external_forecast_horizon

    for index, row in df.iterrows():
        train_start_time = row[TIME_COL_NAME]
        series_data = row[VALUE_COL_NAME]

        # Creating training and test series. Test series will be only used during evaluation
        train_series_data = series_data[:len(series_data) - forecast_horizon]
        test_series_data = series_data[(len(series_data) - forecast_horizon) : len(series_data)]

        train_series_list.append(train_series_data)
        test_series_list.append(test_series_data)

        # We use full length training series to train the model as we do not tune hyperparameters
        # FieldName.START: pd.Timestamp(train_start_time, freq=freq)

        train_series_full_list.append({
            FieldName.TARGET: train_series_data,
            FieldName.START: pd.Timestamp(train_start_time)
        })

        test_series_full_list.append({
            FieldName.TARGET: series_data,
            FieldName.START: pd.Timestamp(train_start_time)
        })

    train_ds = ListDataset(train_series_full_list, freq=freq)
    test_ds = ListDataset(test_series_full_list, freq=freq)

    estimator = SimpleFeedForwardEstimator(context_length=lag,
                                               prediction_length=forecast_horizon)

    predictor = estimator.train(training_data=train_ds)

    forecast_it, ts_it = make_evaluation_predictions(dataset=test_ds, predictor=predictor, num_samples=100)

    # Time series predictions
    forecasts = list(forecast_it)

    tss = list(ts_it)

    evaluator = Evaluator(quantiles=[0.1, 0.5, 0.9])
    agg_metrics, item_metrics = evaluator(tss, forecasts)

    return agg_metrics["MASE"]


DATA_DIR = config(
    "DATA_DIR", cast=Path, default=Path(__file__).parent.parent.parent / "_data"
)
OUTPUT_DIR = config(
    "OUTPUT_DIR", cast=Path, default=Path(__file__).parent.parent.parent / "_output"
)
datasets_info = toml.load(DATA_DIR / "ftsfr_datasets_paths.toml")

file_path = DATA_DIR / datasets_info["treas_yield_curve_zero_coupon"]
raw_df = pd.read_parquet(file_path)

proc_df = raw_df.groupby('entity').agg(lambda x: pd.array(x)).reset_index()
proc_df['date'] = proc_df['date'].iloc[0][0]

# Define forecasting parameters
test_ratio = 0.2  # Use last 20% of the data for testing
forecast_horizon = 20  # 20 business days, 4 weeks, about a month
seasonality = 5  # 5 for weekly patterns (business days)

mean_mase = get_deep_nn_forecasts(100, proc_df, 1)

print("\FFNN Forecasting Results:")
print(f"Mean MASE: {mean_mase:.4f}")


results_df = pd.DataFrame(
    {
        "model": ["FFNN"],
        "seasonality": [seasonality],
        "mean_mase": [mean_mase],
        # "median_mase": [median_mase],
        # "entity_count": [len(mase_values)],
    }
)


results_df.to_csv(OUTPUT_DIR / "raw_results" / "ffnn_results.csv", index=False)
