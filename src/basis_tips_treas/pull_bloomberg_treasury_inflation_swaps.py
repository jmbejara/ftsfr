from xbbg import blp
from pathlib import Path

from settings import config

OUTPUT_DIR = config("OUTPUT_DIR")
START_DATE = config("START_DATE", default="2020-01-01")
END_DATE = config("END_DATE", default="2025-01-01")


def pull_treasury_inflation_swaps(
    start_date: str = START_DATE,
    end_date: str = END_DATE,
):
    """
    Connects to Bloomberg via xbbg, pulls historical daily prices for USD
    Treasury Inflation Swaps, and returns a DataFrame with columns matching
    the expected schema.

    :param start_date: Start date in 'YYYY-MM-DD' format (str).
    :param end_date: End date in 'YYYY-MM-DD' format (str).
    :return: A pandas DataFrame containing the replicated data.
    """

    # Tickers to replicate. Adjust as needed for 1M, 3M, 6M, etc.
    tickers = [
        "USSWIT1 BGN Curncy",  # 1Y
        "USSWIT2 BGN Curncy",  # 2Y
        "USSWIT3 BGN Curncy",  # 3Y
        "USSWIT4 BGN Curncy",  # 4Y
        "USSWIT5 BGN Curncy",  # 5Y
        "USSWIT10 BGN Curncy",  # 10Y
        "USSWIT20 BGN Curncy",  # 20Y
        "USSWIT30 BGN Curncy",  # 30Y
    ]

    fields = ["PX_LAST"]

    # Pull data using xbbg's bdh function
    df = blp.bdh(tickers=tickers, flds=fields, start_date=start_date, end_date=end_date)
    # 'df' is a multi-index DataFrame with (date) as the index and (ticker, field) as columns.
    # Drop the second level of columns ("PX_LAST"), so columns are just the tickers
    df.columns = df.columns.droplevel(level=1)

    df = df.reset_index()

    df = df.rename(columns={"index": "Dates", "date": "Dates"})

    # Reorder columns so "Dates" is first, followed by each ticker
    col_order = ["Dates"] + tickers
    df = df[col_order]

    return df


if __name__ == "__main__":
    # Pull data and save to the configured OUTPUT_DIR
    df = pull_treasury_inflation_swaps()
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "treasury_inflation_swaps.parquet"
    df.to_parquet(output_path, index=False)
