"""
Simple Darts global-model forecasting example (single-file).

Standard interface:
  - Dataset path via environment variable `DATASET_PATH`
  - Run with `pixi run main`
  - Test GPU with `pixi run test-gpu`

What it does:
  1) Loads the full panel (all series) from an ftsfr_*.parquet dataset
  2) Trains a global Darts model (default: DLinear)
  3) Forecasts on the test sets of all series
  4) Reports aggregate MASE across series

Notes:
  - Dataset metadata (frequency, seasonality) is read from datasets.toml via config_reader.
  - Assumes standardized ftsfr format with columns: 'unique_id', 'ds', 'y'.
  - Change MODEL_NAME to try 'dlinear' or 'nlinear'.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from darts import TimeSeries
from darts.models import DLinearModel, NLinearModel
from darts.metrics import mase

# Allow importing shared config reader from parent directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config_reader import get_model_config  # type: ignore


# -----------------------------------------------------------------------------
# Configuration (edit these two lines)
# -----------------------------------------------------------------------------

# Choose a global model: 'dlinear' or 'nlinear' (default: 'dlinear')
MODEL_NAME: str = os.environ.get("MODEL_NAME", "dlinear")


def load_panel_series(dataset_path: Path) -> List[TimeSeries]:
    """
    Load a parquet with standardized ftsfr schema and return a list of Darts TimeSeries,
    one per 'unique_id'. Requires columns: 'unique_id', 'ds', 'y'.
    """
    df = pd.read_parquet(dataset_path)
    required_cols = {"unique_id", "ds", "y"}
    missing = required_cols.difference(df.columns)
    if missing:
        raise KeyError(f"Dataset is missing required columns: {sorted(missing)}")

    df = df.dropna(subset=["ds", "y"]).sort_values(by=["unique_id", "ds"])  # type: ignore[arg-type]
    series_list = TimeSeries.from_group_dataframe(
        df,
        group_cols=["unique_id"],
        time_col="ds",
        value_cols="y",
    )
    return series_list


def train_test_split_series(
    series: TimeSeries, test_split: float
) -> Tuple[TimeSeries, TimeSeries]:
    n = len(series)
    test_len = max(1, int(round(n * test_split)))
    split_point = max(1, n - test_len)
    train, test = series[:split_point], series[split_point:]
    return train, test


def create_model(model_name: str, seasonality: int):
    name = model_name.lower()
    if name == "dlinear":
        return DLinearModel(n_epochs=10)
    if name == "nlinear":
        return NLinearModel(n_epochs=10)
    raise ValueError(
        f"Unsupported MODEL_NAME: {model_name}. Use 'dlinear' or 'nlinear'."
    )


def main():
    # Get config from shared reader (requires DATASET_PATH env var)
    test_split, frequency, seasonality, dataset_path, _output_dir, dataset_name = (
        get_model_config()
    )

    series_list = load_panel_series(Path(dataset_path))
    if len(series_list) == 0:
        raise ValueError("No series found after grouping by 'unique_id'.")

    # Split all series
    splits = [train_test_split_series(s, float(test_split)) for s in series_list]
    train_list = [t for t, _ in splits]
    test_list = [u for _, u in splits]

    model = create_model(MODEL_NAME, seasonality)
    model.fit(train_list)

    # Predict for all series, then compute global MASE using Darts' built-in metric
    fcst_list = []
    for train_s, test_s in zip(train_list, test_list):
        horizon = len(test_s)
        fcst_list.append(model.predict(n=horizon, series=train_s))

    mase_mean = mase(
        actual_series=test_list, pred_series=fcst_list, insample=train_list
    )

    # Summary
    print("Darts Global Example")
    print(f"  Dataset: {dataset_name}")
    print(f"  Model:   {MODEL_NAME}")
    print(f"  Num series: {len(series_list)}")
    print(f"  Frequency: {frequency}, Seasonality: {seasonality}")
    print(
        f"  Mean MASE across series: {mase_mean:.4f}"
        if mase_mean == mase_mean
        else "  Mean MASE: NaN (undefined)"
    )


if __name__ == "__main__":
    main()
