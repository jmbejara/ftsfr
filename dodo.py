"""
Default dodo file that routes to dodo_01_pull.py

This file enables users to run `doit` without arguments and get the pull tasks.
For other steps, use:
  - doit -f dodo_00_pull_bloomberg.py  (Bloomberg-only pulls)
  - doit -f dodo_02_forecasting.py     (forecasting jobs)
  - doit -f dodo_03_sensitivity.py     (data-cleaning sensitivity analysis)
  - doit -f dodo_04_paper.py           (paper, slides, internet appendix)
"""

# Import all tasks from the pull module
# This works because doit looks for functions starting with "task_"
# and objects with "create_doit_tasks" in the namespace
from dodo_01_pull import *

# You could also optionally restrict which tasks run by default:
# DOIT_CONFIG = {
#     'default_tasks': ['pull', 'format'],  # specify which tasks to run by default
# }
