import pandas as pd
from model_classes.helper_func import process_df
import os

def cutoff_calc(dataset_path,
                dataset_name,
                frequency,
                seasonality,
                test_split):
    """
    Writes cutoff date of df to common parquet file. Cutoff date is the first date in the
    test_data obtained by splitting the df using the process_df function.
    """

    df = pd.read_parquet(dataset_path)

    _, test_data, _ = process_df(df,
                                 frequency,
                                 seasonality,
                                 test_split)
    
    cutoff_date = test_data['ds'].min()

    new_entry = pd.DataFrame({
        "dataset_name": [dataset_name],
        "cutoff_date": [cutoff_date],
    })
    
    if os.path.exists("cutoff_dates.parquet"):
        cutoff_data = pd.read_parquet("cutoff_dates.parquet")
        cutoff_data = pd.concat([cutoff_data, new_entry])
    else:
        cutoff_data = new_entry

    cutoff_data.to_parquet("cutoff_dates.parquet")

    return cutoff_date

if __name__ == "__main__":
    print(pd.read_parquet("cutoff_dates.parquet"))