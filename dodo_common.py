"""
Common utilities and configuration shared across all dodo files.
"""

import sys
import os
from pathlib import Path
import shutil
import tomli
import subprocess
import time
import re
import pandas as pd

sys.path.insert(1, str((Path(__file__).parent / "src").resolve()))

from settings import config


# --------------------------------------------------------------------
# Safer file copy/move behavior for Windows/corporate shares
# --------------------------------------------------------------------
# Disable metadata copying that can fail on network drives
def _noop(*_args, **_kwargs):
    pass


shutil.copymode = _noop  # used by shutil.copy
shutil.copystat = _noop  # used by shutil.copy2 / copytree
shutil.copy2 = shutil.copy  # make copy2 behave like copy (no metadata)


def _python_copy_file_command(source_path: Path, destination_path: Path) -> str:
    """Return a Python command string that safely copies a single file.

    Uses shutil.copyfile (content only) and creates the destination parent directory.
    """
    src = str(Path(source_path))
    dst = str(Path(destination_path))
    return (
        'python -c "import shutil, os; from pathlib import Path; '
        f"src=r'{src}'; dst=r'{dst}'; "
        "Path(dst).parent.mkdir(parents=True, exist_ok=True); "
        'shutil.copyfile(src, dst)"'
    )


def _python_move_file_command(source_path: Path, destination_path: Path) -> str:
    """Return a Python command string that safely moves a single file.

    Ensures the destination directory exists, then uses shutil.move.
    shutil.move will internally copy (using our patched behavior) if needed.
    """
    src = str(Path(source_path))
    dst = str(Path(destination_path))
    return (
        'python -c "import shutil; from pathlib import Path; '
        f"src=r'{src}'; dst=r'{dst}'; "
        "Path(dst).parent.mkdir(parents=True, exist_ok=True); "
        'shutil.move(src, dst)"'
    )


def _python_copy_tree_command(dir_path: Path, destination_folder: Path) -> str:
    """Return a Python command string that safely copies all contents of a directory.

    Recursively creates directories and copies files using shutil.copyfile.
    """
    src = str(Path(dir_path))
    dst = str(Path(destination_folder))
    code = (
        "import os, shutil; from pathlib import Path; "
        f"src=r'{src}'; dst=r'{dst}'; "
        "Path(dst).mkdir(parents=True, exist_ok=True); "
        "\nfor root, dirs, files in os.walk(src):\n"
        "    rel = os.path.relpath(root, src)\n"
        "    target = os.path.join(dst, rel)\n"
        "    os.makedirs(target, exist_ok=True)\n"
        "    for f in files:\n"
        "        shutil.copyfile(os.path.join(root, f), os.path.join(target, f))\n"
    )
    return f'python -c "{code}"'


# Ensure child processes (spawned by tasks) can import modules from `src/`
_src_path = str((Path(__file__).parent / "src").resolve())
os.environ["PYTHONPATH"] = _src_path + (
    os.pathsep + os.environ.get("PYTHONPATH", "")
    if os.environ.get("PYTHONPATH")
    else ""
)


# Common configuration
BASE_DIR = Path(config("BASE_DIR"))
DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))
OS_TYPE = config("OS_TYPE")


# Get pixi executable path
PIXI_EXECUTABLE = shutil.which("pixi")
if not PIXI_EXECUTABLE:
    # Fallback to common installation paths
    if Path.home().joinpath(".pixi/bin/pixi").exists():
        PIXI_EXECUTABLE = str(Path.home() / ".pixi/bin/pixi")
    else:
        PIXI_EXECUTABLE = "pixi"  # Hope it's in PATH at runtime


def debug_action(cmd):
    """Action function that prints command before executing"""
    print(f"\n🔍 DEBUG: About to execute: {cmd}")
    print("=" * 60)

    # Start timing
    start_time = time.time()
    result = subprocess.run(cmd, shell=True)
    end_time = time.time()
    wall_time_seconds = end_time - start_time

    # Extract model name and dataset path from command for timing CSV
    if result.returncode == 0 and "python models/run_model.py" in cmd:
        try:
            # Parse command to extract model name and dataset path
            match = re.search(r"--model (\w+)", cmd)
            model_name = match.group(1) if match else "unknown"

            match = re.search(r"--dataset-path ([^\s]+)", cmd)
            dataset_path = match.group(1) if match else "unknown"

            # Extract dataset name from path (remove ftsfr_ prefix and file extension)
            dataset_name = Path(dataset_path).stem.replace("ftsfr_", "")

            # Create timing directory and file
            timing_dir = OUTPUT_DIR / "forecasting" / "timing" / model_name
            timing_dir.mkdir(parents=True, exist_ok=True)
            timing_file = timing_dir / f"{dataset_name}_timing.csv"

            # Create timing data
            timing_data = pd.DataFrame(
                {
                    "Model": [model_name],
                    "Dataset": [dataset_name],
                    "Wall_Time_Seconds": [wall_time_seconds],
                }
            )

            # Save timing CSV
            timing_data.to_csv(timing_file, index=False)
            print(f"⏱️  Execution time: {wall_time_seconds:.2f} seconds")
            print(f"📊 Timing saved to: {timing_file}")

        except Exception as e:
            print(f"⚠️  Warning: Could not save timing data: {e}")

    return result.returncode == 0


# Helper functions for handling Jupyter Notebook tasks
def jupyter_execute_notebook(notebook_path):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --inplace {notebook_path}"


def jupyter_to_html(notebook_path, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --output-dir={output_dir} {notebook_path}"


def jupyter_to_md(notebook_path, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --output-dir={output_dir} {notebook_path}"


def jupyter_to_python(notebook_path, notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --to python {notebook_path} --output _{notebook}.py --output-dir {build_dir}"


def jupyter_clear_output(notebook_path):
    """Clear the output of a notebook"""
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace {notebook_path}"


def mv(from_path, to_path):
    """Copy a notebook to a folder"""
    from_path = Path(from_path)
    to_path = Path(to_path)
    to_path.mkdir(parents=True, exist_ok=True)
    return _python_move_file_command(from_path, to_path / from_path.name)


def copy_dir_contents_to_folder(dir_path, destination_folder):
    """Copy a directory to a folder"""
    dir_path = Path(dir_path)
    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    return _python_copy_tree_command(dir_path, destination_folder)


# --------------------------------------------------------------------
# Dataset dependency tracking utilities
# --------------------------------------------------------------------


def load_module_requirements(datasets_toml_path="datasets.toml"):
    """Load module requirements from datasets.toml."""
    with open(datasets_toml_path, "rb") as f:
        datasets_config = tomli.load(f)

    module_requirements = {}

    for module_name, module_config in datasets_config.items():
        if isinstance(module_config, dict) and "required_data_sources" in module_config:
            module_requirements[module_name] = module_config["required_data_sources"]

    return module_requirements


def check_module_availability(module_requirements, data_sources):
    """Return availability map for modules based on available data sources."""
    module_availability = {}

    for module_name, required_sources in module_requirements.items():
        module_availability[module_name] = all(
            data_sources.get(source, False) for source in required_sources
        )

    return module_availability


def get_missing_sources(module_name, module_requirements, data_sources):
    """Return missing data sources for a given module."""
    if module_name not in module_requirements:
        return []

    required = module_requirements[module_name]
    return [source for source in required if not data_sources.get(source, False)]


def get_available_datasets(
    module_requirements, data_dir, datasets_toml_path="datasets.toml"
):
    """Return dataset metadata for modules that have all prerequisites satisfied."""
    with open(datasets_toml_path, "rb") as f:
        datasets_config = tomli.load(f)

    available_datasets = {}

    for module_name, is_available in module_requirements.items():
        if not is_available:
            continue

        if module_name in datasets_config and isinstance(datasets_config[module_name], dict):
            module_config = datasets_config[module_name]

            for key, value in module_config.items():
                if (
                    key.startswith("ftsfr_")
                    and isinstance(value, dict)
                    and "description" in value
                ):
                    dataset_name = key.replace("ftsfr_", "")

                    available_datasets[dataset_name] = {
                        "path": Path(data_dir) / "formatted" / module_name / f"{key}.parquet",
                        "module": module_name,
                        "frequency": value.get("frequency", "D"),
                        "seasonality": value.get("seasonality"),
                        "is_balanced": value.get("is_balanced", False),
                        "description": value.get("description", ""),
                    }

    return available_datasets


def get_format_task_name(module_name):
    """Return the doit task name that formats a given module's dataset."""
    task_name_mapping = {
        "cds_returns": "calc_cds_returns",
    }

    return task_name_mapping.get(module_name, module_name)


def get_docs_task_dependencies(module_requirements):
    """Return documentation task dependencies for available modules."""
    docs_task_by_module = {
        "cds_bond_basis": "format:summary_cds_bond_basis_ipynb",
        "cds_returns": "format:summary_cds_returns_ipynb",
        "cip": "format:summary_cip_ipynb",
        "corp_bond_returns": "format:summary_corp_bond_returns_ipynb",
        "us_treasury_returns": "format:summary_treasury_bond_returns_ipynb",
        "basis_tips_treas": "format:summary_basis_tips_treas_ipynb",
        "basis_treas_sf": "format:summary_basis_treas_sf_ipynb",
        "basis_treas_swap": "format:summary_basis_treas_swap_ipynb",
    }

    return [
        task_name
        for module_name, task_name in docs_task_by_module.items()
        if module_requirements.get(module_name, False)
    ]


def notebook_subtask(task_config):
    """
    Generate notebook task configuration with unified workflow for .py and .ipynb files.

    Creates a two-stage process:
    1. Normalize: Convert source to stable .py file in OUTPUT_DIR
    2. Execute & Render: Run .py, convert to notebook, execute, generate HTML

    Parameters:
    - task_config: dict with keys:
        - name: str, task name
        - notebook_path: str, path to .py or .ipynb file
        - file_dep: list, additional file dependencies (optional)
        - targets: list, additional targets (optional)

    Yields task configuration(s) for doit.
    """
    name = task_config["name"]
    source_path = Path(task_config["notebook_path"])
    file_dep = task_config.get("file_dep", [])
    targets = task_config.get("targets", [])

    # Intermediate .py file in OUTPUT_DIR
    py_filename = f"_{name}_ipynb.py"
    py_path = OUTPUT_DIR / py_filename

    # Stage 1: Normalize to .py in OUTPUT_DIR
    # Create the normalize action based on file type
    if source_path.suffix == ".py":
        normalize_actions = [
            f"mkdir -p {OUTPUT_DIR}"
            if OS_TYPE == "nix"
            else f"mkdir {OUTPUT_DIR} 2>nul || echo.",
            _python_copy_file_command(source_path, py_path),
        ]
    elif source_path.suffix == ".ipynb":
        normalize_actions = [
            f"mkdir -p {OUTPUT_DIR}"
            if OS_TYPE == "nix"
            else f"mkdir {OUTPUT_DIR} 2>nul || echo.",
            f"jupyter nbconvert --to python --output {py_path} {source_path}",
        ]
    else:
        raise ValueError(
            f"Unsupported file type: {source_path.suffix}. Must be .py or .ipynb"
        )

    yield {
        "name": f"{name}_normalize",
        "actions": normalize_actions,
        "file_dep": [str(source_path)],
        "targets": [str(py_path)],
        "clean": True,
    }

    # Stage 2: Execute and render
    # Work in the source directory to preserve relative paths
    working_notebook = source_path.with_suffix(".ipynb")

    # Determine whether to move or copy based on source file type
    if source_path.suffix == ".py":
        # For .py sources, the .ipynb is intermediate, so move it
        notebook_transfer_cmd = mv(working_notebook, OUTPUT_DIR / "_notebook_build")
    else:
        # For .ipynb sources, preserve the original by copying
        notebook_transfer_cmd = _python_copy_file_command(
            working_notebook, OUTPUT_DIR / "_notebook_build" / working_notebook.name
        )

    # For .py sources, clear outputs before moving; for .ipynb sources, after copying
    clear_output_action = (
        jupyter_clear_output(working_notebook)
        if source_path.suffix == ".ipynb"
        else "echo 'Skipping output clear for .py source'"
    )

    yield {
        "name": name,
        "actions": [
            f"""python -c "import sys; from datetime import datetime; print(f'Start {name}: {{datetime.now()}}', file=sys.stderr)" """,
            # Ensure output directories exist
            f"mkdir -p {OUTPUT_DIR / '_notebook_build'}"
            if OS_TYPE == "nix"
            else f"mkdir {OUTPUT_DIR / '_notebook_build'} 2>nul || echo.",
            # Convert source to notebook format (in source directory)
            f"ipynb-py-convert {source_path} {working_notebook}"
            if source_path.suffix == ".py"
            else "echo 'Using existing notebook'",
            # Execute notebook in its original directory (preserves relative paths)
            jupyter_execute_notebook(working_notebook),
            # Generate HTML
            jupyter_to_html(working_notebook, OUTPUT_DIR),
            # Move or copy executed notebook to build directory based on source type
            notebook_transfer_cmd,
            # Clear outputs to prevent constant re-runs (only for .ipynb sources)
            clear_output_action,
            f"""python -c "import sys; from datetime import datetime; print(f'End {name}: {{datetime.now()}}', file=sys.stderr)" """,
        ],
        "file_dep": [
            str(py_path),  # Depend on normalized .py for stability
            *file_dep,
        ],
        "targets": [
            OUTPUT_DIR / f"{name}.html",
            OUTPUT_DIR / "_notebook_build" / f"{name}.ipynb",
            *targets,
        ],
        "clean": True,
    }


# Load configuration from subscriptions.toml
def load_subscriptions():
    with open("subscriptions.toml", "rb") as f:
        return tomli.load(f)


# Load module requirements from datasets.toml
def load_all_module_requirements():
    return load_module_requirements()


# Forecasting-specific utilities
def load_models_config(config_path="forecasting/models_config.toml"):
    """Load the models configuration from TOML file."""
    with open(config_path, "rb") as f:
        return tomli.load(f)


def setup_module_requirements():
    """Set up module requirements based on subscriptions configuration."""
    subscriptions_toml = load_subscriptions()
    module_requirements_dict = load_all_module_requirements()
    module_requirements = {}
    for module_name, required_sources in module_requirements_dict.items():
        module_requirements[module_name] = all(
            subscriptions_toml["data_sources"].get(source, False)
            for source in required_sources
        )
    return module_requirements, subscriptions_toml


def check_required_files(module_requirements):
    """Check if required data files exist before running forecasts"""
    available_datasets = get_available_datasets(module_requirements, DATA_DIR)

    missing_files = []
    for dataset_name, dataset_info in available_datasets.items():
        if not dataset_info["path"].exists():
            missing_files.append(str(dataset_info["path"]))

    if missing_files:
        print("\nWarning: The following required data files are missing:")
        for f in missing_files:
            print(f"  - {f}")
        print("\nPlease run 'doit -f dodo_01_pull.py' first to generate these files.")
        print("Continuing anyway...\n")
