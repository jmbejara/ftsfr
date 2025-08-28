"""
cutoff_calc.py

This script calculates cutoff dates for all available datasets and saves them
to a common parquet file. The cutoff date is the first date in the test_data
obtained by splitting the dataset using the process_df function.

The script reads the list of available datasets from available_datasets.csv
and processes each one to determine its test cutoff date.
"""

import pandas as pd
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model_classes.helper_func import process_df


def load_available_datasets(output_dir):
    """Load the list of available datasets from CSV."""
    csv_path = output_dir / "available_datasets.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"available_datasets.csv not found at {csv_path}. "
            "Please run 'doit determine_available_datasets' first."
        )

    return pd.read_csv(csv_path)


def convert_to_expected_format(df, dataset_path):
    """
    Convert a DataFrame to the format expected by process_df.

    Expected format: DataFrame with columns ['ds', 'y', 'unique_id']
    where 'ds' is datetime, 'y' is numeric values, and 'unique_id' identifies series.

    Args:
        df: Input DataFrame
        dataset_path: Path to the dataset file (for error messages)

    Returns:
        DataFrame in the expected format
    """
    # Check if already in expected format (either order)
    if all(col in df.columns for col in ["ds", "y", "unique_id"]):
        # The DataFrame has the right columns, but we need to ensure proper types and order
        df = df.copy()

        # Reorder columns to match what process_df expects: ['ds', 'y', 'unique_id']
        df = df[["ds", "y", "unique_id"]]

        # Convert 'ds' to datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(df["ds"]):
            try:
                df["ds"] = pd.to_datetime(df["ds"])
            except Exception as e:
                raise ValueError(
                    f"Could not parse date column 'ds' in {dataset_path}: {e}"
                )

        # Ensure 'y' is numeric
        if not pd.api.types.is_numeric_dtype(df["y"]):
            try:
                df["y"] = pd.to_numeric(df["y"], errors="coerce")
                df = df.dropna(subset=["y"])
            except Exception as e:
                raise ValueError(
                    f"Could not convert 'y' column to numeric in {dataset_path}: {e}"
                )

        # Handle potential duplicate combinations of unique_id and ds
        # This can cause issues in process_df
        df = df.drop_duplicates(subset=["unique_id", "ds"])

        # Ensure unique_id is string type
        df["unique_id"] = df["unique_id"].astype(str)

        if df.empty:
            raise ValueError(
                f"No valid data found in {dataset_path} after type conversion"
            )

        return df

    # Handle wide format (multiple columns with dates as index)
    if len(df.columns) > 2:
        # Reset index to make date a column
        df = df.reset_index()

        # Find the date column
        date_col = None
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(
                df[col]
            ) or pd.api.types.is_string_dtype(df[col]):
                # Check if this looks like a date column
                if col.lower() in ["date", "time", "ds"] or "date" in col.lower():
                    date_col = col
                    break

        if date_col is None:
            # Assume first column is date if it looks like it
            first_col = df.columns[0]
            if pd.api.types.is_datetime64_any_dtype(
                df[first_col]
            ) or pd.api.types.is_string_dtype(df[first_col]):
                date_col = first_col
            else:
                raise ValueError(f"Could not identify date column in {dataset_path}")

        # Convert date column to datetime if needed
        if pd.api.types.is_string_dtype(df[date_col]):
            try:
                df[date_col] = pd.to_datetime(df[date_col])
            except Exception as e:
                raise ValueError(
                    f"Could not parse date column '{date_col}' in {dataset_path}: {e}"
                )

        # Melt to long format
        value_columns = [col for col in df.columns if col != date_col]
        df_melted = df.melt(id_vars=[date_col], var_name="unique_id", value_name="y")

        # Rename date column to 'ds'
        df_melted = df_melted.rename(columns={date_col: "ds"})

        # Drop rows with NaN values in 'y'
        df_melted = df_melted.dropna(subset=["y"])

        # Ensure 'y' is numeric
        df_melted["y"] = pd.to_numeric(df_melted["y"], errors="coerce")
        df_melted = df_melted.dropna(subset=["y"])

        # Handle potential duplicate combinations of unique_id and ds
        df_melted = df_melted.drop_duplicates(subset=["unique_id", "ds"])

        # Ensure unique_id is string type
        df_melted["unique_id"] = df_melted["unique_id"].astype(str)

        if df_melted.empty:
            raise ValueError(f"No valid numeric data found in {dataset_path}")

        return df_melted

    # Handle long format but with different column names
    elif len(df.columns) == 2:
        # Check if we have date and value columns
        date_col = None
        value_col = None

        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(
                df[col]
            ) or pd.api.types.is_string_dtype(df[col]):
                date_col = col
            elif pd.api.types.is_numeric_dtype(df[col]):
                value_col = col

        if date_col is None or value_col is None:
            raise ValueError(
                f"Could not identify date and value columns in {dataset_path}"
            )

        # Convert date column to datetime if needed
        if pd.api.types.is_string_dtype(df[date_col]):
            try:
                df[date_col] = pd.to_datetime(df[date_col])
            except Exception as e:
                raise ValueError(
                    f"Could not parse date column '{date_col}' in {dataset_path}: {e}"
                )

        # Create expected format
        result = df[[date_col, value_col]].copy()
        result.columns = ["ds", "y"]
        result["unique_id"] = "series_1"

        # Drop rows with NaN values
        result = result.dropna()

        # Handle potential duplicate combinations of unique_id and ds
        result = result.drop_duplicates(subset=["unique_id", "ds"])

        if result.empty:
            raise ValueError(f"No valid data found in {dataset_path}")

        return result

    else:
        raise ValueError(f"Unexpected DataFrame shape in {dataset_path}: {df.shape}")


def calculate_cutoff_for_dataset(dataset_path, frequency, seasonality, test_split):
    """
    Calculate the min date, cutoff date and max date for a single dataset.

    Args:
        dataset_path: Path to the dataset parquet file
        frequency: Data frequency (e.g., 'D', 'M', 'Q')
        seasonality: Seasonal period length
        test_split: Fraction of data to use for testing

    Returns:
        Tuple of (min_date, cutoff_date, max_date) where min_date is the minimum date,
        cutoff_date is the first date in test set and max_date is the maximum date
        in the entire dataset
    """
    # Load the dataset
    df = pd.read_parquet(dataset_path)

    # Convert to expected format
    df = convert_to_expected_format(df, dataset_path)

    # Get the min and max dates from the entire dataset
    min_date = df["ds"].min()
    max_date = df["ds"].max()

    # Process the dataframe to get train/test split
    _, test_data, _ = process_df(df, frequency, seasonality, test_split)

    # Get the cutoff date (first date in test set)
    cutoff_date = test_data["ds"].min()

    return min_date, cutoff_date, max_date


def calculate_all_cutoff_dates(output_dir):
    """
    Calculate min dates, cutoff dates and max dates for all available datasets.

    Args:
        output_dir: Directory containing available_datasets.csv and where to save cutoff_dates.parquet

    Returns:
        DataFrame with all min dates, cutoff dates and max dates
    """
    # Load available datasets
    available_datasets = load_available_datasets(output_dir)

    if available_datasets.empty:
        print("Warning: No available datasets found!")
        return pd.DataFrame(
            columns=[
                "dataset_name",
                "full_name",
                "min_date",
                "cutoff_date",
                "max_date",
                "frequency",
                "seasonality",
            ]
        )

    print(f"Calculating cutoff dates for {len(available_datasets)} datasets...")

    cutoff_results = []
    failed_datasets = []

    for _, row in available_datasets.iterrows():
        try:
            dataset_path = Path(row["file_path"])
            frequency = row["frequency"]
            seasonality = int(row["seasonality"])
            test_split = 0.2  # Default test split

            print(f"  Processing {row['full_name']}...")

            min_date, cutoff_date, max_date = calculate_cutoff_for_dataset(
                dataset_path, frequency, seasonality, test_split
            )

            cutoff_results.append(
                {
                    "full_name": row["full_name"],
                    "min_date": min_date,
                    "cutoff_date": cutoff_date,
                    "max_date": max_date,
                    "frequency": frequency,
                    "seasonality": seasonality,
                    "file_path": str(dataset_path),
                }
            )

            print(
                f"    Min date: {min_date}, Cutoff date: {cutoff_date}, Max date: {max_date}"
            )

        except Exception as e:
            error_msg = f"Error processing {row['full_name']}: {str(e)}"
            print(f"    {error_msg}")
            failed_datasets.append(
                {
                    "full_name": row["full_name"],
                    "error": str(e),
                    "file_path": str(row["file_path"]),
                }
            )
            continue

    # Create DataFrame from results
    cutoff_df = pd.DataFrame(cutoff_results)

    # Convert datetime columns to date format for cleaner output
    if not cutoff_df.empty:
        cutoff_df["min_date"] = pd.to_datetime(cutoff_df["min_date"]).dt.date
        cutoff_df["cutoff_date"] = pd.to_datetime(cutoff_df["cutoff_date"]).dt.date
        cutoff_df["max_date"] = pd.to_datetime(cutoff_df["max_date"]).dt.date

        # Reorder columns to have min_date, cutoff_date, max_date in sequence
        cutoff_df = cutoff_df[
            [
                "full_name",
                "min_date",
                "cutoff_date",
                "max_date",
                "frequency",
                "seasonality",
                "file_path",
            ]
        ]

        print(f"\nSuccessfully calculated cutoff dates for {len(cutoff_df)} datasets.")
    else:
        print("\nNo cutoff dates were calculated successfully.")

    if failed_datasets:
        print(f"\nFailed to process {len(failed_datasets)} datasets:")
        for failed in failed_datasets:
            print(f"  - {failed['full_name']}: {failed['error']}")

        # Save failed datasets for debugging
        failed_df = pd.DataFrame(failed_datasets)
        failed_path = output_dir / "failed_cutoff_calculations.csv"
        failed_df.to_csv(failed_path, index=False)
        print(f"\nSaved failed dataset details to: {failed_path}")

    return cutoff_df


def main():
    """Main function to calculate cutoff dates for all available datasets."""
    # Get output directory
    try:
        from settings import config

        output_dir = Path(config("OUTPUT_DIR"))
    except ImportError:
        output_dir = Path(__file__).parent.parent / "_output"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Calculate cutoff dates for all datasets
    cutoff_df = calculate_all_cutoff_dates(output_dir)

    # Save results to CSV file
    output_path = output_dir / "cutoff_dates.csv"
    cutoff_df.to_csv(output_path, index=False)

    print(f"\nSaved cutoff dates to: {output_path}")

    # Display summary
    if not cutoff_df.empty:
        print("\nCutoff dates summary:")
        print(
            cutoff_df[
                [
                    "full_name",
                    "min_date",
                    "cutoff_date",
                    "max_date",
                    "frequency",
                    "seasonality",
                ]
            ].to_string(index=False)
        )

    return cutoff_df


if __name__ == "__main__":
    main()
