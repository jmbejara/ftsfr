import pandas as pd
import json
from settings import config

DATA_DIR = config("DATA_DIR")

data = pd.read_parquet(f"{DATA_DIR}/merged_bond_treasuries_redcode.parquet")
data['year'] = data["date"].dt.year

red_code_dict = {}
for y in list(data['year'].unique()):
    y_df = data[data['year'] == y]
    red_code_dict[y] = list(y_df['redcode'].unique())
d = {int(key): value for key, value in red_code_dict.items()}
with open(f"{DATA_DIR}/red_code_dict.json", 'w') as file:
    json.dump(d, file)