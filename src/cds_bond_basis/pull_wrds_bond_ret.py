"""
Pull WRDS Bond Returns project data (wrdsapps_bondret.bondret).

This is the corporate-bond panel used by Siriwardane, Sunderam, and Wallen
(2021) as their primary bond pricing source. We use it instead of the Open
Source Bond Asset Pricing (OSBAP) panel because the paper requires
ISIN-level merging into Markit RED codes and pulls Z-spread inputs
(coupon, accrued interest, next coupon date, day-count basis) that OSBAP
does not provide.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import wrds

from settings import config

DATA_DIR = Path(config("DATA_DIR")) / "cds_bond_basis"
WRDS_USERNAME = config("WRDS_USERNAME")

# Paper sample is 2010-2020; user wants the full available WRDS window.
START_DATE = pd.Timestamp(config("BOND_RET_START_DATE", default="2002-07-01"))
END_DATE = pd.Timestamp(config("END_DATE", default="2025-12-31"))
MIN_OUTSTANDING_THOUSANDS = 100


def _get_where_clauses(year, start_date, end_date):
    """Build per-year SQL filters mirroring the paper sample criteria."""
    year_start = pd.Timestamp(year=year, month=1, day=1)
    next_year_start = pd.Timestamp(year=year + 1, month=1, day=1)
    window_start = max(year_start, start_date)
    window_end = min(next_year_start, end_date + pd.Timedelta(days=1))

    return [
        f"date >= '{window_start.date()}' AND date < '{window_end.date()}'",
        "security_level = 'SEN'",
        "maturity BETWEEN (date + INTERVAL '1 year') AND (date + INTERVAL '10 years')",
        f"amount_outstanding > {MIN_OUTSTANDING_THOUSANDS}",
        "conv = 0",
        "price_eom >= 50",
        "isin IS NOT NULL AND TRIM(isin) <> ''",
    ]


def get_bondret_data_as_dict(
    wrds_username=WRDS_USERNAME,
    start_date=START_DATE,
    end_date=END_DATE,
):
    """Pull WRDS Bond Returns data year-by-year and return as {year: df}."""
    db = wrds.Connection(wrds_username=wrds_username)

    yearly_data = {}
    for year in range(start_date.year, end_date.year + 1):
        print(f"Pulling wrdsapps_bondret.bondret for {year}...", flush=True)
        where_clauses = _get_where_clauses(
            year, start_date=start_date, end_date=end_date
        )
        query = f"""
        SELECT
            date,
            issue_id,
            cusip,
            bond_sym_id,
            bsym,
            isin,
            company_symbol,
            bond_type,
            security_level,
            conv,
            offering_date,
            offering_amt,
            offering_price,
            principal_amt,
            maturity,
            treasury_maturity,
            coupon,
            day_count_basis,
            dated_date,
            first_interest_date,
            last_interest_date,
            ncoups,
            t_date,
            t_volume,
            t_dvolume,
            t_spread,
            t_yld_pt,
            yield,
            amount_outstanding,
            price_eom,
            price_ldm,
            price_l5m,
            gap,
            coupmonth,
            nextcoup,
            coupamt,
            coupacc,
            multicoups,
            ret_eom,
            ret_ldm,
            ret_l5m,
            tmt,
            remcoups,
            duration,
            r_sp,
            r_mr,
            r_fr,
            n_sp,
            n_mr,
            n_fr,
            rating_num,
            rating_cat,
            rating_class,
            defaulted,
            default_date,
            default_type,
            reinstated,
            reinstated_date
        FROM wrdsapps_bondret.bondret
        WHERE {' AND '.join(where_clauses)}
        """
        df = db.raw_sql(
            query,
            date_cols=[
                "date",
                "offering_date",
                "maturity",
                "dated_date",
                "first_interest_date",
                "last_interest_date",
                "t_date",
                "nextcoup",
                "default_date",
                "reinstated_date",
            ],
        )
        df["year"] = year
        yearly_data[year] = df
        print(f"Finished {year}: {len(df)} rows", flush=True)

    return yearly_data


def combine_bondret_data(bondret_data):
    """Concatenate year-keyed DataFrames."""
    if not bondret_data:
        return pd.DataFrame()
    return pd.concat(list(bondret_data.values()), ignore_index=True)


def pull_bondret_data(
    wrds_username=WRDS_USERNAME,
    start_date=START_DATE,
    end_date=END_DATE,
):
    """Pull and combine."""
    data_by_year = get_bondret_data_as_dict(
        wrds_username=wrds_username, start_date=start_date, end_date=end_date
    )
    return combine_bondret_data(data_by_year)


def load_bondret_filtered(data_dir=DATA_DIR):
    """Load cached filtered WRDS Bond Returns pull."""
    path = Path(data_dir) / "wrds_bondret_filtered.parquet"
    return pd.read_parquet(path)


def clean_bondret_for_cds_basis(df: pd.DataFrame) -> pd.DataFrame:
    """Project-ready bond panel for the CDS-bond basis pipeline."""
    cols_needed = [
        "date",
        "issue_id",
        "isin",
        "cusip",
        "principal_amt",
        "amount_outstanding",
        "maturity",
        "coupon",
        "day_count_basis",
        "dated_date",
        "first_interest_date",
        "last_interest_date",
        "ncoups",
        "nextcoup",
        "remcoups",
        "coupacc",
        "price_eom",
        "tmt",
        "t_volume",
        "t_dvolume",
        "rating_class",
    ]
    cols_present = [c for c in cols_needed if c in df.columns]
    cleaned = df[cols_present].copy()

    if "isin" in cleaned.columns:
        cleaned["isin"] = cleaned["isin"].astype(str).str.strip().str.upper()

    required_cols = [
        c
        for c in ["date", "isin", "maturity", "coupon", "principal_amt", "price_eom"]
        if c in cleaned.columns
    ]
    if required_cols:
        cleaned = cleaned.dropna(subset=required_cols)

    dedupe_keys = [c for c in ["date", "isin", "issue_id"] if c in cleaned.columns]
    if dedupe_keys:
        cleaned = cleaned.drop_duplicates(subset=dedupe_keys, keep="first")

    sort_cols = [c for c in ["date", "isin", "issue_id"] if c in cleaned.columns]
    if sort_cols:
        cleaned = cleaned.sort_values(sort_cols)

    return cleaned.reset_index(drop=True)


def load_bondret_project(data_dir=DATA_DIR):
    """Load cleaned project panel."""
    path = Path(data_dir) / "wrds_bondret_project.parquet"
    return pd.read_parquet(path)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df_full = pull_bondret_data(wrds_username=WRDS_USERNAME)
    out_full_path = DATA_DIR / "wrds_bondret_filtered.parquet"
    df_full.to_parquet(out_full_path)
    print(
        f"Saved full filtered pull: {len(df_full)} rows to {out_full_path}",
        flush=True,
    )

    df_project = clean_bondret_for_cds_basis(df_full)
    out_project_path = DATA_DIR / "wrds_bondret_project.parquet"
    df_project.to_parquet(out_project_path)
    print(
        f"Saved project-ready panel: {len(df_project)} rows to {out_project_path}",
        flush=True,
    )


if __name__ == "__main__":
    main()
