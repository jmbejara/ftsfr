import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import toml

from settings import config

BASE_DIR = config("BASE_DIR")
OUTPUT_DIR = config("OUTPUT_DIR")

# Read benchmarks.toml
with open(BASE_DIR / "benchmarks.toml", "r") as f:
    benchmarks = toml.load(f)

models = benchmarks["models"]
models_activated = [model for model in models if models[model]]

results_files = [
    OUTPUT_DIR / "raw_results" / f"{model}_results.csv" for model in models_activated
]

## Read all results files and concatenate them
results = pd.concat([pd.read_csv(file) for file in results_files])

results.to_csv(OUTPUT_DIR / "results_all.csv", index=False)

latex_string = results.to_latex(index=False, escape=True)
# print(latex_string)
with open(OUTPUT_DIR / "results_all.tex", "w") as f:
    f.write(latex_string)
