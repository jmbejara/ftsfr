# Data Glimpses Report: FTSFR only
Total FTSFR datasets: 41

This report provides enhanced analysis specifically for FTSFR (Financial Time Series Forecasting Repository) datasets, including:
- Detailed null value analysis for all columns
- Row uniqueness verification
- Standard dataset metadata and glimpses

## Summary of FTSFR Datasets by Task

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
- [`ftsfr_corp_bond_cs_deciles_clean_trace_mmn_avg5.parquet`](#ftsfr-corp-bond-cs-deciles-clean-trace-mmn-avg5-parquet)
- [`ftsfr_corp_bond_cs_deciles_clean_trace_naive.parquet`](#ftsfr-corp-bond-cs-deciles-clean-trace-naive-parquet)
- [`ftsfr_corp_bond_cs_deciles_mmn_biased.parquet`](#ftsfr-corp-bond-cs-deciles-mmn-biased-parquet)
- [`ftsfr_corp_bond_cs_deciles_mmn_corrected.parquet`](#ftsfr-corp-bond-cs-deciles-mmn-corrected-parquet)
- [`ftsfr_corp_bond_portfolio_returns.parquet`](#ftsfr-corp-bond-portfolio-returns-parquet)
- [`ftsfr_corp_bond_returns.parquet`](#ftsfr-corp-bond-returns-parquet)
- [`ftsfr_corp_bond_str_deciles_naive.parquet`](#ftsfr-corp-bond-str-deciles-naive-parquet)
- [`ftsfr_corp_bond_str_deciles_return_gap.parquet`](#ftsfr-corp-bond-str-deciles-return-gap-parquet)
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
- [`ftsfr_cjs_option_returns_l1_filters.parquet`](#ftsfr-cjs-option-returns-l1-filters-parquet)
- [`ftsfr_cjs_option_returns_l3_filters.parquet`](#ftsfr-cjs-option-returns-l3-filters-parquet)
- [`ftsfr_hkm_option_returns.parquet`](#ftsfr-hkm-option-returns-parquet)
- [`ftsfr_treas_bond_portfolio_returns.parquet`](#ftsfr-treas-bond-portfolio-returns-parquet)
- [`ftsfr_treas_bond_returns.parquet`](#ftsfr-treas-bond-returns-parquet)
- [`ftsfr_treas_portfolios_permissive.parquet`](#ftsfr-treas-portfolios-permissive-parquet)
- [`ftsfr_treas_portfolios_strict.parquet`](#ftsfr-treas-portfolios-strict-parquet)
- [`ftsfr_CRSP_monthly_stock_ret.parquet`](#ftsfr-crsp-monthly-stock-ret-parquet)
- [`ftsfr_CRSP_monthly_stock_retx.parquet`](#ftsfr-crsp-monthly-stock-retx-parquet)
- [`ftsfr_ff25_size_bm_crsp_breaks.parquet`](#ftsfr-ff25-size-bm-crsp-breaks-parquet)
- [`ftsfr_ff25_size_bm_nyse_breaks.parquet`](#ftsfr-ff25-size-bm-nyse-breaks-parquet)

---

## ftsfr_tips_treasury_basis.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/basis_tips_treas/ftsfr_tips_treasury_basis.parquet`
**Size:** 206422 bytes | **Type:** Parquet | **Shape:** 20,647 rows × 3 columns

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
**Size:** 175480 bytes | **Type:** Parquet | **Shape:** 24,537 rows × 3 columns

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
**Size:** 169285 bytes | **Type:** Parquet | **Shape:** 32,022 rows × 3 columns

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
**Size:** 7920 bytes | **Type:** Parquet | **Shape:** 546 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-387.5177840337986, max=57.59304878255962, mean=-62.13, median=-47.59822949472496
```

### Date/Datetime Column Statistics
```
ds: min=2002-07-31 00:00:00, max=2025-03-31 00:00:00
```

---

## ftsfr_CDS_bond_basis_non_aggregated.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/cds_bond_basis/ftsfr_CDS_bond_basis_non_aggregated.parquet`
**Size:** 1.4 MB | **Type:** Parquet | **Shape:** 185,931 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-999.6092364237279, max=998.565884895731, mean=-62.44, median=-44.41025002527942
```

### Date/Datetime Column Statistics
```
ds: min=2002-07-31 00:00:00, max=2025-04-30 00:00:00
```

---

## ftsfr_CDS_contract_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/cds_returns/ftsfr_CDS_contract_returns.parquet`
**Size:** 1.7 MB | **Type:** Parquet | **Shape:** 201,830 rows × 4 columns

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
y: min=-1.805303277625713, max=1.2258522666583374, mean=0.00, median=0.0016596277982949825
__index_level_0__: min=0, max=657848, mean=330612.87, median=331160.0
```

### Date/Datetime Column Statistics
```
ds: min=2001-01-01 00:00:00, max=2023-12-01 00:00:00
```

---

## ftsfr_CDS_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/cds_returns/ftsfr_CDS_portfolio_returns.parquet`
**Size:** 57490 bytes | **Type:** Parquet | **Shape:** 5,510 rows × 4 columns

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
y: min=5.3628018753738094e-05, max=0.019341884154433435, mean=0.00, median=0.000844851743564012
__index_level_0__: min=0, max=5519, mean=2759.04, median=2759.5
```

### Date/Datetime Column Statistics
```
ds: min=2001-01-01 00:00:00, max=2023-12-01 00:00:00
```

---

## ftsfr_CIP_spreads.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/cip/ftsfr_CIP_spreads.parquet`
**Size:** 405254 bytes | **Type:** Parquet | **Shape:** 43,490 rows × 3 columns

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
**Size:** 96115 bytes | **Type:** Parquet | **Shape:** 11,553 rows × 3 columns

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

## ftsfr_corp_bond_cs_deciles_clean_trace_mmn_avg5.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/corp_bond_returns/ftsfr_corp_bond_cs_deciles_clean_trace_mmn_avg5.parquet`
**Size:** 24622 bytes | **Type:** Parquet | **Shape:** 2,720 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.22357092935502973, max=0.25356670278634535, mean=0.00, median=0.0016059214131858583
```

### Date/Datetime Column Statistics
```
ds: min=2002-07-31 00:00:00, max=2025-02-28 00:00:00
```

---

## ftsfr_corp_bond_cs_deciles_clean_trace_naive.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/corp_bond_returns/ftsfr_corp_bond_cs_deciles_clean_trace_naive.parquet`
**Size:** 24450 bytes | **Type:** Parquet | **Shape:** 2,700 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.2248109225996762, max=0.2596163986608802, mean=0.00, median=0.0013400098346253945
```

### Date/Datetime Column Statistics
```
ds: min=2002-07-31 00:00:00, max=2024-12-31 00:00:00
```

---

## ftsfr_corp_bond_cs_deciles_mmn_biased.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/corp_bond_returns/ftsfr_corp_bond_cs_deciles_mmn_biased.parquet`
**Size:** 21895 bytes | **Type:** Parquet | **Shape:** 2,420 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.2594052674114324, max=0.2513002401918888, mean=0.01, median=0.005170805499523739
```

### Date/Datetime Column Statistics
```
ds: min=2002-08-31 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_corp_bond_cs_deciles_mmn_corrected.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/corp_bond_returns/ftsfr_corp_bond_cs_deciles_mmn_corrected.parquet`
**Size:** 21927 bytes | **Type:** Parquet | **Shape:** 2,420 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.24688298917418602, max=0.2495876823518415, mean=0.01, median=0.004856605189169083
```

### Date/Datetime Column Statistics
```
ds: min=2002-08-31 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_corp_bond_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/corp_bond_returns/ftsfr_corp_bond_portfolio_returns.parquet`
**Size:** 15518 bytes | **Type:** Parquet | **Shape:** 2,690 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float32        
```

### Numeric Column Statistics
```
y: min=-0.29776981472969055, max=0.3147818148136139, mean=0.01, median=0.00559262465685606
```

### Date/Datetime Column Statistics
```
ds: min=2002-08-31 00:00:00, max=2024-12-31 00:00:00
```

---

## ftsfr_corp_bond_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/corp_bond_returns/ftsfr_corp_bond_returns.parquet`
**Size:** 7.6 MB | **Type:** Parquet | **Shape:** 1,859,498 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float32        
```

### Numeric Column Statistics
```
y: min=-0.9981083273887634, max=9.000757217407227, mean=0.00, median=0.0037167782429605722
```

### Date/Datetime Column Statistics
```
ds: min=2002-08-31 00:00:00, max=2025-03-31 00:00:00
```

---

## ftsfr_corp_bond_str_deciles_naive.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/corp_bond_returns/ftsfr_corp_bond_str_deciles_naive.parquet`
**Size:** 24447 bytes | **Type:** Parquet | **Shape:** 2,710 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.2352337616651138, max=0.29116162225490994, mean=0.00, median=0.0051665858754277845
```

### Date/Datetime Column Statistics
```
ds: min=2002-08-31 00:00:00, max=2025-02-28 00:00:00
```

---

## ftsfr_corp_bond_str_deciles_return_gap.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/corp_bond_returns/ftsfr_corp_bond_str_deciles_return_gap.parquet`
**Size:** 24413 bytes | **Type:** Parquet | **Shape:** 2,710 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.2416465447245652, max=0.2608625376225763, mean=0.00, median=0.004795266069267316
```

### Date/Datetime Column Statistics
```
ds: min=2002-08-31 00:00:00, max=2025-02-28 00:00:00
```

---

## ftsfr_treas_yield_curve_zero_coupon.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/fed_yield_curve/ftsfr_treas_yield_curve_zero_coupon.parquet`
**Size:** 2.4 MB | **Type:** Parquet | **Shape:** 374,312 rows × 4 columns

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
y: min=0.0554, max=16.462, mean=5.60, median=5.2962389140670005
__index_level_0__: min=0, max=502889, mean=226669.36, median=211886.5
```

### Date/Datetime Column Statistics
```
ds: min=1961-06-14 00:00:00, max=2025-09-12 00:00:00
```

---

## ftsfr_FX_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/foreign_exchange/ftsfr_FX_returns.parquet`
**Size:** 540474 bytes | **Type:** Parquet | **Shape:** 52,473 rows × 4 columns

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
y: min=-0.0871113821876851, max=0.21402418151392366, mean=0.00, median=3.297222222222222e-05
__index_level_0__: min=726, max=61109, mean=30845.96, median=31254.0
```

### Date/Datetime Column Statistics
```
ds: min=1999-02-09 00:00:00, max=2025-02-28 00:00:00
```

---

## ftsfr_he_kelly_manela_all.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/he_kelly_manela/ftsfr_he_kelly_manela_all.parquet`
**Size:** 10082 bytes | **Type:** Parquet | **Shape:** 1,032 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.2811, max=0.3965, mean=0.00, median=0.00395
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-01 00:00:00, max=2012-12-01 00:00:00
```

---

## ftsfr_he_kelly_manela_factors_daily.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/he_kelly_manela/ftsfr_he_kelly_manela_factors_daily.parquet`
**Size:** 121548 bytes | **Type:** Parquet | **Shape:** 9,531 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.1603005169783553, max=0.1935092357636356, mean=0.00, median=0.0002479190852231
```

### Date/Datetime Column Statistics
```
ds: min=2000-01-03 00:00:00, max=2018-12-11 00:00:00
```

---

## ftsfr_he_kelly_manela_factors_monthly.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/he_kelly_manela/ftsfr_he_kelly_manela_factors_monthly.parquet`
**Size:** 12487 bytes | **Type:** Parquet | **Shape:** 1,174 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.2811, max=0.3965, mean=0.01, median=0.004699999999999999
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-01 00:00:00, max=2018-11-01 00:00:00
```

---

## ftsfr_french_portfolios_25_daily_size_and_bm.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/ken_french_data_library/ftsfr_french_portfolios_25_daily_size_and_bm.parquet`
**Size:** 2.2 MB | **Type:** Parquet | **Shape:** 650,575 rows × 3 columns

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
**Size:** 947632 bytes | **Type:** Parquet | **Shape:** 390,075 rows × 3 columns

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
**Size:** 948984 bytes | **Type:** Parquet | **Shape:** 390,075 rows × 3 columns

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
**Size:** 13.9 MB | **Type:** Parquet | **Shape:** 1,906,765 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=0.0, max=1.0230938416422288, mean=0.08, median=0.05780420579828501
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/nyu_call_report/ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet`
**Size:** 6.1 MB | **Type:** Parquet | **Shape:** 832,902 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=0.0, max=0.9987931814753357, mean=0.07, median=0.05177395811931505
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_nyu_call_report_holding_company_leverage.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/nyu_call_report/ftsfr_nyu_call_report_holding_company_leverage.parquet`
**Size:** 6.0 MB | **Type:** Parquet | **Shape:** 831,858 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=1.0, max=14698.6, mean=11.62, median=10.981269862683128
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_nyu_call_report_leverage.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/nyu_call_report/ftsfr_nyu_call_report_leverage.parquet`
**Size:** 13.4 MB | **Type:** Parquet | **Shape:** 1,849,957 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=0.952712100139082, max=36527.066666666666, mean=11.86, median=11.121173104434908
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_cjs_option_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/options/ftsfr_cjs_option_returns.parquet`
**Size:** 86028 bytes | **Type:** Parquet | **Shape:** 15,552 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.4527408759578536, max=1.546129568151272, mean=-0.01, median=0.0
```

### Date/Datetime Column Statistics
```
ds: min=1996-01-31 00:00:00, max=2019-12-31 00:00:00
```

---

## ftsfr_cjs_option_returns_l1_filters.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/options/ftsfr_cjs_option_returns_l1_filters.parquet`
**Size:** 119884 bytes | **Type:** Parquet | **Shape:** 15,552 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.345428230125723, max=0.7833790941426158, mean=-0.00, median=-0.006498290569884879
```

### Date/Datetime Column Statistics
```
ds: min=1996-01-31 00:00:00, max=2019-12-31 00:00:00
```

---

## ftsfr_cjs_option_returns_l3_filters.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/options/ftsfr_cjs_option_returns_l3_filters.parquet`
**Size:** 86229 bytes | **Type:** Parquet | **Shape:** 15,552 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.41676144499828416, max=2.000989147256664, mean=-0.00, median=0.0
```

### Date/Datetime Column Statistics
```
ds: min=1996-01-31 00:00:00, max=2019-12-31 00:00:00
```

---

## ftsfr_hkm_option_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/options/ftsfr_hkm_option_returns.parquet`
**Size:** 37424 bytes | **Type:** Parquet | **Shape:** 5,184 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.4007418311074428, max=0.8153642585692351, mean=-0.01, median=-0.0010693203501211206
```

### Date/Datetime Column Statistics
```
ds: min=1996-01-31 00:00:00, max=2019-12-31 00:00:00
```

---

## ftsfr_treas_bond_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/us_treasury_returns/ftsfr_treas_bond_portfolio_returns.parquet`
**Size:** 59620 bytes | **Type:** Parquet | **Shape:** 6,659 rows × 3 columns

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
ds: min=1970-01-31 00:00:00, max=2025-08-31 00:00:00
```

---

## ftsfr_treas_bond_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/us_treasury_returns/ftsfr_treas_bond_returns.parquet`
**Size:** 918854 bytes | **Type:** Parquet | **Shape:** 121,827 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                Float64        
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
unique_id: min=200636.0, max=208448.0, mean=204544.46, median=204055.0
y: min=-0.15135394584216577, max=0.1751899693786838, mean=0.00, median=0.003016939008775532
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-31 00:00:00, max=2025-08-31 00:00:00
```

---

## ftsfr_treas_portfolios_permissive.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/us_treasury_returns/ftsfr_treas_portfolios_permissive.parquet`
**Size:** 60611 bytes | **Type:** Parquet | **Shape:** 6,739 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.06045740780772699, max=0.1210504349533954, mean=0.00, median=0.0037053095216066164
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-31 00:00:00, max=2026-04-30 00:00:00
```

---

## ftsfr_treas_portfolios_strict.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/us_treasury_returns/ftsfr_treas_portfolios_strict.parquet`
**Size:** 60476 bytes | **Type:** Parquet | **Shape:** 6,737 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.062063648538674354, max=0.1210504349533954, mean=0.00, median=0.003803967966345523
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-31 00:00:00, max=2026-04-30 00:00:00
```

---

## ftsfr_CRSP_monthly_stock_ret.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_ret.parquet`
**Size:** 15.7 MB | **Type:** Parquet | **Shape:** 3,810,519 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                Int64          
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
unique_id: min=10000, max=93436, mean=49672.81, median=48195.0
y: min=-1.0, max=26.583827, mean=0.01, median=0.0
```

### Date/Datetime Column Statistics
```
ds: min=1926-01-30 00:00:00, max=2024-12-31 00:00:00
```

---

## ftsfr_CRSP_monthly_stock_retx.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_retx.parquet`
**Size:** 14.4 MB | **Type:** Parquet | **Shape:** 3,810,519 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                Int64          
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
unique_id: min=10000, max=93436, mean=49672.81, median=48195.0
y: min=-1.0, max=26.583827, mean=0.01, median=0.0
```

### Date/Datetime Column Statistics
```
ds: min=1926-01-30 00:00:00, max=2024-12-31 00:00:00
```

---

## ftsfr_ff25_size_bm_crsp_breaks.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/wrds_crsp_compustat/ftsfr_ff25_size_bm_crsp_breaks.parquet`
**Size:** 151826 bytes | **Type:** Parquet | **Shape:** 18,798 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.356376960504943, max=0.5612853884390135, mean=0.01, median=0.012013706464488216
```

### Date/Datetime Column Statistics
```
ds: min=1961-07-31 00:00:00, max=2024-12-31 00:00:00
```

---

## ftsfr_ff25_size_bm_nyse_breaks.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/formatted/wrds_crsp_compustat/ftsfr_ff25_size_bm_nyse_breaks.parquet`
**Size:** 151808 bytes | **Type:** Parquet | **Shape:** 18,798 rows × 3 columns

**All rows unique:** ✅ Yes

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.34166685527837604, max=0.42345806932975555, mean=0.01, median=0.01303340016647999
```

### Date/Datetime Column Statistics
```
ds: min=1961-07-31 00:00:00, max=2024-12-31 00:00:00
```