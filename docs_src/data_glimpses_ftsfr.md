# Data Glimpses Report: FTSFR only
Total FTSFR datasets: 58

This report provides enhanced analysis specifically for FTSFR (Financial Time Series Forecasting Repository) datasets, including:
- Detailed null value analysis for all columns
- Row uniqueness verification
- Standard dataset metadata and glimpses

## Summary of FTSFR Datasets by Task

### Format
#### Format: Basis Tips Treas
- [`ftsfr_tips_treasury_basis.parquet`](#ftsfr-tips-treasury-basis-parquet)
#### Format: Basis Treas Sf
- [`ftsfr_treasury_sf_basis.parquet`](#ftsfr-treasury-sf-basis-parquet)
#### Format: Basis Treas Swap
- [`ftsfr_treasury_swap_basis.parquet`](#ftsfr-treasury-swap-basis-parquet)
#### Format: Cds Bond Basis
- [`ftsfr_CDS_bond_basis_aggregated.parquet`](#ftsfr-cds-bond-basis-aggregated-parquet)
- [`ftsfr_CDS_bond_basis_non_aggregated.parquet`](#ftsfr-cds-bond-basis-non-aggregated-parquet)
#### Format: Cds Returns
- [`ftsfr_CDS_contract_returns.parquet`](#ftsfr-cds-contract-returns-parquet)
- [`ftsfr_CDS_portfolio_returns.parquet`](#ftsfr-cds-portfolio-returns-parquet)
#### Format: Cip
- [`ftsfr_CIP_spreads.parquet`](#ftsfr-cip-spreads-parquet)
#### Format: Commodities
- [`ftsfr_commodities_returns.parquet`](#ftsfr-commodities-returns-parquet)
#### Format: Corp Bond Returns
- [`ftsfr_corp_bond_portfolio_returns.parquet`](#ftsfr-corp-bond-portfolio-returns-parquet)
- [`ftsfr_corp_bond_returns.parquet`](#ftsfr-corp-bond-returns-parquet)
#### Format: Fed Yield Curve
- [`ftsfr_treas_yield_curve_zero_coupon.parquet`](#ftsfr-treas-yield-curve-zero-coupon-parquet)
#### Format: Foreign Exchange
- [`ftsfr_FX_returns.parquet`](#ftsfr-fx-returns-parquet)
#### Format: He Kelly Manela
- [`ftsfr_he_kelly_manela_all.parquet`](#ftsfr-he-kelly-manela-all-parquet)
- [`ftsfr_he_kelly_manela_factors_daily.parquet`](#ftsfr-he-kelly-manela-factors-daily-parquet)
- [`ftsfr_he_kelly_manela_factors_monthly.parquet`](#ftsfr-he-kelly-manela-factors-monthly-parquet)
#### Format: Ken French Data Library
- [`ftsfr_french_portfolios_25_daily_size_and_bm.parquet`](#ftsfr-french-portfolios-25-daily-size-and-bm-parquet)
- [`ftsfr_french_portfolios_25_daily_size_and_inv.parquet`](#ftsfr-french-portfolios-25-daily-size-and-inv-parquet)
- [`ftsfr_french_portfolios_25_daily_size_and_op.parquet`](#ftsfr-french-portfolios-25-daily-size-and-op-parquet)
#### Format: Nyu Call Report
- [`ftsfr_nyu_call_report_cash_liquidity.parquet`](#ftsfr-nyu-call-report-cash-liquidity-parquet)
- [`ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet`](#ftsfr-nyu-call-report-holding-company-cash-liquidity-parquet)
- [`ftsfr_nyu_call_report_holding_company_leverage.parquet`](#ftsfr-nyu-call-report-holding-company-leverage-parquet)
- [`ftsfr_nyu_call_report_leverage.parquet`](#ftsfr-nyu-call-report-leverage-parquet)
#### Format: Options
- [`ftsfr_cjs_option_returns.parquet`](#ftsfr-cjs-option-returns-parquet)
- [`ftsfr_hkm_option_returns.parquet`](#ftsfr-hkm-option-returns-parquet)
#### Format: Us Treasury Returns
- [`ftsfr_treas_bond_portfolio_returns.parquet`](#ftsfr-treas-bond-portfolio-returns-parquet)
- [`ftsfr_treas_bond_returns.parquet`](#ftsfr-treas-bond-returns-parquet)
#### Format: Wrds Crsp Compustat
- [`ftsfr_CRSP_monthly_stock_ret.parquet`](#ftsfr-crsp-monthly-stock-ret-parquet)
- [`ftsfr_CRSP_monthly_stock_retx.parquet`](#ftsfr-crsp-monthly-stock-retx-parquet)

### Organize Ftsfr Datasets
- [`ftsfr_tips_treasury_basis.parquet`](#ftsfr-tips-treasury-basis-parquet)
- [`ftsfr_treasury_sf_basis.parquet`](#ftsfr-treasury-sf-basis-parquet)
- [`ftsfr_treasury_swap_basis.parquet`](#ftsfr-treasury-swap-basis-parquet)
- [`ftsfr_CDS_bond_basis_aggregated.parquet`](#ftsfr-cds-bond-basis-aggregated-parquet)
- [`ftsfr_CDS_bond_basis_non_aggregated.parquet`](#ftsfr-cds-bond-basis-non-aggregated-parquet)
- [`ftsfr_CDS_contract_returns.parquet`](#ftsfr-cds-contract-returns-parquet)
- [`ftsfr_CDS_portfolio_returns.parquet`](#ftsfr-cds-portfolio-returns-parquet)
- [`ftsfr_CIP_spreads.parquet`](#ftsfr-cip-spreads-parquet)
- [`ftsfr_commodities_returns.parquet`](#ftsfr-commodities-returns-parquet)
- [`ftsfr_corp_bond_portfolio_returns.parquet`](#ftsfr-corp-bond-portfolio-returns-parquet)
- [`ftsfr_corp_bond_returns.parquet`](#ftsfr-corp-bond-returns-parquet)
- [`ftsfr_treas_yield_curve_zero_coupon.parquet`](#ftsfr-treas-yield-curve-zero-coupon-parquet)
- [`ftsfr_FX_returns.parquet`](#ftsfr-fx-returns-parquet)
- [`ftsfr_he_kelly_manela_all.parquet`](#ftsfr-he-kelly-manela-all-parquet)
- [`ftsfr_he_kelly_manela_factors_daily.parquet`](#ftsfr-he-kelly-manela-factors-daily-parquet)
- [`ftsfr_he_kelly_manela_factors_monthly.parquet`](#ftsfr-he-kelly-manela-factors-monthly-parquet)
- [`ftsfr_french_portfolios_25_daily_size_and_bm.parquet`](#ftsfr-french-portfolios-25-daily-size-and-bm-parquet)
- [`ftsfr_french_portfolios_25_daily_size_and_inv.parquet`](#ftsfr-french-portfolios-25-daily-size-and-inv-parquet)
- [`ftsfr_french_portfolios_25_daily_size_and_op.parquet`](#ftsfr-french-portfolios-25-daily-size-and-op-parquet)
- [`ftsfr_nyu_call_report_cash_liquidity.parquet`](#ftsfr-nyu-call-report-cash-liquidity-parquet)
- [`ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet`](#ftsfr-nyu-call-report-holding-company-cash-liquidity-parquet)
- [`ftsfr_nyu_call_report_holding_company_leverage.parquet`](#ftsfr-nyu-call-report-holding-company-leverage-parquet)
- [`ftsfr_nyu_call_report_leverage.parquet`](#ftsfr-nyu-call-report-leverage-parquet)
- [`ftsfr_cjs_option_returns.parquet`](#ftsfr-cjs-option-returns-parquet)
- [`ftsfr_hkm_option_returns.parquet`](#ftsfr-hkm-option-returns-parquet)
- [`ftsfr_treas_bond_portfolio_returns.parquet`](#ftsfr-treas-bond-portfolio-returns-parquet)
- [`ftsfr_treas_bond_returns.parquet`](#ftsfr-treas-bond-returns-parquet)
- [`ftsfr_CRSP_monthly_stock_ret.parquet`](#ftsfr-crsp-monthly-stock-ret-parquet)
- [`ftsfr_CRSP_monthly_stock_retx.parquet`](#ftsfr-crsp-monthly-stock-retx-parquet)

---

## ftsfr_tips_treasury_basis.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/basis_tips_treas/ftsfr_tips_treasury_basis.parquet`
**Size:** 206374 bytes | **Type:** Parquet | **Shape:** 20,647 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='us', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-28.952341619528084, max=243.18891701256675, mean=24.87, median=23.50302543169036
```

### Date/Datetime Column Statistics
```
ds: min=2004-07-21 00:00:00, max=2025-05-30 00:00:00
```

---

## ftsfr_treasury_sf_basis.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/basis_treas_sf/ftsfr_treasury_sf_basis.parquet`
**Size:** 175432 bytes | **Type:** Parquet | **Shape:** 24,537 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='us', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-420.7967777777778, max=288.82433333333336, mean=-23.23, median=-10.56133333333333
```

### Date/Datetime Column Statistics
```
ds: min=2004-06-23 00:00:00, max=2025-01-08 00:00:00
```

---

## ftsfr_treasury_swap_basis.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/basis_treas_swap/ftsfr_treasury_swap_basis.parquet`
**Size:** 169214 bytes | **Type:** Parquet | **Shape:** 32,022 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='us', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-105.0, max=87.79999999999997, mean=-12.67, median=-10.899999999999999
```

### Date/Datetime Column Statistics
```
ds: min=2001-12-20 00:00:00, max=2025-08-11 00:00:00
```

---

## ftsfr_CDS_bond_basis_aggregated.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/ftsfr_CDS_bond_basis_aggregated.parquet`
**Size:** 7441 bytes | **Type:** Parquet | **Shape:** 346 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-5.751113076375435, max=9.081822277149262, mean=1.81, median=2.002582027998724
```

### Date/Datetime Column Statistics
```
ds: min=2002-09-30 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_CDS_bond_basis_non_aggregated.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/ftsfr_CDS_bond_basis_non_aggregated.parquet`
**Size:** 1007324 bytes | **Type:** Parquet | **Shape:** 91,742 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-99.98623956278941, max=99.84502978149779, mean=2.32, median=3.127317613581347
```

### Date/Datetime Column Statistics
```
ds: min=2002-09-30 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_CDS_contract_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_returns/ftsfr_CDS_contract_returns.parquet`
**Size:** 3.0 MB | **Type:** Parquet | **Shape:** 201,830 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-1.805303277625713, max=1.2258522666583378, mean=0.00, median=0.0016596077365234052
__index_level_0__: min=0, max=657848, mean=330612.87, median=331160.0
```

### Date/Datetime Column Statistics
```
ds: min=2001-01-01 00:00:00, max=2023-12-01 00:00:00
```

---

## ftsfr_CDS_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_returns/ftsfr_CDS_portfolio_returns.parquet`
**Size:** 93610 bytes | **Type:** Parquet | **Shape:** 5,510 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=5.3636447198150465e-05, max=0.019337155864089337, mean=0.00, median=0.0008424713798078191
__index_level_0__: min=0, max=5519, mean=2759.22, median=2759.5
```

### Date/Datetime Column Statistics
```
ds: min=2001-01-01 00:00:00, max=2023-12-01 00:00:00
```

---

## ftsfr_CIP_spreads.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cip/ftsfr_CIP_spreads.parquet`
**Size:** 535436 bytes | **Type:** Parquet | **Shape:** 43,490 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-75.02010739148606, max=439.59367390435733, mean=18.90, median=12.660612223492215
```

### Date/Datetime Column Statistics
```
ds: min=2001-12-04 00:00:00, max=2025-02-28 00:00:00
```

---

## ftsfr_commodities_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/commodities/ftsfr_commodities_returns.parquet`
**Size:** 126310 bytes | **Type:** Parquet | **Shape:** 11,553 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.6026668174158621, max=0.6741843598832211, mean=0.00, median=-5.1923181702440147e-05
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-30 00:00:00, max=2025-08-12 00:00:00
```

---

## ftsfr_corp_bond_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/corp_bond_returns/ftsfr_corp_bond_portfolio_returns.parquet`
**Size:** 28080 bytes | **Type:** Parquet | **Shape:** 2,420 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                Float64        
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
unique_id: min=1.0, max=10.0, mean=5.50, median=5.5
y: min=-0.2357410309055786, max=0.21497478314108745, mean=0.00, median=0.004769802911585877
```

### Date/Datetime Column Statistics
```
ds: min=2002-08-31 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_corp_bond_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/corp_bond_returns/ftsfr_corp_bond_returns.parquet`
**Size:** 8.8 MB | **Type:** Parquet | **Shape:** 1,046,059 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.9753107633155358, max=3.68351, mean=0.00, median=0.0033377041526085
```

### Date/Datetime Column Statistics
```
ds: min=2002-08-31 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_treas_yield_curve_zero_coupon.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/fed_yield_curve/ftsfr_treas_yield_curve_zero_coupon.parquet`
**Size:** 5.0 MB | **Type:** Parquet | **Shape:** 373,592 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=0.0554, max=16.462, mean=5.60, median=5.3053296461184996
__index_level_0__: min=0, max=502139, mean=226282.43, median=211512.5
```

### Date/Datetime Column Statistics
```
ds: min=1961-06-14 00:00:00, max=2025-08-08 00:00:00
```

---

## ftsfr_FX_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/foreign_exchange/ftsfr_FX_returns.parquet`
**Size:** 949613 bytes | **Type:** Parquet | **Shape:** 52,473 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-1.0326500049101444, max=8.548700375536482, mean=1.77, median=1.0010820813484795
__index_level_0__: min=726, max=61109, mean=30845.96, median=31254.0
```

### Date/Datetime Column Statistics
```
ds: min=1999-02-09 00:00:00, max=2025-02-28 00:00:00
```

---

## ftsfr_tips_treasury_basis.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/basis_tips_treas/ftsfr_tips_treasury_basis.parquet`
**Size:** 206374 bytes | **Type:** Parquet | **Shape:** 20,647 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='us', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-28.952341619528084, max=243.18891701256675, mean=24.87, median=23.50302543169036
```

### Date/Datetime Column Statistics
```
ds: min=2004-07-21 00:00:00, max=2025-05-30 00:00:00
```

---

## ftsfr_treasury_sf_basis.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/basis_treas_sf/ftsfr_treasury_sf_basis.parquet`
**Size:** 175432 bytes | **Type:** Parquet | **Shape:** 24,537 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='us', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-420.7967777777778, max=288.82433333333336, mean=-23.23, median=-10.56133333333333
```

### Date/Datetime Column Statistics
```
ds: min=2004-06-23 00:00:00, max=2025-01-08 00:00:00
```

---

## ftsfr_treasury_swap_basis.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/basis_treas_swap/ftsfr_treasury_swap_basis.parquet`
**Size:** 169214 bytes | **Type:** Parquet | **Shape:** 32,022 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='us', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-105.0, max=87.79999999999997, mean=-12.67, median=-10.899999999999999
```

### Date/Datetime Column Statistics
```
ds: min=2001-12-20 00:00:00, max=2025-08-11 00:00:00
```

---

## ftsfr_CDS_bond_basis_aggregated.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/cds_bond_basis/ftsfr_CDS_bond_basis_aggregated.parquet`
**Size:** 7441 bytes | **Type:** Parquet | **Shape:** 346 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-5.751113076375435, max=9.081822277149262, mean=1.81, median=2.002582027998724
```

### Date/Datetime Column Statistics
```
ds: min=2002-09-30 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_CDS_bond_basis_non_aggregated.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/cds_bond_basis/ftsfr_CDS_bond_basis_non_aggregated.parquet`
**Size:** 1007324 bytes | **Type:** Parquet | **Shape:** 91,742 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-99.98623956278941, max=99.84502978149779, mean=2.32, median=3.127317613581347
```

### Date/Datetime Column Statistics
```
ds: min=2002-09-30 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_CDS_contract_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/cds_returns/ftsfr_CDS_contract_returns.parquet`
**Size:** 3.0 MB | **Type:** Parquet | **Shape:** 201,830 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-1.805303277625713, max=1.2258522666583378, mean=0.00, median=0.0016596077365234052
__index_level_0__: min=0, max=657848, mean=330612.87, median=331160.0
```

### Date/Datetime Column Statistics
```
ds: min=2001-01-01 00:00:00, max=2023-12-01 00:00:00
```

---

## ftsfr_CDS_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/cds_returns/ftsfr_CDS_portfolio_returns.parquet`
**Size:** 93610 bytes | **Type:** Parquet | **Shape:** 5,510 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=5.3636447198150465e-05, max=0.019337155864089337, mean=0.00, median=0.0008424713798078191
__index_level_0__: min=0, max=5519, mean=2759.22, median=2759.5
```

### Date/Datetime Column Statistics
```
ds: min=2001-01-01 00:00:00, max=2023-12-01 00:00:00
```

---

## ftsfr_CIP_spreads.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/cip/ftsfr_CIP_spreads.parquet`
**Size:** 535436 bytes | **Type:** Parquet | **Shape:** 43,490 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-75.02010739148606, max=439.59367390435733, mean=18.90, median=12.660612223492215
```

### Date/Datetime Column Statistics
```
ds: min=2001-12-04 00:00:00, max=2025-02-28 00:00:00
```

---

## ftsfr_commodities_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/commodities/ftsfr_commodities_returns.parquet`
**Size:** 126310 bytes | **Type:** Parquet | **Shape:** 11,553 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.6026668174158621, max=0.6741843598832211, mean=0.00, median=-5.1923181702440147e-05
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-30 00:00:00, max=2025-08-12 00:00:00
```

---

## ftsfr_corp_bond_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/corp_bond_returns/ftsfr_corp_bond_portfolio_returns.parquet`
**Size:** 28080 bytes | **Type:** Parquet | **Shape:** 2,420 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                Float64        
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
unique_id: min=1.0, max=10.0, mean=5.50, median=5.5
y: min=-0.2357410309055786, max=0.21497478314108745, mean=0.00, median=0.004769802911585877
```

### Date/Datetime Column Statistics
```
ds: min=2002-08-31 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_corp_bond_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/corp_bond_returns/ftsfr_corp_bond_returns.parquet`
**Size:** 8.8 MB | **Type:** Parquet | **Shape:** 1,046,059 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.9753107633155358, max=3.68351, mean=0.00, median=0.0033377041526085
```

### Date/Datetime Column Statistics
```
ds: min=2002-08-31 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_treas_yield_curve_zero_coupon.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/fed_yield_curve/ftsfr_treas_yield_curve_zero_coupon.parquet`
**Size:** 5.0 MB | **Type:** Parquet | **Shape:** 373,592 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=0.0554, max=16.462, mean=5.60, median=5.3053296461184996
__index_level_0__: min=0, max=502139, mean=226282.43, median=211512.5
```

### Date/Datetime Column Statistics
```
ds: min=1961-06-14 00:00:00, max=2025-08-08 00:00:00
```

---

## ftsfr_FX_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/foreign_exchange/ftsfr_FX_returns.parquet`
**Size:** 949613 bytes | **Type:** Parquet | **Shape:** 52,473 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-1.0326500049101444, max=8.548700375536482, mean=1.77, median=1.0010820813484795
__index_level_0__: min=726, max=61109, mean=30845.96, median=31254.0
```

### Date/Datetime Column Statistics
```
ds: min=1999-02-09 00:00:00, max=2025-02-28 00:00:00
```

---

## ftsfr_he_kelly_manela_all.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/he_kelly_manela/ftsfr_he_kelly_manela_all.parquet`
**Size:** 23389 bytes | **Type:** Parquet | **Shape:** 2,064 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.2811, max=2012.9658, mean=95.79, median=0.0509
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-01 00:00:00, max=2012-12-01 00:00:00
```

---

## ftsfr_he_kelly_manela_factors_daily.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/he_kelly_manela/ftsfr_he_kelly_manela_factors_daily.parquet`
**Size:** 257321 bytes | **Type:** Parquet | **Shape:** 19,063 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.1603005169783573, max=4698.062377977052, mean=77.57, median=0.0327419481774856
```

### Date/Datetime Column Statistics
```
ds: min=2000-01-03 00:00:00, max=2018-12-11 00:00:00
```

---

## ftsfr_he_kelly_manela_factors_monthly.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/he_kelly_manela/ftsfr_he_kelly_manela_factors_monthly.parquet`
**Size:** 26737 bytes | **Type:** Parquet | **Shape:** 2,348 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.2811, max=2012.9658, mean=92.06, median=0.052500000000000005
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-01 00:00:00, max=2018-11-01 00:00:00
```

---

## ftsfr_french_portfolios_25_daily_size_and_bm.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/ken_french_data_library/ftsfr_french_portfolios_25_daily_size_and_bm.parquet`
**Size:** 2.3 MB | **Type:** Parquet | **Shape:** 650,575 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.9998999999999999, max=1.2793999999999999, mean=0.00, median=0.0008
```

### Date/Datetime Column Statistics
```
ds: min=1926-07-01 00:00:00, max=2025-06-30 00:00:00
```

---

## ftsfr_french_portfolios_25_daily_size_and_inv.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/ken_french_data_library/ftsfr_french_portfolios_25_daily_size_and_inv.parquet`
**Size:** 1.3 MB | **Type:** Parquet | **Shape:** 390,075 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.2089, max=0.1524, mean=0.00, median=0.0008
```

### Date/Datetime Column Statistics
```
ds: min=1963-07-01 00:00:00, max=2025-06-30 00:00:00
```

---

## ftsfr_french_portfolios_25_daily_size_and_op.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/ken_french_data_library/ftsfr_french_portfolios_25_daily_size_and_op.parquet`
**Size:** 1.3 MB | **Type:** Parquet | **Shape:** 390,075 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.21719999999999998, max=0.3675, mean=0.00, median=0.0008
```

### Date/Datetime Column Statistics
```
ds: min=1963-07-01 00:00:00, max=2025-06-30 00:00:00
```

---

## ftsfr_nyu_call_report_cash_liquidity.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/nyu_call_report/ftsfr_nyu_call_report_cash_liquidity.parquet`
**Size:** 23.3 MB | **Type:** Parquet | **Shape:** 1,907,787 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-0.004637848248033172, max=1.0230938416422288, mean=0.08, median=0.05778000501127537
__index_level_0__: min=0, max=1919807, mean=960164.61, median=959908.0
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/nyu_call_report/ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet`
**Size:** 10.3 MB | **Type:** Parquet | **Shape:** 832,932 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-0.0024056979902961173, max=0.9987931814753357, mean=0.07, median=0.051772243080015184
__index_level_0__: min=0, max=833009, mean=416491.05, median=416474.5
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_nyu_call_report_holding_company_leverage.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/nyu_call_report/ftsfr_nyu_call_report_holding_company_leverage.parquet`
**Size:** 10.3 MB | **Type:** Parquet | **Shape:** 832,603 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-61371.42307692308, max=14698.6, mean=11.29, median=10.97832010425305
__index_level_0__: min=0, max=832641, mean=416317.15, median=416309.0
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_nyu_call_report_leverage.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/nyu_call_report/ftsfr_nyu_call_report_leverage.parquet`
**Size:** 22.7 MB | **Type:** Parquet | **Shape:** 1,852,190 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-61371.42307692308, max=36527.066666666666, mean=11.51, median=11.116404014942502
__index_level_0__: min=0, max=1915410, mean=963560.88, median=964297.5
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_cjs_option_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/options/ftsfr_cjs_option_returns.parquet`
**Size:** 91630 bytes | **Type:** Parquet | **Shape:** 15,552 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.13864600229548996, max=2.791869182116687, mean=0.02, median=0.0
```

### Date/Datetime Column Statistics
```
ds: min=1996-01-31 00:00:00, max=2019-12-31 00:00:00
```

---

## ftsfr_hkm_option_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/options/ftsfr_hkm_option_returns.parquet`
**Size:** 39817 bytes | **Type:** Parquet | **Shape:** 5,184 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.07194785160690693, max=0.9284949815963346, mean=0.02, median=0.004017050151524223
```

### Date/Datetime Column Statistics
```
ds: min=1996-01-31 00:00:00, max=2019-12-31 00:00:00
```

---

## ftsfr_treas_bond_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/us_treasury_returns/ftsfr_treas_bond_portfolio_returns.parquet`
**Size:** 75901 bytes | **Type:** Parquet | **Shape:** 6,639 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.06045740780772699, max=0.1210504349533954, mean=0.00, median=0.0038475717070697857
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-31 00:00:00, max=2025-06-30 00:00:00
```

---

## ftsfr_treas_bond_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/us_treasury_returns/ftsfr_treas_bond_returns.parquet`
**Size:** 1.2 MB | **Type:** Parquet | **Shape:** 121,123 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                Float64        
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
unique_id: min=200636.0, max=208417.0, mean=204526.79, median=204053.0
y: min=-0.15135394584216577, max=0.1751899693786838, mean=0.00, median=0.0030176055730861684
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-31 00:00:00, max=2025-06-30 00:00:00
```

---

## ftsfr_CRSP_monthly_stock_ret.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_ret.parquet`
**Size:** 37.3 MB | **Type:** Parquet | **Shape:** 3,810,519 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                Int64          
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
unique_id: min=10000, max=93436, mean=49672.81, median=48195.0
y: min=-1.0, max=26.583827, mean=0.01, median=0.0
__index_level_0__: min=0, max=3826456, mean=1913243.22, median=1912631.0
```

### Date/Datetime Column Statistics
```
ds: min=1926-01-30 00:00:00, max=2024-12-31 00:00:00
```

---

## ftsfr_CRSP_monthly_stock_retx.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_retx.parquet`
**Size:** 34.0 MB | **Type:** Parquet | **Shape:** 3,810,519 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                Int64          
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
unique_id: min=10000, max=93436, mean=49672.81, median=48195.0
y: min=-1.0, max=26.583827, mean=0.01, median=0.0
__index_level_0__: min=0, max=3826456, mean=1913243.22, median=1912631.0
```

### Date/Datetime Column Statistics
```
ds: min=1926-01-30 00:00:00, max=2024-12-31 00:00:00
```

---

## ftsfr_he_kelly_manela_all.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/he_kelly_manela/ftsfr_he_kelly_manela_all.parquet`
**Size:** 23389 bytes | **Type:** Parquet | **Shape:** 2,064 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.2811, max=2012.9658, mean=95.79, median=0.0509
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-01 00:00:00, max=2012-12-01 00:00:00
```

---

## ftsfr_he_kelly_manela_factors_daily.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/he_kelly_manela/ftsfr_he_kelly_manela_factors_daily.parquet`
**Size:** 257321 bytes | **Type:** Parquet | **Shape:** 19,063 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.1603005169783573, max=4698.062377977052, mean=77.57, median=0.0327419481774856
```

### Date/Datetime Column Statistics
```
ds: min=2000-01-03 00:00:00, max=2018-12-11 00:00:00
```

---

## ftsfr_he_kelly_manela_factors_monthly.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/he_kelly_manela/ftsfr_he_kelly_manela_factors_monthly.parquet`
**Size:** 26737 bytes | **Type:** Parquet | **Shape:** 2,348 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.2811, max=2012.9658, mean=92.06, median=0.052500000000000005
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-01 00:00:00, max=2018-11-01 00:00:00
```

---

## ftsfr_french_portfolios_25_daily_size_and_bm.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/ken_french_data_library/ftsfr_french_portfolios_25_daily_size_and_bm.parquet`
**Size:** 2.3 MB | **Type:** Parquet | **Shape:** 650,575 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.9998999999999999, max=1.2793999999999999, mean=0.00, median=0.0008
```

### Date/Datetime Column Statistics
```
ds: min=1926-07-01 00:00:00, max=2025-06-30 00:00:00
```

---

## ftsfr_french_portfolios_25_daily_size_and_inv.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/ken_french_data_library/ftsfr_french_portfolios_25_daily_size_and_inv.parquet`
**Size:** 1.3 MB | **Type:** Parquet | **Shape:** 390,075 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.2089, max=0.1524, mean=0.00, median=0.0008
```

### Date/Datetime Column Statistics
```
ds: min=1963-07-01 00:00:00, max=2025-06-30 00:00:00
```

---

## ftsfr_french_portfolios_25_daily_size_and_op.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/ken_french_data_library/ftsfr_french_portfolios_25_daily_size_and_op.parquet`
**Size:** 1.3 MB | **Type:** Parquet | **Shape:** 390,075 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.21719999999999998, max=0.3675, mean=0.00, median=0.0008
```

### Date/Datetime Column Statistics
```
ds: min=1963-07-01 00:00:00, max=2025-06-30 00:00:00
```

---

## ftsfr_nyu_call_report_cash_liquidity.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_cash_liquidity.parquet`
**Size:** 23.3 MB | **Type:** Parquet | **Shape:** 1,907,787 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-0.004637848248033172, max=1.0230938416422288, mean=0.08, median=0.05778000501127537
__index_level_0__: min=0, max=1919807, mean=960164.61, median=959908.0
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet`
**Size:** 10.3 MB | **Type:** Parquet | **Shape:** 832,932 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-0.0024056979902961173, max=0.9987931814753357, mean=0.07, median=0.051772243080015184
__index_level_0__: min=0, max=833009, mean=416491.05, median=416474.5
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_nyu_call_report_holding_company_leverage.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_holding_company_leverage.parquet`
**Size:** 10.3 MB | **Type:** Parquet | **Shape:** 832,603 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-61371.42307692308, max=14698.6, mean=11.29, median=10.97832010425305
__index_level_0__: min=0, max=832641, mean=416317.15, median=416309.0
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_nyu_call_report_leverage.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_leverage.parquet`
**Size:** 22.7 MB | **Type:** Parquet | **Shape:** 1,852,190 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-61371.42307692308, max=36527.066666666666, mean=11.51, median=11.116404014942502
__index_level_0__: min=0, max=1915410, mean=963560.88, median=964297.5
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_cjs_option_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/options/ftsfr_cjs_option_returns.parquet`
**Size:** 91630 bytes | **Type:** Parquet | **Shape:** 15,552 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.13864600229548996, max=2.791869182116687, mean=0.02, median=0.0
```

### Date/Datetime Column Statistics
```
ds: min=1996-01-31 00:00:00, max=2019-12-31 00:00:00
```

---

## ftsfr_hkm_option_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/options/ftsfr_hkm_option_returns.parquet`
**Size:** 39817 bytes | **Type:** Parquet | **Shape:** 5,184 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.07194785160690693, max=0.9284949815963346, mean=0.02, median=0.004017050151524223
```

### Date/Datetime Column Statistics
```
ds: min=1996-01-31 00:00:00, max=2019-12-31 00:00:00
```

---

## ftsfr_treas_bond_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/ftsfr_treas_bond_portfolio_returns.parquet`
**Size:** 75901 bytes | **Type:** Parquet | **Shape:** 6,639 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.06045740780772699, max=0.1210504349533954, mean=0.00, median=0.0038475717070697857
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-31 00:00:00, max=2025-06-30 00:00:00
```

---

## ftsfr_treas_bond_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/ftsfr_treas_bond_returns.parquet`
**Size:** 1.2 MB | **Type:** Parquet | **Shape:** 121,123 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                Float64        
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
unique_id: min=200636.0, max=208417.0, mean=204526.79, median=204053.0
y: min=-0.15135394584216577, max=0.1751899693786838, mean=0.00, median=0.0030176055730861684
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-31 00:00:00, max=2025-06-30 00:00:00
```

---

## ftsfr_CRSP_monthly_stock_ret.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_ret.parquet`
**Size:** 37.3 MB | **Type:** Parquet | **Shape:** 3,810,519 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                Int64          
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
unique_id: min=10000, max=93436, mean=49672.81, median=48195.0
y: min=-1.0, max=26.583827, mean=0.01, median=0.0
__index_level_0__: min=0, max=3826456, mean=1913243.22, median=1912631.0
```

### Date/Datetime Column Statistics
```
ds: min=1926-01-30 00:00:00, max=2024-12-31 00:00:00
```

---

## ftsfr_CRSP_monthly_stock_retx.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_retx.parquet`
**Size:** 34.0 MB | **Type:** Parquet | **Shape:** 3,810,519 rows × 4 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                Int64          
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
unique_id: min=10000, max=93436, mean=49672.81, median=48195.0
y: min=-1.0, max=26.583827, mean=0.01, median=0.0
__index_level_0__: min=0, max=3826456, mean=1913243.22, median=1912631.0
```

### Date/Datetime Column Statistics
```
ds: min=1926-01-30 00:00:00, max=2024-12-31 00:00:00
```