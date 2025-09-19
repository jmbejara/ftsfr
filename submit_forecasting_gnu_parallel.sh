#!/bin/bash
#SBATCH --job-name=forecast_parallel
#SBATCH --nodes=19
#SBATCH --exclusive
#SBATCH --time=7-00:00:00
#SBATCH --output=./_output/forecasting/logs/slurm-%j.out
#SBATCH --error=./_output/forecasting/logs/slurm-%j.err

SECONDS=0

echo "Job started at: $(date)"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Nodes allocated: ${SLURM_NODELIST}"
echo "CPUs per node: ${SLURM_CPUS_ON_NODE}"

OUTPUT_ROOT="./_output/forecasting"
LOG_ROOT="${OUTPUT_ROOT}/logs"
JOBS_FILE="./src/forecasting/forecasting_jobs.txt"
PARALLEL_JOBLOG="${LOG_ROOT}/parallel_joblog.txt"

mkdir -p "${LOG_ROOT}" "${OUTPUT_ROOT}/error_metrics"

if [ ! -f "${JOBS_FILE}" ]; then
    echo "ERROR: Jobs file not found: ${JOBS_FILE}"
    exit 1
fi

# Export CPU count for StatsForecast to use all cores on the node
export STATSFORECAST_N_JOBS=${SLURM_CPUS_ON_NODE:-$(nproc --all 2>/dev/null || echo 1)}
echo "Using ${STATSFORECAST_N_JOBS} CPUs per node for StatsForecast"

# Load required modules
module use -a /opt/aws_ofropt/Ubuntu_Modulefiles
module load anaconda3/3.11.4 R/4.4.0 parallel

# Activate conda/virtual environment if needed
# source /path/to/your/venv/bin/activate
# conda activate forecasting_env

echo "[$(date)] Launching GNU parallel with ${SLURM_NNODES:-19} parallel jobs (one per node)"

# Run parallel with one job per node, letting GNU parallel handle all the complexity
parallel --joblog "${PARALLEL_JOBLOG}" \
         --resume \
         --resume-failed \
         --jobs ${SLURM_NNODES:-19} \
         --results "${LOG_ROOT}/results/{#}/" \
         --line-buffer \
         --will-cite \
         --env STATSFORECAST_N_JOBS \
         :::: "${JOBS_FILE}"

PARALLEL_EXIT_CODE=$?

if [ ${PARALLEL_EXIT_CODE} -ne 0 ]; then
    echo "[$(date)] GNU parallel reported non-zero exit code: ${PARALLEL_EXIT_CODE}"
    echo "[$(date)] Review ${PARALLEL_JOBLOG} for details"
else
    echo "[$(date)] GNU parallel completed successfully"
fi

echo "Job completed at: $(date)"
echo "Total runtime: ${SECONDS} seconds"

# Use sacct for post-job memory statistics
if command -v sacct &> /dev/null; then
    echo "Memory usage statistics:"
    sacct -j ${SLURM_JOB_ID} --format=JobID,MaxRSS,MaxVMSize,AveRSS 2>/dev/null || true
fi

exit 0
