from pathlib import Path

import pandas as pd
import pandas_datareader.data as web

import config

DATA_DIR = config.DATA_DIR
START_DATE = config.START_DATE
END_DATE = config.END_DATE

series_to_pull = {
    ## Interest Rates
    "DGS1MO": "1-Month Treasury Yield",
    "DGS3MO": "3-Month Treasury Yield",
    "DGS6MO": "6-Month Treasury Yield",
    "DGS1": "1-Year Treasury Yield",
    "DGS2": "2-Year Treasury Yield",
    "DGS3": "3-Year Treasury Yield",
}


def pull_fred(start_date=START_DATE, end_date=END_DATE, ffill=True):
    """
    Lookup series code, e.g., like this:
    https://fred.stlouisfed.org/series/RPONTSYD
    """
    df = web.DataReader(list(series_to_pull.keys()), "fred", start_date, end_date)

    return df


def load_fred(data_dir=DATA_DIR):
    """
    Must first run this module as main to pull and save data.
    """
    file_path = Path(data_dir) / "fred.parquet"
    df = pd.read_parquet(file_path)
    # df = pd.read_csv(file_path, parse_dates=["DATE"])
    # df = df.set_index("DATE")
    return df


if __name__ == "__main__":
    today = pd.Timestamp.today().strftime("%Y-%m-%d")
    end_date = today
    df = pull_fred(START_DATE, end_date)
    filedir = Path(DATA_DIR)
    filedir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(filedir / "fred.parquet")
