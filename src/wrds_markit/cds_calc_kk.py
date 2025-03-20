import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
import polars as pl

# Read the Parquet file
raw_rates = pd.read_parquet("../../fed_yield_curve.parquet")  
cds_spread = pl.read_parquet("../../markit_cds.parquet")  


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
    raw_rates.columns = raw_rates.columns.str.extract(r"(\d+)$")[0].astype(int)
    rates = (
        raw_rates[
            (raw_rates.index >= pd.to_datetime(start_date))
            & (raw_rates.index <= pd.to_datetime(end_date))
        ]
        / 100
    )

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
        interpolated_values = cs(
            quarterly_maturities
        )  # Interpolate for quarterly intervals
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

    quarterly_discount = pd.DataFrame(
        columns=quarterly_rates.columns, index=quarterly_rates.index
    )
    for col in quarterly_rates.columns:
        quarterly_discount[col] = quarterly_rates[col].apply(
            lambda x: np.exp(-(col * x) / 4)
        )

    return quarterly_discount




cds_spread_noNA = cds_spread.drop_nulls(subset=["parspread"])

cds_spread_noNA = cds_spread_noNA.drop(['convspreard', 'year', 'redcode'])


# Check for missing values
missing_values = cds_spread_noNA.select(pl.all().null_count())

print(missing_values)

# Check for duplicates
num_all_duplicates = cds_spread_noNA.shape[0] - cds_spread_noNA.unique().shape[0]
print(num_all_duplicates)

# See the duplicated rows

duplicated_rows = cds_spread_noNA.join(
    cds_spread_noNA.group_by(cds_spread_noNA.columns).agg(pl.count()).filter(pl.col("count") > 1).select(cds_spread_noNA.columns),
    on=cds_spread_noNA.columns,
    how="inner"
)

print(duplicated_rows)


# Drop duplicates

cds_spread_unique = cds_spread_noNA.unique()
print(len(cds_spread_unique))

print(cds_spread_unique)


# Convert date column to year-month format for bucketing
cds_spread_unique = cds_spread_unique.with_columns(
    pl.col("date").dt.strftime("%Y-%m").alias("year_month")
)

# Step 1: Filter for 5Y tenor
spread_5y = cds_spread_unique.filter(pl.col("tenor") == "5Y")

# Step 2: Get the first available spread for each ticker in each month
first_spread_5y = (
    spread_5y.sort("date")
    .group_by(["ticker", "year_month"])
    .first()
    .select(["ticker", "year_month", "parspread"])
)

# Step 3: Compute separate credit quantiles per month
credit_quantiles = (
    first_spread_5y.group_by("year_month").agg([
        pl.col("parspread").quantile(0.2).alias("q1"),
        pl.col("parspread").quantile(0.4).alias("q2"),
        pl.col("parspread").quantile(0.6).alias("q3"),
        pl.col("parspread").quantile(0.8).alias("q4")
    ])
)

# Step 4: Assign each ticker to a credit quantile based on first available 5Y spread
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

# Step 5: Assign the computed credit quantile to every tenor of the same ticker
cds_spreads_final = cds_spread_unique.join(
    first_spread_5y, on=["ticker", "year_month"], how="left"
)


# Print the resulting dataframe
print(cds_spreads_final)

cds_spreads_final = cds_spreads_final.sort("date")


# Sanity check Filter rows for ticker "WESTLB" and year_month "2003-04"
westlb_april_2003 = cds_spreads_final.filter(
    (pl.col("ticker") == "WESTLB") & (pl.col("year_month") == "2003-10")
)

print(westlb_april_2003)

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

portfolio_dict = {}

# Iterate over all combinations of tenor-quantile pairs
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

print(portfolio_dict["5Y_Q3"])

# Dictionary to store statistics for each portfolio
portfolio_stats = {}

# Iterate over all 20 portfolio DataFrames
for key, df in portfolio_dict.items():
    stats = df.select([
        pl.col("rep_parspread").mean().alias("mean_parspread"),
        pl.col("rep_parspread").min().alias("min_parspread"),
        pl.col("rep_parspread").max().alias("max_parspread"),
        (pl.col("rep_parspread").max() - pl.col("rep_parspread").min()).alias("range_parspread")
    ])
    
    # Store statistics in dictionary
    portfolio_stats[key] = stats

# Display statistics for one portfolio (example: "5Y_Q3")
print(portfolio_stats["5Y_Q3"])


import pandas as pd
import numpy as np
import polars as pl

def calc_cds_return_for_portfolios(portfolio_dict, raw_rates, start_date = "2003-01-01", end_date = "2023-01-01"):
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

    # Iterate over each portfolio in portfolio_dict
    for key, portfolio_df in portfolio_dict.items():
        print(f"Processing portfolio: {key}")

        # Ensure pivot_table is structured correctly in Polars
        pivot_table = (
            portfolio_df.pivot(index="date", columns="tenor", values="rep_parspread")
            .sort("date")  # Ensure proper time-series ordering
        )

        pivot_table = pivot_table.rename({col: f"{key}" for col in pivot_table.columns if col != "date"})


        # Compute lambda using He-Kelly formula
        loss_given_default = 0.6
        lambda_df = 4 * np.log(1 + (pivot_table.select(pl.exclude("date")) / (4 * loss_given_default)))
#         lambda_df = (
#     pivot_table.select(pl.exclude("date"))
#     .with_columns((4 * np.log(1 + (pl.all() / (4 * loss_given_default)))).alias("lambda"))
# )

        # Define quarters
        quarters = np.arange(0.25, 20.25, 0.25)

        # Step 3: Compute risky duration
        risky_duration = pivot_table.select("date").clone()  # Initialize with date column

        #for tenor_col in lambda_df.columns:
            # Compute survival probabilities
        survival_probs = pl.DataFrame(
            {"date": pivot_table["date"]}
        ).with_columns([
            pl.lit(np.exp(-q * lambda_df.flatten())).alias(str(q)) for q in quarters
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

        # Compute risky duration
        #temp_df = discount_filtered * survival_probs_filtered
        # Ensure "Date" column is removed before multiplying
        # Keep the "Date" column separately
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

            # Step 4: Compute CDS return
            # Shift the values by one row to get the previous day's data
            # Shift the values by one row (previous row values)
        risky_duration_shifted = risky_duration.select(pl.all().exclude("date")).shift(1)
        cds_spread_shifted = pivot_table.select(pl.all().exclude("date")).shift(1)

        # Compute the daily spread change manually using shift
        cds_spread_change = pivot_table.select(pl.all().exclude("date")) - pivot_table.select(pl.all().exclude("date")).shift(1)

        # Compute the CDS return
        cds_return = (
            (cds_spread_shifted / 250) + (cds_spread_change * risky_duration_shifted.select("sum"))
        ).drop_nulls()

        # Reattach the "date" column
        # Select the "date" column and shift it to exclude the first row
        date_column = risky_duration.select("date").slice(1)

        # Add the modified "date" column back to cds_return
        cds_return = cds_return.with_columns(date_column)


        # Store results in dictionary
        cds_return_dict[key] = cds_return

    return cds_return_dict


calc_cds_return_for_portfolios(portfolio_dict, raw_rates, "2003-01-01", "2003-12-31")

