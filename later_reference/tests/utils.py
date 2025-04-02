import functools
import os

from models.error_metrics import TEST_PATH_ERROR_METRICS_RESULTS
from models.time_series_model import TEST_PATH_TIME_SERIES_MODELS_RESULTS


def del_test_files():
    if os.path.exists(TEST_PATH_TIME_SERIES_MODELS_RESULTS):
        os.remove(TEST_PATH_TIME_SERIES_MODELS_RESULTS)
    if os.path.exists(TEST_PATH_ERROR_METRICS_RESULTS):
        os.remove(TEST_PATH_ERROR_METRICS_RESULTS)
    return True


def del_files(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            del_test_files()
            return result
        except Exception as e:
            del_test_files()
            raise e

    return wrapper
