import pandas as pd
from scipy.optimize import linear_sum_assignment


def generate_corr_matrix(df_return, hkm_df):
    corr_matrix = pd.DataFrame(index=df_return.columns, columns=hkm_df.columns)

    for col1 in df_return.columns:
        for col2 in hkm_df.columns:
            x = df_return[col1].fillna(0)
            y = hkm_df[col2].fillna(0)
            corr_matrix.loc[col1, col2] = x.corr(y)

    return corr_matrix


def decide_optimal_pairs(corr_matrix):
    cost_matrix = -corr_matrix.values.astype(float)

    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    optimal_pairs = []

    for r, c in zip(row_ind, col_ind):
        row_label = corr_matrix.index[r]
        col_label = corr_matrix.columns[c]
        corr_value = corr_matrix.iloc[r, c]
        optimal_pairs.append((row_label, col_label, corr_value))

    optimal_pairs_df = pd.DataFrame(
        optimal_pairs, columns=["Commodity_1", "Commodity_2", "Correlation"]
    )

    optimal_pairs_df = optimal_pairs_df.sort_values(by="Correlation", ascending=False)

    return optimal_pairs_df.reset_index(drop=True), row_ind, col_ind
