from typing import Union, List
import datetime


class TimeSeriesModel:
    def __init__(
        self,
        y: str,
        X: Union[List[str], str],
        training_window: List[datetime.date],
        forecasting_window: List[datetime.date],
        n_steps_forecasting: int,
        intersect_forecasting: bool = False,
    ):
        self.y = y
        self.X = X
        self.training_window = training_window
        self.forecasting_window = forecasting_window
        self.n_steps_forecasting = n_steps_forecasting
        self.intersect_forecasting = intersect_forecasting
