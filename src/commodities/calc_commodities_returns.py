import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import extract_hkm_cmdty
import load_futures_data
import pandas as pd
from replicate_cmdty import generate_corr_matrix, decide_optimal_pairs
from settings import config

DATA_DIR = config("DATA_DIR")
BASE_DIR = Path(config("BASE_DIR"))

metal_map = {
    "Aluminum": ("LMAHDY Comdty_PX_LAST", "LMAHDS03 Comdty_PX_LAST"),
    "Nickel": ("LMNIDY Comdty_PX_LAST", "LMNIDS03 Comdty_PX_LAST"),
    "Lead": ("LMPBDY Comdty_PX_LAST", "LMPBDS03 Comdty_PX_LAST"),
    "Zinc": ("LMZSDY Comdty_PX_LAST", "LMZSDS03 Comdty_PX_LAST"),
    "Copper": ("LMCADY Comdty_PX_LAST", "LMCADS03 Comdty_PX_LAST"),
}
ticker_to_commodity = {
    "CO2 Comdty_PX_LAST": "Crude Oil",
    "QS2 Comdty_PX_LAST": "Gasoil",
    "CL2 Comdty_PX_LAST": "WTI Crude",
    "XB2 Comdty_PX_LAST": "Unl. Gasoline",
    "HO2 Comdty_PX_LAST": "Heating Oil",
    "NG2 Comdty_PX_LAST": "Natural Gas",
    "CT2 Comdty_PX_LAST": "Cotton",
    "KC2 Comdty_PX_LAST": "Coffee",
    "CC2 Comdty_PX_LAST": "Cocoa",
    "SB2 Comdty_PX_LAST": "Sugar",
    "S 2 Comdty_PX_LAST": "Soybeans",
    "KW2 Comdty_PX_LAST": "Kansas Wheat",
    "C 2 Comdty_PX_LAST": "Corn",
    "W 2 Comdty_PX_LAST": "Wheat",
    "LH2 Comdty_PX_LAST": "Lean Hogs",
    "FC2 Comdty_PX_LAST": "Feeder Cattle",
    "LC2 Comdty_PX_LAST": "Live Cattle",
    "GC2 Comdty_PX_LAST": "Gold",
    "SI2 Comdty_PX_LAST": "Silver",
    "Aluminum": "Aluminum",
    "Nickel": "Nickel",
    "Lead": "Lead",
    "Zinc": "Zinc",
    "Copper": "Copper",
}


def wide_to_long_returns(df, list_of_return_ticker):
    """
    Converts a wide-format return DataFrame to long-format with columns: ds, unique_id, y
    """

    if "yyyymm" in df.columns:
        id_col = "yyyymm"
    elif "Date" in df.columns:
        id_col = "Date"
    else:
        raise ValueError("No date column found!")

    cols = [id_col] + list_of_return_ticker
    df_sub = df[cols].copy()

    df_long = df_sub.melt(
        id_vars=id_col,
        value_vars=list_of_return_ticker,
        var_name="unique_id",
        value_name="y",
    )
    df_long = df_long.rename(columns={id_col: "ds"})

    df_long = df_long.dropna(subset=["y"])

    df_long = df_long.sort_values(["unique_id", "ds"]).reset_index(drop=True)

    return df_long[["unique_id", "ds", "y"]]


def calc_return_manual(df):
    df = df[df["Contract"] <= 4]
    df["Date"] = pd.to_datetime(df["Date"])
    df["YearMonth"] = df["Date"].dt.to_period("M")
    last_prices = (
        df.groupby(["Commodity", "YearMonth", "Contract"])
        .apply(lambda x: x.loc[x["Date"].idxmax()])
        .reset_index(drop=True)
    )
    avg_price = (
        last_prices.groupby(["Commodity", "YearMonth"])["ClosePrice"]
        .mean()
        .reset_index()
    )
    avg_price_pivot = avg_price.pivot(
        index="YearMonth", columns="Commodity", values="ClosePrice"
    )
    monthly_return = avg_price_pivot.pct_change()
    # pivot_table = df.pivot_table(values='ClosePrice', index=['YearMonth'],columns="Commodity", aggfunc="mean")
    monthly_return["Month"] = pd.to_datetime(
        monthly_return.index.astype(str), format="%Y-%m"
    )
    monthly_return["yyyymm"] = monthly_return["Month"].dt.strftime("%Y%m")
    monthly_return = monthly_return.set_index("yyyymm")
    return monthly_return


def generate_replication_gsci(data_dir=DATA_DIR):
    df_return1 = load_futures_data.load_gsci_data(data_dir=data_dir)
    hkm_df = extract_hkm_cmdty.extract_hkm_cmdty(
        data_dir=BASE_DIR / "_data" / "he_kelly_manela"
    )
    corr_matrix1 = generate_corr_matrix(df_return1, hkm_df)
    corr_matrix_float1 = corr_matrix1.astype(float)
    optimal_pairs_df1, _, _ = decide_optimal_pairs(corr_matrix_float1)
    optimal_pairs_df1["GSCI Index"] = optimal_pairs_df1["Commodity_1"].str.replace(
        "_PX_LAST_Return", "", regex=False
    )
    # optimal_pairs_df1 = optimal_pairs_df1.rename(columns={"Commodity_2": "HKM Column Name"})
    list_of_return_ticker = optimal_pairs_df1["Commodity_1"].to_list()
    gsci_replication_df = wide_to_long_returns(df_return1, list_of_return_ticker)

    return gsci_replication_df


def calc_lme_monthly_1mprice(lme_df, metal_map, date_col="index", price_func=None):
    df = lme_df.copy()
    df["Date"] = pd.to_datetime(df[date_col])
    df = df.sort_values("Date").drop(columns=[date_col])

    for cash_col, m3_col in metal_map.values():
        df[cash_col] = pd.to_numeric(df[cash_col], errors="coerce")
        df[m3_col] = pd.to_numeric(df[m3_col], errors="coerce")

    if price_func is None:
        price_func = lambda cash, m3: cash + (m3 - cash) / 3

    price_df = pd.DataFrame(index=df.index)
    for metal, (cash_col, m3_col) in metal_map.items():
        price_df[metal] = price_func(df[cash_col], df[m3_col])

    price_df["Date"] = df["Date"]
    price_df["Month"] = price_df["Date"].dt.to_period("M")
    price_df = price_df.sort_values("Date")
    price_monthly = price_df.groupby("Month").last()

    price_monthly["yyyymm"] = price_monthly.index.strftime("%Y%m")
    price_monthly["Date"] = price_monthly.index.to_timestamp("M")

    cols = ["yyyymm", "Date"] + [
        c for c in price_monthly.columns if c not in ["yyyymm", "Date", "Month"]
    ]
    price_monthly = price_monthly[cols].reset_index(drop=True)

    return price_monthly


def calc_lme_monthly_return(price_monthly):
    ret_df = price_monthly.copy()
    value_cols = [col for col in ret_df.columns if col not in ["yyyymm", "Date"]]
    ret_only = ret_df[value_cols].pct_change()
    ret_only["yyyymm"] = ret_df["yyyymm"]
    ret_only["Date"] = ret_df["Date"]
    ret_only = ret_only[
        ["yyyymm", "Date"]
        + [col for col in value_cols if col not in ["yyyymm", "Date"]]
    ]
    ret_only = ret_only.dropna(subset=[value_cols[0]]).reset_index(drop=True)
    return ret_only


def compute_second_contract_return(commodity_futures_df, date_col="index"):
    df = commodity_futures_df.copy()
    df["Date"] = pd.to_datetime(df[date_col])
    df = df.sort_values("Date").drop(columns=[date_col])
    df["Month"] = df["Date"].dt.to_period("M")
    df_monthly = df.groupby("Month").last()

    second_contract_cols = [
        col for col in df_monthly.columns if col.endswith("2 Comdty_PX_LAST")
    ]
    for col in second_contract_cols:
        df_monthly[col] = pd.to_numeric(df_monthly[col], errors="coerce")

    ret_df = df_monthly[second_contract_cols].pct_change(fill_method=None)
    ret_df["yyyymm"] = ret_df.index.strftime("%Y%m")
    ret_df["Date"] = ret_df.index.to_timestamp("M")

    ret_df = ret_df.reset_index(drop=True)
    cols = ["yyyymm", "Date"] + second_contract_cols
    ret_df = ret_df[cols]

    return ret_df


def generate_replication_future_ticker(data_dir=DATA_DIR):
    hkm_df = extract_hkm_cmdty.extract_hkm_cmdty(
        data_dir=BASE_DIR / "_data" / "he_kelly_manela"
    )
    commodity_futures_df = load_futures_data.load_commodities_future(data_dir=data_dir)
    lme_df = load_futures_data.load_lme_metals(data_dir=data_dir)
    monthly_1mprice = calc_lme_monthly_1mprice(lme_df, metal_map, date_col="index")
    lme_monthly_return = calc_lme_monthly_return(monthly_1mprice)

    cmt_monthly_return = compute_second_contract_return(commodity_futures_df)
    combined_df = pd.merge(
        cmt_monthly_return,
        lme_monthly_return.drop(columns=["Date"]),
        how="inner",
        on=["yyyymm"],
        suffixes=("", "_LME"),
    ).set_index("yyyymm")
    common_idx = hkm_df.index.intersection(combined_df.index)
    he_kelly_sub = hkm_df.loc[common_idx]
    carry_sub = combined_df.loc[common_idx]
    corr_matrix2 = generate_corr_matrix(he_kelly_sub, carry_sub)
    corr_matrix_float2 = corr_matrix2.astype(float)
    optimal_pairs_df2, _, _ = decide_optimal_pairs(corr_matrix_float2)

    optimal_pairs_df2["Commodity_Name"] = optimal_pairs_df2["Commodity_2"].map(
        ticker_to_commodity
    )
    list_of_return_ticker = optimal_pairs_df2["Commodity_2"].to_list()
    gsci_replication_df = wide_to_long_returns(combined_df, list_of_return_ticker)
    return gsci_replication_df


def monthly_returns_mixed_prices(
    df_in: pd.DataFrame,
    date_col: str = "index",
    suffixes: tuple = ("Comdty_PX_LAST", "Curncy_PX_LAST"),
) -> pd.DataFrame:
    """
    Compute end-of-month simple returns for columns ending with the given suffixes,
    e.g. "... Comdty_PX_LAST" and/or "... Curncy_PX_LAST". Works with both
    single-level and MultiIndex columns. Returns are based on month-end prices.

    Output index: 'yyyymm' (string), with a 'Date' month-end timestamp column.

    Parameters
    ----------
    df_in : pd.DataFrame
        Source DataFrame containing a date column and price columns.
    date_col : str, default "index"
        Name of the date-like column to parse.
    suffixes : tuple, default ("Comdty_PX_LAST", "Curncy_PX_LAST")
        Column suffixes to include when extracting price series.

    Returns
    -------
    pd.DataFrame
        ["yyyymm", "Date", <one column per selected instrument>],
        where each instrument column is the monthly simple return.
    """
    df = df_in.copy()

    # 1) Parse and sort by date to ensure month-end selection is correct
    df["Date"] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.sort_values("Date")

    # 2) Extract price columns for the requested suffixes
    if isinstance(df.columns, pd.MultiIndex):
        # Collect sub-frames for each suffix level and merge them
        collected = []
        for sfx in suffixes:
            if sfx in df.columns.get_level_values(-1):
                sub = df.xs(sfx, axis=1, level=-1)  # remaining levels become columns
                # Avoid name collisions by appending a short tag when needed
                short_tag = "curncy" if "Curncy" in sfx else "comdty"
                new_cols = []
                seen = set()
                for c in sub.columns.astype(str):
                    name = c
                    if name in seen:
                        name = f"{name}_{short_tag}"
                    seen.add(name)
                    new_cols.append(name)
                sub.columns = new_cols
                collected.append(sub)

        if not collected:
            raise ValueError(f"No MultiIndex columns with last level in {suffixes} found.")
        price_df = pd.concat(collected, axis=1)

    else:
        # Single-level columns: keep those that end with any of the suffixes
        sel_cols = [c for c in df.columns if any(str(c).endswith(sfx) for sfx in suffixes)]
        if not sel_cols:
            raise ValueError(f"No columns ending with any of {suffixes} were found.")
        price_df = df[sel_cols].copy()

        # Normalize names by stripping the matched suffix; if collision, append a tag
        normalized = []
        seen = set()
        for c in price_df.columns:
            s = str(c)
            matched = None
            for sfx in suffixes:
                if s.endswith(sfx):
                    matched = sfx
                    break
            base = s[: -len(matched)].rstrip() if matched else s
            name = base
            if name in seen:
                tag = "curncy" if matched and "Curncy" in matched else "comdty"
                name = f"{base}_{tag}"
            seen.add(name)
            normalized.append(name)
        price_df.columns = normalized

    # Convert to numeric in case of object dtypes
    price_df = price_df.apply(pd.to_numeric, errors="coerce")

    # 3) Month-end prices = last available obs in each calendar month
    price_df["Month"] = df["Date"].dt.to_period("M")
    monthly_px = price_df.groupby("Month").last()

    # 4) Simple monthly returns; for log returns use: np.log(monthly_px).diff()
    rets = monthly_px.pct_change()

    # 5) Package output: 'yyyymm' index + month-end 'Date' column
    out = rets.copy()
    out["yyyymm"] = out.index.strftime("%Y%m")
    out["Date"] = out.index.to_timestamp("M")

    cols = ["yyyymm", "Date"] + [c for c in rets.columns]
    out = out.reset_index(drop=True)[cols]
    out = out.set_index("yyyymm")
    return out

def load_commodities_returns(data_dir=DATA_DIR):
    df_gsci = generate_replication_gsci(data_dir=data_dir)
    return df_gsci

if __name__ == "__main__":
    # Output paths
    path_gsci = DATA_DIR / "futures_returns_gsci.parquet"
    path_ticker = DATA_DIR / "futures_returns_future_ticker.parquet"

    # Create directory if needed
    path_gsci.parent.mkdir(parents=True, exist_ok=True)

    # Generate and save replication data
    df_gsci = generate_replication_gsci(data_dir=DATA_DIR)
    df_gsci.to_parquet(path_gsci)

    df_ticker = generate_replication_future_ticker(data_dir=DATA_DIR)
    df_ticker.to_parquet(path_ticker)


    print("Replication outputs saved as pickle files:")
    print(f" - GSCI-based: {path_gsci}")
    print(f" - Futures ticker-based: {path_ticker}")
