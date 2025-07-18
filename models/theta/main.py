"""
Theta using darts.

Performs local forecasting using Theta. Reports both mean and
median MASE for local forecasts.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") # This should be here to suppress warnings on import
import os
# Darts-based imports
from darts.models import Theta
from darts.utils.utils import SeasonalityMode
import sys
sys.path.append('../')
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":

    # Read env variables
    dataset_path = Path(os.environ["FTSFR_DATASET_PATH"])
    frequency = os.environ["FTSFR_FREQUENCY"]
    seasonality = int(os.environ["SEASONALITY"])
    if os.environ.get("OUTPUT_DIR", None) is not None:
        OUTPUT_DIR = Path(os.environ["OUTPUT_DIR"])
    else:
        OUTPUT_DIR = Path().resolve().parent.parent / "_output"

    dataset_name = str(os.path.basename(dataset_path)).split(".")[0].removeprefix("ftsfr_")

    theta_obj = DartsLocal(Theta(season_mode = SeasonalityMode.ADDITIVE),
                            "theta", 
                            0.2, 
                            frequency, 
                            seasonality, 
                            dataset_path, 
                            OUTPUT_DIR)
    
    theta_obj.main_workflow()