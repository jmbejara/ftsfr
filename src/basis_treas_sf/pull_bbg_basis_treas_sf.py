"""
pull_bbg_basis_treas_sf.py

Pull USD OIS term structure from Bloomberg via xbbg and materialize an
Excel file compatible with `clean_treas_sf_excel.py`.

Notes
-----
- This script only handles OIS. The Treasury spot-futures inputs remain
  sourced from the manually maintained Excel referenced by
  `clean_treas_sf_excel.py`.
- No printing to stdout to keep scripts quiet, per project style guide.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import List

import pandas as pd
from xbbg import blp

from settings import config


# Configuration via settings.py
MANUAL_DATA_DIR: Path = config("MANUAL_DATA_DIR")
START_DATE: str = config("START_DATE", default="2004-01-01")
END_DATE: str = config("END_DATE", default=str(date.today()))


def ois_tickers() -> List[str]:
    """Bloomberg tickers for USD OIS curve used downstream.

    Matches the mapping expected in `clean_treas_sf_excel.py`.
    """
    return [
        "USSO1Z CMPN Curncy",  # 1W
        "USSOA CMPN Curncy",  # 1M
        "USSOB CMPN Curncy",  # 2M
        "USSOC CMPN Curncy",  # 3M
        "USSOF CMPN Curncy",  # 6M
        "USSO1 CMPN Curncy",  # 1Y
        "USSO2 CMPN Curncy",  # 2Y
        "USSO3 CMPN Curncy",  # 3Y
        "USSO4 CMPN Curncy",  # 4Y
        "USSO5 CMPN Curncy",  # 5Y
        "USSO7 CMPN Curncy",  # 7Y
        "USSO10 CMPN Curncy",  # 10Y
        "USSO15 CMPN Curncy",  # 15Y
        "USSO20 CMPN Curncy",  # 20Y
        "USSO30 CMPN Curncy",  # 30Y
    ]


def pull_ois_history(start_date: str = START_DATE, end_date: str = END_DATE) -> pd.DataFrame:
    """Fetch historical USD OIS levels (PX_LAST) from Bloomberg via xbbg.

    Returns a DataFrame with columns ["Date", <tickers...>] where tickers are
    the Bloomberg composite OIS mnemonics used by the cleaning script.
    """
    tickers = ois_tickers()
    df = blp.bdh(tickers=tickers, flds=["PX_LAST"], start_date=start_date, end_date=end_date)

    # Drop the field-level in the MultiIndex columns, yielding tickers-only columns
    if isinstance(df.columns, pd.MultiIndex) and df.columns.nlevels == 2:
        df.columns = df.columns.droplevel(level=1)

    df = df.reset_index().rename(columns={"index": "Date", "date": "Date"})
    # Ensure Date is datetime (no tz)
    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
    # Columns in desired order: Date then tickers
    df = df[["Date", *tickers]]
    return df


def write_bloomberg_style_excel_for_ois(df: pd.DataFrame, excel_path: Path) -> None:
    """Write an Excel file shaped like a typical Bloomberg export that the
    existing cleaning script expects to read and post-process.

    The shape satisfies the operations in `clean_treas_sf_excel.py`:
    - Drop first 4 columns
    - Drop top 3 rows
    - Drop rows with index 1 and 2 (post-reset)
    - Use row 0 as header ("Date" plus tickers)
    - Data starts after that
    """
    tickers = [c for c in df.columns if c != "Date"]

    # Build padded rows matching the expected Bloomberg-like layout
    left_pad_cols = 4

    # 3 top rows to be discarded entirely
    top_pad = [["" for _ in range(left_pad_cols + 1 + len(tickers))] for _ in range(3)]

    # Header row: Date + tickers
    header_row = ["" for _ in range(left_pad_cols)] + ["Date", *tickers]

    # 2 additional rows often present in BBG exports (fld desc / currency)
    # We insert blank rows that will be dropped by the cleaning script
    drop_rows_after_header = [["" for _ in range(left_pad_cols + 1 + len(tickers))] for _ in range(2)]

    # Actual data rows
    data_rows: List[List[object]] = []
    for _, row in df.iterrows():
        data_rows.append([
            *(["" for _ in range(left_pad_cols)]),
            row["Date"],
            *[row[t] for t in tickers],
        ])

    # Combine all parts
    full_rows = top_pad + [header_row] + drop_rows_after_header + data_rows
    sheet_df = pd.DataFrame(full_rows)

    excel_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        sheet_df.to_excel(writer, index=False, header=False)


if __name__ == "__main__":
    ois = pull_ois_history()
    out_path = Path(MANUAL_DATA_DIR) / "OIS.xlsx"
    write_bloomberg_style_excel_for_ois(ois, out_path)


