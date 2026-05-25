"""
Short-Term-Reversal replication of Dickerson, Robotti, and Rossetti (2026,
"The Corporate Bond Factor Replication Crisis," arXiv:2604.07880).

Dickerson et al. identify *Latent Implementation Bias* (LIB) as a Correlated
Errors-In-Variables (CEIV) problem: when the same noisy month-end TRACE
price enters both the sorting signal and the return-denominator, the price
noise delta_t shows up on both sides of every long-short factor, and the
resulting mechanical correlation manifests as a spurious premium.

The cleanest illustration of this bias is the short-term-reversal signal,
because the signal IS literally the most recent return -- the noise in the
signal and the noise in the return denominator are perfectly mechanically
linked. Dickerson et al. report the headline result for this signal
(introduction, page 3):

    "Short-term reversal illustrates the severity of LIB, with the premium
     dropping from -0.99% to -0.09% per month after correction
     (t-statistic: -4.46 to -0.51), and bias comprising over 90% of the
     documented effect."

This script implements two of their three "approaches" (Section 3 of the
paper), using the case_study_clean_trace stage1 daily panel as the
underlying data:

  - Approach 1 (Unadjusted, "naive"): signal at month-end t, return measured
    from month-end t to month-end t+1. The month-end price P_t enters the
    signal AND the return denominator, so noise delta_t enters both. This
    is the standard convention in the literature.

  - Approach 3 (Return gap, "implementable"): signal at month-end t, return
    measured from month-*begin* t+1 (first available trade in the first 5
    business days of t+1) to month-end t+1. The signal noise delta_t no
    longer enters the return denominator (which uses P^bgn_{t+1}), breaking
    the mechanical link.

We use Approach 3 rather than Approach 2 (the "signal gap") because OSBAP's
ret_vw_bgn -- which is Approach 3 in their dataset -- is the canonical
implementation, and the comparison is symmetric. The mechanism the bias
relies on (same delta_t in signal and return-start) is broken either way.

The short-term reversal signal is defined as the past-month return:
    str_t = (P^end_t / P^end_{t-1}) - 1
With this convention, D10 is the recent-winners decile and D1 is the
recent-losers decile, so the long-short D10 - D1 is *negative* when
reversal works (winners underperform losers next month). This matches
Dickerson's sign convention.

Output:
  DATA_DIR/corp_bond_returns/ftsfr_corp_bond_str_deciles_naive.parquet
  DATA_DIR/corp_bond_returns/ftsfr_corp_bond_str_deciles_return_gap.parquet
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import warnings

import polars as pl

from settings import config  # type: ignore  # noqa: E402

warnings.filterwarnings("ignore", category=DeprecationWarning)

DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))
PAPER_DIR = OUTPUT_DIR / "forecasting" / "paper"
PAPER_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CLEAN_TRACE_DIR = (
    Path.home() / "GitRepositories" / "finm-32900-ALL" / "case_study_clean_trace"
)
CLEAN_TRACE_DIR = Path(os.environ.get("CLEAN_TRACE_DIR", DEFAULT_CLEAN_TRACE_DIR))
STAGE1_LATEST = CLEAN_TRACE_DIR / "_data" / "stage1" / "stage1_latest.parquet"

# Dickerson, Robotti, Rossetti (2026), Section 2.2:
#   "The monthly price is the last available daily price within the last
#    five business days of the month (NYSE calendar)."
#   "month-begin returns (computed from the first (last) available price
#    within the first five (last five) business days of month t+1)"
EOM_LOOKBACK_DAYS = 5
BOM_LOOKAHEAD_DAYS = 5


def _ensure_source() -> None:
    if not STAGE1_LATEST.exists():
        raise FileNotFoundError(
            f"Source file not found: {STAGE1_LATEST}\n"
            "Either run the case_study_clean_trace pipeline first or set the "
            "CLEAN_TRACE_DIR environment variable to a directory containing "
            "_data/stage1/stage1_latest.parquet."
        )


def load_stage1() -> pl.DataFrame:
    # accpmt is the cumulative coupon paid since the bond's dated date.
    # Differences in accpmt across two dates equal the coupon cash flow
    # received between those dates (per $100 face). This lets us implement
    # the Dickerson, Robotti, and Rossetti (2026) Eqn (1)/(2) return
    # numerators that include C_{t+1} directly from stage1, without a
    # separate FISD coupon-schedule lookup.
    cols = [
        "cusip_id",
        "trd_exctn_dt",
        "prfull",
        "accpmt",
        "bond_amt_outstanding",
    ]
    df = pl.read_parquet(STAGE1_LATEST, columns=cols)
    df = df.filter(pl.col("prfull").is_not_null() & (pl.col("prfull") > 0))
    # accpmt is non-decreasing by construction; missing values are rare
    # and treated as no-coupon (we'll forward-fill within bond for safety).
    df = df.sort(["cusip_id", "trd_exctn_dt"])
    df = df.with_columns(pl.col("accpmt").forward_fill().over("cusip_id"))
    df = df.filter(pl.col("accpmt").is_not_null())
    return df


def build_eom_bom_panel(stage1: pl.DataFrame) -> pl.DataFrame:
    """For each (cusip, calendar month), extract:
      - p_eom : last available prfull within the last EOM_LOOKBACK_DAYS
                business days of the month
      - p_bom : first available prfull within the first BOM_LOOKAHEAD_DAYS
                business days of the month

    Returns a long bond-month panel keyed by (cusip_id, ym) with both
    end-of-month and (next-month) beginning-of-month prices available.
    """
    df = stage1.with_columns(pl.col("trd_exctn_dt").dt.truncate("1mo").alias("ym"))

    # Rank within (cusip, ym) by trading-date ascending and descending.
    df = df.with_columns(
        pl.col("trd_exctn_dt").rank(method="ordinal").over(["cusip_id", "ym"]).alias("rk_asc"),
        pl.col("trd_exctn_dt")
        .rank(method="ordinal", descending=True)
        .over(["cusip_id", "ym"])
        .alias("rk_desc"),
    )

    # End-of-month observation: the latest observation within the cusip-month,
    # provided it lies in the last EOM_LOOKBACK_DAYS business days of the
    # calendar month. We approximate "last 5 business days" by requiring the
    # observation date to be within 5 weekday-business days of the calendar
    # month-end (Polars: business_day_count between obs and month-end <= 5).
    df = df.with_columns(
        pl.col("ym").dt.month_end().alias("month_end_cal"),
        pl.col("ym").alias("month_begin_cal"),
    )
    df = df.with_columns(
        # Approximate business-day distance via calendar-day distance / (5/7).
        # The clean_trace pipeline already uses NYSE calendar for stage1, so
        # most month-end trading days will be near the calendar month-end.
        ((pl.col("month_end_cal") - pl.col("trd_exctn_dt")).dt.total_days())
        .alias("days_from_month_end"),
        ((pl.col("trd_exctn_dt") - pl.col("month_begin_cal")).dt.total_days())
        .alias("days_from_month_begin"),
    )

    # EOM: pick the latest observation per (cusip, ym) whose calendar-day
    # distance from month-end is at most 7 (covers any 5 business days + a
    # weekend buffer). Also record accpmt at EOM (cumulative coupons paid
    # by the bond up to that date, per $100 face).
    eom_candidates = df.filter(pl.col("days_from_month_end") <= 7)
    eom = (
        eom_candidates
        .sort(["cusip_id", "ym", "trd_exctn_dt"])
        .group_by(["cusip_id", "ym"])
        .agg(
            [
                pl.col("prfull").last().alias("p_eom"),
                pl.col("accpmt").last().alias("accpmt_eom"),
                pl.col("trd_exctn_dt").last().alias("eom_dt"),
                pl.col("bond_amt_outstanding").last().alias("amt_outstanding"),
            ]
        )
    )

    # BOM: pick the earliest observation per (cusip, ym) whose calendar-day
    # distance from month-begin is at most 7 (covers first 5 business days).
    bom_candidates = df.filter(pl.col("days_from_month_begin") <= 7)
    bom = (
        bom_candidates
        .sort(["cusip_id", "ym", "trd_exctn_dt"])
        .group_by(["cusip_id", "ym"])
        .agg(
            [
                pl.col("prfull").first().alias("p_bom"),
                pl.col("accpmt").first().alias("accpmt_bom"),
                pl.col("trd_exctn_dt").first().alias("bom_dt"),
            ]
        )
    )

    panel = eom.join(bom, on=["cusip_id", "ym"], how="inner")
    return panel.sort(["cusip_id", "ym"])


def attach_returns_and_signal(panel: pl.DataFrame) -> pl.DataFrame:
    """For each (cusip, ym = t), implement Dickerson, Robotti, and Rossetti
    (2026) Eqns (1) and (2). Letting P denote prfull (clean + accrued) and
    Delta_accpmt denote the coupon cash flow received between two dates:

      signal_str = (P_eom_t + C_t) / P_eom_{t-1} - 1
                     where C_t = accpmt_eom_t - accpmt_eom_{t-1}

      ret_naive  = (P_eom_{t+1} + C_naive) / P_eom_t - 1                (1)
                     where C_naive = accpmt_eom_{t+1} - accpmt_eom_t

      ret_gap    = (P_eom_{t+1} + C_gap) / P_bom_{t+1} - 1              (2)
                     where C_gap = accpmt_eom_{t+1} - accpmt_bom_{t+1}

    Requires consecutive months t-1, t, t+1 to all be populated for the
    bond.
    """
    panel = panel.with_columns(
        [
            pl.col("p_eom").shift(1).over("cusip_id").alias("p_eom_prev"),
            pl.col("accpmt_eom").shift(1).over("cusip_id").alias("accpmt_eom_prev"),
            pl.col("ym").shift(1).over("cusip_id").alias("ym_prev"),
            pl.col("p_eom").shift(-1).over("cusip_id").alias("p_eom_next"),
            pl.col("accpmt_eom").shift(-1).over("cusip_id").alias("accpmt_eom_next"),
            pl.col("p_bom").shift(-1).over("cusip_id").alias("p_bom_next"),
            pl.col("accpmt_bom").shift(-1).over("cusip_id").alias("accpmt_bom_next"),
            pl.col("ym").shift(-1).over("cusip_id").alias("ym_next"),
        ]
    )
    panel = panel.with_columns(
        [
            pl.col("ym").dt.offset_by("-1mo").alias("ym_prev_expected"),
            pl.col("ym").dt.offset_by("1mo").alias("ym_next_expected"),
        ]
    )
    panel = panel.filter(
        pl.col("ym_prev").is_not_null()
        & pl.col("ym_next").is_not_null()
        & (pl.col("ym_prev") == pl.col("ym_prev_expected"))
        & (pl.col("ym_next") == pl.col("ym_next_expected"))
        & pl.col("p_eom_prev").is_not_null()
        & pl.col("p_eom_next").is_not_null()
        & pl.col("p_bom_next").is_not_null()
        & pl.col("accpmt_eom_prev").is_not_null()
        & pl.col("accpmt_eom_next").is_not_null()
        & pl.col("accpmt_bom_next").is_not_null()
        & (pl.col("amt_outstanding") > 0)
    )
    # Coupon cash flow in each holding window. By construction accpmt is
    # non-decreasing, so these should be >= 0.
    panel = panel.with_columns(
        [
            (pl.col("accpmt_eom") - pl.col("accpmt_eom_prev")).alias("C_signal"),
            (pl.col("accpmt_eom_next") - pl.col("accpmt_eom")).alias("C_naive"),
            (pl.col("accpmt_eom_next") - pl.col("accpmt_bom_next")).alias("C_gap"),
        ]
    )
    panel = panel.with_columns(
        [
            (((pl.col("p_eom") + pl.col("C_signal")) / pl.col("p_eom_prev")) - 1.0)
            .alias("signal_str"),
            (((pl.col("p_eom_next") + pl.col("C_naive")) / pl.col("p_eom")) - 1.0)
            .alias("ret_naive"),
            (((pl.col("p_eom_next") + pl.col("C_gap")) / pl.col("p_bom_next")) - 1.0)
            .alias("ret_gap"),
        ]
    )
    return panel.select(
        ["cusip_id", "ym", "signal_str", "ret_naive", "ret_gap", "amt_outstanding"]
    )


def vw_decile_returns(
    monthly: pl.DataFrame, signal_col: str, ret_col: str, n_dec: int = 10
) -> pl.DataFrame:
    df = monthly.filter(pl.col(signal_col).is_not_null() & pl.col(ret_col).is_not_null())
    df = df.with_columns(
        (pl.col(signal_col).rank(method="ordinal").over("ym") - 1).alias("rk"),
        pl.len().over("ym").alias("n_in_month"),
    )
    df = df.with_columns(
        ((pl.col("rk") * n_dec) // pl.col("n_in_month") + 1).cast(pl.Int64).alias("decile")
    )
    df = df.with_columns(
        pl.when(pl.col("decile") > n_dec)
        .then(n_dec)
        .otherwise(pl.col("decile"))
        .alias("decile")
    )
    valid_months = (
        df.group_by("ym")
        .agg(pl.col("decile").n_unique().alias("k"))
        .filter(pl.col("k") == n_dec)
        .select("ym")
    )
    df = df.join(valid_months, on="ym", how="inner")
    agg = (
        df.group_by(["ym", "decile"])
        .agg(
            (
                (pl.col(ret_col) * pl.col("amt_outstanding")).sum()
                / pl.col("amt_outstanding").sum()
            ).alias("y")
        )
        .sort(["ym", "decile"])
    )
    return agg


def to_ftsfr_long(decile_panel: pl.DataFrame, label_prefix: str) -> pl.DataFrame:
    out = decile_panel.with_columns(
        (
            pl.lit(label_prefix + "_decile_")
            + pl.col("decile").cast(pl.Int64).cast(pl.Utf8).str.zfill(2)
        ).alias("unique_id"),
        pl.col("ym").dt.month_end().alias("ds"),
    ).select(["unique_id", "ds", "y"])
    return out.drop_nulls(subset=["y"])


def long_short_stats(decile_panel: pl.DataFrame) -> dict:
    wide = (
        decile_panel.pivot(index="ym", on="decile", values="y", aggregate_function="first")
        .sort("ym")
    )
    ls = (wide["10"] - wide["1"]).drop_nulls()
    n = ls.len()
    if n == 0:
        return {}
    mean_m = float(ls.mean())
    std_m = float(ls.std(ddof=1))
    t_stat = (mean_m / (std_m / (n ** 0.5))) if std_m > 0 and n > 1 else float("nan")
    sharpe_ann = (mean_m / std_m * (12 ** 0.5)) if std_m > 0 else float("nan")
    return {
        "n_months": n,
        "ls_pct_mo": mean_m * 100,
        "ls_pct_yr": mean_m * 12 * 100,
        "t_stat": t_stat,
        "sharpe_ann": sharpe_ann,
    }


def emit_paper_tabular(naive_stats: dict, gap_stats: dict) -> None:
    """Write a small LaTeX tabular for the paper, parallel in style to the
    OSBAP-based mmn_dickerson_tabular.tex."""
    delta_yr = gap_stats["ls_pct_yr"] - naive_stats["ls_pct_yr"]
    rel_pct = (delta_yr / naive_stats["ls_pct_yr"]) * 100.0 if naive_stats["ls_pct_yr"] != 0 else float("nan")

    rows = [
        # Approach 1 (naive)
        " & ".join(
            [
                r"Approach 1: month-end signal, month-end return (\textit{naive})",
                f"{naive_stats['ls_pct_mo']:+.3f}",
                f"({naive_stats['t_stat']:+.2f})",
                f"{naive_stats['ls_pct_yr']:+.2f}",
                f"{naive_stats['sharpe_ann']:+.2f}",
            ]
        )
        + r" \\",
        # Approach 3 (return gap)
        " & ".join(
            [
                r"Approach 3: month-end signal, month-begin return gap (\textit{implementable})",
                f"{gap_stats['ls_pct_mo']:+.3f}",
                f"({gap_stats['t_stat']:+.2f})",
                f"{gap_stats['ls_pct_yr']:+.2f}",
                f"{gap_stats['sharpe_ann']:+.2f}",
            ]
        )
        + r" \\",
    ]

    tex = (
        r"\begin{tabular}{lrcrr}" + "\n"
        r"\toprule" + "\n"
        r"Construction & $\overline{\mathrm{D10}{-}\mathrm{D1}}$ (\%/mo) & "
        r"$t$-stat & Annualised (\%) & Sharpe \\" + "\n"
        r"\midrule" + "\n"
        + "\n".join(rows) + "\n"
        r"\midrule" + "\n"
        r"$\Delta$ (Approach 3 $-$ Approach 1) & & & "
        f"{delta_yr:+.2f} ({rel_pct:+.0f}\\%) & \n"
        r"\\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
    )

    out_path = PAPER_DIR / "str_dickerson_tabular.tex"
    out_path.write_text(tex)
    print(f"Wrote {out_path}")


def summarize_long_short(decile_panel: pl.DataFrame, label: str) -> None:
    wide = (
        decile_panel.pivot(index="ym", on="decile", values="y", aggregate_function="first")
        .sort("ym")
    )
    # D10 - D1: winners minus losers. Negative when reversal works.
    ls = (wide["10"] - wide["1"]).drop_nulls()
    n = ls.len()
    if n == 0:
        print(f"  {label}: no long-short months available")
        return
    mean_m = float(ls.mean())
    std_m = float(ls.std(ddof=1))
    t_stat = (mean_m / (std_m / (n ** 0.5))) if std_m > 0 and n > 1 else float("nan")
    sharpe_ann = (mean_m / std_m * (12 ** 0.5)) if std_m > 0 else float("nan")
    print(
        f"  {label}: D10-D1 = {mean_m * 100:+.3f}%/mo  "
        f"({mean_m * 12 * 100:+.2f}%/yr)  t = {t_stat:+.2f}  "
        f"Sharpe (ann) = {sharpe_ann:+.2f}  n = {n}"
    )


def main() -> None:
    _ensure_source()
    print(f"Loading {STAGE1_LATEST}...")
    stage1 = load_stage1()
    print(f"  rows: {stage1.height:,}")
    print(f"  date range: {stage1['trd_exctn_dt'].min()} -> {stage1['trd_exctn_dt'].max()}")

    print("\nBuilding (EOM, BOM) bond-month panel...")
    panel = build_eom_bom_panel(stage1)
    print(f"  bond-month rows with both EOM and BOM observations: {panel.height:,}")

    print("\nAttaching prev/next observations and computing STR signal + both returns...")
    monthly = attach_returns_and_signal(panel)
    print(f"  bond-month rows with valid str + naive + gap: {monthly.height:,}")
    print(f"  date range: {monthly['ym'].min()} -> {monthly['ym'].max()}")

    print("\nBuilding decile panels...")
    naive_dec = vw_decile_returns(monthly, signal_col="signal_str", ret_col="ret_naive")
    gap_dec = vw_decile_returns(monthly, signal_col="signal_str", ret_col="ret_gap")

    print("\nLong-short summaries (D10-D1, value-weighted, monthly):")
    print(f"  Dickerson, Robotti & Rossetti (2026, p.3) headline for full universe:")
    print(f"      -0.99%/mo (t=-4.46)  vs corrected  -0.09%/mo (t=-0.51)")
    summarize_long_short(naive_dec, "Approach 1 (naive, end-end)")
    summarize_long_short(gap_dec, "Approach 3 (return gap, end-bgn->end)")

    out_dir = DATA_DIR / "corp_bond_returns"
    out_dir.mkdir(parents=True, exist_ok=True)
    naive_path = out_dir / "ftsfr_corp_bond_str_deciles_naive.parquet"
    gap_path = out_dir / "ftsfr_corp_bond_str_deciles_return_gap.parquet"
    to_ftsfr_long(naive_dec, "str_naive").write_parquet(naive_path)
    to_ftsfr_long(gap_dec, "str_gap").write_parquet(gap_path)
    print(f"\nWrote {naive_path}")
    print(f"Wrote {gap_path}")

    # Emit a small LaTeX tabular for the paper exhibit.
    naive_stats = long_short_stats(naive_dec)
    gap_stats = long_short_stats(gap_dec)
    if naive_stats and gap_stats:
        emit_paper_tabular(naive_stats, gap_stats)


if __name__ == "__main__":
    main()
