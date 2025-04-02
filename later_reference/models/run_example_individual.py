import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from models.dataset import Dataset
from models.univariate_local import (
    HoltWintersForecasting,
    MeanForecasting,
    NaiveForecasting,
    SarimaForecasting,
)

if __name__ == "__main__":
    Dataset.reset_tables_in_memory()
    dataset = Dataset.from_parquet(
        y="ken_french_portfolios/french_portfolios_25_monthly_size_and_bm/SMALL LoBM",
        time_frequency="M",
    )
    models = [
        HoltWintersForecasting,
        MeanForecasting,
        NaiveForecasting,
        SarimaForecasting,
    ]
    for model in models:
        model_instance = model.from_dataset(
            dataset=dataset,
            step_size=1,
            n_forecasting=12,
        )
        model_instance.build_divisions()
        model_instance.run()
        model_instance.assess_error()
        model_instance.save()
