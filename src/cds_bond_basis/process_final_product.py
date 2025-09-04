# from settings import config
import pandas as pd
from matplotlib import pyplot as plt

# OUTPUT_DIR = config("OUTPUT_DIR")
# DATA_DIR = config("DATA_DIR")

# FINAL_ANALYSIS_FILE_NAME = "final_data.parquet"


def process_cb_spread(df):
    """
    INPUT WAS PREVIOUS FINAL PRODUCT
    df: dataframe with par spread values merged into all values where there was a possible cubic spline
       'cusip', -- cusip of the entire bond issue, unique bond identifier
       'date', -- reporting date
       'mat_days', -- days till maturity
       BOND_YIELD, -- MMN adjusted bond yield
       'CS', -- credit spread
        'size_ig', -- 0 if no ig bonds in portfolio, 1 if yes
        'size_jk', -- 0 if no junk bonds in portfolio, 1 if yes
       'par_spread', -- parspread of CDS, backed out by Cubic Spline

    output:
        additional columns:
        FR: Z-spread of the bond
            FR = CS column
        CB: implied return on CDS-bond spread
            CB = par_spread - FR
        rfr: implied risk free rate
            rfr = (BOND_YIELD - CS) - CB
        contain_rating: if it has IG or Junk bonds
            0 if it contains Junk
            1 if it contains IG
        c_rating: IG, Junk, or combo
            0 if it only contains Junk
            1 if it only contains IG
            2 if it contains both
    """
    df = df.copy()
    df["FR"] = df["CS"]
    df["CB"] = df["par_spread"] - df["FR"]
    df["rfr"] = df["BOND_YIELD"] - df["CS"] - df["CB"]

    df = df[df["rfr"].abs() < 1]  # remove unreasonable data, rfr is in absolute space

    # change to percent
    df["rfr"] = df["rfr"] * 100

    # labeling
    rating_map = {(0, 1): "High Yield", (1, 0): "Investment Grade", (1, 1): "IG + HY"}

    # build a tuple series, then map
    df["c_rating"] = df[["size_ig", "size_jk"]].apply(tuple, axis=1).map(rating_map)

    return df


def output_cb_final_products(df):
    """
    INPUT is from previous function

    df: dataframe with par spread values merged into all values where there was a possible cubic spline
        'cusip', -- cusip of the entire bond issue, unique bond identifier
        'date', -- reporting date
        'mat_days', -- days till maturity
        BOND_YIELD, -- MMN adjusted bond yield
        'CS', -- credit spread
            'size_ig', -- 0 if no ig bonds in portfolio, 1 if yes
            'size_jk', -- 0 if no junk bonds in portfolio, 1 if yes
        'par_spread', -- parspread of CDS, backed out by Cubic Spline
    additional columns:
    FR: Z-spread of the bond
        FR = CS column
    CB: implied return on CDS-bond spread
        CB = par_spread - FR
    rfr: implied risk free rate
        rfr = (BOND_YIELD - CS) - CB
    contain_rating: if it has IG or Junk bonds
        0 if it contains Junk
        1 if it contains IG
    c_rating: IG, Junk, or combo
        "High Yield" if it only contains Junk
        "Investment Grade" if it only contains IG
        "IG + HY" if it contains both

    output:
        agg_df: aggregated dataframe where data is combined
            date: date of the aggregated collection
            c_rating: IG, Junk, or combo
                0 if it only contains Junk
                1 if it only contains IG
                2 if it contains both
            rfr: implied risk free rate
                desired value from stat arbitrage
        non_agg_df: non aggregated dataframe, keeping individual bond issue
            date: date of bond data
            cusip: cusip of the entire bond issue, unique bond identifier
            rfr: implied risk free rate
                desired value from stat arbitrage

    """

    # filter out for combination of IG and HY
    df = df.loc[df["c_rating"] != "IG + HY"]
    
    # outliers were removed so aggregation should be ok
    agg_df = df[["c_rating", "date", "rfr"]].groupby(["c_rating", "date"]).mean().reset_index()

    # no grouping or aggregation here
    non_agg_df = df[["cusip", "date", "rfr"]]

    return agg_df, non_agg_df


def generate_graph(df, col="rfr"):
    """
    Generates a time series plot for given columns based on c_rating.

    Parameters:
    - df: DataFrame with columns ['date', 'c_rating', col]
    - col: primary series name (default 'Implied Risk-Free Rate (percent)')
    """
    # ensure datetime
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # group by date and rating
    df_grouped = df.groupby(["date", "c_rating"])[col].mean().reset_index()

    # prepare figure
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # color palette (extendable)
    primary_colors = [
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red",
        "tab:purple",
        "tab:brown",
    ]

    handles_all, labels_all = [], []

    # plot each rating as a separate line
    for idx, rating in enumerate(["High Yield", "Investment Grade"]):
        series = df_grouped[df_grouped["c_rating"] == rating]
        (ln,) = ax1.plot(
            series["date"],
            series[col],
            label=f"rating {rating}",
            color=primary_colors[idx % len(primary_colors)],
            linewidth=1.0,
        )
        handles_all.append(ln)
        labels_all.append(f"{rating}")

    # horizontal zero line
    ax1.axhline(0, color="black", linewidth=0.8)

    # labels and grid
    ax1.set_xlabel("Dates")
    ax1.set_ylabel(f"{'Implied Risk-Free Rate (percent)'}", color="black")
    ax1.tick_params(axis="y", labelcolor="black")
    ax1.grid(True, linewidth=0.3, alpha=0.7)
    ax1.legend(
        handles_all,
        labels_all,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.25),
        ncol=min(len(labels_all), 6),
        frameon=False,
        fontsize=10,
    )
    # adjust layout to fit legend
    plt.subplots_adjust(bottom=0.25)
    plt.show()
