"""
create_data_glimpses.py

Parses dodo.py to find all CSV/Parquet files and creates comprehensive
data glimpse reports in both XML (machine-readable) and TXT (human-readable) formats.
"""

import argparse
import os
import xml.sax.saxutils as saxutils
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path

import polars as pl

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))
BASE_DIR = Path(config("BASE_DIR"))


def parse_dodo_tasks():
    """Use doit's internal API to get all tasks and their associated data files."""
    import sys
    from pathlib import Path
    
    # Add the project root to the Python path
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    import dodo
    
    # Get all task functions from the dodo module
    task_functions = [getattr(dodo, name) for name in dir(dodo) if name.startswith('task_')]
    
    # Dictionary to store task_name -> list of files
    task_files = {}
    
    # Generate tasks from each task function
    for task_func in task_functions:
        try:
            # Call the task function to get task(s)
            result = task_func()
            
            # Handle both single tasks and generators
            if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
                # It's a generator or list of tasks
                for task_dict in result:
                    if isinstance(task_dict, dict):
                        process_task_dict(task_dict, task_func.__name__, task_files)
            elif isinstance(result, dict):
                # It's a single task dictionary
                process_task_dict(result, task_func.__name__, task_files)
        except Exception as e:
            print(f"Warning: Could not process task function {task_func.__name__}: {e}")
            continue
    
    return task_files


def process_task_dict(task_dict, base_name, task_files):
    """Process a single task dictionary to extract files."""
    # Get the task name
    if 'name' in task_dict:
        # For subtasks, combine base name with task name
        if base_name.startswith('task_'):
            base_name = base_name[5:]  # Remove 'task_' prefix
        task_name = f"{base_name}:{task_dict['name']}"
    else:
        # For simple tasks without names
        if base_name.startswith('task_'):
            task_name = base_name[5:]  # Remove 'task_' prefix
        else:
            task_name = base_name
    
    files = set()
    
    # Extract files from targets
    if 'targets' in task_dict and task_dict['targets']:
        for target in task_dict['targets']:
            target_str = str(target)
            if target_str.endswith(('.csv', '.parquet')):
                files.add(target_str)
    
    # Extract files from file_dep
    if 'file_dep' in task_dict and task_dict['file_dep']:
        for dep in task_dict['file_dep']:
            dep_str = str(dep)
            if dep_str.endswith(('.csv', '.parquet')):
                files.add(dep_str)
    
    if files:
        task_files[task_name] = sorted(files)


def get_dataset_report(filepath):
    """Return a dict with file metadata, shape, columns, sample values, numeric stats, and glimpse."""
    report = {}
    try:
        # File info
        report["file_size_bytes"] = os.path.getsize(filepath)
        report["file_size_mb"] = report["file_size_bytes"] / (1024 * 1024)
        report["file_type"] = Path(filepath).suffix.replace(".", "").upper()
        # Load data
        if filepath.endswith(".csv"):
            df = pl.read_csv(filepath, n_rows=10000)
        else:
            df = pl.read_parquet(filepath)
        # Shape
        report["n_rows"], report["n_cols"] = df.shape
        # Columns info
        null_counts = df.null_count().to_dicts()[0]
        columns = []
        for col in df.columns:
            dtype = str(df.schema[col])
            n_null = null_counts.get(col, 0)
            pct_null = (
                (n_null / report["n_rows"] * 100) if report["n_rows"] > 0 else 0.0
            )
            columns.append(
                {"name": col, "dtype": dtype, "pct_null": pct_null, "n_null": n_null}
            )
        report["columns"] = columns
        # Sample values
        sample = df.head(5).to_dicts()
        report["sample_values"] = sample
        # Capture polars text representation of first 5 rows
        output = StringIO()
        with redirect_stdout(output):
            df.glimpse()
        report["sample_text"] = output.getvalue()
        # Numeric stats
        numeric_types = {
            pl.Int8,
            pl.Int16,
            pl.Int32,
            pl.Int64,
            pl.UInt8,
            pl.UInt16,
            pl.UInt32,
            pl.UInt64,
            pl.Float32,
            pl.Float64,
        }
        numeric_cols = [c for c in df.columns if df.schema[c] in numeric_types]
        numeric_stats = []
        if numeric_cols:
            stats_df = df.select(
                [
                    *(pl.col(c).min().alias(f"{c}_min") for c in numeric_cols),
                    *(pl.col(c).max().alias(f"{c}_max") for c in numeric_cols),
                    *(pl.col(c).mean().alias(f"{c}_mean") for c in numeric_cols),
                    *(pl.col(c).median().alias(f"{c}_median") for c in numeric_cols),
                ]
            )
            stats_dict = stats_df.to_dicts()[0]
            for col in numeric_cols:
                numeric_stats.append(
                    {
                        "name": col,
                        "min": stats_dict.get(f"{col}_min"),
                        "max": stats_dict.get(f"{col}_max"),
                        "mean": stats_dict.get(f"{col}_mean"),
                        "median": stats_dict.get(f"{col}_median"),
                    }
                )
        report["numeric_stats"] = numeric_stats
        # Glimpse
        output = StringIO()
        with redirect_stdout(output):
            df.glimpse(max_items_per_column=0)
        report["glimpse"] = output.getvalue()
    except Exception as e:
        report["error"] = f"ERROR: Could not read file - {str(e)}"
    return report


def format_task_name(task_name):
    """Format task name for display."""
    # Handle subtask names like "pull:cds_bond_basis"
    if ":" in task_name:
        main_task, sub_task = task_name.split(":", 1)
        # Format both parts
        main_formatted = main_task.replace("_", " ").title()
        sub_formatted = sub_task.replace("_", " ").title()
        return f"{main_formatted}: {sub_formatted}"
    else:
        # Handle simple task names
        formatted = task_name.replace("_", " ").title()
        return formatted


def get_task_category(task_name):
    """Extract the main task category from a task name."""
    if ":" in task_name:
        return task_name.split(":", 1)[0]
    else:
        return task_name


def format_file_size(size_bytes):
    """Format file size in human-readable format."""
    size_mb = size_bytes / (1024 * 1024)
    if size_mb < 1:
        return f"{size_bytes} bytes"
    elif size_mb < 1024:
        return f"{size_mb:.1f} MB"
    else:
        return f"{size_mb / 1024:.1f} GB"


def filename_to_anchor(filename):
    """Convert a filename to a markdown anchor link format."""
    # Convert to lowercase and replace non-alphanumeric characters with hyphens
    # Keep the full filename including extension since section headers include it
    anchor = filename.lower()
    anchor = ''.join(c if c.isalnum() else '-' for c in anchor)
    # Remove multiple consecutive hyphens and leading/trailing hyphens
    while '--' in anchor:
        anchor = anchor.replace('--', '-')
    anchor = anchor.strip('-')
    return anchor


def create_txt_report(existing_files, include_samples=True, include_stats=True):
    """Create a human-readable TXT format Data Glimpses Report."""
    output_lines = []

    # Parse dodo tasks to group files
    task_files = parse_dodo_tasks()

    # Create a mapping of files to tasks
    file_to_tasks = {}
    for task, files in task_files.items():
        for f in files:
            if f in existing_files:
                if f not in file_to_tasks:
                    file_to_tasks[f] = []
                file_to_tasks[f].append(task)

    # Header
    output_lines.append("# Data Glimpses Report")
    output_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append(f"Total files: {len(existing_files)}")
    output_lines.append("")

    # Summary section grouped by task categories and subtasks
    output_lines.append("## Summary of Datasets by Task")
    output_lines.append("")

    # Group files by their task categories
    task_grouped = {}
    for f in sorted(existing_files):
        tasks = file_to_tasks.get(f, ["Unknown"])
        for task in tasks:
            category = get_task_category(task)
            if category not in task_grouped:
                task_grouped[category] = {}
            if task not in task_grouped[category]:
                task_grouped[category][task] = []
            task_grouped[category][task].append(f)

    # Output the summary
    for category in sorted(task_grouped.keys()):
        category_formatted = format_task_name(category)
        output_lines.append(f"### {category_formatted}")
        
        for task in sorted(task_grouped[category].keys()):
            if ":" in task:
                # This is a subtask, show it as a subheading
                task_formatted = format_task_name(task)
                output_lines.append(f"#### {task_formatted}")
                for f in sorted(task_grouped[category][task]):
                    filename = Path(f).name
                    anchor = filename_to_anchor(filename)
                    output_lines.append(f"- [`{filename}`](#{anchor})")
            else:
                # This is a main task without subtasks
                for f in sorted(task_grouped[category][task]):
                    filename = Path(f).name
                    anchor = filename_to_anchor(filename)
                    output_lines.append(f"- [`{filename}`](#{anchor})")
        output_lines.append("")

    output_lines.append("---")

    # Process each file
    for i, f in enumerate(sorted(existing_files), 1):
        filename = Path(f).name
        report = get_dataset_report(f)

        output_lines.append("")
        output_lines.append(f"## {filename}")
        output_lines.append(f"**Path:** `{f}`")

        if "error" in report:
            output_lines.append(f"**ERROR:** {report['error']}")
            output_lines.append("---")
            continue

        # File metadata
        output_lines.append(
            f"**Size:** {format_file_size(report['file_size_bytes'])} | **Type:** {report['file_type'].capitalize()} | **Shape:** {report['n_rows']:,} rows × {report['n_cols']} columns"
        )
        output_lines.append("")

        # Columns section
        output_lines.append("### Columns")
        output_lines.append("```")
        for col in report["columns"]:
            null_info = f" ({col['pct_null']:.1f}% null)" if col['pct_null'] > 0 else ""
            output_lines.append(f"{col['name']:<40} {col['dtype']:<15}{null_info}")
        output_lines.append("```")
        output_lines.append("")

        # Sample values section (conditional)
        if include_samples:
            output_lines.append("### Sample Values (first 5 rows)")
            output_lines.append("```")
            output_lines.append(report["sample_text"].rstrip())
            output_lines.append("```")
            output_lines.append("")

        # Numeric statistics section (conditional)
        if include_stats and report["numeric_stats"]:
            output_lines.append("### Numeric Column Statistics")
            output_lines.append("```")
            for stat in report["numeric_stats"]:
                output_lines.append(
                    f"{stat['name']}: min={stat['min']}, max={stat['max']}, "
                    f"mean={stat['mean']:.2f}, median={stat['median']}"
                )
            output_lines.append("```")
            output_lines.append("")

        # Add separator between datasets
        output_lines.append("---")

    # Remove the final separator so document doesn't end with a transition
    if output_lines and output_lines[-1] == "---":
        output_lines.pop()
        # Also remove the empty line before it if it exists
        if output_lines and output_lines[-1] == "":
            output_lines.pop()

    return "\n".join(output_lines)


def create_xml_report(existing_files):
    """Create a machine-readable XML format Data Glimpses Report."""
    output_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<data_glimpses_report>",
        "  <summary>",
    ]

    # Add summary section
    for f in sorted(existing_files):
        filename = Path(f).name
        output_lines.append(
            f'    <dataset filename="{saxutils.escape(filename)}" path="{saxutils.escape(str(f))}"/>'
        )
    output_lines.append("  </summary>")
    output_lines.append("  <datasets>")

    # Add each dataset
    for f in sorted(existing_files):
        filename = Path(f).name
        report = get_dataset_report(f)
        output_lines.append(
            f'    <dataset filename="{saxutils.escape(filename)}" path="{saxutils.escape(str(f))}">'
        )

        # File info
        if "error" in report:
            output_lines.append(
                f"      <error>{saxutils.escape(report['error'])}</error>"
            )
            output_lines.append("    </dataset>")
            continue

        output_lines.append(
            f'      <file_info size_mb="{report["file_size_mb"]:.1f}" type="{report["file_type"]}"/>'
        )
        output_lines.append(
            f'      <shape rows="{report["n_rows"]}" cols="{report["n_cols"]}"/>'
        )

        # Columns
        output_lines.append("      <columns>")
        for col in report["columns"]:
            output_lines.append(
                f'        <column name="{saxutils.escape(col["name"])}" dtype="{saxutils.escape(col["dtype"])}" pct_null="{col["pct_null"]:.1f}"/>'
            )
        output_lines.append("      </columns>")

        # Sample values
        output_lines.append("      <sample_values>")
        for row in report["sample_values"]:
            # Show as dict string, truncate if too long
            row_str = str(row)
            if len(row_str) > 300:
                row_str = row_str[:297] + "..."
            output_lines.append(f"        <row>{saxutils.escape(row_str)}</row>")
        output_lines.append("      </sample_values>")

        # Numeric stats
        if report["numeric_stats"]:
            output_lines.append("      <numeric_stats>")
            for stat in report["numeric_stats"]:
                output_lines.append(
                    f'        <column name="{saxutils.escape(stat["name"])}" min="{stat["min"]}" max="{stat["max"]}" mean="{stat["mean"]}" median="{stat["median"]}"/>'
                )
            output_lines.append("      </numeric_stats>")

        # Glimpse
        output_lines.append("      <glimpse><![CDATA[")
        output_lines.append(report["glimpse"].rstrip())
        output_lines.append("      ]]></glimpse>")
        output_lines.append("    </dataset>")

    output_lines.append("  </datasets>")
    output_lines.append("</data_glimpses_report>")

    return "\n".join(output_lines)


def main():
    """Main function to create the data glimpses files in both XML and TXT formats."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate data glimpses report from dodo.py tasks")
    parser.add_argument("--no-samples", action="store_true", 
                       help="Exclude sample values sections from the report")
    parser.add_argument("--no-stats", action="store_true", 
                       help="Exclude numeric column statistics sections from the report")
    args = parser.parse_args()
    
    print("Parsing dodo.py for tasks and data files...")
    task_files = parse_dodo_tasks()

    # Collect all files and check which exist
    all_files = set()
    for files in task_files.values():
        all_files.update(files)

    existing_files = {f for f in all_files if Path(f).exists()}

    print(
        f"Found {len(task_files)} tasks with {len(existing_files)} existing data files"
    )

    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate and save TXT report
    print("\nGenerating TXT report...")
    include_samples = not args.no_samples
    include_stats = not args.no_stats
    
    if args.no_samples:
        print("  - Excluding sample values sections")
    if args.no_stats:
        print("  - Excluding numeric statistics sections")
    
    txt_content = create_txt_report(existing_files, include_samples=include_samples, include_stats=include_stats)
    # txt_output_file = OUTPUT_DIR / "data_glimpses.txt"
    txt_output_file = BASE_DIR / "docs_src" / "data_glimpses.md"
    with open(txt_output_file, "w", encoding="utf-8") as f:
        f.write(txt_content)
    print(f"Human-readable TXT report saved to: {txt_output_file}")

    # Generate and save XML report
    # print("\nGenerating XML report...")
    # xml_content = create_xml_report(existing_files)
    # # xml_output_file = OUTPUT_DIR / "data_glimpses.xml"
    # # xml_output_file = BASE_DIR / "docs_src" / "data_glimpses.xml"
    # with open(xml_output_file, "w", encoding="utf-8") as f:
    #     f.write(xml_content)
    # print(f"Machine-readable XML report saved to: {xml_output_file}")

    print(f"\nProcessed {len(existing_files)} files from {len(task_files)} tasks")
    print("Report generated successfully!")


if __name__ == "__main__":
    main()
