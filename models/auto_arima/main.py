"""
AutoARIMA using darts

Performs local forecasting using AutoARIMA. Reports both mean and
median MASE for local forecasts.
"""

from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import AutoARIMA
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)

    auto_arima_obj = DartsLocal(AutoARIMA(season_length = seasonality),
                                "auto_arima", 
                                *env_vars)

    auto_arima_obj.main_workflow()