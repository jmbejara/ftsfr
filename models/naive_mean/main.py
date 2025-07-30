"""
NaiveMean using darts

Performs local forecasting using NaiveMean. Reports both mean and
median MASE for local forecasts.
"""

from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import NaiveMean
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)

    naive_mean_obj = DartsLocal(NaiveMean(),
                            "naive_mean",
                            *env_vars)
    naive_mean_obj.main_workflow()