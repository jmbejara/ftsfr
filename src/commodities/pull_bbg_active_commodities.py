"""
pull_bbg_commodities.py

Pull active composite commodity futures (generic 'A') from Bloomberg and save to disk.

This script fetches PX_LAST for a curated set of commodities using Bloomberg's
active composite tickers (root + 'A'). Active composites automatically follow
the most liquid contract through rolls, which makes them suitable for computing
price returns without manual roll handling.

Functions
---------
- pull_active_commodities_prices: returns a wide pandas DataFrame with PX_LAST
- load_active_commodities_prices: loads the saved parquet from disk

Output file
-----------
- commodity_futures_active.parquet
"""

from pathlib import Path
import warnings
import pandas as pd

from settings import config


DATA_DIR = config("DATA_DIR")


# Mapping of commodity display names to Bloomberg root tickers
COMMODITIES = {
    # Agriculture
    "Barley": "WA",
    "Butter": "BUT",
    "Canola": "RS",
    "Cocoa": "CC",
    "Coffee": "KC",
    "Corn": "C ",
    "Cotton": "CT",
    "Lumber": "LB",
    "Oats": "O ",
    "Orange juice": "JO",
    "Rough rice": "RR",
    "Soybean meal": "SM",
    "Soybeans": "S ",
    "Wheat": "W ",
    # Energy
    "Crude Oil": "CL",
    "Gasoline": "XB",
    "Heating Oil": "HO",
    "Natural gas": "NG",
    "Propane": "PN",
    "Unleaded gas": "HU",
    # Livestock
    "Broilers": "AH",
    "Feeder cattle": "FC",
    "Lean hogs": "LH",
    "Live cattle": "LC",
    # Metals
    "Aluminium": "AL",
    "Coal": "QL",
    "Copper": "HG",
    "Gold": "GC",
    "Palladium": "PA",
    "Platinum": "PL",
    "Silver": "SI",
}


def _build_active_ticker(symbol_root: str, security_type: str = "Comdty") -> str:
    """Compose a Bloomberg active composite futures ticker string.

    Example: _build_active_ticker("CL") -> "CLA Comdty"
             _build_active_ticker("C ") -> "C A Comdty" (roots with trailing space)
    """
    return f"{symbol_root}A {security_type}"


def pull_active_commodities_prices(
    start_date: str = "1970-01-01",
    end_date: str | None = None,
    commodities_map: dict[str, str] = COMMODITIES,
    field: str = "PX_LAST",
    coverage_threshold: float = 0.50,
) -> pd.DataFrame:
    """Pull active composite futures prices (generic 'A') for many commodities.

    Returns a wide DataFrame with one column per active ticker (e.g., "CLA Comdty_PX_LAST"),
    date index reset to a column named "index" for consistency with other loaders.
    """
    from xbbg import blp

    if end_date is None:
        end_date = pd.Timestamp.today().strftime("%Y-%m-%d")

    tickers = [_build_active_ticker(root) for root in commodities_map.values()]

    def _validate_coverage(
        df_wide: pd.DataFrame,
        threshold: float,
        start_date_str: str,
        end_date_str: str,
        fld: str,
    ) -> None:
        """Validate series coverage and emit warnings per series below threshold.

        - Raise ValueError only if a series is completely empty (0% non-null).
        - Otherwise, emit a warning for each series with non-null coverage < threshold.
        - Include ticker and requested date range in messages to aid debugging.
        """
        if df_wide is None or df_wide.empty:
            raise ValueError("No data returned from Bloomberg for requested tickers.")

        # Ensure expected date column exists and compute coverage on data columns only
        date_col = "index" if "index" in df_wide.columns else df_wide.columns[0]
        total_rows = len(df_wide)
        empty_series: list[str] = []

        for col in df_wide.columns:
            if col == date_col:
                continue
            series = df_wide[col]
            non_null_count = int(series.notna().sum())
            non_null_ratio = (
                float(non_null_count) / float(total_rows) if total_rows > 0 else 0.0
            )

            # Derive readable ticker name by stripping the field suffix if present
            suffix = f"_{fld}"
            ticker_name = col[: -len(suffix)] if col.endswith(suffix) else col

            if non_null_ratio == 0.0:
                empty_series.append(ticker_name)
            elif non_null_ratio < threshold:
                pct = f"{non_null_ratio:.1%}"
                warnings.warn(
                    (
                        f"Low data coverage for ticker '{ticker_name}' from {start_date_str} to {end_date_str}: "
                        f"{pct} non-null (<{threshold:.0%})."
                    ),
                    category=UserWarning,
                )

        if empty_series:
            empties = ", ".join(empty_series)
            raise ValueError(
                f"No data returned (0% non-null) for tickers [{empties}] from {start_date_str} to {end_date_str}."
            )

    try:
        df = blp.bdh(
            tickers=tickers, flds=[field], start_date=start_date, end_date=end_date
        )
    except Exception:
        df = None

    if df is None or df.empty:
        frames: list[pd.DataFrame] = []
        for tkr in tickers:
            try:
                sub = blp.bdh(
                    tickers=tkr, flds=[field], start_date=start_date, end_date=end_date
                )
            except Exception:
                continue
            if sub is None or sub.empty:
                continue
            if isinstance(sub.columns, pd.MultiIndex):
                sub.columns = [f"{c[0]}_{c[1]}" for c in sub.columns]
            else:
                only = sub.columns[0]
                sub = sub.rename(columns={only: f"{tkr}_{only}"})
            frames.append(sub)
        if not frames:
            raise ValueError(
                "No data returned from Bloomberg for any requested ticker (per-ticker fallback)."
            )
        wide = pd.concat(frames, axis=1).reset_index()
        _validate_coverage(wide, coverage_threshold, start_date, end_date, field)
        return wide

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [f"{c[0]}_{c[1]}" for c in df.columns]
    df = df.reset_index()
    _validate_coverage(df, coverage_threshold, start_date, end_date, field)
    return df


def load_active_commodities_prices(data_dir=DATA_DIR) -> pd.DataFrame:
    path = Path(data_dir) / "commodity_futures_active.parquet"
    return pd.read_parquet(path)


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = pull_active_commodities_prices()
    path = DATA_DIR / "commodity_futures_active.parquet"
    df.to_parquet(path)
