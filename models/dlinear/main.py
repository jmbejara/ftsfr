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
    
    env_vars = env_reader(os.environ)
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars
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