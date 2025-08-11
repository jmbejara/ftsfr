"""
Simple Nixtla (StatsForecast) example: load a dataset, train a model, forecast, and compute MASE.

Standard interface:
  - Dataset path via environment variable `DATASET_PATH`
  - Run with `pixi run main`
  - Test GPU with `pixi run test-gpu`
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd

from statsforecast import StatsForecast
from statsforecast.models import ETS, Naive, SeasonalNaive

# Allow importing shared config reader from parent directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config_reader import get_model_config  # type: ignore


# ----------------------------
# User-configurable parameters
# ----------------------------

# Choose a simple model: "seasonal_naive", "naive", or "ets"
MODEL_NAME = os.environ.get("MODEL_NAME", "seasonal_naive")

# Optional: horizon. If None, defaults to the dataset's seasonality from datasets.toml
HORIZON_ENV = os.environ.get("HORIZON")
HORIZON: int | None = int(HORIZON_ENV) if HORIZON_ENV is not None else None


# ----------------------------
# Implementation
# ----------------------------


@dataclass(frozen=True)
class DatasetMeta:
    frequency_key: str
    seasonality: int


FREQ_MAP: Dict[str, str] = {
    # Map repository frequency keys to pandas/StatsForecast freq strings
    "B": "B",
    "D": "D",
    "W": "W",
    "MS": "MS",
    "ME": "M",  # month end -> pandas 'M'
    "QS": "QS",
    "QE": "Q",  # quarter end -> pandas 'Q'
    "YS": "YS",
    "YE": "Y",
}


# Removed local datasets.toml readers; use shared config_reader.get_model_config


def load_panel_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    # Ensure types
    df = df[["unique_id", "ds", "y"]].copy()
    if not np.issubdtype(df["ds"].dtype, np.datetime64):
        df["ds"] = pd.to_datetime(df["ds"], utc=False, errors="raise")
    return df


def split_train_test(df: pd.DataFrame, h: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = df.sort_values(["unique_id", "ds"])  # ensure order

    # train: all but last h per series; test: last h per series
    def _split(group: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        if len(group) <= h:
            return group.iloc[0:0], group  # empty train, all test
        return group.iloc[:-h], group.iloc[-h:]

    trains: Iterable[pd.DataFrame] = []
    tests: Iterable[pd.DataFrame] = []
    for _, g in df.groupby("unique_id", sort=False):
        tr, te = _split(g)
        trains.append(tr)
        tests.append(te)
    train_df = pd.concat(trains, ignore_index=True)
    test_df = pd.concat(tests, ignore_index=True)
    return train_df, test_df


def build_model(name: str, seasonality: int):
    name = name.lower()
    if name == "seasonal_naive":
        return SeasonalNaive(season_length=seasonality)
    if name == "naive":
        return Naive()
    if name == "ets":
        # ETS handles seasonality internally; still pass freq to StatsForecast
        return ETS(season_length=seasonality, model="AAN")
    raise ValueError(
        "Unsupported MODEL_NAME. Choose from {'seasonal_naive','naive','ets'}."
    )


def forecast_panel(train_df: pd.DataFrame, model, freq: str, h: int) -> pd.DataFrame:
    sf = StatsForecast(models=[model], freq=freq, n_jobs=1)
    sf.fit(df=train_df)
    fcst = sf.forecast(df=train_df, h=h)
    # Rename prediction column to 'y_hat'
    pred_cols = [c for c in fcst.columns if c not in ("unique_id", "ds")]
    if len(pred_cols) != 1:
        raise RuntimeError("Expected a single model column in forecast output.")
    fcst = fcst.rename(columns={pred_cols[0]: "y_hat"})
    return fcst


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
        # Fallback to non-seasonal naive differences
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
    test_merged = test_df.merge(fcst_df, on=["unique_id", "ds"], how="inner")
    mases: list[float] = []
    for uid, g in test_merged.groupby("unique_id", sort=False):
        y_train = train_df.loc[train_df["unique_id"] == uid, "y"].values
        y_test = g["y"].values
        y_hat = g["y_hat"].values
        mases.append(compute_mase_per_series(y_train, y_test, y_hat, seasonal_period))
    mases_arr = np.array(mases, dtype=float)
    return float(np.nanmean(mases_arr))


def main() -> None:
    # Get config from shared reader (requires DATASET_PATH env var)
    test_split, frequency_key, seasonality, dataset_path, _output_dir, dataset_name = (
        get_model_config()
    )
    freq = FREQ_MAP.get(frequency_key, None)
    h = HORIZON if HORIZON is not None else int(seasonality)

    df = load_panel_dataset(Path(dataset_path))

    train_df, test_df = split_train_test(df, h=h)
    model = build_model(MODEL_NAME, seasonality=int(seasonality))
    fcst_df = forecast_panel(train_df, model=model, freq=freq, h=h)

    mase = compute_panel_mase(
        train_df=train_df,
        test_df=test_df,
        fcst_df=fcst_df,
        seasonal_period=int(seasonality),
    )

    n_series = df["unique_id"].nunique()
    print(
        f"Dataset={dataset_name} | Model={MODEL_NAME} | H={h} | Series={n_series} | MASE={mase:.4f}"
    )


if __name__ == "__main__":
    main()
