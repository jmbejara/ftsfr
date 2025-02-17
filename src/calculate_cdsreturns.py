import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
from pathlib import Path

def process_rates(raw_rates, start_date, end_date):
    """
    Processes raw interest rate data by filtering within a specified date range 
    and converting column names to numerical maturity values.

    Parameters:
    - raw_rates (DataFrame): The raw interest rate data with column names like 'SVENY01', 'SVENY02', etc.
    - start_date (str or datetime): The start date for filtering.
    - end_date (str or datetime): The end date for filtering.

    Returns:
    - DataFrame: Processed interest rate data with maturity values as column names and rates in decimal form.
    """
    raw_rates = raw_rates.dropna()  
    # Filter by the specified date range
    raw_rates.columns = raw_rates.columns.str.extract(r'(\d+)$')[0].astype(int)
    rates = raw_rates[(raw_rates.index >= pd.to_datetime(start_date)) & (raw_rates.index <= pd.to_datetime(end_date))]/100
    
    return rates


def extrapolate_rates(rates):
    """
    Applies cubic spline extrapolation to fill in interest rate values at quarterly intervals.

    Parameters:
    - rates (DataFrame): A DataFrame where columns represent maturity years, 
                         and values are interest rates.

    Returns:
    - df_quarterly: A DataFrame with interpolated rates at quarterly maturities.
    """
    years = np.array(rates.columns)  
    # Define the new maturities at quarterly intervals (0.25, 0.5, ..., 30)
    quarterly_maturities = np.arange(0.25, 30.25, 0.25)

    interpolated_data = []

    for _, row in rates.iterrows():
        values = row.values  # Get values for the current row
        cs = CubicSpline(years, values, extrapolate=True)  # Create spline function
        interpolated_values = cs(quarterly_maturities)  # Interpolate for quarterly intervals
        interpolated_data.append(interpolated_values)  # Append results

    # Create a new DataFrame with interpolated values for all rows
    df_quarterly = pd.DataFrame(interpolated_data, columns=quarterly_maturities)
    df_quarterly.index = rates.index
    return df_quarterly

def calc_discount(df, start_date, end_date):
    """
    Calculates the discount factor for given interest rate data using quarterly rates.

    Parameters:
    - df (DataFrame): The raw interest rate data.
    - start_date (str or datetime): The start date for filtering.
    - end_date (str or datetime): The end date for filtering.

    Returns:
    - DataFrame: Discount factors for various maturities.
    """
    # Call the function to get rates
    rates_data = process_rates(df, start_date, end_date)  
    if rates_data is None:
        print("No data available for the given date range.")
        return None

    quarterly_rates = extrapolate_rates(rates_data)

    quarterly_discount = pd.DataFrame(columns=quarterly_rates.columns, index=quarterly_rates.index)
    for col in quarterly_rates.columns:
        quarterly_discount[col] = quarterly_rates[col].apply(lambda x: np.exp(-(col * x) / 4))

    return quarterly_discount

def assign_quantiles(group, n_quantiles=20):
    """
    Assigns quantile rankings to a DataFrame based on the 'parspread' column.

    Parameters:
    - group (DataFrame): The input pandas DataFrame containing at least the 'parspread' column.
    - n_quantiles (int): The number of quantiles to divide the data into. Default is 20.

    Returns:
    - DataFrame: The modified input DataFrame with a new 'quantile' column indicating the quantile ranking of each 'parspread'.
    """
    group['quantile'] = pd.qcut(group['parspread'], n_quantiles, labels=False) + 1
    return group

def process_cds(cds_spread, start_date, end_date, method = 'mean'):
    """
    Processes CDS spread data by filtering, backfilling missing values, 
    grouping by date and ticker, and assigning quantiles.

    Parameters:
    - cds_spread (DataFrame): The CDS spread data containing 'date', 'ticker', and 'parspread' columns.
    - start_date (str or datetime): The start date for filtering.
    - end_date (str or datetime): The end date for filtering.
    - method (str): Aggregation method ('mean', 'median', 'weighted') for computing CDS spread values.

    Returns:
    - DataFrame: A pivot table of CDS spreads with quantile groupings.
    """
    cds_spread = cds_spread[(cds_spread['date']>= start_date) & (cds_spread['date']<end_date)]
    cds_spread= cds_spread.bfill()
    cds_spread = cds_spread.set_index('date')
    cds_spread.index = pd.to_datetime(cds_spread.index)

    cds_unique = cds_spread.groupby(['date','ticker']).mean().reset_index()
    cds_unique = cds_unique.sort_values(['date', 'parspread'])

    # Group by 'date' and apply the function to assign quantiles
    cds_unique_groups = cds_unique.groupby('date').apply(assign_quantiles)
    cds_unique_groups.rename(columns={'date': 'Date'}, inplace=True)


    cds_unique_groups.reset_index(inplace=True)

    cds_unique_groups.set_index('quantile', inplace = True)

    def weighted_mean(data):
        weights = data['parspread']
        return (data['parspread'] * weights).sum() / weights.sum()

    if method == 'mean':
        comb_spread = cds_unique_groups.groupby(['quantile', 'Date'])['parspread'].mean().reset_index()
    elif method == 'median':
        comb_spread = cds_unique_groups.groupby(['quantile', 'Date'])['parspread'].median().reset_index()
    elif method == 'weighted':
        comb_spread = cds_unique_groups.groupby(['quantile', 'Date']).apply(weighted_mean).reset_index(name = 'parspread')

    # Pivot the table to have 'date' as index, 'quantile' as columns, and mean 'parspread' as values
    pivot_table = comb_spread.pivot_table(index='Date', columns='quantile', values='parspread')
    return pivot_table

def calc_cds_return(cds_spread, raw_rates, start_date, end_date):
    """ 
    Calculates CDS returns using spread data and the He-Kelly formula.

    Parameters:
    - cds_spread (DataFrame): The CDS spread data containing 'date', 'ticker', and 'parspread' columns.
    - raw_rates (DataFrame): The raw interest rate data for discount calculations.
    - start_date (str or datetime): The start date for filtering.
    - end_date (str or datetime): The end date for filtering.

    Returns:
    - DataFrame: Calculated CDS returns based on the He-Kelly formula.
    """
    pivot_table = process_cds(cds_spread, start_date, end_date)
    loss_given_default = 0.6
    lambda_df = 4 * np.log(1+(pivot_table/(4*loss_given_default)))

    quarters = np.arange(0.25, 20.25, 0.25)  # 1 to 20 quarters
    quarterly_discount = calc_discount(raw_rates, start_date, end_date)
    quarterly_discount = quarterly_discount[:-1]

    risky_duration = pd.DataFrame(index=lambda_df.index, columns= lambda_df.columns)
    for col in lambda_df.columns:
            quarterly_survival_probability = pd.DataFrame(index=lambda_df.index, columns=quarters)
            for quarter in quarters:
                quarterly_survival_probability[quarter] = np.exp(-((quarter * lambda_df[col])))
            quarterly_discount = quarterly_discount.loc[:,quarterly_discount.columns.isin(quarters)]
            quarterly_discount_filtered = quarterly_discount[quarterly_discount.index.isin(quarterly_survival_probability.index)]
            quarterly_survival_probability_filtered = quarterly_survival_probability[quarterly_survival_probability.index.isin(quarterly_discount.index)]
            temp_df = quarterly_discount_filtered * quarterly_survival_probability_filtered
            temp_df.dropna(inplace=True)
            risky_duration[col] = 0.25 * temp_df.sum(axis=1)
    risky_duration.dropna(inplace=True)
    risky_duration_shifted = risky_duration.shift(1)
    cds_spread_shifted = pivot_table.shift(1)
    cds_spread_change = pivot_table.diff()
    cds_return = (-(cds_spread_shifted/250) + (cds_spread_change * risky_duration_shifted))
    cds_return.dropna(inplace=True)
    return cds_return
