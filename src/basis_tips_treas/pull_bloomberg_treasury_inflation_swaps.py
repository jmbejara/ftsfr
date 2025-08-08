from xbbg import blp
from decouple import config

OUTPUT_DIR = config("OUTPUT_DIR")
START_DATE = config("START_DATE", "2020-01-01")
END_DATE = config("END_DATE", "2025-01-01")

def pull_treasury_inflation_swaps(
    start_date=START_DATE,
    end_date=END_DATE,
    output_path="treasury_inflation_swaps.csv"
):
    """
    Connects to Bloomberg via xbbg, pulls historical daily prices for USD
    Treasury Inflation Swaps, and saves them to a CSV with columns matching
    the provided treasury_inflation_swaps.csv file.

    :param start_date: Start date in 'YYYY-MM-DD' format (str).
    :param end_date: End date in 'YYYY-MM-DD' format (str).
    :param output_path: Path to save the resulting CSV file.
    :return: A pandas DataFrame containing the replicated data.
    """

    # Tickers to replicate. Adjust as needed for 1M, 3M, 6M, etc.
    tickers = [
        "USSWIT1 BGN Curncy",   # 1Y
        "USSWIT2 BGN Curncy",   # 2Y
        "USSWIT3 BGN Curncy",   # 3Y
        "USSWIT4 BGN Curncy",   # 4Y
        "USSWIT5 BGN Curncy",   # 5Y
        "USSWIT10 BGN Curncy",  # 10Y
        "USSWIT20 BGN Curncy",  # 20Y
        "USSWIT30 BGN Curncy",  # 30Y
    ]

    fields = ["PX_LAST"]

    # Pull data using xbbg's bdh function
    df = blp.bdh(
        tickers=tickers,
        flds=fields,
        start_date=start_date,
        end_date=end_date
    )
    # 'df' is a multi-index DataFrame with (date) as the index and (ticker, field) as columns.
    # Drop the second level of columns ("PX_LAST"), so columns are just the tickers
    df.columns = df.columns.droplevel(level=1)

    df = df.reset_index()

    df = df.rename(columns={"index": "Dates", "date": "Dates"})

    # Reorder columns so "Dates" is first, followed by each ticker
    col_order = ["Dates"] + tickers
    df = df[col_order]

    df.to_csv(output_path, index=False)

    return df


if __name__ == "__main__":
    pull_treasury_inflation_swaps()
