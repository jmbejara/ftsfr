"""
Pooled Regression(PR) using darts and scikit-learn. It is a generic gaussian
linear model.

Performs both local and global forecasting using PR. Reports both mean and
median MASE for local forecasts.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import SKLearnModel
from sklearn.linear_model import TweedieRegressor
import sys
sys.path.append('../')
from model_classes.darts_local_class import DartsLocal

if __name__ == "__main__":
    
    dataset_path = Path(os.environ["DATASET_PATH"])
    frequency = os.environ["FREQUENCY"]
    seasonality = int(os.environ["SEASONALITY"])
    if os.environ.get("OUTPUT_DIR", None) is not None:
        OUTPUT_DIR = Path(os.environ["OUTPUT_DIR"])
    else:
        OUTPUT_DIR = Path().resolve().parent.parent / "_output"
    pr_obj = DartsLocal(SKLearnModel(model = TweedieRegressor(power=0),
                                        lags = seasonality * 4,
                                        output_chunk_length = 1,
                                        multi_models = False),
                                "pr", 
                                0.2, 
                                frequency, 
                                seasonality, 
                                dataset_path, 
                                OUTPUT_DIR)

    pr_obj.main_workflow()