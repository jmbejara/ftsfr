import datetime
import logging
import os
import re
import signal
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import models.univariate_local as mul
from models.dataset import Dataset

log_file_name = f"logs/log_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), log_file_name),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException()


signal.signal(signal.SIGALRM, timeout_handler)
TIMEOUT_SECONDS = 60


def get_parquets(ignore_parquets=[], only_keep_specific=[]):
    parquets = []
    for root, dirs, files in os.walk("_data"):
        for file in files:
            if file.endswith(".parquet"):
                parquets.append(os.path.join(root, file))
    parquets = [p.replace("_data/", "").replace(".parquet", "") for p in parquets]
    parquets = [p for p in parquets if not filter_in_list(p, ignore_parquets)]
    if only_keep_specific != [] and only_keep_specific is not None:
        parquets = [p for p in parquets if filter_in_list(p, only_keep_specific)]
    return parquets


def get_forecasting_models(ignore_models=[], only_keep_specific=[]):
    forecasting_models = [
        getattr(mul, name) for name in dir(mul) if name.endswith("Forecasting")
    ]
    forecasting_models = [
        f for f in forecasting_models if not filter_in_list(f.__name__, ignore_models)
    ]
    if only_keep_specific != [] and only_keep_specific is not None:
        forecasting_models = [
            f
            for f in forecasting_models
            if filter_in_list(f.__name__, only_keep_specific)
        ]
    return forecasting_models


def filter_in_list(string, list):
    return any(bool(re.search(s, str(string))) for s in list)


STEP_SIZE = 1
N_FORECASTING = 12


if __name__ == "__main__":
    forecasting_models = get_forecasting_models(
        ignore_models=["Lstm", "Sarima", "HoltWinters"]
    )
    parquets = get_parquets()
    for parquet in parquets:
        datasets = Dataset.from_parquet_all_from_table(parquet)
        for dataset in datasets:
            for model in forecasting_models:
                time_start = datetime.datetime.now()
                model_instance = model.from_dataset(
                    dataset=dataset,
                    step_size=STEP_SIZE,
                    n_forecasting=N_FORECASTING,
                )
                model_instance.build_divisions()
                if model_instance.is_it_already_in_results():
                    logging.info(
                        f"Skipped due to already being in results {model.__name__}(parquet={parquet}, y={dataset.get_y_name()})"
                    )
                    continue
                try:
                    signal.alarm(TIMEOUT_SECONDS)  # Start timeout
                    model_instance.run()
                    signal.alarm(0)
                except TimeoutException:
                    logging.info(
                        f"Timed out {TIMEOUT_SECONDS} seconds before finishing {model.__name__}(parquet={parquet}, y={dataset.get_y_name()})"
                    )
                    continue
                model_instance.assess_error()
                model_instance.save()
                time_delta = (datetime.datetime.now() - time_start).total_seconds()
                logging.info(
                    f"Processed {model.__name__}(parquet={parquet}, y={dataset.get_y_name()}) in {time_delta}s"
                )
