"""
Autoregressive recurrent neural network based forecasting(DeepAR) using GluonTS.

Performs both local and global forecasting using DeepAR. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""

from pathlib import Path
from warnings import filterwarnings

filterwarnings("ignore")

import os
# This option is important if running on an mps(e.g. MacBook) device to enable
# CPU fallback for PyTorch
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
from gluonts.torch import DeepAREstimator
import sys
sys.path.append('../')
from model_classes.gluonts_main_class import GluontsMain

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars
    deepar_obj = GluontsMain(DeepAREstimator(
        freq=frequency, context_length = seasonality * 4, prediction_length = 1
    ),
                           "deepar",
                           0.2,
                           frequency,
                           seasonality,
                           dataset_path,
                           OUTPUT_DIR)
    
    deepar_obj.main_workflow()