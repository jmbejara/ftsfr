"""
Assemble results from forecasting CSV files with auto vs non-auto model filtering.

This script:
1. Reads all CSV files from _output/forecasting/error_metrics/{dataset}/{model}.csv
2. Filters auto vs non-auto model duplicates (prefer auto if valid, else non-auto)
3. Normalizes model names to non-auto versions
4. Adds 'auto' boolean column to track which version was used
5. Outputs consolidated results to _output/forecasting/results_all.csv
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path for settings import
sys.path.insert(0, str(Path(__file__).parent))

from settings import config

OUTPUT_DIR = Path(config("OUTPUT_DIR"))
FORECASTING_DIR = OUTPUT_DIR / "forecasting"
ERROR_METRICS_DIR = FORECASTING_DIR / "error_metrics"


def is_valid_result(row):
    """
    Check if a result row has valid MASE and R2oos values.
    Valid = non-zero, non-null, non-infinite
    """
    mase = row["MASE"]
    r2oos = row["R2oos"]

    # Convert to numeric if they're strings
    try:
        mase = float(mase)
        r2oos = float(r2oos)
    except (ValueError, TypeError):
        return False

    # Check if values are valid (not null, not infinite, not zero)
    if pd.isna(mase) or pd.isna(r2oos):
        return False
    if not np.isfinite(mase) or not np.isfinite(r2oos):
        return False
    if mase == 0 or r2oos == 0:
        return False

    return True


def normalize_model_name(model_name):
    """
    Convert model name to non-auto version.
    auto_deepar -> deepar
    auto_nbeats -> nbeats
    deepar -> deepar (unchanged)
    """
    if model_name.startswith("auto_"):
        return model_name[5:]  # Remove 'auto_' prefix
    return model_name


def parse_csv_stem(stem: str):
    """Split a CSV file stem into (model_name, loss, scale_entity).

    Naming convention used by forecast_neural_auto.py:
        {model}__{loss}                 -> dual-fit, no entity scaling
        {model}__{loss}__entityscale    -> dual-fit, per-entity scaling
        {model}                         -> legacy: classical, or pre-bundle neural

    Returns:
        Tuple (model_name, loss, scale_entity) where loss is one of
        {'mae', 'mse', 'NA'} and scale_entity is bool.
    """
    parts = stem.split("__")
    if len(parts) == 1:
        return parts[0], "NA", False
    if len(parts) == 2 and parts[1] in ("mae", "mse"):
        return parts[0], parts[1], False
    if len(parts) == 3 and parts[1] in ("mae", "mse") and parts[2] == "entityscale":
        return parts[0], parts[1], True
    # Unrecognized pattern; fall back to treating the whole stem as the model.
    return stem, "NA", False


def load_all_csv_files():
    """
    Load all CSV files from the error_metrics directory structure.
    Returns a DataFrame with all results.
    """
    if not ERROR_METRICS_DIR.exists():
        print(f"Error: Directory not found: {ERROR_METRICS_DIR}")
        sys.exit(1)

    all_results = []

    # Iterate through dataset directories
    for dataset_dir in ERROR_METRICS_DIR.iterdir():
        if not dataset_dir.is_dir():
            continue

        dataset_name = dataset_dir.name

        # Iterate through model CSV files
        for csv_file in dataset_dir.glob("*.csv"):
            parsed_model, parsed_loss, parsed_scale = parse_csv_stem(csv_file.stem)

            try:
                df = pd.read_csv(csv_file)

                # Should have exactly one row per file
                if len(df) != 1:
                    print(f"Warning: Expected 1 row in {csv_file}, found {len(df)}")
                    if len(df) == 0:
                        continue
                    df = df.head(1)  # Take first row if multiple

                # The CSV row may already contain a 'loss' / 'scale_entity' column
                # (forecast_neural_auto.py writes them); fall back to what we
                # parsed from the filename when absent.
                if "loss" not in df.columns:
                    df["loss"] = parsed_loss
                if "scale_entity" not in df.columns:
                    df["scale_entity"] = parsed_scale

                # Force model_name to the base (loss-suffix stripped) so the
                # auto-vs-non-auto filter and downstream pivots see one model.
                df["model_name"] = parsed_model

                # Add file path info for debugging
                df["_dataset_from_path"] = dataset_name
                df["_model_from_path"] = csv_file.stem

                all_results.append(df)

            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
                continue

    if not all_results:
        print("Error: No CSV files found or all files failed to load")
        sys.exit(1)

    # Concatenate all results
    results_df = pd.concat(all_results, ignore_index=True)
    print(f"Loaded {len(results_df)} raw results from {len(all_results)} CSV files")

    return results_df


def _pick_source_row(rows, side: str):
    """Pick the best row for a given metric side ('mae' or 'mse').

    Preference within each (dataset, normalized_model, scale_entity) group:
      1. Auto row matching the target loss, if is_valid_result
      2. Legacy auto row with loss='NA' (pre-bundle CSVs), if is_valid_result
         — preserves the historical auto-first preference for back-compat.
      3. Non-auto row with loss='NA' (forecast_neural.py output), if is_valid_result
      4. Any auto row for the OTHER loss as last resort
      5. First row if nothing else is valid
    """
    target_auto = [r for r in rows if r["model_name"].startswith("auto_") and r.get("loss") == side]
    legacy_auto_na = [r for r in rows if r["model_name"].startswith("auto_") and r.get("loss") == "NA"]
    non_auto_na = [r for r in rows if not r["model_name"].startswith("auto_") and r.get("loss") == "NA"]
    other_auto = [
        r for r in rows
        if r["model_name"].startswith("auto_") and r.get("loss") in ("mae", "mse") and r.get("loss") != side
    ]

    for bucket in (target_auto, legacy_auto_na, non_auto_na, other_auto):
        for r in bucket:
            if is_valid_result(r):
                return r
    # Nothing valid; fall back to the first row of the first non-empty bucket
    for bucket in (target_auto, legacy_auto_na, non_auto_na, other_auto, rows):
        if bucket:
            return bucket[0] if isinstance(bucket, list) else next(iter(bucket))
    return None


def filter_auto_vs_nonuto_duplicates(df):
    """Assemble one metric-aligned row per (dataset, normalized_model, scale_entity).

    MASE/MASE-derived columns come from the best mae-side source row;
    MSE/RMSE/R2oos come from the best mse-side source row. The auto-vs-non-auto
    fallback now operates *within* the metric-side pick, so a missing
    `auto_X__mae.csv` will be back-filled by the legacy single-loss `X.csv`
    (non-auto, loss=NA) or the pre-bundle `auto_X.csv`.
    """
    filtered_results = []

    for dataset_name in df["dataset_name"].unique():
        dataset_df = df[df["dataset_name"] == dataset_name].copy()

        # Group rows by (normalized model name, scale_entity).
        model_groups = {}
        for _, row in dataset_df.iterrows():
            normalized_name = normalize_model_name(row["model_name"])
            group_key = (
                normalized_name,
                bool(row.get("scale_entity", False)),
            )
            model_groups.setdefault(group_key, []).append(row)

        # For each (normalized_model, scale_entity) group, build a metric-aligned row
        for (normalized_name, scale_tag), rows in model_groups.items():
            mae_src = _pick_source_row(rows, "mae")
            mse_src = _pick_source_row(rows, "mse")

            if mae_src is None and mse_src is None:
                continue

            # If only one side is found, mirror it to the other so MASE and
            # R2-side both have *some* value (lets legacy/classical pipelines
            # work unchanged).
            if mae_src is None:
                mae_src = mse_src
            if mse_src is None:
                mse_src = mae_src

            combined = mae_src.copy()
            combined["MASE"] = mae_src["MASE"]
            combined["MSE"] = mse_src["MSE"]
            combined["RMSE"] = mse_src["RMSE"]
            combined["R2oos"] = mse_src["R2oos"]
            # Carry the legacy per-series-mean R² through if present, so the
            # paper can report it as a sensitivity column.
            if "R2oos_per_series_mean" in mse_src.index:
                combined["R2oos_per_series_mean"] = mse_src["R2oos_per_series_mean"]
            time_mae = pd.to_numeric(mae_src.get("time_taken", 0), errors="coerce")
            time_mse = pd.to_numeric(mse_src.get("time_taken", 0), errors="coerce")
            if mae_src is mse_src:
                combined["time_taken"] = time_mae
            else:
                combined["time_taken"] = (
                    (0 if pd.isna(time_mae) else time_mae)
                    + (0 if pd.isna(time_mse) else time_mse)
                )

            mae_is_auto = mae_src["model_name"].startswith("auto_")
            mse_is_auto = mse_src["model_name"].startswith("auto_")
            combined["auto"] = bool(mae_is_auto and mse_is_auto)

            mae_loss = mae_src.get("loss", "NA")
            mse_loss = mse_src.get("loss", "NA")
            if mae_loss == "mae" and mse_loss == "mse":
                combined["loss"] = "dual"
            elif mae_loss == mse_loss:
                combined["loss"] = mae_loss
            else:
                combined["loss"] = f"{mae_loss}|{mse_loss}"

            combined["model_name"] = normalized_name
            combined["scale_entity"] = scale_tag

            filtered_results.append(combined)

    return pd.DataFrame(filtered_results)


def main():
    print("Assembling forecasting results with auto vs non-auto filtering...")
    print(f"Reading from: {ERROR_METRICS_DIR}")
    print("=" * 60)

    # Load all CSV files
    raw_df = load_all_csv_files()

    # Show what we loaded
    print("\nRaw data summary:")
    print(f"  Total rows: {len(raw_df)}")
    print(f"  Unique datasets: {raw_df['dataset_name'].nunique()}")
    print(f"  Unique models: {raw_df['model_name'].nunique()}")

    # Filter auto vs non-auto duplicates
    print("\nFiltering auto vs non-auto duplicates...")
    filtered_df = filter_auto_vs_nonuto_duplicates(raw_df)

    # Show filtering results
    print("\nFiltered data summary:")
    print(f"  Total rows: {len(filtered_df)}")
    print(f"  Unique datasets: {filtered_df['dataset_name'].nunique()}")
    print(f"  Unique models: {filtered_df['model_name'].nunique()}")
    print(f"  Auto versions used: {filtered_df['auto'].sum()}")
    print(f"  Non-auto versions used: {(~filtered_df['auto']).sum()}")

    # Clean up columns
    columns_to_keep = [
        "model_name",
        "dataset_name",
        "MASE",
        "MSE",
        "RMSE",
        "R2oos",  # pooled / panel-wide (headline)
        "R2oos_per_series_mean",  # legacy formula (kept for sensitivity)
        "time_taken",
        "auto",
        "loss",
        "scale_entity",
    ]
    # Some legacy CSVs lack loss/scale_entity columns; backfill if missing
    if "loss" not in filtered_df.columns:
        filtered_df["loss"] = "NA"
    if "scale_entity" not in filtered_df.columns:
        filtered_df["scale_entity"] = False
    if "R2oos_per_series_mean" not in filtered_df.columns:
        # Older CSVs only have the (then-headline) per-series-mean R² stored
        # under R2oos; surface that as the sensitivity column so the
        # downstream table builder still sees something.
        filtered_df["R2oos_per_series_mean"] = filtered_df["R2oos"]
    final_df = filtered_df[columns_to_keep].copy()

    # Sort for consistent output
    final_df = final_df.sort_values(["dataset_name", "model_name", "loss", "scale_entity"])

    # final_df rows are already metric-aligned by filter_auto_vs_nonuto_duplicates
    # (one row per (dataset, normalized_model, scale_entity) with MASE-side from
    # mae-loss source and R2-side from mse-loss source). Split by scale_entity
    # so create_results_tables.py keeps reading a single results_all.csv shape.
    output_file = FORECASTING_DIR / "results_all.csv"
    main_df = final_df[~final_df["scale_entity"]].drop(columns=["scale_entity"])
    main_df.to_csv(output_file, index=False)
    print(f"\nSaved metric-aligned results (no entity-scaling) to: {output_file}")

    scaled_subset = final_df[final_df["scale_entity"]].drop(columns=["scale_entity"])
    if not scaled_subset.empty:
        scaled_out = FORECASTING_DIR / "results_all_entityscaled.csv"
        scaled_subset.to_csv(scaled_out, index=False)
        print(f"Saved metric-aligned entity-scaled results to: {scaled_out}")

    # Show some quality stats (over the metric-aligned, no-scaling table)
    print("\nData quality summary (metric-aligned, no entity scaling):")
    mase_valid = pd.to_numeric(main_df["MASE"], errors="coerce")
    r2oos_valid = pd.to_numeric(main_df["R2oos"], errors="coerce")

    print(
        f"  MASE - Valid: {mase_valid.notna().sum()}, Invalid: {mase_valid.isna().sum()}"
    )
    print(
        f"  R2oos - Valid: {r2oos_valid.notna().sum()}, Invalid: {r2oos_valid.isna().sum()}"
    )

    if mase_valid.notna().any():
        print(f"  MASE range: {mase_valid.min():.4f} to {mase_valid.max():.4f}")
    if r2oos_valid.notna().any():
        print(f"  R2oos range: {r2oos_valid.min():.4f} to {r2oos_valid.max():.4f}")

    print("\n" + "=" * 60)
    print("Assembly complete!")


if __name__ == "__main__":
    main()
