"""
TiDE using darts

Performs both local and global forecasting using a TiDE. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") # This should be here to suppress warnings on import
import os
# Darts-based imports
from darts.models import TiDEModel
import sys
sys.path.append('../')
from model_classes.darts_global_class import DartsGlobal

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

    tide_obj = DartsGlobal(TiDEModel(
                                input_chunk_length=seasonality * 4,
                                output_chunk_length=1,
                            ),
                           "tide",
                           0.2,
                           frequency,
                           seasonality,
                           dataset_path,
                           OUTPUT_DIR,
                           scaling = True,
                           interpolation=True,
                           f32 = True)
    
    tide_obj.main_workflow()