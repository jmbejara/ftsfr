#!/bin/bash
#SBATCH --job-name=forecast_parallel
#SBATCH --nodes=20
#SBATCH --exclusive
#SBATCH --time=7-00:00:00
#SBATCH --output=./_output/forecasting/logs/slurm-%j.out
#SBATCH --error=./_output/forecasting/logs/slurm-%j.err

SECONDS=0

echo "Job started at: $(date)"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Nodes allocated: ${SLURM_NODELIST}"
echo "CPUs per node: ${SLURM_CPUS_ON_NODE}"

declare -r OUTPUT_ROOT="./_output/forecasting"
declare -r LOG_ROOT="${OUTPUT_ROOT}/logs"
declare -r JOBS_FILE="./src/forecasting/forecasting_jobs.txt"
declare -r PARALLEL_JOBLOG="${LOG_ROOT}/parallel_joblog.txt"

mkdir -p "${LOG_ROOT}/failed" "${OUTPUT_ROOT}/error_metrics"
touch "${LOG_ROOT}/successful_jobs.txt" "${LOG_ROOT}/failed_jobs.txt" "${LOG_ROOT}/warnings.txt" "${PARALLEL_JOBLOG}"

if [ ! -f "${JOBS_FILE}" ]; then
    echo "ERROR: Jobs file not found: ${JOBS_FILE}"
    exit 1
fi

mapfile -t JOB_COMMANDS < "${JOBS_FILE}"
if [ ${#JOB_COMMANDS[@]} -eq 0 ]; then
    echo "No jobs found in ${JOBS_FILE}. Nothing to do."
    exit 0
fi

if [ -n "${SLURM_CPUS_ON_NODE:-}" ]; then
    export STATSFORECAST_N_JOBS=${SLURM_CPUS_ON_NODE}
else
    export STATSFORECAST_N_JOBS=$(nproc --all 2>/dev/null || echo 1)
fi

echo "Using ${STATSFORECAST_N_JOBS} CPUs per node for StatsForecast"

if [ -n "${SLURM_CPUS_ON_NODE:-}" ] && [ -n "${SLURM_NNODES:-}" ]; then
    PARALLEL_MAX_JOBS=$((SLURM_CPUS_ON_NODE * SLURM_NNODES))
else
    PARALLEL_MAX_JOBS=0
fi

echo "Configuring GNU parallel with max jobs: ${PARALLEL_MAX_JOBS:-auto}"

module use -a /opt/aws_ofropt/Ubuntu_Modulefiles
module load anaconda3/3.11.4 TeXLive/2023 R/4.4.0 stata/17 parallel

export OUTPUT_ROOT LOG_ROOT
export SHELL=/bin/bash

run_forecasting_job() {
    local JOB_CMD="$1"

    if [ -z "${JOB_CMD}" ]; then
        echo "[$(date)] Skipping empty job definition"
        return 0
    fi

    local DATASET
    local MODEL
    DATASET=$(echo "${JOB_CMD}" | sed -n 's/.*--dataset \([^ ]*\).*/\1/p')
    MODEL=$(echo "${JOB_CMD}" | sed -n 's/.*--model \([^ ]*\).*/\1/p')

    if [ -z "${DATASET}" ] || [ -z "${MODEL}" ]; then
        local MSG="[$(date)] ERROR: Could not parse dataset/model from command: ${JOB_CMD}"
        echo "${MSG}" | tee -a "${LOG_ROOT}/warnings.txt"
        echo "${MSG}" >> "${LOG_ROOT}/failed_jobs.txt"
        return 1
    fi

    local DATASET_DIR="${OUTPUT_ROOT}/error_metrics/${DATASET}"
    local MODEL_LOG_DIR="${LOG_ROOT}/${DATASET}/${MODEL}"
    local OUTPUT_FILE="${DATASET_DIR}/${MODEL}.csv"

    if [ -f "${OUTPUT_FILE}" ]; then
        echo "[$(date)] Output already exists for ${DATASET}/${MODEL}; skipping"
        return 0
    fi

    mkdir -p "${DATASET_DIR}" "${MODEL_LOG_DIR}"

    echo "[$(date)] Starting ${DATASET}/${MODEL}"
    echo "[$(date)] Command: ${JOB_CMD}" > "${MODEL_LOG_DIR}/output.log"

    eval "${JOB_CMD}" >> "${MODEL_LOG_DIR}/output.log" 2>&1
    local EXIT_CODE=$?

    if [ ${EXIT_CODE} -ne 0 ]; then
        local FAIL_MSG="[$(date)] ERROR: ${DATASET}/${MODEL} failed with exit code ${EXIT_CODE}"
        echo "${FAIL_MSG}" | tee -a "${LOG_ROOT}/failed_jobs.txt"
        mkdir -p "${LOG_ROOT}/failed/${DATASET}"
        cp "${MODEL_LOG_DIR}/output.log" "${LOG_ROOT}/failed/${DATASET}/${MODEL}_failed.log" 2>/dev/null || true
    else
        if [ -f "${OUTPUT_FILE}" ]; then
            echo "[$(date)] SUCCESS: ${DATASET}/${MODEL}" | tee -a "${LOG_ROOT}/successful_jobs.txt"
        else
            local WARN_MSG="[$(date)] WARNING: ${DATASET}/${MODEL} completed but output missing (${OUTPUT_FILE})"
            echo "${WARN_MSG}" | tee -a "${LOG_ROOT}/warnings.txt"
            echo "${WARN_MSG}" >> "${LOG_ROOT}/failed_jobs.txt"
            mkdir -p "${LOG_ROOT}/failed/${DATASET}"
            cp "${MODEL_LOG_DIR}/output.log" "${LOG_ROOT}/failed/${DATASET}/${MODEL}_failed.log" 2>/dev/null || true
            EXIT_CODE=20
        fi
    fi

    echo "[$(date)] Finished ${DATASET}/${MODEL} (exit code: ${EXIT_CODE})"
    return ${EXIT_CODE}
}
export -f run_forecasting_job

echo "[$(date)] Launching GNU parallel"

PARALLEL_CMD=(parallel --will-cite --line-buffer --tag --keep-order --joblog "${PARALLEL_JOBLOG}" --resume --env run_forecasting_job --env OUTPUT_ROOT --env LOG_ROOT --env STATSFORECAST_N_JOBS)
if [ "${PARALLEL_MAX_JOBS}" -gt 0 ]; then
    PARALLEL_CMD+=(--jobs "${PARALLEL_MAX_JOBS}")
else
    PARALLEL_CMD+=(--jobs 0)
fi

printf '%s\0' "${JOB_COMMANDS[@]}" | "${PARALLEL_CMD[@]}" --null run_forecasting_job
PARALLEL_EXIT_CODE=$?

if [ ${PARALLEL_EXIT_CODE} -ne 0 ]; then
    echo "[$(date)] GNU parallel reported non-zero exit code: ${PARALLEL_EXIT_CODE}"
    echo "[$(date)] Review ${PARALLEL_JOBLOG} and failed_jobs.txt for details"
else
    echo "[$(date)] GNU parallel completed successfully"
fi

echo "Job completed at: $(date)"
echo "Total runtime: ${SECONDS} seconds"

if command -v sstat &> /dev/null; then
    echo "Memory usage statistics:"
    sstat -j ${SLURM_JOB_ID} --format=JobID,MaxRSS,MaxVMSize,AveRSS 2>/dev/null || true
fi

exit ${PARALLEL_EXIT_CODE}
