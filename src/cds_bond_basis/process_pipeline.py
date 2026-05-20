"""
Orchestrate the CDS-bond basis pipeline from merges to final outputs.

Steps:
1) Merge RED codes + CDS spreads into the bond panel.
2) Add Z-spread estimates per bond observation.
3) Process final CDS basis outputs (aggregates, stats, chart).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from matplotlib import pyplot as plt

import merge_cds_bond
import merge_z_spread_bond
import process_final_product
from settings import config

DATA_DIR = Path(config("DATA_DIR")) / "cds_bond_basis"
OUTPUT_DIR = Path(config("OUTPUT_DIR"))


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1/3: Merging RED + CDS into bond panel...")
    merge_cds_bond.main()

    print("Step 2/3: Adding z-spread columns...")
    merge_z_spread_bond.main()

    print("Step 3/3: Processing final CDS basis outputs...")
    in_path = DATA_DIR / "final_data_with_z_spread.parquet"
    df = pd.read_parquet(in_path)
    df_proc = process_final_product.process_cb_spread(df)
    agg_df, non_agg_df, stats_df = (
        process_final_product.output_cb_final_products_by_period(df_proc)
    )

    df_proc.to_parquet(DATA_DIR / "cds_basis_processed.parquet")
    agg_df.to_parquet(DATA_DIR / "cds_basis_aggregated.parquet")
    non_agg_df.to_parquet(DATA_DIR / "cds_basis_non_aggregated.parquet")
    stats_df.to_csv(DATA_DIR / "cds_basis_summary_stats.csv", index=False)

    fig, _ = process_final_product.generate_graph_by_period(
        agg_df, col="cds_basis_spread_bps"
    )
    fig.savefig(OUTPUT_DIR / "cds_basis_by_rating.png", dpi=160)
    plt.close(fig)

    # Paper-ready single-panel plot (full available sample) used by draft_ftsfr.tex
    # via the cache_latex_artifacts step. Kept under the legacy filename
    # CDS_replicate.png so existing LaTeX references continue to resolve.
    fig2, _ = process_final_product.generate_graph(
        agg_df[agg_df["analysis_period"] == "full_period"],
        col="cds_basis_spread_bps",
    )
    fig2.savefig(OUTPUT_DIR / "CDS_replicate.png", dpi=160)
    plt.close(fig2)

    print(f"Saved: {DATA_DIR / 'cds_basis_processed.parquet'} ({len(df_proc)} rows)")
    print(f"Saved: {DATA_DIR / 'cds_basis_aggregated.parquet'} ({len(agg_df)} rows)")
    print(
        f"Saved: {DATA_DIR / 'cds_basis_non_aggregated.parquet'} ({len(non_agg_df)} rows)"
    )
    print(f"Saved: {DATA_DIR / 'cds_basis_summary_stats.csv'}")
    print(f"Saved: {OUTPUT_DIR / 'cds_basis_by_rating.png'}")
    print(f"Saved: {OUTPUT_DIR / 'CDS_replicate.png'}")
    print("Done.")


if __name__ == "__main__":
    main()
