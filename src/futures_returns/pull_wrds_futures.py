import sys
from pathlib import Path

import pandas as pd
import polars as pl
import wrds

sys.path.insert(0, str(Path(__file__).parent.parent))
from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")


def fetch_wrds_contract_info(product_contract_code):
    """
    Fetch rows from wrds_contract_info.

    Parameters
    ----------
    product_contract_code : int
        The commodity's integer contract code (e.g., 3160).

    Returns
    -------
    pandas.DataFrame
        Columns include: futcode, contrcode, contrname, contrdate, startdate, lasttrddate.
    """
    db = wrds.Connection(wrds_username=WRDS_USERNAME)
    query = f"""
    SELECT futcode, contrcode, contrname, contrdate, startdate, lasttrddate
    FROM tr_ds_fut.wrds_contract_info
    WHERE contrcode = {product_contract_code}
    """
    df = db.raw_sql(query)
    db.close()
    return df


def fetch_wrds_fut_contract(futcodes_contrdates):
    """
    Fetch daily settlement prices from wrds_fut_contract.

    Parameters
    ----------
    futcodes_contrdates : dict
        Keys are futcode values, and values are corresponding contract date strings.

    Returns
    -------
    pandas.DataFrame
        Columns include: futcode, date_, settlement, and a 'contrdate' column mapped from futcodes_contrdates.
    """
    db = wrds.Connection(wrds_username=WRDS_USERNAME)
    query = f"""
    SELECT futcode, date_, settlement
    FROM tr_ds_fut.wrds_fut_contract
    WHERE futcode IN {tuple(futcodes_contrdates.keys())}
    """
    df = db.raw_sql(query)
    df["date_"] = pd.to_datetime(df["date_"])
    df["contrdate"] = df["futcode"].map(futcodes_contrdates)
    db.close()
    return df


def pull_all_futures_data():
    """
    Pull raw data from WRDS for all product codes in product_list,
    then concatenate into one DataFrame.

    Returns
    -------
    pandas.DataFrame
        Combined daily settlements for all relevant product codes.
    """
    product_list = [
        3160,
        289,
        3161,
        1980,
        2038,
        3247,
        1992,
        361,
        385,
        2036,
        379,
        3256,
        396,
        430,
        1986,
        2091,
        2029,
        2060,
        3847,
        2032,
        3250,
        2676,
        2675,
        3126,
        2087,
        2026,
        2020,
        2065,
        2074,
        2108,
    ]
    all_frames = []
    for code in product_list:
        info_df = fetch_wrds_contract_info(code)
        if info_df.empty:
            continue
        futcodes_contrdates = info_df.set_index("futcode")["contrdate"].to_dict()
        data_contracts = fetch_wrds_fut_contract(futcodes_contrdates)
        if not data_contracts.empty:
            data_contracts["product_code"] = code
            all_frames.append(data_contracts)
    final_df = pd.concat(all_frames, ignore_index=True)
    final_df = final_df.rename(columns={"date_": "date"})
    return final_df


def load_combined_futures_data(data_dir=DATA_DIR, format="pandas"):
    """
    Checks if a combined (paper + current) futures dataset already exists locally.
    If so, reads from that file to avoid repeated WRDS pulls.
    If not, pulls from WRDS, saves to a local parquet file, and returns it.

    Returns
    -------
    pandas.DataFrame
        A DataFrame of daily settlement data spanning both 'paper' and 'current' periods.
    """
    data_dir = Path(data_dir)
    path = data_dir / "wrds_futures.parquet"
    if format == "pandas":
        df = pd.read_parquet(path)
    elif format == "polars":
        df = pl.read_parquet(path)
    else:
        raise ValueError(f"Invalid format: {format}")
    return df


def pull_wrds_tables(data_dir=DATA_DIR):
    """
    Pull selected tables from WRDS.
    """
    db = wrds.Connection(wrds_username=WRDS_USERNAME)
    df = db.get_table(library="tr_ds_fut", table="wrds_cseries_info")
    df.to_csv(data_dir / "wrds_cseries_info.csv")
    df.to_parquet(data_dir / "wrds_cseries_info.parquet")

    df = db.get_table(library="tr_ds_fut", table="dsfutcalcserval")
    df.to_csv(data_dir / "dsfutcalcserval.csv")
    df.to_parquet(data_dir / "dsfutcalcserval.parquet")

    db.close()

if __name__ == "__main__":
    df = pull_all_futures_data()
    path = DATA_DIR / "wrds_futures.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path)
