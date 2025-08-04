# Data Glimpses Report
Total files: 43

## Summary of Datasets by Task

### Compile Sphinx Docs
- [`clean_1970_2008_commodities_data.csv`](#clean-1970-2008-commodities-data-csv)
- [`clean_2009_2024_commodities_data.csv`](#clean-2009-2024-commodities-data-csv)
- [`commodities_data.csv`](#commodities-data-csv)
- [`commodity_futures.parquet`](#commodity-futures-parquet)
- [`filtered_info.csv`](#filtered-info-csv)
- [`gsci_indices.parquet`](#gsci-indices-parquet)
- [`raw_data.csv`](#raw-data-csv)

### Create Data Glimpses
- [`clean_1970_2008_commodities_data.csv`](#clean-1970-2008-commodities-data-csv)
- [`clean_2009_2024_commodities_data.csv`](#clean-2009-2024-commodities-data-csv)
- [`commodities_data.csv`](#commodities-data-csv)
- [`commodity_futures.parquet`](#commodity-futures-parquet)
- [`filtered_info.csv`](#filtered-info-csv)
- [`gsci_indices.parquet`](#gsci-indices-parquet)
- [`raw_data.csv`](#raw-data-csv)

### Format
#### Format: Cds Bond Basis
- [`Final_data.parquet`](#final-data-parquet)
- [`Red_Data.parquet`](#red-data-parquet)
- [`ftsfr_CDS_bond_basis_aggregated.parquet`](#ftsfr-cds-bond-basis-aggregated-parquet)
- [`ftsfr_CDS_bond_basis_non_aggregated.parquet`](#ftsfr-cds-bond-basis-non-aggregated-parquet)
#### Format: Cds Returns
- [`ftsfr_CDS_contract_returns.parquet`](#ftsfr-cds-contract-returns-parquet)
- [`ftsfr_CDS_portfolio_returns.parquet`](#ftsfr-cds-portfolio-returns-parquet)
- [`markit_cds_contract_returns.parquet`](#markit-cds-contract-returns-parquet)
- [`markit_cds_returns.parquet`](#markit-cds-returns-parquet)
#### Format: Cip
- [`cip_spreads.parquet`](#cip-spreads-parquet)
- [`ftsfr_CIP_spreads.parquet`](#ftsfr-cip-spreads-parquet)
#### Format: Corp Bond Returns
- [`corp_bond_portfolio_returns.parquet`](#corp-bond-portfolio-returns-parquet)
- [`ftsfr_corp_bond_portfolio_returns.parquet`](#ftsfr-corp-bond-portfolio-returns-parquet)
- [`ftsfr_corp_bond_returns.parquet`](#ftsfr-corp-bond-returns-parquet)
#### Format: Fed Yield Curve
- [`ftsfr_treas_yield_curve_zero_coupon.parquet`](#ftsfr-treas-yield-curve-zero-coupon-parquet)
#### Format: Foreign Exchange
- [`ftsfr_FX_returns.parquet`](#ftsfr-fx-returns-parquet)
#### Format: Futures Returns
- [`futures_returns.parquet`](#futures-returns-parquet)
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
#### Format: Portfolios
- [`cjs_portfolio_returns_1996-01_2019-12.parquet`](#cjs-portfolio-returns-1996-01-2019-12-parquet)
- [`hkm_portfolio_returns_1996-01_2019-12.parquet`](#hkm-portfolio-returns-1996-01-2019-12-parquet)
#### Format: Us Treasury Returns
- [`ftsfr_treas_bond_portfolio_returns.parquet`](#ftsfr-treas-bond-portfolio-returns-parquet)
- [`ftsfr_treas_bond_returns.parquet`](#ftsfr-treas-bond-returns-parquet)
- [`issue_dates.parquet`](#issue-dates-parquet)
- [`treasuries_with_run_status.parquet`](#treasuries-with-run-status-parquet)
#### Format: Wrds Crsp Compustat
- [`ftsfr_CRSP_monthly_stock_ret.parquet`](#ftsfr-crsp-monthly-stock-ret-parquet)
- [`ftsfr_CRSP_monthly_stock_retx.parquet`](#ftsfr-crsp-monthly-stock-retx-parquet)

---

## Final_data.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/Final_data.parquet`
**Size:** 18.7 MB | **Type:** Parquet | **Shape:** 653,331 rows × 9 columns

### Columns
```
cusip                                    String         
date                                     Datetime(time_unit='ns', time_zone=None)
mat_days                                 Float64         (5.4% null)
BOND_YIELD                               Float64         (9.7% null)
CS                                       Float64         (9.7% null)
size_ig                                  Float64         (5.4% null)
size_jk                                  Float64         (5.4% null)
par_spread                               Float64         (5.4% null)
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
mat_days: min=360.99999999999994, max=36525.0, mean=3796.56, median=2461.0
BOND_YIELD: min=-0.79189766622368, max=11.679347680642085, mean=0.05, median=0.0419328913688659
CS: min=-0.8427172227775009, max=11.666247680642083, mean=0.02, median=0.01608780586788075
size_ig: min=0.0, max=1.0, mean=0.82, median=1.0
size_jk: min=0.0, max=1.0, mean=0.98, median=1.0
par_spread: min=-277.079498250281, max=1307.7831991672729, mean=0.06, median=0.007558154277775008
__index_level_0__: min=39, max=1392527, mean=692523.03, median=696215.0
```

### Date/Datetime Column Statistics
```
date: min=2002-09-30 00:00:00, max=2022-09-30 00:00:00
```

---

## Red_Data.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/Red_Data.parquet`
**Size:** 20.2 MB | **Type:** Parquet | **Shape:** 1,393,014 rows × 9 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
cusip                                    String         
issuer_cusip                             String         
BOND_YIELD                               Float64         (10.5% null)
CS                                       Float64         (10.5% null)
size_ig                                  Float64         (5.9% null)
size_jk                                  Float64         (5.9% null)
mat_days                                 Float64         (5.9% null)
redcode                                  String         
```

### Numeric Column Statistics
```
BOND_YIELD: min=-0.79189766622368, max=24.42611933726512, mean=0.05, median=0.0434126391410827
CS: min=-0.8427172227775009, max=24.41471933726512, mean=0.03, median=0.0170076781690773
size_ig: min=0.0, max=1.0, mean=0.82, median=1.0
size_jk: min=0.0, max=1.0, mean=0.98, median=1.0
mat_days: min=360.99999999999994, max=36525.0, mean=3765.83, median=2480.0
```

### Date/Datetime Column Statistics
```
date: min=2002-08-31 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_CDS_bond_basis_aggregated.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/ftsfr_CDS_bond_basis_aggregated.parquet`
**Size:** 2648 bytes | **Type:** Parquet | **Shape:** 3 rows × 3 columns

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=0.011816992084125148, max=0.02442321441593389, mean=0.02, median=0.022377150480063716
```

### Date/Datetime Column Statistics
```
ds: min=2011-09-22 11:50:47, max=2014-01-19 07:45:18
```

---

## ftsfr_CDS_bond_basis_non_aggregated.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/ftsfr_CDS_bond_basis_non_aggregated.parquet`
**Size:** 5.0 MB | **Type:** Parquet | **Shape:** 585,501 rows × 3 columns

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-0.9998623956278941, max=0.9984502978149778, mean=0.02, median=0.025790764565877616
```

### Date/Datetime Column Statistics
```
ds: min=2002-09-30 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_CDS_contract_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_returns/ftsfr_CDS_contract_returns.parquet`
**Size:** 2.1 MB | **Type:** Parquet | **Shape:** 657,849 rows × 3 columns

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64         (69.3% null)
```

### Numeric Column Statistics
```
y: min=-1.801384532077174, max=1.225852266658336, mean=0.00, median=0.0016597483959082115
```

### Date/Datetime Column Statistics
```
ds: min=2001-01-01 00:00:00, max=2023-12-01 00:00:00
```

---

## ftsfr_CDS_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_returns/ftsfr_CDS_portfolio_returns.parquet`
**Size:** 59069 bytes | **Type:** Parquet | **Shape:** 5,520 rows × 3 columns

### Columns
```
ds                                       Datetime(time_unit='ns', time_zone=None)
unique_id                                String         
y                                        Float64         (0.2% null)
```

### Numeric Column Statistics
```
y: min=5.369743582546023e-05, max=0.019347339453824004, mean=0.00, median=0.0008434645081699891
```

### Date/Datetime Column Statistics
```
ds: min=2001-01-01 00:00:00, max=2023-12-01 00:00:00
```

---

## markit_cds_contract_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_returns/markit_cds_contract_returns.parquet`
**Size:** 1.7 MB | **Type:** Parquet | **Shape:** 657,849 rows × 5 columns

### Columns
```
ticker                                   String         
tenor                                    String         
Month                                    Datetime(time_unit='ns', time_zone=None)
credit_quantile                          Int32          
monthly_return                           Float64        
```

### Numeric Column Statistics
```
credit_quantile: min=1, max=5, mean=2.99, median=3.0
monthly_return: min=-1.801384532077174, max=1.225852266658336, mean=nan, median=nan
```

### Date/Datetime Column Statistics
```
Month: min=2001-01-01 00:00:00, max=2023-12-01 00:00:00
```

---

## markit_cds_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_returns/markit_cds_returns.parquet`
**Size:** 50492 bytes | **Type:** Parquet | **Shape:** 276 rows × 21 columns

### Columns
```
Month                                    Datetime(time_unit='ns', time_zone=None)
3Y_Q1                                    Float64        
3Y_Q2                                    Float64        
3Y_Q3                                    Float64         (0.4% null)
3Y_Q4                                    Float64        
3Y_Q5                                    Float64         (0.4% null)
5Y_Q1                                    Float64        
5Y_Q2                                    Float64        
5Y_Q3                                    Float64         (0.4% null)
5Y_Q4                                    Float64        
5Y_Q5                                    Float64         (0.4% null)
7Y_Q1                                    Float64        
7Y_Q2                                    Float64         (0.4% null)
7Y_Q3                                    Float64         (0.4% null)
7Y_Q4                                    Float64        
7Y_Q5                                    Float64         (0.4% null)
10Y_Q1                                   Float64        
10Y_Q2                                   Float64         (0.4% null)
10Y_Q3                                   Float64         (0.4% null)
10Y_Q4                                   Float64        
10Y_Q5                                   Float64         (0.4% null)
```

### Numeric Column Statistics
```
3Y_Q1: min=5.369743582546023e-05, max=0.0012980230560060175, mean=0.00, median=0.00017743687127700332
3Y_Q2: min=9.890717740049931e-05, max=0.0017588284785996988, mean=0.00, median=0.0002987134278182274
3Y_Q3: min=0.00016861626747910653, max=0.002827035917619095, mean=0.00, median=0.0004872614951597473
3Y_Q4: min=0.0003547487444510221, max=0.008640120439165816, mean=0.00, median=0.0008249659736536659
3Y_Q5: min=0.001030621917200844, max=0.017049098762459358, mean=0.00, median=0.003318161851193739
5Y_Q1: min=8.237507062114346e-05, max=0.0013420012384308677, mean=0.00, median=0.00027969724547605157
5Y_Q2: min=0.00016716533693172939, max=0.0015301593893626284, mean=0.00, median=0.0005009607208141808
5Y_Q3: min=0.0002442534777740146, max=0.0029749808499448527, mean=0.00, median=0.000755465681070655
5Y_Q4: min=0.0006774992502349696, max=0.00865081300728354, mean=0.00, median=0.0013604492672859567
5Y_Q5: min=0.001823802572132216, max=0.01831490376557743, mean=0.01, median=0.004584026504554917
7Y_Q1: min=0.00010969553239569861, max=0.001395262057975026, mean=0.00, median=0.00036196106090487993
7Y_Q2: min=8.178435897309316e-05, max=0.001531547466269419, mean=0.00, median=0.0006681111979401365
7Y_Q3: min=0.00012350865211231362, max=0.0030665824725507854, mean=0.00, median=0.0009957907324064793
7Y_Q4: min=0.0011033433829667895, max=0.007199576463468103, mean=0.00, median=0.002065332885962982
7Y_Q5: min=0.0024406343187873274, max=0.01900882113270006, mean=0.01, median=0.00542397295941808
10Y_Q1: min=0.00013495731545203112, max=0.000906246428705273, mean=0.00, median=0.0004826144845039398
10Y_Q2: min=7.050177956378875e-05, max=0.0015003347431000102, mean=0.00, median=0.0007530286580239831
10Y_Q3: min=0.00014069043206568028, max=0.0031375800133079854, mean=0.00, median=0.0011660230700828562
10Y_Q4: min=0.001372121612567035, max=0.007455084170904128, mean=0.00, median=0.002304823617233342
10Y_Q5: min=0.0030454563814391435, max=0.019347339453824004, mean=0.01, median=0.006118495066802664
```

### Date/Datetime Column Statistics
```
Month: min=2001-01-01 00:00:00, max=2023-12-01 00:00:00
```

---

## cip_spreads.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cip/cip_spreads.parquet`
**Size:** 463478 bytes | **Type:** Parquet | **Shape:** 6,790 rows × 9 columns

### Columns
```
AUD                                      Float64         (11.5% null)
CAD                                      Float64         (16.0% null)
CHF                                      Float64         (41.1% null)
EUR                                      Float64         (23.2% null)
GBP                                      Float64         (11.2% null)
JPY                                      Float64         (15.1% null)
NZD                                      Float64         (14.5% null)
SEK                                      Float64         (26.8% null)
index                                    Date           
```

### Numeric Column Statistics
```
AUD: min=-58.53520492586132, max=339.68876731391674, mean=1.89, median=1.1534613513037661
CAD: min=-11.13750568037226, max=313.1892275693841, mean=15.41, median=10.361567750541223
CHF: min=-9.265949135860806, max=181.36353541348308, mean=34.16, median=29.999955867636082
EUR: min=-22.949139790071722, max=370.9439992219156, mean=26.25, median=21.257006012834353
GBP: min=-11.71473649302368, max=287.634939349282, mean=14.36, median=8.552763054047798
JPY: min=-31.23245606446813, max=439.59367390435733, mean=37.54, median=31.855508763267146
NZD: min=-65.25243119248204, max=257.4711793363026, mean=0.09, median=-5.4573860355283665
SEK: min=-75.02010739148606, max=374.5435302007317, mean=29.33, median=21.911787065051698
```

### Date/Datetime Column Statistics
```
index: min=1999-02-08, max=2025-02-28
```

---

## ftsfr_CIP_spreads.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cip/ftsfr_CIP_spreads.parquet`
**Size:** 515176 bytes | **Type:** Parquet | **Shape:** 43,490 rows × 3 columns

### Columns
```
unique_id                                Date           
ds                                       String         
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-75.02010739148606, max=439.59367390435733, mean=18.90, median=12.660612223492215
```

### Date/Datetime Column Statistics
```
unique_id: min=2001-12-04, max=2025-02-28
```

---

## corp_bond_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/corp_bond_returns/corp_bond_portfolio_returns.parquet`
**Size:** 30784 bytes | **Type:** Parquet | **Shape:** 242 rows × 11 columns

### Columns
```
1.0                                      Float64        
2.0                                      Float64        
3.0                                      Float64        
4.0                                      Float64        
5.0                                      Float64        
6.0                                      Float64        
7.0                                      Float64        
8.0                                      Float64        
9.0                                      Float64        
10.0                                     Float64        
date                                     Datetime(time_unit='ns', time_zone=None)
```

### Numeric Column Statistics
```
1.0: min=-0.03068268413930533, max=0.06950119876242539, mean=0.00, median=0.0025212548659277806
2.0: min=-0.03154058146950561, max=0.09200405914825867, mean=0.00, median=0.0033263712962400167
3.0: min=-0.04204252908317171, max=0.0950101115275016, mean=0.00, median=0.003868204582278221
4.0: min=-0.05147918759840897, max=0.08843591054859191, mean=0.00, median=0.004903852973122345
5.0: min=-0.05805336409042862, max=0.06776123719196807, mean=0.00, median=0.005554600117954448
6.0: min=-0.06360918103223694, max=0.061527786407500645, mean=0.00, median=0.005963022144223493
7.0: min=-0.07895884316221219, max=0.06603249291317947, mean=0.01, median=0.007335034911052822
8.0: min=-0.09269304837386032, max=0.08062643339966763, mean=0.01, median=0.006837097384664679
9.0: min=-0.12523765291001504, max=0.14530789126043045, mean=0.01, median=0.007428867950410213
10.0: min=-0.2357410309055786, max=0.21497478314108745, mean=0.01, median=0.007058037007308077
```

### Date/Datetime Column Statistics
```
date: min=2002-08-31 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_corp_bond_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/corp_bond_returns/ftsfr_corp_bond_portfolio_returns.parquet`
**Size:** 28080 bytes | **Type:** Parquet | **Shape:** 2,420 rows × 3 columns

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
**Size:** 13.0 MB | **Type:** Parquet | **Shape:** 1,046,059 rows × 4 columns

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-0.9753107633155358, max=3.68351, mean=0.00, median=0.0033377041526085
__index_level_0__: min=0, max=1572380, mean=775814.95, median=760643.0
```

### Date/Datetime Column Statistics
```
ds: min=2002-08-31 00:00:00, max=2022-09-30 00:00:00
```

---

## ftsfr_treas_yield_curve_zero_coupon.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/fed_yield_curve/ftsfr_treas_yield_curve_zero_coupon.parquet`
**Size:** 3.6 MB | **Type:** Parquet | **Shape:** 501,840 rows × 3 columns

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64         (25.6% null)
```

### Numeric Column Statistics
```
y: min=0.0554, max=16.462, mean=5.60, median=5.30861424468
```

### Date/Datetime Column Statistics
```
ds: min=1961-06-14 00:00:00, max=2025-07-25 00:00:00
```

---

## ftsfr_FX_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/foreign_exchange/ftsfr_FX_returns.parquet`
**Size:** 574390 bytes | **Type:** Parquet | **Shape:** 52,473 rows × 3 columns

### Columns
```
unique_id                                Date           
ds                                       String         
y                                        Float64        
```

### Numeric Column Statistics
```
y: min=-1.0174066673165025, max=8.606725628359724, mean=1.77, median=1.001
```

### Date/Datetime Column Statistics
```
unique_id: min=1999-02-09, max=2025-02-28
```

---

## futures_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/futures_returns/futures_returns.parquet`
**Size:** 18.4 MB | **Type:** Parquet | **Shape:** 4,947,175 rows × 5 columns

### Columns
```
futcode                                  Float64        
date                                     Datetime(time_unit='ns', time_zone=None)
settlement                               Float64         (0.1% null)
contrdate                                String         
product_code                             Int64          
```

### Numeric Column Statistics
```
futcode: min=37.0, max=489247.0, mean=205222.38, median=181741.0
settlement: min=-37.630005, max=24480.0, mean=599.01, median=59.75
product_code: min=289, max=3847, mean=2122.46, median=2060.0
```

### Date/Datetime Column Statistics
```
date: min=1973-01-02 00:00:00, max=2025-07-30 00:00:00
```

---

## ftsfr_he_kelly_manela_all.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/he_kelly_manela/ftsfr_he_kelly_manela_all.parquet`
**Size:** 23389 bytes | **Type:** Parquet | **Shape:** 2,064 rows × 3 columns

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
**Size:** 369916 bytes | **Type:** Parquet | **Shape:** 19,063 rows × 4 columns

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-0.1603005169783573, max=4698.062377977052, mean=77.57, median=0.0327419481774856
__index_level_0__: min=0, max=19063, mean=9531.75, median=9532.0
```

### Date/Datetime Column Statistics
```
ds: min=2000-01-03 00:00:00, max=2018-12-11 00:00:00
```

---

## ftsfr_he_kelly_manela_factors_monthly.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/he_kelly_manela/ftsfr_he_kelly_manela_factors_monthly.parquet`
**Size:** 26737 bytes | **Type:** Parquet | **Shape:** 2,348 rows × 3 columns

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
**Size:** 15.5 MB | **Type:** Parquet | **Shape:** 1,919,810 rows × 3 columns

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64         (0.6% null)
```

### Numeric Column Statistics
```
y: min=-0.004637848248033172, max=inf, mean=inf, median=0.05778003041054232
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet`
**Size:** 6.8 MB | **Type:** Parquet | **Shape:** 833,010 rows × 3 columns

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64         (0.0% null)
```

### Numeric Column Statistics
```
y: min=-0.0024056979902961173, max=0.9987931814753357, mean=0.07, median=0.051772243080015184
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_nyu_call_report_holding_company_leverage.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_holding_company_leverage.parquet`
**Size:** 6.8 MB | **Type:** Parquet | **Shape:** 833,010 rows × 3 columns

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64         (0.0% null)
```

### Numeric Column Statistics
```
y: min=-61371.42307692308, max=inf, mean=inf, median=10.979716024340771
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## ftsfr_nyu_call_report_leverage.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_leverage.parquet`
**Size:** 15.1 MB | **Type:** Parquet | **Shape:** 1,919,810 rows × 3 columns

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64         (3.3% null)
```

### Numeric Column Statistics
```
y: min=-61371.42307692308, max=inf, mean=inf, median=11.125577574699662
```

### Date/Datetime Column Statistics
```
ds: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
```

---

## cjs_portfolio_returns_1996-01_2019-12.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/options/cjs_portfolio_returns_1996-01_2019-12.parquet`
**Size:** 122079 bytes | **Type:** Parquet | **Shape:** 15,552 rows × 3 columns

### Columns
```
return                                   Float64        
ftfsa_id                                 String         
date                                     Datetime(time_unit='ns', time_zone=None)
```

### Numeric Column Statistics
```
return: min=-0.13864600229548996, max=2.791869182116687, mean=0.02, median=0.0
```

### Date/Datetime Column Statistics
```
date: min=1996-01-31 00:00:00, max=2019-12-31 00:00:00
```

---

## ftsfr_cjs_option_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/options/ftsfr_cjs_option_returns.parquet`
**Size:** 91678 bytes | **Type:** Parquet | **Shape:** 15,552 rows × 3 columns

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
**Size:** 39865 bytes | **Type:** Parquet | **Shape:** 5,184 rows × 3 columns

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

## hkm_portfolio_returns_1996-01_2019-12.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/options/hkm_portfolio_returns_1996-01_2019-12.parquet`
**Size:** 51931 bytes | **Type:** Parquet | **Shape:** 5,184 rows × 3 columns

### Columns
```
return                                   Float64        
ftfsa_id                                 String         
date                                     Datetime(time_unit='ns', time_zone=None)
```

### Numeric Column Statistics
```
return: min=-0.07194785160690693, max=0.9284949815963346, mean=0.02, median=0.004017050151524223
```

### Date/Datetime Column Statistics
```
date: min=1996-01-31 00:00:00, max=2019-12-31 00:00:00
```

---

## ftsfr_treas_bond_portfolio_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/ftsfr_treas_bond_portfolio_returns.parquet`
**Size:** 113785 bytes | **Type:** Parquet | **Shape:** 6,639 rows × 4 columns

### Columns
```
unique_id                                String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
y: min=-0.06045740780772699, max=0.1210504349533954, mean=0.00, median=0.0038475717070697857
__index_level_0__: min=0, max=6659, mean=3325.80, median=3325.0
```

### Date/Datetime Column Statistics
```
ds: min=1970-01-31 00:00:00, max=2025-06-30 00:00:00
```

---

## ftsfr_treas_bond_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/ftsfr_treas_bond_returns.parquet`
**Size:** 1.2 MB | **Type:** Parquet | **Shape:** 121,123 rows × 3 columns

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

## issue_dates.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/issue_dates.parquet`
**Size:** 28638 bytes | **Type:** Parquet | **Shape:** 1,014 rows × 3 columns

### Columns
```
totalTendered                            Float64        
totalAccepted                            Float64        
issueDate                                Datetime(time_unit='ns', time_zone=None)
```

### Numeric Column Statistics
```
totalTendered: min=0.0, max=566665759500.0, mean=138791817700.39, median=78702920500.0
totalAccepted: min=0.0, max=255492688300.0, mean=56627258666.07, median=34664402000.0
```

### Date/Datetime Column Statistics
```
issueDate: min=1979-11-15 00:00:00, max=2025-08-15 00:00:00
```

---

## treasuries_with_run_status.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/treasuries_with_run_status.parquet`
**Size:** 1.2 MB | **Type:** Parquet | **Shape:** 2,437,981 rows × 5 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
run                                      Int64          
term                                     String         
type                                     String         
cusip                                    String         
```

### Numeric Column Statistics
```
run: min=0, max=84, mean=21.42, median=17.0
```

### Date/Datetime Column Statistics
```
date: min=1979-11-15 00:00:00, max=2025-08-04 00:00:00
```

---

## ftsfr_CRSP_monthly_stock_ret.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_ret.parquet`
**Size:** 21.6 MB | **Type:** Parquet | **Shape:** 3,826,457 rows × 3 columns

### Columns
```
unique_id                                Int64          
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64         (0.4% null)
```

### Numeric Column Statistics
```
unique_id: min=10000, max=93436, mean=49674.72, median=48215.0
y: min=-1.0, max=26.583827, mean=0.01, median=0.0
```

### Date/Datetime Column Statistics
```
ds: min=1925-12-31 00:00:00, max=2024-12-31 00:00:00
```

---

## ftsfr_CRSP_monthly_stock_retx.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_retx.parquet`
**Size:** 18.3 MB | **Type:** Parquet | **Shape:** 3,826,457 rows × 3 columns

### Columns
```
unique_id                                Int64          
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64         (0.4% null)
```

### Numeric Column Statistics
```
unique_id: min=10000, max=93436, mean=49674.72, median=48215.0
y: min=-1.0, max=26.583827, mean=0.01, median=0.0
```

### Date/Datetime Column Statistics
```
ds: min=1925-12-31 00:00:00, max=2024-12-31 00:00:00
```

---

## clean_1970_2008_commodities_data.csv
**Path:** `src/futures_returns/clean_1970_2008_commodities_data.csv`
**Size:** 52.7 MB | **Type:** Csv | **Shape:** 1,489,401 rows × 5 columns

### Columns
```
Date                                     String         
Commodity                                String         
Contract                                 Int64          
ClosePrice                               Float64        
YearMonth                                String         
```

### Numeric Column Statistics
```
Contract: min=1, max=12, mean=4.90, median=5.0
ClosePrice: min=0.14, max=85419.0625, mean=921.31, median=194.006
```

---

## clean_2009_2024_commodities_data.csv
**Path:** `src/futures_returns/clean_2009_2024_commodities_data.csv`
**Size:** 34.8 MB | **Type:** Csv | **Shape:** 982,950 rows × 5 columns

### Columns
```
Date                                     String         
Commodity                                String         
Contract                                 Int64          
ClosePrice                               Float64        
YearMonth                                String         
```

### Numeric Column Statistics
```
Contract: min=1, max=12, mean=5.95, median=6.0
ClosePrice: min=-38.42, max=6884.0, mean=570.32, median=242.69
```

---

## commodities_data.csv
**Path:** `src/futures_returns/commodities_data.csv`
**Size:** 71.1 MB | **Type:** Csv | **Shape:** 2,566,132 rows × 4 columns

### Columns
```
Commodity                                String         
Contract                                 Int64          
Date                                     String         
PX_LAST                                  Float64        
```

### Numeric Column Statistics
```
Contract: min=1, max=12, mean=5.32, median=5.0
PX_LAST: min=-38.42, max=85419.0625, mean=810.87, median=219.69
```

---

## commodity_futures.parquet
**Path:** `src/futures_returns/commodity_futures.parquet`
**Size:** 2.4 MB | **Type:** Parquet | **Shape:** 16,858 rows × 58 columns

### Columns
```
index                                    Date           
CO1 Comdty_PX_LAST                       Float64         (43.9% null)
CO2 Comdty_PX_LAST                       Float64         (43.8% null)
CO3 Comdty_PX_LAST                       Float64         (44.6% null)
QS1 Comdty_PX_LAST                       Float64         (45.4% null)
QS2 Comdty_PX_LAST                       Float64         (45.4% null)
QS3 Comdty_PX_LAST                       Float64         (45.4% null)
CL1 Comdty_PX_LAST                       Float64         (37.1% null)
CL2 Comdty_PX_LAST                       Float64         (37.0% null)
CL3 Comdty_PX_LAST                       Float64         (37.0% null)
XB1 Comdty_PX_LAST                       Float64         (70.5% null)
XB2 Comdty_PX_LAST                       Float64         (70.5% null)
XB3 Comdty_PX_LAST                       Float64         (70.5% null)
HO1 Comdty_PX_LAST                       Float64         (41.8% null)
HO2 Comdty_PX_LAST                       Float64         (41.8% null)
HO3 Comdty_PX_LAST                       Float64         (41.8% null)
NG1 Comdty_PX_LAST                       Float64         (47.5% null)
NG2 Comdty_PX_LAST                       Float64         (47.4% null)
NG3 Comdty_PX_LAST                       Float64         (47.4% null)
CT1 Comdty_PX_LAST                       Float64         (1.7% null)
CT2 Comdty_PX_LAST                       Float64         (1.6% null)
CT3 Comdty_PX_LAST                       Float64         (2.0% null)
KC1 Comdty_PX_LAST                       Float64         (22.2% null)
KC2 Comdty_PX_LAST                       Float64         (21.4% null)
KC3 Comdty_PX_LAST                       Float64         (21.5% null)
CC1 Comdty_PX_LAST                       Float64         (2.9% null)
CC2 Comdty_PX_LAST                       Float64         (2.3% null)
CC3 Comdty_PX_LAST                       Float64         (2.3% null)
SB1 Comdty_PX_LAST                       Float64         (4.3% null)
SB2 Comdty_PX_LAST                       Float64         (4.3% null)
SB3 Comdty_PX_LAST                       Float64         (4.6% null)
S 1 Comdty_PX_LAST                       Float64         (1.4% null)
S 2 Comdty_PX_LAST                       Float64         (1.4% null)
S 3 Comdty_PX_LAST                       Float64         (1.4% null)
KW1 Comdty_PX_LAST                       Float64         (17.1% null)
KW2 Comdty_PX_LAST                       Float64         (17.1% null)
KW3 Comdty_PX_LAST                       Float64         (17.1% null)
C 1 Comdty_PX_LAST                       Float64         (1.4% null)
C 2 Comdty_PX_LAST                       Float64         (1.3% null)
C 3 Comdty_PX_LAST                       Float64         (1.3% null)
W 1 Comdty_PX_LAST                       Float64         (1.4% null)
W 2 Comdty_PX_LAST                       Float64         (1.3% null)
W 3 Comdty_PX_LAST                       Float64         (1.3% null)
LH1 Comdty_PX_LAST                       Float64         (41.3% null)
LH2 Comdty_PX_LAST                       Float64         (41.4% null)
LH3 Comdty_PX_LAST                       Float64         (41.5% null)
FC1 Comdty_PX_LAST                       Float64         (20.2% null)
FC2 Comdty_PX_LAST                       Float64         (19.9% null)
FC3 Comdty_PX_LAST                       Float64         (20.1% null)
LC1 Comdty_PX_LAST                       Float64         (9.4% null)
LC2 Comdty_PX_LAST                       Float64         (9.4% null)
LC3 Comdty_PX_LAST                       Float64         (9.4% null)
GC1 Comdty_PX_LAST                       Float64         (25.1% null)
GC2 Comdty_PX_LAST                       Float64         (24.7% null)
GC3 Comdty_PX_LAST                       Float64         (24.7% null)
SI1 Comdty_PX_LAST                       Float64         (24.9% null)
SI2 Comdty_PX_LAST                       Float64         (24.7% null)
SI3 Comdty_PX_LAST                       Float64         (24.7% null)
```

### Numeric Column Statistics
```
CO1 Comdty_PX_LAST: min=9.64, max=146.08, mean=52.14, median=48.44
CO2 Comdty_PX_LAST: min=9.91, max=146.6, mean=52.03, median=49.05
CO3 Comdty_PX_LAST: min=10.16, max=147.05, mean=52.43, median=50.33
QS1 Comdty_PX_LAST: min=91.25, max=1522.5, mean=476.38, median=455.5
QS2 Comdty_PX_LAST: min=92.25, max=1333.75, mean=474.58, median=458.0
QS3 Comdty_PX_LAST: min=94.25, max=1340.5, mean=473.45, median=460.75
CL1 Comdty_PX_LAST: min=-37.63, max=145.29, mean=46.78, median=35.78
CL2 Comdty_PX_LAST: min=10.54, max=145.86, mean=46.76, median=35.035
CL3 Comdty_PX_LAST: min=10.58, max=146.13, mean=46.73, median=34.49
XB1 Comdty_PX_LAST: min=41.18, max=427.62, mean=214.31, median=209.345
XB2 Comdty_PX_LAST: min=49.47, max=408.39, mean=213.22, median=207.835
XB3 Comdty_PX_LAST: min=54.75, max=389.16, mean=212.27, median=206.685
HO1 Comdty_PX_LAST: min=29.52, max=513.54, mean=147.06, median=129.47
HO2 Comdty_PX_LAST: min=30.11, max=441.81, mean=146.73, median=129.8
HO3 Comdty_PX_LAST: min=30.76, max=430.21, mean=146.54, median=130.0
NG1 Comdty_PX_LAST: min=1.046, max=15.378, mean=3.73, median=2.959
NG2 Comdty_PX_LAST: min=1.1, max=15.427, mean=3.81, median=3.018
NG3 Comdty_PX_LAST: min=1.125, max=15.287, mean=3.87, median=3.084
CT1 Comdty_PX_LAST: min=20.8, max=215.15, mean=61.57, median=63.0
CT2 Comdty_PX_LAST: min=21.28, max=214.14, mean=61.60, median=63.625
CT3 Comdty_PX_LAST: min=21.33, max=203.97, mean=61.63, median=64.15
KC1 Comdty_PX_LAST: min=41.5, max=438.9, mean=132.44, median=125.55
KC2 Comdty_PX_LAST: min=45.15, max=425.1, mean=132.39, median=125.85
KC3 Comdty_PX_LAST: min=46.7, max=408.2, mean=132.86, median=126.0
CC1 Comdty_PX_LAST: min=211.0, max=12565.0, mean=1872.48, median=1596.0
CC2 Comdty_PX_LAST: min=220.0, max=11904.0, mean=1860.13, median=1603.0
CC3 Comdty_PX_LAST: min=229.0, max=11279.0, mean=1854.69, median=1615.0
SB1 Comdty_PX_LAST: min=1.25, max=65.2, mean=11.52, median=10.15
SB2 Comdty_PX_LAST: min=1.3, max=63.44, mean=11.54, median=10.19
SB3 Comdty_PX_LAST: min=1.34, max=60.05, mean=11.49, median=10.18
S 1 Comdty_PX_LAST: min=204.5, max=1771.0, mean=701.46, median=623.25
S 2 Comdty_PX_LAST: min=208.0, max=1768.25, mean=701.28, median=627.75
S 3 Comdty_PX_LAST: min=207.25, max=1766.25, mean=699.65, median=631.0
KW1 Comdty_PX_LAST: min=128.0, max=1367.75, mean=440.36, median=397.75
KW2 Comdty_PX_LAST: min=130.125, max=1369.25, mean=444.01, median=397.0
KW3 Comdty_PX_LAST: min=131.75, max=1370.0, mean=446.87, median=395.0
C 1 Comdty_PX_LAST: min=100.875, max=831.25, mean=289.81, median=259.25
C 2 Comdty_PX_LAST: min=102.5, max=838.75, mean=292.81, median=262.25
C 3 Comdty_PX_LAST: min=107.375, max=837.75, mean=295.33, median=264.25
W 1 Comdty_PX_LAST: min=114.25, max=1425.25, mean=385.80, median=354.25
W 2 Comdty_PX_LAST: min=119.625, max=1294.0, mean=391.57, median=356.0
W 3 Comdty_PX_LAST: min=125.5, max=1279.0, mean=394.93, median=355.25
LH1 Comdty_PX_LAST: min=21.1, max=133.875, mean=65.06, median=62.15
LH2 Comdty_PX_LAST: min=28.075, max=132.825, mean=65.91, median=64.35
LH3 Comdty_PX_LAST: min=33.875, max=133.0, mean=67.08, median=66.05
FC1 Comdty_PX_LAST: min=25.5, max=313.15, mean=101.50, median=84.45
FC2 Comdty_PX_LAST: min=26.85, max=312.75, mean=101.60, median=83.925
FC3 Comdty_PX_LAST: min=26.6, max=310.55, mean=102.00, median=83.8
LC1 Comdty_PX_LAST: min=22.95, max=228.2, mean=79.36, median=71.375
LC2 Comdty_PX_LAST: min=23.0, max=219.25, mean=79.23, median=70.775
LC3 Comdty_PX_LAST: min=23.325, max=215.875, mean=79.33, median=70.8
GC1 Comdty_PX_LAST: min=102.4, max=3431.2, mean=767.51, median=417.4
GC2 Comdty_PX_LAST: min=102.7, max=3452.8, mean=769.45, median=421.5
GC3 Comdty_PX_LAST: min=103.1, max=3480.5, mean=774.09, median=426.65
SI1 Comdty_PX_LAST: min=3.51, max=48.584, mean=11.96, median=7.575
SI2 Comdty_PX_LAST: min=3.55, max=48.599, mean=12.05, median=7.6835
SI3 Comdty_PX_LAST: min=3.573, max=48.609, mean=12.15, median=7.804
```

### Date/Datetime Column Statistics
```
index: min=1959-07-01, max=2025-07-03
```

---

## filtered_info.csv
**Path:** `src/futures_returns/filtered_info.csv`
**Size:** 458045 bytes | **Type:** Csv | **Shape:** 3,427 rows × 13 columns

### Columns
```
                                         Int64          
calcseriescode                           Int64          
clscode                                  Int64          
dsmnem                                   String         
calcseriesname                           String         
isocurrcode                              String         
isocurrdesc                              String         
rollmethodcode                           Int64          
rollmethoddesc                           String         
positionfwdcode                          Int64          
positionfwddesc                          String         
calcmthcode                              String         
trdmonths                                String          (98.3% null)
```

### Numeric Column Statistics
```
: min=7, max=29578, mean=16597.36, median=17813.0
calcseriescode: min=8, max=29995, mean=16660.16, median=17836.0
clscode: min=2, max=4812, mean=2358.46, median=2403.0
rollmethodcode: min=0, max=1, mean=0.51, median=1.0
positionfwdcode: min=0, max=9, mean=0.91, median=0.0
```

---

## gsci_indices.parquet
**Path:** `src/futures_returns/gsci_indices.parquet`
**Size:** 2.0 MB | **Type:** Parquet | **Shape:** 15,272 rows × 25 columns

### Columns
```
index                                    Date           
SPGCBRP Index_PX_LAST                    Float64         (56.4% null)
SPGCGOP Index_PX_LAST                    Float64         (56.4% null)
SPGCCLP Index_PX_LAST                    Float64         (36.5% null)
SPGCHUP Index_PX_LAST                    Float64         (38.2% null)
SPGCHOP Index_PX_LAST                    Float64         (29.9% null)
SPGCNGP Index_PX_LAST                    Float64         (48.1% null)
SPGCCTP Index_PX_LAST                    Float64         (20.0% null)
SPGCKCP Index_PX_LAST                    Float64         (26.6% null)
SPGCCCP Index_PX_LAST                    Float64         (31.5% null)
SPGCSBP Index_PX_LAST                    Float64         (13.4% null)
SPGCSOP Index_PX_LAST                    Float64         (8.4% null)
SPGCKWP Index_PX_LAST                    Float64         (56.4% null)
SPGCCNP Index_PX_LAST                    Float64         (8.4% null)
SPGCWHP Index_PX_LAST                    Float64         (8.4% null)
SPGCLHP Index_PX_LAST                    Float64         (18.3% null)
SPGCFCP Index_PX_LAST                    Float64         (61.3% null)
SPGCLCP Index_PX_LAST                    Float64         (8.4% null)
SPGCGCP Index_PX_LAST                    Float64         (21.6% null)
SPGCSIP Index_PX_LAST                    Float64         (13.4% null)
SPGCIAP Index_PX_LAST                    Float64         (43.1% null)
SPGCIKP Index_PX_LAST                    Float64         (46.5% null)
SPGCILP Index_PX_LAST                    Float64         (49.8% null)
SPGCIZP Index_PX_LAST                    Float64         (43.1% null)
SPGCICP Index_PX_LAST                    Float64         (20.0% null)
```

### Numeric Column Statistics
```
SPGCBRP Index_PX_LAST: min=85.0295, max=1574.401, mean=535.02, median=514.5391500000001
SPGCGOP Index_PX_LAST: min=83.9114, max=1394.014, mean=475.62, median=459.79895
SPGCCLP Index_PX_LAST: min=26.951, max=1818.372, mean=373.76, median=239.3859
SPGCHUP Index_PX_LAST: min=92.861, max=2548.616, mean=905.51, median=861.777
SPGCHOP Index_PX_LAST: min=64.8596, max=785.5128, mean=241.62, median=204.8156
SPGCNGP Index_PX_LAST: min=1.38733, max=12860.73, mean=1654.48, median=140.5376
SPGCCTP Index_PX_LAST: min=20.0144, max=337.9354, mean=97.02, median=74.5711
SPGCKCP Index_PX_LAST: min=5.81163, max=371.3201, mean=65.97, median=33.93933
SPGCCCP Index_PX_LAST: min=4.05504, max=108.1477, mean=21.54, median=11.501085
SPGCSBP Index_PX_LAST: min=6.30204, max=1328.392, mean=57.00, median=18.565269999999998
SPGCSOP Index_PX_LAST: min=99.7519, max=714.491, mean=309.81, median=281.5665
SPGCKWP Index_PX_LAST: min=10.86842, max=140.7057, mean=42.85, median=46.5597
SPGCCNP Index_PX_LAST: min=4.560629, max=331.9445, mean=71.85, median=53.25036
SPGCWHP Index_PX_LAST: min=4.09038, max=645.9026, mean=111.92, median=103.99674999999999
SPGCLHP Index_PX_LAST: min=6.12682, max=425.417, mean=133.16, median=117.48205
SPGCFCP Index_PX_LAST: min=80.03, max=158.5639, mean=110.96, median=108.9892
SPGCLCP Index_PX_LAST: min=95.9177, max=686.5271, mean=360.99, median=348.52795000000003
SPGCGCP Index_PX_LAST: min=28.9087, max=398.9086, mean=93.53, median=91.2284
SPGCSIP Index_PX_LAST: min=21.98021, max=1154.509, mean=96.84, median=69.09691
SPGCIAP Index_PX_LAST: min=18.71784, max=100.0, mean=45.39, median=42.8971
SPGCIKP Index_PX_LAST: min=42.8746, max=844.8805, mean=195.91, median=177.1975
SPGCILP Index_PX_LAST: min=39.7621, max=461.1942, mean=156.97, median=172.1947
SPGCIZP Index_PX_LAST: min=29.4915, max=151.1885, mean=62.96, median=60.65394
SPGCICP Index_PX_LAST: min=33.3476, max=918.4696, mean=325.40, median=174.1641
```

### Date/Datetime Column Statistics
```
index: min=1964-11-30, max=2025-06-23
```

---

## raw_data.csv
**Path:** `src/futures_returns/raw_data.csv`
**Size:** 576624 bytes | **Type:** Csv | **Shape:** 13,982 rows × 6 columns

### Columns
```
                                         Int64          
index                                    String         
KW1 Comdty_PX_LAST                       Float64         (0.1% null)
KW2 Comdty_PX_LAST                       Float64         (0.1% null)
KW3 Comdty_PX_LAST                       Float64         (0.1% null)
SI3 Comdty_PX_LAST                       String          (9.2% null)
```

### Numeric Column Statistics
```
: min=0, max=13981, mean=6990.50, median=6990.5
KW1 Comdty_PX_LAST: min=128.0, max=1367.75, mean=440.32, median=397.5
KW2 Comdty_PX_LAST: min=130.125, max=1369.25, mean=443.96, median=396.75
KW3 Comdty_PX_LAST: min=131.75, max=1370.0, mean=446.81, median=395.0
```