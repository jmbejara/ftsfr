import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from he_kelly_manela.pull_he_kelly_manela import load_he_kelly_manela_all
from settings import config


DATA_DIR = Path(config("DATA_DIR"))


def extract_hkm_cmdty(data_dir=DATA_DIR):
    he_kelly_manela = load_he_kelly_manela_all(data_dir)
    he_kelly_manela.columns.str.contains("cmd").sum()

    col_lst = ["yyyymm"]
    for i in range(1, 10):
        col_lst.append(f"Commod_0{i}")
    for i in range(10, 24):
        col_lst.append(f"Commod_{i}")
    hkm_df = he_kelly_manela[col_lst].dropna(axis=0)
    hkm_df["yyyymm"] = hkm_df["yyyymm"].astype(int).astype(str)
    hkm_df = hkm_df.set_index("yyyymm")
    return hkm_df
