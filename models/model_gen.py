import os
import stat
from pathlib import Path

import logging
logger = logging.getLogger("model_gen")

def build_models(model_dir, import_string, main_template, pixi_template,
                 class_name):
    
    logger.info("build_models called. Building " + class_name + ".")
    for model_data in model_dir:

        # Setting up the directory
        curr_model = model_data["obj_name"]

        logger.info("Build process began for " + curr_model + ".")

        try:
            os.mkdir(curr_model)
            logger.info("Created directory for " + curr_model)
        except FileExistsError:
            pass
        except Exception as e:
            raise
        
        os.chmod(curr_model, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | \
                             stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | \
                             stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH)
        
        logger.info("Changed permissions for the directory.")
        
        # Setups imports
        imports = model_data['imports']
        import_str = import_string + imports[0]
        if len(imports) > 1:
            import_str += "\n".join(imports[1:])
        model_data['imports'] = import_str

        logger.info("Created import string.")

        # Creating files
        with open("./" + curr_model + "/main.py", "w") as main_f:
            main_f.write(main_template.format(**model_data))
        
        logger.info("Created main.py")
        
        with open("./" + curr_model + "/pixi.toml", "w") as pixi_f:
            pixi_f.write(pixi_template.format(**model_data))
        
        logger.info("Created pixi.toml")

        logger.info("Build process completed for " + curr_model + ".")

    return

if __name__ == "__main__":

    log_path = Path().resolve() / "model_logs"
    Path(log_path).mkdir(parents = True, exist_ok = True)
    log_path = log_path / "model_gen.log"
    logging.basicConfig(filename = log_path,
                        filemode = "w", # Overwrites previously existing logs
                        format = "%(asctime)s"+\
                        " - %(levelname)s - %(message)s",
                        level = logging.DEBUG)

    logger.info("Model generator script called.")

    # Import strings
    darts_import_string = "from darts.models import "
    nixtla_import_string = "from neuralforecast.models import "
    gluonts_import_string = "from gluonts.torch import "

    import_strings = [
        darts_import_string,
        darts_import_string,
        nixtla_import_string,
        gluonts_import_string
    ]
    
    # Model dictionaries
    local_models_darts = [
        
        # Models listed in alphabetical order as per model_name

        {"model_name" : "ARIMA",
        "obj_name" : "arima",
        "estimator_func" : "ARIMA(p = 1, d = 1, q = 1)",
        "imports" : ["ARIMA"]},

        {"model_name" : "AutoARIMA",
        "obj_name" : "auto_arima",
        "estimator_func" : "AutoARIMA(season_length = env_vars[2])",
        "imports" : ["AutoARIMA"]},

        {"model_name" : "AutoCES",
        "obj_name" : "auto_ces",
        "estimator_func" : "AutoCES(season_length = env_vars[2])",
        "imports" : ["AutoCES"]},

        {"model_name" : "AutoETS",
        "obj_name" : "auto_ets",
        "estimator_func" : "AutoETS(season_length = env_vars[2])",
        "imports" : ["AutoETS"]},

        {"model_name" : "AutoMFLES",
        "obj_name" : "auto_mfles",
        "estimator_func" : "AutoMFLES(test_size = 1,"+\
        " season_length = env_vars[2])",
        "imports" : ["AutoMFLES"]},

        {"model_name" : "AutoTBATS",
        "obj_name" : "auto_tbats",
        "estimator_func" : "AutoTBATS(season_length = env_vars[2])",
        "imports" : ["AutoTBATS"]},

        {"model_name" : "AutoTheta",
        "obj_name" : "auto_theta",
        "estimator_func" : "AutoTheta(season_length = env_vars[2])",
        "imports" : ["AutoTheta"]},

        {"model_name" : "Exponential Smoothing",
        "obj_name" : "ets",
        "estimator_func" : "ExponentialSmoothing(trend = ModelMode.ADDITIVE, "+\
        "seasonal = SeasonalityMode.NONE)",
        "imports" : ["ExponentialSmoothing",
        "from darts.utils.utils import ModelMode, SeasonalityMode"]},

        {"model_name" : "NaiveDrift",
        "obj_name" : "naive_drift",
        "estimator_func" : "NaiveDrift()",
        "imports" : ["NaiveDrift"]},

        {"model_name" : "NaiveMean",
        "obj_name" : "naive_mean",
        "estimator_func" : "NaiveMean()",
        "imports" : ["NaiveMean"]},

        {"model_name" : "NaiveMovingAverage",
        "obj_name" : "naive_movav",
        "estimator_func" : "NaiveMovingAverage("+\
        "input_chunk_length = env_vars[2] * 4)",
        "imports" : ["NaiveMovingAverage"]},

        {"model_name" : "NaiveSeasonal",
        "obj_name" : "naive_seasonal",
        "estimator_func" : "NaiveSeasonal(K = env_vars[2])",
        "imports" : ["NaiveSeasonal"]},

        {"model_name" : "Pooled Regression",
        "obj_name" : "pr",
        "estimator_func" : "SKLearnModel(model = TweedieRegressor(power=0),"+\
                                        "lags = env_vars[2] * 4,"+\
                                        "output_chunk_length = 1,"+\
                                        "multi_models = False)",
        "imports" : ["SKLearnModel",
                     "from sklearn.linear_model import TweedieRegressor"]},
        
        {"model_name" : "Prophet",
        "obj_name" : "prophet",
        "estimator_func" : "Prophet()",
        "imports" : ["Prophet"]},

        {"model_name" : "Simple Exponential Smoothing",
        "obj_name" : "ses",
        "estimator_func" : "ExponentialSmoothing(trend = ModelMode.NONE, "+\
        "seasonal = SeasonalityMode.NONE)",
        "imports" : ["ExponentialSmoothing",
        "from darts.utils.utils import ModelMode, SeasonalityMode"]},

        {"model_name" : "TBATS",
        "obj_name" : "tbats",
        "estimator_func" : "TBATS(season_length = env_vars[2])",
        "imports" : ["TBATS"]},

        {"model_name" : "Theta",
        "obj_name" : "theta",
        "estimator_func" : "Theta(season_mode = SeasonalityMode.ADDITIVE)",
        "imports" : ["Theta",
                     "from darts.utils.utils import SeasonalityMode"]},

    ]
    global_models_darts = [
        
        # Catboost not supported yet because it needs a custom install in pixi

        # {"model_name" : "CatBoost",
        # "obj_name" : "catboost",
        # "estimator_func" : "CatBoostModel(
        #                         "lags=env_vars[2] * 4,"
        #                         "output_chunk_length=1,"
        #                         "multi_models=False,"
        #                         "task_type = \\",
        #                         "'GPU' if is_available() else 'CPU',"
        #                     ")",
        # "imports" : ["CatBoostModel",
        #              "from torch.cuda import is_available"]},

        {"model_name" : "DLinear",
        "obj_name" : "dlinear",
        "estimator_func" : "DLinearModel("+\
                                "input_chunk_length = env_vars[2] * 4,"+\
                                "output_chunk_length=1,"+\
                            ")",
        "imports" : ["DLinearModel"]},

        {"model_name" : "Global Naive Aggregate",
        "obj_name" : "global_naive_agg",
        "estimator_func" : "GlobalNaiveAggregate("+\
                                "input_chunk_length = env_vars[2] * 4,"+\
                                "output_chunk_length=1,"+\
                            ")",
        "imports" : ["GlobalNaiveAggregate"]},

        {"model_name" : "Global Naive Drift",
        "obj_name" : "global_naive_dri",
        "estimator_func" : "GlobalNaiveDrift("+\
                                "input_chunk_length = env_vars[2] * 4,"+\
                                "output_chunk_length=1,"+\
                            ")",
        "imports" : ["GlobalNaiveDrift"]},

        {"model_name" : "Global Naive Seasonal",
        "obj_name" : "global_naive_sea",
        "estimator_func" : "GlobalNaiveSeasonal("+\
                                "input_chunk_length = env_vars[2] * 4,"+\
                                "output_chunk_length=1,"+\
                            ")",
        "imports" : ["GlobalNaiveSeasonal"]},

        {"model_name" : "N-BEATS",
        "obj_name" : "nbeats",
        "estimator_func" : "NBEATSModel("+\
                                "input_chunk_length = env_vars[2] * 4,"+\
                                "output_chunk_length=1,"+\
                            ")",
        "imports" : ["NBEATSModel"]},

        {"model_name" : "NHiTS",
        "obj_name" : "nhits",
        "estimator_func" : "NHiTSModel("+\
                                "input_chunk_length = env_vars[2] * 4,"+\
                                "output_chunk_length=1,"+\
                            ")",
        "imports" : ["NHiTSModel"]},

        {"model_name" : "NLinear",
        "obj_name" : "nlinear",
        "estimator_func" : "NLinearModel("+\
                                "input_chunk_length = env_vars[2] * 4,"+\
                                "output_chunk_length=1,"+\
                            ")",
        "imports" : ["NLinearModel"]},

        {"model_name" : "TiDE",
        "obj_name" : "tide",
        "estimator_func" : "TiDEModel("+\
                                "input_chunk_length = env_vars[2] * 4,"+\
                                "output_chunk_length=1,"+\
                            ")",
        "imports" : ["TiDEModel"]},

        {"model_name" : "Transformer",
        "obj_name" : "transformer",
        "estimator_func" : "TransformerModel("+\
                                "input_chunk_length = env_vars[2] * 4,"+\
                                "output_chunk_length=1,"+\
                            ")",
        "imports" : ["TransformerModel"]},

    ]
    nixtla_models = [
        {"model_name" : "Autoformer",
         "obj_name" : "autoformer",
         "estimator_func" : "Autoformer",
         "imports" : ["Autoformer"]},

        {"model_name" : "Informer",
         "obj_name" : "informer",
         "estimator_func" : "Informer",
         "imports" : ["Informer"]},
    ]
    
    gluonts_models = [
        {"model_name" : "DeepAR",
         "obj_name" : "deepar",
         "estimator_func" : "DeepAREstimator"+\
         "(freq=env_vars[1], context_length = env_vars[2] * 4,"+\
         " prediction_length = 1)",
         "imports" : ["DeepAREstimator"]},

        {"model_name" : "FFNN",
         "obj_name" : "ffnn",
         "estimator_func" : "SimpleFeedForwardEstimator"+\
         "(context_length = env_vars[2] * 4, prediction_length = 1)",
         "imports" : ["SimpleFeedForwardEstimator"]},

         {"model_name" : "PatchTST",
         "obj_name" : "patchtst",
         "estimator_func" : "PatchTSTEstimator("+\
                                "patch_len = env_vars[2],"+\
                                "context_length = env_vars[2] * 4,"+\
                                "prediction_length = 1,"+\
                                "stride = 4)",
         "imports" : ["PatchTSTEstimator"]},

         {"model_name" : "WaveNet",
         "obj_name" : "wavenet",
         "estimator_func" : "WaveNetEstimator(freq = env_vars[1],"+\
                                             "prediction_length=1)",
         "imports" : ["WaveNetEstimator"]},
    ]

    model_dirs = [local_models_darts,
                  global_models_darts,
                  nixtla_models,
                  gluonts_models]

    # Paths that contain example files for main.py and pixi.toml
    examples_path = Path("./examples")
    darts_local_path = examples_path / "DartsLocal"
    darts_global_path = examples_path / "DartsGlobal"
    nixtla_path = examples_path / "Nixtla"
    gluonts_path = examples_path / "GluonTS"

    paths = [darts_local_path,
             darts_global_path,
             nixtla_path,
             gluonts_path]
    
    # Templates for various classes
    # Index 0 : Darts Local main.py
    # Index 1 : Darts Local pixi.toml
    # Index 2 : Darts Global main.py
    # Index 3 : Darts Global pixi.toml
    # Index 4 : Nixtla main.py
    # Index 5 : Nixtla pixi.toml
    # Index 6 : GluonTS main.py
    # Index 7 : GluonTS pixi.toml
    templates = []
    # Darts local
    for path in paths:
        
        with open(path / "main.txt", "r") as main:
            templates.append(main.read())

        with open(path / "pixi.txt", "r") as pixi:
            templates.append(pixi.read())
    
    class_name = ["DartsLocal", "DartsGlobal", "Nixtla", "GluonTS"]

    logger.info("Templates loaded. All variables set up.")
    logger.info("Starting the directory and file generation.")

    # Building the models
    # Can customise range to select specific packages or for darts specific
    # model types
    for i in [0, 1, 2, 3]:
        build_models(model_dirs[i],
                     import_strings[i],
                     templates[2 * i],
                     templates[2 * i + 1],
                     class_name[i])