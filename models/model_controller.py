"""
model_controller.py

A controller for orchestrating multiple model runs, parallel execution,
and batch processing of forecasting models.

Usage:
    # Run all models
    python model_controller.py --all

    # Run specific models
    python model_controller.py --models arima transformer nbeats

    # Run all models of a specific class
    python model_controller.py --class DartsLocal

    # Run models in parallel
    python model_controller.py --all --parallel --workers 4
"""

import os
import sys
import argparse
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
import json
from time import strftime
from pathlib import Path
import logging

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from run_model import run_model, load_config


def run_model_wrapper(model_name, config_path, workflow="main", log_path = None):
    """
    Wrapper function for running a model that captures output and errors.

    Returns:
        tuple: (model_name, success, duration, error_message)
    """
    start_time = datetime.now()
    try:
        run_model(model_name, config_path, workflow, log_path)
        duration = (datetime.now() - start_time).total_seconds()
        return model_name, True, duration, None
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        return model_name, False, duration, str(e)


def run_models_sequential(models, config_path, workflow="main", log_path = None):
    """Run models sequentially."""
    results = []
    total_models = len(models)

    print(f"\nRunning {total_models} models sequentially (workflow: {workflow})...")
    print("-" * 60)

    for i, model_name in enumerate(models, 1):
        print(f"\n[{i}/{total_models}] Running {model_name}...")
        result = run_model_wrapper(model_name, config_path, workflow, log_path)
        results.append(result)

        if result[1]:  # Success
            print(f"✓ {model_name} completed in {result[2]:.2f}s")
        else:
            print(f"✗ {model_name} failed: {result[3]}")

    return results


def run_models_parallel(models, config_path, workflow="main", max_workers=None, log_path = None):
    """Run models in parallel using ProcessPoolExecutor."""
    results = []
    total_models = len(models)

    if max_workers is None:
        max_workers = min(multiprocessing.cpu_count(), total_models)

    print(
        f"\nRunning {total_models} models in parallel (max {max_workers} workers, workflow: {workflow})..."
    )
    print("-" * 60)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(
                run_model_wrapper, model_name, config_path, workflow, log_path
            ): model_name
            for model_name in models
        }

        # Process completed tasks
        completed = 0
        for future in as_completed(futures):
            completed += 1
            model_name = futures[future]
            result = future.result()
            results.append(result)

            if result[1]:  # Success
                print(
                    f"[{completed}/{total_models}] ✓ {model_name} completed in {result[2]:.2f}s"
                )
            else:
                print(
                    f"[{completed}/{total_models}] ✗ {model_name} failed: {result[3]}"
                )

    return results


def filter_models_by_class(config, model_class):
    """Filter models by their class type."""
    return [name for name, cfg in config.items() if cfg.get("class") == model_class]


def print_summary(results):
    """Print a summary of the run results."""
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    successful = sum(1 for r in results if r[1])
    failed = sum(1 for r in results if not r[1])
    total_time = sum(r[2] for r in results)

    print(f"\nTotal models: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total time: {total_time:.2f}s")

    if failed > 0:
        print("\nFailed models:")
        for r in results:
            if not r[1]:
                print(f"  - {r[0]}: {r[3]}")

    # Sort by duration and show top 5 slowest
    sorted_results = sorted(results, key=lambda x: x[2], reverse=True)
    print("\nTop 5 slowest models:")
    for r in sorted_results[:5]:
        print(f"  - {r[0]}: {r[2]:.2f}s")


def save_results(results, output_file):
    """Save results to a JSON file."""
    results_data = {
        "timestamp": datetime.now().isoformat(),
        "results": [
            {"model": r[0], "success": r[1], "duration": r[2], "error": r[3]}
            for r in results
        ],
    }

    with open(output_file, "w") as f:
        json.dump(results_data, f, indent=2)

    print(f"\nResults saved to: {output_file}")


def list_available_models(config):
    """List all available models grouped by class."""
    print("\nAvailable models:")
    print("-" * 40)

    # Group by class
    by_class = {}
    for name, cfg in config.items():
        class_name = cfg.get("class", "Unknown")
        if class_name not in by_class:
            by_class[class_name] = []
        by_class[class_name].append(name)

    # Print grouped
    for class_name in sorted(by_class.keys()):
        print(f"\n{class_name}:")
        for model in sorted(by_class[class_name]):
            print(f"  - {model}")


def main():

    log_path = Path(__file__).resolve().parent / "model_logs" / "model_controller_logs" / strftime("%d%b%Y-%H:%M:%S")
    try:
        Path(log_path).mkdir(parents = True, exist_ok = True)
    except:
        pass
    logging.basicConfig(level = logging.DEBUG)

    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Controller for running multiple forecasting models"
    )

    # Model selection arguments
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Run all available models")
    group.add_argument(
        "--models", nargs="+", help="Run specific models (space-separated list)"
    )
    group.add_argument(
        "--class-name",
        choices=["DartsLocal", "DartsGlobal", "NixtlaMain", "GluontsMain", "TimesFM"],
        help="Run all models of a specific class",
    )
    group.add_argument("--list", action="store_true", help="List all available models")

    # Execution options
    parser.add_argument(
        "--parallel", action="store_true", help="Run models in parallel"
    )
    parser.add_argument(
        "--workers", type=int, help="Number of parallel workers (default: CPU count)"
    )

    # Other options
    parser.add_argument(
        "--config", default="models_config.toml", help="Path to configuration file"
    )
    parser.add_argument("--save-results", help="Save results to JSON file")
    parser.add_argument(
        "--workflow",
        choices=["main", "train", "inference", "evaluate"],
        default="main",
        help="Which workflow to run (default: main)",
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Handle list command
    if args.list:
        list_available_models(config)
        return

    # Determine which models to run
    if args.all:
        models = list(config.keys())
    elif args.models:
        # Validate model names
        invalid = [m for m in args.models if m not in config]
        if invalid:
            print(f"Error: Unknown models: {', '.join(invalid)}")
            list_available_models(config)
            return
        models = args.models
    elif args.class_name:
        models = filter_models_by_class(config, args.class_name)
        if not models:
            print(f"No models found for class: {args.class_name}")
            return

    # Run models
    start_time = datetime.now()

    if args.parallel:
        results = run_models_parallel(models, args.config, args.workflow, args.workers, log_path)
    else:
        results = run_models_sequential(models, args.config, args.workflow, log_path)

    total_duration = (datetime.now() - start_time).total_seconds()

    # Print summary
    print_summary(results)
    print(f"\nTotal execution time: {total_duration:.2f}s")

    # Save results if requested
    if args.save_results:
        save_results(results, args.save_results)


if __name__ == "__main__":
    main()
