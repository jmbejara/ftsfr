"""
Dickerson, Robotti, and Rossetti (2024) -- inspired replication exhibit.

Their core claim is that the credit-spread long--short premium in corporate
bonds is partly an artefact of market-microstructure noise (MMN): the same
bid--ask-averaged TRACE prices feed both the credit-spread signal and the
realised return, creating a mechanical reversal that inflates the apparent
predictability. Their MMN correction breaks the mechanical link and reduces
the long--short premium by 50--65%.

We do not have the OSBAP unadjusted-signals dataset on hand
(`mmn_price_based_signals_2025.parquet` is published separately), but the
OSBAP README endorses an equivalent comparison on the main panel: holding
the (MMN-adjusted) credit-spread signal `cs` fixed, switch the realised
return between

  - `ret_vw`    : month-end value-weighted return. Signal price (end of
                  month t) coincides with the return-start price, so any
                  residual MMN at end-of-month-t enters both, producing the
                  same mechanical reversal that Dickerson critiques.
  - `ret_vw_bgn`: month-begin value-weighted return. Signal price (end of
                  month t) is separated from the return-start price (begin
                  of month t+1) by a full bid--ask cycle, breaking the
                  signal--return contamination.

The OSBAP README explicitly notes: "ret_vw_bgn ... Avoids microstructure
bias when signal price = return start price ... Use ... for testing
implementable returns."

We sort bonds into 10 value-weighted deciles by `cs` each month using the
NYSE-style construction (no NYSE breakpoints here -- credit-spread deciles
are CRSP-wide by convention in the literature), and compute the
decile-10-minus-decile-1 long--short under each return convention. The gap
between the two long--short spreads is the portion of the apparent premium
that is attributable to the signal--return microstructure link.

Output:
  - DATA_DIR/corp_bond_returns/mmn_dickerson_replication.csv
  - OUTPUT_DIR/forecasting/paper/mmn_dickerson_tabular.tex
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import warnings

import numpy as np
import pandas as pd

import pull_open_source_bond  # type: ignore  # noqa: E402
from settings import config  # type: ignore  # noqa: E402

warnings.filterwarnings("ignore", category=DeprecationWarning)

DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))
PAPER_DIR = OUTPUT_DIR / "forecasting" / "paper"
PAPER_DIR.mkdir(parents=True, exist_ok=True)


def assign_deciles(df: pd.DataFrame, signal_col: str = "cs") -> pd.DataFrame:
    """Cross-sectional decile assignment by signal, each month."""

    def q(group: pd.DataFrame) -> pd.DataFrame:
        group = group.copy()
        nonnull = group[signal_col].dropna().shape[0]
        if nonnull < 10:
            group["decile"] = pd.NA
            return group
        try:
            group["decile"] = (
                pd.qcut(group[signal_col], 10, labels=False, duplicates="drop") + 1
            )
        except ValueError:
            group["decile"] = pd.NA
        return group

    return df.groupby("date", group_keys=False).apply(q)


def value_weighted_decile_returns(
    df: pd.DataFrame, ret_col: str, value_col: str = "mcap_e"
) -> pd.DataFrame:
    """Value-weighted return per (date, decile)."""
    df = df.dropna(subset=["decile"]).copy()

    def vw(group: pd.DataFrame) -> float:
        w = group[value_col].values
        r = group[ret_col].values
        mask = ~(np.isnan(w) | np.isnan(r))
        if mask.sum() == 0:
            return np.nan
        return float((r[mask] * w[mask]).sum() / w[mask].sum())

    out = (
        df.groupby(["date", "decile"])
        .apply(vw, include_groups=False)
        .reset_index(name="ret")
    )
    return out


def long_short_stats(
    decile_panel: pd.DataFrame, label: str
) -> dict[str, float | str]:
    """Compute D10-D1 long-short summary statistics."""
    wide = decile_panel.pivot(index="date", columns="decile", values="ret").sort_index()
    ls = wide[10] - wide[1]
    n = ls.notna().sum()
    mean_m = float(ls.mean())
    std_m = float(ls.std(ddof=1))
    t_stat = float(mean_m / (std_m / np.sqrt(n))) if n > 1 else float("nan")
    sharpe_ann = float(mean_m / std_m * np.sqrt(12)) if std_m > 0 else float("nan")
    return {
        "label": label,
        "d1_mean_pct_mo": float(wide[1].mean() * 100),
        "d10_mean_pct_mo": float(wide[10].mean() * 100),
        "ls_mean_pct_mo": mean_m * 100,
        "ls_mean_pct_yr": mean_m * 12 * 100,
        "ls_std_pct_mo": std_m * 100,
        "ls_t_stat": t_stat,
        "ls_sharpe_ann": sharpe_ann,
        "n_months": int(n),
    }


def main() -> None:
    bd = pull_open_source_bond.load_corporate_bond_returns(
        data_dir=DATA_DIR / "corp_bond_returns"
    )

    needed = ["date", "cusip", "cs", "ret_vw", "ret_vw_bgn", "mcap_e"]
    bd = bd[needed].dropna(subset=["cs", "ret_vw", "ret_vw_bgn", "mcap_e"]).copy()
    bd = assign_deciles(bd, signal_col="cs")

    panels = {
        "ret_vw": value_weighted_decile_returns(bd, ret_col="ret_vw"),
        "ret_vw_bgn": value_weighted_decile_returns(bd, ret_col="ret_vw_bgn"),
    }

    rows = [
        long_short_stats(
            panels["ret_vw"],
            label="ret_vw (signal-date contaminated)",
        ),
        long_short_stats(
            panels["ret_vw_bgn"],
            label="ret_vw_bgn (implementable)",
        ),
    ]
    df = pd.DataFrame(rows)
    df["delta_ls_pct_yr"] = df["ls_mean_pct_yr"] - df["ls_mean_pct_yr"].iloc[0]
    csv_path = DATA_DIR / "corp_bond_returns" / "mmn_dickerson_replication.csv"
    df.to_csv(csv_path, index=False, float_format="%.4f")
    print(f"Wrote {csv_path}")
    print()
    print(df.to_string(index=False))

    # Emit a self-contained tabular for the paper.
    tex_rows = []
    # Row labels are intentionally short; the realised-return convention is
    # fully explained in the table caption note.
    label_map = {
        "ret_vw (signal-date contaminated)":
            r"\texttt{ret\_vw} (contaminated)",
        "ret_vw_bgn (implementable)":
            r"\texttt{ret\_vw\_bgn} (implementable)",
    }
    for i, r in df.iterrows():
        cells = [
            label_map[r["label"]],
            f"{r['ls_mean_pct_mo']:.3f}",
            f"({r['ls_t_stat']:.2f})",
            f"{r['ls_mean_pct_yr']:.2f}",
            f"{r['ls_sharpe_ann']:.2f}",
        ]
        tex_rows.append(" & ".join(cells) + r" \\")

    delta_yr = df["ls_mean_pct_yr"].iloc[1] - df["ls_mean_pct_yr"].iloc[0]
    delta_pct = delta_yr / df["ls_mean_pct_yr"].iloc[0] * 100.0

    tex = (
        r"\begin{tabular}{lrcrr}" "\n"
        r"\toprule" "\n"
        r"Realised-return convention & "
        r"$\overline{\mathrm{D10}{-}\mathrm{D1}}$ (\%/mo) & "
        r"$t$-stat & "
        r"Annualised (\%) & "
        r"Sharpe \\" "\n"
        r"\midrule" "\n"
        + "\n".join(tex_rows) + "\n"
        r"\midrule" "\n"
        r"$\Delta$ (implementable $-$ contaminated) & & & "
        f"{delta_yr:+.2f} & \n"
        r"\\" "\n"
        r"\bottomrule" "\n"
        r"\end{tabular}" "\n"
    )

    tex_path = PAPER_DIR / "mmn_dickerson_tabular.tex"
    tex_path.write_text(tex)
    print(f"\nWrote {tex_path}")

    print(
        f"\nSummary: switching from ret_vw to ret_vw_bgn drops the D10-D1 "
        f"long-short by {delta_yr:.2f} pp/yr "
        f"({delta_pct:+.1f}% relative)."
    )


if __name__ == "__main__":
    main()
