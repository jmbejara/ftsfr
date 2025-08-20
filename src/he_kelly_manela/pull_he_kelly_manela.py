import sys
import zipfile
from pathlib import Path
import urllib3

sys.path.insert(0, str(Path(__file__).parent.parent))

from io import BytesIO

import pandas as pd
import requests

# Suppress SSL warnings when verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from settings import config

DATA_DIR = config("DATA_DIR")
URL = "https://apps.olin.wustl.edu/faculty/manela/hkm/intermediarycapitalrisk/He_Kelly_Manela_Factors.zip"


def pull_he_kelly_manela(data_dir=DATA_DIR):
    """
    Download the He-Kelly-Manela factors and test portfolios data
    """
    # DATA_DIR.mkdir(parents=True, exist_ok=True)
    response = requests.get(URL, verify=False)
    zip_file = BytesIO(response.content)
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(data_dir)


def load_he_kelly_manela_factors_monthly(data_dir=DATA_DIR):
    path = data_dir / "He_Kelly_Manela_Factors_monthly.csv"
    _df = pd.read_csv(path)
    _df["date"] = pd.to_datetime(_df["yyyymm"], format="%Y%m")
    return _df


def load_he_kelly_manela_factors_daily(data_dir=DATA_DIR):
    path = data_dir / "He_Kelly_Manela_Factors_daily.csv"
    _df = pd.read_csv(path)
    _df["date"] = pd.to_datetime(_df["yyyymmdd"], format="%Y%m%d")
    return _df


def load_he_kelly_manela_all(data_dir=DATA_DIR):
    path = data_dir / "He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv"
    _df = pd.read_csv(path)
    _df["date"] = pd.to_datetime(_df["yyyymm"], format="%Y%m")
    return _df


if __name__ == "__main__":
    data_dir = DATA_DIR
    pull_he_kelly_manela(data_dir=data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
