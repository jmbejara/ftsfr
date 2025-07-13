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
    df["FR"] = df["CS"]
    df["CB"] = df["par_spread"] - df["FR"]
    df["rfr"] = df["BOND_YIELD"] - df["CS"] - df["CB"]

    df = df[df["rfr"].abs() < 1]  # remove unreasonable data, rfr is in absolute space

    rating_map = {(0, 1): 0, (1, 0): 1, (1, 1): 2}

    # build a tuple series, then map
    df["c_rating"] = df[["size_ig", "size_jk"]].apply(tuple, axis=1).map(rating_map)

    return df


def generate_graph(df, col="rfr", col2=None, two=False):
    """
    Generates a time series plot for given columns based on c_rating.

    Parameters:
    - df: DataFrame with columns ['date', 'c_rating', col, (col2)]
    - col: primary series name (default 'rfr')
    - col2: secondary series name if two=True
    - two: if True, plots col2 on a secondary y-axis
    """
    # ensure datetime
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # group once for both columns
    if two and col2 is not None:
        df_grouped = df.groupby(["date", "c_rating"])[[col, col2]].mean().reset_index()
    else:
        df_grouped = df.groupby(["date", "c_rating"])[col].mean().reset_index()

    # prepare figure
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # colors/markers for up to 3 categories—extend as needed
    primary_colors = ["tab:blue", "tab:orange", "tab:green"]
    primary_markers = ["o", "s", "^"]

    # plot each c_rating on primary axis
    for idx, rating in enumerate(sorted(df_grouped["c_rating"].unique())):
        series = df_grouped[df_grouped["c_rating"] == rating]
        ax1.plot(
            series["date"],
            series[col],
            label=f"rating {rating} → {col}",
            color=primary_colors[idx % len(primary_colors)],
            marker=primary_markers[idx % len(primary_markers)],
            linestyle="-",
        )

    ax1.set_xlabel("Date")
    ax1.set_ylabel(f"{col}", color="black")
    ax1.tick_params(axis="y", labelcolor="black")
    ax1.grid(True)
    ax1.legend(loc="upper left")

    # secondary axis for col2
    if two and col2 is not None:
        ax2 = ax1.twinx()
        secondary_markers = ["x", "d", "P"]
        secondary_colors = ["tab:red", "tab:purple", "tab:cyan"]

        for idx, rating in enumerate(sorted(df_grouped["c_rating"].unique())):
            series = df_grouped[df_grouped["c_rating"] == rating]
            ax2.plot(
                series["date"],
                series[col2],
                label=f"rating {rating}: {col2}",
                color=secondary_colors[idx % len(secondary_colors)],
                marker=secondary_markers[idx % len(secondary_markers)],
                linestyle="--",
            )

        ax2.set_ylabel(f"{col2}", color="black")
        ax2.tick_params(axis="y", labelcolor="black")
        ax2.legend(loc="upper right")

    # title & save
    title = f"Time Series of {col}" + (f" vs {col2}" if two and col2 else "")
    plt.title(title)
    # outpath = OUTPUT_DIR / f"{title.replace(' ', '_')}.png"
    # fig.savefig(outpath, bbox_inches='tight')
    plt.show()
