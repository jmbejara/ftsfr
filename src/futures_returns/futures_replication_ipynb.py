# %%
"""
for this file, I am going to try the group-9 methods again and to see if any improvements could be made to improve the replication quality on the yang table 1 results, and to replicate the he-kelly-manela commodities return results.
"""

# %%
import pandas as pd
import load_futures_data

# %%
wrds_futures = load_futures_data.load_wrds_futures()

# %%
wrds_futures.head(5)

# %%
wrds_futures["contrdate"]


# %%
def parse_contrdate(c):
    """
    Parse a contract date string (MMYY or MM/YY) into a monthly pandas.Period.

    Parameters
    ----------
    c : str
        Contract date in the format 'MMYY' or 'MM/YY'.

    Returns
    -------
    pandas.Period
        A monthly Period object corresponding to the parsed year and month.
    """
    try:
        c = c.replace("/", "")
        mm = int(c[:2])
        yy = int(c[2:])
        year = 2000 + yy if yy < 50 else 1900 + yy
        return pd.Period(f"{year}-{mm:02d}", freq="M")
    except:
        return pd.NaT  # or None


def futures_series_to_monthly(df):
    """
    Convert a daily futures DataFrame into a monthly frequency by taking
    the last available daily row for each (futcode, month). Also parses
    contract periods and drops date columns to produce a final monthly dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain columns ['futcode', 'date_', 'contrdate', 'settlement'].

    Returns
    -------
    pandas.DataFrame
        Monthly data with columns ['futcode', 'contr_period', 'obs_period', 'settlement'].
        Each row corresponds to the last daily entry in that month for the given futcode.
    """

    df = df.sort_values(["futcode", "date"])
    monthly_df = df.groupby(["futcode", df["date"].dt.to_period("M")]).tail(1).copy()

    monthly_df["contr_period"] = monthly_df["contrdate"].apply(parse_contrdate)
    monthly_df["obs_period"] = monthly_df["date"].dt.to_period("M")

    monthly_df = monthly_df.drop(columns=["date", "contrdate"])
    monthly_df = monthly_df.sort_values(by=["obs_period", "contr_period"])
    return monthly_df


# %%
monthly_df = futures_series_to_monthly(wrds_futures)

# %%

monthly_df = monthly_df[~monthly_df["settlement"].isna()]

# %%
monthly_df[monthly_df["contr_period"].isna()]

# %%
# yang paper started at 01 1973
monthly_df

# %%

import numpy as np


def compute_monthly_basis(monthly_df):
    """
    Compute the monthly basis for each product and observation period.

    Parameters
    ----------
    monthly_df : pandas.DataFrame
        DataFrame with columns ['product_code', 'obs_period', 'contr_period', 'settlement'].
        Each row is a futures contract with a settlement price and a delivery date.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns ['product_code', 'obs_period', 'basis'] containing
        the log-slope basis for each product and observation period, annualized.
    """

    # Ensure correct types
    monthly_df = monthly_df.copy()
    # monthly_df["contr_period"] = pd.to_datetime(monthly_df["contr_period"]).dt.to_period("M")
    # monthly_df["obs_period"] = pd.to_datetime(monthly_df["obs_period"]).dt.to_period("M")

    # Calculate months to maturity
    monthly_df["months_to_maturity"] = (
        monthly_df["contr_period"] - monthly_df["obs_period"]
    ).apply(lambda x: x.n)

    # Filter only contracts with 1 <= maturity <= 12
    valid_contracts = monthly_df[
        (monthly_df["months_to_maturity"] >= 1)
        & (monthly_df["months_to_maturity"] <= 12)
    ]

    basis_list = []

    grouped = valid_contracts.groupby(["product_code", "obs_period"])

    for (product_code, obs_period), group in grouped:
        if group.shape[0] < 2:
            continue  # Skip if not enough contracts to compute slope

        group = group.sort_values("months_to_maturity")

        f1 = group.iloc[0]
        f2 = group.iloc[-1]

        T1 = f1["months_to_maturity"]
        T2 = f2["months_to_maturity"]

        try:
            log_diff = np.log(f1["settlement"]) - np.log(f2["settlement"])
            # I times 100 here to adhere to the group-9 formula and it actually presents a better result.
            basis = log_diff / (T2 - T1) * 100
            basis_annualized = basis * 12
            basis_list.append(
                {
                    "product_code": product_code,
                    "obs_period": obs_period,
                    "basis": basis_annualized,
                }
            )
        except (ValueError, ZeroDivisionError, FloatingPointError):
            continue

    basis_df = pd.DataFrame(basis_list)
    return basis_df


# %%
basis_df = compute_monthly_basis(monthly_df)

# %%
basis_df


# %%
def compute_excess_returns(monthly_df):
    df = monthly_df[["product_code", "obs_period", "contr_period", "settlement"]].copy()
    df.rename(
        columns={"obs_period": "t", "contr_period": "T", "settlement": "F"},
        inplace=True,
    )
    df["maturity"] = (df["T"] - df["t"]).apply(lambda x: x.n)
    df = df[df["maturity"] > 1]

    df_shifted = df.copy()
    df_shifted["t"] = df_shifted["t"] - 1
    df_shifted.rename(columns={"F": "F_next"}, inplace=True)

    merged = pd.merge(
        df,
        df_shifted[["product_code", "t", "T", "F_next"]],
        on=["product_code", "t", "T"],
        how="inner",
    )

    merged["excess_ret"] = merged["F_next"] / merged["F"] - 1

    summary = (
        merged.groupby("product_code")["excess_ret"]
        .agg(
            mean_ret=lambda x: x.mean() * 12,
            std_ret=lambda x: x.std() * np.sqrt(12),
            n="count",
        )
        .reset_index()
    )
    summary["Sharpe_ratio"] = summary["mean_ret"] / summary["std_ret"]
    return merged, summary


# %%
def compute_summary_stats(basis_df: pd.DataFrame) -> pd.DataFrame:
    """
    Replicates Table 1 in Yang (2013) using basis data:
    - Basis (mean)
    - Frequency of backwardation
    - E[Re] = mean return
    - σ[Re] = std dev of return
    - Sharpe ratio

    Parameters
    ----------
    basis_df : pd.DataFrame
        Must contain columns ['product_code', 'obs_period', 'basis']

    Returns
    -------
    pd.DataFrame
        Summary statistics for each product
    """
    summary_list = []

    for code, group in basis_df.groupby("product_code"):
        basis = group["basis"].mean()
        n_obs = group["basis"].count()
        freq_bw = (group["basis"] > 0).mean() * 100
        # expected_ret = excess_return_df["excess_return"].mean()
        # std_ret = group["basis"].std()
        # sharpe = expected_ret / std_ret if std_ret != 0 else np.nan

        summary_list.append(
            {
                "product_code": code,
                "N": n_obs,
                "Basis": basis,
                "Freq. of bw.": freq_bw,
                # "E[Re]": expected_ret,
                # "σ[Re]": std_ret,
                # "Sharpe ratio": sharpe
            }
        )

    return pd.DataFrame(summary_list)


# %%
sample_df = basis_df[
    (basis_df["obs_period"] >= "1970-01") & (basis_df["obs_period"] <= "2008-12")
]

# %%
summary_df = compute_summary_stats(sample_df)

# %%
summary_df

# %%
PRODUCT_NAME_MAP = {
    3160: "Barley",
    289: "Butter",
    3161: "Canola",
    1980: "Cocoa",
    2038: "Coffee",
    3247: "Corn",
    1992: "Cotton",
    361: "Lumber",
    385: "Oats",
    2036: "Orange Juice",
    379: "Rough Rice",
    3256: "Soybean Meal",
    396: "Soybeans",
    430: "Wheat",
    1986: "Crude Oil",
    2091: "Gasoline",
    2029: "Heating Oil",
    2060: "Natural Gas",
    3847: "Propane",
    2032: "Unleaded Gas",
    3250: "Feeder Cattle",
    2676: "Lean Hogs",
    2675: "Live Cattle",
    3126: "Aluminum",
    2087: "Coal",
    2026: "Copper",
    2020: "Gold",
    2065: "Palladium",
    2074: "Platinum",
    2108: "Silver",
}

summary_df["Commodity"] = summary_df["product_code"].map(PRODUCT_NAME_MAP)

# %%
summary_df

# %%
import pandas as pd

# Manually reloading the structured data from the LaTeX table (N and Basis columns only)
data = [
    # Agriculture
    ["Barley", "WA", 235, -3.66],
    ["Butter", "02", 141, -3.68],
    ["Canola", "WC", 377, -2.98],
    ["Cocoa", "CC", 452, -2.61],
    ["Coffee", "KC", 420, -2.57],
    ["Corn", "C-", 468, -6.03],
    ["Cotton", "CT", 452, -1.75],
    ["Lumber", "LB", 468, -5.63],
    ["Oats", "O-", 468, -5.65],
    ["Orange Juice", "JO", 448, -3.08],
    ["Rough Rice", "RR", 265, -7.56],
    ["Soybean Meal", "SM", 468, 0.20],
    ["Soybeans", "S-", 468, -0.58],
    ["Wheat", "W-", 468, -2.88],
    # Energy
    ["Crude Oil", "CL", 295, 4.25],
    ["Gasoline", "RB", 275, 8.09],
    ["Heating Oil", "HO", 345, 1.49],
    ["Natural Gas", "NG", 216, -3.63],
    ["Propane", "PN", 247, 5.53],
    ["Unleaded Gas", "HU", 250, 8.62],
    # Livestock
    ["Broilers", "BR", 19, 4.58],
    ["Feeder Cattle", "FC", 443, 0.35],
    ["Lean Hogs", "LH", 468, 2.66],
    ["Live Cattle", "LC", 468, 0.46],
    # Metals
    ["Aluminum", "AL", 215, 1.06],
    ["Coal", "QL", 85, -1.55],
    ["Copper", "HG", 412, 0.52],
    ["Gold", "GC", 400, -6.24],
    ["Palladium", "PA", 362, -2.16],
    ["Platinum", "PL", 410, -3.21],
    ["Silver", "SI", 419, -6.51],
]

# Create DataFrame
paper_table = pd.DataFrame(data, columns=["Commodity", "Symbol", "N", "Basis"])


# %%
paper_table

# %%
comparison_df = summary_df.merge(paper_table, on="Commodity")
comparison_df["N_diff"] = comparison_df["N_x"] - comparison_df["N_y"]
comparison_df["Basis_diff"] = comparison_df["Basis_x"] - comparison_df["Basis_y"]
comparison_df["Basis_pct"] = comparison_df["Basis_diff"] / comparison_df["Basis_y"]
comparison_df["N_pct"] = comparison_df["N_diff"] / comparison_df["N_y"]
comparison_df[["Commodity", "Basis_diff", "Basis_pct", "N_diff", "N_pct"]]

# %%
monthly_df


# %%
def compute_monthly_excess_return(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute monthly excess return for each commodity and contract maturity.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: ['product_code', 'obs_period', 'contr_period', 'settlement']

    Returns
    -------
    pd.DataFrame
        DataFrame with added 'excess_return' column.
    """
    df = df.copy()

    # Convert period columns to datetime
    # df['obs_period'] = pd.to_datetime(df['obs_period'])
    # df['contr_period'] = pd.to_datetime(df['contr_period'])

    # Sort for lagging purposes
    # what if shift one goes to the previous one? with differnet product number?
    df.sort_values(by=["product_code", "contr_period", "obs_period"], inplace=True)

    # Group by product_code and contract maturity
    df["F_t"] = df["settlement"]
    df["F_t+1"] = df.groupby(["product_code", "contr_period"])["settlement"].shift(-1)

    # Compute return (only when both F_t and F_t+1 are available)
    df["excess_return"] = df["F_t+1"] / df["F_t"] - 1
    df = df.dropna(subset=["excess_return"])

    return df


# %%
compute_monthly_excess_return(monthly_df)


# %%
def summarize_excess_return(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize monthly excess return statistics by product_code.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain: 'product_code', 'excess_return', 'basis' (optional)

    Returns
    -------
    pd.DataFrame
        Summary table with N, Basis, Freq. of bw., E[Re], σ[Re], Sharpe ratio
    """
    grouped = df.groupby("product_code")

    summary = pd.DataFrame(
        {
            # "N": grouped.size(),
            # "Basis": grouped["basis"].mean() * 12 if "basis" in df.columns else np.nan,
            # "Freq. of bw.": grouped.apply(lambda g: (g["basis"] > 0).mean() * 100 if "basis" in g else np.nan),
            "E[Re]": grouped["excess_return"].mean() * 12 * 100,
            "σ[Re]": grouped["excess_return"].std(ddof=0) * np.sqrt(12) * 100,
        }
    )

    summary["Sharpe ratio"] = summary["E[Re]"] / summary["σ[Re]"] * 100

    return summary


# %%
summary_df_with_sharpe = summarize_excess_return(
    compute_monthly_excess_return(monthly_df)
)

# %%
summary_df_with_sharpe = summary_df_with_sharpe.reset_index()

# %%
summary_df_with_sharpe["Commodity"] = summary_df_with_sharpe["product_code"].map(
    PRODUCT_NAME_MAP
)

# %%
summary_df_with_sharpe

# %%
monthly_excess_return = compute_monthly_excess_return(monthly_df)

# %%
monthly_excess_return["months_to_maturity"] = (
    monthly_excess_return["contr_period"] - monthly_excess_return["obs_period"]
).apply(lambda x: x.n)

# %%
monthly_excess_return

# %%
df_filtered = monthly_excess_return[monthly_excess_return["months_to_maturity"] <= 4]
he_rep_returns = (
    df_filtered.groupby(["product_code", "obs_period"])["excess_return"]
    .mean()
    .reset_index()
)

# %%
he_rep_returns["Commodity"] = he_rep_returns["product_code"].map(PRODUCT_NAME_MAP)

# %%
returns_pivot = he_rep_returns.pivot(
    index="obs_period", columns="Commodity", values="excess_return"
)

# %%
returns_pivot


# %%
import sys
from pathlib import Path

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# Plotting style
sns.set()

# Add project root to path
project_root = Path().resolve().parent
sys.path.insert(0, str(project_root))

# Load project modules
from he_kelly_manela import pull_he_kelly_manela

# Load project settings
from settings import config

DATA_DIR = Path(config("DATA_DIR")) / "cds_returns"
HE_DATA_DIR = Path(config("DATA_DIR")) / "he_kelly_manela"


# %%

he_kelly = pull_he_kelly_manela.load_he_kelly_manela_all(data_dir=HE_DATA_DIR)

he_kelly.columns.str.contains("cmd").sum()

# %%

col_lst = ["yyyymm"]
for i in range(1, 10):
    col_lst.append(f"Commod_0{i}")
for i in range(10, 24):
    col_lst.append(f"Commod_{i}")

# %%
he_kelly_df = he_kelly[col_lst].dropna(axis=0)
he_kelly_df["Month"] = pd.to_datetime(
    he_kelly_df["yyyymm"].astype(int).astype(str), format="%Y%m"
)
he_kelly_df = he_kelly_df.drop(columns="yyyymm")
he_kelly_df = he_kelly_df.set_index("Month")


# %%
he_kelly_df

# %%
returns_pivot = returns_pivot.fillna(0)
returns_pivot = returns_pivot.reset_index().set_index("obs_period")

# %%
returns_pivot.index = returns_pivot.index.rename("Month")

# %%
he_kelly_df.index

# %%
he_kelly_df.index = he_kelly_df.index.to_period("M")


# %%
returns_pivot = returns_pivot["1986-09":"2012-12"]

# %%
corr_matrix = pd.DataFrame(index=returns_pivot.columns, columns=he_kelly_df.columns)


for col1 in returns_pivot.columns:
    for col2 in he_kelly_df.columns:
        x = returns_pivot[col1].fillna(0)
        y = he_kelly_df[col2].fillna(0)
        corr_matrix.loc[col1, col2] = x.corr(y)

# %%
returns_pivot

# %%
corr_matrix

# %%
corr_matrix_float = corr_matrix.astype(float)
import seaborn as sns


corr_matrix = corr_matrix.astype(float)

plt.figure(figsize=(10, 8))

sns.heatmap(
    corr_matrix_float,
    annot=False,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    square=True,
    linewidths=0.5,
    cbar=True,
)

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()
