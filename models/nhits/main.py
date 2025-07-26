"""
NHiTS using darts

Performs both local and global forecasting using a Transformer. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import NHiTSModel
import sys
sys.path.append('../')
from model_classes.darts_global_class import DartsGlobal

if __name__ == "__main__":
    
    dataset_path = Path(os.environ["DATASET_PATH"])
    frequency = os.environ["FREQUENCY"]
    seasonality = int(os.environ["SEASONALITY"])
    if os.environ.get("OUTPUT_DIR", None) is not None:
        OUTPUT_DIR = Path(os.environ["OUTPUT_DIR"])
    else:
        OUTPUT_DIR = Path().resolve().parent.parent / "_output"
    nhits_obj = DartsGlobal(NHiTSModel(
                                input_chunk_length=seasonality * 4,
                                output_chunk_length=1,
                            ),
                           "nhits",
                           0.2,
                           frequency,
                           seasonality,
                           dataset_path,
                           OUTPUT_DIR,
                           scaling = True,
                           interpolation=True,
                           f32 = True)
    
    nhits_obj.main_workflow()