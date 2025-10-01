# %%
"""
# TIPS-Treasury Basis Spread Forecasting Walkthrough

This walkthrough demonstrates forecasting the 2-year TIPS-Treasury basis spread
using StatsForecast. The TIPS-Treasury basis represents the arbitrage spread
between Treasury Inflation-Protected Securities (TIPS) and nominal Treasury bonds.

This example helps us understand:
- How different statistical models perform on financial arbitrage spreads
- Which models capture the mean-reversion patterns typical of basis spreads
- Why certain models work well (or poorly) for this type of financial data

Based on the Nixtla StatsForecast documentation walkthrough, adapted for
financial time series data from the ftsfr repository.
"""

# %%
"""
## Data Overview

The TIPS-Treasury basis dataset contains arbitrage spreads for different maturities:
- arb_2: 2-year maturity
- arb_5: 5-year maturity
- arb_10: 10-year maturity
- arb_20: 20-year maturity

For this walkthrough, we'll focus on the 2-year maturity (arb_2) to understand
how well different models can forecast this financial arbitrage spread.
"""

# %%
"""
## Load and Prepare Data

Load the TIPS-Treasury basis data and filter to the 2-year maturity.
The data is in long format with columns: unique_id, ds (timestamp), y (basis spread).
"""

# %%
import polars as pl
import pandas as pd
from pathlib import Path
import sys

import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.auto import (
    AutoDeepAR,
    AutoNBEATS,
    AutoNHITS,
    AutoDLinear,
    AutoNLinear,
    AutoVanillaTransformer,
    AutoTiDE,
    AutoKAN,
)
from neuralforecast.losses.pytorch import MAE, DistributionLoss


# %%
# Define path to data
# Handle both notebook and script contexts
try:
    # When running as a script
    REPO_ROOT = Path(__file__).parent.parent.parent
except NameError:
    # When running as a notebook, resolve from where notebook is executed
    # Notebook is in src/forecasting/, so go up 2 levels to repo root
    REPO_ROOT = Path().resolve().parent.parent

data_path = REPO_ROOT / "_data/formatted/basis_tips_treas/ftsfr_tips_treasury_basis.parquet"

# Define output directory for plots
OUTPUT_DIR = REPO_ROOT / "_output"
PLOTS_DIR = OUTPUT_DIR / "forecasting" / "paper"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# Allow importing helper utilities defined alongside this script
try:
    scripts_path = Path(__file__).parent
except NameError:
    scripts_path = REPO_ROOT / "src" / "forecasting"

if str(scripts_path) not in sys.path:
    sys.path.append(str(scripts_path))

from forecast_neural_auto import (
    create_auto_config_deepar,
    create_auto_config_nbeats,
    create_auto_config_nhits,
    create_auto_config_simple,
    create_auto_config_transformer,
    create_auto_config_tide,
    create_auto_config_kan,
    detect_hardware,
)


# Helper function to save and show plots
def save_and_show_plot(filename):
    """Save current plot to OUTPUT_DIR and then show it."""
    plot_path = PLOTS_DIR / filename
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Saved plot to {plot_path}")
    plt.show()

# %%
# Load data and filter to 2-year maturity
df_raw = pl.read_parquet(data_path)
df_2yr = df_raw.filter(pl.col("unique_id") == "arb_2")

# Convert to pandas for StatsForecast
Y_df = df_2yr.to_pandas()

# Resample to monthly frequency (last business day of month)
Y_df['ds'] = pd.to_datetime(Y_df['ds'])
Y_df = Y_df.set_index('ds').resample('BME').last().reset_index()
Y_df['unique_id'] = 'arb_2'  # Restore unique_id column

# Handle missing values (forward fill then backward fill if needed)
Y_df['y'] = Y_df['y'].ffill().bfill()

print(f"Loaded {len(Y_df)} observations of 2-year TIPS-Treasury basis spread (monthly)")
print(f"Date range: {Y_df['ds'].min()} to {Y_df['ds'].max()}")
Y_df.head()

# %%
"""
## Data Exploration

Before modeling, let's examine the data characteristics:
- Time series plot to see trends and volatility
- Basic statistics
- Check for missing values
"""

# %%
# Basic statistics
print("Summary Statistics:")
print(Y_df['y'].describe())
print(f"\nMissing values: {Y_df['y'].isna().sum()}")

# %%
"""
## Visualize the Full Time Series

Plot the complete 2-year TIPS-Treasury basis spread to understand its behavior.
"""

# %%
from statsforecast import StatsForecast

# %%
StatsForecast.plot(Y_df)

# %%
"""
## Train/Test Split

For financial data, we'll use the most recent portion for testing.
We'll forecast the last 12 months.
"""

# %%
test_size = 12  # 12 months
train_df = Y_df.iloc[:-test_size].copy()
test_df = Y_df.iloc[-test_size:].copy()

print(f"Training set: {len(train_df)} observations")
print(f"Test set: {len(test_df)} observations")
print(f"Test period: {test_df['ds'].min()} to {test_df['ds'].max()}")

# %%
"""
## Define Models for Comparison

We align this walkthrough with the model registry defined in
`models_config.toml`, focusing on the statistically oriented models plus the
auto-tuned neural networks:

**Statistical baselines:**
1. **HistoricAverage** – simple long-run mean.
2. **AutoARIMA** – seasonal ARIMA with automatic order selection.
3. **Simple Exponential Smoothing (SES)** – non-seasonal exponential smoothing.
4. **Theta** – decomposes the series with an annual seasonality component.

**Auto-tuned neural networks (Optuna search):**
5. **Auto DeepAR**
6. **Auto N-BEATS**
7. **Auto N-HiTS**
8. **Auto DLinear**
9. **Auto NLinear**
10. **Auto Vanilla Transformer**
11. **Auto TiDE**
12. **Auto KAN**

All neural models reuse the Auto configurations from
`forecast_neural_auto.py`, trading compute time for stronger accuracy. Every
model uses a 12-month seasonality, matching the annual structure in
Treasury basis spreads (auction cycles, year-end flows, and inflation seasonality).
"""

# %%
from statsforecast.models import (
    HistoricAverage,
    SeasonalNaive,
    AutoARIMA,
    SimpleExponentialSmoothing,
    Theta,
)

# %%
# Set seasonality to annual (12 months per year)
# TIPS-Treasury basis spreads often exhibit annual patterns due to:
# - Tax effects and year-end flows
# - Treasury issuance cycles
# - Seasonal inflation patterns
season_length = 12
forecast_horizon = test_size

# Statistical models from the registry with informative aliases
stats_models = [
    HistoricAverage(alias="HistAvg"),
    AutoARIMA(
        season_length=season_length,
        max_p=5,
        max_q=5,
        max_P=2,
        max_Q=2,
        seasonal=True,
        stepwise=True,
        approximation=False,
        max_order=10,
        alias="ARIMA",
    ),
    # SimpleExponentialSmoothing(alpha=0.1, alias="SES"),  # Commented out for debugging
    Theta(season_length=season_length, alias="Theta"),
]

stats_model_aliases = [model.alias for model in stats_models]

# Detect available hardware once to reuse the auto model tuning utilities
hardware_config = detect_hardware()

# Store lightning logs for the neural auto models under the repository output directory
auto_logs_dir = (REPO_ROOT / "_output/forecasting/logs/example_forecasts").resolve()

# Number of Optuna trials per auto model (higher -> better performance, more compute)
auto_num_samples = 12

def build_auto_neural_models(horizon: int, log_root: Path) -> list:
    """Construct the auto neural models with consistent configuration."""

    log_root = Path(log_root)
    log_root.mkdir(parents=True, exist_ok=True)

    return [
        AutoDeepAR(
            h=horizon,
            config=create_auto_config_deepar(
                season_length,
                lightning_logs_dir=str((log_root / "auto_deepar").resolve()),
                debug=False,
                hardware_config=hardware_config,
            ),
            loss=DistributionLoss(distribution="Normal"),
            backend="optuna",
            num_samples=auto_num_samples,
            alias="DeepAR",
        ),
        # AutoNBEATS(  # Commented out for debugging
        #     h=horizon,
        #     config=create_auto_config_nbeats(
        #         season_length,
        #         horizon,
        #         lightning_logs_dir=str((log_root / "auto_nbeats").resolve()),
        #         debug=False,
        #         hardware_config=hardware_config,
        #     ),
        #     loss=MAE(),
        #     backend="optuna",
        #     num_samples=auto_num_samples,
        #     alias="NBEATS",
        # ),
        # AutoNHITS(  # Commented out for debugging
        #     h=horizon,
        #     config=create_auto_config_nhits(
        #         season_length,
        #         lightning_logs_dir=str((log_root / "auto_nhits").resolve()),
        #         debug=False,
        #         hardware_config=hardware_config,
        #     ),
        #     loss=MAE(),
        #     backend="optuna",
        #     num_samples=auto_num_samples,
        #     alias="NHITS",
        # ),
        AutoDLinear(
            h=horizon,
            config=create_auto_config_simple(
                season_length,
                lightning_logs_dir=str((log_root / "auto_dlinear").resolve()),
                debug=False,
                hardware_config=hardware_config,
            ),
            loss=MAE(),
            backend="optuna",
            num_samples=auto_num_samples,
            alias="DLinear",
        ),
        # AutoNLinear(  # Commented out for debugging
        #     h=horizon,
        #     config=create_auto_config_simple(
        #         season_length,
        #         lightning_logs_dir=str((log_root / "auto_nlinear").resolve()),
        #         debug=False,
        #         hardware_config=hardware_config,
        #     ),
        #     loss=MAE(),
        #     backend="optuna",
        #     num_samples=auto_num_samples,
        #     alias="NLinear",
        # ),
        AutoVanillaTransformer(
            h=horizon,
            config=create_auto_config_transformer(
                season_length,
                lightning_logs_dir=str((log_root / "auto_vanilla_transformer").resolve()),
                debug=False,
                hardware_config=hardware_config,
            ),
            loss=MAE(),
            backend="optuna",
            num_samples=auto_num_samples,
            alias="Transformer",
        ),
        AutoTiDE(
            h=horizon,
            config=create_auto_config_tide(
                season_length,
                lightning_logs_dir=str((log_root / "auto_tide").resolve()),
                debug=False,
                hardware_config=hardware_config,
            ),
            loss=MAE(),
            backend="optuna",
            num_samples=auto_num_samples,
            alias="TiDE",
        ),
        # AutoKAN(  # Commented out for debugging
        #     h=horizon,
        #     config=create_auto_config_kan(
        #         season_length,
        #         lightning_logs_dir=str((log_root / "auto_kan").resolve()),
        #         debug=False,
        #         hardware_config=hardware_config,
        #     ),
        #     loss=MAE(),
        #     backend="optuna",
        #     num_samples=auto_num_samples,
        #     alias="KAN",
        # ),
    ]


neural_models = build_auto_neural_models(forecast_horizon, auto_logs_dir)

neural_model_aliases = [repr(model) for model in neural_models]

model_names = stats_model_aliases + neural_model_aliases
print(f"Models to evaluate: {', '.join(model_names)}")

# %%
"""
## Initialize StatsForecast

Create the StatsForecast object with:
- Our selected models
- Business month end frequency (BME)
- Parallel processing for speed
- SeasonalNaive as fallback if any model fails
"""

# %%
sf = StatsForecast(
    models=stats_models,
    freq="BME",  # Business month end frequency
    fallback_model=SeasonalNaive(season_length=1),  # Simple fallback (non-seasonal)
    n_jobs=-1,  # Use all available cores
)
sf

# %%
"""
## Generate Point Forecasts

Use the full training data to generate forecasts for the test period.
We'll include 90% prediction intervals to assess uncertainty.
"""

# %%
stats_forecasts_df = sf.forecast(df=train_df, h=test_size, level=[90])
stats_forecasts_df.head()

# %%
"""
## Fit Auto Neural Models

Run the Optuna-powered auto neural networks using the same training window.
The helper configs from `forecast_neural_auto.py` provide tuned search spaces
and hardware-aware Lightning settings.
"""

# %%
nf = NeuralForecast(models=neural_models, freq="BME")
nf.fit(df=train_df)

neural_forecasts_df = nf.predict()
neural_forecasts_df.head()

# %%
"""
## Combine Forecasts Across All Models

Merge the statistical and neural forecasts so downstream evaluation considers
the full model roster.
"""

# %%
combined_forecasts_df = pd.merge(
    stats_forecasts_df,
    neural_forecasts_df,
    on=["unique_id", "ds"],
    how="outer",
)
combined_forecasts_df = combined_forecasts_df.sort_values(["unique_id", "ds"]).reset_index(drop=True)
combined_forecasts_df.head()

# %%
"""
## Visualize Forecasts vs Actuals

Plot the forecasts from all models against the actual test data.
This helps us see:
- Which models track the actual movements
- Which models produce realistic prediction intervals
- Which models may be too aggressive or too conservative
"""

# %%
# Combine train and test for plotting
sf.plot(Y_df, stats_forecasts_df, max_insample_length=200)

# %%
"""
### Focus on Specific Models

Let's compare a few specific models in detail to understand their behavior.
"""

# %%
sf.plot(
    Y_df,
    stats_forecasts_df,
    models=["HistAvg", "ARIMA", "Theta"],
    level=[90],
    max_insample_length=200,
)

# # %%  # Commented out - SES model not active
# sf.plot(
#     Y_df,
#     stats_forecasts_df,
#     models=["HistAvg", "SES", "ARIMA"],
#     level=[90],
#     max_insample_length=200,
# )

# %%
"""
### Visualize Auto Neural Forecasts

Plot the auto neural predictions alongside the actual test observations.
"""

# %%
# Filter to only point estimate columns (exclude prediction intervals and quantiles)
def is_point_estimate(col):
    """Check if column is a point estimate (not a quantile or prediction interval)."""
    col_lower = col.lower()
    exclude_patterns = ["-lo-", "-hi-", "-median", "-quantile", "quantile-"]
    return not any(pattern in col_lower for pattern in exclude_patterns)

# Get all point estimate columns from both stats and neural forecasts
# Exclude HistAvg from plotting
all_model_cols = [
    col for col in combined_forecasts_df.columns
    if col not in ["unique_id", "ds", "HistAvg"] and is_point_estimate(col)
]

# Calculate how many months back to show (at least 60 months = 5 years)
lookback_months = 60
lookback_idx = max(0, len(Y_df) - lookback_months - test_size)
historical_df = Y_df.iloc[lookback_idx:]

fig, ax = plt.subplots(figsize=(14, 6))

# Plot historical data (train + test)
ax.plot(historical_df["ds"], historical_df["y"], label="Actual", linewidth=2, color="black", zorder=10)

# Plot all model forecasts
for col in all_model_cols:
    ax.plot(combined_forecasts_df["ds"], combined_forecasts_df[col], label=col, linewidth=1.5, alpha=0.8)

# Add vertical line at train/test split
ax.axvline(x=test_df["ds"].iloc[0], color="gray", linestyle="--", alpha=0.5, label="Forecast Start")

ax.set_title("All Model Forecasts vs Actuals (Last 5+ Years)")
ax.set_xlabel("Date")
ax.set_ylabel("Basis Spread")
ax.legend(ncol=2, fontsize="small", loc="best")
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_and_show_plot("example_forecasts_all_models.png")

# %%
"""
## Cross-Validation for Robust Evaluation (COMMENTED OUT FOR DEBUGGING)

This section is commented out to speed up debugging.
Uncomment when you want to run full cross-validation analysis.
"""

# # %%
# """
# Instead of a single train/test split, we'll use cross-validation with multiple
# windows to get a more robust assessment of model performance.
#
# We'll use:
# - Forecast horizon: 12 months (matching the held-out forecast horizon)
# - Step size: 12 months (non-overlapping windows)
# - Up to 5 windows (limited by data length)
# """
#
# # %%
# cv_horizon = forecast_horizon
# max_windows = max(1, (len(Y_df) // cv_horizon) - 1)
# cv_windows = min(5, max_windows)
#
# stats_cv_df = sf.cross_validation(
#     df=Y_df,
#     h=cv_horizon,
#     step_size=cv_horizon,
#     n_windows=cv_windows,
# )
# stats_cv_df.head()
#
# # %%
# """
# ### Neural Cross-Validation
#
# Refit the auto neural models within the cross-validation windows to evaluate
# their stability across different training periods.
# """
#
# # %%
# neural_cv_models = build_auto_neural_models(cv_horizon, auto_logs_dir / "cv")
# nf_cv = NeuralForecast(models=neural_cv_models, freq="BME")
#
# neural_cv_df = nf_cv.cross_validation(
#     df=Y_df,
#     n_windows=cv_windows,
#     step_size=cv_horizon,
# )
# neural_cv_df.head()
#
# # %%
# """
# ### Combine Cross-Validation Results
# """
#
# # %%
# neural_cv_df_no_target = neural_cv_df.drop(columns=[col for col in ["y"] if col in neural_cv_df.columns])
# cv_df = pd.merge(
#     stats_cv_df,
#     neural_cv_df_no_target,
#     on=["unique_id", "ds", "cutoff"],
#     how="inner",
# )
# cv_df.head()
#
# # %%
# """
# ## Evaluate Model Performance
#
# Calculate error metrics for each model across all cross-validation windows:
# - MASE (Mean Absolute Scaled Error): Scale-independent metric
# - MSE (Mean Squared Error): Penalizes large errors
# - RMSE (Root Mean Squared Error): In same units as original data
# """
#
# # %%
# import numpy as np
#
# # %%
# def select_point_forecast_columns(df):
#     """Return the forecast columns excluding prediction interval outputs."""
#
#     exclude_cols = {"unique_id", "ds", "y", "cutoff"}
#     point_cols = []
#
#     for col in df.columns:
#         if col in exclude_cols:
#             continue
#
#         col_lower = col.lower()
#         if any(token in col_lower for token in ["-lo-", "-hi-"]):
#             continue
#         if col_lower.endswith("-median"):
#             continue
#
#         point_cols.append(col)
#
#     return point_cols
#
# # %%
# # Calculate MASE (needs training data for scaling)
# # For MASE, we need to create a naive forecast baseline
# # Use the training data to compute seasonal naive errors for scaling
# mase_scores = {}
# mse_scores = {}
# rmse_scores = {}
#
# model_cols = select_point_forecast_columns(cv_df)
#
# for model_col in model_cols:
#     # Calculate MSE
#     model_mse = ((cv_df["y"] - cv_df[model_col]) ** 2).mean()
#     mse_scores[model_col] = model_mse
#     rmse_scores[model_col] = np.sqrt(model_mse)
#
#     # Calculate MASE (using seasonal naive as baseline)
#     # MASE = MAE / MAE_baseline where baseline is seasonal naive
#     mae = np.abs(cv_df["y"] - cv_df[model_col]).mean()
#
#     # Seasonal naive baseline (compare with value from season_length periods ago)
#     # For the training set
#     train_y = train_df["y"].values
#     if len(train_y) > season_length:
#         naive_errors = np.abs(train_y[season_length:] - train_y[:-season_length])
#     else:
#         naive_errors = np.abs(np.diff(train_y))
#     mae_baseline = naive_errors.mean()
#
#     mase_scores[model_col] = mae / mae_baseline if mae_baseline > 0 else np.inf
#
# # %%
# """
# ## Model Performance Summary
#
# Compare all models across the three metrics.
# Lower values are better for all metrics.
#
# Interpretation:
# - MASE < 1: Better than seasonal naive baseline
# - MASE = 1: Same as seasonal naive
# - MASE > 1: Worse than seasonal naive
# """
#
# # %%
# import pandas as pd
#
# # %%
# # Create comparison table
# comparison_df = pd.DataFrame({
#     "Model": model_cols,
#     "MASE": [mase_scores[m] for m in model_cols],
#     "MSE": [mse_scores[m] for m in model_cols],
#     "RMSE": [rmse_scores[m] for m in model_cols],
# })
#
# # Sort by MASE (lower is better)
# comparison_df = comparison_df.sort_values("MASE")
# comparison_df
#
# # %%
# """
# ## Visualize Model Rankings
#
# Create a visual comparison of model performance across metrics.
# """
#
# # %%
# fig, axes = plt.subplots(1, 3, figsize=(15, 5))
#
# # MASE
# axes[0].barh(comparison_df["Model"], comparison_df["MASE"])
# axes[0].set_xlabel("MASE")
# axes[0].set_title("Mean Absolute Scaled Error\n(Lower is Better)")
# axes[0].axvline(x=1.0, color='r', linestyle='--', label='Naive Baseline')
# axes[0].legend()
#
# # MSE
# axes[1].barh(comparison_df["Model"], comparison_df["MSE"])
# axes[1].set_xlabel("MSE")
# axes[1].set_title("Mean Squared Error\n(Lower is Better)")
#
# # RMSE
# axes[2].barh(comparison_df["Model"], comparison_df["RMSE"])
# axes[2].set_xlabel("RMSE")
# axes[2].set_title("Root Mean Squared Error\n(Lower is Better)")
#
# plt.tight_layout()
# save_and_show_plot("example_forecasts_model_rankings.png")
#
# # %%
# """
# ## Identify Best Model
#
# Select the model with the lowest MASE score and visualize its performance.
# """
#
# # %%
# best_model = comparison_df.iloc[0]["Model"]
# print(f"Best performing model: {best_model}")
# print(f"MASE: {comparison_df.iloc[0]['MASE']:.4f}")
# print(f"RMSE: {comparison_df.iloc[0]['RMSE']:.4f}")
#
# # %%
# # Visualize best model's forecast with actuals
# best_forecast = combined_forecasts_df[combined_forecasts_df["unique_id"] == "arb_2"]
#
# fig, ax = plt.subplots(figsize=(12, 5))
# ax.plot(train_df["ds"], train_df["y"], label="Train", color="tab:blue", alpha=0.6)
# ax.plot(test_df["ds"], test_df["y"], label="Actual (Test)", color="black", linewidth=2)
# ax.plot(
#     best_forecast["ds"],
#     best_forecast[best_model],
#     label=f"Forecast ({best_model})",
#     linewidth=2,
# )
#
# lower_col = f"{best_model}-lo-90"
# upper_col = f"{best_model}-hi-90"
# if lower_col in best_forecast.columns and upper_col in best_forecast.columns:
#     ax.fill_between(
#         best_forecast["ds"],
#         best_forecast[lower_col],
#         best_forecast[upper_col],
#         alpha=0.2,
#         color="tab:orange",
#         label="90% interval",
#     )
#
# ax.set_title(f"Best Model ({best_model}) Forecast vs Actual")
# ax.set_xlabel("Date")
# ax.set_ylabel("Basis Spread")
# ax.legend(loc="upper left")
# plt.tight_layout()
# save_and_show_plot("example_forecasts_best_model.png")

# %%
"""
## Insights and Conclusions

### Key Findings:

1. **Best Model**: The model with the lowest MASE performs best at forecasting
   the 2-year TIPS-Treasury basis spread.

2. **Model Comparison**:
   - The auto neural family (N-BEATS, NHITS, TiDE, Transformer) explores rich function spaces
     and can outperform statistical baselines when structural breaks are limited.
   - AutoARIMA and Theta remain strong interpretable baselines that often compete closely
     thanks to annual differencing and mean-reverting behavior.
   - SES provides a lightweight control, highlighting how much the more expressive models gain.

3. **Why This Matters**:
   - TIPS-Treasury basis spreads represent arbitrage opportunities
   - Understanding which models work helps identify when spreads deviate from expected patterns
   - Poor model performance might indicate structural breaks or regime changes

### Next Steps:

- Experiment with different forecast horizons
- Try models with exogenous variables (volatility, liquidity measures)
- Compare performance across different maturities (2yr, 5yr, 10yr, 20yr)
- Investigate periods where all models perform poorly (potential regime changes)
"""

# %%
"""
## Appendix: Individual Model Analysis

For deeper investigation, we can look at each model's forecasts individually
to understand their specific behavior patterns.
"""

# %%
# # Show forecast statistics for each model
# for model in model_cols[:3]:  # Show first 3 models as example
#     print(f"\n{model} Forecast Statistics:")
#     print(f"Mean: {combined_forecasts_df[model].mean():.4f}")
#     print(f"Std: {combined_forecasts_df[model].std():.4f}")
#     print(f"Min: {combined_forecasts_df[model].min():.4f}")
#     print(f"Max: {combined_forecasts_df[model].max():.4f}")
