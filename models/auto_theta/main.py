"""
AutoTheta using darts

Performs local forecasting using AutoTheta. Reports both mean and
median MASE for local forecasts.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import AutoTheta
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    auto_theta_obj = DartsLocal(AutoTheta(season_length = env_vars[2]),
                                "auto_theta", 
                                *env_vars)
    auto_theta_obj.main_workflow()