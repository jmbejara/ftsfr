# Data Glimpses Report
Generated: 2025-06-19 20:03:11
Total files: 15

## Summary of Datasets by Task

### Assemble Results
- [`arima_results.csv`](#arima-results-csv)
- [`simple_exponential_smoothing_results.csv`](#simple-exponential-smoothing-results-csv)
- [`results_all.csv`](#results-all-csv)

### Forecast
#### Forecast: Arima
- [`arima_results.csv`](#arima-results-csv)
#### Forecast: Simple Exponential Smoothing
- [`simple_exponential_smoothing_results.csv`](#simple-exponential-smoothing-results-csv)

### Format
#### Format: Calc Cds Returns
- [`markit_cds_returns.parquet`](#markit-cds-returns-parquet)
#### Format: Cds Bond Basis
- [`Final_data.parquet`](#final-data-parquet)
- [`Red_Data.parquet`](#red-data-parquet)
#### Format: Corp Bond Returns
- [`corp_bond_portfolio_returns.parquet`](#corp-bond-portfolio-returns-parquet)
#### Format: Fed Yield Curve
- [`ftsfr_treas_yield_curve_zero_coupon.parquet`](#ftsfr-treas-yield-curve-zero-coupon-parquet)
#### Format: Futures Returns
- [`futures_returns.parquet`](#futures-returns-parquet)
#### Format: Nyu Call Report
- [`ftsfr_nyu_call_report_cash_liquidity.parquet`](#ftsfr-nyu-call-report-cash-liquidity-parquet)
- [`ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet`](#ftsfr-nyu-call-report-holding-company-cash-liquidity-parquet)
- [`ftsfr_nyu_call_report_holding_company_leverage.parquet`](#ftsfr-nyu-call-report-holding-company-leverage-parquet)
- [`ftsfr_nyu_call_report_leverage.parquet`](#ftsfr-nyu-call-report-leverage-parquet)
#### Format: Wrds Crsp Compustat
- [`ftsfr_CRSP_monthly_stock_ret.parquet`](#ftsfr-crsp-monthly-stock-ret-parquet)
- [`ftsfr_CRSP_monthly_stock_retx.parquet`](#ftsfr-crsp-monthly-stock-retx-parquet)

---

## Final_data.parquet
**Path:** `/Users/arshkumar/JB/ftsfr/_data/cds_bond_basis/Final_data.parquet`
**Size:** 1038295 bytes | **Type:** Parquet | **Shape:** 28,667 rows × 9 columns

### Columns
```
cusip                                    String         
date                                     Datetime(time_unit='ns', time_zone=None)
mat_days                                 Float64         (6.9% null)
BOND_YIELD                               Float64         (11.6% null)
CS                                       Float64         (11.6% null)
size_ig                                  Float64         (6.9% null)
size_jk                                  Float64         (6.9% null)
par_spread                               Float64         (6.9% null)
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
mat_days: min=363.0, max=36516.0, mean=3856.70, median=2513.0
BOND_YIELD: min=-0.2148487372494935, max=0.9514264593127048, mean=0.05, median=0.0464350605010986
CS: min=-0.2350270544393278, max=0.9440691614682412, mean=0.02, median=0.01965415518558645
size_ig: min=0.0, max=1.0, mean=0.76, median=1.0
size_jk: min=0.0, max=1.0, mean=0.98, median=1.0
par_spread: min=-13.051245732738076, max=45.110770582488456, mean=0.11, median=0.010004951771566519
__index_level_0__: min=10402, max=1391541, mean=689134.38, median=699949.0
```

---

## Red_Data.parquet
**Path:** `/Users/arshkumar/JB/ftsfr/_data/cds_bond_basis/Red_Data.parquet`
**Size:** 20.2 MB | **Type:** Parquet | **Shape:** 1,392,507 rows × 9 columns

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
BOND_YIELD: min=-0.79189766622368, max=24.42611933726512, mean=0.05, median=0.04342172670364375
CS: min=-0.8427172227775009, max=24.41471933726512, mean=0.03, median=0.01700886045541
size_ig: min=0.0, max=1.0, mean=0.82, median=1.0
size_jk: min=0.0, max=1.0, mean=0.98, median=1.0
mat_days: min=360.99999999999994, max=36525.0, mean=3766.73, median=2480.0
```

---

## markit_cds_returns.parquet
**Path:** `/Users/arshkumar/JB/ftsfr/_data/cds_returns/markit_cds_returns.parquet`
**Size:** 50616 bytes | **Type:** Parquet | **Shape:** 276 rows × 21 columns

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
3Y_Q1: min=5.371658264298698e-05, max=0.0012984858902217822, mean=0.00, median=0.00017827402150010982
3Y_Q2: min=9.870136573632674e-05, max=0.0017586072397138203, mean=0.00, median=0.0003031592445867868
3Y_Q3: min=0.0001684337421296743, max=0.0028413166686972933, mean=0.00, median=0.0004832672363692339
3Y_Q4: min=0.00035449081199087363, max=0.008636568917665144, mean=0.00, median=0.0008245199654941964
3Y_Q5: min=0.0010295466088669554, max=0.017052373909298535, mean=0.00, median=0.003330403181429091
5Y_Q1: min=8.237507062114348e-05, max=0.001342001238430868, mean=0.00, median=0.0002795825488220994
5Y_Q2: min=0.00016613549989386023, max=0.0015301593893626286, mean=0.00, median=0.0005015117039972594
5Y_Q3: min=0.0002442534777740146, max=0.0029902068025779993, mean=0.00, median=0.0007583209877857211
5Y_Q4: min=0.0006771152212967646, max=0.008650813007283542, mean=0.00, median=0.0013491719925552426
5Y_Q5: min=0.0018247947084999439, max=0.01831490376557743, mean=0.01, median=0.004605743110627891
7Y_Q1: min=0.00010966558944852241, max=0.001394881201460759, mean=0.00, median=0.0003598823070267437
7Y_Q2: min=8.177990832986773e-05, max=0.0015258687452614184, mean=0.00, median=0.0006690495790859072
7Y_Q3: min=0.00012346564089683233, max=0.0030800321218594825, mean=0.00, median=0.000997375101844041
7Y_Q4: min=0.001104650859692401, max=0.0072038950370688325, mean=0.00, median=0.002064188069841373
7Y_Q5: min=0.0024360601323442227, max=0.019000003641099567, mean=0.01, median=0.0054535075210321565
10Y_Q1: min=0.00013486972984516672, max=0.0009096632123143637, mean=0.00, median=0.00048197729080199075
10Y_Q2: min=7.051907297346936e-05, max=0.0014944988988713271, mean=0.00, median=0.0007534827745877545
10Y_Q3: min=0.00014061917113890177, max=0.0031503081603452675, mean=0.00, median=0.0011654253088051035
10Y_Q4: min=0.0013590671509860206, max=0.007458313744444359, mean=0.00, median=0.0023217931990416408
10Y_Q5: min=0.0030394362001676897, max=0.019333984161258262, mean=0.01, median=0.006115734817777269
```

---

## corp_bond_portfolio_returns.parquet
**Path:** `/Users/arshkumar/JB/ftsfr/_data/corp_bond_returns/corp_bond_portfolio_returns.parquet`
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

---

## ftsfr_treas_yield_curve_zero_coupon.parquet
**Path:** `/Users/arshkumar/JB/ftsfr/_data/fed_yield_curve/ftsfr_treas_yield_curve_zero_coupon.parquet`
**Size:** 3.6 MB | **Type:** Parquet | **Shape:** 500,640 rows × 3 columns

### Columns
```
entity                                   String         
date                                     Datetime(time_unit='ns', time_zone=None)
value                                    Float64         (25.7% null)
```

### Numeric Column Statistics
```
value: min=0.0554, max=16.462, mean=5.61, median=5.3232729844415
```

---

## futures_returns.parquet
**Path:** `/Users/arshkumar/JB/ftsfr/_data/futures_returns/futures_returns.parquet`
**Size:** 18.2 MB | **Type:** Parquet | **Shape:** 4,921,751 rows × 5 columns

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
futcode: min=37.0, max=487137.0, mean=204053.20, median=180720.0
settlement: min=-37.630005, max=24480.0, mean=591.56, median=59.699997
product_code: min=289, max=3847, mean=2121.62, median=2060.0
```

---

## ftsfr_nyu_call_report_cash_liquidity.parquet
**Path:** `/Users/arshkumar/JB/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_cash_liquidity.parquet`
**Size:** 15.5 MB | **Type:** Parquet | **Shape:** 1,919,810 rows × 3 columns

### Columns
```
entity                                   String         
date                                     Datetime(time_unit='ns', time_zone=None)
value                                    Float64         (0.6% null)
```

### Numeric Column Statistics
```
value: min=-0.004637848248033172, max=inf, mean=inf, median=0.05778003041054232
```

---

## ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet
**Path:** `/Users/arshkumar/JB/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet`
**Size:** 15.4 MB | **Type:** Parquet | **Shape:** 1,919,810 rows × 3 columns

### Columns
```
entity                                   String          (0.0% null)
date                                     Datetime(time_unit='ns', time_zone=None)
value                                    Float64         (0.6% null)
```

### Numeric Column Statistics
```
value: min=-0.004637848248033172, max=inf, mean=inf, median=0.05778003041054232
```

---

## ftsfr_nyu_call_report_holding_company_leverage.parquet
**Path:** `/Users/arshkumar/JB/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_holding_company_leverage.parquet`
**Size:** 6.8 MB | **Type:** Parquet | **Shape:** 833,187 rows × 3 columns

### Columns
```
entity                                   String         
date                                     Datetime(time_unit='ns', time_zone=None)
value                                    Float64         (0.0% null)
```

### Numeric Column Statistics
```
value: min=-61371.42307692308, max=inf, mean=inf, median=10.980478367317396
```

---

## ftsfr_nyu_call_report_leverage.parquet
**Path:** `/Users/arshkumar/JB/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_leverage.parquet`
**Size:** 15.1 MB | **Type:** Parquet | **Shape:** 1,919,810 rows × 3 columns

### Columns
```
entity                                   String         
date                                     Datetime(time_unit='ns', time_zone=None)
value                                    Float64         (3.3% null)
```

### Numeric Column Statistics
```
value: min=-61371.42307692308, max=inf, mean=inf, median=11.125577574699662
```

---

## ftsfr_CRSP_monthly_stock_ret.parquet
**Path:** `/Users/arshkumar/JB/ftsfr/_data/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_ret.parquet`
**Size:** 37.3 MB | **Type:** Parquet | **Shape:** 3,826,457 rows × 4 columns

### Columns
```
entity                                   Int64          
date                                     Datetime(time_unit='ns', time_zone=None)
value                                    Float64         (0.4% null)
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
entity: min=10000, max=93436, mean=49674.72, median=48215.0
value: min=-1.0, max=26.583827, mean=0.01, median=0.0
__index_level_0__: min=0, max=499999, mean=246934.99, median=247938.0
```

---

## ftsfr_CRSP_monthly_stock_retx.parquet
**Path:** `/Users/arshkumar/JB/ftsfr/_data/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_retx.parquet`
**Size:** 33.9 MB | **Type:** Parquet | **Shape:** 3,826,457 rows × 4 columns

### Columns
```
entity                                   Int64          
date                                     Datetime(time_unit='ns', time_zone=None)
value                                    Float64         (0.4% null)
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
entity: min=10000, max=93436, mean=49674.72, median=48215.0
value: min=-1.0, max=26.583827, mean=0.01, median=0.0
__index_level_0__: min=0, max=499999, mean=246934.99, median=247938.0
```

---

## arima_results.csv
**Path:** `/Users/arshkumar/JB/ftsfr/_output/raw_results/arima_results.csv`
**Size:** 108 bytes | **Type:** Csv | **Shape:** 1 rows × 5 columns

### Columns
```
model                                    String         
seasonality                              Int64          
mean_mase                                Float64        
median_mase                              Float64        
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=5, max=5, mean=5.00, median=5.0
mean_mase: min=9.83930260256351, max=9.83930260256351, mean=9.84, median=9.83930260256351
median_mase: min=9.485053711101472, max=9.485053711101472, mean=9.49, median=9.485053711101472
entity_count: min=30, max=30, mean=30.00, median=30.0
```

---

## simple_exponential_smoothing_results.csv
**Path:** `/Users/arshkumar/JB/ftsfr/_output/raw_results/simple_exponential_smoothing_results.csv`
**Size:** 133 bytes | **Type:** Csv | **Shape:** 1 rows × 5 columns

### Columns
```
model                                    String         
seasonality                              Int64          
mean_mase                                Float64        
median_mase                              Float64        
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=5, max=5, mean=5.00, median=5.0
mean_mase: min=9.80730049361067, max=9.80730049361067, mean=9.81, median=9.80730049361067
median_mase: min=9.47550110922832, max=9.47550110922832, mean=9.48, median=9.47550110922832
entity_count: min=30, max=30, mean=30.00, median=30.0
```

---

## results_all.csv
**Path:** `/Users/arshkumar/JB/ftsfr/_output/results_all.csv`
**Size:** 176 bytes | **Type:** Csv | **Shape:** 2 rows × 5 columns

### Columns
```
model                                    String         
seasonality                              Int64          
mean_mase                                Float64        
median_mase                              Float64        
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=5, max=5, mean=5.00, median=5.0
mean_mase: min=9.80730049361067, max=9.83930260256351, mean=9.82, median=9.823301548087091
median_mase: min=9.47550110922832, max=9.485053711101472, mean=9.48, median=9.480277410164895
entity_count: min=30, max=30, mean=30.00, median=30.0
```