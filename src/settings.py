"""Load project configurations from .env files or from the command line.

Provides easy access to paths and credentials used in the project.
Meant to be used as an imported module.

If `settings.py` is run on its own, it will create the appropriate
directories.

For information about the rationale behind decouple and this module,
see https://pypi.org/project/python-decouple/

Note that decouple mentions that it will help to ensure that
the project has "only one configuration module to rule all your instances."
This is achieved by putting all the configuration into the `.env` file.
You can have different sets of variables for difference instances,
such as `.env.development` or `.env.production`. You would only
need to copy over the settings from one into `.env` to switch
over to the other configuration, for example.


Example
-------
Create a file called `myexample.py` with the following content:
```
from settings import config
DATA_DIR = config("DATA_DIR")

print(f"Using DATA_DIR: {DATA_DIR}")
```
and run
```
>>> python myexample.py --DATA_DIR=/path/to/data
/path/to/data
```
and compare to
```
>>> export DATA_DIR=/path/to/other
>>> python myexample.py
/path/to/other
```

"""

import os
import sys
import warnings
from pathlib import Path
from platform import system

from decouple import Config, RepositoryEnv, undefined
from decouple import config as _config_decouple


def find_project_root():
    """Find the project root directory using environment variables or marker files.

    The function determines the project root directory based on the following
    order of precedence:

    1.  Checks for the `BASE_DIR` environment variable. If set, its value is
        returned as the project root path.
    2.  If `BASE_DIR` is not set, it searches upwards from the current working
        directory (`Path.cwd()`) for specific marker files or directories.
    3.  The search checks for the following markers in each parent directory,
        in this order:
        - `pyproject.toml` (file)
        - `.env` (file)
        - `requirements.txt` (file)
        - `.git` (directory)
        - `LICENSE` (file)
    4.  The directory containing the first marker found is returned as the
        project root.
    5.  If the search reaches the filesystem root without finding any marker,
        a warning is issued, and the current working directory is returned.

    Returns
    -------
    pathlib.Path
        The absolute path to the determined project root directory, or the
        current working directory if no root could be determined.

    Raises
    ------
    FileNotFoundError
        If the `BASE_DIR` environment variable is not set and no marker
        file/directory could be found by traversing up from the current
        working directory.
    """
    # 1. Check for BASE_DIR environment variable
    base_dir_env = os.environ.get("BASE_DIR")
    if base_dir_env:
        return Path(base_dir_env).resolve()

    # 2. Search upwards for markers
    original_cwd = Path.cwd().resolve()
    current_dir = original_cwd
    markers = [
        ("pyproject.toml", "file"),
        (".env", "file"),
        ("requirements.txt", "file"),
        (".git", "dir"),
        ("LICENSE", "file"),
    ]

    while True:
        for marker_name, marker_type in markers:
            marker_path = current_dir / marker_name
            found = False
            if marker_type == "file" and marker_path.is_file():
                found = True
            elif marker_type == "dir" and marker_path.is_dir():
                found = True

            if found:
                return current_dir

        # Move to parent directory
        parent_dir = current_dir.parent

        # Check if we have reached the root directory
        if parent_dir == current_dir:
            break

        current_dir = parent_dir

    # 5. If no marker found after reaching the root, issue warning and return cwd
    warning_message = (
        "Could not find project root marker. Set the BASE_DIR environment variable or ensure "
        f"one of the following markers exists in the root or parent directories: "
        f"{[m[0] for m in markers]}. Returning current working directory: {original_cwd}"
    )
    warnings.warn(warning_message, UserWarning)
    return original_cwd


def find_all_caps_cli_vars(argv=sys.argv):
    """Find all command line arguments that are all caps.

    Find all command line arguments that are all caps and defined
    with a long option, for example, --DATA_DIR or --MANUAL_DATA_DIR.
    When that option is found, the value of the option is returned.

    For example, if the command line is:
    ```
    python settings.py --DATA_DIR=/path/to/data --MANUAL_DATA_DIR=/path/to/manual_data
    ```
    Then the function will return:
    ```
    {'DATA_DIR': '/path/to/data', 'MANUAL_DATA_DIR': '/path/to/manual_data'}
    ```

    For example:
    ```
    >>> argv = [
        '/opt/homebrew/Caskroom/mambaforge/base/envs/ftsf/lib/python3.12/site-packages/ipykernel_launcher.py',
        '--f=/Users/jbejarano/Library/Jupyter/runtime/kernel-v37ea18e94713e364855d5610175b766ee99909eab.json',
        '--DATA_DIR=/path/to/data',
        '--MANUAL_DATA_DIR=/path/to/manual_data'
    ]
    >>> cli_vars = find_all_caps_cli_vars(argv)
    >>> cli_vars
    {'DATA_DIR': '/path/to/data', 'MANUAL_DATA_DIR': '/path/to/manual_data'}
    ```
    """
    result = {}
    i = 0
    while i < len(argv):
        arg = argv[i]
        # Handle --VAR=value format
        if arg.startswith("--") and "=" in arg and arg[2:].split("=")[0].isupper():
            var_name, value = arg[2:].split("=", 1)
            result[var_name] = value
        # Handle --VAR value format (where value is the next argument)
        elif arg.startswith("--") and arg[2:].isupper() and i + 1 < len(argv):
            var_name = arg[2:]
            value = argv[i + 1]
            # Only use this value if it doesn't look like another option
            if not value.startswith("--"):
                result[var_name] = value
                i += 1  # Skip the next argument since we used it as a value
        i += 1
    return result


def load_subscriptions():
    # candidate paths: ./env then ../.env, then ../../.env
    estimated_project_root = find_project_root()
    candidates = [
        Path.cwd() / ".env",
        estimated_project_root / ".env",
    ]
    env_file = next((p for p in candidates if p.is_file()), None)
    if not env_file:
        warning_message = f"No .env found in {candidates}."
        warnings.warn(warning_message, UserWarning)
        return _config_decouple
    return Config(repository=RepositoryEnv(str(env_file)))


def if_relative_make_abs(path):
    """If a relative path is given, make it absolute, assuming
    that it is relative to the project root directory (BASE_DIR)

    Example
    -------
    ```
    >>> if_relative_make_abs(Path('_data'))
    WindowsPath('C:/Users/jdoe/GitRepositories/blank_project/_data')

    >>> if_relative_make_abs(Path("C:/Users/jdoe/GitRepositories/blank_project/_output"))
    WindowsPath('C:/Users/jdoe/GitRepositories/blank_project/_output')
    ```
    """
    path = Path(path)
    if path.is_absolute():
        abs_path = path.resolve()
    else:
        abs_path = (defaults["BASE_DIR"] / path).resolve()
    return abs_path


########################################################
## Define defaults
########################################################
cli_vars = find_all_caps_cli_vars()
_config = load_subscriptions()
defaults = {}


# OS type
def get_os():
    os_name = system()
    if os_name == "Windows":
        return "windows"
    elif os_name == "Darwin" or os_name == "Linux":
        return "nix"
    else:
        return "unknown"


if "OS_TYPE" in cli_vars:
    defaults["OS_TYPE"] = cli_vars["OS_TYPE"]
else:
    defaults["OS_TYPE"] = get_os()


# Absolute path to root directory of the project
if "BASE_DIR" in cli_vars:
    defaults["BASE_DIR"] = Path(cli_vars["BASE_DIR"])
else:
    defaults["BASE_DIR"] = find_project_root()

# User name
if defaults["OS_TYPE"] == "windows":
    USERPROFILE = os.environ["USERPROFILE"]
    USER = Path(USERPROFILE).name
elif defaults["OS_TYPE"] == "nix":
    USER = _config("USER", default="")
else:
    raise ValueError(f"Unsupported OS type: {defaults['OS_TYPE']}")

# Org Stuff
defaults["USER"] = USER
defaults["DATA_DIR"] = if_relative_make_abs(
    _config("DATA_DIR", default=Path("_data"), cast=Path)
)


## Stata executable
def get_stata_exe():
    """Get the name of the Stata executable based on the OS type."""
    if defaults["OS_TYPE"] == "windows":
        return "StataMP-64.exe"
    elif defaults["OS_TYPE"] == "nix":
        return "stata-mp"
    else:
        raise ValueError("Unknown OS type")


if "STATA_EXE" in cli_vars:
    defaults["STATA_EXE"] = cli_vars["STATA_EXE"]
else:
    defaults["STATA_EXE"] = get_stata_exe()


## File paths
defaults = {
    "DATA_DIR": if_relative_make_abs(Path("_data")),
    "MANUAL_DATA_DIR": if_relative_make_abs(Path("data_manual")),
    "OUTPUT_DIR": if_relative_make_abs(Path("_output")),
    "DOCS_BUILD_DIR": if_relative_make_abs(Path("_docs")),
    **defaults,
}


def config(
    var_name,
    default=undefined,
    cast=undefined,
    cli_vars=cli_vars,
    convert_dir_vars_to_abs_path=True,
):
    """Config defines a variable that can be used in the project. The definition of variables follows
    an order of precedence:
    1. Command line arguments
    2. Environment variables
    3. Settings.py file
    4. Defaults defined in-line in the local file
    5. Error
    """

    # 1. Command line arguments (highest priority)
    if var_name in cli_vars and cli_vars[var_name] is not None:
        value = cli_vars[var_name]
        # Apply cast if provided
        if cast is not undefined:
            value = cast(value)
        if "DIR" in var_name and convert_dir_vars_to_abs_path:
            value = if_relative_make_abs(Path(value))
        return value

    # 2. Environment variables through decouple
    # Use decouple but with a sentinel default to detect if it was found
    env_sentinel = object()
    env_value = _config(var_name, default=env_sentinel)
    if env_value is not env_sentinel:
        # Found in environment
        if cast is not undefined:
            env_value = cast(env_value)
        if "DIR" in var_name and convert_dir_vars_to_abs_path:
            env_value = if_relative_make_abs(Path(env_value))
        return env_value

    # 3. Settings.py defaults dictionary
    if var_name in defaults:
        default_value = defaults[var_name]
        # If default_value is directly usable (not a dict with metadata)
        if cast is not undefined:
            default_value = cast(default_value)
        return default_value

    # 4. Use the default value provided in the local file. Error if not found
    return _config(var_name, default=default, cast=cast)


def get_data_module_directories(path_to_src_dir=defaults["BASE_DIR"] / "src"):
    """
    Get the directories for the data modules.

    Walk through the src directory and return a list of all the directories
    (not the files, just the folder names).
    """
    data_module_dirs = []
    for dir_path, dir_names, file_names in os.walk(path_to_src_dir):
        for dir_name in dir_names:
            if dir_name.startswith("_"):
                continue
            data_module_dirs.append(dir_name)
    return data_module_dirs


def create_directories():
    config("DATA_DIR").mkdir(parents=True, exist_ok=True)
    config("OUTPUT_DIR").mkdir(parents=True, exist_ok=True)
    config("DOCS_BUILD_DIR").mkdir(parents=True, exist_ok=True)

    raw_results_dir = config("OUTPUT_DIR") / "raw_results"
    raw_results_dir.mkdir(parents=True, exist_ok=True)

    # Create directories for each data module
    data_module_dirs = get_data_module_directories()
    for data_module_dir in data_module_dirs:
        data_module_dir = config("DATA_DIR") / data_module_dir
        data_module_dir.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    create_directories()
