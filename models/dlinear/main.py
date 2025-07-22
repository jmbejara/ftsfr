"""
D-Linear using darts

Performs both local and global forecasting using a D-Linear. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import DLinearModel
import sys
sys.path.append('../')
from model_classes.darts_global_class import DartsGlobal

if __name__ == "__main__":

    # Environment variables
    dataset_path = Path(os.environ["DATASET_PATH"])
    frequency = os.environ["FREQUENCY"]
    seasonality = int(os.environ["SEASONALITY"])
    if os.environ.get("OUTPUT_DIR", None) is not None:
        OUTPUT_DIR = Path(os.environ["OUTPUT_DIR"])
    else:
        OUTPUT_DIR = Path().resolve().parent.parent / "_output"

    dataset_name = str(os.path.basename(dataset_path)).split(".")[0].removeprefix("ftsfr_")

    dlinear_obj = DartsGlobal(DLinearModel(
                                input_chunk_length=seasonality * 4,
                                output_chunk_length=1,
                            ),
                           "dlinear",
                           0.2,
                           frequency,
                           seasonality,
                           dataset_path,
                           OUTPUT_DIR,
                           scaling = True,
                           interpolation=True,
                           f32 = True)
    
    dlinear_obj.main_workflow()