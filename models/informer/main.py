"""
Informer using Nixtla's neuralforecast

Performs both local and global forecasting using a Informer. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""

import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.nixtla_main_class import NixtlaMain
from neuralforecast.models import Informer
import os
from pathlib import Path

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
        
    informer = NixtlaMain(Informer,
                            "informer",
                            *env_vars)
    
    informer.main_workflow()