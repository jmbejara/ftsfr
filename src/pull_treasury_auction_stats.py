"""
Downloads treasury auction data from TreasuryDirect.gov
See here: https://treasurydirect.gov/TA_WS/securities/jqsearch
"""

import json
import urllib.request
from pathlib import Path

import pandas as pd

from settings import config

SUBFOLDER = "crsp_treasury"
DATA_DIR = Path(config("DATA_DIR"))


def pull_treasury_auction_data():
    url = "https://treasurydirect.gov/TA_WS/securities/jqsearch?format=jsonp"

    with urllib.request.urlopen(url) as wpg:
        x = wpg.read()
        data = json.loads(x.replace(b");", b"").replace(b"callback (", b""))

    df = pd.DataFrame(data["securityList"])

    # Date columns
    date_cols = [
        "issueDate",
        "maturityDate",
        "announcementDate",
        "auctionDate",
        "datedDate",
        "backDatedDate",
        "callDate",
        "calledDate",
        "firstInterestPaymentDate",
        "maturingDate",
        "originalDatedDate",
        "originalIssueDate",
        "tintCusip1DueDate",
        "tintCusip2DueDate",
    ]
    df[date_cols] = df[date_cols].apply(pd.to_datetime, errors="coerce")

    # Numeric columns (percentages and amounts)
    numeric_cols = [
        "interestRate",
        "accruedInterestPer1000",
        "accruedInterestPer100",
        "adjustedAccruedInterestPer1000",
        "adjustedPrice",
        "allocationPercentage",
        "averageMedianDiscountRate",
        "averageMedianInvestmentRate",
        "averageMedianPrice",
        "bidToCoverRatio",
        "totalAccepted",
        "totalTendered",
    ]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # Boolean columns
    bool_cols = [
        "backDated",
        "callable",
        "cashManagementBillCMB",
        "fimaIncluded",
        "floatingRate",
        "reopening",
        "somaIncluded",
        "strippable",
        "tips",
    ]
    for col in bool_cols:
        df[col] = df[col].map({"true": True, "false": False})

    return df


def load_treasury_auction_data(data_dir: Path):
    df = pd.read_parquet(data_dir / SUBFOLDER / "treasury_auction_stats.parquet")
    return df


def _demo():
    # Set display options to show all columns
    pd.set_option("display.max_columns", None)  # Show all columns
    pd.set_option("display.width", None)  # Don't wrap to multiple lines
    pd.set_option("display.max_rows", None)  # Show all rows

    df.dtypes
    df.info()


if __name__ == "__main__":
    # Create subfolder
    dir_path = DATA_DIR / SUBFOLDER
    dir_path.mkdir(parents=True, exist_ok=True)

    df = pull_treasury_auction_data()
    df.to_parquet(dir_path / "treasury_auction_stats.parquet", index=False)

# with open(data_dir / 'treasury_auction_stats.json', 'w') as json_file:
#     json.dump(data, json_file)
