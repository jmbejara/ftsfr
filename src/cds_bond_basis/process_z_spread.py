"""
Z-spread processing for the CDS-bond basis pipeline.

For each (date, bond), solve for the constant continuous-compounded spread z
that reprices observed bond cash flows off the fitted NSS Treasury curve:

    Price_obs = sum_i CF_i * DF_tsy(t_i; theta) * exp(-z * t_i)

This is the "FR_{i,t,tau}" object in Siriwardane, Sunderam, Wallen (2021).
The CDS-bond basis is then par_spread - z_spread.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd
from scipy.optimize import brentq

from finm.fixedincome import discount, spot

import gsw2006_yield_curve as yc
from settings import config

DATA_DIR = Path(config("DATA_DIR"))
# Use the "_all" variant which preserves NSS parameters (BETA0..3, TAU1, TAU2)
# needed to back out a Fed-fitted Treasury curve when the CRSP NSS fit is
# pathological (e.g., produces 25% spot rates on certain dates).
FED_CURVE_PATH = DATA_DIR / "fed_yield_curve" / "fed_yield_curve_all.parquet"


def _to_timestamp(x):
    return pd.Timestamp(x)


def _ensure_positive_time(times):
    times = np.asarray(times, dtype=float)
    return times[times > 0]


def normalize_day_count_basis(day_count_basis):
    """Normalize day-count strings; default to 30/360."""
    if day_count_basis is None or pd.isna(day_count_basis):
        return "30/360"
    dcb = str(day_count_basis).strip().upper()
    if dcb in {"", "NAN", "NONE"}:
        return "30/360"
    if "ACT" in dcb and "360" in dcb:
        return "ACT/360"
    if "ACT" in dcb and "ACT" in dcb:
        return "ACT/ACT"
    if "30" in dcb and "360" in dcb:
        return "30/360"
    return "30/360"


def year_fraction(start_date, end_date, day_count_basis="30/360"):
    """Year fraction under 30/360, ACT/ACT, or ACT/360 conventions."""
    start = _to_timestamp(start_date)
    end = _to_timestamp(end_date)
    if end <= start:
        return 0.0

    dcb = normalize_day_count_basis(day_count_basis)
    if dcb == "ACT/360":
        return (end - start).days / 360.0
    if dcb == "ACT/ACT":
        return (end - start).days / 365.25

    y1, m1, d1 = start.year, start.month, min(start.day, 30)
    y2, m2, d2 = end.year, end.month, end.day
    if d2 == 31 and d1 == 30:
        d2 = 30
    return (360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)) / 360.0


def _build_coupon_schedule_from_next_coupon(
    quote_date, maturity_date, next_coupon_date, coupon_frequency=2
):
    """Build forward coupon dates from next coupon to maturity."""
    if next_coupon_date is None or pd.isna(next_coupon_date):
        return None

    quote_date = _to_timestamp(quote_date)
    maturity_date = _to_timestamp(maturity_date)
    next_coupon_date = _to_timestamp(next_coupon_date)

    if next_coupon_date <= quote_date:
        return None
    if next_coupon_date > maturity_date:
        return None

    months = int(round(12 / coupon_frequency))
    dates = []
    d = next_coupon_date
    while d < maturity_date:
        if d > quote_date:
            dates.append(d)
        d = d + pd.DateOffset(months=months)
    dates.append(maturity_date)
    return pd.DatetimeIndex(sorted(set(dates)))


def build_bond_cashflows(
    quote_date,
    maturity_date,
    coupon_rate,
    day_count_basis="30/360",
    next_coupon_date=None,
    principal=100.0,
    coupon_frequency=2,
    coupon_is_percent=True,
):
    """Build coupon + principal cash flows for a fixed-rate bond."""
    quote_date = _to_timestamp(quote_date)
    maturity_date = _to_timestamp(maturity_date)
    if maturity_date <= quote_date:
        return np.array([], dtype=float), np.array([], dtype=float)

    cpn = float(coupon_rate)
    if coupon_is_percent:
        cpn = cpn / 100.0

    coupon_dates = None
    if next_coupon_date is not None and not pd.isna(next_coupon_date):
        coupon_dates = _build_coupon_schedule_from_next_coupon(
            quote_date=quote_date,
            maturity_date=maturity_date,
            next_coupon_date=next_coupon_date,
            coupon_frequency=coupon_frequency,
        )

    if coupon_dates is None or len(coupon_dates) == 0:
        times = np.array(
            [year_fraction(quote_date, maturity_date, day_count_basis=day_count_basis)],
            dtype=float,
        )
        cfs = np.array([principal], dtype=float)
        return times, cfs

    payment_dates = pd.DatetimeIndex(coupon_dates).sort_values()
    times = np.array(
        [
            year_fraction(quote_date, d, day_count_basis=day_count_basis)
            for d in payment_dates
        ],
        dtype=float,
    )
    times = _ensure_positive_time(times)
    if len(times) == 0:
        return np.array([], dtype=float), np.array([], dtype=float)

    cpn_cf = principal * cpn / coupon_frequency
    cfs = np.full(shape=len(times), fill_value=cpn_cf, dtype=float)
    cfs[-1] += principal
    return times, cfs


def price_from_curve_and_zspread(times, cash_flows, nss_params, z_spread):
    """Price from NSS curve + constant z-spread (continuous compounding)."""
    if len(times) == 0:
        return np.nan

    base_df = discount(times, params=np.asarray(nss_params, dtype=float))
    spread_df = np.exp(-float(z_spread) * np.asarray(times, dtype=float))
    return float(
        np.dot(np.asarray(cash_flows, dtype=float), base_df * spread_df)
    )


def calculate_z_spread(
    quote_date,
    maturity_date,
    coupon_rate,
    observed_price,
    nss_params,
    day_count_basis="30/360",
    next_coupon_date=None,
    principal=100.0,
    coupon_frequency=2,
    coupon_is_percent=True,
    price_is_clean=False,
    accrued_interest=None,
    z_lower=-0.20,
    z_upper=0.20,
):
    """Solve for z-spread that matches the observed bond price."""
    obs_price = float(observed_price)
    nss_params = np.asarray(nss_params, dtype=float)
    ai_used = np.nan
    if price_is_clean:
        if accrued_interest is None or pd.isna(accrued_interest):
            ai_used = 0.0
            clean_price_status = "clean_price_ai_assumed_zero"
        else:
            ai_used = float(accrued_interest)
            clean_price_status = "clean_price_ai_input"
        obs_price = obs_price + ai_used
    else:
        clean_price_status = "dirty_price_input"

    times, cash_flows = build_bond_cashflows(
        quote_date=quote_date,
        maturity_date=maturity_date,
        coupon_rate=coupon_rate,
        day_count_basis=day_count_basis,
        next_coupon_date=next_coupon_date,
        principal=principal,
        coupon_frequency=coupon_frequency,
        coupon_is_percent=coupon_is_percent,
    )
    if len(times) == 0:
        return {
            "z_spread": np.nan,
            "z_spread_bps": np.nan,
            "model_price": np.nan,
            "status": "failed: no_cashflows",
            "accrued_interest_used": ai_used,
            "price_input_status": clean_price_status,
        }

    def objective(z):
        model_price = price_from_curve_and_zspread(
            times, cash_flows, nss_params, z
        )
        return model_price - obs_price

    f_lo = objective(z_lower)
    f_hi = objective(z_upper)

    if np.isnan(f_lo) or np.isnan(f_hi):
        return {
            "z_spread": np.nan,
            "z_spread_bps": np.nan,
            "model_price": np.nan,
            "status": "failed: invalid_objective",
            "accrued_interest_used": ai_used,
            "price_input_status": clean_price_status,
        }

    if f_lo * f_hi > 0:
        return {
            "z_spread": np.nan,
            "z_spread_bps": np.nan,
            "model_price": np.nan,
            "status": "failed: root_not_bracketed",
            "accrued_interest_used": ai_used,
            "price_input_status": clean_price_status,
        }

    z_star = brentq(objective, z_lower, z_upper, maxiter=200, xtol=1e-10)
    model_price = price_from_curve_and_zspread(
        times, cash_flows, nss_params, z_star
    )

    return {
        "z_spread": float(z_star),
        "z_spread_bps": float(z_star * 1e4),
        "model_price": float(model_price),
        "status": "ok",
        "accrued_interest_used": ai_used,
        "price_input_status": clean_price_status,
    }


def get_nss_params_for_date(
    quote_date,
    df_treasury: pd.DataFrame | None = None,
    fed_curve_df: pd.DataFrame | None = None,
    fed_fallback_tolerance_pct_pts: float = 0.5,
):
    """
    Return NSS parameters for the requested date.

    Resolves the target date to the latest prior CRSP quote date in the same
    month if no exact match exists. If a Fed GSW table with NSS columns is
    available and the CRSP-based fit looks pathological, fall back to the Fed
    parameters for that date.
    """
    PARAMS0 = np.array([1.0, 10.0, 3.0, 3.0, 3.0, 3.0], dtype=float)

    qd = _to_timestamp(quote_date)

    if df_treasury is None:
        df_treasury = yc.load_crsp_treasury_for_fitting()

    caldt = pd.to_datetime(df_treasury["caldt"])
    available_dates = pd.DatetimeIndex(
        caldt.dropna().drop_duplicates().sort_values()
    )
    resolved_date, date_match = yc._resolve_quote_date(qd, available_dates)
    if pd.isna(resolved_date):
        raise ValueError(
            f"No Treasury quote date available for target date {qd.date()} "
            f"(date_match={date_match})."
        )

    params_star, _ = yc.fit_curve_for_quote_date(
        pd.Timestamp(resolved_date), df_treasury, params0=PARAMS0
    )
    params_crsp = np.asarray(params_star, dtype=float)

    if fed_curve_df is None:
        if FED_CURVE_PATH.exists():
            fed_curve_df = pd.read_parquet(FED_CURVE_PATH)
        else:
            fed_curve_df = None

    if fed_curve_df is None:
        return params_crsp

    fed_df = fed_curve_df.copy()
    fed_df.index = pd.to_datetime(fed_df.index)
    fed_dates = pd.DatetimeIndex(
        fed_df.index.dropna().drop_duplicates().sort_values()
    )
    fed_date_used, _ = yc._resolve_quote_date(qd, fed_dates)
    if pd.isna(fed_date_used):
        return params_crsp

    fed_row = fed_df.loc[pd.Timestamp(fed_date_used)]
    required_fed_cols = {
        "SVENY01",
        "SVENY05",
        "SVENY10",
        "BETA0",
        "BETA1",
        "BETA2",
        "BETA3",
        "TAU1",
        "TAU2",
    }
    if not required_fed_cols.issubset(set(fed_row.index)):
        return params_crsp

    crsp_spots_pct = np.array(
        [
            float(spot([1.0], params_crsp)[0] * 100),
            float(spot([5.0], params_crsp)[0] * 100),
            float(spot([10.0], params_crsp)[0] * 100),
        ],
        dtype=float,
    )
    fed_spots_pct = np.array(
        [
            float(fed_row["SVENY01"]),
            float(fed_row["SVENY05"]),
            float(fed_row["SVENY10"]),
        ],
        dtype=float,
    )
    abs_diff = np.abs(crsp_spots_pct - fed_spots_pct)
    if np.any(abs_diff > float(fed_fallback_tolerance_pct_pts)):
        params_fed = np.array(
            [
                float(fed_row["TAU1"]),
                float(fed_row["TAU2"]),
                float(fed_row["BETA0"]) / 100.0,
                float(fed_row["BETA1"]) / 100.0,
                float(fed_row["BETA2"]) / 100.0,
                float(fed_row["BETA3"]) / 100.0,
            ],
            dtype=float,
        )
        return params_fed

    return params_crsp
