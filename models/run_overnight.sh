#!/bin/bash

# run_overnight.sh
# 
# A simple wrapper script to run all models on all datasets overnight.
# This script sets up the environment and runs the batch script with
# sensible defaults for overnight execution.
#
# Usage:
#   ./run_overnight.sh
#   ./run_overnight.sh --parallel --workers 4
#   ./run_overnight.sh --models arima transformer

set -e  # Exit on any error

# Default values
PARALLEL=false
WORKERS=""
MODELS=""
DATASETS=""
SAVE_RESULTS="overnight_results_$(date +%Y%m%d_%H%M%S).json"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --parallel)
            PARALLEL=true
            shift
            ;;
        --workers)
            WORKERS="--workers $2"
            shift 2
            ;;
        --models)
            MODELS="--models $2"
            shift 2
            ;;
        --datasets)
            DATASETS="--datasets $2"
            shift 2
            ;;
        --save-results)
            SAVE_RESULTS="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--parallel] [--workers N] [--models model1 model2] [--datasets dataset1 dataset2] [--save-results filename]"
            exit 1
            ;;
    esac
done

echo "=========================================="
echo "Starting overnight model run"
echo "=========================================="
echo "Timestamp: $(date)"
echo "Parallel: $PARALLEL"
if [ ! -z "$WORKERS" ]; then
    echo "Workers: $WORKERS"
fi
if [ ! -z "$MODELS" ]; then
    echo "Models: $MODELS"
fi
if [ ! -z "$DATASETS" ]; then
    echo "Datasets: $DATASETS"
fi
echo "Results will be saved to: $SAVE_RESULTS"
echo "=========================================="

# Change to the models directory
cd "$(dirname "$0")"

# Check if we're in the right directory
if [ ! -f "run_all_models_all_datasets.py" ]; then
    echo "Error: run_all_models_all_datasets.py not found in current directory"
    exit 1
fi

# Build the command
CMD="python run_all_models_all_datasets.py --save-results $SAVE_RESULTS"

if [ "$PARALLEL" = true ]; then
    CMD="$CMD --parallel"
fi

if [ ! -z "$WORKERS" ]; then
    CMD="$CMD $WORKERS"
fi

if [ ! -z "$MODELS" ]; then
    CMD="$CMD $MODELS"
fi

if [ ! -z "$DATASETS" ]; then
    CMD="$CMD $DATASETS"
fi

echo "Executing: $CMD"
echo "=========================================="

# Run the command
start_time=$(date +%s)
$CMD
end_time=$(date +%s)

duration=$((end_time - start_time))
hours=$((duration / 3600))
minutes=$(((duration % 3600) / 60))
seconds=$((duration % 60))

echo "=========================================="
echo "Overnight run completed!"
echo "End time: $(date)"
echo "Total duration: ${hours}h ${minutes}m ${seconds}s"
echo "Results saved to: $SAVE_RESULTS"
echo "=========================================="
