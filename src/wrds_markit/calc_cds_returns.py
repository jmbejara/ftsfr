import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import datetime
import io

import numpy as np
import pandas as pd
import polars as pl
import pull_fed_yield_curve
import pull_markit_cds
import pull_fred
import requests
from scipy.interpolate import CubicSpline

from settings import config

DATA_DIR = config("DATA_DIR")
START_DATE = pull_markit_cds.START_DATE
END_DATE = pull_markit_cds.END_DATE
# Uncomment for testing smaller timeframe
# START_DATE = pd.Timestamp("2015-01-01")
# END_DATE = pd.Timestamp("2020-01-01")

# Set SUBFOLDER to the folder containing this file
SUBFOLDER = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

swap_rates = pull_fred.load_fred(data_dir=DATA_DIR)

def process_rates(raw_rates = None, start_date = START_DATE, end_date = END_DATE):
    """
    Processes raw interest rate data by filtering within a specified date range
    and converting column names to numerical maturity values.

    Parameters:
    - raw_rates (DataFrame): Raw interest rate data with column names like 'SVENY01', 'SVENY02', etc.
    - start_date (str or datetime): Start date for filtering.
    - end_date (str or datetime): End date for filtering.

    Returns:
    - DataFrame: Processed interest rate data with maturity values as column names and rates in decimal form.
    """
    raw_rates = raw_rates.copy().dropna()
    short_tenor_rates = swap_rates[["DGS3MO", "DGS6MO"]]
    short_tenor_rates_renamed = short_tenor_rates.rename(columns={
    'DGS3MO': 0.25,
    'DGS6MO': 0.5
})
    raw_rates.columns = raw_rates.columns.str.extract(r"(\d+)$")[0].astype(int)  # Extract numeric part from column names
    rates = raw_rates[
        (raw_rates.index >= pd.to_datetime(start_date)) &
        (raw_rates.index <= pd.to_datetime(end_date))
    ] # / 100  # Convert percentages to decimal format

    merged_rates = pd.merge(rates, short_tenor_rates_renamed, left_index=True, right_index=True, how='inner').sort_values('Date')
    cols = merged_rates.columns.tolist()
    ordered_cols = [0.25, 0.5] + [col for col in cols if col not in [0.25, 0.5]]
    merged_rates = merged_rates[ordered_cols]
    return merged_rates

def extrapolate_rates(rates = None):
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
    # 3m, 6m, 9m, 1Y, 1.25Y, 1.5Y, 1.75Y, 2Y 

    interpolated_data = []

    for _, row in rates.iterrows():
        values = row.values  # Get values for the current row
        cs = CubicSpline(years, values, extrapolate=True)  # Create spline function
        interpolated_values = cs(
            quarterly_maturities
        )  # Interpolate for quarterly intervals
        interpolated_data.append(interpolated_values)  # Append results

    # Create a new DataFrame with interpolated values for all rows
    df_quarterly = pd.DataFrame(interpolated_data, columns=quarterly_maturities)
    df_quarterly.index = rates.index
    return df_quarterly

def calc_discount(raw_rates = None, start_date = START_DATE, end_date = END_DATE):
    """
    Calculates the discount factor for given interest rate data using quarterly rates.

    Parameters:
    - raw_rates (DataFrame): The raw interest rate data.
    - start_date (str or datetime): The start date for filtering.
    - end_date (str or datetime): The end date for filtering.

    Returns:
    - DataFrame: Discount factors for various maturities.
    """
    # Call the function to get rates
    rates_data = process_rates(raw_rates, start_date, end_date)
    if rates_data is None:
        print("No data available for the given date range.")
        return None

    quarterly_rates = extrapolate_rates(rates_data)

    quarterly_discount = pd.DataFrame(
        columns=quarterly_rates.columns, index=quarterly_rates.index
    )
    for col in quarterly_rates.columns:
        quarterly_discount[col] = quarterly_rates[col].apply(
            lambda x: np.exp(-(col * x) / 4)
        )

    return quarterly_discount

def get_portfolio_dict(start_date = START_DATE, end_date = END_DATE, cds_spreads = None):
    """
    Creates a dictionary of credit portfolios based on the CDS spread data.

    Parameters:
    - start_date (str or datetime): Start date for filtering.
    - end_date (str or datetime): End date for filtering.
    - cds_spreads (pl.DataFrame): CDS spread data.
    
    Returns:
    - dict: Dictionary where keys are tenor-quantile pairs and values are Polars DataFrames.
    """

    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    if isinstance(cds_spreads, pd.DataFrame):
        cds_spreads = pl.from_pandas(cds_spreads)
    # Filter DataFrame
    filtered_cds_spread = cds_spreads.filter(
        (pl.col("date") >= start_date) & (pl.col("date") <= end_date)
    )
    filtered_cds_spread_us_only = filtered_cds_spread.filter(pl.col("country") == "United States")
    # Data Cleaning and Preparation
    cds_spread_noNA = filtered_cds_spread_us_only.drop_nulls(subset=["parspread"])
    cds_spread_noNA = cds_spread_noNA.drop(['convspreard', 'year', 'redcode'])

    # Remove duplicates
    cds_spread_unique = cds_spread_noNA.unique()
    cds_spread_unique = cds_spread_unique.filter(pl.col("parspread") <= 0.5) #Done by Palhares, remove spreads grater than 50%

    # Convert date column to year-month format
    cds_spread_unique = cds_spread_unique.with_columns(
        pl.col("date").dt.strftime("%Y-%m").alias("year_month")
    )

    # Compute Credit Quantiles
    spread_5y = cds_spread_unique.filter(pl.col("tenor") == "5Y")

    # Get first available spread for each ticker in each month
    first_spread_5y = (
        spread_5y.sort("date")
        .group_by(["ticker", "year_month"])
        .first()
        .select(["ticker", "year_month", "parspread"])
    )

    # Compute separate credit quantiles per month
    credit_quantiles = (
        first_spread_5y.group_by("year_month").agg([
            pl.col("parspread").quantile(0.2).alias("q1"),
            pl.col("parspread").quantile(0.4).alias("q2"),
            pl.col("parspread").quantile(0.6).alias("q3"),
            pl.col("parspread").quantile(0.8).alias("q4")
        ])
    )

    # Assign credit quantile labels
    first_spread_5y = first_spread_5y.join(credit_quantiles, on="year_month")

    first_spread_5y = first_spread_5y.with_columns(
        pl.when(pl.col("parspread") <= pl.col("q1"))
        .then(1)
        .when(pl.col("parspread") <= pl.col("q2"))
        .then(2)
        .when(pl.col("parspread") <= pl.col("q3"))
        .then(3)
        .when(pl.col("parspread") <= pl.col("q4"))
        .then(4)
        .otherwise(5)
        .alias("credit_quantile")
    ).select(["ticker", "year_month", "credit_quantile"])

    # Assign computed credit quantiles to all tenors
    cds_spreads_final = cds_spread_unique.join(
        first_spread_5y, on=["ticker", "year_month"], how="left"
    )
    cds_spreads_final = cds_spreads_final.sort("date")

    # Compute Representative Parspread
    relevant_tenors = ["3Y", "5Y", "7Y", "10Y"]
    relevant_quantiles = [1, 2, 3, 4, 5]

    filtered_df = cds_spreads_final.filter(
        (pl.col("tenor").is_in(relevant_tenors)) & 
        (pl.col("credit_quantile").is_in(relevant_quantiles))
    )

    rep_parspread_df = (
        filtered_df
        .group_by(["date", "tenor", "credit_quantile"])
        .agg(pl.col("parspread").mean().alias("rep_parspread"))
    )

    # Convert 'date' column to month level (truncate to the first day of the month)
    rep_parspread_df = rep_parspread_df.with_columns(
        pl.col("date").dt.truncate("1mo").alias("month")
    )

    portfolio_dict = {}

    for tenor in relevant_tenors:
        for quantile in relevant_quantiles:
            key = f"{tenor}_Q{quantile}"  # Example key: "5Y_Q3"
            
            # Filter dataframe for this specific tenor-quantile pair
            portfolio_df = rep_parspread_df.filter(
                (pl.col("tenor") == tenor) & (pl.col("credit_quantile") == quantile)
            )

            portfolio_df = portfolio_df.sort("date")
            
            # Store in dictionary
            portfolio_dict[key] = portfolio_df
    return portfolio_dict

def calc_cds_return_for_portfolios(portfolio_dict = None, raw_rates = None, start_date = START_DATE, end_date = END_DATE):
    """
    Calculates CDS returns for each portfolio in the portfolio_dict using the He-Kelly formula.

    Parameters:
    - portfolio_dict (dict): Dictionary where keys are tenor-quantile pairs and values are Polars DataFrames.
    - raw_rates (pd.DataFrame): Raw interest rate data.
    - start_date (str or datetime): Start date for filtering.
    - end_date (str or datetime): End date for filtering.

    Returns:
    - dict: Dictionary where keys are tenor-quantile pairs and values are Polars DataFrames of CDS returns.
    """
    # Step 1: Compute discount rates
    quarterly_discount_pd = calc_discount(raw_rates, start_date, end_date)  # Output is Pandas
    quarterly_discount_pd = quarterly_discount_pd.iloc[:-1]  # Remove last row

    # Convert Pandas quarterly discount to Polars for compatibility
    quarterly_discount = pl.from_pandas(quarterly_discount_pd.reset_index())

    # Storage for results
    cds_return_dict = {}

    fiveY_lambda_dict = {}

    #Obtain the lambdas to use; Lambda is calculating using the cds spreads of the 5 year tenor
    for key, portfolio_df in portfolio_dict.items():
        if key.startswith("5Y_Q"):
            # Ensure pivot_table is structured correctly in Polars
            pivot_table = portfolio_df.pivot(index="date", on="tenor", values="rep_parspread")


            # Check if the 5Y tenor exists
            if "5Y" in pivot_table.columns:
                # Extract the entire 5Y tenor spread as a DataFrame
                spread_5Y_df = pivot_table.select(pl.col("5Y"))

                # Compute lambda using the He-Kelly formula
                loss_given_default = 0.6
                lambda_df = 4 * np.log(1 + (spread_5Y_df / (4 * loss_given_default)))

                # Store the entire lambda DataFrame for the quintile
                fiveY_lambda_dict[key] = lambda_df

    # Iterate over each portfolio in portfolio_dict
    for key, portfolio_df in portfolio_dict.items():

        # Ensure pivot_table is structured correctly in Polars
        pivot_table = portfolio_df.pivot(index="date", on="tenor", values="rep_parspread")

        pivot_table = pivot_table.rename({col: f"{key}" for col in pivot_table.columns if col != "date"})
        # Compute lambda using He-Kelly formula, set the loss given default as constant 0.6
        loss_given_default = 0.6
        quintile_number = key.split("_Q")[-1]
        vol_target_key = f"5Y_Q{quintile_number}"
        lambda_constant = fiveY_lambda_dict.get(vol_target_key, None)
        # Define quarters
        quarters = np.arange(0.25, 20.25, 0.25)

        # Step 3: Compute risky duration
        risky_duration = pivot_table.select("date").clone()  # Initialize with date column

        lambda_vals = lambda_constant.flatten()

# Ensure lambda_vals matches pivot_table length
        if len(lambda_vals) > len(pivot_table):
            lambda_vals = lambda_vals[:len(pivot_table)]
        elif len(lambda_vals) < len(pivot_table):
            raise ValueError("lambda_constant has fewer rows than pivot_table. Cannot continue.")

        # Now use lambda_vals instead of lambda_constant.flatten()
        survival_probs = pl.DataFrame({"date": pivot_table["date"]}).with_columns([
    pl.Series(name=str(q), values=np.exp(-q * lambda_vals)) for q in quarters
])


        # Convert Pandas-based discount factors into Polars before filtering
        discount_filtered = quarterly_discount.select(["Date"] + [
            str(q) for q in quarters if str(q) in quarterly_discount.columns
        ])

        # Align dates between quarterly discount and survival probabilities
        survival_probs_filtered = survival_probs.filter(
            pl.col("date").is_in(quarterly_discount["Date"])
        )

        discount_filtered = discount_filtered.rename({"Date": "date"})
        
        # set intersection of dates
        dates_df = discount_filtered.select("date")
        dates_spf = survival_probs_filtered.select("date")
        dates_df = dates_df.join(dates_spf, on="date", how="inner")
        discount_filtered = discount_filtered.filter(
            pl.col("date").is_in(dates_df["date"])
        )
        survival_probs_filtered = survival_probs_filtered.filter(
            pl.col("date").is_in(dates_df["date"])
        )

        # Compute risky duration
        date_column = survival_probs_filtered.select("date")

        # Drop "Date" only from numerical columns for multiplication
        temp_df = discount_filtered.drop("date") * survival_probs_filtered.drop("date")

        # Reattach the "Date" column after multiplication
        temp_df = temp_df.with_columns(date_column)
        


        # Ensure "Date" is present in both DataFrames
        risky_duration = risky_duration.join(temp_df, on="date", how="left")

        # Backfill missing values in temp_df for dates in risky_duration
        risky_duration = risky_duration.fill_null(strategy="backward")
        risky_duration = risky_duration.fill_null(strategy="forward")

        # Compute risky duration and assign to the column
        risky_duration = risky_duration.with_columns(
            (0.25 * risky_duration.select(pl.exclude("date")).sum_horizontal())
        )

        risky_duration_shifted = risky_duration.select(pl.all().exclude("date")).shift(1)
        cds_spread_shifted = pivot_table.select(pl.all().exclude("date")).shift(1)

        # Compute the daily spread change manually using shift
        cds_spread_change = pivot_table.select(pl.all().exclude("date")) - pivot_table.select(pl.all().exclude("date")).shift(1)

        # Compute the CDS return
        cds_return = (
            (cds_spread_shifted / 250) + (cds_spread_change * risky_duration_shifted.select("sum"))
        ).drop_nulls()

        # Select the "date" column and shift it to exclude the first row
        date_column = risky_duration.select("date").slice(1)

        # Add the modified "date" column back to cds_return
        cds_return = cds_return.with_columns(date_column)

        # Store results in dictionary
        cds_return_dict[key] = cds_return

    return cds_return_dict

def calculate_monthly_returns(daily_returns_dict = None):
    """
    Calculates monthly returns for each portfolio in the daily_returns_dict.

    Parameters:
    - daily_returns_dict (dict): Dictionary where keys are tenor-quantile pairs and values are Polars DataFrames.

    Returns:
    - dict: Dictionary where keys are tenor-quantile pairs and values are Polars DataFrames of monthly returns.
    """
    monthly_returns_dict = {}
    fiveY_vol_dict = {}
    for key, df in daily_returns_dict.items():
        # Check if the portfolio key corresponds to a 5Y quintile
        if key.startswith("5Y_Q"):
            # Ensure 'date' column is in datetime format and truncate to the first day of the month
            df = df.with_columns(pl.col("date").dt.truncate("1mo").alias("Month"))

            # Calculate monthly returns
            monthly_returns = (
                df.group_by("Month")
                .agg(
                    (pl.col(key) + 1).product() - 1  # Aggregate to compute monthly returns
                ).rename({f"{key}": f"{key} Monthly Return"})  # Rename column
            )

            # Calculate the volatility of monthly returns
            vol = monthly_returns.select(f"{key} Monthly Return").std().item()
            fiveY_vol_dict[key] = vol

    for key, df in daily_returns_dict.items():
        # Ensure 'date' column is in datetime format and truncate to the first day of the month
        df = df.with_columns(pl.col("date").dt.truncate("1mo").alias("Month"))

        # Compute monthly returns 
        monthly_returns = (
            df.group_by("Month")
            .agg(
                (pl.col(key) + 1).product() - 1  # Directly apply product aggregation
            ).rename({f"{key}": f"{key} Monthly Return"})  # Rename column
        )

        # Calculate monthly volatility of the portfolio
        portfolio_std = monthly_returns.select(f"{key} Monthly Return").std().item()

        # Identify the corresponding 5Y quintile for volatility scaling
        vol_target_key = "5Y_Q" + key.split("_Q")[-1]
        target_std = fiveY_vol_dict.get(vol_target_key, None)

        # Scale the monthly returns 
        if target_std is not None and portfolio_std > 0:
            scale_factor = target_std / portfolio_std
            
            # Scale the monthly returns
            monthly_returns = monthly_returns.with_columns(
                (pl.col(f"{key} Monthly Return") * scale_factor).alias(f"{key} Scaled Monthly Return")
            )

        # Store in the dictionary with the same key
        monthly_returns_dict[key] = monthly_returns
    frames = []
    for key, df in monthly_returns_dict.items():
        scaled_col_name = [col for col in df.columns if "Scaled" in col][0]
        small_df = df.select([
            pl.col("Month"),
            pl.col(scaled_col_name).alias(key)  # Rename the scaled column to the dictionary key
        ])
        frames.append(small_df)
    month_df = frames[0].select("Month")

    # Now extract the value columns (excluding Month)
    value_dfs = [df.select(key) for df, key in zip(frames, monthly_returns_dict.keys())]

    # Horizontally concatenate
    final_df = pl.concat([month_df] + value_dfs, how="horizontal")
    final_df = final_df.sort("Month")

    return final_df

def run_cds_calculation(raw_rates = None, cds_spreads = None, start_date = START_DATE, end_date = END_DATE):
    """
    Runs the entire CDS return calculation process.

    Parameters:
    - raw_rates (DataFrame): Raw interest rate data.
    - cds_spreads (DataFrame): CDS spread data.
    - start_date (str or datetime): Start date for filtering.
    - end_date (str or datetime): End date for filtering.

    Returns:
    - dict: Dictionary where keys are tenor-quantile pairs and values are Polars DataFrames of monthly returns.
    """
    rates_data = process_rates(raw_rates, start_date, end_date)
    portfolio_dict = get_portfolio_dict(start_date, end_date, cds_spreads)
    daily_returns_dict = calc_cds_return_for_portfolios(portfolio_dict, raw_rates, start_date, end_date)
    monthly_returns = calculate_monthly_returns(daily_returns_dict)
    return monthly_returns

if __name__ == "__main__":
    raw_rates = pull_fed_yield_curve.load_fed_yield_curve(data_dir=DATA_DIR )
    cds_spreads = pull_markit_cds.load_cds_data(data_dir=DATA_DIR )
    cds_returns = run_cds_calculation(raw_rates = raw_rates, cds_spreads = cds_spreads, start_date = START_DATE, end_date = END_DATE)
    cds_returns.write_parquet(DATA_DIR / "markit_cds_returns.parquet")
