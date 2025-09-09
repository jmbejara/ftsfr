#!/usr/bin/env python3
"""
organize_ftsfr_datasets.py - Organize and filter ftsfr datasets

This script scans the DATA_DIR for all ftsfr_*.parquet files, filters out entities 
with fewer than MIN_OBSERVATIONS time observations, and saves the filtered datasets to 
_data/formatted/ while preserving the module folder structure.
"""

import polars as pl
from pathlib import Path
from typing import List, Dict
import argparse

# Import config from settings
from settings import config

DATA_DIR = config("DATA_DIR")
MIN_OBSERVATIONS = 1

def find_ftsfr_files(data_dir: Path) -> Dict[str, List[Path]]:
    """
    Find all ftsfr_*.parquet files in the data directory.
    
    Args:
        data_dir: Path to the data directory to scan
        
    Returns:
        Dictionary mapping module names to lists of ftsfr files
    """
    ftsfr_files = {}
    
    # Scan all subdirectories for ftsfr_*.parquet files
    for module_dir in data_dir.iterdir():
        if not module_dir.is_dir():
            continue
            
        module_name = module_dir.name
        ftsfr_files[module_name] = []
        
        # Find all ftsfr_*.parquet files in this module directory
        for file_path in module_dir.glob("ftsfr_*.parquet"):
            ftsfr_files[module_name].append(file_path)
    
    return ftsfr_files


def filter_and_save_datasets(data_dir: Path, ftsfr_files: Dict[str, List[Path]]) -> List[Path]:
    """
    Filter datasets to keep only entities with >=MIN_OBSERVATIONS observations and save to formatted structure.
    
    Args:
        data_dir: Path to the data directory
        ftsfr_files: Dictionary mapping module names to ftsfr file lists
        
    Returns:
        List of created file paths in the formatted directory
    """
    formatted_dir = data_dir / "formatted"
    created_files = []
    
    # Create the main formatted directory
    formatted_dir.mkdir(exist_ok=True)
    
    # Process each module
    for module_name, files in ftsfr_files.items():
        # Create module directory in formatted structure
        module_formatted_dir = formatted_dir / module_name
        module_formatted_dir.mkdir(exist_ok=True)
        
        # Process each ftsfr file
        for source_file in files:
            destination_file = module_formatted_dir / source_file.name
            
            try:
                # Load dataset with Polars
                df = pl.read_parquet(source_file)
                
                # Identify entity column
                entity_col = None
                entity_candidates = ['unique_id', 'id', 'entity_id', 'series_id']
                for col in entity_candidates:
                    if col in df.columns:
                        entity_col = col
                        break
                
                if entity_col is None:
                    print(f"  Warning: No entity column found in {source_file.name}, copying without filtering")
                    # If no entity column found, just copy the file
                    df.write_parquet(destination_file)
                    created_files.append(destination_file)
                    continue
                
                # Count observations per entity
                entity_counts = df.group_by(entity_col).len().sort(entity_col)
                
                # Get entities with >=MIN_OBSERVATIONS observations
                valid_entities = entity_counts.filter(pl.col("len") >= MIN_OBSERVATIONS)[entity_col]
                
                # Filter the dataset
                filtered_df = df.filter(pl.col(entity_col).is_in(valid_entities))
                
                # Save filtered dataset
                filtered_df.write_parquet(destination_file)
                created_files.append(destination_file)
                
                # Print filtering stats
                original_entities = len(entity_counts)
                kept_entities = len(valid_entities)
                print(f"  {source_file.name}: kept {kept_entities}/{original_entities} entities (filtered out {original_entities - kept_entities} with <MIN_OBSERVATIONS observations)")
                
            except Exception as e:
                print(f"  Error processing {source_file.name}: {e}")
                continue
    
    return created_files


def main():
    """Main function to organize ftsfr datasets."""
    parser = argparse.ArgumentParser(description="Organize ftsfr datasets into formatted structure")
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR,
                        help=f"Data directory to scan (default: {DATA_DIR})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without actually copying files")
    
    args = parser.parse_args()
    
    data_dir = Path(args.data_dir)
    
    if not data_dir.exists():
        raise ValueError(f"Error: Data directory {data_dir} does not exist!")
    
    # Find all ftsfr files
    ftsfr_files = find_ftsfr_files(data_dir)
    
    # Report what was found
    total_files = sum(len(files) for files in ftsfr_files.values())
    
    if args.dry_run:
        print("\nDry run - no files were copied.")
        return 0
    
    # Filter datasets and save to formatted structure
    _ = filter_and_save_datasets(data_dir, ftsfr_files)
    
    return 0


if __name__ == "__main__":
    exit(main())