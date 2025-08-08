"""
Common utilities and configuration shared across all dodo files.
"""

import sys
import os
from pathlib import Path
import shutil
import toml

sys.path.insert(1, str((Path(__file__).parent / "src").resolve()))

from settings import config
from dependency_tracker import (
    load_module_requirements,
)

# Ensure child processes (spawned by tasks) can import modules from `src/`
_src_path = str((Path(__file__).parent / "src").resolve())
os.environ["PYTHONPATH"] = (
    _src_path
    + (
        os.pathsep + os.environ.get("PYTHONPATH", "")
        if os.environ.get("PYTHONPATH")
        else ""
    )
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
    if OS_TYPE == "nix":
        command = f"mv {from_path} {to_path}"
    else:
        command = f"move {from_path} {to_path}"
    return command


def copy_dir_contents_to_folder(dir_path, destination_folder):
    """Copy a directory to a folder"""
    dir_path = Path(dir_path)
    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    if OS_TYPE == "nix":
        command = f"cp -r {dir_path}/ {destination_folder}"
    else:
        command = f"xcopy /E /I {dir_path}/ {destination_folder}"
    return command


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
            f"cp {source_path} {py_path}"
            if OS_TYPE == "nix"
            else f"copy {source_path} {py_path}",
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
        if OS_TYPE == "nix":
            notebook_transfer_cmd = (
                f"cp {working_notebook} {OUTPUT_DIR / '_notebook_build'}"
            )
        else:
            notebook_transfer_cmd = (
                f"copy {working_notebook} {OUTPUT_DIR / '_notebook_build'}"
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
    with open("subscriptions.toml", "r") as f:
        return toml.load(f)


# Load module requirements from datasets.toml
def load_all_module_requirements():
    return load_module_requirements()
