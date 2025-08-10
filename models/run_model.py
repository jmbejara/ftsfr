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
import tomli
import importlib
import subprocess
import logging
from pathlib import Path
from warnings import filterwarnings


# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_reader import get_model_config

filterwarnings("ignore")


def load_config(config_path="models_config.toml"):
    """Load the models configuration from TOML file."""
    with open(config_path, "rb") as f:
        return tomli.load(f)


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


def get_estimator_class(model_config):
    """
    Get the estimator class from the model configuration.

    Args:
        model_config: Dictionary containing model configuration

    Returns:
        Estimator class (not instantiated)
    """
    # Import the estimator class
    module_path, class_name = model_config["estimator_class"].rsplit(".", 1)
    module = importlib.import_module(module_path)
    estimator_class = getattr(module, class_name)
    return estimator_class


def get_nixtla_estimator_params(model_config, env_vars):
    """
    Get estimator parameters for Nixtla models, including environment variable overrides.

    Args:
        model_config: Dictionary containing model configuration
        env_vars: Environment variables tuple (test_split, frequency, seasonality, data_path, output_dir)

    Returns:
        Dictionary of estimator parameters
    """
    # Extract dataset parameters
    test_split, frequency, seasonality, data_path, output_dir = env_vars

    # Process imports if any
    imports_context = {}
    if "imports" in model_config:
        imports_context = process_imports(model_config["imports"])

    # Process estimator parameters
    params = {}
    for key, value in model_config.get("estimator_params", {}).items():
        # Evaluate special parameters (like ModelMode.ADDITIVE)
        value = evaluate_special_params(value, imports_context)
        params[key] = value

    # Set default input_size for Nixtla models
    if "input_size" not in params:
        params["input_size"] = seasonality * 4

    # Environment variable overrides for debugging
    # Allow overriding max_steps via environment variable for debugging
    if "N_EPOCHS" in os.environ:
        n_epochs = int(os.environ["N_EPOCHS"])
        # For Nixtla models, use max_steps instead of max_epochs (which is deprecated)
        # Use a very small number of steps for debugging (e.g., 50 steps)
        max_steps = n_epochs * 50
        params["max_steps"] = max_steps
        print(
            f"Overriding max_steps to {max_steps} via environment variable for Nixtla model"
        )

    return params


def create_estimator(model_config, env_vars):
    """
    Create an estimator instance based on the model configuration.

    Args:
        model_config: Dictionary containing model configuration
        env_vars: Environment variables tuple (test_split, frequency, seasonality, data_path, output_dir)

    Returns:
        Instantiated estimator object
    """
    # Import the estimator class
    estimator_class = get_estimator_class(model_config)

    # Extract dataset parameters
    test_split, frequency, seasonality, data_path, output_dir = env_vars

    # Convert frequency for GluonTS models (ME -> M)
    def convert_frequency_for_gluonts(freq):
        """Convert frequency strings for GluonTS compatibility."""
        if freq == "ME":
            return "M"  # Month end -> Month
        return freq

    # Process imports if any
    imports_context = {}
    if "imports" in model_config:
        imports_context = process_imports(model_config["imports"])

    # Process estimator parameters
    params = {}
    for key, value in model_config.get("estimator_params", {}).items():
        # Evaluate special parameters (like ModelMode.ADDITIVE)
        value = evaluate_special_params(value, imports_context)
        params[key] = value

    # Inject dataset-specific parameters based on model requirements
    model_name = model_config.get("estimator_class", "")

    # Models that need season_length
    if any(
        name in model_name
        for name in [
            "AutoARIMA",
            "AutoCES",
            "AutoETS",
            "AutoMFLES",
            "AutoTBATS",
            "AutoTheta",
            "TBATS",
        ]
    ):
        if "season_length" not in params:
            params["season_length"] = seasonality

    # Models that need input_chunk_length (typically seasonality * 4)
    if any(
        name in model_name
        for name in [
            "DLinearModel",
            "GlobalNaive",
            "NBEATSModel",
            "NHiTSModel",
            "NLinearModel",
            "TiDEModel",
            "TransformerModel",
            "NaiveMovingAverage",
        ]
    ):
        if "input_chunk_length" not in params:
            params["input_chunk_length"] = seasonality * 4

    # Nixtla models that need input_size (typically seasonality * 4)
    if any(
        name in model_name
        for name in [
            "Autoformer",
            "Informer",
        ]
    ):
        if "input_size" not in params:
            params["input_size"] = seasonality * 4

    # Models that need lags
    if "CatBoostModel" in model_name or (
        "SKLearnModel" in model_name and "lags" not in params
    ):
        params["lags"] = seasonality * 4

    # Models that need K (for NaiveSeasonal)
    if model_name.startswith(("NaiveSeasonal")) and "K" not in params:
        params["K"] = seasonality

    # GluonTS models that need frequency
    if any(name in model_name for name in ["DeepAREstimator", "WaveNetEstimator"]):
        if "freq" not in params:
            params["freq"] = convert_frequency_for_gluonts(frequency)

    # GluonTS models that need context_length
    if any(
        name in model_name
        for name in [
            "DeepAREstimator",
            "SimpleFeedForwardEstimator",
            "PatchTSTEstimator",
        ]
    ):
        if "context_length" not in params:
            params["context_length"] = seasonality * 4

    # PatchTST specific
    if "PatchTSTEstimator" in model_name and "patch_len" not in params:
        params["patch_len"] = seasonality

    # Special handling for certain models
    if model_config.get("special_handler") == "catboost":
        # Check for GPU availability
        try:
            subprocess.check_output("nvidia-smi")
            params["task_type"] = "GPU"
        except Exception:
            params["task_type"] = "CPU"

    # Environment variable overrides for debugging
    # Allow overriding n_epochs via environment variable for debugging
    print(
        f"DEBUG: Checking for N_EPOCHS environment variable. Available env vars: {[k for k in os.environ.keys() if 'EPOCH' in k.upper()]}"
    )
    if "N_EPOCHS" in os.environ:
        n_epochs = int(os.environ["N_EPOCHS"])
        print(f"DEBUG: Found N_EPOCHS={n_epochs}")

        # Handle different parameter names for different model types
        if any(
            name in model_name
            for name in [
                "DeepAREstimator",
                "SimpleFeedForwardEstimator",
                "PatchTSTEstimator",
                "WaveNetEstimator",
            ]
        ):
            # GluonTS models use trainer_kwargs with max_epochs
            if "trainer_kwargs" not in params:
                params["trainer_kwargs"] = {}
            params["trainer_kwargs"]["max_epochs"] = n_epochs
            print(
                f"Overriding max_epochs to {n_epochs} via environment variable for GluonTS model"
            )
        elif any(
            name in model_name
            for name in [
                "DLinearModel",
                "NLinearModel",
                "TransformerModel",
                "NBEATSModel",
                "NHiTSModel",
                "TiDEModel",
            ]
        ):
            # Darts neural models use n_epochs directly
            params["n_epochs"] = n_epochs
            print(
                f"Overriding n_epochs to {n_epochs} via environment variable for Darts neural model"
            )
        else:
            # Skip n_epochs for models that don't support it (e.g., ARIMA, Prophet, etc.)
            print(f"Skipping n_epochs override for {model_name} - not a neural model")

    return estimator_class(**params)


def run_model(model_name, config_path="models_config.toml", workflow="main"):
    """
    Run a specific model based on its configuration.

    Args:
        model_name: Name of the model to run (e.g., 'arima', 'transformer')
        config_path: Path to the configuration file
        workflow: Which workflow to run ('main', 'train', 'inference', 'evaluate')
    """
    # Load configuration
    config = load_config(config_path)

    if model_name not in config:
        raise ValueError(f"Model '{model_name}' not found in configuration")

    model_config = config[model_name]

    # Read configuration (dataset config + environment overrides)
    dataset_config = get_model_config(os.environ)
    # Unpack for backward compatibility
    env_vars = dataset_config[
        :5
    ]  # (test_split, frequency, seasonality, dataset_path, output_dir)
    dataset_name = dataset_config[5]

    # Setup logging
    data_path = env_vars[3]

    log_path = Path().resolve() / "model_logs" / "run_model_runs" / model_name
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
    model_class = model_config["class"]
    display_name = model_config.get("display_name", model_name)

    # Dynamically import the required model class only when needed
    if model_class == "DartsLocal":
        from model_classes.darts_local_class import DartsLocal

        estimator = create_estimator(model_config, env_vars)
        model_obj = DartsLocal(estimator, model_name, *env_vars)
    elif model_class == "DartsGlobal":
        from model_classes.darts_global_class import DartsGlobal

        estimator = create_estimator(model_config, env_vars)
        model_obj = DartsGlobal(
            estimator,
            model_name,
            *env_vars,
            scaling=model_config.get("scaling", True),
            interpolation=model_config.get("interpolation", True),
            f32=model_config.get("f32", False),
        )
    elif model_class == "NixtlaMain":
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        from model_classes.nixtla_main_class import NixtlaMain

        # For Nixtla models, we need the estimator class and parameters
        estimator_class = get_estimator_class(model_config)
        # Get estimator parameters for Nixtla models (including n_epochs override)
        estimator_params = get_nixtla_estimator_params(model_config, env_vars)
        model_obj = NixtlaMain(
            estimator_class, model_name, *env_vars, estimator_params=estimator_params
        )
    elif model_class == "GluontsMain":
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        from model_classes.gluonts_main_class import GluontsMain

        estimator = create_estimator(model_config, env_vars)
        model_obj = GluontsMain(estimator, model_name, *env_vars)
    elif model_class == "TimesFM":
        # Add the timesfm directory to the path for local import
        timesfm_path = os.path.join(os.path.dirname(__file__), "timesfm")
        if timesfm_path not in sys.path:
            sys.path.insert(0, timesfm_path)
        from main import TimesFMForecasting

        model_obj = TimesFMForecasting(
            model_config.get("model_version", "500m"), *env_vars
        )
        model_obj.inference_workflow()
        return
    else:
        raise ValueError(f"Unknown model class: {model_class}")

    # Run the selected workflow
    if workflow == "main":
        model_obj.main_workflow()
    elif workflow == "train":
        model_obj.training_workflow()
    elif workflow == "inference":
        model_obj.inference_workflow()
    elif workflow == "evaluate":
        # For evaluate-only workflow, we need to load predictions first
        model_obj.load_forecast()
        model_obj.calculate_error()
        model_obj.print_summary()
        model_obj.save_results()
    else:
        raise ValueError(f"Unknown workflow: {workflow}")


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
    parser.add_argument(
        "--workflow",
        choices=["main", "train", "inference", "evaluate"],
        default="main",
        help="Which workflow to run (default: main)",
    )

    args = parser.parse_args()

    # Run the specified model
    run_model(args.model, args.config, args.workflow)


if __name__ == "__main__":
    main()
