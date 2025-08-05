"""
Calculate CDS returns following He, Kelly, and Manela (2017) methodology.

This module replicates monthly CDS portfolio returns as constructed in He, Kelly, and Manela (2017)
and Palhares (2013)'s paper "Cash-Flow Maturity and Risk Premia in CDS Markets."

The CDS return calculation uses the He-Kelly formula:

    CDS_Return_t = CDS_{t-1}/250 + ΔCDS_t * RD_{t-1}

Where:
- CDS_{t-1}/250: Carry return, daily accrual from previous day's spread (annualized over 250 days)
- ΔCDS_t: Daily change in spread
- RD_{t-1}: Risky duration, proxy for PV of future spread payments

Risky Duration is calculated as:

    RD_t = 1/4 * Σ_{j=1}^{4M} e^{-jλ/4} * e^{-jr_t^{(j/4)}/4}

Where:
- M: CDS maturity in years (e.g., 5)
- r_t^{(j/4)}: Quarterly risk-free rate
- λ: Default intensity, computed as: λ = 4 * log(1 + CDS/(4L))
- L: Loss given default (assumed constant at 0.6)

Portfolio Construction:
- Focus on US single-name 5Y CDS contracts
- Sort firms into 5 credit quality quintiles based on 5Y spreads each month
- Create 20 portfolios: 4 tenors (3Y, 5Y, 7Y, 10Y) * 5 credit quintiles
- Calculate returns for both individual contracts and portfolios

Data Filtering:
- USD-denominated CDS contracts only
- XR (no restructuring) contracts only
- Maximum spread of 50% (5000 bps)
- Standard tenors: 3Y, 5Y, 7Y, 10Y
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


import datetime
import time

import numpy as np
import pandas as pd
import polars as pl
import pull_fed_yield_curve
import pull_fred
import pull_markit_cds
from scipy.interpolate import CubicSpline

from settings import config

DATA_DIR = config("DATA_DIR")
START_DATE = pull_markit_cds.START_DATE
END_DATE = pull_markit_cds.END_DATE
# Uncomment for testing smaller timeframe
# START_DATE = pd.Timestamp("2015-01-01")
# END_DATE = pd.Timestamp("2020-01-01")

swap_rates = pull_fred.load_fred(data_dir=DATA_DIR)


def _format_elapsed_time(seconds):
    """Format elapsed time in a human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f} sec"
    elif seconds < 3600:
        return f"{seconds / 60:.1f} min"
    else:
        return f"{seconds / 3600:.1f} hours"


def process_rates(raw_rates=None, start_date=START_DATE, end_date=END_DATE):
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
    short_tenor_rates_renamed = short_tenor_rates.rename(
        columns={"DGS3MO": 0.25, "DGS6MO": 0.5}
    )
    raw_rates.columns = raw_rates.columns.str.extract(r"(\d+)$")[0].astype(
        int
    )  # Extract numeric part from column names
    rates = raw_rates[
        (raw_rates.index >= pd.to_datetime(start_date))
        & (raw_rates.index <= pd.to_datetime(end_date))
    ]  # / 100  # Convert percentages to decimal format

    merged_rates = pd.merge(
        rates, short_tenor_rates_renamed, left_index=True, right_index=True, how="inner"
    ).sort_index()
    cols = merged_rates.columns.tolist()
    ordered_cols = [0.25, 0.5] + [col for col in cols if col not in [0.25, 0.5]]
    merged_rates = merged_rates[ordered_cols]
    return merged_rates


def extrapolate_rates(rates=None):
    """
    Interpolates interest rates to quarterly intervals using cubic splines.

    Since CDS spreads are paid quarterly, we need quarterly risk-free rates
    for the risky duration calculation. This function takes annual rates
    (plus 3M and 6M) and interpolates to get rates at 0.25, 0.5, 0.75, 1.0,
    1.25, ... up to 30 years.

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


def calc_discount(raw_rates=None, start_date=START_DATE, end_date=END_DATE):
    """
    Calculates discount factors from interest rates for risky duration computation.

    Discount factors are computed as e^(-r*t/4) where r is the quarterly rate
    and t is the time in quarters. These factors are used to discount the
    expected CDS payments in the risky duration calculation.

    Parameters:
    - raw_rates (DataFrame): The raw interest rate data.
    - start_date (str or datetime): The start date for filtering.
    - end_date (str or datetime): The end date for filtering.

    Returns:
    - DataFrame: Discount factors for various maturities, with columns
                 representing quarters (0.25, 0.5, ..., 30).
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


def _get_filtered_cds_data_with_quantiles(
    start_date=START_DATE, end_date=END_DATE, cds_spreads=None
):
    """
    Common function to filter CDS data and assign credit quantiles.

    This function applies the standard filters for the He-Kelly-Manela methodology:
    - Only US CDS contracts
    - Parspreads <= 50% (5000 bps) to exclude distressed names
    - Assigns credit quality quintiles based on 5Y spreads each month

    Credit quintiles are computed monthly, with Q1 being the safest (lowest spread)
    and Q5 being the riskiest (highest spread). This allows tracking of credit
    migration and ensures balanced portfolios across the credit spectrum.

    Parameters:
    - start_date (str or datetime): Start date for filtering.
    - end_date (str or datetime): End date for filtering.
    - cds_spreads (pl.LazyFrame or pl.DataFrame): CDS spread data.

    Returns:
    - pl.LazyFrame: Filtered CDS data with credit quantile assignments.
    """
    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    if isinstance(cds_spreads, pd.DataFrame):
        cds_spreads = pl.from_pandas(cds_spreads)

    # Work with LazyFrame for memory efficiency
    if isinstance(cds_spreads, pl.DataFrame):
        cds_spreads = cds_spreads.lazy()

    # Build the query lazily - filter and clean data
    cds_spread_clean = (
        cds_spreads.filter(
            (pl.col("date") >= start_date)
            & (pl.col("date") <= end_date)
            & (pl.col("country") == "United States")
            & (pl.col("parspread").is_not_null())
            & (pl.col("parspread") <= 0.5)  # Remove spreads greater than 50%
        )
        .drop(["convspreard", "year", "redcode"])
        .unique()
        .with_columns(pl.col("date").dt.strftime("%Y-%m").alias("year_month"))
    )

    # Compute Credit Quantiles - need to collect here for quantile calculations
    spread_5y = cds_spread_clean.filter(pl.col("tenor") == "5Y")

    # Get first available spread for each ticker in each month
    first_spread_5y = (
        spread_5y.sort("date")
        .group_by(["ticker", "year_month"])
        .first()
        .select(["ticker", "year_month", "parspread"])
        .collect()  # Collect here as we need quantiles
    )

    # Compute separate credit quantiles per month
    credit_quantiles = first_spread_5y.group_by("year_month").agg(
        [
            pl.col("parspread").quantile(0.2).alias("q1"),
            pl.col("parspread").quantile(0.4).alias("q2"),
            pl.col("parspread").quantile(0.6).alias("q3"),
            pl.col("parspread").quantile(0.8).alias("q4"),
        ]
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

    # Continue with lazy operations - join back the quantiles
    cds_spreads_final = cds_spread_clean.join(
        first_spread_5y.lazy(), on=["ticker", "year_month"], how="left"
    ).sort("date")

    return cds_spreads_final


def get_contract_data(start_date=START_DATE, end_date=END_DATE, cds_spreads=None):
    """
    Gets individual CDS contract data with credit quantile assignments.

    Parameters:
    - start_date (str or datetime): Start date for filtering.
    - end_date (str or datetime): End date for filtering.
    - cds_spreads (pl.LazyFrame or pl.DataFrame): CDS spread data.

    Returns:
    - pl.DataFrame: DataFrame with individual contract data including credit quantiles.
    """
    # Get filtered data with quantiles
    cds_spreads_final = _get_filtered_cds_data_with_quantiles(
        start_date, end_date, cds_spreads
    )

    # Filter to relevant tenors and collect
    relevant_tenors = ["3Y", "5Y", "7Y", "10Y"]

    contract_data = cds_spreads_final.filter(
        (pl.col("tenor").is_in(relevant_tenors))
        & (pl.col("credit_quantile").is_not_null())
    ).collect()

    return contract_data


def get_portfolio_dict(start_date=START_DATE, end_date=END_DATE, cds_spreads=None):
    """
    Creates a dictionary of credit portfolios based on the CDS spread data.

    Parameters:
    - start_date (str or datetime): Start date for filtering.
    - end_date (str or datetime): End date for filtering.
    - cds_spreads (pl.LazyFrame or pl.DataFrame): CDS spread data.

    Returns:
    - dict: Dictionary where keys are tenor-quantile pairs and values are Polars DataFrames.
    """
    # Get filtered data with quantiles using the common function
    cds_spreads_final = _get_filtered_cds_data_with_quantiles(
        start_date, end_date, cds_spreads
    )

    # Compute Representative Parspread lazily
    relevant_tenors = ["3Y", "5Y", "7Y", "10Y"]
    relevant_quantiles = [1, 2, 3, 4, 5]

    rep_parspread_df = (
        cds_spreads_final.filter(
            (pl.col("tenor").is_in(relevant_tenors))
            & (pl.col("credit_quantile").is_in(relevant_quantiles))
        )
        .group_by(["date", "tenor", "credit_quantile"])
        .agg(pl.col("parspread").mean().alias("rep_parspread"))
        .with_columns(pl.col("date").dt.truncate("1mo").alias("month"))
    )

    portfolio_dict = {}

    # Collect individual portfolio data only when needed
    for tenor in relevant_tenors:
        for quantile in relevant_quantiles:
            key = f"{tenor}_Q{quantile}"  # Example key: "5Y_Q3"

            # Filter and collect only this specific portfolio
            portfolio_df = (
                rep_parspread_df.filter(
                    (pl.col("tenor") == tenor) & (pl.col("credit_quantile") == quantile)
                )
                .sort("date")
                .collect()  # Only collect the small subset we need
            )

            # Store in dictionary
            portfolio_dict[key] = portfolio_df
    return portfolio_dict


def _get_quarterly_discount_polars(
    raw_rates=None, start_date=START_DATE, end_date=END_DATE
):
    """
    Helper function to compute quarterly discount rates and convert to Polars format.

    Parameters:
    - raw_rates (pd.DataFrame): Raw interest rate data.
    - start_date (str or datetime): Start date for filtering.
    - end_date (str or datetime): End date for filtering.

    Returns:
    - pl.DataFrame: Quarterly discount rates in Polars format.
    """
    quarterly_discount_pd = calc_discount(
        raw_rates, start_date, end_date
    )  # Output is Pandas
    quarterly_discount_pd = quarterly_discount_pd.iloc[:-1]  # Remove last row

    # Convert Pandas quarterly discount to Polars for compatibility
    return pl.from_pandas(quarterly_discount_pd.reset_index())


def calc_cds_return_for_contracts(
    contract_data=None, raw_rates=None, start_date=START_DATE, end_date=END_DATE
):
    """
    Calculates CDS returns for individual contracts using the He-Kelly formula.

    The return calculation follows:
    CDS_Return_t = CDS_{t-1}/250 + ΔCDS_t × RD_{t-1}

    Where:
    - CDS_{t-1}/250: Daily carry from holding the protection (spread accrual)
    - ΔCDS_t: Change in CDS spread (mark-to-market component)
    - RD_{t-1}: Risky duration (sensitivity to spread changes)

    Lambda (default intensity) is calculated from 5Y spreads for each ticker,
    or averaged by credit quantile if 5Y data is unavailable.

    Parameters:
    - contract_data (pl.DataFrame): DataFrame with individual contract data.
    - raw_rates (pd.DataFrame): Raw interest rate data.
    - start_date (str or datetime): Start date for filtering.
    - end_date (str or datetime): End date for filtering.

    Returns:
    - pl.DataFrame: Daily returns with columns: ticker, tenor, date,
                    credit_quantile, daily_return.
    """
    # Step 1: Compute discount rates
    quarterly_discount = _get_quarterly_discount_polars(raw_rates, start_date, end_date)

    # Step 2: Calculate lambda for each contract based on 5Y spreads within same credit quantile
    # First, get 5Y spreads for lambda calculation
    fiveY_data = contract_data.filter(pl.col("tenor") == "5Y")

    # Calculate lambda for each ticker-date combination
    loss_given_default = 0.6
    fiveY_lambdas = fiveY_data.with_columns(
        (4 * np.log(1 + (pl.col("parspread") / (4 * loss_given_default)))).alias(
            "lambda"
        )
    ).select(["ticker", "date", "credit_quantile", "lambda"])

    # Join lambda values back to all contracts (using ticker and date)
    contract_data_with_lambda = contract_data.join(
        fiveY_lambdas, on=["ticker", "date", "credit_quantile"], how="left"
    )

    # For contracts without 5Y data, use average lambda from same quantile
    avg_lambda_by_quantile = fiveY_lambdas.group_by(["date", "credit_quantile"]).agg(
        pl.col("lambda").mean().alias("avg_lambda")
    )

    contract_data_with_lambda = contract_data_with_lambda.join(
        avg_lambda_by_quantile, on=["date", "credit_quantile"], how="left"
    ).with_columns(
        pl.coalesce([pl.col("lambda"), pl.col("avg_lambda")]).alias("lambda_final")
    )

    # Step 3: Calculate risky duration and returns for each contract
    # Sort by ticker, tenor, and date to ensure proper shift operations
    contract_data_sorted = contract_data_with_lambda.sort(["ticker", "tenor", "date"])

    # Calculate risky duration
    quarters = np.arange(0.25, 20.25, 0.25)

    # Initialize result list
    all_contract_returns = []

    # Process each unique ticker-tenor combination
    unique_contracts = contract_data_sorted.select(["ticker", "tenor"]).unique()
    total_contracts = len(unique_contracts)

    print(f"\nProcessing {total_contracts} individual CDS contracts...")
    start_time = time.time()

    for idx, row in enumerate(unique_contracts.iter_rows()):
        ticker, tenor = row

        # Progress update every 100 contracts or at milestones
        if idx % 100 == 0 or idx in [
            total_contracts // 4,
            total_contracts // 2,
            3 * total_contracts // 4,
        ]:
            elapsed = time.time() - start_time
            progress_pct = (idx / total_contracts) * 100

            # Estimate time remaining
            if idx > 0:
                rate = idx / elapsed
                remaining = (total_contracts - idx) / rate
                print(
                    f"  Progress: {idx}/{total_contracts} contracts ({progress_pct:.1f}%), "
                    f"Elapsed: {_format_elapsed_time(elapsed)}, "
                    f"Est. remaining: {_format_elapsed_time(remaining)}"
                )

        # Get data for this specific contract
        contract = contract_data_sorted.filter(
            (pl.col("ticker") == ticker) & (pl.col("tenor") == tenor)
        ).sort("date")

        if len(contract) < 2:
            continue  # Need at least 2 dates to calculate returns

        # Extract dates and lambda values
        dates = contract["date"].to_numpy()
        lambda_vals = contract["lambda_final"].to_numpy()
        parspreads = contract["parspread"].to_numpy()

        # Calculate survival probabilities for each date
        survival_probs_list = []
        for lambda_val in lambda_vals:
            survival_probs = np.exp(-quarters * lambda_val)
            survival_probs_list.append(survival_probs)

        # Get discount factors for matching dates
        discount_dates = quarterly_discount["index"].to_numpy()

        # Calculate risky duration for each date
        risky_durations = []
        for i, date in enumerate(dates):
            if date in discount_dates:
                date_idx = np.where(discount_dates == date)[0][0]
                discount_row = quarterly_discount.row(date_idx)[1:]  # Skip date column

                # Calculate risky duration
                rd = 0.25 * sum(
                    survival_probs_list[i][j] * discount_row[j]
                    for j in range(min(len(quarters), len(discount_row)))
                )
                risky_durations.append(rd)
            else:
                risky_durations.append(np.nan)

        # Calculate daily returns
        daily_returns = []
        for i in range(1, len(parspreads)):
            if not np.isnan(risky_durations[i - 1]):
                carry = parspreads[i - 1] / 250
                spread_change = parspreads[i] - parspreads[i - 1]
                daily_return = carry + (spread_change * risky_durations[i - 1])
                daily_returns.append(daily_return)
            else:
                daily_returns.append(np.nan)

        # Create result dataframe for this contract
        if daily_returns:
            result_df = pl.DataFrame(
                {
                    "ticker": [ticker] * len(daily_returns),
                    "tenor": [tenor] * len(daily_returns),
                    "date": dates[1:],  # Skip first date
                    "credit_quantile": contract["credit_quantile"][1:],
                    "daily_return": daily_returns,
                }
            )
            all_contract_returns.append(result_df)

    # Combine all contract returns
    if all_contract_returns:
        final_returns = pl.concat(all_contract_returns).sort(
            ["ticker", "tenor", "date"]
        )
        total_elapsed = time.time() - start_time
        print(
            f"  Completed: {total_contracts}/{total_contracts} contracts (100.0%), "
            f"Total time: {_format_elapsed_time(total_elapsed)}"
        )
        return final_returns
    else:
        # Return empty DataFrame with correct schema
        return pl.DataFrame(
            {
                "ticker": pl.Series([], dtype=pl.Utf8),
                "tenor": pl.Series([], dtype=pl.Utf8),
                "date": pl.Series([], dtype=pl.Date),
                "credit_quantile": pl.Series([], dtype=pl.Int64),
                "daily_return": pl.Series([], dtype=pl.Float64),
            }
        )


def calc_cds_return_for_portfolios(
    portfolio_dict=None, raw_rates=None, start_date=START_DATE, end_date=END_DATE
):
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
    quarterly_discount = _get_quarterly_discount_polars(raw_rates, start_date, end_date)

    # Storage for results
    cds_return_dict = {}

    fiveY_lambda_dict = {}

    # Obtain the lambdas to use; Lambda is calculating using the cds spreads of the 5 year tenor
    for key, portfolio_df in portfolio_dict.items():
        if key.startswith("5Y_Q"):
            # Ensure pivot_table is structured correctly in Polars
            pivot_table = portfolio_df.pivot(
                index="date", on="tenor", values="rep_parspread"
            )

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
    total_portfolios = len(portfolio_dict)
    print(f"\nProcessing {total_portfolios} CDS portfolios...")
    portfolio_start_time = time.time()

    for portfolio_idx, (key, portfolio_df) in enumerate(portfolio_dict.items()):
        # Progress update
        if portfolio_idx % 5 == 0 or portfolio_idx == total_portfolios - 1:
            elapsed = time.time() - portfolio_start_time
            progress_pct = ((portfolio_idx + 1) / total_portfolios) * 100
            print(
                f"  Portfolio {portfolio_idx + 1}/{total_portfolios}: {key} ({progress_pct:.0f}%), "
                f"Elapsed: {_format_elapsed_time(elapsed)}"
            )
        # Ensure pivot_table is structured correctly in Polars
        pivot_table = portfolio_df.pivot(
            index="date", on="tenor", values="rep_parspread"
        )

        pivot_table = pivot_table.rename(
            {col: f"{key}" for col in pivot_table.columns if col != "date"}
        )
        # Compute lambda using He-Kelly formula, set the loss given default as constant 0.6
        loss_given_default = 0.6
        quintile_number = key.split("_Q")[-1]
        vol_target_key = f"5Y_Q{quintile_number}"
        lambda_constant = fiveY_lambda_dict.get(vol_target_key, None)
        # Define quarters
        quarters = np.arange(0.25, 20.25, 0.25)

        # Step 3: Compute risky duration
        risky_duration = pivot_table.select(
            "date"
        ).clone()  # Initialize with date column

        lambda_vals = lambda_constant.flatten()

        # Ensure lambda_vals matches pivot_table length
        if len(lambda_vals) > len(pivot_table):
            lambda_vals = lambda_vals[: len(pivot_table)]
        elif len(lambda_vals) < len(pivot_table):
            raise ValueError(
                "lambda_constant has fewer rows than pivot_table. Cannot continue."
            )

        # Now use lambda_vals instead of lambda_constant.flatten()
        survival_probs = pl.DataFrame({"date": pivot_table["date"]}).with_columns(
            [pl.Series(name=str(q), values=np.exp(-q * lambda_vals)) for q in quarters]
        )

        # Convert Pandas-based discount factors into Polars before filtering
        discount_filtered = quarterly_discount.select(
            ["index"]
            + [str(q) for q in quarters if str(q) in quarterly_discount.columns]
        )

        # Align dates between quarterly discount and survival probabilities
        survival_probs_filtered = survival_probs.filter(
            pl.col("date").is_in(quarterly_discount["index"].to_list())
        )

        discount_filtered = discount_filtered.rename({"index": "date"})

        # set intersection of dates
        dates_df = discount_filtered.select("date")
        dates_spf = survival_probs_filtered.select("date")
        dates_df = dates_df.join(dates_spf, on="date", how="inner")
        discount_filtered = discount_filtered.filter(
            pl.col("date").is_in(dates_df["date"].to_list())
        )
        survival_probs_filtered = survival_probs_filtered.filter(
            pl.col("date").is_in(dates_df["date"].to_list())
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

        risky_duration_shifted = risky_duration.select(pl.all().exclude("date")).shift(
            1
        )
        cds_spread_shifted = pivot_table.select(pl.all().exclude("date")).shift(1)

        # Compute the daily spread change manually using shift
        cds_spread_change = pivot_table.select(
            pl.all().exclude("date")
        ) - pivot_table.select(pl.all().exclude("date")).shift(1)

        # Compute the CDS return
        cds_return = (
            (cds_spread_shifted / 250)
            + (cds_spread_change * risky_duration_shifted.select("sum"))
        ).drop_nulls()

        # Select the "date" column and shift it to exclude the first row
        date_column = risky_duration.select("date").slice(1)

        # Add the modified "date" column back to cds_return
        cds_return = cds_return.with_columns(date_column)

        # Store results in dictionary
        cds_return_dict[key] = cds_return

    total_elapsed = time.time() - portfolio_start_time
    print(
        f"  Completed all {total_portfolios} portfolios in {_format_elapsed_time(total_elapsed)}"
    )
    return cds_return_dict


def calculate_monthly_contract_returns(daily_contract_returns=None):
    """
    Calculates monthly returns for individual CDS contracts.

    Parameters:
    - daily_contract_returns (pl.DataFrame): DataFrame with daily contract returns.

    Returns:
    - pl.DataFrame: DataFrame with monthly contract returns.
    """
    if daily_contract_returns is None or daily_contract_returns.is_empty():
        return pl.DataFrame(
            {
                "ticker": pl.Series([], dtype=pl.Utf8),
                "tenor": pl.Series([], dtype=pl.Utf8),
                "Month": pl.Series([], dtype=pl.Date),
                "credit_quantile": pl.Series([], dtype=pl.Int64),
                "monthly_return": pl.Series([], dtype=pl.Float64),
            }
        )

    # Add month column
    daily_with_month = daily_contract_returns.with_columns(
        pl.col("date").dt.truncate("1mo").alias("Month")
    )

    # Calculate monthly returns for each contract
    monthly_returns = (
        daily_with_month.group_by(["ticker", "tenor", "Month", "credit_quantile"])
        .agg(((pl.col("daily_return") + 1).product() - 1).alias("monthly_return"))
        .sort(["ticker", "tenor", "Month"])
    )

    return monthly_returns


def calculate_monthly_returns(daily_returns_dict=None):
    """
    Calculates monthly returns for portfolios with volatility scaling.

    This function:
    1. Compounds daily returns to monthly frequency
    2. Calculates volatility for each 5Y portfolio (used as benchmark)
    3. Scales returns of all portfolios to match their corresponding 5Y volatility

    The volatility scaling ensures that portfolios with the same credit quality
    but different tenors have comparable risk levels, making it easier to
    analyze the term structure of CDS returns.

    Parameters:
    - daily_returns_dict (dict): Dictionary where keys are tenor-quantile pairs
                                 (e.g., "3Y_Q1") and values are Polars DataFrames.

    Returns:
    - pl.DataFrame: Combined DataFrame with scaled monthly returns for all portfolios.
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
                    (pl.col(key) + 1).product()
                    - 1  # Aggregate to compute monthly returns
                )
                .rename({f"{key}": f"{key} Monthly Return"})  # Rename column
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
            )
            .rename({f"{key}": f"{key} Monthly Return"})  # Rename column
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
                (pl.col(f"{key} Monthly Return") * scale_factor).alias(
                    f"{key} Scaled Monthly Return"
                )
            )

        # Store in the dictionary with the same key
        monthly_returns_dict[key] = monthly_returns
    frames = []
    for key, df in monthly_returns_dict.items():
        scaled_col_name = [col for col in df.columns if "Scaled" in col][0]
        small_df = df.select(
            [
                pl.col("Month"),
                pl.col(scaled_col_name).alias(
                    key
                ),  # Rename the scaled column to the dictionary key
            ]
        )
        frames.append(small_df)
    month_df = frames[0].select("Month")

    # Now extract the value columns (excluding Month)
    value_dfs = [df.select(key) for df, key in zip(frames, monthly_returns_dict.keys())]

    # Horizontally concatenate
    final_df = pl.concat([month_df] + value_dfs, how="horizontal")
    final_df = final_df.sort("Month")

    return final_df


def run_cds_calculation(
    raw_rates=None, cds_spreads=None, start_date=START_DATE, end_date=END_DATE
):
    """
    Main entry point for CDS return calculation following He-Kelly-Manela methodology.

    This function orchestrates the entire calculation process:
    1. Filters CDS data to US contracts with spreads <= 50%
    2. Assigns credit quality quintiles based on 5Y spreads
    3. Calculates daily returns using risky duration adjustment
    4. Aggregates to monthly frequency with volatility scaling

    The output includes both:
    - Contract-level returns: Individual CDS contracts (ticker-tenor pairs)
    - Portfolio-level returns: 20 portfolios (4 tenors × 5 credit quintiles)

    Parameters:
    - raw_rates (DataFrame): Fed yield curve data for discount factors.
    - cds_spreads (pl.LazyFrame or DataFrame): Raw CDS spread data from Markit.
    - start_date (str or datetime): Start date for filtering.
    - end_date (str or datetime): End date for filtering.

    Returns:
    - tuple: (contract_monthly_returns, portfolio_monthly_returns)
             Both are DataFrames with monthly return data.
    """
    print("\n" + "=" * 60)
    print("Starting CDS return calculation")
    print(f"Date range: {start_date} to {end_date}")
    print("=" * 60)

    overall_start = time.time()

    # Get contract-level data
    print("\n1. Loading and filtering CDS data...")
    step_start = time.time()
    contract_data = get_contract_data(start_date, end_date, cds_spreads)
    print(f"   Loaded {len(contract_data):,} contract-date observations")
    print(f"   Time: {_format_elapsed_time(time.time() - step_start)}")

    # Calculate contract-level returns
    print("\n2. Calculating daily contract-level returns...")
    step_start = time.time()
    daily_contract_returns = calc_cds_return_for_contracts(
        contract_data, raw_rates, start_date, end_date
    )
    print(f"   Generated {len(daily_contract_returns):,} daily returns")
    print(f"   Time: {_format_elapsed_time(time.time() - step_start)}")

    print("\n3. Aggregating to monthly contract returns...")
    step_start = time.time()
    monthly_contract_returns = calculate_monthly_contract_returns(
        daily_contract_returns
    )
    print(f"   Generated {len(monthly_contract_returns):,} monthly contract returns")
    print(f"   Time: {_format_elapsed_time(time.time() - step_start)}")

    # Calculate portfolio-level returns
    print("\n4. Creating portfolio structure...")
    step_start = time.time()
    portfolio_dict = get_portfolio_dict(start_date, end_date, cds_spreads)
    print(f"   Created {len(portfolio_dict)} portfolios")
    print(f"   Time: {_format_elapsed_time(time.time() - step_start)}")

    print("\n5. Calculating daily portfolio returns...")
    step_start = time.time()
    daily_returns_dict = calc_cds_return_for_portfolios(
        portfolio_dict, raw_rates, start_date, end_date
    )
    print(f"   Time: {_format_elapsed_time(time.time() - step_start)}")

    print("\n6. Aggregating and scaling monthly portfolio returns...")
    step_start = time.time()
    monthly_portfolio_returns = calculate_monthly_returns(daily_returns_dict)
    print(
        f"   Generated returns for {len(monthly_portfolio_returns.columns) - 1} portfolios"
    )
    print(f"   Time: {_format_elapsed_time(time.time() - step_start)}")

    total_elapsed = time.time() - overall_start
    print("\n" + "=" * 60)
    print(f"Total calculation time: {_format_elapsed_time(total_elapsed)}")
    print("=" * 60 + "\n")

    return monthly_contract_returns, monthly_portfolio_returns


def load_portfolio(data_dir=DATA_DIR):
    """
    Load portfolio-level CDS returns.
    Must first run this module as main to pull and save data.
    """
    file_path = Path(data_dir) / "markit_cds_returns.parquet"
    df = pd.read_parquet(file_path)
    return df


def load_contract_returns(data_dir=DATA_DIR):
    """
    Load contract-level CDS returns.
    Must first run this module as main to pull and save data.
    """
    file_path = Path(data_dir) / "markit_cds_contract_returns.parquet"
    df = pd.read_parquet(file_path)
    return df


if __name__ == "__main__":
    # DATA_DIR already handles command line args via settings.py
    data_dir = DATA_DIR

    print("\nCDS Return Calculation Script")
    print(f"Data directory: {data_dir}")

    print("\nLoading interest rate data...")
    raw_rates = pull_fed_yield_curve.load_fed_yield_curve(data_dir=data_dir)

    print("Loading CDS spread data...")
    # Load CDS data as LazyFrame for memory efficiency
    cds_spreads = pl.scan_parquet(data_dir / "markit_cds.parquet")

    # Calculate both contract and portfolio returns
    contract_returns, portfolio_returns = run_cds_calculation(
        raw_rates=raw_rates,
        cds_spreads=cds_spreads,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    # Save both contract and portfolio returns
    print("\nSaving results...")
    save_start = time.time()
    contract_returns.write_parquet(data_dir / "markit_cds_contract_returns.parquet")
    print(
        f"  Saved contract returns: {data_dir / 'markit_cds_contract_returns.parquet'}"
    )

    portfolio_returns.write_parquet(data_dir / "markit_cds_returns.parquet")
    print(f"  Saved portfolio returns: {data_dir / 'markit_cds_returns.parquet'}")
    print(f"  Save time: {_format_elapsed_time(time.time() - save_start)}")

    print("\nCalculation complete!")
