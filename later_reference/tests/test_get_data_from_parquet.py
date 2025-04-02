import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from models.dataset import Dataset
from models.univariate_local import (
    HoltWintersForecasting,
    MeanForecasting,
    NaiveForecasting,
    SarimaForecasting,
)

UNIVARIATE_LOCAL = [
    HoltWintersForecasting,
    MeanForecasting,
    NaiveForecasting,
    SarimaForecasting,
]


def test_get_data_from_parquet():
    dataset = Dataset.from_parquet(
        y="french_portfolios_25_monthly_size_and_bm_equal_weighted/SMALL LoBM"
    )
    assert isinstance(dataset, Dataset)
    assert dataset.get_y().columns[0] == "SMALL LoBM"
    assert dataset.get_X() is None


def test_get_all_data_from_parquet_table():
    datasets = Dataset.from_parquet_all_from_table(
        y_table="french_portfolios_25_monthly_size_and_bm_equal_weighted",
    )
    assert isinstance(datasets, list)
    table = Dataset.get_table_from_memory(
        "french_portfolios_25_monthly_size_and_bm_equal_weighted"
    )
    for dataset in datasets:
        assert isinstance(dataset, Dataset)
        assert dataset.get_y().columns[0] in list(table.columns)
        assert dataset.get_X() is None
        table.drop(dataset.get_y().columns[0], axis=1, inplace=True)
    if len(table.columns) == 1:
        assert table.columns[0].lower() == "date"
    else:
        assert len(table.columns) == 0
