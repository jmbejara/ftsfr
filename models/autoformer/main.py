"""
Autoformer using Nixtla's neuralforecast

Performs both local and global forecasting using a Autoformer. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""

import sys
sys.path.append('../')
from model_classes.nixtla_main_class import NixtlaMain
from neuralforecast.models import Autoformer
import os
from pathlib import Path

if __name__ == "__main__":
    
    dataset_path = Path(os.environ["DATASET_PATH"])
    frequency = os.environ["FREQUENCY"]
    seasonality = int(os.environ["SEASONALITY"])
    if os.environ.get("OUTPUT_DIR", None) is not None:
        OUTPUT_DIR = Path(os.environ["OUTPUT_DIR"])
    else:
        OUTPUT_DIR = Path().resolve().parent.parent / "_output"
    autoformer = NixtlaMain(estimator=Autoformer,
                            model_name="autoformer",
                            test_split=0.2,
                            frequency=frequency,
                            seasonality=seasonality,
                            data_path=dataset_path,
                            output_path=OUTPUT_DIR)
    autoformer.main_workflow()