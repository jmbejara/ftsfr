"""DoIt tasks for generating and running forecasting jobs."""

from pathlib import Path
import shlex

from dodo_common import OUTPUT_DIR, debug_action


def task_generate_forecasting_jobs():
    """Generate the forecasting_jobs.txt file used by SLURM submission."""

    jobs_file = Path("src/forecasting/forecasting_jobs.txt")

    return {
        "actions": [
            (debug_action, ["python src/forecasting/generate_forecasting_jobs.py --skip-existing"])
        ],
        "file_dep": [
            "src/forecasting/generate_forecasting_jobs.py",
            "src/forecasting/models_config.toml",
            "datasets.toml",
            OUTPUT_DIR / "available_datasets.csv",
        ],
        "targets": [
            str(jobs_file)
        ],
        "clean": True,
        "verbosity": 2,
    }


def task_run_forecasting_jobs():
    """Run each forecasting job listed in src/forecasting/forecasting_jobs.txt."""

    jobs_file = Path("src/forecasting/forecasting_jobs.txt")

    try:
        commands = [line.strip() for line in jobs_file.read_text().splitlines() if line.strip()]
    except FileNotFoundError:
        commands = []

    for command in commands:
        parts = shlex.split(command)
        if len(parts) < 2:
            continue

        script_path = Path(parts[1]).resolve()

        dataset = None
        model = None
        if "--dataset" in parts:
            dataset = parts[parts.index("--dataset") + 1]
        if "--model" in parts:
            model = parts[parts.index("--model") + 1]

        task_name = f"{dataset or 'unknown_dataset'}:{model or 'unknown_model'}"

        targets = []
        if dataset and model:
            targets.append(OUTPUT_DIR / "forecasting" / "error_metrics" / dataset / f"{model}.csv")

        yield {
            "name": task_name,
            "actions": [
                (debug_action, [command])
            ],
            "file_dep": [str(jobs_file), str(script_path)],
            "task_dep": ["generate_forecasting_jobs"],
            "targets": [str(path) for path in targets],
            "clean": True,
            "verbosity": 2,
        }
