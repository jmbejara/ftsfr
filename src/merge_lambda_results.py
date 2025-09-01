#!/usr/bin/env python3
"""
merge_lambda_results.py - Generate rsync command to merge lambda results with local error metrics

This script generates an rsync command to copy files from ./lambda_results to 
./_output/forecasting/error_metrics/ without deleting existing local files.
Lambda results take precedence when files exist in both locations.
"""

from pathlib import Path


def generate_merge_command():
    """Generate rsync command to merge lambda results with local error metrics."""
    lambda_dir = Path("./lambda_results")
    local_dir = Path("./_output/forecasting/error_metrics")
    
    if not lambda_dir.exists():
        print(f"Error: {lambda_dir.absolute()} does not exist!")
        return
    
    # Create local directory if it doesn't exist
    local_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate rsync command
    # -a: archive mode (preserves permissions, timestamps, etc.)
    # -v: verbose
    # -h: human-readable progress
    # --progress: show progress
    # --update: skip files that are newer on the destination (but we want lambda to override, so we don't use this)
    # --backup: make backups of existing files (optional)
    # --suffix: suffix for backup files (optional)
    
    rsync_cmd = f"""rsync -avh --progress \\
  "{lambda_dir.absolute()}/" \\
  "{local_dir.absolute()}/"
"""
    
    print("=" * 60)
    print("RSYNC COMMAND TO MERGE LAMBDA RESULTS")
    print("=" * 60)
    print("This command will:")
    print("  - Copy all files from lambda_results to _output/forecasting/error_metrics/")
    print("  - Overwrite local files if they exist in lambda_results")
    print("  - Keep local files that don't exist in lambda_results")
    print("  - Create any missing directories")
    print()
    print("Command:")
    print(rsync_cmd)
    
    # Also save to a shell script
    script_path = Path("_output") / "merge_lambda_results.sh"
    script_path.parent.mkdir(exist_ok=True)
    
    with open(script_path, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# Generated rsync command to merge lambda results with local error metrics\n")
        f.write("# This will overwrite local files if they exist in lambda_results\n")
        f.write("# but will keep local files that don't exist in lambda_results\n\n")
        f.write(rsync_cmd.strip() + "\n")
    
    script_path.chmod(0o755)  # Make executable
    print(f"Command also saved to: {script_path}")
    print(f"Run with: bash {script_path}")


if __name__ == "__main__":
    generate_merge_command()