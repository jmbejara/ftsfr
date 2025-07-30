"""
NaiveDrift using darts

Performs local forecasting using NaiveDrift. Reports both mean and
median MASE for local forecasts.
"""

from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import NaiveDrift
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)

    naive_drift_obj = DartsLocal(NaiveDrift(),
                            "naive_drift",
                            *env_vars)
    naive_drift_obj.main_workflow()