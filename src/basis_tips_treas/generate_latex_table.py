r"""
This module loads summary data from a CSV file and converts it into a LaTeX table.

The summary CSV file is expected to be located at:
    OUTPUT_DATA / 'tips_treasury_summary.csv'

The generated LaTeX table is saved as:
    OUTPUT_DATA / 'tips_treasury_summary_table.tex'

You can include the resulting .tex file in your LaTeX documents. For example:

\documentclass{article}
\usepackage{booktabs}
\begin{document}
\begin{table}
\centering
\input{tips_treasury_summary_table.tex}
\end{table}
\end{document}
"""

import pandas as pd
from pathlib import Path
from settings import config

# Set up the directory where the summary CSV file is stored
OUTPUT_DATA = Path(config("OUTPUT_DIR"))

# Optional: Suppress scientific notation and set float formatting for LaTeX output
pd.set_option('display.float_format', lambda x: '%.2f' % x)
float_format_func = lambda x: '{:.2f}'.format(x)

# Define the path to the summary CSV file
csv_file = OUTPUT_DATA / 'tips_treasury_summary.csv'

# Read the CSV file into a DataFrame, using the first column as the index
df_summary = pd.read_csv(csv_file, index_col=0)

# Convert the DataFrame to a LaTeX table string
latex_table_string = df_summary.to_latex(float_format=float_format_func, escape=False)

# Optionally, print the LaTeX table string to the console for verification
print(latex_table_string)

# Define the output file path for the LaTeX table
output_tex_file = OUTPUT_DATA / 'tips_treasury_summary_table.tex'

# Write the LaTeX table string to the .tex file
with open(output_tex_file, "w") as f:
    f.write(latex_table_string)
