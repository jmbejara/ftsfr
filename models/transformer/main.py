"""
Transformer using darts

Performs both local and global forecasting using a Transformer. Reports both mean and
median MASE for local forecasts and a single global MASE.
"""
from pathlib import Path
from warnings import filterwarnings
filterwarnings("ignore") 
import os
# Darts-based imports
from darts.models import TransformerModel
import sys
sys.path.append('../')
from env_reader import env_reader
from model_classes.darts_global_class import DartsGlobal

if __name__ == "__main__":
    
    env_vars = env_reader(os.environ)

    transformer_obj = DartsGlobal(TransformerModel(
                                input_chunk_length=seasonality * 4,
                                output_chunk_length=1,
                            ),
                            "transformer",
                            *env_vars,
                            scaling = True,
                            interpolation=True,
                            f32 = True)
    
    transformer_obj.inference_workflow()