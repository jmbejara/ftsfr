"""
run_all_models_all_datasets.py

A comprehensive script that runs all forecasting models on all available datasets.
This script is designed to be robust and continue running even if individual
model-dataset combinations fail.

Features:
- Runs all models from models_config.toml on all datasets from datasets.toml
- Robust error handling - continues on failures
- Comprehensive logging to track progress and errors
- Progress tracking with timestamps
- Results summary at the end
- Can be run overnight with confidence

Usage:
    python run_all_models_all_datasets.py
    python run_all_models_all_datasets.py --parallel --workers 4
    python run_all_models_all_datasets.py --models arima transformer --datasets cds_returns.ftsfr_CDS_contract_returns
"""

import os
import sys
import argparse
import tomli
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
import json
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import traceback

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from run_model import run_model, load_config


def setup_logging(log_dir: Path) -> logging.Logger:
    """Setup comprehensive logging for the batch run."""
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a unique log file for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"batch_run_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting batch run - logging to {log_file}")
    return logger


def get_all_datasets() -> List[str]:
    """Get all available datasets from datasets.toml."""
    datasets = []
    
    # Load datasets.toml
    config_path = Path(__file__).parent.parent / "datasets.toml"
    with open(config_path, "rb") as f:
        datasets_config = tomli.load(f)
    
    # Extract all dataset paths
    for section, content in datasets_config.items():
        if isinstance(content, dict):
            for subsection, subcontent in content.items():
                if isinstance(subcontent, dict) and any(key in subcontent for key in ["frequency", "seasonality"]):
                    # This is a dataset with configuration
                    dataset_path = f"../_data/{subsection}.parquet"
                    datasets.append(dataset_path)
    
    return sorted(datasets)


def get_all_models(config_path: str = "models_config.toml") -> List[str]:
    """Get all available models from models_config.toml."""
    config = load_config(config_path)
    return list(config.keys())


def run_single_model_dataset(
    model_name: str, 
    dataset_path: str, 
    config_path: str = "models_config.toml",
    workflow: str = "main"
) -> Dict:
    """
    Run a single model on a single dataset with comprehensive error handling.
    
    Returns:
        Dict with results including success status, timing, and error details
    """
    start_time = datetime.now()
    result = {
        "model": model_name,
        "dataset": dataset_path,
        "start_time": start_time.isoformat(),
        "success": False,
        "duration": 0.0,
        "error": None,
        "error_traceback": None
    }
    
    try:
        # Set environment variables for this run
        os.environ["DATASET_PATH"] = dataset_path
        
        # Run the model
        run_model(model_name, config_path, workflow)
        
        # Success
        end_time = datetime.now()
        result.update({
            "success": True,
            "duration": (end_time - start_time).total_seconds(),
            "end_time": end_time.isoformat()
        })
        
    except Exception as e:
        # Failure
        end_time = datetime.now()
        result.update({
            "success": False,
            "duration": (end_time - start_time).total_seconds(),
            "end_time": end_time.isoformat(),
            "error": str(e),
            "error_traceback": traceback.format_exc()
        })
    
    return result


def run_models_sequential(
    models: List[str], 
    datasets: List[str], 
    config_path: str = "models_config.toml",
    workflow: str = "main",
    logger: Optional[logging.Logger] = None
) -> List[Dict]:
    """Run all model-dataset combinations sequentially."""
    results = []
    total_combinations = len(models) * len(datasets)
    current = 0
    
    if logger:
        logger.info(f"Starting sequential run of {total_combinations} model-dataset combinations")
    
    for model_name in models:
        for dataset_path in datasets:
            current += 1
            
            if logger:
                logger.info(f"[{current}/{total_combinations}] Running {model_name} on {dataset_path}")
            
            result = run_single_model_dataset(model_name, dataset_path, config_path, workflow)
            results.append(result)
            
            if result["success"]:
                if logger:
                    logger.info(f"✓ {model_name} on {dataset_path} completed in {result['duration']:.2f}s")
            else:
                if logger:
                    logger.warning(f"✗ {model_name} on {dataset_path} failed: {result['error']}")
    
    return results


def run_models_parallel(
    models: List[str], 
    datasets: List[str], 
    config_path: str = "models_config.toml",
    workflow: str = "main",
    max_workers: Optional[int] = None,
    logger: Optional[logging.Logger] = None
) -> List[Dict]:
    """Run all model-dataset combinations in parallel."""
    results = []
    total_combinations = len(models) * len(datasets)
    
    if max_workers is None:
        max_workers = min(multiprocessing.cpu_count(), total_combinations)
    
    if logger:
        logger.info(f"Starting parallel run of {total_combinations} combinations with {max_workers} workers")
    
    # Create all combinations
    combinations = [(model, dataset) for model in models for dataset in datasets]
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(run_single_model_dataset, model, dataset, config_path, workflow): (model, dataset)
            for model, dataset in combinations
        }
        
        # Process completed tasks
        completed = 0
        for future in as_completed(futures):
            completed += 1
            model, dataset = futures[future]
            result = future.result()
            results.append(result)
            
            if logger:
                if result["success"]:
                    logger.info(f"[{completed}/{total_combinations}] ✓ {model} on {dataset} completed in {result['duration']:.2f}s")
                else:
                    logger.warning(f"[{completed}/{total_combinations}] ✗ {model} on {dataset} failed: {result['error']}")
    
    return results


def print_summary(results: List[Dict], logger: Optional[logging.Logger] = None):
    """Print a comprehensive summary of the batch run results."""
    total = len(results)
    successful = sum(1 for r in results if r["success"])
    failed = total - successful
    total_time = sum(r["duration"] for r in results)
    
    summary = f"""
{'='*80}
BATCH RUN SUMMARY
{'='*80}
Total combinations: {total}
Successful: {successful}
Failed: {failed}
Success rate: {successful/total*100:.1f}%
Total execution time: {total_time:.2f}s

Failed combinations:"""
    
    if logger:
        logger.info(summary)
    else:
        print(summary)
    
    # Show failed combinations
    failed_results = [r for r in results if not r["success"]]
    if failed_results:
        for result in failed_results:
            error_msg = f"  - {result['model']} on {result['dataset']}: {result['error']}"
            if logger:
                logger.warning(error_msg)
            else:
                print(error_msg)
    
    # Show top 5 slowest successful runs
    successful_results = [r for r in results if r["success"]]
    if successful_results:
        sorted_results = sorted(successful_results, key=lambda x: x["duration"], reverse=True)
        print("\nTop 5 slowest successful runs:")
        for result in sorted_results[:5]:
            print(f"  - {result['model']} on {result['dataset']}: {result['duration']:.2f}s")


def save_results(results: List[Dict], output_file: str, logger: Optional[logging.Logger] = None):
    """Save detailed results to a JSON file."""
    results_data = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": len(results),
            "successful": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
            "total_duration": sum(r["duration"] for r in results)
        },
        "results": results
    }
    
    with open(output_file, "w") as f:
        json.dump(results_data, f, indent=2)
    
    if logger:
        logger.info(f"Results saved to: {output_file}")
    else:
        print(f"\nResults saved to: {output_file}")


def main():
    """Main entry point for the batch run script."""
    parser = argparse.ArgumentParser(
        description="Run all forecasting models on all available datasets"
    )
    
    # Model and dataset selection
    parser.add_argument(
        "--models", 
        nargs="+", 
        help="Specific models to run (default: all models)"
    )
    parser.add_argument(
        "--datasets", 
        nargs="+", 
        help="Specific datasets to run (default: all datasets)"
    )
    
    # Execution options
    parser.add_argument(
        "--parallel", 
        action="store_true", 
        help="Run combinations in parallel"
    )
    parser.add_argument(
        "--workers", 
        type=int, 
        help="Number of parallel workers (default: CPU count)"
    )
    
    # Other options
    parser.add_argument(
        "--config", 
        default="models_config.toml", 
        help="Path to models configuration file"
    )
    parser.add_argument(
        "--workflow",
        choices=["main", "train", "inference", "evaluate"],
        default="main",
        help="Which workflow to run (default: main)"
    )
    parser.add_argument(
        "--save-results", 
        help="Save detailed results to JSON file"
    )
    parser.add_argument(
        "--log-dir", 
        default="model_logs/batch_runs",
        help="Directory for batch run logs"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_dir = Path(args.log_dir)
    logger = setup_logging(log_dir)
    
    # Get all models and datasets
    all_models = get_all_models(args.config)
    all_datasets = get_all_datasets()
    
    # Filter if specific models/datasets requested
    models = args.models if args.models else all_models
    datasets = args.datasets if args.datasets else all_datasets
    
    # Validate models
    invalid_models = [m for m in models if m not in all_models]
    if invalid_models:
        logger.error(f"Unknown models: {', '.join(invalid_models)}")
        return
    
    # For datasets, we'll be more flexible - just check if the file exists
    for dataset in datasets:
        if not Path(dataset).exists():
            logger.warning(f"Dataset file not found: {dataset}")
            logger.warning("Continuing anyway - the model will fail if the file is truly missing")
    
    logger.info(f"Running {len(models)} models on {len(datasets)} datasets")
    logger.info(f"Total combinations: {len(models) * len(datasets)}")
    logger.info(f"Models: {', '.join(models)}")
    logger.info(f"Datasets: {', '.join(datasets)}")
    
    # Run the combinations
    start_time = datetime.now()
    
    if args.parallel:
        results = run_models_parallel(
            models, datasets, args.config, args.workflow, args.workers, logger
        )
    else:
        results = run_models_sequential(
            models, datasets, args.config, args.workflow, logger
        )
    
    total_duration = (datetime.now() - start_time).total_seconds()
    
    # Print summary
    print_summary(results, logger)
    logger.info(f"Total batch execution time: {total_duration:.2f}s")
    
    # Save results if requested
    if args.save_results:
        save_results(results, args.save_results, logger)
    
    logger.info("Batch run completed!")


if __name__ == "__main__":
    main()
