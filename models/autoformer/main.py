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
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars
    autoformer = NixtlaMain(estimator=Autoformer,
                            model_name="autoformer",
                            test_split=0.2,
                            frequency=frequency,
                            seasonality=seasonality,
                            data_path=dataset_path,
                            output_path=OUTPUT_DIR)
    autoformer.inference_workflow()