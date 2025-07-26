"""
FFNN using GluonTS.

Performs both local and global forecasting using FFNN. Reports both mean and
median MASE for local forecasts and a single global MASE. Adapted from Monash.
"""

from pathlib import Path
from warnings import filterwarnings

filterwarnings("ignore")

import os
# This option is important if running on an mps(e.g. MacBook) device to enable
# CPU fallback for PyTorch
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
from gluonts.torch.model.simple_feedforward import SimpleFeedForwardEstimator
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.gluonts_main_class import GluontsMain

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars
    ffnn_obj = GluontsMain(SimpleFeedForwardEstimator(
        context_length = seasonality * 4, prediction_length=1
    ),
                           "ffnn",
                           0.2,
                           frequency,
                           seasonality,
                           dataset_path,
                           OUTPUT_DIR)
    
    ffnn_obj.main_workflow()