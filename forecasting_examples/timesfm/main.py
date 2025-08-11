"""
Single-file TimesFM example: load an ftsfr parquet dataset, forecast with TimesFM, compute MASE.

Standard interface:
  - Dataset path via environment variable `DATASET_PATH`
  - Run with `pixi run main`
  - Test GPU with `pixi run test-gpu`
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd

import timesfm

# Allow importing shared config reader from parent directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config_reader import get_model_config  # type: ignore


# ----------------------------
# User-configurable parameters
# ----------------------------

# Optional: override forecast horizon (defaults to dataset seasonality); can be set via env var HORIZON
HORIZON_ENV = os.environ.get("HORIZON")
HORIZON: int | None = int(HORIZON_ENV) if HORIZON_ENV is not None else None

# Use 500m or 200m checkpoint
TIMESFM_VERSION = "500m"


# ----------------------------
# Implementation
# ----------------------------


FREQ_MAP: Dict[str, str] = {
    "B": "B",
    "D": "D",
    "W": "W",
    "MS": "MS",
    "ME": "M",
    "QS": "QS",
    "QE": "Q",
    "YS": "YS",
    "YE": "Y",
}


# Removed local datasets.toml readers; use shared config_reader.get_model_config


def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    # Standardized columns per repo conventions
    if "unique_id" not in df.columns:
        # backward compatibility in case some datasets use 'id'
        df = df.rename(columns={"id": "unique_id"})
    df = df[["unique_id", "ds", "y"]].copy()
    if not np.issubdtype(df["ds"].dtype, np.datetime64):
        df["ds"] = pd.to_datetime(df["ds"], utc=False, errors="raise")
    return df.sort_values(["unique_id", "ds"]).reset_index(drop=True)


def split_train_test(df: pd.DataFrame, h: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    def _split(group: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        if len(group) <= h:
            return group.iloc[0:0], group
        return group.iloc[:-h], group.iloc[-h:]

    trains, tests = [], []
    for _, g in df.groupby("unique_id", sort=False):
        tr, te = _split(g)
        trains.append(tr)
        tests.append(te)
    return pd.concat(trains, ignore_index=True), pd.concat(tests, ignore_index=True)


def compute_mase_per_series(
    y_train: np.ndarray, y_test: np.ndarray, y_hat: np.ndarray, seasonal_period: int
) -> float:
    y_train = np.asarray(y_train, dtype=float)
    y_test = np.asarray(y_test, dtype=float)
    y_hat = np.asarray(y_hat, dtype=float)
    if len(y_test) == 0 or len(y_hat) == 0 or len(y_test) != len(y_hat):
        return np.nan
    if len(y_train) > seasonal_period:
        scale = np.mean(np.abs(y_train[seasonal_period:] - y_train[:-seasonal_period]))
    elif len(y_train) > 1:
        scale = np.mean(np.abs(np.diff(y_train)))
    else:
        return np.nan
    if scale == 0:
        return np.nan
    mae = np.mean(np.abs(y_test - y_hat))
    return float(mae / scale)


def compute_panel_mase(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    fcst_df: pd.DataFrame,
    seasonal_period: int,
) -> float:
    merged = test_df.merge(fcst_df, on=["unique_id", "ds"], how="inner")
    mases = []
    for uid, g in merged.groupby("unique_id", sort=False):
        y_train = train_df.loc[train_df["unique_id"] == uid, "y"].values
        y_test = g["y"].values
        y_hat = g["y_hat"].values
        mases.append(compute_mase_per_series(y_train, y_test, y_hat, seasonal_period))
    return float(np.nanmean(np.array(mases, dtype=float)))


def build_timesfm(version: str, backend: str):
    if version == "200m":
        repo_id = "google/timesfm-1.0-200m-pytorch"
    else:
        repo_id = "google/timesfm-2.0-500m-pytorch"
    model = timesfm.TimesFm(
        hparams=timesfm.TimesFmHparams(
            backend=backend,  # "gpu" or "cpu"
            per_core_batch_size=32,
            horizon_len=128,
            num_layers=50,
            use_positional_embedding=False,
            context_len=2048,
        ),
        checkpoint=timesfm.TimesFmCheckpoint(huggingface_repo_id=repo_id),
    )
    return model


def infer_backend() -> str:
    # Prefer GPU if available
    try:
        import torch

        if torch.cuda.is_available():
            return "gpu"
    except Exception:
        pass
    return "cpu"


def timesfm_forecast(
    df_train: pd.DataFrame, freq: str, model: timesfm.TimesFm
) -> pd.DataFrame:
    # Forecast next step per series using TimesFM convenience API
    forecast_df = model.forecast_on_df(
        inputs=df_train,
        freq=freq,
        value_name="y",
        num_jobs=-1,
    )
    # timesfm column contains the prediction; keep only next step per series
    forecast_df = forecast_df[["unique_id", "ds", "timesfm"]]
    forecast_df = forecast_df.groupby("unique_id", as_index=False).first()
    forecast_df = forecast_df.rename(columns={"timesfm": "y_hat"})
    return forecast_df


def main() -> None:
    # Get config from shared reader (requires DATASET_PATH env var)
    test_split, freq_key, seasonality, dataset_path, _output_dir, dataset_name = (
        get_model_config()
    )
    freq = FREQ_MAP.get(freq_key, None)
    h = HORIZON if HORIZON is not None else int(seasonality)

    df = load_dataset(Path(dataset_path))
    df_train, df_test = split_train_test(df, h=h)

    backend = infer_backend()
    model = build_timesfm(TIMESFM_VERSION, backend=backend)

    # TimesFM returns a full horizon forecast if we slide windows; for simplicity, do one-step per step
    # Build forecasts for each test timestamp sequentially
    unique_test_ts = sorted(df_test["ds"].unique().tolist())
    all_fcst = []
    for ts in unique_test_ts:
        train_until_ts = df[df["ds"] < ts]
        fcst_step = model.forecast_on_df(
            inputs=train_until_ts,
            freq=freq,
            value_name="y",
            num_jobs=-1,
        )[["unique_id", "ds", "timesfm"]]
        # Keep only the forecast for the next horizon (TimesFM returns future ds)
        fcst_next = fcst_step.groupby("unique_id", as_index=False).first()
        fcst_next["ds"] = ts
        fcst_next = fcst_next.rename(columns={"timesfm": "y_hat"})
        all_fcst.append(fcst_next)

    fcst_df = pd.concat(all_fcst, ignore_index=True)

    mase = compute_panel_mase(
        train_df=df_train, test_df=df_test, fcst_df=fcst_df, seasonal_period=seasonality
    )
    n_series = df["unique_id"].nunique()
    print(
        f"Dataset={dataset_name} | Model=TimesFM-{TIMESFM_VERSION} | Backend={infer_backend()} | H={h} | Series={n_series} | MASE={mase:.4f}"
    )


if __name__ == "__main__":
    main()
