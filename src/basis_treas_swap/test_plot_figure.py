"""Tests functions in plot_figure.py
"""
from plot_figure import *
from pandas.tseries.offsets import DateOffset
import matplotlib
matplotlib.use('Agg')

output_dir = Path(config("OUTPUT_DIR"))

def test_plot_figure():
    """Create a dummy DataFrame, and check if it saves the correct name in the dir
    """
    # Create dict for DataFrame
    arb_df = {}
    col = []
    start = pd.Timestamp(config("START_DATE")).date()
    arb_df[start] = [x for x in range(7)]
    arb_df[start + DateOffset(months=1)] = [x for x in range(7, 14)]
    for year in [1,20,2,30,3,5,10]:
        col.append(f'Arb_Swap_{year}')
    arb_df = pd.DataFrame.from_dict(arb_df, orient = 'index', columns = col)

    file = os.path.join(output_dir, "dummy_plot.png")
    plot_figure(arb_df, file)

    assert os.path.exists(file)

def test_plot_supplementary():
    """Create a dummy DataFrame, and check if it saves the correct name in the dir
    """

    # DataFrame
    arb_df = {}
    col = []
    start = pd.Timestamp(config("START_DATE")).date()
    arb_df[start] = [x for x in range(1, 14)]
    arb_df[start + DateOffset(months=1)] = [x for x in range(20, 34)]
    for year in [1,20,2,30,3,5,10]:
        col.append(f'GT{year} Govt')
    for year in [1,20,2,30,3,5,10]:
        col.append(f'USSO{year} CMPN Curncy')
    arb_df = pd.DataFrame.from_dict(arb_df, orient = 'index', columns = col)

    # running plot_supplementary
    file = os.path.join(output_dir, "replication_figure.png")
    plot_supplementary(arb_df, file)

    # checking all the files generated
    for year in [1,20,2,30,3,5,10]:
        file = os.path.join(output_dir, f"replication_figure{year}.png")
        assert os.path.exists(file)

def test_plot_main():
    """Runs plot_main() and checks if the plots are saved correctly
    Note: It only passes/works when running with a bloomberg-enabled machine.
    """
    plot_main()
    file_r = os.path.join(output_dir, 'replicated_swap_spread_arb_figure.png')
    file_u = os.path.join(output_dir, 'updated_swap_spread_arb_figure.png')
    assert os.path.exists(file_r) and os.path.exists(file_u)