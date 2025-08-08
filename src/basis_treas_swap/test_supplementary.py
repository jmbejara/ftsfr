"""Test functions present in supplementary.py"""

from supplementary import *
from pandas.tseries.offsets import DateOffset


def test_replication_df():
    """Tests replication_df to ensure that the output dataframe
    has the correct data in it.
    """
    years = [1, 2, 3, 5, 10, 20, 30]
    t_list = [f"GT{year} Govt" for year in years]
    s_list = [f"USSO{year} CMPN Curncy" for year in years]
    total_list = t_list + s_list
    raw_syields = pull_raw_syields()
    swap_df = clean_raw_syields(raw_syields)
    raw_tyields = pull_raw_tyields()
    treasury_df = clean_raw_tyields(raw_tyields)
    output = replication_df(treasury_df, swap_df)
    assert [a for a, _ in output.columns] == total_list


def test_sup_table():
    """Creates a dummy table, and check if it saves the correct name in the dir"""
    arb_df = {}
    col = []
    start = pd.Timestamp(config("START_DATE")).date()
    arb_df[start] = [x for x in range(7)]
    arb_df[start + DateOffset(months=1)] = [x for x in range(7, 14)]
    for year in [1, 20, 2, 30, 3, 5, 10]:
        col.append(f"Arb_Swap_{year}")
    arb_df = pd.DataFrame.from_dict(arb_df, orient="index", columns=col)

    file = os.path.join(output_dir, "dummy_table.txt")
    sup_table(arb_df, file)

    assert os.path.exists(file)
