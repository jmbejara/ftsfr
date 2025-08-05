import sys
from pathlib import Path
import warnings

sys.path.insert(0, str(Path(__file__).parent.parent))


import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

from settings import config

DATA_DIR = config("DATA_DIR")
BOND_RED_CODE_FILE_NAME = "corporate_bond_returns.parquet"
CDS_FILE_NAME = "cds_final.parquet"
FINAL_ANALYSIS_FILE_NAME = "final_data.parquet"
RED_CODE_FILE_NAME = "RED_and_ISIN_mapping.parquet"


def merge_red_code_into_bond_treas(bond_treas_df, red_c_df):
    """
    bond_treas_df: dataframe containing merged corporate bond and treasury data, we will only use the below columnes
        date, -- date when data was collected
        cusip, -- cusip of bond itself
        issuer_cusip, -- cusip of issuing firm
        'BOND_YIELD', -- yield of bond removing market microstructure effects
        CS, -- Credit Spread we replace Z-spread with
        size_ig, -- 0 if no ig bonds in portfolio, 1 if yes
        size_jk, -- 0 if no junk bonds in portfolio, 1 if yes
        tmt, -- time to maturity in months where months are 30 days

    red_c_df: dataframe containing red code merging information
        redcode, -- redcode of the issuer
        ticker, -- ticker of the issuer
        obl_cusip, -- cusip of an issue, the first 6 objects characters of the string should be the issuers tag
        isin, -- these are product specific
        tier -- tier of product


    output: dataframe with the issuer cusip and red_code now added
        date, -- date when data was collected
        cusip, -- unique bond identifier
        issuer_cusip, -- cusip of issuing firm
        CS, -- Credit Spread we replace Z-spread with
        size_ig, -- 0 if no ig bonds in portfolio, 1 if yes
        size_jk, -- 0 if no junk bonds in portfolio, 1 if yes
        mat_days, -- time to maturity in days
        redcode -- redcode is issuer specific, used to merge CDS values later on
    """

    red_c_df = red_c_df[["obl_cusip", "redcode"]].dropna()
    red_c_df["issuer_cusip"] = red_c_df.apply(lambda row: row["obl_cusip"][:6], axis=1)

    # only need these 2 to merge
    red_c_df = (
        red_c_df[["issuer_cusip", "redcode"]].drop_duplicates().reset_index(drop=True)
    )

    # should drop all uneeded elements
    merged_df = bond_treas_df.merge(red_c_df, on="issuer_cusip", how="inner")
    merged_df["mat_days"] = (
        merged_df["tmt"] * 30
    )  # for maturity days, easier to cubic spline

    return merged_df[
        [
            "date",
            "cusip",
            "issuer_cusip",
            "BOND_YIELD",
            "CS",
            "size_ig",
            "size_jk",
            "mat_days",
            "redcode",
        ]
    ]


def merge_cds_into_bonds(bond_red_df, cds_df):
    """
    bond_red_df: dataframe with the issuer cusip and red_code now added
        date, -- date when data was collected
        cusip, -- cusip of the entire bond issue, unique bond identifier
        issuer_cusip, -- cusip of issuing firm
        BOND_YIELD, -- MMN adjusted bond yield
        CS, -- Credit Spread we replace Z-spread with
        size_ig, -- 0 if no ig bonds in portfolio, 1 if yes
        size_jk, -- 0 if no junk bonds in portfolio, 1 if yes
        mat_days, -- time to maturity in days
        redcode -- redcode is issuer specific, used to merge CDS values later on

    cds_df: dataframe containing cds_data
        date, -- date of report
        'ticker', -- ticker of issuer
        'redcode', -- redcode of issuer
        'parspread', -- parspread
        'tenor', -- tenor, how long
        'tier', -- tier of debt
        'country', -- country of issuer
        'year' -- year of date

    output: dataframe with par spread values merged into all values where there was a possible cubic spline
        'cusip', -- cusip of the entire bond issue, unique bond identifier
       'date', -- reporting date
       'mat_days', -- days till maturity
       'BOND_YIELD', -- MMN adjusted bond yield
       'CS', -- credit spread
        'size_ig', -- 0 if no ig bonds in portfolio, 1 if yes
        'size_jk', -- 0 if no junk bonds in portfolio, 1 if yes
       'par_spread', -- parspread of CDS, backed out by Cubic Spline
    """
    date_set = set(bond_red_df.date.unique())
    cds_df = cds_df[cds_df["date"].isin(date_set)].dropna(
        subset=["date", "parspread", "tenor", "redcode"]
    )

    # par spread values are roughly consistent for each tenor, make broad assumptions on true value on par spread
    c_df_avg = cds_df.groupby(
        cds_df.columns.difference(["parspread"]).tolist(), as_index=False
    ).agg({"parspread": "median"})

    df_unique_count = (
        c_df_avg.groupby(["redcode", "date"])["tenor"].nunique().reset_index()
    )
    df_unique_count.rename(columns={"tenor": "unique_tenor_count"}, inplace=True)

    # need at least 2 for cubic spline
    df_unique_count = df_unique_count[df_unique_count["unique_tenor_count"] > 1]

    # grab the filtered_cds_df by using df_uni_count as a filter
    filtered_cds_df = c_df_avg.merge(
        df_unique_count[["redcode", "date"]], on=["redcode", "date"], how="inner"
    )

    # my mapping to convert tenor to days to get a rough approximation of a daily spline
    tenor_to_days = {
        "1Y": 365,
        "3Y": 3 * 365,
        "5Y": 5 * 365,
        "7Y": 7 * 365,
        "10Y": 10 * 365,
    }

    filtered_cds_df["tenor_days"] = filtered_cds_df["tenor"].map(tenor_to_days)

    # Dictionary to store cubic splines for each (redcode, date) pair
    cubic_splines = {}
    WARN = False

    # Group by (redcode, date) and create splines
    for (redcode, date), group in filtered_cds_df.groupby(["redcode", "date"]):
        x = group["tenor_days"].values
        y = group["parspread"].values

        sorted_indices = np.argsort(x)
        x_sorted, y_sorted = x[sorted_indices], y[sorted_indices]

        # Fit cubic spline
        try:
            cubic_splines[(redcode, date)] = CubicSpline(x_sorted, y_sorted)
        except:
            WARN = True
            # print(x_sorted)
            # print(y_sorted)

    if WARN:
        warnings.warn("Failed to fit cubic spline for (redcode, date)")

    # START filtering the bond dataframe to make the merge easier
    red_set = set(filtered_cds_df["redcode"].unique())
    bond_red_df = bond_red_df[bond_red_df["redcode"].isin(red_set)]

    # vectorized function to grab the par spread
    def add_par_spread_vectorized(df):
        # Create a copy to avoid SettingWithCopyWarning
        df = df.copy()

        mask = df.set_index(["redcode", "date"]).index.isin(cubic_splines.keys())

        # spline interpolation only for matching keys
        valid_rows = df.loc[mask]
        df.loc[mask, "par_spread"] = valid_rows.apply(
            lambda row: cubic_splines[(row["redcode"], row["date"])](row["mat_days"]),
            axis=1,
        )

        df["par_spread"] = df["par_spread"].fillna(np.nan)

        return df

    par_df = add_par_spread_vectorized(bond_red_df)
    par_df = par_df.dropna(subset=["par_spread"])

    # keep only the important columns
    par_df = par_df[
        [
            "cusip",
            "date",
            "mat_days",
            "BOND_YIELD",
            "CS",
            "size_ig",
            "size_jk",
            "par_spread",
        ]
    ]

    # have had issues with a phantom array column
    def safe_convert(x):
        """Convert lists and arrays to tuples while keeping other data types unchanged."""
        if isinstance(x, list):
            return tuple(x)
        elif isinstance(x, np.ndarray):
            return (
                tuple(x.tolist()) if x.ndim > 0 else x.item()
            )  # Convert array to tuple if not scalar
        else:
            return x

    # Apply safe conversion
    par_df = par_df.map(safe_convert)
    par_df = par_df.drop_duplicates()

    return par_df


# THIS MAIN FUNCTION IS NOT DONE YET, WILL BE RESOLVED SOON or not at all


def main():
    """
    Main function to load data, process it, and merge Treasury data into Bonds.
    """
    print("Loading data...")
    # Keeping these global vars down here for now for ease of reference
    RED_CODE_FILE_NAME = "RED_and_ISIN_mapping.parquet"
    CORPORATES_MONTHLY_FILE_NAME = "corporate_bond_returns.parquet"
    CDS_FILE_NAME = (
        "markit_cds.parquet"  # Assuming this is the file name from Kaustaub's script
    )

    corp_bonds_data = pd.read_parquet(f"{DATA_DIR}/{CORPORATES_MONTHLY_FILE_NAME}")
    red_data = pd.read_parquet(f"{DATA_DIR}/{RED_CODE_FILE_NAME}")
    cds_data = pd.read_parquet(f"{DATA_DIR}/{CDS_FILE_NAME}")

    corp_red_data = merge_red_code_into_bond_treas(corp_bonds_data, red_data)
    final_data = merge_cds_into_bonds(corp_red_data, cds_data)
    # Missing a step of "process final data" from the ipynb

    print("Saving processed data...")
    corp_red_data.to_parquet(
        f"{DATA_DIR}/{'Red_Data.parquet'}"
    )  # change name of file as needed
    final_data.to_parquet(f"{DATA_DIR}/{'Final_data.parquet'}")

    print("Processing complete. Data saved.")


if __name__ == "__main__":
    main()
