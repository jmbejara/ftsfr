"""
AutoTBATS using darts

Performs local forecasting using AutoTBATS. Reports both mean and
median MASE for local forecasts.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import AutoTBATS
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    auto_tbats_obj = DartsLocal(AutoTBATS(season_length = env_vars[2]),
                                "auto_tbats", 
                                *env_vars)

    auto_tbats_obj.main_workflow()