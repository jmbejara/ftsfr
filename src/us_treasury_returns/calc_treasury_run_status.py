"""
calc_treasury_run_status.py

Identifies on-the-run U.S. Treasury securities for each date and term.

This module processes treasury auction data to determine which Treasury notes and bonds
are "on-the-run" (the most recently issued securities) versus "off-the-run" (older issues)
for each trading date. On-the-run securities are important benchmarks in fixed income
markets as they typically have the highest liquidity and are used for pricing other securities.

Inputs:
    - treasury_auction_stats.parquet: Contains U.S. Treasury auction data with columns:
        - cusip: Security identifier
        - issueDate: Date the security was issued
        - maturityDate: Date the security matures
        - type: Security type (Note, Bond, etc.)
        - term: Security term/maturity length
        - totalTendered: Total amount tendered in the auction
        - totalAccepted: Total amount accepted in the auction

Outputs:
    - issue_dates.parquet: Aggregated total tendered and accepted amounts by issue date
    - treasuries_with_run_status.parquet: Daily snapshot of on-the-run securities with columns:
        - date: Trading date
        - run: 0 for on-the-run, incrementing for older issues
        - term: Security term
        - type: Security type (Note or Bond)
        - cusip: Security identifier

The module filters for Note and Bond types only, excluding Bills and other security types.
For each date, it identifies the most recently issued security that hasn't matured yet
for each term/type combination.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pathlib import Path

import numpy as np
import pandas as pd

from settings import config

DATA_DIR = Path(config("DATA_DIR"))


def process_issue_date(df):
    """process_issue_date
    returns a DataFrame with totalTendered and totalAccepted for each issueDate.

    Args:
        df (DataFrame): treasury_auction_stats.parquet
    """

    return df.groupby("issueDate").sum(numeric_only=True)[
        ["totalTendered", "totalAccepted"]
    ]


def process_ontherun(df, start_date="1800-01-01"):
    """
    Processes a DataFrame to return the most recently issued CUSIP for each date,
    excluding those that are expired.

    Args:
        df (pd.DataFrame): DataFrame containing bond auction data. Expected to have
                           columns like 'date', 'term', 'cusip', 'maturityDate', 'issueDate'.
        start_date (str, optional): The starting date from which to consider data.
                                    Defaults to '1800-01-01'. The actual starting date will be
                                    set as start_date = max(start_date, df.issueDate.min()).

    Returns:
        pd.DataFrame: A DataFrame with columns ['date', 'run', 'term', 'cusip'],
                      containing the most recent CUSIPs for each term and date,
                      up to the offruns limit, if applicable.
    """

    COLS = ["date", "run", "term", "type", "cusip"]
    if df.empty:
        return pd.DataFrame(columns=COLS)

    def calculate_run_byterm(df, term, start_date, dates):
        temp_df = df[(df.term == term) & (df.maturityDate >= start_date)].sort_values(
            "issueDate", ascending=False
        )
        res = []
        for d in dates:
            row = temp_df[(temp_df.issueDate <= d) & (d <= temp_df.maturityDate)][
                ["term", "type", "cusip"]
            ]
            # if offruns != -1:
            #     row = row.iloc[:offruns+1]
            row = row[~row.duplicated(subset="cusip", keep="first")]
            row["date"] = d
            row["run"] = np.arange(len(row))
            res.append(row)
        res = pd.concat(res).reset_index(drop=True)[COLS]
        return res

    lastday = np.min([pd.Timestamp.today(), df.maturityDate.max()])
    start_date = np.max([pd.to_datetime(start_date), df.issueDate.min()])

    dates = pd.bdate_range(start_date, lastday, name="date")
    types = df.type.unique().tolist()

    firstissue = (
        df.sort_values(["maturityDate", "issueDate"])
        .groupby("cusip")
        .first()
        .reset_index()
    )

    res = []
    for t in types:
        temp = firstissue[firstissue.type == t]
        terms = temp.term.unique().tolist()
        for term in terms:
            res.append(calculate_run_byterm(temp, term, start_date, dates))
    res = (
        pd.concat(res)
        .sort_values(by=["date", "run", "term", "type"])
        .reset_index(drop=True)
    )
    return res


if __name__ == "__main__":
    # DATA_DIR = DATA_DIR / "us_treasury_returns"
    data_dir = DATA_DIR
    data_dir.mkdir(parents=True, exist_ok=True)

    # with warnings.catch_warnings():
    #     warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)
    #     dat = pd.read_csv(
    #         data_dir / "treasury_auction_stats.csv",
    #         parse_dates=["issueDate", "maturityDate"],
    #     )
    dat = pd.read_parquet(data_dir / "treasury_auction_stats.parquet")

    sub_cols = [
        "cusip",
        "issueDate",
        "maturityDate",
        "type",
        "term",
        "totalTendered",
        "totalAccepted",
    ]

    dat = dat[sub_cols][dat["type"].isin(["Note", "Bond"])]
    # dat = dat[sub_cols]

    issue_dates = process_issue_date(dat)
    issue_dates.to_parquet(data_dir / "issue_dates.parquet")

    preload = process_ontherun(dat)
    preload.to_parquet(data_dir / "treasuries_with_run_status.parquet", index=False)
