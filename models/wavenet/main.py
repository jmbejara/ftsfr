"""
WaveNet using GluonTS.

Performs both local and global forecasting using WaveNet. Reports both mean and
median MASE for local forecasts and a single global MASE. Adapted from Monash.
"""

from pathlib import Path
from warnings import filterwarnings

filterwarnings("ignore")

import os
# This option is important if running on an mps(e.g. MacBook) device to enable
# CPU fallback for PyTorch
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
from gluonts.torch import WaveNetEstimator

import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.gluonts_main_class import GluontsMain

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    wavenet_obj = GluontsMain(WaveNetEstimator(freq = frequency, prediction_length=1),
                            "wavenet",
                            *env_vars)
    
    wavenet_obj.main_workflow()