"""
N-Linear using darts

Performs both local and global forecasting using a N-Linear. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import NLinearModel
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_global_class import DartsGlobal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars
    nlinear_obj = DartsGlobal(NLinearModel(
                                input_chunk_length=seasonality * 4,
                                output_chunk_length=1,
                            ),
                           "nlinear",
                           *env_vars,
                           scaling = True,
                           interpolation=True,
                           f32 = True)
    nlinear_obj.main_workflow()