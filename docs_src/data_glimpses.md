# Data Glimpses Report
Generated: 2025-07-10 16:42:26
Total files: 19

## Summary of Datasets by Task

### Assemble Results
- [`arima_results.csv`](#arima-results-csv)
- [`simple_exponential_smoothing_results.csv`](#simple-exponential-smoothing-results-csv)
- [`results_all.csv`](#results-all-csv)

### Create Data Glimpses
- [`filtered_info.csv`](#filtered-info-csv)

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
#### Format: Cip
- [`cip_spreads.parquet`](#cip-spreads-parquet)
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
#### Format: Us Treasury Returns
- [`issue_dates.parquet`](#issue-dates-parquet)
- [`treasuries_with_run_status.parquet`](#treasuries-with-run-status-parquet)
#### Format: Wrds Crsp Compustat
- [`ftsfr_CRSP_monthly_stock_ret.parquet`](#ftsfr-crsp-monthly-stock-ret-parquet)
- [`ftsfr_CRSP_monthly_stock_retx.parquet`](#ftsfr-crsp-monthly-stock-retx-parquet)

---

## Final_data.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/Final_data.parquet`
**Size:** 18.7 MB | **Type:** Parquet | **Shape:** 653,228 rows × 9 columns

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
mat_days: min=360.99999999999994, max=36525.0, mean=3796.94, median=2462.0
BOND_YIELD: min=-0.79189766622368, max=11.679347680642085, mean=0.05, median=0.0419370446205139
CS: min=-0.8427172227775009, max=11.666247680642083, mean=0.02, median=0.0160909154748749
size_ig: min=0.0, max=1.0, mean=0.82, median=1.0
size_jk: min=0.0, max=1.0, mean=0.98, median=1.0
par_spread: min=-277.079498250281, max=1307.7831991672729, mean=0.06, median=0.0075589020693470985
__index_level_0__: min=39, max=1392383, mean=692416.28, median=696029.0
```

---

## Red_Data.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/Red_Data.parquet`
**Size:** 20.2 MB | **Type:** Parquet | **Shape:** 1,392,870 rows × 9 columns

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
BOND_YIELD: min=-0.79189766622368, max=24.42611933726512, mean=0.05, median=0.0434166188240051
CS: min=-0.8427172227775009, max=24.41471933726512, mean=0.03, median=0.0170097161030346
size_ig: min=0.0, max=1.0, mean=0.82, median=1.0
size_jk: min=0.0, max=1.0, mean=0.98, median=1.0
mat_days: min=360.99999999999994, max=36525.0, mean=3766.07, median=2480.0
```

---

## markit_cds_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_returns/markit_cds_returns.parquet`
**Size:** 50612 bytes | **Type:** Parquet | **Shape:** 276 rows × 21 columns

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
3Y_Q1: min=5.389689731366252e-05, max=0.0012972343600382446, mean=0.00, median=0.00017837457365309987
3Y_Q2: min=9.771449867174918e-05, max=0.001757310815728772, mean=0.00, median=0.0003011161215830114
3Y_Q3: min=0.00016913607602179957, max=0.0028324389890417175, mean=0.00, median=0.000485779349839776
3Y_Q4: min=0.00035288472820092955, max=0.008641248005009428, mean=0.00, median=0.0008268060284415124
3Y_Q5: min=0.0010272207148105958, max=0.017051761117074984, mean=0.00, median=0.003333183248464348
5Y_Q1: min=8.275439968574716e-05, max=0.0013420012384308677, mean=0.00, median=0.0002781480228990496
5Y_Q2: min=0.00016537177377839998, max=0.001530159389362629, mean=0.00, median=0.000501261859826796
5Y_Q3: min=0.0002442534777740146, max=0.0029820907585587086, mean=0.00, median=0.0007583209877857211
5Y_Q4: min=0.0006704490162541266, max=0.008650813007283542, mean=0.00, median=0.0013628831500126504
5Y_Q5: min=0.0018230444667404195, max=0.018314903765577425, mean=0.01, median=0.004595504716873754
7Y_Q1: min=0.00010966962933265006, max=0.0013949325863888305, mean=0.00, median=0.0003618103806222818
7Y_Q2: min=8.184532729079774e-05, max=0.001531432278264998, mean=0.00, median=0.0006683869286375066
7Y_Q3: min=0.0001235477998526692, max=0.003074855495910384, mean=0.00, median=0.000995591729802539
7Y_Q4: min=0.0010978498635662321, max=0.007197178253333162, mean=0.00, median=0.0020605433190841304
7Y_Q5: min=0.0024328731886759884, max=0.01900305868243827, mean=0.01, median=0.005422328703091937
10Y_Q1: min=0.0001350211969086215, max=0.0009063400972020281, mean=0.00, median=0.0004824748535625107
10Y_Q2: min=7.05582757313702e-05, max=0.0015004388490293034, mean=0.00, median=0.0007531659859585654
10Y_Q3: min=0.0001407362718215997, max=0.003145879011273593, mean=0.00, median=0.0011662997146133626
10Y_Q4: min=0.001358972284302623, max=0.007451035992175151, mean=0.00, median=0.0023143766609362904
10Y_Q5: min=0.003034199956717164, max=0.019339084808444634, mean=0.01, median=0.006114826402134227
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

---

## ftsfr_treas_yield_curve_zero_coupon.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/fed_yield_curve/ftsfr_treas_yield_curve_zero_coupon.parquet`
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
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/futures_returns/futures_returns.parquet`
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
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_cash_liquidity.parquet`
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
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_holding_company_cash_liquidity.parquet`
**Size:** 6.8 MB | **Type:** Parquet | **Shape:** 833,010 rows × 3 columns

### Columns
```
entity                                   String         
date                                     Datetime(time_unit='ns', time_zone=None)
value                                    Float64         (0.0% null)
```

### Numeric Column Statistics
```
value: min=-0.0024056979902961173, max=0.9987931814753357, mean=0.07, median=0.051772243080015184
```

---

## ftsfr_nyu_call_report_holding_company_leverage.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_holding_company_leverage.parquet`
**Size:** 6.8 MB | **Type:** Parquet | **Shape:** 833,010 rows × 3 columns

### Columns
```
entity                                   String         
date                                     Datetime(time_unit='ns', time_zone=None)
value                                    Float64         (0.0% null)
```

### Numeric Column Statistics
```
value: min=-61371.42307692308, max=inf, mean=inf, median=10.979716024340771
```

---

## ftsfr_nyu_call_report_leverage.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_leverage.parquet`
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

## issue_dates.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/issue_dates.parquet`
**Size:** 28572 bytes | **Type:** Parquet | **Shape:** 1,011 rows × 3 columns

### Columns
```
totalTendered                            Float64        
totalAccepted                            Float64        
issueDate                                Datetime(time_unit='ns', time_zone=None)
```

### Numeric Column Statistics
```
totalTendered: min=0.0, max=566665759500.0, mean=137880865017.41, median=78532939000.0
totalAccepted: min=0.0, max=255492688300.0, mean=56243429773.29, median=34536730000.0
```

---

## treasuries_with_run_status.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/treasuries_with_run_status.parquet`
**Size:** 1.2 MB | **Type:** Parquet | **Shape:** 2,425,829 rows × 5 columns

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
run: min=0, max=84, mean=21.38, median=17.0
```

---

## ftsfr_CRSP_monthly_stock_ret.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_ret.parquet`
**Size:** 21.6 MB | **Type:** Parquet | **Shape:** 3,826,457 rows × 3 columns

### Columns
```
entity                                   Int64          
date                                     Datetime(time_unit='ns', time_zone=None)
value                                    Float64         (0.4% null)
```

### Numeric Column Statistics
```
entity: min=10000, max=93436, mean=49674.72, median=48215.0
value: min=-1.0, max=26.583827, mean=0.01, median=0.0
```

---

## ftsfr_CRSP_monthly_stock_retx.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_retx.parquet`
**Size:** 18.3 MB | **Type:** Parquet | **Shape:** 3,826,457 rows × 3 columns

### Columns
```
entity                                   Int64          
date                                     Datetime(time_unit='ns', time_zone=None)
value                                    Float64         (0.4% null)
```

### Numeric Column Statistics
```
entity: min=10000, max=93436, mean=49674.72, median=48215.0
value: min=-1.0, max=26.583827, mean=0.01, median=0.0
```

---

## arima_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/arima_results.csv`
**Size:** 100 bytes | **Type:** Csv | **Shape:** 1 rows × 5 columns

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
mean_mase: min=10.02251905522711, max=10.02251905522711, mean=10.02, median=10.02251905522711
median_mase: min=9.836494729603285, max=9.836494729603285, mean=9.84, median=9.836494729603285
entity_count: min=30, max=30, mean=30.00, median=30.0
```

---

## simple_exponential_smoothing_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/simple_exponential_smoothing_results.csv`
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
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/results_all.csv`
**Size:** 168 bytes | **Type:** Csv | **Shape:** 2 rows × 5 columns

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
mean_mase: min=9.80730049361067, max=10.02251905522711, mean=9.91, median=9.914909774418891
median_mase: min=9.47550110922832, max=9.836494729603285, mean=9.66, median=9.655997919415803
entity_count: min=30, max=30, mean=30.00, median=30.0
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