# Data Sources and Data Sets

This document lists all data sources used in the codebase, the specific databases/tables accessed, and the subscriptions required to run the code successfully.

## Data Source Summary Table

| Data Source         | Database/Table(s)                        | Subscription/Access Required         |
|---------------------|------------------------------------------|--------------------------------------|
| He, Kelly, Manela   | (public URLs)                            | None (public)                        |
| Ken French Library  | (public URLs)                            | None (public)                        |
| NYU Call Report     | (public URLs)                            | None (public)                        |
| Fed Yield Curve     | (public URLs)                            | None (public)                        |
| Open Source Bond Asset Pricing | (public URLs)                 | None (public)                        |
| WRDS Compustat      | comp.funda                               | WRDS + Compustat North America       |
| WRDS Bond Returns   | wrdsapps_bondret.bondret                 | WRDS + Bond Returns                  |
| WRDS CRSP           | crsp.stksecurityinfohdr, crsp.msf_v2, crsp.ccmxpf_linktable | WRDS + CRSP (Stock, Link)           |
| WRDS CRSP Treasury  | crspm.tfz_dly, crspm.tfz_iss             | WRDS + CRSP US Treasury              |
| WRDS Markit CDS     | markit.CDS{year}, markit_red.redobllookup, markit.redent | WRDS + Markit CDS                   |
| WRDS Mergent FISD   | (via mapping to Markit RED codes)        | WRDS + Mergent FISD                  |

## Data Modules

Data modules are subfolders in the `src` directory that contain a set of scripts that generate 1 or more related datasets. These data sets are grouped together because they use the same data sources. The following lists the data modules, such as `cds_bond_basis`, along with the data sources used in each module.

 - `bond_returns`: Calculates returns for corporate bonds, sovereign bonds, and treasury bonds. Uses Open Source Bond Asset Pricing and WRDS Bond Returns.
 - `cds_bond_basis`: Uses Open Source Bond Asset Pricing and WRDS Markit CDS.
 - `fed_yield_curve`: Uses Fed Yield Curve data downloaded from the US Federal Reserve Board of Governors website.
 - `foreign_exchange`: Uses ...
 - `he_kelly_manela`: Uses "He, Kelly, Manela Test Portfolios and Factors" data downloaded from Asaf Manela's website.
 - `ken_french_data_library`: Pulls data from the Ken French Data Library, using the Pandas Data Reader Python package.
 - `nyu_call_report`: 
 - `wrds_bank_premium`: 
 - `wrds_crsp_compustat`: 
 - `wrds_markit`: 

**Misc**

- [x] CRSP Returns (with and without dividends)
- [ ] Compustat Panel Data
- [x] Fama-French Portfolio Returns
- [x] Treasury Yield Curve
- [x] Bank Call Report Data

**He, Kelly, Manela Test Portfolios**

We can just use the test portfolios as downloaded from their website, though it
would be nice to use data up until the present day.

- [x] Equity CLOSE
- [.] Treasury Securities
- [.] Corporate Bonds
- [.] Sovereign Bonds
- [.] Options
- [.] Foreign Exchange
- [.] Commodities CLOSE
- [.] CDS CLOSE

**He, Kelly, Manela Disaggregated Data**

- [.] Equity
- [.] Treasury Securities
- [.] Corporate Bonds
- [ ] Sovereign Bonds
- [.] Options
- [ ] Foreign Exchange
- [ ] Commodities
- [.] CDS

**Segmented Arbitrage, Arbitrage Spreads**

- [ ] CIP
- [.] Box Spread
- [.] Equity Spot-Futures
- [.] Treasury Spot-Futures
- [.] Treasury Swap
- [.] TIPS-Treasury
- [.] CDS-Bond Basis


## Notes

- WRDS is not a monolithic subscription. Each dataset listed above typically requires a separate subscription through the WRDS platform.
- Public data sources (Ken French Data Library, Fed Yield Curve) typically don't require paid subscriptions.
- Access credentials for WRDS are configured in environment variables. Please set the `.env` file following the `.env.example` file.
- Specify which subscriptions you have access to in the `config.toml` file.
