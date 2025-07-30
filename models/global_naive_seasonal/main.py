"""
GlobalNaiveSeasonal using darts

Performs both local and global forecasting using a GlobalNaiveSeasonal. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import GlobalNaiveSeasonal
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_global_class import DartsGlobal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)

    # Raises a non-breaking error when trying to save model

    global_naive_seasonal_obj = DartsGlobal(GlobalNaiveSeasonal(
                                input_chunk_length=env_vars[2] * 4,
                                output_chunk_length=1,
                            ),
                            "global_naive_seasonal",
                            *env_vars,
                            scaling = True,
                            interpolation=True,
                            f32 = True)
    
    global_naive_seasonal_obj.main_workflow()