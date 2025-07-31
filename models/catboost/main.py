"""
Catboost using darts

Performs both local and global forecasting using Catboost. Reports both mean and
median MASE for local forecasts and a single global MASE.

NOTE: training this model, especially on data which is considered large either
due to the number of series, the number of values in a single series, or both
requires large amounts of computation power.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
import subprocess
import logging
# Darts-based imports
from darts.models import CatBoostModel
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_global_class import DartsGlobal

logger = logging.getLogger("main")

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)
    
    data_path = env_vars[3]

    dataset_name = str(os.path.basename(data_path)).split(".")[0]
    dataset_name = dataset_name.removeprefix("ftsfr_")

    # Sets up logging for this model - dataset pair
    log_path = Path().resolve().parent / "model_logs" / "catboost"
    Path(log_path).mkdir(parents = True, exist_ok = True)
    log_path = log_path / (dataset_name + ".log")
    logging.basicConfig(filename = log_path,
                        filemode = "w", # Overwrites previously existing logs
                        format = "%(asctime)s - catboost - %(name)-12s"+\
                        " - %(levelname)s - %(message)s",
                        level = logging.DEBUG)

    logger.info("Running main. Environment variables read.")

    # Check for an NVIDIA GPU
    try:
        subprocess.check_output("nvidia-smi")
        task_type = "GPU"
    except Exception:
        task_type = "CPU"
    
    logger.info("Device: " + task_type + ".")

    catboost_obj = DartsGlobal(CatBoostModel(
                                lags=env_vars[2] * 4,
                                output_chunk_length=1,
                                # Training a single global model for global forecasting
                                multi_models=False,
                                task_type=task_type,
                            ),
                           "catboost",
                           *env_vars,
                           scaling = False,
                           interpolation=True)
    
    catboost_obj.main_workflow()