"""
Build the MMN-sensitivity comparison table used in the
'Sensitivity to cleaning method' subsection.

Reads the per-(dataset, model) error-metric CSVs produced by the forecasting
pipeline for the two cleaning variants of the CS-decile portfolios, and emits
a LaTeX tabular comparing R^2_oos and MASE side by side.

Rows: forecasting models.
Columns: (R^2_oos x {MMN-biased, MMN-corrected}, MASE x {MMN-biased, MMN-corrected}).
"""

from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from settings import config

OUTPUT_DIR = Path(config("OUTPUT_DIR"))
METRICS_DIR = OUTPUT_DIR / "forecasting" / "error_metrics"
PAPER_DIR = OUTPUT_DIR / "forecasting" / "paper"
PAPER_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = {
    "biased": "ftsfr_corp_bond_cs_deciles_mmn_biased",
    "corrected": "ftsfr_corp_bond_cs_deciles_mmn_corrected",
}

# Model order and display names for the table.
# Order matches the columns of the paper's main results tables:
# (Stats baselines, then auto-neural models).
MODELS = [
    ("historic_average",         "HistAvg"),
    ("auto_arima",               "ARIMA"),
    ("ses",                      "SES"),
    ("theta",                    "Theta"),
    ("auto_dlinear",             "DLinear"),
    ("auto_deepar",              "DeepAR"),
    ("auto_kan",                 "KAN"),
    ("auto_nbeats",              "NBEATS"),
    ("auto_nhits",               "NHITS"),
    ("auto_nlinear",             "NLinear"),
    ("auto_tide",                "TiDE"),
    ("auto_vanilla_transformer", "Transformer"),
]


def _read(path):
    return pd.read_csv(path) if path.exists() else None


def load_metric(dataset, model):
    """Metric-aligned load mirroring assemble_results.py: MASE comes from the
    MAE-trained fit (``{model}__mae.csv``) and R2oos from the MSE-trained fit
    (``{model}__mse.csv``); the bare ``{model}.csv`` covers stats models and
    legacy single-loss runs."""
    base = METRICS_DIR / dataset
    plain = _read(base / f"{model}.csv")
    mae = _read(base / f"{model}__mae.csv")
    mse = _read(base / f"{model}__mse.csv")
    mase_src = mae if mae is not None else plain
    r2_src = mse if mse is not None else plain
    if mase_src is None or r2_src is None:
        return None
    return {
        "MASE": float(mase_src["MASE"].iloc[0]),
        "R2oos": float(r2_src["R2oos"].iloc[0]),
    }


def fmt_dash(x, n=3):
    if pd.isna(x):
        return "--"
    return f"{x:.{n}f}"


def fmt_signed(x, n=3):
    if pd.isna(x):
        return "--"
    return f"{x:+.{n}f}"


def main():
    rows = []
    for mkey, mname in MODELS:
        row = {"Model": mname}
        for variant_label, ds in DATASETS.items():
            m = load_metric(ds, mkey)
            row[f"MASE_{variant_label}"] = m["MASE"] if m else float("nan")
            row[f"R2oos_{variant_label}"] = m["R2oos"] if m else float("nan")
        # Computed differences
        row["dR2oos"] = row["R2oos_corrected"] - row["R2oos_biased"]
        row["dMASE"] = row["MASE_corrected"] - row["MASE_biased"]
        rows.append(row)
    df = pd.DataFrame(rows)

    # Write CSV for reference
    csv_path = PAPER_DIR / "mmn_sensitivity_table.csv"
    df.to_csv(csv_path, index=False, float_format="%.4f")
    print(f"Wrote {csv_path}")

    # Identify the best model in each level column.
    # R^2_oos: higher is better. MASE: lower is better.
    # Delta columns are sensitivity measures, not performance metrics, so
    # they are not bolded.
    best_idx = {
        "R2oos_biased": df["R2oos_biased"].idxmax(),
        "R2oos_corrected": df["R2oos_corrected"].idxmax(),
        "MASE_biased": df["MASE_biased"].idxmin(),
        "MASE_corrected": df["MASE_corrected"].idxmin(),
    }

    def bold_if_best(value_str, col, idx):
        if idx == best_idx[col] and value_str != "--":
            return f"\\textbf{{{value_str}}}"
        return value_str

    # Write LaTeX tabular (no \begin{table}, just the tabular contents
    # so the .tex file can be \input{}-ed into the paper). With 12 models
    # the row block is taller, so we use scriptsize and tighter column sep
    # in the surrounding table environment in the paper.
    header = (
        "\\begin{tabular}{lrrrrrr}\n"
        "\\toprule\n"
        "& \\multicolumn{3}{c}{$R^2_{\\text{oos}}$} & \\multicolumn{3}{c}{MASE} \\\\\n"
        "\\cmidrule(lr){2-4}\\cmidrule(lr){5-7}\n"
        "Model & MMN-biased & MMN-corrected & $\\Delta$ & MMN-biased & MMN-corrected & $\\Delta$ \\\\\n"
        "\\midrule\n"
    )
    body_rows = []
    for idx, r in df.iterrows():
        body_rows.append(
            " & ".join([
                r["Model"],
                bold_if_best(fmt_dash(r["R2oos_biased"]), "R2oos_biased", idx),
                bold_if_best(fmt_dash(r["R2oos_corrected"]), "R2oos_corrected", idx),
                fmt_signed(r["dR2oos"]),
                bold_if_best(fmt_dash(r["MASE_biased"]), "MASE_biased", idx),
                bold_if_best(fmt_dash(r["MASE_corrected"]), "MASE_corrected", idx),
                fmt_signed(r["dMASE"]),
            ]) + " \\\\"
        )
    body = "\n".join(body_rows)
    footer = "\n\\bottomrule\n\\end{tabular}\n"
    tex = header + body + footer

    tex_path = PAPER_DIR / "mmn_sensitivity_tabular.tex"
    tex_path.write_text(tex)
    print(f"Wrote {tex_path}")

    # Also print to stdout
    print("\n--- Table preview ---")
    print(df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    main()
