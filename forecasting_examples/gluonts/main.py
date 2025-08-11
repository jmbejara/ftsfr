"""
Simple GluonTS forecasting example (single-file).

Standard interface:
  - Dataset path via environment variable `DATASET_PATH`
  - Run with `pixi run main`
  - Test GPU with `pixi run test-gpu`

What it does:
  1) Loads one univariate series from an ftsfr_*.parquet dataset (columns: 'unique_id', 'ds', 'y')
  2) Trains a GluonTS model (default: DeepAR)
  3) Forecasts on the test set
  4) Reports MASE
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd

from gluonts.dataset.common import ListDataset
from gluonts.torch import Trainer
from gluonts.torch.model.deepar import DeepAREstimator
from gluonts.torch.model.simple_feedforward import SimpleFeedForwardEstimator

# Allow importing shared config reader from parent directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config_reader import get_model_config  # type: ignore


# -----------------------------------------------------------------------------
# Configuration (edit these lines)
# -----------------------------------------------------------------------------

# Choose a simple model: 'deepar' or 'ffnn'
MODEL_NAME: str = "deepar"

# Optionally pick a specific series within a panel dataset via env var UNIQUE_ID
UNIQUE_ID: Optional[str] = os.environ.get("UNIQUE_ID")

# TEST_SPLIT, FREQUENCY, SEASONALITY, DATASET_PATH are provided by config_reader

# Training epochs kept small for fast demo runs
MAX_EPOCHS: int = int(os.environ.get("N_EPOCHS", 5))


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def convert_frequency_for_gluonts(freq: str) -> str:
    """Convert datasets.toml frequency to GluonTS-friendly frequency."""
    mapping = {
        "ME": "M",  # month end -> month
        "QE": "Q",  # quarter end -> quarter
    }
    return mapping.get(freq, freq)


def load_univariate_series(
    dataset_path: Path, unique_id: Optional[str]
) -> pd.DataFrame:
    """
    Load a parquet with standardized ftsfr schema and return filtered DataFrame for one series.
    Requires columns: 'unique_id', 'ds', 'y'.
    """
    df = pd.read_parquet(dataset_path)
    required_cols = {"unique_id", "ds", "y"}
    missing = required_cols.difference(df.columns)
    if missing:
        raise KeyError(f"Dataset is missing required columns: {sorted(missing)}")

    if unique_id is None:
        series_id = df["unique_id"].iloc[0]
    else:
        series_id = unique_id

    slim = (
        df.loc[df["unique_id"] == series_id, ["ds", "y"]]
        .dropna()
        .sort_values(by="ds")
        .reset_index(drop=True)
    )
    return slim


def train_test_split(
    values: np.ndarray, test_split: float
) -> Tuple[np.ndarray, np.ndarray]:
    n = len(values)
    test_len = max(1, int(round(n * test_split)))
    split_point = n - test_len
    return values[:split_point], values[split_point:]


def create_estimator(
    model_name: str, freq: str, seasonality: int, prediction_length: int
):
    name = model_name.lower()
    context_length = max(seasonality * 4, prediction_length)
    trainer = Trainer(max_epochs=MAX_EPOCHS)

    if name == "deepar":
        return DeepAREstimator(
            freq=freq,
            prediction_length=prediction_length,
            context_length=context_length,
            trainer=trainer,
        )
    if name == "ffnn":
        return SimpleFeedForwardEstimator(
            freq=freq,
            prediction_length=prediction_length,
            context_length=context_length,
            trainer=trainer,
        )
    raise ValueError("Unsupported MODEL_NAME: use 'deepar' or 'ffnn'.")


def mase_manual(
    y_true: np.ndarray, y_pred: np.ndarray, y_insample: np.ndarray, m: int
) -> float:
    """
    Compute MASE manually.

    MASE = MAE(test) / MAE(seasonal naive on insample), with seasonal period m.
    """
    mae_num = np.mean(np.abs(y_true - y_pred))

    m_eff = int(m) if int(m) > 0 else 1
    if len(y_insample) <= m_eff:
        m_eff = 1

    diffs = np.abs(y_insample[m_eff:] - y_insample[:-m_eff])
    denom = np.mean(diffs) if len(diffs) > 0 else np.nan

    if denom == 0 or np.isnan(denom):
        return np.nan
    return float(mae_num / denom)


def main():
    # Get config from shared reader (requires DATASET_PATH env var)
    test_split, frequency_raw, seasonality, dataset_path, _output_dir, dataset_name = (
        get_model_config()
    )
    freq = convert_frequency_for_gluonts(frequency_raw)

    df = load_univariate_series(Path(dataset_path), UNIQUE_ID)
    values = df["y"].to_numpy(dtype=float)
    index = pd.to_datetime(df["ds"])  # ensure pandas datetime index

    train_values, test_values = train_test_split(values, float(test_split))
    prediction_length = len(test_values)

    estimator = create_estimator(MODEL_NAME, freq, seasonality, prediction_length)

    # Build GluonTS datasets
    train_ds = ListDataset(
        [
            {
                "start": pd.Timestamp(index.iloc[0]),
                "target": train_values,
            }
        ],
        freq=freq,
    )

    predictor = estimator.train(train_ds)

    test_input = ListDataset(
        [
            {
                "start": pd.Timestamp(index.iloc[0]),
                "target": train_values,
            }
        ],
        freq=freq,
    )

    forecast = list(predictor.predict(test_input))[0]
    y_pred = forecast.mean.reshape(-1)

    mase = mase_manual(test_values, y_pred, train_values, m=seasonality)

    # Summary
    print("GluonTS Simple Example")
    print(f"  Dataset: {dataset_name}")
    print(f"  Model:   {MODEL_NAME}")
    print(
        f"  Series length: {len(values)} (train={len(train_values)}, test={len(test_values)})"
    )
    print(f"  Frequency: {freq} (raw: {frequency_raw}), Seasonality: {seasonality}")
    print(f"  MASE: {mase:.4f}" if mase == mase else "  MASE: NaN (undefined)")


if __name__ == "__main__":
    main()
