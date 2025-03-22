import pandas as pd
import pull_CRSP_Compustat
import pull_ken_french_data
from calc_Fama_French_1993 import (
    calc_book_equity_and_years_in_compustat,
    calculate_market_equity,
    compare_with_actual_ff_factors,
    create_Fama_French_factors,
    create_fama_french_portfolios,
    subset_CRSP_to_common_stock_and_exchanges,
)
from pandas import Timestamp
from pandas.testing import assert_frame_equal

from settings import config

DATA_DIR = config("DATA_DIR")


comp = pull_CRSP_Compustat.load_compustat(data_dir=DATA_DIR)
crsp = pull_CRSP_Compustat.load_CRSP_stock_ciz(data_dir=DATA_DIR)
ccm = pull_CRSP_Compustat.load_CRSP_Comp_Link_Table(data_dir=DATA_DIR)


def test_calc_book_equity_and_years_in_compustat():
    comp = pull_CRSP_Compustat.load_compustat(data_dir=DATA_DIR)
    comp = calc_book_equity_and_years_in_compustat(comp)

    output = comp[["gvkey", "datadate", "be"]].head(10)
    # expected = misc_tools.df_to_literal(output)
    # print(expected)
    expected = pd.DataFrame(
        {
            "gvkey": [
                "001000",
                "001000",
                "001000",
                "001000",
                "001000",
                "001000",
                "001000",
                "001000",
                "001000",
                "001000",
            ],
            "datadate": [
                Timestamp("1961-12-31 00:00:00"),
                Timestamp("1962-12-31 00:00:00"),
                Timestamp("1963-12-31 00:00:00"),
                Timestamp("1964-12-31 00:00:00"),
                Timestamp("1965-12-31 00:00:00"),
                Timestamp("1966-12-31 00:00:00"),
                Timestamp("1967-12-31 00:00:00"),
                Timestamp("1968-12-31 00:00:00"),
                Timestamp("1969-12-31 00:00:00"),
                Timestamp("1970-12-31 00:00:00"),
            ],
            "be": [
                None,
                None,
                0.561,
                0.627,
                0.491,
                0.834,
                0.744,
                2.571,
                10.211,
                10.544,
            ],
        },
        index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    )

    assert_frame_equal(output, expected, rtol=1e-3)


def test_subset_CRSP_to_common_stock_and_exchanges():
    crsp = pull_CRSP_Compustat.load_CRSP_stock_ciz(data_dir=DATA_DIR)
    crsp = subset_CRSP_to_common_stock_and_exchanges(crsp)

    output = crsp.loc[crsp["jdate"] <= "2022", :].shape
    expected = (3348395, 16)

    assert output == expected


def test_calculate_market_equity():
    crsp = pull_CRSP_Compustat.load_CRSP_stock_ciz(data_dir=DATA_DIR)
    crsp = subset_CRSP_to_common_stock_and_exchanges(crsp)
    crsp2 = calculate_market_equity(crsp)

    output = crsp2[["permco", "mthcaldt", "me"]].head()
    # expected = misc_tools.df_to_literal(output)
    # print(expected)

    expected = pd.DataFrame(
        {
            "permco": [7952, 7952, 7952, 7952, 7952],
            "mthcaldt": [
                Timestamp("1986-01-31 00:00:00"),
                Timestamp("1986-02-28 00:00:00"),
                Timestamp("1986-03-31 00:00:00"),
                Timestamp("1986-04-30 00:00:00"),
                Timestamp("1986-05-30 00:00:00"),
            ],
            "me": [16100.0, 11960.0, 16330.0, 15172.0, 11793.859375],
        },
        index=[1109366, 1115040, 1120723, 1126421, 1132127],
    )
    assert_frame_equal(output, expected, rtol=1e-3)


def test_fama_french_portfolios():
    ff_portfolios = pull_ken_french_data.load_sheet("6_Portfolios_2x3", sheet_name="0")
    column_map = {
        "BIG HiBM": "BH",  # Big stocks with high BM
        "BIG LoBM": "BL",  # Big stocks with low BM
        "ME1 BM2": "BME",  # The medium BM portfolio for big stocks
        # (ME1 is Market Equity 1, where ME is used to measure size)
        "ME2 BM2": "SME",  # The medium BM portfolio for small stocks
        # (ME2 is Market Equity 2, where ME is used to measure size)
        "SMALL HiBM": "SH",  # Small stocks with high BM
        "SMALL LoBM": "SL",  # Small stocks with low BM
    }
    ff_portfolios.rename(columns=column_map, inplace=True)
    ff_portfolios["Date"] = ff_portfolios["Date"].dt.to_period("M").dt.to_timestamp("M")
    ff_portfolios = ff_portfolios.set_index("Date").sort_index(axis=1)
    ff_portfolios.columns.name = "sbport"

    vwret, vwret_n = create_fama_french_portfolios(data_dir=DATA_DIR)
    vwret["Date"] = vwret["jdate"]
    vwret_n["Date"] = vwret_n["jdate"]
    # reshape, so that jdate is the index, categories of sbport are columns, vwret is the values
    # Also, sort columns alphabetically
    vwret = vwret.pivot(index="Date", columns="sbport", values="vwret")
    vwret_n = vwret_n.pivot(index="Date", columns="sbport", values="n_firms")
    vwret = vwret.sort_index(axis=1)
    vwret_n = vwret_n.sort_index(axis=1)

    vwret = vwret.loc["1965-01-01":"2022-12-31", :] * 100
    ff_portfolios = ff_portfolios.loc["1965-01-01":"2022-12-31", :]

    # For each column, check if the average absolute difference between the
    # corresponding columns in vwret and ff_portfolios is less than 0.1
    assert (vwret["BH"] - ff_portfolios["BH"]).abs().mean() < 0.6
    assert (vwret["BL"] - ff_portfolios["BL"]).abs().mean() < 0.2
    assert (vwret["BME"] - ff_portfolios["BME"]).abs().mean() < 2.4
    assert (vwret["SH"] - ff_portfolios["SH"]).abs().mean() < 0.3
    assert (vwret["SL"] - ff_portfolios["SL"]).abs().mean() < 0.3
    assert (vwret["SME"] - ff_portfolios["SME"]).abs().mean() < 2.3

    # For each column, check that the correlation between the column in
    # vwret and the column in ff_portfolios is greater than 0.9
    assert (
        pd.concat([vwret["BH"], ff_portfolios["BH"]], axis=1).corr().iloc[0, 1] > 0.98
    )
    assert (
        pd.concat([vwret["BL"], ff_portfolios["BL"]], axis=1).corr().iloc[0, 1] > 0.98
    )
    assert (
        pd.concat([vwret["BME"], ff_portfolios["BME"]], axis=1).corr().iloc[0, 1] > 0.82
    )
    assert (
        pd.concat([vwret["SH"], ff_portfolios["SH"]], axis=1).corr().iloc[0, 1] > 0.98
    )
    assert (
        pd.concat([vwret["SL"], ff_portfolios["SL"]], axis=1).corr().iloc[0, 1] > 0.98
    )
    assert (
        pd.concat([vwret["SME"], ff_portfolios["SME"]], axis=1).corr().iloc[0, 1] > 0.82
    )


def test_compare_manual_factors_against_ken_french_library():
    ff_factors_web = pull_ken_french_data.load_sheet(
        "F-F_Research_Data_Factors", sheet_name="0"
    )
    ff_factors_web["Date"] = ff_factors_web["Date"] + pd.offsets.MonthEnd(0)

    vwret, vwret_n, ff_factors, ff_nfirms = create_Fama_French_factors(
        data_dir=DATA_DIR
    )
    ff_factors = ff_factors.rename(
        columns={"date": "Date", "SMB": "SMB_manual", "HML": "HML_manual"}
    )
    ff_factors["Date"] = ff_factors["Date"] + pd.offsets.MonthEnd(0)
    ff_factors["SMB_manual"] = ff_factors["SMB_manual"] * 100
    ff_factors["HML_manual"] = ff_factors["HML_manual"] * 100

    df = pd.merge(ff_factors_web, ff_factors, on="Date").set_index("Date")
    df = df.loc["1965-01-01":"2022-12-31", :]

    # df[["SMB", "SMB_manual"]].plot()
    # df[["HML", "HML_manual"]].plot()
    assert (df["SMB"] - df["SMB_manual"]).abs().mean() < 0.25
    assert (df["HML"] - df["HML_manual"]).abs().mean() < 0.40

    assert df[["SMB", "SMB_manual"]].corr().iloc[0, 1] > 0.99
    assert df[["HML", "HML_manual"]].corr().iloc[0, 1] > 0.98


def test_compare_manual_factors_against_crsp():
    vwret, vwret_n, ff_factors, ff_nfirms = create_Fama_French_factors(
        data_dir=DATA_DIR
    )
    ff_compare, ff_compare_post_1970 = compare_with_actual_ff_factors(
        ff_factors, data_dir=DATA_DIR
    )
    ff_compare.info()

    assert ff_compare[["smb_actual", "smb_manual"]].corr().iloc[0, 1] > 0.98
    assert ff_compare[["hml_actual", "hml_manual"]].corr().iloc[0, 1] > 0.97

    assert ff_compare_post_1970[["smb_actual", "smb_manual"]].corr().iloc[0, 1] > 0.99
    assert ff_compare_post_1970[["hml_actual", "hml_manual"]].corr().iloc[0, 1] > 0.98
