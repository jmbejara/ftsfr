import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import toml

from settings import config
from dependency_tracker import (
    load_module_requirements,
    check_module_availability,
    get_available_datasets,
)

BASE_DIR = config("BASE_DIR")
DATA_DIR = config("DATA_DIR")
OUTPUT_DIR = config("OUTPUT_DIR")

# Read config.toml
with open(BASE_DIR / "config.toml", "r") as f:
    benchmarks = toml.load(f)

models = benchmarks["models"]
models_activated = [model for model in models if models[model]]
data_sources = benchmarks["data_sources"]

# Get available datasets
module_requirements_dict = load_module_requirements()
module_requirements = check_module_availability(module_requirements_dict, data_sources)
available_datasets = get_available_datasets(module_requirements, DATA_DIR)

# Find all result files matching the pattern {model}_{dataset}_results.csv
results_files = []
for model in models_activated:
    for dataset_name in available_datasets:
        result_file = OUTPUT_DIR / "raw_results" / f"{model}_{dataset_name}_results.csv"
        if result_file.exists():
            results_files.append(result_file)

if not results_files:
    print("No result files found!")
    sys.exit(1)

## Read all results files and concatenate them
results_list = []
for file in results_files:
    df = pd.read_csv(file)
    # Extract model and dataset name from filename
    filename = file.stem  # removes .csv
    # Remove the _results suffix
    name_without_results = filename.rsplit("_results", 1)[0]
    
    # Find which model this file belongs to by checking which model name is a prefix
    model_name = None
    dataset_name = None
    for model in models_activated:
        if name_without_results.startswith(model + "_"):
            model_name = model
            # The dataset name is everything after the model name and underscore
            dataset_name = name_without_results[len(model) + 1:]
            break
    
    if model_name and dataset_name:
        df["model"] = model_name
        df["dataset"] = dataset_name
        results_list.append(df)
    else:
        print(f"Warning: Could not parse model and dataset from filename: {filename}")
        continue

results = pd.concat(results_list)

results.to_csv(OUTPUT_DIR / "results_all.csv", index=False)

latex_string = results.to_latex(index=False, escape=True)
# print(latex_string)
with open(OUTPUT_DIR / "results_all.tex", "w") as f:
    f.write(latex_string)
