"""
N-BEATS using darts

Performs both local and global forecasting using a N-BEATS. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import NBEATSModel
import sys
sys.path.append('../')
from model_classes.darts_global_class import DartsGlobal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars
    nbeats_obj = DartsGlobal(NBEATSModel(
                                input_chunk_length=seasonality * 4,
                                output_chunk_length=1,
                            ),
                           "nbeats",
                           0.2,
                           frequency,
                           seasonality,
                           dataset_path,
                           OUTPUT_DIR,
                           scaling = True,
                           interpolation=True,
                           f32 = True)
    
    nbeats_obj.main_workflow()