"""
Simple Exponential Smoothing(SES) using darts.

Performs local forecasting using SES. Reports both mean and
median MASE for local forecasts.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore")
import os
# Darts-based imports
from darts.models import ExponentialSmoothing
from darts.utils.utils import ModelMode, SeasonalityMode
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)

    ses_obj = DartsLocal(ExponentialSmoothing(trend=ModelMode.NONE,
                                              seasonal=SeasonalityMode.NONE),
                                "ses",
                                *env_vars)

    ses_obj.main_workflow()