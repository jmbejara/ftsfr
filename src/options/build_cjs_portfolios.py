"""
Reusable CJS (Constantinides, Jackwerth, Savov 2013) 54-portfolio
construction, factored out of `portfolios.ipynb` so it can be applied to
options data filtered at different cleaning levels.

The construction follows CJS:
1. Bucket each option into a (cp_flag, moneyness_id, maturity_id) cell.
2. Within each cell, compute a bivariate Gaussian kernel weight per date over
   moneyness and days-to-maturity.
3. Drop options with weight < 1% per (date, cell).
4. Compute option_elasticity using Black-Scholes delta.
5. Aggregate to leverage-adjusted daily portfolio returns; the call portfolio
   adds (1 - inv_weight) * rf, the put portfolio adds (1 + inv_weight) * rf
   and flips the option contribution sign.
6. Compound daily portfolio returns to monthly.

The function accepts a filtered options DataFrame (after some cleaning level
has been applied) and returns a long-format DataFrame of CJS portfolio
returns suitable for downstream FTSFR conversion.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm


MONEYNESS_TARGETS = [0.900, 0.925, 0.950, 0.975, 1.000, 1.025, 1.050, 1.075, 1.100]
MATURITY_TARGETS = [30, 60, 90]
CP_FLAGS = ["C", "P"]

KERNEL_BW_MONEYNESS = 0.0125
KERNEL_BW_TTM_DAYS = 10.0
MIN_KERNEL_WEIGHT = 0.01


def _ensure_required_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add mid_price / days_to_maturity / moneyness if missing.

    L1-filtered data has the raw OptionMetrics columns and `moneyness` (from
    `level_1_filters.calc_moneyness`) but does not have `mid_price` or
    `days_to_maturity` consistently populated. This shim adds them so the
    same construction code works for L1 and L3 inputs.
    """
    df = df.copy()
    # Some intermediate parquets save with a non-unique MultiIndex (e.g.,
    # L3 is indexed by [date, exdate, moneyness]). Flatten before doing
    # column-wise groupby assigns.
    if df.index.nlevels > 1 or df.index.name is not None or not df.index.is_unique:
        df = df.reset_index(drop=False)
        # Drop any duplicate columns that may have been promoted from the
        # index but already exist as data columns.
        df = df.loc[:, ~df.columns.duplicated(keep="last")]
    if "mid_price" not in df.columns:
        df["mid_price"] = (df["best_bid"] + df["best_offer"]) / 2.0
    if "days_to_maturity" not in df.columns:
        df["days_to_maturity"] = df["exdate"] - df["date"]
    if pd.api.types.is_timedelta64_dtype(df["days_to_maturity"]):
        df["ttm_days"] = df["days_to_maturity"].dt.days.astype(float)
    else:
        df["ttm_days"] = df["days_to_maturity"].astype(float)
    if "moneyness" not in df.columns:
        df["moneyness"] = df["strike_price"] / df["close"]
    return df


def _assign_cells(df: pd.DataFrame) -> pd.DataFrame:
    """Assign each option to its (cp_flag, moneyness_id, maturity_id) cell
    by closest target. Options far from any target are dropped via the
    kernel-weight floor downstream.
    """
    df = df.copy()
    money = df["moneyness"].to_numpy()
    money_targets = np.array(MONEYNESS_TARGETS)
    money_dist = np.abs(money[:, None] - money_targets[None, :])
    df["moneyness_id"] = money_targets[money_dist.argmin(axis=1)]

    ttm = df["ttm_days"].to_numpy()
    ttm_targets = np.array(MATURITY_TARGETS, dtype=float)
    ttm_dist = np.abs(ttm[:, None] - ttm_targets[None, :])
    df["maturity_id"] = ttm_targets[ttm_dist.argmin(axis=1)].astype(int)

    df["ftsfa_id"] = (
        df["cp_flag"].astype(str)
        + "_"
        + (df["moneyness_id"] * 1000).round().astype(int).astype(str)
        + "_"
        + df["maturity_id"].astype(int).astype(str)
    )
    return df


def _kernel_weights_group(group: pd.DataFrame) -> pd.Series:
    """Bivariate Gaussian kernel weight for one (date, ftsfa_id) cell."""
    target_money = group["moneyness_id"].iloc[0]
    target_ttm = group["maturity_id"].iloc[0]
    dx = (group["moneyness"].to_numpy() - target_money) / KERNEL_BW_MONEYNESS
    dy = (group["ttm_days"].to_numpy() - target_ttm) / KERNEL_BW_TTM_DAYS
    w = np.exp(-0.5 * (dx * dx + dy * dy))
    s = w.sum()
    if s == 0:
        return pd.Series(np.zeros(len(group)), index=group.index)
    return pd.Series(w / s, index=group.index)


def _attach_kernel_weights(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["kernel_weight"] = (
        df.groupby(["date", "ftsfa_id"], group_keys=False).apply(_kernel_weights_group)
    )
    return df


def _bsm_elasticity(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    T = df["ttm_days"].to_numpy() / 365.0
    S = df["close"].to_numpy()
    K = df["strike_price"].to_numpy()
    r = (df["tb_m3"].to_numpy() / 100.0) if "tb_m3" in df.columns else np.zeros(len(df))
    sigma = df["IV"].to_numpy()
    safe = (sigma > 0) & (T > 0) & (S > 0) & (K > 0)
    d1 = np.full(len(df), np.nan)
    d1[safe] = (
        np.log(S[safe] / K[safe]) + (r[safe] + 0.5 * sigma[safe] ** 2) * T[safe]
    ) / (sigma[safe] * np.sqrt(T[safe]))
    delta = np.where(df["cp_flag"].to_numpy() == "C", norm.cdf(d1), norm.cdf(d1) - 1.0)
    # Use mid_price as denominator; avoid divide-by-zero
    mid = df["mid_price"].to_numpy()
    mid_safe = np.where(np.abs(mid) > 1e-8, mid, np.nan)
    df["option_elasticity"] = delta * S / mid_safe
    return df


def _daily_portfolio_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Compute leverage-adjusted daily portfolio returns per (date, ftsfa_id).

    The portfolio is *formed* at t-1 and *held* to t, exactly as in CJS:

    - The single-option return is measured over one *contract* held from t-1 to
      t -- NOT across the heterogeneous strikes/expiries that merely share a
      portfolio cell on a given day. Contract identity is
      (secid, cp_flag, strike_price, exdate); secid is constant in this SPX
      panel but is included for safety.
    - The kernel weight, BSM elasticity and risk-free rate are all taken at the
      FORMATION date t-1 (lagged by contract), so the realized t-1->t move
      cannot leak into its own weighting (no look-ahead).
    - The 1% kernel-weight floor and the renormalization-to-1 are applied to
      those formation weights, so each day's basket is a proper weighted
      average of the contracts actually held.
    """
    contract_keys = [
        c
        for c in ["secid", "cp_flag", "strike_price", "exdate"]
        if c in df.columns
    ]
    df = df.sort_values(contract_keys + ["date"]).copy()
    g = df.groupby(contract_keys)
    df["mid_price_lag"] = g["mid_price"].shift(1)
    # Formation-date (t-1) basket inputs, lagged within each contract.
    df["w_form"] = g["kernel_weight"].shift(1)
    df["elast_form"] = g["option_elasticity"].shift(1)
    if "tb_m3" in df.columns:
        df["daily_rf"] = g["tb_m3"].shift(1) / 100.0 / 252.0
    else:
        df["daily_rf"] = 0.0

    df["option_return"] = (df["mid_price"] - df["mid_price_lag"]) / df["mid_price_lag"]
    # Keep only rows with a complete formation basket and a realized return
    # (drops each contract's first observation, which has no t-1 to form from).
    df = df[
        df["option_return"].notna()
        & df["w_form"].notna()
        & df["elast_form"].notna()
    ].copy()

    # CJS basket selection is as of formation: drop tiny formation weights, then
    # renormalize the survivors so the kernel weights sum to 1 within (date,cell).
    df = df[df["w_form"] >= MIN_KERNEL_WEIGHT].copy()
    df["w_form"] = df["w_form"] / df.groupby(["date", "ftsfa_id"])[
        "w_form"
    ].transform("sum")

    # weight = kernel_weight / elasticity ; return_contrib = weight * option_return
    df["inv_weight"] = df["w_form"] / df["elast_form"]
    df["inv_return"] = df["inv_weight"] * df["option_return"]

    grouped = df.groupby(["date", "ftsfa_id"])
    port = grouped.agg(
        total_inv_weight=("inv_weight", "sum"),
        total_inv_return=("inv_return", "sum"),
        daily_rf=("daily_rf", "first"),
        cp_flag=("cp_flag", "first"),
    ).reset_index()

    call_mask = port["cp_flag"] == "C"
    put_mask = port["cp_flag"] == "P"
    port["portfolio_return"] = np.nan
    port.loc[call_mask, "portfolio_return"] = (
        port.loc[call_mask, "total_inv_return"]
        + (1.0 - port.loc[call_mask, "total_inv_weight"]) * port.loc[call_mask, "daily_rf"]
    )
    port.loc[put_mask, "portfolio_return"] = (
        -port.loc[put_mask, "total_inv_return"]
        + (1.0 + port.loc[put_mask, "total_inv_weight"]) * port.loc[put_mask, "daily_rf"]
    )
    return port


def _compound_monthly(port_daily: pd.DataFrame, label_prefix: str) -> pd.DataFrame:
    daily = port_daily.pivot_table(
        index="date", columns="ftsfa_id", values="portfolio_return"
    )
    monthly = daily.resample("ME").apply(lambda x: (1 + x).prod() - 1)
    monthly = monthly.reset_index().melt(
        id_vars="date", var_name="ftsfa_id", value_name="y"
    )
    monthly["unique_id"] = label_prefix + "_" + monthly["ftsfa_id"].astype(str)
    monthly = monthly.rename(columns={"date": "ds"})
    monthly = monthly[["unique_id", "ds", "y"]].dropna().reset_index(drop=True)
    return monthly


def build_cjs_portfolios(
    filtered_df: pd.DataFrame, label_prefix: str = "cjs"
) -> pd.DataFrame:
    """End-to-end CJS portfolio construction from a filtered options panel.

    Returns a long-format DataFrame with columns [unique_id, ds, y] for the
    54 (= 2 cp_flags x 9 moneyness x 3 maturity) CJS portfolios.
    """
    df = _ensure_required_columns(filtered_df)
    df = df[df["IV"].notna() & (df["IV"] > 0)]
    df = df[df["mid_price"].notna() & (df["mid_price"] > 0)]
    df = df[df["ttm_days"].between(7, 180)]
    df = _assign_cells(df)
    df = _attach_kernel_weights(df)
    df = _bsm_elasticity(df)
    df = df[df["option_elasticity"].notna()]
    # NOTE: the 1% kernel-weight floor is intentionally NOT applied here. It is
    # applied inside _daily_portfolio_returns on the *formation-date* (lagged)
    # weights, together with renormalization, so basket selection and weighting
    # are both as of t-1 (no look-ahead).
    port_daily = _daily_portfolio_returns(df)
    panel = _compound_monthly(port_daily, label_prefix=label_prefix)
    return panel
