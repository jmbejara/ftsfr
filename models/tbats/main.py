"""
TBATS using darts.

Performs local forecasting using TBATS. Reports both mean and
median MASE for local forecasts.
"""

from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import TBATS
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars
    
    tbats_obj = DartsLocal(TBATS(season_length = env_vars[2]),
                                "tbats", 
                                *env_vars)

    tbats_obj.main_workflow()