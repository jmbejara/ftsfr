# %%
"""
# Illustrative Forecasts: What Different Methods *Look Like*

This walkthrough produces the two-panel illustration figure used in the paper's
Forecasting Methodology section. It is **not** part of the formal benchmark
evaluation (that lives in `dodo_02_forecasting.py` and is summarized in the
results tables); its only purpose is to give the reader a visual sense of how
qualitatively different the forecast *paths* of the different model families
are, on two contrasting kinds of financial data.

To avoid singling out any one entity, each panel shows a **cross-sectional
average**: we forecast every series in the panel individually and then average
the realized series and the per-method forecasts across all entities.

- **Panel (a): Treasury spot-futures ("cash-futures") basis.** Averaged across
  the five tenors (2Y, 5Y, 10Y, 20Y, 30Y). Monthly; trained through Dec 2018 and
  forecast over the twelve months of 2019.
- **Panel (b): bank holding company (BHC) cash liquidity.** Averaged across the
  BHCs that report continuously over the display window. Quarterly; trained
  through 2016 Q4 and forecast over the twelve quarters of 2017--2019.

Both panels use the same representative quartet, one model from each family in
our roster, so the panels are directly comparable:

- **ARIMA** and **Theta** -- the two classical statistical workhorses.
- **NLinear** -- the strongest *hybrid* linear method on basis spreads.
- **N-BEATS** -- the strongest *pure deep-learning* method on basis spreads.

(NLinear and N-BEATS are the basis-spread leaders in
`_output/forecasting/paper/model_summary_by_category.csv`; we hold the quartet
fixed across both panels for comparability.)

Two deliberate departures from the benchmark proper, both in service of the
illustration: (1) we forecast a 12-step path in one shot, whereas the benchmark
evaluates a rolling one-step-ahead horizon -- a multi-step path is what makes the
differences in shape visible; (2) the neural models are trained *globally* over
each panel's entities (the univariate-global design of the benchmark), and we
display the cross-entity average.
"""

# %%
import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Safe for headless / notebook-execution builds
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import polars as pl

from neuralforecast import NeuralForecast
from neuralforecast.auto import AutoNBEATS, AutoNLinear
from neuralforecast.losses.pytorch import MAE

from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, SeasonalNaive, Theta

# %%
# Resolve repo root whether run as a script or executed as a notebook.
try:
    REPO_ROOT = Path(__file__).parent.parent.parent
    SCRIPTS_DIR = Path(__file__).parent
except NameError:
    REPO_ROOT = Path().resolve().parent.parent
    SCRIPTS_DIR = REPO_ROOT / "src" / "forecasting"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.append(str(SCRIPTS_DIR))

from forecast_neural_auto import (  # noqa: E402
    create_auto_config_nbeats,
    create_auto_config_simple,
    detect_hardware,
)

PLOTS_DIR = REPO_ROOT / "_output" / "forecasting" / "paper"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)
PLOT_PATH = PLOTS_DIR / "example_forecasts_illustration.png"
CSV_PATH = PLOTS_DIR / "example_forecasts_illustration.csv"
LOGS_DIR = REPO_ROOT / "_output" / "forecasting" / "logs" / "example_forecasts_illustration"

# Optuna trials per neural model. 8 is enough to tune these small models for an
# illustration; override with a small value (e.g. 2) for a quick smoke test.
AUTO_NUM_SAMPLES = int(os.environ.get("FTSFR_EXAMPLE_NUM_SAMPLES", "8"))
# Optional cap on entities per panel for fast smoke tests (default: use all).
MAX_ENTITIES = os.environ.get("FTSFR_EXAMPLE_MAX_ENTITIES")
MAX_ENTITIES = int(MAX_ENTITIES) if MAX_ENTITIES else None

# (column, label, color) for each illustrated method. Family membership is
# explained in the figure caption/prose, so we keep the legend labels bare.
SERIES_STYLE = [
    ("ARIMA", "ARIMA", "tab:blue"),
    ("Theta", "Theta", "tab:green"),
    ("NLinear", "NLinear", "tab:orange"),
    ("N-BEATS", "N-BEATS", "tab:red"),
]

# Per-panel configuration.
PANELS = [
    {
        "key": "treasury_sf",
        "tag": "(a)",
        "data_path": REPO_ROOT
        / "_data/formatted/basis_treas_sf/ftsfr_treasury_sf_basis.parquet",
        "freq": "ME",
        "season": 12,
        "cutoff": pd.Timestamp("2018-12-31"),
        "horizon": 12,
        "plot_start": pd.Timestamp("2014-01-01"),
        "ylabel": "Basis (bps)",
    },
    {
        "key": "bhc_cash_liquidity",
        "tag": "(b)",
        "data_path": REPO_ROOT
        / "_data/formatted/nyu_call_report/ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet",
        "freq": "QE",
        "season": 4,
        "cutoff": pd.Timestamp("2016-12-31"),
        "horizon": 12,
        "plot_start": pd.Timestamp("2008-03-31"),
        "ylabel": "Cash liquidity (ratio)",
    },
]

# %%
"""
## Helpers

`load_panel` collapses each entity to period-end values (mirroring the
benchmark's month-/quarter-end normalization). `select_balanced` keeps the
entities that report continuously over the display window, so the
cross-sectional average has a stable composition. `run_panel` trains the
statistical and neural models on the training window and returns the
cross-entity average of the realized series and of each method's forecast.
"""

# %%
def load_panel(data_path: Path, freq: str) -> pd.DataFrame:
    raw = pl.read_parquet(data_path).to_pandas()
    raw["ds"] = pd.to_datetime(raw["ds"])
    pieces = []
    for uid, g in raw.groupby("unique_id"):
        s = g.set_index("ds")["y"].resample(freq).last().ffill().bfill()
        pieces.append(pd.DataFrame({"unique_id": uid, "ds": s.index, "y": s.values}))
    return pd.concat(pieces, ignore_index=True)


def horizon_dates(cutoff: pd.Timestamp, horizon: int, freq: str):
    grid = pd.date_range(cutoff, periods=horizon + 1, freq=freq)
    return list(grid[1:])  # the `horizon` period-ends strictly after the cutoff


def select_balanced(panel: pd.DataFrame, plot_start, forecast_end, freq):
    periods = pd.date_range(plot_start, forecast_end, freq=freq)
    piv = panel.pivot_table(index="unique_id", columns="ds", values="y")
    cols = [p for p in periods if p in piv.columns]
    keep = piv[cols].dropna(how="any").index.tolist()
    return keep


def run_panel(cfg: dict) -> dict:
    freq, season = cfg["freq"], cfg["season"]
    cutoff, horizon = cfg["cutoff"], cfg["horizon"]
    fdates = horizon_dates(cutoff, horizon, freq)
    forecast_end = fdates[-1]

    panel = load_panel(cfg["data_path"], freq)
    keep = select_balanced(panel, cfg["plot_start"], forecast_end, freq)
    if MAX_ENTITIES and len(keep) > MAX_ENTITIES:
        # Deterministic subsample for smoke tests.
        keep = sorted(keep)[:: max(1, len(keep) // MAX_ENTITIES)][:MAX_ENTITIES]
    print(
        f"[{cfg['key']}] entities used (balanced over "
        f"{cfg['plot_start'].date()}..{forecast_end.date()}): {len(keep)}"
    )

    panel = panel[panel["unique_id"].isin(keep)]
    train_df = panel[panel["ds"] <= cutoff].copy()

    # Statistical models (configured exactly as in forecast_stats.py).
    sf = StatsForecast(
        models=[
            AutoARIMA(season_length=season, alias="ARIMA"),
            Theta(season_length=season, alias="Theta"),
        ],
        freq=freq,
        fallback_model=SeasonalNaive(season_length=season),
        n_jobs=1,  # robust across script/notebook execution
    )
    stats_fc = sf.forecast(df=train_df, h=horizon)

    # Neural models trained globally across the panel's entities.
    log_root = (LOGS_DIR / cfg["key"]).resolve()
    log_root.mkdir(parents=True, exist_ok=True)
    hw = detect_hardware()
    nf = NeuralForecast(
        models=[
            AutoNLinear(
                h=horizon,
                config=create_auto_config_simple(
                    season,
                    lightning_logs_dir=str((log_root / "auto_nlinear").resolve()),
                    debug=False,
                    hardware_config=hw,
                ),
                loss=MAE(),
                backend="optuna",
                num_samples=AUTO_NUM_SAMPLES,
                alias="NLinear",
            ),
            AutoNBEATS(
                h=horizon,
                config=create_auto_config_nbeats(
                    season,
                    horizon,
                    lightning_logs_dir=str((log_root / "auto_nbeats").resolve()),
                    debug=False,
                    hardware_config=hw,
                ),
                loss=MAE(),
                backend="optuna",
                num_samples=AUTO_NUM_SAMPLES,
                alias="N-BEATS",
            ),
        ],
        freq=freq,
    )
    nf.fit(df=train_df, val_size=horizon)
    neural_fc = nf.predict()

    fc = pd.merge(stats_fc, neural_fc, on=["unique_id", "ds"], how="outer")

    # Cross-entity averages.
    method_cols = [c for c, _, _ in SERIES_STYLE if c in fc.columns]
    method_avg = fc.groupby("ds")[method_cols].mean().sort_index()

    disp = panel[(panel["ds"] >= cfg["plot_start"]) & (panel["ds"] <= forecast_end)]
    realized_avg = disp.groupby("ds")["y"].mean().sort_index()

    return {
        "cfg": cfg,
        "n_entities": len(keep),
        "realized_avg": realized_avg,
        "method_avg": method_avg,
        "cutoff": cutoff,
    }


# %%
"""
## Run both panels
"""

# %%
results = [run_panel(cfg) for cfg in PANELS]

# %%
"""
## Assemble the two-panel figure

The figure carries no titles -- the titles and notes live in the LaTeX caption.
We match the graphics style of the other basis-spread figures in the paper:
year ticks, a horizontal dashed grid, no top/right spines, and a single legend
centered below the panels. Forecast paths are anchored to the realized average
at the cutoff so the lines emanate from the realized series.
"""

# %%
def anchored(cutoff, realized_avg, ds_index, values):
    anchor_val = realized_avg.loc[cutoff]
    return [cutoff, *list(ds_index)], [anchor_val, *list(values)]


tidy_rows = []
fig, axes = plt.subplots(2, 1, figsize=(11, 9), dpi=300)

for ax, res in zip(axes, results):
    cfg = res["cfg"]
    realized_avg, method_avg, cutoff = res["realized_avg"], res["method_avg"], res["cutoff"]

    for ds, v in realized_avg.items():
        tidy_rows.append((cfg["key"], ds, "Realized", v))
    ax.plot(
        realized_avg.index, realized_avg.values,
        color="black", linewidth=2.3, label="Realized", zorder=10,
    )

    for col, label, color in SERIES_STYLE:
        if col not in method_avg.columns:
            continue
        xs, ys = anchored(cutoff, realized_avg, method_avg.index, method_avg[col].values)
        ax.plot(xs, ys, color=color, linewidth=1.9, alpha=0.95, label=label)
        for ds, v in zip(method_avg.index, method_avg[col].values):
            tidy_rows.append((cfg["key"], ds, label, v))

    ax.axvline(x=cutoff, color="gray", linestyle=":", linewidth=1.2, alpha=0.8)
    ax.annotate(
        "forecast start", xy=(cutoff, ax.get_ylim()[0]),
        xytext=(4, 8), textcoords="offset points",
        ha="left", va="bottom", fontsize=10, color="gray",
    )
    ax.text(
        0.008, 0.94, cfg["tag"], transform=ax.transAxes,
        fontsize=13, fontweight="bold", va="top", ha="left",
    )
    ax.set_ylabel(cfg["ylabel"], fontsize=13)
    ax.xaxis.set_major_locator(mdates.YearLocator(1 if cfg["freq"] == "ME" else 2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.xaxis.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

axes[-1].set_xlabel("Date", fontsize=13)

# Single shared legend below the panels.
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.01),
    ncol=5, fontsize=12, frameon=True,
)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(PLOT_PATH, dpi=300, bbox_inches="tight")
print(f"Saved illustration figure to {PLOT_PATH}")

pd.DataFrame(tidy_rows, columns=["panel", "ds", "series", "value"]).to_csv(
    CSV_PATH, index=False
)
print(f"Saved plotted data to {CSV_PATH}")
