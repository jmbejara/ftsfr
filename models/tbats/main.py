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
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    dataset_path = Path(os.environ["DATASET_PATH"])
    frequency = os.environ["FREQUENCY"]
    seasonality = int(os.environ["SEASONALITY"])
    if os.environ.get("OUTPUT_DIR", None) is not None:
        OUTPUT_DIR = Path(os.environ["OUTPUT_DIR"])
    else:
        OUTPUT_DIR = Path().resolve().parent.parent / "_output"
    
    tbats_obj = DartsLocal(TBATS(season_length = seasonality),
                                "tbats", 
                                0.2, 
                                frequency, 
                                seasonality, 
                                dataset_path, 
                                OUTPUT_DIR)

    tbats_obj.main_workflow()