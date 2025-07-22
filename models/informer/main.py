"""
Informer using Nixtla's neuralforecast

Performs both local and global forecasting using a Informer. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""

import sys
sys.path.append('../')
from model_classes.nixtla_main_class import NixtlaMain
from neuralforecast.models import Informer
import os
from pathlib import Path

if __name__ == "__main__":

   # Read environment variables
    dataset_path = Path(os.environ["DATASET_PATH"])
    frequency = os.environ["FREQUENCY"]
    OUTPUT_DIR = Path(
        os.environ.get("OUTPUT_DIR",
                       Path(__file__).parent.parent.parent / "_output")
    )
    seasonality = int(os.environ["SEASONALITY"])

    informer = NixtlaMain(estimator=Informer,
                            model_name="informer",
                            test_split=0.2,
                            frequency=frequency,
                            seasonality=seasonality,
                            data_path=dataset_path,
                            output_path=OUTPUT_DIR)
    informer.main_workflow()