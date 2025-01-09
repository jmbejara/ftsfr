# Financial Time-Series Forecasting Archive

This repository contains a collection of financial time-series forecasting models. It produces esting a benchmark for prac

## Create Virtual Environment
The virtual environment is created using conda. It is used to manage the dependencies of the package.

The following steps are used to create the virtual environment.

Inside your terminal, write:
```bash
conda create -n ftsf python=3.12.6
```

Activate virtual environment:
```bash
conda activate ftsf
```

Install packages:
```bash
pip install -r requirements-dev.txt
```

Install pre-commit hooks:
```bash
pre-commit install
```
