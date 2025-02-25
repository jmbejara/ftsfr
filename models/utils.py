import numpy as np
import pandas as pd


def create_simulated_y(
    start="2020-01-01", freq="D", n_periods=1000, to_frame=False, std=1
):
    if n_periods % 1 == 0:
        n_periods = int(n_periods)
    else:
        raise ValueError("n_periods must be an integer.")
    y = pd.Series(
        np.random.normal(0, std, n_periods),
        index=pd.date_range(start=start, periods=n_periods, freq=freq),
        name="y",
    )
    return y.to_frame(name="y") if to_frame else y


def create_simulated_X(
    start="2020-01-01", freq="D", n_periods=1000, n_features=10, std=1
):
    X = pd.DataFrame(
        np.random.normal(0, std, (n_periods, n_features)),
        index=pd.date_range(start=start, periods=n_periods, freq=freq),
        columns=[f"x{i}" for i in range(n_features)],
    )
    return X


def _calc_periods_per_year(dates) -> str:
    """
    Given a list/array-like of dates, attempt to infer the frequency
    (daily, weekly, monthly, etc.) and return one of the keys in
    PERIODS_PER_YEAR_MAP:
        "D"  -> 252   (Daily)
        "W"  -> 52    (Weekly)
        "BM" -> 12    (Monthly, not necessarily month-end)
        "ME" -> 12    (Monthly, all month-end)
        "BQ" -> 4     (Quarterly)
        "BA" -> 2     (Semiannual, or even annual in practice)

    If fewer than 20 dates are provided, the function raises a ValueError
    forcing the user to specify the frequency manually.

    :param dates: A list/array-like of datetime objects (or date strings).
    :return: A string key from PERIODS_PER_YEAR_MAP indicating the inferred frequency.
    """

    if len(dates) < 20:
        raise ValueError(
            "Not enough data points to auto-detect 'periods_per_year'. "
            "At least 20 dates are required. Please specify manually."
        )

    dates = pd.to_datetime(dates)
    dates = np.sort(dates)

    day_diffs = np.diff(dates) / np.timedelta64(1, "D")  # length n-1
    median_gap = np.median(day_diffs)
    if median_gap < 2:
        max_gap = np.percentile(day_diffs, 90)
        frequency = "DU" if max_gap >= 2 else "D"
    elif median_gap < 10:
        frequency = "W"
    elif median_gap < 40:
        # Distinguish "month-end" vs. "business-monthly"
        is_month_end = all(d == (d + pd.tseries.offsets.MonthEnd(0)) for d in dates)
        frequency = "ME" if is_month_end else "BM"
    elif median_gap < 80:
        frequency = "BQ"
    elif median_gap < 200:
        frequency = "BA"
    else:
        frequency = "A"
    return frequency
