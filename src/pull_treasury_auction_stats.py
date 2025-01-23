"""
Downloads treasury auction data from TreasuryDirect.gov
See here: https://treasurydirect.gov/TA_WS/securities/jqsearch
"""

import urllib.request, json
import pandas as pd
from pathlib import Path

from settings import config

SUBFOLDER = "crsp_treasury"
DATA_DIR = Path(config("DATA_DIR"))


def pull_treasury_auction_data():
    url = "https://treasurydirect.gov/TA_WS/securities/jqsearch?format=jsonp"

    with urllib.request.urlopen(url) as wpg:
        x = wpg.read()
        data = json.loads(x.replace(b");", b"").replace(b"callback (", b""))

    return pd.DataFrame(data["securityList"])


if __name__ == "__main__":
    # Create subfolder
    data_dir = DATA_DIR / SUBFOLDER
    data_dir.mkdir(parents=True, exist_ok=True)

    df = pull_treasury_auction_data()
    df.to_csv(data_dir / "treasury_auction_stats.csv", index=False)

# with open(data_dir / 'treasury_auction_stats.json', 'w') as json_file:
#     json.dump(data, json_file)
