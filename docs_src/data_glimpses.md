# Data Glimpses Report
Generated: 2025-07-11 15:25:28
Total files: 31

## Summary of Datasets by Task

### Assemble Results
- [`results_all.csv`](#results-all-csv)

### Create Data Glimpses
- [`filtered_info.csv`](#filtered-info-csv)

### Forecast
#### Forecast: Arima:Crsp Monthly Stock Ret
- [`arima_CRSP_monthly_stock_ret_results.csv`](#arima-crsp-monthly-stock-ret-results-csv)
#### Forecast: Arima:Crsp Monthly Stock Retx
- [`arima_CRSP_monthly_stock_retx_results.csv`](#arima-crsp-monthly-stock-retx-results-csv)
#### Forecast: Arima:Nyu Call Report Cash Liquidity
- [`arima_nyu_call_report_cash_liquidity_results.csv`](#arima-nyu-call-report-cash-liquidity-results-csv)
#### Forecast: Arima:Nyu Call Report Holding Company Cash Liquidity
- [`arima_nyu_call_report_holding_company_cash_liquidity_results.csv`](#arima-nyu-call-report-holding-company-cash-liquidity-results-csv)
#### Forecast: Arima:Nyu Call Report Holding Company Leverage
- [`arima_nyu_call_report_holding_company_leverage_results.csv`](#arima-nyu-call-report-holding-company-leverage-results-csv)
#### Forecast: Arima:Nyu Call Report Leverage
- [`arima_nyu_call_report_leverage_results.csv`](#arima-nyu-call-report-leverage-results-csv)
#### Forecast: Arima:Treas Yield Curve Zero Coupon
- [`arima_treas_yield_curve_zero_coupon_results.csv`](#arima-treas-yield-curve-zero-coupon-results-csv)
#### Forecast: Simple Exponential Smoothing:Crsp Monthly Stock Ret
- [`simple_exponential_smoothing_CRSP_monthly_stock_ret_results.csv`](#simple-exponential-smoothing-crsp-monthly-stock-ret-results-csv)
#### Forecast: Simple Exponential Smoothing:Crsp Monthly Stock Retx
- [`simple_exponential_smoothing_CRSP_monthly_stock_retx_results.csv`](#simple-exponential-smoothing-crsp-monthly-stock-retx-results-csv)
#### Forecast: Simple Exponential Smoothing:Nyu Call Report Cash Liquidity
- [`simple_exponential_smoothing_nyu_call_report_cash_liquidity_results.csv`](#simple-exponential-smoothing-nyu-call-report-cash-liquidity-results-csv)
#### Forecast: Simple Exponential Smoothing:Nyu Call Report Holding Company Cash Liquidity
- [`simple_exponential_smoothing_nyu_call_report_holding_company_cash_liquidity_results.csv`](#simple-exponential-smoothing-nyu-call-report-holding-company-cash-liquidity-results-csv)
#### Forecast: Simple Exponential Smoothing:Nyu Call Report Holding Company Leverage
- [`simple_exponential_smoothing_nyu_call_report_holding_company_leverage_results.csv`](#simple-exponential-smoothing-nyu-call-report-holding-company-leverage-results-csv)
#### Forecast: Simple Exponential Smoothing:Nyu Call Report Leverage
- [`simple_exponential_smoothing_nyu_call_report_leverage_results.csv`](#simple-exponential-smoothing-nyu-call-report-leverage-results-csv)
#### Forecast: Simple Exponential Smoothing:Treas Yield Curve Zero Coupon
- [`simple_exponential_smoothing_treas_yield_curve_zero_coupon_results.csv`](#simple-exponential-smoothing-treas-yield-curve-zero-coupon-results-csv)

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

### Date/Datetime Column Statistics
```
date: min=2002-09-30 00:00:00, max=2022-09-30 00:00:00
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

### Date/Datetime Column Statistics
```
date: min=2002-08-31 00:00:00, max=2022-09-30 00:00:00
```

---

## markit_cds_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_returns/markit_cds_returns.parquet`
**Size:** 50535 bytes | **Type:** Parquet | **Shape:** 276 rows × 21 columns

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
3Y_Q1: min=5.363935700769991e-05, max=0.0012966191222173818, mean=0.00, median=0.00017742643235087478
3Y_Q2: min=9.768582355352707e-05, max=0.0017582343617051745, mean=0.00, median=0.00030060113250072876
3Y_Q3: min=0.0001692871827227437, max=0.00282193678620524, mean=0.00, median=0.000484803693926573
3Y_Q4: min=0.0003521369455619236, max=0.00863525009208177, mean=0.00, median=0.0008263675668610626
3Y_Q5: min=0.001026338082917369, max=0.01705520454748883, mean=0.00, median=0.0033080984744244825
5Y_Q1: min=8.237507062114346e-05, max=0.0013420012384308677, mean=0.00, median=0.0002781720715588909
5Y_Q2: min=0.00016524729187250561, max=0.0015301593893626284, mean=0.00, median=0.0005008729740653138
5Y_Q3: min=0.0002442534777740146, max=0.002971342162028545, mean=0.00, median=0.0007583209877857211
5Y_Q4: min=0.0006687052947333961, max=0.008650813007283544, mean=0.00, median=0.0013625318468836192
5Y_Q5: min=0.00181917402378029, max=0.01831490376557743, mean=0.01, median=0.004578982999241088
7Y_Q1: min=0.00010968950345817599, max=0.0013951853734684514, mean=0.00, median=0.0003599757073368534
7Y_Q2: min=8.178920933243406e-05, max=0.0015413478896171664, mean=0.00, median=0.0006681189735361849
7Y_Q3: min=0.0001235120318572379, max=0.0030617731028812914, mean=0.00, median=0.0009952357261063366
7Y_Q4: min=0.0010937964393106117, max=0.007201780315151483, mean=0.00, median=0.002065965101952431
7Y_Q5: min=0.0024324716175340663, max=0.019001627230267697, mean=0.01, median=0.0054341026251013705
10Y_Q1: min=0.00013506646234164385, max=0.0009066439448785757, mean=0.00, median=0.00048248137033890146
10Y_Q2: min=7.049849688730241e-05, max=0.0015099564273773761, mean=0.00, median=0.000753628375294099
10Y_Q3: min=0.00014067599298683156, max=0.0031317827593038386, mean=0.00, median=0.0011648808575763286
10Y_Q4: min=0.001369220402154251, max=0.007455434370823786, mean=0.00, median=0.00231176963926917
10Y_Q5: min=0.003034334451151845, max=0.019338067096909068, mean=0.01, median=0.006138726217706769
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

## ftsfr_treas_yield_curve_zero_coupon.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/fed_yield_curve/ftsfr_treas_yield_curve_zero_coupon.parquet`
**Size:** 3.6 MB | **Type:** Parquet | **Shape:** 500,640 rows × 3 columns

### Columns
```
id                                       String         
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64         (25.7% null)
```

### Numeric Column Statistics
```
y: min=0.0554, max=16.462, mean=5.61, median=5.3232729844415
```

### Date/Datetime Column Statistics
```
ds: min=1961-06-14 00:00:00, max=2025-05-30 00:00:00
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

### Date/Datetime Column Statistics
```
date: min=1973-01-02 00:00:00, max=2025-06-11 00:00:00
```

---

## ftsfr_nyu_call_report_cash_liquidity.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/ftsfr_nyu_call_report_cash_liquidity.parquet`
**Size:** 15.5 MB | **Type:** Parquet | **Shape:** 1,919,810 rows × 3 columns

### Columns
```
id                                       String         
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
id                                       String         
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
id                                       String         
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
id                                       String         
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

### Date/Datetime Column Statistics
```
issueDate: min=1979-11-15 00:00:00, max=2025-06-30 00:00:00
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

### Date/Datetime Column Statistics
```
date: min=1979-11-15 00:00:00, max=2025-06-16 00:00:00
```

---

## ftsfr_CRSP_monthly_stock_ret.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_crsp_compustat/ftsfr_CRSP_monthly_stock_ret.parquet`
**Size:** 21.6 MB | **Type:** Parquet | **Shape:** 3,826,457 rows × 3 columns

### Columns
```
id                                       Int64          
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64         (0.4% null)
```

### Numeric Column Statistics
```
id: min=10000, max=93436, mean=49674.72, median=48215.0
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
id                                       Int64          
ds                                       Datetime(time_unit='ns', time_zone=None)
y                                        Float64         (0.4% null)
```

### Numeric Column Statistics
```
id: min=10000, max=93436, mean=49674.72, median=48215.0
y: min=-1.0, max=26.583827, mean=0.01, median=0.0
```

### Date/Datetime Column Statistics
```
ds: min=1925-12-31 00:00:00, max=2024-12-31 00:00:00
```

---

## arima_CRSP_monthly_stock_ret_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/arima_CRSP_monthly_stock_ret_results.csv`
**Size:** 110 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                String          (100.0% null)
median_mase                              String          (100.0% null)
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=12, max=12, mean=12.00, median=12.0
entity_count: min=0, max=0, mean=0.00, median=0.0
```

---

## arima_CRSP_monthly_stock_retx_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/arima_CRSP_monthly_stock_retx_results.csv`
**Size:** 111 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                String          (100.0% null)
median_mase                              String          (100.0% null)
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=12, max=12, mean=12.00, median=12.0
entity_count: min=0, max=0, mean=0.00, median=0.0
```

---

## arima_nyu_call_report_cash_liquidity_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/arima_nyu_call_report_cash_liquidity_results.csv`
**Size:** 160 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                Float64        
median_mase                              Float64        
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=4, max=4, mean=4.00, median=4.0
mean_mase: min=0.6807426850857086, max=0.6807426850857086, mean=0.68, median=0.6807426850857086
median_mase: min=5.680051796656961e-07, max=5.680051796656961e-07, mean=0.00, median=5.680051796656961e-07
entity_count: min=23080, max=23080, mean=23080.00, median=23080.0
```

---

## arima_nyu_call_report_holding_company_cash_liquidity_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/arima_nyu_call_report_holding_company_cash_liquidity_results.csv`
**Size:** 177 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                Float64        
median_mase                              Float64        
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=4, max=4, mean=4.00, median=4.0
mean_mase: min=0.6465407384816415, max=0.6465407384816415, mean=0.65, median=0.6465407384816415
median_mase: min=1.9842410132783244e-06, max=1.9842410132783244e-06, mean=0.00, median=1.9842410132783244e-06
entity_count: min=13018, max=13018, mean=13018.00, median=13018.0
```

---

## arima_nyu_call_report_holding_company_leverage_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/arima_nyu_call_report_holding_company_leverage_results.csv`
**Size:** 169 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                Float64        
median_mase                              Float64        
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=4, max=4, mean=4.00, median=4.0
mean_mase: min=0.5052603950471181, max=0.5052603950471181, mean=0.51, median=0.5052603950471181
median_mase: min=7.32862022786383e-05, max=7.32862022786383e-05, mean=0.00, median=7.32862022786383e-05
entity_count: min=12998, max=12998, mean=12998.00, median=12998.0
```

---

## arima_nyu_call_report_leverage_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/arima_nyu_call_report_leverage_results.csv`
**Size:** 140 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                Float64        
median_mase                              Float64        
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=4, max=4, mean=4.00, median=4.0
mean_mase: min=inf, max=inf, mean=inf, median=inf
median_mase: min=3.6358875807745753e-06, max=3.6358875807745753e-06, mean=0.00, median=3.6358875807745753e-06
entity_count: min=22125, max=22125, mean=22125.00, median=22125.0
```

---

## arima_treas_yield_curve_zero_coupon_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/arima_treas_yield_curve_zero_coupon_results.csv`
**Size:** 150 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
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

## simple_exponential_smoothing_CRSP_monthly_stock_ret_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/simple_exponential_smoothing_CRSP_monthly_stock_ret_results.csv`
**Size:** 133 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                String          (100.0% null)
median_mase                              String          (100.0% null)
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=12, max=12, mean=12.00, median=12.0
entity_count: min=0, max=0, mean=0.00, median=0.0
```

---

## simple_exponential_smoothing_CRSP_monthly_stock_retx_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/simple_exponential_smoothing_CRSP_monthly_stock_retx_results.csv`
**Size:** 134 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                String          (100.0% null)
median_mase                              String          (100.0% null)
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=12, max=12, mean=12.00, median=12.0
entity_count: min=0, max=0, mean=0.00, median=0.0
```

---

## simple_exponential_smoothing_nyu_call_report_cash_liquidity_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/simple_exponential_smoothing_nyu_call_report_cash_liquidity_results.csv`
**Size:** 180 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                Float64        
median_mase                              Float64        
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=4, max=4, mean=4.00, median=4.0
mean_mase: min=1.3356393215328441, max=1.3356393215328441, mean=1.34, median=1.3356393215328441
median_mase: min=0.6864494775899312, max=0.6864494775899312, mean=0.69, median=0.6864494775899312
entity_count: min=23730, max=23730, mean=23730.00, median=23730.0
```

---

## simple_exponential_smoothing_nyu_call_report_holding_company_cash_liquidity_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/simple_exponential_smoothing_nyu_call_report_holding_company_cash_liquidity_results.csv`
**Size:** 196 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                Float64        
median_mase                              Float64        
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=4, max=4, mean=4.00, median=4.0
mean_mase: min=1.2130974835899908, max=1.2130974835899908, mean=1.21, median=1.2130974835899908
median_mase: min=0.6496576764068551, max=0.6496576764068551, mean=0.65, median=0.6496576764068551
entity_count: min=13429, max=13429, mean=13429.00, median=13429.0
```

---

## simple_exponential_smoothing_nyu_call_report_holding_company_leverage_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/simple_exponential_smoothing_nyu_call_report_holding_company_leverage_results.csv`
**Size:** 190 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                Float64        
median_mase                              Float64        
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=4, max=4, mean=4.00, median=4.0
mean_mase: min=1.2652801154329865, max=1.2652801154329865, mean=1.27, median=1.2652801154329865
median_mase: min=0.8013520218131988, max=0.8013520218131988, mean=0.80, median=0.8013520218131988
entity_count: min=13410, max=13410, mean=13410.00, median=13410.0
```

---

## simple_exponential_smoothing_nyu_call_report_leverage_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/simple_exponential_smoothing_nyu_call_report_leverage_results.csv`
**Size:** 159 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                Float64        
median_mase                              Float64        
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=4, max=4, mean=4.00, median=4.0
mean_mase: min=inf, max=inf, mean=inf, median=inf
median_mase: min=0.7954910280050491, max=0.7954910280050491, mean=0.80, median=0.7954910280050491
entity_count: min=22763, max=22763, mean=22763.00, median=22763.0
```

---

## simple_exponential_smoothing_treas_yield_curve_zero_coupon_results.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/raw_results/simple_exponential_smoothing_treas_yield_curve_zero_coupon_results.csv`
**Size:** 175 bytes | **Type:** Csv | **Shape:** 1 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                Float64        
median_mase                              Float64        
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=5, max=5, mean=5.00, median=5.0
mean_mase: min=13.873554916199861, max=13.873554916199861, mean=13.87, median=13.873554916199861
median_mase: min=14.317112704291796, max=14.317112704291796, mean=14.32, median=14.317112704291796
entity_count: min=30, max=30, mean=30.00, median=30.0
```

---

## results_all.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_output/results_all.csv`
**Size:** 1259 bytes | **Type:** Csv | **Shape:** 14 rows × 7 columns

### Columns
```
model                                    String         
dataset                                  String         
frequency                                String         
seasonality                              Int64          
mean_mase                                Float64         (28.6% null)
median_mase                              Float64         (28.6% null)
entity_count                             Int64          
```

### Numeric Column Statistics
```
seasonality: min=4, max=12, mean=6.43, median=4.0
mean_mase: min=0.5052603950471181, max=inf, mean=inf, median=1.3004597184829152
median_mase: min=5.680051796656961e-07, max=14.317112704291796, mean=2.71, median=0.6680535769983932
entity_count: min=0, max=23730, mean=10329.50, median=13008.0
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