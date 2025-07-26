"""
Theta using darts.

Performs local forecasting using Theta. Reports both mean and
median MASE for local forecasts.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import Theta
from darts.utils.utils import SeasonalityMode
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars
    theta_obj = DartsLocal(Theta(season_mode = SeasonalityMode.ADDITIVE),
                            "theta", 
                            0.2, 
                            frequency, 
                            seasonality, 
                            dataset_path, 
                            OUTPUT_DIR)

    theta_obj.main_workflow()