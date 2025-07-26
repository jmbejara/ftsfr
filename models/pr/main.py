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
    
    env_vars = env_reader(os.environ)
    
    dataset_path, frequency, seasonality, output_dir, test_split = env_vars
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