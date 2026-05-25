"""
Build the stacked 'Sensitivity to cleaning method - robustness across asset
classes' table referenced from the paper.

Mirrors the structure of build_mmn_sensitivity_table.py but stacks three
demos as panels under a single tabular:

  Panel A: Options - L1 vs L3 filters (CJS 54 portfolios)
  Panel B: FF25 size x BM - NYSE vs CRSP breakpoints
  Panel C: Treasury portfolios - GSW strict vs permissive

Within each panel, rows are forecasting models and columns are
(R^2_oos x {variant A, variant B}, MASE x {variant A, variant B}, deltas).
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

# Each panel: (panel_label, variant_A_dataset, variant_B_dataset,
# variant_A_column_header, variant_B_column_header).
PANELS = [
    (
        "Panel A: Options (CJS 54)",
        "ftsfr_cjs_option_returns_l1_filters",
        "ftsfr_cjs_option_returns_l3_filters",
        "L1 filters",
        "L3 filters",
    ),
    (
        "Panel B: FF25 (Size x BM)",
        "ftsfr_ff25_size_bm_nyse_breaks",
        "ftsfr_ff25_size_bm_crsp_breaks",
        "NYSE breaks",
        "CRSP breaks",
    ),
    (
        "Panel C: Treasury portfolios",
        "ftsfr_treas_portfolios_permissive",
        "ftsfr_treas_portfolios_strict",
        "Permissive",
        "GSW strict",
    ),
    (
        "Panel D: Corp bond STR (clean\\_trace)",
        "ftsfr_corp_bond_str_deciles_naive",
        "ftsfr_corp_bond_str_deciles_return_gap",
        "Naive (Approach 1)",
        "Return gap (Approach 3)",
    ),
]

# Same model ordering and display names as the MMN sensitivity table so the
# two tables read consistently.
MODELS = [
    ("historic_average", "HistAvg"),
    ("auto_arima", "ARIMA"),
    ("ses", "SES"),
    ("theta", "Theta"),
    ("auto_dlinear", "DLinear"),
    ("auto_deepar", "DeepAR"),
    ("auto_kan", "KAN"),
    ("auto_nbeats", "NBEATS"),
    ("auto_nhits", "NHITS"),
    ("auto_nlinear", "NLinear"),
    ("auto_tide", "TiDE"),
    ("auto_vanilla_transformer", "Transformer"),
]


def load_metric(dataset: str, model: str):
    p = METRICS_DIR / dataset / f"{model}.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p)
    return {"MASE": float(df["MASE"].iloc[0]), "R2oos": float(df["R2oos"].iloc[0])}


def fmt_dash(x, n=3):
    if pd.isna(x):
        return "--"
    return f"{x:.{n}f}"


def fmt_signed(x, n=3):
    if pd.isna(x):
        return "--"
    return f"{x:+.{n}f}"


def panel_dataframe(dataset_a: str, dataset_b: str) -> pd.DataFrame:
    rows = []
    for mkey, mname in MODELS:
        ma = load_metric(dataset_a, mkey)
        mb = load_metric(dataset_b, mkey)
        rows.append(
            {
                "Model": mname,
                "R2oos_a": ma["R2oos"] if ma else float("nan"),
                "R2oos_b": mb["R2oos"] if mb else float("nan"),
                "MASE_a": ma["MASE"] if ma else float("nan"),
                "MASE_b": mb["MASE"] if mb else float("nan"),
            }
        )
    df = pd.DataFrame(rows)
    df["dR2oos"] = df["R2oos_b"] - df["R2oos_a"]
    df["dMASE"] = df["MASE_b"] - df["MASE_a"]
    return df


def emit_panel_rows(df: pd.DataFrame) -> str:
    best_r2_a = df["R2oos_a"].idxmax() if df["R2oos_a"].notna().any() else None
    best_r2_b = df["R2oos_b"].idxmax() if df["R2oos_b"].notna().any() else None
    best_mase_a = df["MASE_a"].idxmin() if df["MASE_a"].notna().any() else None
    best_mase_b = df["MASE_b"].idxmin() if df["MASE_b"].notna().any() else None

    def bold(value_str, idx, best_idx):
        if best_idx is None or idx != best_idx or value_str == "--":
            return value_str
        return f"\\textbf{{{value_str}}}"

    lines = []
    for idx, r in df.iterrows():
        lines.append(
            " & ".join(
                [
                    r["Model"],
                    bold(fmt_dash(r["R2oos_a"]), idx, best_r2_a),
                    bold(fmt_dash(r["R2oos_b"]), idx, best_r2_b),
                    fmt_signed(r["dR2oos"]),
                    bold(fmt_dash(r["MASE_a"]), idx, best_mase_a),
                    bold(fmt_dash(r["MASE_b"]), idx, best_mase_b),
                    fmt_signed(r["dMASE"]),
                ]
            )
            + " \\\\"
        )
    return "\n".join(lines)


def build_table() -> str:
    """Build the full stacked tabular as a single LaTeX string that the paper
    can \\input directly."""
    header_block = (
        "\\begin{tabular}{lrrrrrr}\n"
        "\\toprule\n"
        "& \\multicolumn{3}{c}{$R^2_{\\text{oos}}$} & \\multicolumn{3}{c}{MASE} \\\\\n"
        "\\cmidrule(lr){2-4}\\cmidrule(lr){5-7}\n"
    )

    pieces = [header_block]
    for i, (panel_label, ds_a, ds_b, label_a, label_b) in enumerate(PANELS):
        df = panel_dataframe(ds_a, ds_b)
        # Also write per-panel CSV for inspection / debugging.
        slug = panel_label.split(":")[0].lower().replace(" ", "_")
        csv_path = PAPER_DIR / f"cleaning_sensitivity_{slug}.csv"
        df.to_csv(csv_path, index=False, float_format="%.4f")
        print(f"Wrote {csv_path}")

        col_header = (
            f"Model & {label_a} & {label_b} & $\\Delta$ "
            f"& {label_a} & {label_b} & $\\Delta$ \\\\\n"
        )
        panel_header = (
            f"\\multicolumn{{7}}{{l}}{{\\textit{{{panel_label}}}}} \\\\\n"
            "\\midrule\n"
            + col_header
            + "\\midrule\n"
        )
        pieces.append(panel_header)
        pieces.append(emit_panel_rows(df))
        if i < len(PANELS) - 1:
            pieces.append("\n\\midrule\n")
        else:
            pieces.append("\n\\bottomrule\n")

    pieces.append("\\end{tabular}\n")
    return "".join(pieces)


def main():
    tex = build_table()
    out_path = PAPER_DIR / "cleaning_sensitivity_tabular.tex"
    out_path.write_text(tex)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
