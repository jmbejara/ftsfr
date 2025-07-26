"""
ARIMA using darts

Performs local forecasting using ARIMA. Reports both mean and
median MASE for local forecasts.
"""

from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import ARIMA
import sys
sys.path.append('../')
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars

    arima_obj = DartsLocal(ARIMA(p = 1, d = 1, q = 1),
                            "arima",
                            0.2,
                            frequency,
                            seasonality,
                            dataset_path,
                            OUTPUT_DIR)
    arima_obj.main_workflow()