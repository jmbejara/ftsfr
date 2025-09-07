"""
run_model.py

A unified runner that can execute any forecasting model based on configuration.
This replaces the need for individual main.py files in each model directory.

Usage:
    python run_model.py --model arima
    python run_model.py --model transformer --config custom_config.toml

Output Structure:
    All outputs are saved under {OUTPUT_DIR}/forecasting/ with the following structure:

    {OUTPUT_DIR}/
    └── forecasting/
        ├── logging/{model_name}/{dataset_name}.log       # Training and execution logs
        ├── error_metrics/{model_name}/{dataset_name}.csv # MASE, MAE, RMSE metrics
        ├── model_checkpoints/{model_name}/{dataset_name}/ # Trained model files
        └── forecasts/{model_name}/{dataset_name}/         # Prediction results
            └── forecasts.parquet

    Where:
    - {model_name}: The name of the forecasting model (e.g., 'arima', 'transformer')
    - {dataset_name}: The dataset name without 'ftsfr_' prefix (e.g., 'treas_bond_returns')
    - OUTPUT_DIR: Controlled by --output-dir CLI argument or OUTPUT_DIR environment variable

Error Metrics:
    - MASE: Mean Absolute Scaled Error (primary metric)
    - MAE: Mean Absolute Error
    - RMSE: Root Mean Squared Error
    All three metrics are calculated and saved for every forecasting run.
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
import torch

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Enable MPS fallback for better compatibility with Apple Silicon
# This must be set before any PyTorch operations to avoid NotImplementedError
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

from config_reader import get_model_config

filterwarnings("ignore")


def load_config(config_path=None):
    """Load the models configuration from TOML file."""
    if config_path is None:
        # Try to find models_config.toml relative to this file
        current_dir = Path(__file__).parent

        # First try: current directory (when running from models/ folder)
        config_path = current_dir / "models_config.toml"
        if not config_path.exists():
            # Second try: project root (when running from project root)
            config_path = current_dir.parent / "models" / "models_config.toml"

        if not config_path.exists():
            raise FileNotFoundError(
                f"Could not find models_config.toml in either:\n"
                f"  - {current_dir / 'models_config.toml'}\n"
                f"  - {current_dir.parent / 'models' / 'models_config.toml'}"
            )

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


def create_estimator(model_config, seasonality, frequency, n_epochs=None):
    """
    Create an estimator instance based on the model configuration.

    Args:
        model_config: Dictionary containing model configuration
        seasonality: Seasonal period length
        frequency: Data frequency (e.g., 'D', 'M', 'Q')
        n_epochs: Optional override for number of training epochs (for debugging)

    Returns:
        Instantiated estimator object
    """
    # Import the estimator class
    estimator_class = get_estimator_class(model_config)

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
    
    # StatsForecast AutoARIMA speed optimizations
    if "AutoARIMA" in model_name and model_config.get("class") == "StatsForecastMain":
        # Speed optimizations for StatsForecast AutoARIMA
        if "approximation" not in params:
            params["approximation"] = True  # Use approximation for faster search
        if "stepwise" not in params:
            params["stepwise"] = True  # Use stepwise search instead of grid search
        if "max_p" not in params:
            params["max_p"] = 3  # Limit maximum AR order for speed
        if "max_q" not in params:
            params["max_q"] = 3  # Limit maximum MA order for speed
        if "max_P" not in params:
            params["max_P"] = 2  # Limit seasonal AR order for speed
        if "max_Q" not in params:
            params["max_Q"] = 2  # Limit seasonal MA order for speed
        print(f"Applied speed optimizations for StatsForecast AutoARIMA: approximation={params['approximation']}, stepwise={params['stepwise']}")

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
        for name in ["Autoformer", "Informer", "DLinear", "NLinear", "NBEATS"]
    ):
        if "input_size" not in params:
            params["input_size"] = seasonality * 4

        # Enable Apple Silicon (MPS) for Nixtla models if available
        if torch.backends.mps.is_available():
            params["accelerator"] = "mps"
            print(f"Using Apple Silicon (MPS) for {model_name}")
        elif torch.cuda.is_available():
            params["accelerator"] = "gpu"
            print(f"Using CUDA GPU for {model_name}")
        else:
            params["accelerator"] = "cpu"
            print(f"Using CPU for {model_name}")

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
            # Convert frequency for GluonTS models (ME -> M)
            def convert_frequency_for_gluonts(freq):
                """Convert frequency strings for GluonTS compatibility."""
                if freq == "ME" or freq == "MS":
                    return "M"  # Month end -> Month
                elif freq == "QE" or freq == "QS":
                    return "Q"
                return freq

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

        # Force CPU usage for GluonTS models on Apple Silicon to avoid MPS compatibility issues
        # The _standard_gamma operation used by Student's t-distribution is not implemented on MPS
        if torch.backends.mps.is_available():
            if "trainer_kwargs" not in params:
                params["trainer_kwargs"] = {}
            params["trainer_kwargs"]["accelerator"] = "cpu"
            print(
                f"Forcing CPU usage for GluonTS model {model_name} on Apple Silicon to avoid MPS compatibility issues"
            )

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

    # Apply n_epochs override if provided
    if n_epochs is not None:
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
            print(f"Overriding max_epochs to {n_epochs} for GluonTS model")
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
            print(f"Overriding n_epochs to {n_epochs} for Darts neural model")
        elif model_config["class"] == "NixtlaMain":
            # For Nixtla models, use max_steps instead of max_epochs (which is deprecated)
            # Use a very small number of steps for debugging (e.g., 50 steps)
            max_steps = n_epochs * 50
            params["max_steps"] = max_steps
            print(f"Overriding max_steps to {max_steps} for Nixtla model")
        else:
            # Skip n_epochs for models that don't support it (e.g., ARIMA, Prophet, etc.)
            print(f"Skipping n_epochs override for {model_name} - not a neural model")

    return estimator_class(**params)


def run_model(
    model_name,
    test_split,
    frequency,
    seasonality,
    data_path,
    output_dir,
    config_path=None,
    workflow="main",
    log_path=None,
    n_epochs=None,
    winsorization=None,
):
    """
    Run a specific model based on its configuration.

    Args:
        model_name: Name of the model to run (e.g., 'arima', 'transformer')
        test_split: Fraction of data to use for testing
        frequency: Data frequency (e.g., 'D', 'M', 'Q')
        seasonality: Seasonal period length
        data_path: Path to the dataset file
        output_dir: Directory to save outputs
        config_path: Path to the configuration file
        workflow: Which workflow to run ('main', 'train', 'inference', 'evaluate')
        log_path: Optional path for logging
        n_epochs: Optional override for number of training epochs (for debugging)

    Output Locations:
        For a model 'arima' run on 'ftsfr_treas_bond_returns.parquet' with output_dir='../_output':

        Logs: ../_output/forecasting/logging/arima/treas_bond_returns.log
        Error Metrics: ../_output/forecasting/error_metrics/arima/treas_bond_returns.csv
        Model Files: ../_output/forecasting/model_checkpoints/arima/treas_bond_returns/
        Forecasts: ../_output/forecasting/forecasts/arima/treas_bond_returns/forecasts.parquet

    Error Metrics CSV Format:
        Columns: Model, Dataset, Entities, Seasonality, [Global_]MASE, [Global_]MAE, [Global_]RMSE
        - For local models (DartsLocal): Also includes Median_MASE, Median_MAE, Median_RMSE
        - For global models: Uses Global_ prefix for metrics
    """
    # Load configuration
    config = load_config(config_path)

    if model_name not in config:
        raise ValueError(f"Model '{model_name}' not found in configuration")

    model_config = config[model_name]

    # Nixtla model imports break logging
    # So keeping the create_estimator function here and logging after it
    estimator = create_estimator(
        model_config=model_config,
        seasonality=seasonality,
        frequency=frequency,
        n_epochs=n_epochs,
    )

    if log_path is None:
        # If run_model.py is called instead of through some other file
        # Use the new forecasting logging directory structure
        log_path = Path(output_dir) / "forecasting" / "logging" / model_name
        try:
            log_path.mkdir(parents=True, exist_ok=True)
        except:
            pass
        # Extract dataset name from data_path for logging
        dataset_name = Path(data_path).stem.removeprefix("ftsfr_")
        log_path = log_path / (dataset_name + ".log")
        logging.basicConfig(
            filename=log_path,
            filemode="w",
            format=f"%(asctime)s - {model_name} - %(name)-12s - %(levelname)s - %(message)s",
            level=logging.DEBUG,
        )
        remove_handler = False
    else:
        # Meant for calls from some other file
        log_path = log_path / model_name
        try:
            log_path.mkdir(parents=True, exist_ok=True)
        except:
            pass
        # Extract dataset name from data_path for logging
        dataset_name = Path(data_path).stem.removeprefix("ftsfr_")
        log_path = log_path / (dataset_name + ".log")
        f = logging.Formatter("%(asctime)s - %(name)-12s - %(levelname)s - %(message)s")
        logging.getLogger().setLevel(logging.DEBUG)
        handler_file = logging.FileHandler(log_path, mode="a")
        handler_file.setLevel(logging.DEBUG)
        handler_file.setFormatter(f)
        logging.getLogger().addHandler(handler_file)
        remove_handler = True

    logger = logging.getLogger(f"run_model_{model_name}")
    logger.info(
        f"Running {model_name} model with parameters: test_split={test_split}, frequency={frequency}, seasonality={seasonality}, data_path={data_path}, output_dir={output_dir}"
    )

    # Handle special models
    model_class = model_config["class"]

    # Additional MPS environment variables for better Apple Silicon support
    if torch.backends.mps.is_available():
        os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
        print("DEBUG: Set MPS environment variables for Apple Silicon")

    # Dynamically import the required model class only when needed
    if model_class == "DartsLocal":
        from model_classes.darts_local_class import DartsLocal

        object_class = DartsLocal
    elif model_class == "DartsGlobal":
        from model_classes.darts_global_class import DartsGlobal

        object_class = DartsGlobal
    elif model_class == "NixtlaMain":
        from model_classes.nixtla_main_class import NixtlaMain

        object_class = NixtlaMain
    elif model_class == "StatsForecastMain":
        from model_classes.statsforecast_main_class import StatsForecastMain

        object_class = StatsForecastMain
    elif model_class == "GluontsMain":
        from model_classes.gluonts_main_class import GluontsMain

        object_class = GluontsMain
    elif model_class == "TimesFM":
        # Add the timesfm directory to the path for local import
        timesfm_path = os.path.join(os.path.dirname(__file__), "timesfm")
        if timesfm_path not in sys.path:
            sys.path.insert(0, timesfm_path)
        from main import TimesFMForecasting

        model_obj = TimesFMForecasting(
            model_config.get("model_version", "500m"),
            test_split,
            frequency,
            seasonality,
            data_path,
            output_dir,
        )
        model_obj.inference_workflow()
        return
    else:
        raise ValueError(f"Unknown model class: {model_class}")

    model_obj = object_class(
        estimator, model_name, test_split, frequency, seasonality, data_path, output_dir, winsorization
    )

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

    if remove_handler:
        h_to_remove = logging.getLogger().handlers[-1]
        logging.getLogger().removeHandler(h_to_remove)


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
        default=None,
        help="Path to the configuration file (default: auto-detect models_config.toml)",
    )
    parser.add_argument(
        "--workflow",
        choices=["main", "train", "inference", "evaluate"],
        default="main",
        help="Which workflow to run (default: main)",
    )
    # Add CLI arguments for all environment variables
    parser.add_argument(
        "--dataset-path",
        help="Path to the dataset file (overrides DATASET_PATH env var, e.g. '../_data/us_treasury_returns/ftsfr_treas_bond_returns.parquet')",
    )
    parser.add_argument(
        "--frequency",
        help="Data frequency (overrides FREQUENCY env var, e.g. 'D' for daily, 'M' for monthly, 'Q' for quarterly)",
    )
    parser.add_argument(
        "--seasonality",
        type=int,
        help="Seasonal period length (overrides SEASONALITY env var, e.g. 7 for weekly, 12 for monthly, 4 for quarterly)",
    )
    parser.add_argument(
        "--test-split",
        help="Fraction of data for testing (overrides TEST_SPLIT env var, e.g. 0.2 for 20 percent, 'seasonal' for seasonal split)",
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory (overrides OUTPUT_DIR env var, e.g. '../_output/custom')",
    )
    parser.add_argument(
        "--n-epochs",
        type=int,
        help="Number of training epochs (overrides N_EPOCHS env var, e.g. 5 for quick testing)",
    )
    parser.add_argument(
        "--winsorize",
        help="Override winsorization settings (e.g. '[1.0,99.0]' for 1%%-99%% winsorization, 'none' to disable)",
    )
    # Additional useful CLI arguments
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Enable parallel processing (if supported by the model)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of parallel workers (default: 1)",
    )

    args = parser.parse_args()

    # Create a modified environment dictionary with CLI arguments taking priority
    modified_env = os.environ.copy()

    # Override environment variables with CLI arguments if provided
    if args.dataset_path:
        modified_env["DATASET_PATH"] = args.dataset_path
    if args.frequency:
        modified_env["FREQUENCY"] = args.frequency
    if args.seasonality:
        modified_env["SEASONALITY"] = str(args.seasonality)
    if args.test_split:
        modified_env["TEST_SPLIT"] = args.test_split
    if args.output_dir:
        modified_env["OUTPUT_DIR"] = args.output_dir
    if args.n_epochs:
        modified_env["N_EPOCHS"] = str(args.n_epochs)

    # Read configuration (dataset config + environment overrides)
    dataset_config = get_model_config(modified_env)
    # Unpack the full configuration tuple
    (test_split, frequency, seasonality, data_path, output_dir, dataset_name, winsorization) = dataset_config
    
    # Handle winsorization CLI override
    if args.winsorize is not None:
        if args.winsorize.lower() == 'none':
            winsorization = None
            print("DEBUG: Disabled winsorization via --winsorize none")
        else:
            # Parse format like '[1.0,99.0]'
            try:
                winsorize_str = args.winsorize.strip('[]')
                winsorization = [float(x.strip()) for x in winsorize_str.split(',')]
                if len(winsorization) != 2:
                    raise ValueError("Expected exactly 2 values")
                print(f"DEBUG: Override winsorization to {winsorization} via --winsorize")
            except Exception as e:
                raise ValueError(f"Invalid winsorization format '{args.winsorize}'. Expected format: '[1.0,99.0]' or 'none'") from e

    # Handle N_EPOCHS environment variable for debugging
    n_epochs = None
    if "N_EPOCHS" in modified_env:
        n_epochs = int(modified_env["N_EPOCHS"])
        print(f"DEBUG: Found N_EPOCHS={n_epochs}")

    # Run the specified model
    run_model(
        args.model,
        test_split,
        frequency,
        seasonality,
        data_path,
        output_dir,
        args.config,
        args.workflow,
        n_epochs=n_epochs,
        winsorization=winsorization,
    )


if __name__ == "__main__":
    main()
