"""
AutoMFLES using darts

Performs local forecasting using AutoMFLES. Reports both mean and
median MASE for local forecasts.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import AutoMFLES
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    auto_mfles_obj = DartsLocal(AutoMFLES(test_size = 1, season_length = env_vars[2]),
                                "auto_mfles", 
                                *env_vars)
    auto_mfles_obj.main_workflow()