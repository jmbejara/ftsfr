"""
NaiveMovingAverage using darts

Performs local forecasting using NaiveMovingAverage. Reports both mean and
median MASE for local forecasts.
"""

from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import NaiveMovingAverage
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)

    naive_movav_obj = \
    DartsLocal(NaiveMovingAverage(input_chunk_length = env_vars[2] * 4),
               "naive_movav",
               *env_vars)
    
    naive_movav_obj.main_workflow()