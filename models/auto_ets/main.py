"""
AutoETS using darts

Performs local forecasting using AutoETS. Reports both mean and
median MASE for local forecasts.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import AutoETS
import sys
sys.path.append('../')
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars
    auto_ets_obj = DartsLocal(AutoETS(season_length = seasonality),
                                "auto_ets", 
                                0.2, 
                                frequency, 
                                seasonality, 
                                dataset_path, 
                                OUTPUT_DIR)

    auto_ets_obj.main_workflow()