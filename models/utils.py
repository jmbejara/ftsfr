import numpy as np
import pandas as pd


def create_simulated_y(start="2020-01-01", freq="D", n_periods=1000, to_frame=False):
    if n_periods % 1 == 0:
        n_periods = int(n_periods)
    else:
        raise ValueError("n_periods must be an integer.")
    y = pd.Series(
        np.random.normal(0, 1, n_periods),
        index=pd.date_range(start=start, periods=n_periods, freq=freq),
    )
    return y.to_frame(name="y") if to_frame else y


def create_simulated_X(start="2020-01-01", freq="D", n_periods=1000, n_features=10):
    X = pd.DataFrame(
        np.random.normal(0, 1, (n_periods, n_features)),
        index=pd.date_range(start=start, periods=n_periods, freq=freq),
    )
    return X
