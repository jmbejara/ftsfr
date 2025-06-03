from pathlib import Path
from warnings import filterwarnings

import numpy as np
import pandas as pd
import toml
from decouple import config
from statsmodels.tsa.arima.model import ARIMA
from tqdm import tqdm

# Ignore convergence warnings from ARIMA
filterwarnings("ignore")


def calculate_mase(y_true, y_pred, training_set, seasonality=1):
    """
    Calculate MASE (Mean Absolute Scaled Error) as defined in the Monash Forecasting Archive.

    Parameters:
    -----------
    y_true : array-like
        Actual test values
    y_pred : array-like
        Predicted values from the model
    training_set : array-like
        Training set used to fit the model
    seasonality : int, default=1
        Seasonality of the time series (S parameter in the MASE formula)

    Returns:
    --------
    float
        MASE value
    """
    n_train = len(training_set)
    h = len(y_true)

    # Calculate the numerator: sum of absolute errors
    numerator = np.sum(np.abs(y_true - y_pred))

    # Calculate the denominator: scaled in-sample naive forecast error
    if seasonality >= n_train:
        # Handle case where seasonality is larger than the training set
        denominator = np.sum(np.abs(np.diff(training_set)))
    else:
        # Use seasonal naive forecast for denominator
        denominator = np.sum(
            np.abs(training_set[seasonality:] - training_set[:-seasonality])
        )

    # Adjust denominator as per the formula
    denominator = denominator * (h / (n_train - seasonality))

    # Handle edge cases
    if denominator == 0:
        return np.nan

    return numerator / denominator


def forecast_arima(train_data, test_length, order=(1, 1, 1)):
    """
    Fit ARIMA model and generate forecasts

    Parameters:
    -----------
    train_data : array-like
        Training data
    test_length : int
        Number of periods to forecast
    order : tuple, default=(1,1,1)
        ARIMA order (p,d,q)

    Returns:
    --------
    array-like
        Forecasted values
    """
    try:
        model = ARIMA(train_data, order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=test_length)
        return forecast
    except Exception as e:
        # In case of errors (e.g., non-convergence), return NaN array
        print(f"Error in ARIMA forecasting: {e}")
        return np.full(test_length, np.nan)


DATA_DIR = config(
    "DATA_DIR", cast=Path, default=Path(__file__).parent.parent.parent / "_data"
)
OUTPUT_DIR = config(
    "OUTPUT_DIR", cast=Path, default=Path(__file__).parent.parent.parent / "_output"
)
datasets_info = toml.load(DATA_DIR / "ftsfr_datasets_paths.toml")

file_path = DATA_DIR / datasets_info["treas_yield_curve_zero_coupon"]
df = pd.read_parquet(file_path)


# Define forecasting parameters
test_ratio = 0.2  # Use last 20% of the data for testing
forecast_horizon = 20  # 20 business days, 4 weeks, about a month
seasonality = 5  # 5 for weekly patterns (business days)
arima_order = (1, 1, 1)  # Default ARIMA order, can be tuned

# Process each entity separately
entities = df["entity"].unique()
mase_values = []

print(f"Running ARIMA forecasting for {len(entities)} entities...")

for entity in tqdm(entities):
    # Filter data for the current entity
    entity_data = df[df["entity"] == entity].sort_values("date")
    entity_data = entity_data.dropna()

    if len(entity_data) <= 10:  # Skip entities with too few observations
        continue

    # Extract values
    values = entity_data["value"].values

    # Determine train/test split
    n = len(values)
    test_size = max(1, int(n * test_ratio))
    train_size = n - test_size

    train_data = values[:train_size]
    test_data = values[train_size:]

    forecast_horizon = len(test_data)

    # Generate forecasts using ARIMA
    forecasts = forecast_arima(train_data, forecast_horizon, arima_order)

    # Calculate MASE for this entity
    entity_mase = calculate_mase(test_data, forecasts, train_data, seasonality)

    if not np.isnan(entity_mase):
        mase_values.append(entity_mase)

# Calculate mean MASE across all entities
mean_mase = np.mean(mase_values)
median_mase = np.median(mase_values)


print("\nARIMA Forecasting Results:")
print(f"Number of entities successfully forecasted: {len(mase_values)}")
print(f"Mean MASE: {mean_mase:.4f}")
print(f"Median MASE: {median_mase:.4f}")


results_df = pd.DataFrame(
    {
        "model": ["ARIMA(1,1,1)"],
        "seasonality": [seasonality],
        "mean_mase": [mean_mase],
        "median_mase": [median_mase],
        "entity_count": [len(mase_values)],
    }
)


results_df.to_csv(OUTPUT_DIR / "raw_results" / "arima_results.csv", index=False)
