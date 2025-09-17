#!/bin/bash
#SBATCH --job-name=forecast_array
#SBATCH --array=1-300%9            # 300 jobs total, max 9 concurrent
#SBATCH --exclusive                 # Exclusive node access
#SBATCH --time=7-00:00:00          # 7 days time limit
#SBATCH --output=./_output/forecasting3/logs/slurm-%A_%a.out
#SBATCH --error=./_output/forecasting3/logs/slurm-%A_%a.err


# Print job information
echo "Job started at: $(date)"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Array Task ID: ${SLURM_ARRAY_TASK_ID}"
echo "Node: ${SLURM_NODELIST}"
echo "CPUs on node: ${SLURM_CPUS_ON_NODE}"

# Create base log directory if it doesn't exist
mkdir -p ./_output/forecasting3/logs

# Auto-detect and export CPU count for parallel processing
# This will be used by StatsForecast for parallel model fitting
export STATSFORECAST_N_JOBS=${SLURM_CPUS_ON_NODE}
echo "Using ${STATSFORECAST_N_JOBS} CPUs for parallel processing"

# Load required modules (adjust as needed for your cluster)
module use -a /opt/aws_ofropt/Ubuntu_Modulefiles
module load anaconda3/3.11.4 TeXLive/2023 R/4.4.0 stata/17

# Activate conda/virtual environment if needed
# source /path/to/your/venv/bin/activate
# conda activate forecasting_env

# Read the job command from the file based on array task ID
JOB_CMD=$(sed -n "${SLURM_ARRAY_TASK_ID}p" forecasting_jobs.txt)

# Check if we got a command
if [ -z "$JOB_CMD" ]; then
    echo "ERROR: No command found for task ID ${SLURM_ARRAY_TASK_ID}"
    exit 1
fi

# Extract dataset and model names from the command
# Format: python ./forecasting/forecast.py --dataset DATASET --model MODEL
DATASET=$(echo $JOB_CMD | sed -n 's/.*--dataset \([^ ]*\).*/\1/p')
MODEL=$(echo $JOB_CMD | sed -n 's/.*--model \([^ ]*\).*/\1/p')

if [ -z "$DATASET" ] || [ -z "$MODEL" ]; then
    echo "ERROR: Could not parse dataset or model from command: $JOB_CMD"
    exit 1
fi

echo "Dataset: $DATASET"
echo "Model: $MODEL"

# Check if output already exists (idempotent execution)
OUTPUT_FILE="./_output/forecasting3/error_metrics/${DATASET}/${MODEL}.csv"
if [ -f "$OUTPUT_FILE" ]; then
    echo "Output already exists: $OUTPUT_FILE"
    echo "Skipping job for ${DATASET}/${MODEL} as it has already been completed"
    echo "Job skipped at: $(date)"
    exit 0
fi

# Create output directories
mkdir -p "./_output/forecasting3/error_metrics/${DATASET}"
mkdir -p "./_output/forecasting3/logs/${DATASET}/${MODEL}"

# Log start of actual computation
echo "Starting forecast computation at: $(date)"
echo "Running command: $JOB_CMD"

# Run the forecasting job
# Redirect model-specific output to dataset/model directory
$JOB_CMD > "./_output/forecasting3/logs/${DATASET}/${MODEL}/output.log" 2>&1
EXIT_CODE=$?

# Check exit status
if [ $EXIT_CODE -ne 0 ]; then
    echo "ERROR: Job failed with exit code $EXIT_CODE for ${DATASET}/${MODEL}"
    echo "$(date) - Failed: ${DATASET}/${MODEL} (Exit code: $EXIT_CODE)" >> ./_output/forecasting3/logs/failed_jobs.txt
    
    # Copy error details to failed jobs directory
    mkdir -p "./_output/forecasting3/logs/failed/${DATASET}"
    cp "./_output/forecasting3/logs/${DATASET}/${MODEL}/output.log" \
       "./_output/forecasting3/logs/failed/${DATASET}/${MODEL}_failed.log" 2>/dev/null || true
    
    # Still exit with 0 to allow array to continue
    echo "Job failed but array continues"
    echo "Job ended at: $(date)"
    exit 0
else
    echo "SUCCESS: Job completed successfully for ${DATASET}/${MODEL}"
    echo "$(date) - Success: ${DATASET}/${MODEL}" >> ./_output/forecasting3/logs/successful_jobs.txt
fi

# Check if output was actually created
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "WARNING: Job reported success but output file not found: $OUTPUT_FILE"
    echo "$(date) - Warning: ${DATASET}/${MODEL} - No output file created" >> ./_output/forecasting3/logs/warnings.txt
fi

echo "Job completed at: $(date)"
echo "Total runtime: ${SECONDS} seconds"

# Print memory usage if available
if command -v sstat &> /dev/null; then
    echo "Memory usage statistics:"
    sstat -j ${SLURM_JOB_ID}.${SLURM_ARRAY_TASK_ID} --format=JobID,MaxRSS,MaxVMSize,AveRSS 2>/dev/null || true
fi

exit 0