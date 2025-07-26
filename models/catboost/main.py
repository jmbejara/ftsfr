"""
Catboost using darts

Performs both local and global forecasting using Catboost. Reports both mean and
median MASE for local forecasts and a single global MASE.

NOTE: training this model, especially on data which is considered large either
due to the number of series, the number of values in a single series, or both
requires large amounts of computation power.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
import subprocess
# Darts-based imports
from darts.models import CatBoostModel
import sys
sys.path.append('../')
from model_classes.darts_global_class import DartsGlobal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars
    # Check for an NVIDIA GPU
    try:
        subprocess.check_output("nvidia-smi")
        task_type = "GPU"
    except Exception:
        task_type = "CPU"

    catboost_obj = DartsGlobal(CatBoostModel(
                                lags=seasonality * 4,
                                output_chunk_length=1,
                                # Training a single global model for global forecasting
                                multi_models=False,
                                task_type=task_type,
                            ),
                           "catboost",
                           0.2,
                           frequency,
                           seasonality,
                           dataset_path,
                           OUTPUT_DIR,
                           scaling = False,
                           interpolation=True)
    
    catboost_obj.main_workflow()