"""
PatchTST using GluonTS.

Performs both local and global forecasting using PatchTST. Reports both mean and
median MASE for local forecasts and a single global MASE. Adapted from Monash.
"""

from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore")
import os
# This option is important if running on an mps(e.g. MacBook M-series) device to
# enable CPU fallback for PyTorch
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
from gluonts.torch import PatchTSTEstimator

import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.gluonts_main_class import GluontsMain

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars
    forecast_horizon = 1
    patchtst_obj = GluontsMain(PatchTSTEstimator(
                                patch_len = seasonality,
                                context_length = seasonality * 4,
                                prediction_length = 1,
                                stride = 4,
                            ),
                            "patchtst",
                            0.2,
                            frequency,
                            seasonality,
                            dataset_path,
                            OUTPUT_DIR)
    patchtst_obj.main_workflow()