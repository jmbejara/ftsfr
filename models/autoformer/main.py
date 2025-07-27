"""
Autoformer using Nixtla's neuralforecast

Performs both local and global forecasting using a Autoformer. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""

import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.nixtla_main_class import NixtlaMain
from neuralforecast.models import Autoformer
import os
from pathlib import Path

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    autoformer = NixtlaMain(Autoformer,
                            "autoformer",
                            *env_vars)
    
    autoformer.main_workflow()