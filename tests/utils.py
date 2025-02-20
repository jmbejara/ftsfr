from models.time_series_model import TEST_PATH_TIME_SERIES_MODELS_RESULTS
from models.error_metrics import TEST_PATH_ERROR_METRICS_RESULTS
import os


def del_test_files():
    if os.path.exists(TEST_PATH_TIME_SERIES_MODELS_RESULTS):
        os.remove(TEST_PATH_TIME_SERIES_MODELS_RESULTS)
    if os.path.exists(TEST_PATH_ERROR_METRICS_RESULTS):
        os.remove(TEST_PATH_ERROR_METRICS_RESULTS)
    return True
