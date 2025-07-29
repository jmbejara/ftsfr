"""
AutoCES using darts

Performs local forecasting using AutoCES. Reports both mean and
median MASE for local forecasts.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import AutoCES
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    auto_ces_obj = DartsLocal(AutoCES(season_length = env_vars[2]),
                                "auto_ces", 
                                *env_vars)
    auto_ces_obj.main_workflow()