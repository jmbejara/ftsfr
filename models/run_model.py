"""
run_model.py

A unified runner that can execute any forecasting model based on configuration.
This replaces the need for individual main.py files in each model directory.

Usage:
    python run_model.py --model arima
    python run_model.py --model transformer --config custom_config.toml
"""

import os
import sys
import argparse
import tomllib
import importlib
import subprocess
import logging
from pathlib import Path
from warnings import filterwarnings


# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from env_reader import env_reader
from model_classes.darts_local_class import DartsLocal
from model_classes.darts_global_class import DartsGlobal
from model_classes.nixtla_main_class import NixtlaMain
from model_classes.gluonts_main_class import GluontsMain

filterwarnings("ignore")


def load_config(config_path="models_config.toml"):
    """Load the models configuration from TOML file."""
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def evaluate_param(param_str, env_vars):
    """
    Evaluate parameter strings that contain env_vars references.

    Args:
        param_str: String that may contain env_vars references
        env_vars: Tuple of environment variables (test_split, frequency, seasonality, data_path, output_dir)
    """
    if isinstance(param_str, str) and "env_vars" in param_str:
        # Create a safe evaluation context
        eval_context = {"env_vars": env_vars}
        try:
            return eval(param_str, {"__builtins__": {}}, eval_context)
        except:
            return param_str
    return param_str


def evaluate_special_params(param_str, imports_context):
    """
    Evaluate special parameter strings that reference imported classes.

    Args:
        param_str: String that may contain class references like "ModelMode.ADDITIVE"
        imports_context: Dictionary of imported modules/classes
    """
    if isinstance(param_str, str) and ("." in param_str or "(" in param_str):
        try:
            # Safely evaluate with the imports context
            return eval(param_str, {"__builtins__": {}}, imports_context)
        except:
            return param_str
    return param_str


def process_imports(imports_list):
    """
    Process import statements and return a context dictionary.

    Args:
        imports_list: List of import statements

    Returns:
        Dictionary mapping names to imported objects
    """
    context = {}
    for import_str in imports_list:
        # Parse "from X import Y, Z" style imports
        if import_str.startswith("from "):
            parts = import_str.split(" import ")
            module_path = parts[0].replace("from ", "")
            imports = [i.strip() for i in parts[1].split(",")]

            module = importlib.import_module(module_path)
            for imp in imports:
                context[imp] = getattr(module, imp)

    return context


def create_estimator(model_config, env_vars):
    """
    Create an estimator instance based on the model configuration.

    Args:
        model_config: Dictionary containing model configuration
        env_vars: Environment variables tuple

    Returns:
        Instantiated estimator object
    """
    # Import the estimator class
    module_path, class_name = model_config["estimator_class"].rsplit(".", 1)
    module = importlib.import_module(module_path)
    estimator_class = getattr(module, class_name)

    # Process imports if any
    imports_context = {}
    if "imports" in model_config:
        imports_context = process_imports(model_config["imports"])

    # Process estimator parameters
    params = {}
    for key, value in model_config.get("estimator_params", {}).items():
        # First evaluate env_vars references
        value = evaluate_param(value, env_vars)
        # Then evaluate special parameters (like ModelMode.ADDITIVE)
        value = evaluate_special_params(value, imports_context)
        params[key] = value

    # Special handling for certain models
    if model_config.get("special_handler") == "catboost":
        # Check for GPU availability
        try:
            subprocess.check_output("nvidia-smi")
            params["task_type"] = "GPU"
        except Exception:
            params["task_type"] = "CPU"

    return estimator_class(**params)


def run_model(model_name, config_path="models_config.toml"):
    """
    Run a specific model based on its configuration.

    Args:
        model_name: Name of the model to run (e.g., 'arima', 'transformer')
        config_path: Path to the configuration file
    """
    # Load configuration
    config = load_config(config_path)

    if model_name not in config:
        raise ValueError(f"Model '{model_name}' not found in configuration")

    model_config = config[model_name]

    # Read environment variables
    env_vars = env_reader(os.environ)

    # Setup logging
    data_path = env_vars[3]
    dataset_name = str(os.path.basename(data_path)).split(".")[0]
    dataset_name = dataset_name.removeprefix("ftsfr_")

    log_path = Path().resolve().parent / "model_logs" / model_name
    Path(log_path).mkdir(parents=True, exist_ok=True)
    log_path = log_path / (dataset_name + ".log")
    logging.basicConfig(
        filename=log_path,
        filemode="w",
        format=f"%(asctime)s - {model_name} - %(name)-12s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )

    logger = logging.getLogger("main")
    logger.info(f"Running {model_name} model. Environment variables read.")

    # Handle special models
    if model_config["class"] == "TimesFM":
        # TimesFM has its own implementation
        from timesfm.main import TimesFMForecasting

        model_obj = TimesFMForecasting(
            model_config.get("model_version", "500m"), *env_vars
        )
        model_obj.inference_workflow()
        return

    # Create estimator
    estimator = create_estimator(model_config, env_vars)

    # Create appropriate model object based on class
    model_class = model_config["class"]
    display_name = model_config.get("display_name", model_name)

    if model_class == "DartsLocal":
        model_obj = DartsLocal(estimator, model_name, *env_vars)

    elif model_class == "DartsGlobal":
        model_obj = DartsGlobal(
            estimator,
            model_name,
            *env_vars,
            scaling=model_config.get("scaling", True),
            interpolation=model_config.get("interpolation", True),
            f32=model_config.get("f32", False),
        )

    elif model_class == "NixtlaMain":
        # Nixtla needs special handling for MPS
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        model_obj = NixtlaMain(estimator.__class__, model_name, *env_vars)

    elif model_class == "GluontsMain":
        # GluonTS also needs MPS fallback
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        model_obj = GluontsMain(estimator, model_name, *env_vars)

    else:
        raise ValueError(f"Unknown model class: {model_class}")

    # Run the model workflow
    model_obj.main_workflow()


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Run a forecasting model based on configuration"
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Name of the model to run (e.g., arima, transformer)",
    )
    parser.add_argument(
        "--config",
        default="models_config.toml",
        help="Path to the configuration file (default: models_config.toml)",
    )

    args = parser.parse_args()

    # Run the specified model
    run_model(args.model, args.config)


if __name__ == "__main__":
    main()
