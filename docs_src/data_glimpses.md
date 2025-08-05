# Data Glimpses Report
Total files: 93

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

### Pull
#### Pull: Cds Bond Basis
- [`RED_and_ISIN_mapping.parquet`](#red-and-isin-mapping-parquet)
- [`corporate_bond_returns.parquet`](#corporate-bond-returns-parquet)
- [`markit_cds.parquet`](#markit-cds-parquet)
- [`markit_cds_subsetted_to_crsp.parquet`](#markit-cds-subsetted-to-crsp-parquet)
- [`markit_red_crsp_link.parquet`](#markit-red-crsp-link-parquet)
- [`treasury_bond_returns.parquet`](#treasury-bond-returns-parquet)
#### Pull: Cds Returns
- [`fed_yield_curve.parquet`](#fed-yield-curve-parquet)
- [`fred.parquet`](#fred-parquet)
- [`markit_cds.parquet`](#markit-cds-parquet)
#### Pull: Cip
- [`fx_forward_points.parquet`](#fx-forward-points-parquet)
- [`fx_interest_rates.parquet`](#fx-interest-rates-parquet)
- [`fx_spot_rates.parquet`](#fx-spot-rates-parquet)
#### Pull: Commodities
- [`commodity_futures.parquet`](#commodity-futures-parquet)
- [`gsci_indices.parquet`](#gsci-indices-parquet)
- [`lme_metals.parquet`](#lme-metals-parquet)
#### Pull: Corp Bond Returns
- [`corporate_bond_returns.parquet`](#corporate-bond-returns-parquet)
- [`treasury_bond_returns.parquet`](#treasury-bond-returns-parquet)
#### Pull: Fed Yield Curve
- [`fed_yield_curve.parquet`](#fed-yield-curve-parquet)
#### Pull: Foreign Exchange
- [`fx_daily_data.parquet`](#fx-daily-data-parquet)
- [`fx_monthly_data.parquet`](#fx-monthly-data-parquet)
#### Pull: Futures Returns
- [`wrds_futures.parquet`](#wrds-futures-parquet)
#### Pull: He Kelly Manela
- [`He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv`](#he-kelly-manela-factors-and-test-assets-monthly-csv)
- [`He_Kelly_Manela_Factors_daily.csv`](#he-kelly-manela-factors-daily-csv)
- [`He_Kelly_Manela_Factors_monthly.csv`](#he-kelly-manela-factors-monthly-csv)
#### Pull: Ken French Data Library
- [`french_portfolios_25_daily_size_and_bm.parquet`](#french-portfolios-25-daily-size-and-bm-parquet)
- [`french_portfolios_25_daily_size_and_inv.parquet`](#french-portfolios-25-daily-size-and-inv-parquet)
- [`french_portfolios_25_daily_size_and_op.parquet`](#french-portfolios-25-daily-size-and-op-parquet)
- [`french_portfolios_25_monthly_size_and_bm.parquet`](#french-portfolios-25-monthly-size-and-bm-parquet)
- [`french_portfolios_25_monthly_size_and_inv.parquet`](#french-portfolios-25-monthly-size-and-inv-parquet)
- [`french_portfolios_25_monthly_size_and_op.parquet`](#french-portfolios-25-monthly-size-and-op-parquet)
#### Pull: Nyu Call Report
- [`nyu_call_report.parquet`](#nyu-call-report-parquet)
#### Pull: Options
- [`data_1996-01_2012-01.parquet`](#data-1996-01-2012-01-parquet)
- [`data_2012-02_2019-12.parquet`](#data-2012-02-2019-12-parquet)
#### Pull: Us Treasury Returns
- [`CRSP_TFZ_CONSOLIDATED.parquet`](#crsp-tfz-consolidated-parquet)
- [`CRSP_TFZ_DAILY.parquet`](#crsp-tfz-daily-parquet)
- [`CRSP_TFZ_INFO.parquet`](#crsp-tfz-info-parquet)
- [`CRSP_TFZ_with_runness.parquet`](#crsp-tfz-with-runness-parquet)
- [`treasury_auction_stats.parquet`](#treasury-auction-stats-parquet)
#### Pull: Wrds Bank Premium
- [`idrssd_to_lei.parquet`](#idrssd-to-lei-parquet)
- [`lei_legalevents.parquet`](#lei-legalevents-parquet)
- [`lei_main.parquet`](#lei-main-parquet)
- [`lei_otherentnames.parquet`](#lei-otherentnames-parquet)
- [`lei_successorentity.parquet`](#lei-successorentity-parquet)
- [`wrds_bank_crsp_link.parquet`](#wrds-bank-crsp-link-parquet)
- [`wrds_call_research.parquet`](#wrds-call-research-parquet)
- [`wrds_struct_rel_ultimate.parquet`](#wrds-struct-rel-ultimate-parquet)
#### Pull: Wrds Crsp Compustat
- [`CRSP_Comp_Link_Table.parquet`](#crsp-comp-link-table-parquet)
- [`CRSP_stock_ciz.parquet`](#crsp-stock-ciz-parquet)
- [`Compustat.parquet`](#compustat-parquet)
- [`FF_FACTORS.parquet`](#ff-factors-parquet)

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

## RED_and_ISIN_mapping.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/RED_and_ISIN_mapping.parquet`
**Size:** 238542 bytes | **Type:** Parquet | **Shape:** 10,646 rows × 5 columns

### Columns
```
redcode                                  String         
ticker                                   String         
obl_cusip                                String          (26.8% null)
isin                                     String         
tier                                     String         
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

## corporate_bond_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/corporate_bond_returns.parquet`
**Size:** 271.5 MB | **Type:** Parquet | **Shape:** 1,572,384 rows × 49 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
cusip                                    String         
issuer_cusip                             String         
permno                                   Float64         (9.6% null)
exretn_t+1                               Float64         (33.8% null)
exretnc_bns_t+1                          Float64         (34.4% null)
exretnc_t+1                              Float64         (34.0% null)
exretnc_dur_t+1                          Float64         (34.0% null)
bond_ret_t+1                             Float64         (33.8% null)
bond_ret                                 Float64         (33.5% null)
exretn                                   Float64         (33.5% null)
exretnc_bns                              Float64         (34.2% null)
exretnc                                  Float64         (33.7% null)
exretnc_dur                              Float64         (33.7% null)
rating                                   Float64         (11.1% null)
cs                                       Float64         (11.6% null)
cs_6m_delta                              Float64         (23.6% null)
bond_yield                               Float64         (11.6% null)
bond_amount_out                          Float64         (11.1% null)
offering_amt                             Float64         (11.1% null)
bondprc                                  Float64         (24.4% null)
perc_par                                 Float64         (24.4% null)
tmt                                      Float64         (11.1% null)
duration                                 Float64         (11.6% null)
ind_num_17                               Float64         (34.1% null)
sic_code                                 Float64         (11.1% null)
mom6_1                                   Float64         (6.6% null)
ltrev48_12                               Float64         (51.0% null)
BOND_RET                                 Float64         (23.3% null)
ILLIQ                                    Float64         (27.6% null)
var95                                    Float64         (57.3% null)
n_trades_month                           Float64         (22.9% null)
size_ig                                  Float64         (11.1% null)
size_jk                                  Float64         (11.1% null)
zcb                                      Float64         (11.1% null)
conv                                     Float64         (11.1% null)
BOND_YIELD                               Float64         (17.7% null)
CS                                       Float64         (17.7% null)
BONDPRC                                  Float64         (17.7% null)
PRFULL                                   Float64         (17.7% null)
DURATION                                 Float64         (17.7% null)
CONVEXITY                                Float64         (17.7% null)
CS_6M_DELTA                              Float64         (31.0% null)
bond_value                               Float64         (24.4% null)
BOND_VALUE                               Float64         (17.7% null)
coupon                                   Float64        
bond_type                                String         
principal_amt                            Float64        
bondpar_mil                              Float64         (11.1% null)
```

### Numeric Column Statistics
```
permno: min=10025.0, max=93433.0, mean=51667.80, median=56274.0
exretn_t+1: min=-0.9767107633155356, max=3.68331, mean=0.00, median=0.0024608583916704
exretnc_bns_t+1: min=-0.9788409650955358, max=3.679218441265, mean=0.00, median=0.0013672454083213
exretnc_t+1: min=-0.975496159872277, max=1.0937039372664568, mean=0.00, median=0.00151554299576355
exretnc_dur_t+1: min=-0.9750837579521624, max=1.026469200126305, mean=0.00, median=0.0015140504246088
bond_ret_t+1: min=-0.9753107633155358, max=3.68351, mean=0.00, median=0.0033128735591761
bond_ret: min=-0.9753107633155358, max=3.68351, mean=0.00, median=0.0033377041526085
exretn: min=-0.9767107633155356, max=3.68331, mean=0.00, median=0.0024835982207484
exretnc_bns: min=-0.9788409650955358, max=3.679218441265, mean=0.00, median=0.0013649457596122
exretnc: min=-0.975496159872277, max=1.0937039372664568, mean=0.00, median=0.00151315367870985
exretnc_dur: min=-0.9750837579521624, max=1.026469200126305, mean=0.00, median=0.0015178250172955
rating: min=1.0, max=22.0, mean=8.66, median=8.0
cs: min=-0.9729639446210764, max=0.998901539738254, mean=0.03, median=0.0177682208160528
cs_6m_delta: min=-10.878444246922706, max=9.309785967566132, mean=-0.04, median=-0.0462234915593731
bond_yield: min=-1.0, max=1.0, mean=0.05, median=0.0433994659389245
bond_amount_out: min=1.0, max=15000000.0, mean=555958.59, median=400000.0
offering_amt: min=1.0, max=15000000.0, mean=577398.30, median=400000.0
bondprc: min=0.01, max=3347.9645670033674, mean=104.91, median=104.14881024096384
perc_par: min=0.0001, max=105.34653465346534, mean=1.05, median=1.0415
tmt: min=12.033333333333331, max=1217.5, mean=122.37, median=79.60000000000001
duration: min=0.0333651407924791, max=30.0, mean=6.51, median=5.294389227744916
ind_num_17: min=1.0, max=17.0, mean=12.68, median=14.0
sic_code: min=181.0, max=9532.0, mean=4783.57, median=4922.0
mom6_1: min=-0.97616417196161, max=12.68648163262489, mean=0.02, median=0.0066739471799154
ltrev48_12: min=-0.9685054217585898, max=22.631086156600592, mean=0.16, median=0.1195484294788225
BOND_RET: min=-0.9908377470148158, max=89.81803240743932, mean=0.00, median=0.0025021959575501
ILLIQ: min=-4506.5558135121155, max=10815.473510796275, mean=2.17, median=0.0812535815242251
var95: min=-0.00171, max=0.7020304326820522, mean=0.04, median=0.0300963510511023
n_trades_month: min=1.0, max=24.0, mean=11.59, median=12.0
size_ig: min=0.0, max=1.0, mean=0.78, median=1.0
size_jk: min=0.0, max=1.0, mean=0.97, median=1.0
zcb: min=0.0, max=1.0, mean=0.01, median=0.0
conv: min=0.0, max=1.0, mean=0.00, median=0.0
BOND_YIELD: min=-1.1481999312401832, max=139.41116520263148, mean=0.05, median=0.04279601144790645
CS: min=-1.1611301537537178, max=139.39916520263148, mean=0.03, median=0.01705836639896655
BONDPRC: min=0.0001, max=8491.4861, mean=105.02, median=104.24775
PRFULL: min=0.1009944444335674, max=8491.486257238086, mean=106.38, median=105.58799728776982
DURATION: min=0.0056839521747671, max=35.463740358046394, mean=6.51, median=5.275024154030079
CONVEXITY: min=0.0001021010147481, max=1346.6896180823323, mean=83.44, median=33.81145002739121
CS_6M_DELTA: min=-10.663948714220927, max=7.585603513125841, mean=-0.03, median=-0.0446292284079974
bond_value: min=15.0, max=1899989423.0, mean=65126862.38, median=47239131.0
BOND_VALUE: min=17.0, max=1908028500.0, mean=61961917.12, median=43685320.0
coupon: min=0.0, max=16.5, mean=5.73, median=5.875
principal_amt: min=10.0, max=1000.0, mean=999.81, median=1000.0
bondpar_mil: min=0.001, max=15000.0, mean=555.96, median=400.0
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

## markit_cds.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/markit_cds.parquet`
**Size:** 539.7 MB | **Type:** Parquet | **Shape:** 46,851,870 rows × 7 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
ticker                                   String         
redcode                                  String          (0.0% null)
parspread                                Float64         (0.3% null)
tenor                                    String         
country                                  String         
year                                     Int64          
```

### Numeric Column Statistics
```
parspread: min=6.57e-06, max=491.84276269, mean=0.02, median=0.00783918991183272
year: min=2001, max=2023, mean=2011.46, median=2010.0
```

### Date/Datetime Column Statistics
```
date: min=2001-01-02 00:00:00, max=2023-12-29 00:00:00
```

---

## markit_cds_subsetted_to_crsp.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/markit_cds_subsetted_to_crsp.parquet`
**Size:** 489.2 MB | **Type:** Parquet | **Shape:** 36,382,804 rows × 12 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None) (0.0% null)
ticker                                   String          (0.0% null)
redcode                                  String         
parspread                                Float64         (0.2% null)
tenor                                    String          (0.0% null)
country                                  String          (0.0% null)
year                                     Float64         (0.0% null)
permno                                   Float64        
permco                                   Float64        
flg                                      String         
nameRatio                                Int64          
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
parspread: min=2.001e-05, max=491.84276269, mean=0.02, median=0.007758560333489305
year: min=2001.0, max=2023.0, mean=2010.78, median=2009.0
permno: min=10025.0, max=93423.0, mean=53210.75, median=57665.0
permco: min=7.0, max=60114.0, mean=21824.51, median=21161.0
nameRatio: min=50, max=100, mean=88.24, median=90.0
__index_level_0__: min=0, max=37725767, mean=18328625.79, median=18225252.5
```

### Date/Datetime Column Statistics
```
date: min=2001-01-02 00:00:00, max=2023-12-29 00:00:00
```

---

## markit_red_crsp_link.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/markit_red_crsp_link.parquet`
**Size:** 541363 bytes | **Type:** Parquet | **Shape:** 4,782 rows × 25 columns

### Columns
```
redcode                                  String         
entity_cusip                             String         
ticker                                   String         
referenceentity                          String         
shortname                                String         
lei                                      String          (55.1% null)
entity_type                              String         
jurisdiction                             String         
depthlevel                               String          (87.3% null)
markitsector                             String          (0.1% null)
entity_form                              String          (67.8% null)
companynum_type                          String          (85.3% null)
companynum                               String          (85.3% null)
alternativenames                         String          (97.2% null)
recorddate                               Date            (63.0% null)
validto                                  Date            (58.1% null)
validfrom                                Date            (83.5% null)
permno                                   Float64        
permco                                   Float64        
hdrcusip                                 String         
crspTicker                               String          (0.1% null)
issuernm                                 String         
cusip6                                   String         
flg                                      String         
nameRatio                                Int64          
```

### Numeric Column Statistics
```
permno: min=10025.0, max=93423.0, mean=62661.97, median=77037.0
permco: min=7.0, max=60114.0, mean=25146.44, median=21539.0
nameRatio: min=20, max=100, mean=79.59, median=86.0
```

### Date/Datetime Column Statistics
```
recorddate: min=2002-01-08, max=2025-07-23
validto: min=1995-06-28, max=2025-07-01
validfrom: min=1995-06-28, max=2024-11-04
```

---

## treasury_bond_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_bond_basis/treasury_bond_returns.parquet`
**Size:** 36.6 MB | **Type:** Parquet | **Shape:** 2,381,340 rows × 5 columns

### Columns
```
DATE                                     Int64          
CUSIP                                    String         
tr_return                                Float64         (17.6% null)
tr_ytm_match                             Float64         (26.7% null)
tau                                      Float64        
```

### Numeric Column Statistics
```
DATE: min=20020731, max=20231231, mean=20144649.88, median=20151031.0
tr_return: min=-21.35429959, max=53.313886279, mean=0.22, median=0.09404580914999999
tr_ytm_match: min=0.0039308304, max=8.9466184087, mean=2.47, median=2.355498754
tau: min=-0.167123288, max=180.1260274, mean=7.98, median=4.7123287671
```

---

## fed_yield_curve.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_returns/fed_yield_curve.parquet`
**Size:** 3.2 MB | **Type:** Parquet | **Shape:** 16,728 rows × 31 columns

### Columns
```
SVENY01                                  Float64         (4.4% null)
SVENY02                                  Float64         (4.4% null)
SVENY03                                  Float64         (4.4% null)
SVENY04                                  Float64         (4.4% null)
SVENY05                                  Float64         (4.4% null)
SVENY06                                  Float64         (4.4% null)
SVENY07                                  Float64         (4.4% null)
SVENY08                                  Float64         (19.6% null)
SVENY09                                  Float64         (19.6% null)
SVENY10                                  Float64         (19.6% null)
SVENY11                                  Float64         (19.9% null)
SVENY12                                  Float64         (19.9% null)
SVENY13                                  Float64         (19.9% null)
SVENY14                                  Float64         (19.9% null)
SVENY15                                  Float64         (19.9% null)
SVENY16                                  Float64         (34.3% null)
SVENY17                                  Float64         (34.3% null)
SVENY18                                  Float64         (34.3% null)
SVENY19                                  Float64         (34.3% null)
SVENY20                                  Float64         (34.3% null)
SVENY21                                  Float64         (40.8% null)
SVENY22                                  Float64         (40.8% null)
SVENY23                                  Float64         (40.8% null)
SVENY24                                  Float64         (40.8% null)
SVENY25                                  Float64         (40.8% null)
SVENY26                                  Float64         (40.8% null)
SVENY27                                  Float64         (40.8% null)
SVENY28                                  Float64         (40.8% null)
SVENY29                                  Float64         (40.8% null)
SVENY30                                  Float64         (40.8% null)
Date                                     Datetime(time_unit='ns', time_zone=None)
```

### Numeric Column Statistics
```
SVENY01: min=0.0554, max=16.462, mean=4.82, median=4.87665
SVENY02: min=0.102, max=15.9118, mean=5.01, median=4.8868753520755
SVENY03: min=0.12720000743866, max=15.5746, mean=5.17, median=4.967064475481
SVENY04: min=0.168500006198883, max=15.3498, mean=5.31, median=5.097524521712
SVENY05: min=0.221799999475479, max=15.1776, mean=5.43, median=5.22705
SVENY06: min=0.280600011348724, max=15.0611, mean=5.54, median=5.350854821023
SVENY07: min=0.341300010681152, max=15.0109, mean=5.63, median=5.440074447974499
SVENY08: min=0.40200001001358, max=14.9799, mean=5.83, median=5.801927200545
SVENY09: min=0.461800009012222, max=14.9572, mean=5.92, median=5.877466198994
SVENY10: min=0.52020001411438, max=14.9398, mean=5.99, median=5.9397482168925
SVENY11: min=0.577000021934509, max=14.934, mean=6.06, median=5.969950757447
SVENY12: min=0.632300019264221, max=14.9367, mean=6.11, median=6.005938710184
SVENY13: min=0.685899972915649, max=14.9407, mean=6.16, median=6.046527388536
SVENY14: min=0.737999975681305, max=14.9684, mean=6.21, median=6.0873
SVENY15: min=0.781599998474121, max=15.0394, mean=6.24, median=6.120679528271
SVENY16: min=0.817200005054474, max=15.1073, mean=5.86, median=5.2906
SVENY17: min=0.85290002822876, max=15.1716, mean=5.89, median=5.3335
SVENY18: min=0.888400018215179, max=15.2318, mean=5.92, median=5.3611
SVENY19: min=0.923600018024445, max=15.2879, mean=5.94, median=5.384991808666
SVENY20: min=0.958100020885468, max=15.34, mean=5.96, median=5.4088
SVENY21: min=0.991900026798248, max=10.4856, mean=5.29, median=5.03435
SVENY22: min=1.02479994297028, max=10.5206, mean=5.30, median=5.0307
SVENY23: min=1.0566999912262, max=10.5553, mean=5.30, median=5.025499999999999
SVENY24: min=1.08759999275208, max=10.5893, mean=5.31, median=5.0120000000000005
SVENY25: min=1.11740005016327, max=10.6217, mean=5.31, median=5.00305
SVENY26: min=1.14619994163513, max=10.6526, mean=5.31, median=4.98315
SVENY27: min=1.17379999160767, max=10.6819, mean=5.30, median=4.96675003852844
SVENY28: min=1.20039999485016, max=10.7099, mean=5.30, median=4.949799907684325
SVENY29: min=1.22580003738403, max=10.7365, mean=5.29, median=4.93165
SVENY30: min=1.2503000497818, max=10.7618, mean=5.28, median=4.91175
```

### Date/Datetime Column Statistics
```
Date: min=1961-06-14 00:00:00, max=2025-07-25 00:00:00
```

---

## fred.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_returns/fred.parquet`
**Size:** 122461 bytes | **Type:** Parquet | **Shape:** 6,415 rows × 7 columns

### Columns
```
DGS1MO                                   Float64         (6.4% null)
DGS3MO                                   Float64         (4.2% null)
DGS6MO                                   Float64         (4.2% null)
DGS1                                     Float64         (4.2% null)
DGS2                                     Float64         (4.2% null)
DGS3                                     Float64         (4.2% null)
DATE                                     Datetime(time_unit='ns', time_zone=None)
```

### Numeric Column Statistics
```
DGS1MO: min=0.0, max=6.02, mean=1.62, median=0.96
DGS3MO: min=0.0, max=5.87, mean=1.74, median=1.08
DGS6MO: min=0.02, max=5.61, mean=1.84, median=1.2
DGS1: min=0.04, max=5.49, mean=1.91, median=1.375
DGS2: min=0.09, max=5.29, mean=2.07, median=1.66
DGS3: min=0.1, max=5.26, mean=2.25, median=1.93
```

### Date/Datetime Column Statistics
```
DATE: min=2001-01-01 00:00:00, max=2025-08-01 00:00:00
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
y: min=-1.805771167145001, max=1.2258522666583365, mean=0.00, median=0.00165942357214921
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
y: min=5.3907256347465184e-05, max=0.019317670228214602, mean=0.00, median=0.0008444368017673691
```

### Date/Datetime Column Statistics
```
ds: min=2001-01-01 00:00:00, max=2023-12-01 00:00:00
```

---

## markit_cds.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_returns/markit_cds.parquet`
**Size:** 1.4 GB | **Type:** Parquet | **Shape:** 36,673,117 rows × 15 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
ticker                                   String         
redcode                                  String          (0.0% null)
parspread                                Float64         (0.3% null)
convspreard                              Float64         (20.7% null)
tenor                                    String         
country                                  String         
creditdv01                               Float64         (32.8% null)
riskypv01                                Float64         (32.8% null)
irdv01                                   Float64         (32.8% null)
rec01                                    Float64         (32.8% null)
dp                                       Float64         (32.8% null)
jtd                                      Float64         (32.8% null)
dtz                                      Float64         (32.8% null)
year                                     Int64          
```

### Numeric Column Statistics
```
parspread: min=6.57e-06, max=28.73255034, mean=0.02, median=0.00859374
convspreard: min=6.51e-06, max=33.29895315, mean=0.02, median=0.00901274
creditdv01: min=-129980.22, max=1450128.28, mean=4836.26, median=4708.61
riskypv01: min=0.03, max=10.02, mean=4.54, median=4.67
irdv01: min=-260294.91, max=1449338.67, mean=181.02, median=36.01
rec01: min=-838629.15, max=2833213.38, mean=12284.17, median=7825.39
dp: min=1.170670425e-05, max=1.0, mean=0.14, median=0.07792383818339
jtd: min=4114.93, max=12774322.14, mean=6670226.42, median=6337462.6
dtz: min=104114.93, max=14849492.24, mean=10524286.74, median=10252921.47
year: min=2001, max=2023, mean=2013.61, median=2014.0
```

### Date/Datetime Column Statistics
```
date: min=2001-01-02 00:00:00, max=2023-12-29 00:00:00
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
monthly_return: min=-1.805771167145001, max=1.2258522666583365, mean=nan, median=nan
```

### Date/Datetime Column Statistics
```
Month: min=2001-01-01 00:00:00, max=2023-12-01 00:00:00
```

---

## markit_cds_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cds_returns/markit_cds_returns.parquet`
**Size:** 50527 bytes | **Type:** Parquet | **Shape:** 276 rows × 21 columns

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
3Y_Q1: min=5.3907256347465184e-05, max=0.0012974836896890297, mean=0.00, median=0.0001776013178357204
3Y_Q2: min=9.773547959429239e-05, max=0.0017577818757063132, mean=0.00, median=0.0003019693141803718
3Y_Q3: min=0.00016916296164212405, max=0.0028226224959090793, mean=0.00, median=0.00048601067672548207
3Y_Q4: min=0.00035489114832455915, max=0.00864358877171839, mean=0.00, median=0.0008247730852523188
3Y_Q5: min=0.0010307849448750856, max=0.017031472819558965, mean=0.00, median=0.003338875943245725
5Y_Q1: min=8.275439968574716e-05, max=0.0013420012384308677, mean=0.00, median=0.00027887000200477186
5Y_Q2: min=0.00016532929009160924, max=0.0015301593893626286, mean=0.00, median=0.0005009268881910334
5Y_Q3: min=0.0002442534777740146, max=0.002973919044126916, mean=0.00, median=0.0007583209877857211
5Y_Q4: min=0.0006774992502349697, max=0.008650813007283542, mean=0.00, median=0.0013587489619791837
5Y_Q5: min=0.001823802572132216, max=0.018296624693337593, mean=0.01, median=0.004590051431173414
7Y_Q1: min=0.00010964151183551482, max=0.0013945749485155168, mean=0.00, median=0.0003623615403731995
7Y_Q2: min=8.181643590067579e-05, max=0.0015388646099238036, mean=0.00, median=0.0006669838184098324
7Y_Q3: min=0.00012351514237244048, max=0.0030643487514598953, mean=0.00, median=0.0009942756541370874
7Y_Q4: min=0.0011032129790016032, max=0.0071956819840353235, mean=0.00, median=0.002065088784623438
7Y_Q5: min=0.0024397821963655923, max=0.018984225883366183, mean=0.01, median=0.005423172283498261
10Y_Q1: min=0.00013483294081628093, max=0.0009055446727739869, mean=0.00, median=0.00048207592885402467
10Y_Q2: min=7.057616429322453e-05, max=0.0015085319278383455, mean=0.00, median=0.0007488219594316987
10Y_Q3: min=0.0001406853851101926, max=0.0031347630473006656, mean=0.00, median=0.0011665910466828495
10Y_Q4: min=0.0013478380350864384, max=0.007450226163609099, mean=0.00, median=0.0023127796580387707
10Y_Q5: min=0.0030433466755069856, max=0.019317670228214602, mean=0.01, median=0.006120782679122833
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

## fx_forward_points.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cip/fx_forward_points.parquet`
**Size:** 381386 bytes | **Type:** Parquet | **Shape:** 10,376 rows × 9 columns

### Columns
```
index                                    Date           
AUD3M CMPN Curncy_PX_LAST                Float64         (4.3% null)
CAD3M CMPN Curncy_PX_LAST                Float64         (8.9% null)
CHF3M CMPN Curncy_PX_LAST                Float64         (8.7% null)
EUR3M CMPN Curncy_PX_LAST                Float64         (33.4% null)
GBP3M CMPN Curncy_PX_LAST                Float64         (4.0% null)
JPY3M CMPN Curncy_PX_LAST                Float64         (8.8% null)
NZD3M CMPN Curncy_PX_LAST                Float64         (8.9% null)
SEK3M CMPN Curncy_PX_LAST                Float64         (8.8% null)
```

### Numeric Column Statistics
```
AUD3M CMPN Curncy_PX_LAST: min=-228.11, max=72.0, mean=-39.84, median=-30.56
CAD3M CMPN Curncy_PX_LAST: min=-90.5, max=190.0, mean=9.10, median=0.75
CHF3M CMPN Curncy_PX_LAST: min=-327.01, max=211.0, mean=-47.42, median=-40.03
EUR3M CMPN Curncy_PX_LAST: min=-79.05, max=101.47, mean=23.41, median=23.59
GBP3M CMPN Curncy_PX_LAST: min=-348.54, max=66.64, mean=-46.40, median=-12.11
JPY3M CMPN Curncy_PX_LAST: min=-234.14, max=74.32, mean=-71.75, median=-55.28
NZD3M CMPN Curncy_PX_LAST: min=-159.0, max=82.0, mean=-35.63, median=-39.0
SEK3M CMPN Curncy_PX_LAST: min=-847.0, max=6500.01, mean=27.57, median=-59.55
```

### Date/Datetime Column Statistics
```
index: min=1983-12-13, max=2025-06-17
```

---

## fx_interest_rates.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cip/fx_interest_rates.parquet`
**Size:** 256050 bytes | **Type:** Parquet | **Shape:** 6,867 rows × 10 columns

### Columns
```
index                                    Date           
ADSOC CMPN Curncy_PX_LAST                Float64         (11.0% null)
CDSOC CMPN Curncy_PX_LAST                Float64         (15.5% null)
SFSNTC CMPN Curncy_PX_LAST               Float64         (40.4% null)
EUSWEC CMPN Curncy_PX_LAST               Float64         (13.4% null)
BPSWSC CMPN Curncy_PX_LAST               Float64         (7.2% null)
JYSOC CMPN Curncy_PX_LAST                Float64         (14.6% null)
NDSOC CMPN Curncy_PX_LAST                Float64         (14.0% null)
SKSWTNC BGN Curncy_PX_LAST               Float64         (26.3% null)
USSOC CMPN Curncy_PX_LAST                Float64         (10.8% null)
```

### Numeric Column Statistics
```
ADSOC CMPN Curncy_PX_LAST: min=0.01875, max=7.3985, mean=3.40, median=3.6325
CDSOC CMPN Curncy_PX_LAST: min=0.1675, max=5.165, mean=1.88, median=1.11
SFSNTC CMPN Curncy_PX_LAST: min=-1.025, max=1.8825, mean=-0.21, median=-0.2175
EUSWEC CMPN Curncy_PX_LAST: min=-0.5943, max=5.095, mean=1.37, median=0.6065
BPSWSC CMPN Curncy_PX_LAST: min=0.023, max=5.985, mean=2.27, median=0.70105
JYSOC CMPN Curncy_PX_LAST: min=-0.15125, max=0.699, mean=0.08, median=0.039
NDSOC CMPN Curncy_PX_LAST: min=0.1941, max=8.37125, mean=3.71, median=2.8752500000000003
SKSWTNC BGN Curncy_PX_LAST: min=-0.618, max=5.04, mean=1.21, median=0.95
USSOC CMPN Curncy_PX_LAST: min=0.04302, max=5.4432, mean=1.74, median=1.1179999999999999
```

### Date/Datetime Column Statistics
```
index: min=1999-02-08, max=2025-06-17
```

---

## fx_spot_rates.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/cip/fx_spot_rates.parquet`
**Size:** 546726 bytes | **Type:** Parquet | **Shape:** 14,207 rows × 9 columns

### Columns
```
index                                    Date           
AUD CMPN Curncy_PX_LAST                  Float64         (1.0% null)
CAD CMPN Curncy_PX_LAST                  Float64        
CHF CMPN Curncy_PX_LAST                  Float64        
EUR CMPN Curncy_PX_LAST                  Float64         (51.4% null)
GBP CMPN Curncy_PX_LAST                  Float64        
JPY CMPN Curncy_PX_LAST                  Float64        
NZD CMPN Curncy_PX_LAST                  Float64         (1.2% null)
SEK CMPN Curncy_PX_LAST                  Float64        
```

### Numeric Column Statistics
```
AUD CMPN Curncy_PX_LAST: min=0.479, max=1.4885, mean=0.85, median=0.7698
CAD CMPN Curncy_PX_LAST: min=0.9204, max=1.6135, mean=1.23, median=1.2382
CHF CMPN Curncy_PX_LAST: min=0.7208, max=4.318, mean=1.58, median=1.404
EUR CMPN Curncy_PX_LAST: min=0.8272, max=1.5992, mean=1.18, median=1.1712
GBP CMPN Curncy_PX_LAST: min=1.052, max=2.644, mean=1.68, median=1.612
JPY CMPN Curncy_PX_LAST: min=75.83, max=358.44, mean=156.48, median=123.36
NZD CMPN Curncy_PX_LAST: min=0.3915, max=1.49, mean=0.73, median=0.6724
SEK CMPN Curncy_PX_LAST: min=3.867, max=11.3655, mean=7.15, median=7.1965
```

### Date/Datetime Column Statistics
```
index: min=1971-01-04, max=2025-06-17
```

---

## commodity_futures.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/commodities/commodity_futures.parquet`
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

## gsci_indices.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/commodities/gsci_indices.parquet`
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

## lme_metals.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/commodities/lme_metals.parquet`
**Size:** 457058 bytes | **Type:** Parquet | **Shape:** 9,919 rows × 11 columns

### Columns
```
index                                    Date           
LMAHDY Comdty_PX_LAST                    Float64         (3.8% null)
LMAHDS03 Comdty_PX_LAST                  Float64         (3.1% null)
LMNIDY Comdty_PX_LAST                    Float64         (2.2% null)
LMNIDS03 Comdty_PX_LAST                  Float64         (2.1% null)
LMPBDY Comdty_PX_LAST                    Float64         (2.1% null)
LMPBDS03 Comdty_PX_LAST                  Float64         (2.1% null)
LMZSDY Comdty_PX_LAST                    Float64         (7.1% null)
LMZSDS03 Comdty_PX_LAST                  Float64         (7.1% null)
LMCADY Comdty_PX_LAST                    Float64         (0.2% null)
LMCADS03 Comdty_PX_LAST                  Float64         (0.2% null)
```

### Numeric Column Statistics
```
LMAHDY Comdty_PX_LAST: min=1019.0, max=4290.0, mean=1869.95, median=1784.875
LMAHDS03 Comdty_PX_LAST: min=1040.5, max=3849.0, mean=1878.77, median=1796.0
LMNIDY Comdty_PX_LAST: min=2282.0, max=54050.0, mean=13297.36, median=12072.25
LMNIDS03 Comdty_PX_LAST: min=2331.0, max=51600.0, mean=13224.95, median=11950.0
LMPBDY Comdty_PX_LAST: min=356.0, max=3989.0, mean=1342.98, median=1105.0
LMPBDS03 Comdty_PX_LAST: min=369.0, max=3890.0, mean=1345.08, median=1093.5
LMZSDY Comdty_PX_LAST: min=722.75, max=4603.0, mean=1846.36, median=1780.0
LMZSDS03 Comdty_PX_LAST: min=743.0, max=4515.0, mean=1850.37, median=1772.0
LMCADY Comdty_PX_LAST: min=1287.18, max=11299.5, mean=4684.37, median=3687.5
LMCADS03 Comdty_PX_LAST: min=1301.7, max=10889.0, mean=4665.68, median=3567.0
```

### Date/Datetime Column Statistics
```
index: min=1986-04-01, max=2025-06-20
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

## corporate_bond_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/corp_bond_returns/corporate_bond_returns.parquet`
**Size:** 271.5 MB | **Type:** Parquet | **Shape:** 1,572,384 rows × 49 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
cusip                                    String         
issuer_cusip                             String         
permno                                   Float64         (9.6% null)
exretn_t+1                               Float64         (33.8% null)
exretnc_bns_t+1                          Float64         (34.4% null)
exretnc_t+1                              Float64         (34.0% null)
exretnc_dur_t+1                          Float64         (34.0% null)
bond_ret_t+1                             Float64         (33.8% null)
bond_ret                                 Float64         (33.5% null)
exretn                                   Float64         (33.5% null)
exretnc_bns                              Float64         (34.2% null)
exretnc                                  Float64         (33.7% null)
exretnc_dur                              Float64         (33.7% null)
rating                                   Float64         (11.1% null)
cs                                       Float64         (11.6% null)
cs_6m_delta                              Float64         (23.6% null)
bond_yield                               Float64         (11.6% null)
bond_amount_out                          Float64         (11.1% null)
offering_amt                             Float64         (11.1% null)
bondprc                                  Float64         (24.4% null)
perc_par                                 Float64         (24.4% null)
tmt                                      Float64         (11.1% null)
duration                                 Float64         (11.6% null)
ind_num_17                               Float64         (34.1% null)
sic_code                                 Float64         (11.1% null)
mom6_1                                   Float64         (6.6% null)
ltrev48_12                               Float64         (51.0% null)
BOND_RET                                 Float64         (23.3% null)
ILLIQ                                    Float64         (27.6% null)
var95                                    Float64         (57.3% null)
n_trades_month                           Float64         (22.9% null)
size_ig                                  Float64         (11.1% null)
size_jk                                  Float64         (11.1% null)
zcb                                      Float64         (11.1% null)
conv                                     Float64         (11.1% null)
BOND_YIELD                               Float64         (17.7% null)
CS                                       Float64         (17.7% null)
BONDPRC                                  Float64         (17.7% null)
PRFULL                                   Float64         (17.7% null)
DURATION                                 Float64         (17.7% null)
CONVEXITY                                Float64         (17.7% null)
CS_6M_DELTA                              Float64         (31.0% null)
bond_value                               Float64         (24.4% null)
BOND_VALUE                               Float64         (17.7% null)
coupon                                   Float64        
bond_type                                String         
principal_amt                            Float64        
bondpar_mil                              Float64         (11.1% null)
```

### Numeric Column Statistics
```
permno: min=10025.0, max=93433.0, mean=51667.80, median=56274.0
exretn_t+1: min=-0.9767107633155356, max=3.68331, mean=0.00, median=0.0024608583916704
exretnc_bns_t+1: min=-0.9788409650955358, max=3.679218441265, mean=0.00, median=0.0013672454083213
exretnc_t+1: min=-0.975496159872277, max=1.0937039372664568, mean=0.00, median=0.00151554299576355
exretnc_dur_t+1: min=-0.9750837579521624, max=1.026469200126305, mean=0.00, median=0.0015140504246088
bond_ret_t+1: min=-0.9753107633155358, max=3.68351, mean=0.00, median=0.0033128735591761
bond_ret: min=-0.9753107633155358, max=3.68351, mean=0.00, median=0.0033377041526085
exretn: min=-0.9767107633155356, max=3.68331, mean=0.00, median=0.0024835982207484
exretnc_bns: min=-0.9788409650955358, max=3.679218441265, mean=0.00, median=0.0013649457596122
exretnc: min=-0.975496159872277, max=1.0937039372664568, mean=0.00, median=0.00151315367870985
exretnc_dur: min=-0.9750837579521624, max=1.026469200126305, mean=0.00, median=0.0015178250172955
rating: min=1.0, max=22.0, mean=8.66, median=8.0
cs: min=-0.9729639446210764, max=0.998901539738254, mean=0.03, median=0.0177682208160528
cs_6m_delta: min=-10.878444246922706, max=9.309785967566132, mean=-0.04, median=-0.0462234915593731
bond_yield: min=-1.0, max=1.0, mean=0.05, median=0.0433994659389245
bond_amount_out: min=1.0, max=15000000.0, mean=555958.59, median=400000.0
offering_amt: min=1.0, max=15000000.0, mean=577398.30, median=400000.0
bondprc: min=0.01, max=3347.9645670033674, mean=104.91, median=104.14881024096384
perc_par: min=0.0001, max=105.34653465346534, mean=1.05, median=1.0415
tmt: min=12.033333333333331, max=1217.5, mean=122.37, median=79.60000000000001
duration: min=0.0333651407924791, max=30.0, mean=6.51, median=5.294389227744916
ind_num_17: min=1.0, max=17.0, mean=12.68, median=14.0
sic_code: min=181.0, max=9532.0, mean=4783.57, median=4922.0
mom6_1: min=-0.97616417196161, max=12.68648163262489, mean=0.02, median=0.0066739471799154
ltrev48_12: min=-0.9685054217585898, max=22.631086156600592, mean=0.16, median=0.1195484294788225
BOND_RET: min=-0.9908377470148158, max=89.81803240743932, mean=0.00, median=0.0025021959575501
ILLIQ: min=-4506.5558135121155, max=10815.473510796275, mean=2.17, median=0.0812535815242251
var95: min=-0.00171, max=0.7020304326820522, mean=0.04, median=0.0300963510511023
n_trades_month: min=1.0, max=24.0, mean=11.59, median=12.0
size_ig: min=0.0, max=1.0, mean=0.78, median=1.0
size_jk: min=0.0, max=1.0, mean=0.97, median=1.0
zcb: min=0.0, max=1.0, mean=0.01, median=0.0
conv: min=0.0, max=1.0, mean=0.00, median=0.0
BOND_YIELD: min=-1.1481999312401832, max=139.41116520263148, mean=0.05, median=0.04279601144790645
CS: min=-1.1611301537537178, max=139.39916520263148, mean=0.03, median=0.01705836639896655
BONDPRC: min=0.0001, max=8491.4861, mean=105.02, median=104.24775
PRFULL: min=0.1009944444335674, max=8491.486257238086, mean=106.38, median=105.58799728776982
DURATION: min=0.0056839521747671, max=35.463740358046394, mean=6.51, median=5.275024154030079
CONVEXITY: min=0.0001021010147481, max=1346.6896180823323, mean=83.44, median=33.81145002739121
CS_6M_DELTA: min=-10.663948714220927, max=7.585603513125841, mean=-0.03, median=-0.0446292284079974
bond_value: min=15.0, max=1899989423.0, mean=65126862.38, median=47239131.0
BOND_VALUE: min=17.0, max=1908028500.0, mean=61961917.12, median=43685320.0
coupon: min=0.0, max=16.5, mean=5.73, median=5.875
principal_amt: min=10.0, max=1000.0, mean=999.81, median=1000.0
bondpar_mil: min=0.001, max=15000.0, mean=555.96, median=400.0
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

## treasury_bond_returns.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/corp_bond_returns/treasury_bond_returns.parquet`
**Size:** 36.6 MB | **Type:** Parquet | **Shape:** 2,381,340 rows × 5 columns

### Columns
```
DATE                                     Int64          
CUSIP                                    String         
tr_return                                Float64         (17.6% null)
tr_ytm_match                             Float64         (26.7% null)
tau                                      Float64        
```

### Numeric Column Statistics
```
DATE: min=20020731, max=20231231, mean=20144649.88, median=20151031.0
tr_return: min=-21.35429959, max=53.313886279, mean=0.22, median=0.09404580914999999
tr_ytm_match: min=0.0039308304, max=8.9466184087, mean=2.47, median=2.355498754
tau: min=-0.167123288, max=180.1260274, mean=7.98, median=4.7123287671
```

---

## fed_yield_curve.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/fed_yield_curve/fed_yield_curve.parquet`
**Size:** 3.2 MB | **Type:** Parquet | **Shape:** 16,728 rows × 31 columns

### Columns
```
SVENY01                                  Float64         (4.4% null)
SVENY02                                  Float64         (4.4% null)
SVENY03                                  Float64         (4.4% null)
SVENY04                                  Float64         (4.4% null)
SVENY05                                  Float64         (4.4% null)
SVENY06                                  Float64         (4.4% null)
SVENY07                                  Float64         (4.4% null)
SVENY08                                  Float64         (19.6% null)
SVENY09                                  Float64         (19.6% null)
SVENY10                                  Float64         (19.6% null)
SVENY11                                  Float64         (19.9% null)
SVENY12                                  Float64         (19.9% null)
SVENY13                                  Float64         (19.9% null)
SVENY14                                  Float64         (19.9% null)
SVENY15                                  Float64         (19.9% null)
SVENY16                                  Float64         (34.3% null)
SVENY17                                  Float64         (34.3% null)
SVENY18                                  Float64         (34.3% null)
SVENY19                                  Float64         (34.3% null)
SVENY20                                  Float64         (34.3% null)
SVENY21                                  Float64         (40.8% null)
SVENY22                                  Float64         (40.8% null)
SVENY23                                  Float64         (40.8% null)
SVENY24                                  Float64         (40.8% null)
SVENY25                                  Float64         (40.8% null)
SVENY26                                  Float64         (40.8% null)
SVENY27                                  Float64         (40.8% null)
SVENY28                                  Float64         (40.8% null)
SVENY29                                  Float64         (40.8% null)
SVENY30                                  Float64         (40.8% null)
Date                                     Datetime(time_unit='ns', time_zone=None)
```

### Numeric Column Statistics
```
SVENY01: min=0.0554, max=16.462, mean=4.82, median=4.87665
SVENY02: min=0.102, max=15.9118, mean=5.01, median=4.8868753520755
SVENY03: min=0.12720000743866, max=15.5746, mean=5.17, median=4.967064475481
SVENY04: min=0.168500006198883, max=15.3498, mean=5.31, median=5.097524521712
SVENY05: min=0.221799999475479, max=15.1776, mean=5.43, median=5.22705
SVENY06: min=0.280600011348724, max=15.0611, mean=5.54, median=5.350854821023
SVENY07: min=0.341300010681152, max=15.0109, mean=5.63, median=5.440074447974499
SVENY08: min=0.40200001001358, max=14.9799, mean=5.83, median=5.801927200545
SVENY09: min=0.461800009012222, max=14.9572, mean=5.92, median=5.877466198994
SVENY10: min=0.52020001411438, max=14.9398, mean=5.99, median=5.9397482168925
SVENY11: min=0.577000021934509, max=14.934, mean=6.06, median=5.969950757447
SVENY12: min=0.632300019264221, max=14.9367, mean=6.11, median=6.005938710184
SVENY13: min=0.685899972915649, max=14.9407, mean=6.16, median=6.046527388536
SVENY14: min=0.737999975681305, max=14.9684, mean=6.21, median=6.0873
SVENY15: min=0.781599998474121, max=15.0394, mean=6.24, median=6.120679528271
SVENY16: min=0.817200005054474, max=15.1073, mean=5.86, median=5.2906
SVENY17: min=0.85290002822876, max=15.1716, mean=5.89, median=5.3335
SVENY18: min=0.888400018215179, max=15.2318, mean=5.92, median=5.3611
SVENY19: min=0.923600018024445, max=15.2879, mean=5.94, median=5.384991808666
SVENY20: min=0.958100020885468, max=15.34, mean=5.96, median=5.4088
SVENY21: min=0.991900026798248, max=10.4856, mean=5.29, median=5.03435
SVENY22: min=1.02479994297028, max=10.5206, mean=5.30, median=5.0307
SVENY23: min=1.0566999912262, max=10.5553, mean=5.30, median=5.025499999999999
SVENY24: min=1.08759999275208, max=10.5893, mean=5.31, median=5.0120000000000005
SVENY25: min=1.11740005016327, max=10.6217, mean=5.31, median=5.00305
SVENY26: min=1.14619994163513, max=10.6526, mean=5.31, median=4.98315
SVENY27: min=1.17379999160767, max=10.6819, mean=5.30, median=4.96675003852844
SVENY28: min=1.20039999485016, max=10.7099, mean=5.30, median=4.949799907684325
SVENY29: min=1.22580003738403, max=10.7365, mean=5.29, median=4.93165
SVENY30: min=1.2503000497818, max=10.7618, mean=5.28, median=4.91175
```

### Date/Datetime Column Statistics
```
Date: min=1961-06-14 00:00:00, max=2025-07-25 00:00:00
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
**Size:** 625360 bytes | **Type:** Parquet | **Shape:** 61,110 rows × 3 columns

### Columns
```
unique_id                                String         
ds                                       Date           
y                                        Float64         (14.1% null)
```

### Numeric Column Statistics
```
y: min=-1.0326500049101444, max=8.548700375536482, mean=1.77, median=1.0010820813484795
```

### Date/Datetime Column Statistics
```
ds: min=1999-02-08, max=2025-02-28
```

---

## fx_daily_data.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/foreign_exchange/fx_daily_data.parquet`
**Size:** 2.1 MB | **Type:** Parquet | **Shape:** 14,115 rows × 49 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
dexusal                                  Float64         (3.9% null)
dexalus                                  Float64         (3.9% null)
dexbzus                                  Float64         (46.5% null)
dexcaus                                  Float64         (3.8% null)
dexchus                                  Float64         (22.0% null)
dexdnus                                  Float64         (3.9% null)
dexhkus                                  Float64         (21.6% null)
dexinus                                  Float64         (7.5% null)
dexjpus                                  Float64         (3.9% null)
dexkous                                  Float64         (22.4% null)
dexmaus                                  Float64         (4.0% null)
dexmxus                                  Float64         (44.5% null)
dexusnz                                  Float64         (4.0% null)
dexnzus                                  Float64         (4.0% null)
dexnous                                  Float64         (3.9% null)
dexsius                                  Float64         (21.6% null)
dexsfus                                  Float64         (19.9% null)
dexslus                                  Float64         (10.0% null)
dexsdus                                  Float64         (3.9% null)
dexszus                                  Float64         (3.9% null)
dextaus                                  Float64         (28.6% null)
dexthus                                  Float64         (22.2% null)
dexusuk                                  Float64         (3.9% null)
dexukus                                  Float64         (3.9% null)
dexvzus                                  Float64         (46.6% null)
exauus                                   Float64         (50.3% null)
exbeus                                   Float64         (50.3% null)
exfnus                                   Float64         (50.5% null)
exfrus                                   Float64         (50.3% null)
exgeus                                   Float64         (50.3% null)
exgrus                                   Float64         (64.9% null)
exusir                                   Float64         (50.3% null)
exirus                                   Float64         (50.3% null)
exitus                                   Float64         (50.3% null)
exneus                                   Float64         (50.3% null)
expous                                   Float64         (53.8% null)
exspus                                   Float64         (53.8% null)
exusec                                   Float64         (65.3% null)
execus                                   Float64         (65.3% null)
dexuseu                                  Float64         (53.6% null)
dexeuus                                  Float64         (53.6% null)
dtwexb                                   Float64         (55.2% null)
dtwexbgs                                 Float64         (66.1% null)
dtwexm                                   Float64         (16.2% null)
dtwexafegs                               Float64         (66.1% null)
dtwexo                                   Float64         (55.2% null)
dtwexemegs                               Float64         (66.1% null)
indexgx                                  Float64         (50.3% null)
```

### Numeric Column Statistics
```
dexusal: min=0.4828, max=1.4885, mean=0.85, median=0.77185
dexalus: min=0.6718172657037286, max=2.071251035625518, mean=1.24, median=1.2955885265224771
dexbzus: min=0.832, max=6.2021, mean=2.78, median=2.3308999999999997
dexcaus: min=0.9168, max=1.6128, mean=1.23, median=1.2371
dexchus: min=1.5264, max=8.7409, mean=6.27, median=6.7534
dexdnus: min=4.6605, max=12.3725, mean=6.63, median=6.4084
dexhkus: min=5.127, max=8.7, mean=7.68, median=7.772
dexinus: min=7.19, max=87.57, mean=37.43, median=40.33
dexjpus: min=75.72, max=358.44, mean=156.34, median=123.02
dexkous: min=667.2, max=1960.0, mean=1021.24, median=1073.9
dexmaus: min=2.1048, max=4.7975, mean=3.16, median=3.049
dexmxus: min=3.1022, max=25.132, mean=13.07, median=12.1824
dexusnz: min=0.392, max=1.49, mean=0.73, median=0.6745
dexnzus: min=0.6711409395973155, max=2.5510204081632653, mean=1.47, median=1.4825796886582654
dexnous: min=4.6585, max=11.6842, mean=7.02, median=6.743
dexsius: min=1.2007, max=2.3085, mean=1.62, median=1.5754
dexsfus: min=0.7371, max=19.7787, mean=7.33, median=6.6785499999999995
dexslus: min=6.006, max=365.43, mean=89.46, median=71.9
dexsdus: min=3.867, max=11.345, mean=7.13, median=7.1831499999999995
dexszus: min=0.7296, max=4.318, mean=1.58, median=1.4095
dextaus: min=24.507, max=40.6, mean=31.04, median=30.86
dexthus: min=20.36, max=56.1, mean=31.60, median=31.55
dexusuk: min=1.052, max=2.644, mean=1.68, median=1.613
dexukus: min=0.37821482602118, max=0.9505703422053231, mean=0.62, median=0.6199628022318661
dexvzus: min=0.1697, max=4171327.382, mean=83251.17, median=2.145
exauus: min=9.538, max=26.075, mean=15.22, median=13.95
exbeus: min=27.12, max=69.6, mean=38.61, median=36.73
exfnus: min=3.4554, max=7.115, mean=4.53, median=4.28275
exfrus: min=3.8462, max=10.56, mean=5.67, median=5.5137
exgeus: min=1.3565, max=3.645, mean=2.14, median=1.9458
exgrus: min=52.9, max=410.3, mean=190.00, median=171.0
exusir: min=0.9015, max=2.644, mean=1.71, median=1.596
exirus: min=0.3782, max=1.1093, mean=0.62, median=0.6266
exitus: min=553.1, max=2159.0, mean=1213.29, median=1267.0
exneus: min=1.5192, max=3.9145, mean=2.34, median=2.15
expous: min=21.98, max=190.4, mean=110.26, median=138.775
exspus: min=55.54, max=191.57, mean=108.67, median=113.0
exusec: min=0.6476, max=1.4557, mean=1.14, median=1.158
execus: min=0.687, max=1.5442, mean=0.90, median=0.8636
dexuseu: min=0.827, max=1.601, mean=1.18, median=1.1740499999999998
dexeuus: min=0.6246096189881324, max=1.2091898428053205, mean=0.86, median=0.8517524822739285
dtwexb: min=89.0259, max=131.8808, mean=111.13, median=111.19715
dtwexbgs: min=85.4692, max=130.2142, mean=105.27, median=107.1343
dtwexm: min=68.0137, max=148.1244, mean=94.09, median=92.58865
dtwexafegs: min=81.3834, max=124.9301, mean=101.21, median=103.1372
dtwexo: min=89.0787, max=175.0065, mean=133.45, median=132.75965000000002
dtwexemegs: min=89.1519, max=139.7151, mean=110.67, median=108.3955
indexgx: min=78.4524, max=164.7242, mean=101.64, median=97.59845
```

### Date/Datetime Column Statistics
```
date: min=1971-01-04 00:00:00, max=2025-02-07 00:00:00
```

---

## fx_monthly_data.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/foreign_exchange/fx_monthly_data.parquet`
**Size:** 210726 bytes | **Type:** Parquet | **Shape:** 649 rows × 48 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
exusal                                   Float64        
exalus                                   Float64        
exbzus                                   Float64         (44.4% null)
excaus                                   Float64        
exchus                                   Float64         (18.5% null)
exdnus                                   Float64        
exhkus                                   Float64         (18.5% null)
exinus                                   Float64         (3.7% null)
exjpus                                   Float64        
exkous                                   Float64         (19.0% null)
exmaus                                   Float64        
exmxus                                   Float64         (42.2% null)
exusnz                                   Float64        
exnzus                                   Float64        
exnous                                   Float64        
exsius                                   Float64         (18.5% null)
exsfus                                   Float64        
exslus                                   Float64         (3.7% null)
exsdus                                   Float64        
exszus                                   Float64        
extaus                                   Float64         (23.6% null)
exthus                                   Float64         (18.5% null)
exusuk                                   Float64        
exukus                                   Float64        
exvzus                                   Float64         (44.4% null)
exauus                                   Float64         (48.2% null)
exbeus                                   Float64         (48.2% null)
exfnus                                   Float64         (48.2% null)
exfrus                                   Float64         (48.2% null)
exgeus                                   Float64         (48.2% null)
exgrus                                   Float64         (63.5% null)
exusir                                   Float64         (48.2% null)
exirus                                   Float64         (48.2% null)
exitus                                   Float64         (48.2% null)
exneus                                   Float64         (48.2% null)
expous                                   Float64         (51.9% null)
exspus                                   Float64         (51.9% null)
exusec                                   Float64         (62.9% null)
execus                                   Float64         (62.9% null)
exuseu                                   Float64         (51.8% null)
exeuus                                   Float64         (51.8% null)
twexbmth                                 Float64         (13.1% null)
twexbgsmth                               Float64         (64.7% null)
twexmmth                                 Float64         (13.1% null)
twexafegsmth                             Float64         (64.7% null)
twexomth                                 Float64         (13.1% null)
twexemegsmth                             Float64         (64.7% null)
```

### Numeric Column Statistics
```
exusal: min=0.5016, max=1.4855, mean=0.85, median=0.7717
exalus: min=0.6731740154830024, max=1.993620414673046, mean=1.24, median=1.2958403524685758
exbzus: min=0.8412, max=6.101, mean=2.78, median=2.3251
excaus: min=0.9553, max=1.5997, mean=1.23, median=1.2353
exchus: min=1.5518, max=8.7251, mean=6.27, median=6.7352
exdnus: min=4.7335, max=11.8071, mean=6.63, median=6.4083
exhkus: min=5.1825, max=8.0948, mean=7.68, median=7.7734
exinus: min=7.2719, max=86.2652, mean=37.41, median=40.2738
exjpus: min=76.643, max=358.02, mean=156.57, median=122.6886
exkous: min=669.2476, max=1707.3, mean=1020.10, median=1072.59665
exmaus: min=2.122, max=4.7655, mean=3.16, median=3.048
exmxus: min=3.1078, max=24.1798, mean=13.07, median=12.2366
exusnz: min=0.399, max=1.4864, mean=0.73, median=0.6745
exnzus: min=0.6727664155005383, max=2.506265664160401, mean=1.47, median=1.4825796886582654
exnous: min=4.8167, max=11.3335, mean=7.02, median=6.7496
exsius: min=1.2089, max=2.2582, mean=1.62, median=1.5755
exsfus: min=0.6679, max=19.0322, mean=6.24, median=4.9337
exslus: min=6.0467, max=363.945, mean=88.15, median=68.6295
exsdus: min=3.9166, max=11.1111, mean=7.13, median=7.189
exszus: min=0.78, max=4.3053, mean=1.58, median=1.4111
extaus: min=24.7695, max=40.5006, mean=31.04, median=30.8355
exthus: min=20.5491, max=52.9825, mean=31.55, median=31.506
exusuk: min=1.0931, max=2.6181, mean=1.68, median=1.6145
exukus: min=0.3819563805813376, max=0.9148293843198244, mean=0.62, median=0.6193868070610096
exvzus: min=0.17, max=4191337.2125, mean=100363.82, median=3.6137
exauus: min=9.72, max=25.873, mean=15.24, median=13.922
exbeus: min=27.96, max=66.31, mean=38.63, median=36.805
exfnus: min=3.4926, max=6.8616, mean=4.53, median=4.28285
exfrus: min=4.0048, max=10.0933, mean=5.67, median=5.50065
exgeus: min=1.3812, max=3.637, mean=2.15, median=1.94815
exgrus: min=53.18, max=398.29, mean=189.65, median=170.42
exusir: min=0.9423, max=2.6181, mean=1.71, median=1.5941
exirus: min=0.382, max=1.0612, mean=0.62, median=0.6273
exitus: min=565.26, max=2078.5, mean=1212.33, median=1263.19
exneus: min=1.5474, max=3.7387, mean=2.34, median=2.1525
expous: min=22.41, max=187.03, mean=110.07, median=138.87
exspus: min=55.8, max=183.13, mean=108.62, median=112.66499999999999
exusec: min=0.6752, max=1.4435, mean=1.14, median=1.1575
execus: min=0.6928, max=1.481, mean=0.91, median=0.8639
exuseu: min=0.8525, max=1.5759, mean=1.18, median=1.1743
exeuus: min=0.6345580303318739, max=1.1730205278592374, mean=0.86, median=0.8515711487694798
twexbmth: min=30.638, max=130.7506, mean=84.46, median=95.53444999999999
twexbgsmth: min=86.3178, max=129.0413, mean=105.31, median=107.65
twexmmth: min=69.0608, max=143.9059, mean=94.12, median=92.5692
twexafegsmth: min=82.6783, max=123.1599, mean=101.24, median=103.1943
twexomth: min=1.9979, max=172.8066, mean=80.26, median=98.3551
twexemegsmth: min=89.8244, max=138.5574, mean=110.73, median=108.8631
```

### Date/Datetime Column Statistics
```
date: min=1971-01-31 00:00:00, max=2025-01-31 00:00:00
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

## wrds_futures.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/futures_returns/wrds_futures.parquet`
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

## He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/he_kelly_manela/He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv`
**Size:** 729670 bytes | **Type:** Csv | **Shape:** 516 rows × 257 columns

### Columns
```
yyyymm                                   Float64        
intermediary_capital_ratio               Float64        
intermediary_leverage_ratio_squared      Float64        
intermediary_capital_risk_factor         Float64        
intermediary_value_weighted_investment_return Float64        
mkt_rf                                   Float64        
smb                                      Float64        
hml                                      Float64        
rf                                       Float64        
FF25_01                                  Float64        
FF25_02                                  Float64        
FF25_03                                  Float64        
FF25_04                                  Float64        
FF25_05                                  Float64        
FF25_06                                  Float64        
FF25_07                                  Float64        
FF25_08                                  Float64        
FF25_09                                  Float64        
FF25_10                                  Float64        
FF25_11                                  Float64        
FF25_12                                  Float64        
FF25_13                                  Float64        
FF25_14                                  Float64        
FF25_15                                  Float64        
FF25_16                                  Float64        
FF25_17                                  Float64        
FF25_18                                  Float64        
FF25_19                                  Float64        
FF25_20                                  Float64        
FF25_21                                  Float64        
FF25_22                                  Float64        
FF25_23                                  Float64        
FF25_24                                  Float64        
FF25_25                                  Float64        
US_bonds_01                              Float64         (4.8% null)
US_bonds_02                              Float64         (4.8% null)
US_bonds_03                              Float64         (4.8% null)
US_bonds_04                              Float64         (4.8% null)
US_bonds_05                              Float64         (4.8% null)
US_bonds_06                              Float64         (4.8% null)
US_bonds_07                              Float64         (4.8% null)
US_bonds_08                              Float64         (4.8% null)
US_bonds_09                              Float64         (4.8% null)
US_bonds_10                              Float64         (4.8% null)
US_bonds_11                              Float64         (11.6% null)
US_bonds_12                              Float64         (11.6% null)
US_bonds_13                              Float64         (11.6% null)
US_bonds_14                              Float64         (11.6% null)
US_bonds_15                              Float64         (11.6% null)
US_bonds_16                              Float64         (11.6% null)
US_bonds_17                              Float64         (11.6% null)
US_bonds_18                              Float64         (11.6% null)
US_bonds_19                              Float64         (11.6% null)
US_bonds_20                              Float64         (11.6% null)
Sov_bonds_01                             String          (62.0% null)
Sov_bonds_02                             String          (62.0% null)
Sov_bonds_03                             String          (62.0% null)
Sov_bonds_04                             String          (62.0% null)
Sov_bonds_05                             String          (62.0% null)
Sov_bonds_06                             String          (62.0% null)
Options_01                               String          (39.9% null)
Options_02                               String          (39.9% null)
Options_03                               String          (39.9% null)
Options_04                               String          (39.9% null)
Options_05                               String          (39.9% null)
Options_06                               String          (39.9% null)
Options_07                               String          (39.9% null)
Options_08                               String          (39.9% null)
Options_09                               String          (39.9% null)
Options_10                               String          (39.9% null)
Options_11                               String          (39.9% null)
Options_12                               String          (39.9% null)
Options_13                               String          (39.9% null)
Options_14                               String          (39.9% null)
Options_15                               String          (39.9% null)
Options_16                               String          (39.9% null)
Options_17                               String          (39.9% null)
Options_18                               String          (39.9% null)
CDS_01                                   String          (72.3% null)
CDS_02                                   String          (72.3% null)
CDS_03                                   String          (72.3% null)
CDS_04                                   String          (72.3% null)
CDS_05                                   String          (72.3% null)
CDS_06                                   String          (72.3% null)
CDS_07                                   String          (72.3% null)
CDS_08                                   String          (72.3% null)
CDS_09                                   String          (72.3% null)
CDS_10                                   String          (72.3% null)
CDS_11                                   String          (72.3% null)
CDS_12                                   String          (72.3% null)
CDS_13                                   String          (72.3% null)
CDS_14                                   String          (72.3% null)
CDS_15                                   String          (72.3% null)
CDS_16                                   String          (72.3% null)
CDS_17                                   String          (72.3% null)
CDS_18                                   String          (72.3% null)
CDS_19                                   String          (72.3% null)
CDS_20                                   String          (72.3% null)
Commod_01                                String          (38.8% null)
Commod_02                                String          (38.8% null)
Commod_03                                String          (38.8% null)
Commod_04                                String          (38.8% null)
Commod_05                                String          (38.8% null)
Commod_06                                String          (38.8% null)
Commod_07                                String          (38.8% null)
Commod_08                                String          (38.8% null)
Commod_09                                String          (38.8% null)
Commod_10                                String          (38.8% null)
Commod_11                                String          (38.8% null)
Commod_12                                String          (38.8% null)
Commod_13                                String          (38.8% null)
Commod_14                                String          (38.8% null)
Commod_15                                String          (38.8% null)
Commod_16                                String          (38.8% null)
Commod_17                                String          (38.8% null)
Commod_18                                String          (38.8% null)
Commod_19                                String          (38.8% null)
Commod_20                                String          (38.8% null)
Commod_21                                String          (38.8% null)
Commod_22                                String          (38.8% null)
Commod_23                                String          (38.8% null)
FX_01                                    Float64         (21.1% null)
FX_02                                    Float64         (21.1% null)
FX_03                                    Float64         (21.1% null)
FX_04                                    Float64         (21.1% null)
FX_05                                    Float64         (21.1% null)
FX_06                                    Float64         (21.1% null)
FX_07                                    Float64         (21.1% null)
FX_08                                    Float64         (21.1% null)
FX_09                                    Float64         (21.1% null)
FX_10                                    Float64         (21.1% null)
FX_11                                    Float64         (21.1% null)
FX_12                                    Float64         (21.1% null)
All_01                                   Float64        
All_02                                   Float64        
All_03                                   Float64        
All_04                                   Float64        
All_05                                   Float64        
All_06                                   Float64        
All_07                                   Float64        
All_08                                   Float64        
All_09                                   Float64        
All_10                                   Float64        
All_11                                   Float64        
All_12                                   Float64        
All_13                                   Float64        
All_14                                   Float64        
All_15                                   Float64        
All_16                                   Float64        
All_17                                   Float64        
All_18                                   Float64        
All_19                                   Float64        
All_20                                   Float64        
All_21                                   Float64        
All_22                                   Float64        
All_23                                   Float64        
All_24                                   Float64        
All_25                                   Float64        
All_26                                   Float64         (4.8% null)
All_27                                   Float64         (4.8% null)
All_28                                   Float64         (4.8% null)
All_29                                   Float64         (4.8% null)
All_30                                   Float64         (4.8% null)
All_31                                   Float64         (4.8% null)
All_32                                   Float64         (4.8% null)
All_33                                   Float64         (4.8% null)
All_34                                   Float64         (4.8% null)
All_35                                   Float64         (4.8% null)
All_36                                   Float64         (11.6% null)
All_37                                   Float64         (11.6% null)
All_38                                   Float64         (11.6% null)
All_39                                   Float64         (11.6% null)
All_40                                   Float64         (11.6% null)
All_41                                   Float64         (11.6% null)
All_42                                   Float64         (11.6% null)
All_43                                   Float64         (11.6% null)
All_44                                   Float64         (11.6% null)
All_45                                   Float64         (11.6% null)
All_46                                   String          (62.0% null)
All_47                                   String          (62.0% null)
All_48                                   String          (62.0% null)
All_49                                   String          (62.0% null)
All_50                                   String          (62.0% null)
All_51                                   String          (62.0% null)
All_52                                   String          (39.9% null)
All_53                                   String          (39.9% null)
All_54                                   String          (39.9% null)
All_55                                   String          (39.9% null)
All_56                                   String          (39.9% null)
All_57                                   String          (39.9% null)
All_58                                   String          (39.9% null)
All_59                                   String          (39.9% null)
All_60                                   String          (39.9% null)
All_61                                   String          (39.9% null)
All_62                                   String          (39.9% null)
All_63                                   String          (39.9% null)
All_64                                   String          (39.9% null)
All_65                                   String          (39.9% null)
All_66                                   String          (39.9% null)
All_67                                   String          (39.9% null)
All_68                                   String          (39.9% null)
All_69                                   String          (39.9% null)
All_70                                   String          (72.3% null)
All_71                                   String          (72.3% null)
All_72                                   String          (72.3% null)
All_73                                   String          (72.3% null)
All_74                                   String          (72.3% null)
All_75                                   String          (72.3% null)
All_76                                   String          (72.3% null)
All_77                                   String          (72.3% null)
All_78                                   String          (72.3% null)
All_79                                   String          (72.3% null)
All_80                                   String          (72.3% null)
All_81                                   String          (72.3% null)
All_82                                   String          (72.3% null)
All_83                                   String          (72.3% null)
All_84                                   String          (72.3% null)
All_85                                   String          (72.3% null)
All_86                                   String          (72.3% null)
All_87                                   String          (72.3% null)
All_88                                   String          (72.3% null)
All_89                                   String          (72.3% null)
All_90                                   String          (38.8% null)
All_91                                   String          (38.8% null)
All_92                                   String          (38.8% null)
All_93                                   String          (38.8% null)
All_94                                   String          (38.8% null)
All_95                                   String          (38.8% null)
All_96                                   String          (38.8% null)
All_97                                   String          (38.8% null)
All_98                                   String          (38.8% null)
All_99                                   String          (38.8% null)
All_100                                  String          (38.8% null)
All_101                                  String          (38.8% null)
All_102                                  String          (38.8% null)
All_103                                  String          (38.8% null)
All_104                                  String          (38.8% null)
All_105                                  String          (38.8% null)
All_106                                  String          (38.8% null)
All_107                                  String          (38.8% null)
All_108                                  String          (38.8% null)
All_109                                  String          (38.8% null)
All_110                                  String          (38.8% null)
All_111                                  String          (38.8% null)
All_112                                  String          (38.8% null)
All_113                                  Float64         (21.1% null)
All_114                                  Float64         (21.1% null)
All_115                                  Float64         (21.1% null)
All_116                                  Float64         (21.1% null)
All_117                                  Float64         (21.1% null)
All_118                                  Float64         (21.1% null)
All_119                                  Float64         (21.1% null)
All_120                                  Float64         (21.1% null)
All_121                                  Float64         (21.1% null)
All_122                                  Float64         (21.1% null)
All_123                                  Float64         (21.1% null)
All_124                                  Float64         (21.1% null)
```

### Numeric Column Statistics
```
yyyymm: min=197001.0, max=201212.0, mean=199106.50, median=199106.5
intermediary_capital_ratio: min=0.0223, max=0.134, mean=0.06, median=0.0544
intermediary_leverage_ratio_squared: min=55.7145, max=2012.9658, mean=383.08, median=337.98879999999997
intermediary_capital_risk_factor: min=-0.2795, max=0.3965, mean=-0.00, median=0.0006000000000000001
intermediary_value_weighted_investment_return: min=-0.2811, max=0.3055, mean=0.01, median=0.00865
mkt_rf: min=-0.2324, max=0.161, mean=0.00, median=0.008400000000000001
smb: min=-0.1639, max=0.2202, mean=0.00, median=5e-05
hml: min=-0.1268, max=0.1387, mean=0.00, median=0.0039
rf: min=0.0, max=0.0135, mean=0.00, median=0.0042
FF25_01: min=-0.3423, max=0.3978, mean=0.00, median=0.009049999999999999
FF25_02: min=-0.3094, max=0.3862, mean=0.01, median=0.01395
FF25_03: min=-0.2865, max=0.2813, mean=0.01, median=0.012549999999999999
FF25_04: min=-0.2889, max=0.2778, mean=0.01, median=0.0153
FF25_05: min=-0.2887, max=0.3327, mean=0.01, median=0.014450000000000001
FF25_06: min=-0.3271, max=0.2692, mean=0.01, median=0.013399999999999999
FF25_07: min=-0.3163, max=0.2612, mean=0.01, median=0.0155
FF25_08: min=-0.2776, max=0.2634, mean=0.01, median=0.0149
FF25_09: min=-0.2604, max=0.2734, mean=0.01, median=0.01575
FF25_10: min=-0.2884, max=0.3004, mean=0.01, median=0.01795
FF25_11: min=-0.2963, max=0.2458, mean=0.01, median=0.0156
FF25_12: min=-0.2915, max=0.2503, mean=0.01, median=0.0126
FF25_13: min=-0.245, max=0.2194, mean=0.01, median=0.014499999999999999
FF25_14: min=-0.2282, max=0.234, mean=0.01, median=0.01395
FF25_15: min=-0.2617, max=0.292, mean=0.01, median=0.01625
FF25_16: min=-0.2594, max=0.2582, mean=0.01, median=0.011
FF25_17: min=-0.2883, max=0.2045, mean=0.01, median=0.011699999999999999
FF25_18: min=-0.2595, max=0.2401, mean=0.01, median=0.014450000000000001
FF25_19: min=-0.2102, max=0.2432, mean=0.01, median=0.0149
FF25_20: min=-0.2384, max=0.279, mean=0.01, median=0.015050000000000001
FF25_21: min=-0.2164, max=0.2235, mean=0.01, median=0.0089
FF25_22: min=-0.2242, max=0.1653, mean=0.01, median=0.0111
FF25_23: min=-0.2165, max=0.1908, mean=0.01, median=0.0117
FF25_24: min=-0.1932, max=0.1976, mean=0.01, median=0.01005
FF25_25: min=-0.1913, max=0.1757, mean=0.01, median=0.0119
US_bonds_01: min=-0.0003, max=0.0242, mean=0.00, median=0.0046
US_bonds_02: min=-0.0087, max=0.0451, mean=0.00, median=0.0044
US_bonds_03: min=-0.0245, max=0.0641, mean=0.01, median=0.0045
US_bonds_04: min=-0.0347, max=0.0732, mean=0.01, median=0.0045
US_bonds_05: min=-0.0463, max=0.0918, mean=0.01, median=0.0049
US_bonds_06: min=-0.0527, max=0.0954, mean=0.01, median=0.005
US_bonds_07: min=-0.0541, max=0.0863, mean=0.01, median=0.0053
US_bonds_08: min=-0.0601, max=0.0931, mean=0.01, median=0.0057
US_bonds_09: min=-0.0578, max=0.0938, mean=0.01, median=0.0062
US_bonds_10: min=-0.058, max=0.1211, mean=0.01, median=0.006
US_bonds_11: min=-0.0788, max=0.1274, mean=0.01, median=0.006200000000000001
US_bonds_12: min=-0.0764, max=0.1243, mean=0.01, median=0.0064
US_bonds_13: min=-0.0783, max=0.1326, mean=0.01, median=0.0063
US_bonds_14: min=-0.0786, max=0.1207, mean=0.01, median=0.0067
US_bonds_15: min=-0.0818, max=0.1268, mean=0.01, median=0.0069
US_bonds_16: min=-0.0802, max=0.1293, mean=0.01, median=0.00725
US_bonds_17: min=-0.0817, max=0.1257, mean=0.01, median=0.0076
US_bonds_18: min=-0.0835, max=0.1288, mean=0.01, median=0.0079
US_bonds_19: min=-0.0872, max=0.1103, mean=0.01, median=0.00795
US_bonds_20: min=-0.1021, max=0.1483, mean=0.01, median=0.01
FX_01: min=-0.1414, max=0.112, mean=-0.00, median=-0.0024
FX_02: min=-0.1344, max=0.0689, mean=-0.00, median=0.0017
FX_03: min=-0.1099, max=0.0741, mean=0.00, median=0.001
FX_04: min=-0.1011, max=0.1058, mean=0.00, median=0.0016
FX_05: min=-0.1376, max=0.0917, mean=0.00, median=0.0012
FX_06: min=-0.1109, max=0.0954, mean=0.00, median=0.0045
FX_07: min=-0.1061, max=0.0635, mean=-0.00, median=-0.0009
FX_08: min=-0.1001, max=0.0756, mean=0.00, median=0.001
FX_09: min=-0.0862, max=0.072, mean=0.00, median=0.0015
FX_10: min=-0.0764, max=0.0722, mean=0.00, median=0.0027
FX_11: min=-0.1177, max=0.0838, mean=0.00, median=0.0032
FX_12: min=-0.0849, max=0.1822, mean=0.01, median=0.0067
All_01: min=-0.3423, max=0.3978, mean=0.00, median=0.009049999999999999
All_02: min=-0.3094, max=0.3862, mean=0.01, median=0.01395
All_03: min=-0.2865, max=0.2813, mean=0.01, median=0.012549999999999999
All_04: min=-0.2889, max=0.2778, mean=0.01, median=0.0153
All_05: min=-0.2887, max=0.3327, mean=0.01, median=0.014450000000000001
All_06: min=-0.3271, max=0.2692, mean=0.01, median=0.013399999999999999
All_07: min=-0.3163, max=0.2612, mean=0.01, median=0.0155
All_08: min=-0.2776, max=0.2634, mean=0.01, median=0.0149
All_09: min=-0.2604, max=0.2734, mean=0.01, median=0.01575
All_10: min=-0.2884, max=0.3004, mean=0.01, median=0.01795
All_11: min=-0.2963, max=0.2458, mean=0.01, median=0.0156
All_12: min=-0.2915, max=0.2503, mean=0.01, median=0.0126
All_13: min=-0.245, max=0.2194, mean=0.01, median=0.014499999999999999
All_14: min=-0.2282, max=0.234, mean=0.01, median=0.01395
All_15: min=-0.2617, max=0.292, mean=0.01, median=0.01625
All_16: min=-0.2594, max=0.2582, mean=0.01, median=0.011
All_17: min=-0.2883, max=0.2045, mean=0.01, median=0.011699999999999999
All_18: min=-0.2595, max=0.2401, mean=0.01, median=0.014450000000000001
All_19: min=-0.2102, max=0.2432, mean=0.01, median=0.0149
All_20: min=-0.2384, max=0.279, mean=0.01, median=0.015050000000000001
All_21: min=-0.2164, max=0.2235, mean=0.01, median=0.0089
All_22: min=-0.2242, max=0.1653, mean=0.01, median=0.0111
All_23: min=-0.2165, max=0.1908, mean=0.01, median=0.0117
All_24: min=-0.1932, max=0.1976, mean=0.01, median=0.01005
All_25: min=-0.1913, max=0.1757, mean=0.01, median=0.0119
All_26: min=-0.0003, max=0.0242, mean=0.00, median=0.0046
All_27: min=-0.0087, max=0.0451, mean=0.00, median=0.0044
All_28: min=-0.0245, max=0.0641, mean=0.01, median=0.0045
All_29: min=-0.0347, max=0.0732, mean=0.01, median=0.0045
All_30: min=-0.0463, max=0.0918, mean=0.01, median=0.0049
All_31: min=-0.0527, max=0.0954, mean=0.01, median=0.005
All_32: min=-0.0541, max=0.0863, mean=0.01, median=0.0053
All_33: min=-0.0601, max=0.0931, mean=0.01, median=0.0057
All_34: min=-0.0578, max=0.0938, mean=0.01, median=0.0062
All_35: min=-0.058, max=0.1211, mean=0.01, median=0.006
All_36: min=-0.0788, max=0.1274, mean=0.01, median=0.006200000000000001
All_37: min=-0.0764, max=0.1243, mean=0.01, median=0.0064
All_38: min=-0.0783, max=0.1326, mean=0.01, median=0.0063
All_39: min=-0.0786, max=0.1207, mean=0.01, median=0.0067
All_40: min=-0.0818, max=0.1268, mean=0.01, median=0.0069
All_41: min=-0.0802, max=0.1293, mean=0.01, median=0.00725
All_42: min=-0.0817, max=0.1257, mean=0.01, median=0.0076
All_43: min=-0.0835, max=0.1288, mean=0.01, median=0.0079
All_44: min=-0.0872, max=0.1103, mean=0.01, median=0.00795
All_45: min=-0.1021, max=0.1483, mean=0.01, median=0.01
All_113: min=-0.1414, max=0.112, mean=-0.00, median=-0.0024
All_114: min=-0.1344, max=0.0689, mean=-0.00, median=0.0017
All_115: min=-0.1099, max=0.0741, mean=0.00, median=0.001
All_116: min=-0.1011, max=0.1058, mean=0.00, median=0.0016
All_117: min=-0.1376, max=0.0917, mean=0.00, median=0.0012
All_118: min=-0.1109, max=0.0954, mean=0.00, median=0.0045
All_119: min=-0.1061, max=0.0635, mean=-0.00, median=-0.0009
All_120: min=-0.1001, max=0.0756, mean=0.00, median=0.001
All_121: min=-0.0862, max=0.072, mean=0.00, median=0.0015
All_122: min=-0.0764, max=0.0722, mean=0.00, median=0.0027
All_123: min=-0.1177, max=0.0838, mean=0.00, median=0.0032
All_124: min=-0.0849, max=0.1822, mean=0.01, median=0.0067
```

---

## He_Kelly_Manela_Factors_daily.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/he_kelly_manela/He_Kelly_Manela_Factors_daily.csv`
**Size:** 431266 bytes | **Type:** Csv | **Shape:** 4,766 rows × 5 columns

### Columns
```
yyyymmdd                                 Int64          
intermediary_capital_ratio               Float64        
intermediary_capital_risk_factor         Float64         (0.0% null)
intermediary_value_weighted_investment_return Float64        
intermediary_leverage_ratio_squared      Float64        
```

### Numeric Column Statistics
```
yyyymmdd: min=20000103, max=20181211, mean=20090450.16, median=20090624.5
intermediary_capital_ratio: min=0.0145895067948756, max=0.17355099318704817, mean=0.08, median=0.07230790204221717
intermediary_capital_risk_factor: min=-0.16030051697835737, max=0.1805224049114429, mean=0.00, median=0.00024427127323118573
intermediary_value_weighted_investment_return: min=-0.1183881055505066, max=0.19350923576363566, mean=0.00, median=0.00025370052227591255
intermediary_leverage_ratio_squared: min=33.2005893688213, max=4698.062377977052, mean=310.19, median=191.26190829049523
```

---

## He_Kelly_Manela_Factors_monthly.csv
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/he_kelly_manela/He_Kelly_Manela_Factors_monthly.csv`
**Size:** 25659 bytes | **Type:** Csv | **Shape:** 587 rows × 5 columns

### Columns
```
yyyymm                                   Int64          
intermediary_capital_ratio               Float64        
intermediary_capital_risk_factor         Float64        
intermediary_value_weighted_investment_return Float64        
intermediary_leverage_ratio_squared      Float64        
```

### Numeric Column Statistics
```
yyyymm: min=197001, max=201811, mean=199402.40, median=199406.0
intermediary_capital_ratio: min=0.0223, max=0.134, mean=0.06, median=0.05817808372858584
intermediary_capital_risk_factor: min=-0.2795, max=0.3965, mean=0.00, median=0.0013
intermediary_value_weighted_investment_return: min=-0.2811, max=0.3055, mean=0.01, median=0.008758316861669169
intermediary_leverage_ratio_squared: min=55.7145, max=2012.9658, mean=368.19, median=295.44808224375043
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

## french_portfolios_25_daily_size_and_bm.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/ken_french_data_library/french_portfolios_25_daily_size_and_bm.parquet`
**Size:** 1.2 MB | **Type:** Parquet | **Shape:** 26,023 rows × 26 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
SMALL LoBM                               Float64        
ME1 BM2                                  Float64        
ME1 BM3                                  Float64        
ME1 BM4                                  Float64        
SMALL HiBM                               Float64        
ME2 BM1                                  Float64        
ME2 BM2                                  Float64        
ME2 BM3                                  Float64        
ME2 BM4                                  Float64        
ME2 BM5                                  Float64        
ME3 BM1                                  Float64        
ME3 BM2                                  Float64        
ME3 BM3                                  Float64        
ME3 BM4                                  Float64        
ME3 BM5                                  Float64        
ME4 BM1                                  Float64        
ME4 BM2                                  Float64        
ME4 BM3                                  Float64        
ME4 BM4                                  Float64        
ME4 BM5                                  Float64        
BIG LoBM                                 Float64        
ME5 BM2                                  Float64        
ME5 BM3                                  Float64        
ME5 BM4                                  Float64        
BIG HiBM                                 Float64        
```

### Numeric Column Statistics
```
SMALL LoBM: min=-0.9998999999999999, max=1.2793999999999999, mean=0.00, median=0.0005
ME1 BM2: min=-0.2692, max=0.4579, mean=0.00, median=0.0008
ME1 BM3: min=-0.1979, max=0.371, mean=0.00, median=0.0008
ME1 BM4: min=-0.1459, max=0.245, mean=0.00, median=0.0009
SMALL HiBM: min=-0.1868, max=0.2889, mean=0.00, median=0.001
ME2 BM1: min=-0.1545, max=0.2821, mean=0.00, median=0.0008
ME2 BM2: min=-0.1343, max=0.31, mean=0.00, median=0.0008
ME2 BM3: min=-0.147, max=0.19030000000000002, mean=0.00, median=0.0008
ME2 BM4: min=-0.1543, max=0.2991, mean=0.00, median=0.0008
ME2 BM5: min=-0.157, max=0.27, mean=0.00, median=0.0009
ME3 BM1: min=-0.145, max=0.1375, mean=0.00, median=0.0009
ME3 BM2: min=-0.14029999999999998, max=0.1564, mean=0.00, median=0.0008
ME3 BM3: min=-0.1942, max=0.2341, mean=0.00, median=0.0009
ME3 BM4: min=-0.1521, max=0.2339, mean=0.00, median=0.0008
ME3 BM5: min=-0.1911, max=0.3012, mean=0.00, median=0.0008
ME4 BM1: min=-0.191, max=0.1406, mean=0.00, median=0.0008
ME4 BM2: min=-0.16269999999999998, max=0.22760000000000002, mean=0.00, median=0.0008
ME4 BM3: min=-0.1572, max=0.256, mean=0.00, median=0.0008
ME4 BM4: min=-0.1384, max=0.2143, mean=0.00, median=0.0008
ME4 BM5: min=-0.1754, max=0.33640000000000003, mean=0.00, median=0.0007000000000000001
BIG LoBM: min=-0.1844, max=0.1358, mean=0.00, median=0.0006
ME5 BM2: min=-0.2054, max=0.1677, mean=0.00, median=0.0006
ME5 BM3: min=-0.1894, max=0.2078, mean=0.00, median=0.0005
ME5 BM4: min=-0.2041, max=0.2364, mean=0.00, median=0.0005
BIG HiBM: min=-0.1815, max=0.2396, mean=0.00, median=0.0004
```

### Date/Datetime Column Statistics
```
date: min=1926-07-01 00:00:00, max=2025-06-30 00:00:00
```

---

## french_portfolios_25_daily_size_and_inv.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/ken_french_data_library/french_portfolios_25_daily_size_and_inv.parquet`
**Size:** 752880 bytes | **Type:** Parquet | **Shape:** 15,603 rows × 26 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
SMALL LoINV                              Float64        
ME1 INV2                                 Float64        
ME1 INV3                                 Float64        
ME1 INV4                                 Float64        
SMALL HiINV                              Float64        
ME2 INV1                                 Float64        
ME2 INV2                                 Float64        
ME2 INV3                                 Float64        
ME2 INV4                                 Float64        
ME2 INV5                                 Float64        
ME3 INV1                                 Float64        
ME3 INV2                                 Float64        
ME3 INV3                                 Float64        
ME3 INV4                                 Float64        
ME3 INV5                                 Float64        
ME4 INV1                                 Float64        
ME4 INV2                                 Float64        
ME4 INV3                                 Float64        
ME4 INV4                                 Float64        
ME4 INV5                                 Float64        
BIG LoINV                                Float64        
ME5 INV2                                 Float64        
ME5 INV3                                 Float64        
ME5 INV4                                 Float64        
BIG HiINV                                Float64        
```

### Numeric Column Statistics
```
SMALL LoINV: min=-0.12560000000000002, max=0.1027, mean=0.00, median=0.0011
ME1 INV2: min=-0.1281, max=0.08310000000000001, mean=0.00, median=0.001
ME1 INV3: min=-0.12369999999999999, max=0.08900000000000001, mean=0.00, median=0.001
ME1 INV4: min=-0.1352, max=0.08710000000000001, mean=0.00, median=0.0009
SMALL HiINV: min=-0.1328, max=0.10980000000000001, mean=0.00, median=0.001
ME2 INV1: min=-0.1305, max=0.0967, mean=0.00, median=0.001
ME2 INV2: min=-0.141, max=0.10300000000000001, mean=0.00, median=0.0009
ME2 INV3: min=-0.128, max=0.087, mean=0.00, median=0.0009
ME2 INV4: min=-0.1354, max=0.09939999999999999, mean=0.00, median=0.0009
ME2 INV5: min=-0.1501, max=0.10460000000000001, mean=0.00, median=0.001
ME3 INV1: min=-0.1483, max=0.1108, mean=0.00, median=0.0009
ME3 INV2: min=-0.1381, max=0.1, mean=0.00, median=0.0009
ME3 INV3: min=-0.133, max=0.1116, mean=0.00, median=0.0008
ME3 INV4: min=-0.1249, max=0.1025, mean=0.00, median=0.0009
ME3 INV5: min=-0.1549, max=0.1134, mean=0.00, median=0.0009
ME4 INV1: min=-0.18489999999999998, max=0.1072, mean=0.00, median=0.0008
ME4 INV2: min=-0.1411, max=0.12050000000000001, mean=0.00, median=0.0008
ME4 INV3: min=-0.14429999999999998, max=0.1035, mean=0.00, median=0.0008
ME4 INV4: min=-0.1489, max=0.10949999999999999, mean=0.00, median=0.0008
ME4 INV5: min=-0.1734, max=0.1298, mean=0.00, median=0.0008
BIG LoINV: min=-0.2089, max=0.1524, mean=0.00, median=0.0006
ME5 INV2: min=-0.1844, max=0.11289999999999999, mean=0.00, median=0.0005
ME5 INV3: min=-0.1999, max=0.109, mean=0.00, median=0.0005
ME5 INV4: min=-0.1953, max=0.1139, mean=0.00, median=0.0005
BIG HiINV: min=-0.17739999999999997, max=0.1349, mean=0.00, median=0.0006
```

### Date/Datetime Column Statistics
```
date: min=1963-07-01 00:00:00, max=2025-06-30 00:00:00
```

---

## french_portfolios_25_daily_size_and_op.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/ken_french_data_library/french_portfolios_25_daily_size_and_op.parquet`
**Size:** 754011 bytes | **Type:** Parquet | **Shape:** 15,603 rows × 26 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
SMALL LoOP                               Float64        
ME1 OP2                                  Float64        
ME1 OP3                                  Float64        
ME1 OP4                                  Float64        
SMALL HiOP                               Float64        
ME2 OP1                                  Float64        
ME2 OP2                                  Float64        
ME2 OP3                                  Float64        
ME2 OP4                                  Float64        
ME2 OP5                                  Float64        
ME3 OP1                                  Float64        
ME3 OP2                                  Float64        
ME3 OP3                                  Float64        
ME3 OP4                                  Float64        
ME3 OP5                                  Float64        
ME4 OP1                                  Float64        
ME4 OP2                                  Float64        
ME4 OP3                                  Float64        
ME4 OP4                                  Float64        
ME4 OP5                                  Float64        
BIG LoOP                                 Float64        
ME5 OP2                                  Float64        
ME5 OP3                                  Float64        
ME5 OP4                                  Float64        
BIG HiOP                                 Float64        
```

### Numeric Column Statistics
```
SMALL LoOP: min=-0.1334, max=0.0993, mean=0.00, median=0.0009
ME1 OP2: min=-0.1274, max=0.09609999999999999, mean=0.00, median=0.001
ME1 OP3: min=-0.1316, max=0.0919, mean=0.00, median=0.0009
ME1 OP4: min=-0.21719999999999998, max=0.3675, mean=0.00, median=0.001
SMALL HiOP: min=-0.1496, max=0.1041, mean=0.00, median=0.0011
ME2 OP1: min=-0.1394, max=0.09880000000000001, mean=0.00, median=0.001
ME2 OP2: min=-0.13390000000000002, max=0.0894, mean=0.00, median=0.0008
ME2 OP3: min=-0.1193, max=0.091, mean=0.00, median=0.0009
ME2 OP4: min=-0.1193, max=0.0984, mean=0.00, median=0.0009
ME2 OP5: min=-0.1432, max=0.1235, mean=0.00, median=0.0011
ME3 OP1: min=-0.16219999999999998, max=0.1043, mean=0.00, median=0.0009
ME3 OP2: min=-0.1371, max=0.10710000000000001, mean=0.00, median=0.0008
ME3 OP3: min=-0.14, max=0.114, mean=0.00, median=0.0008
ME3 OP4: min=-0.13699999999999998, max=0.1048, mean=0.00, median=0.0009
ME3 OP5: min=-0.1461, max=0.1292, mean=0.00, median=0.001
ME4 OP1: min=-0.1553, max=0.131, mean=0.00, median=0.0008
ME4 OP2: min=-0.1653, max=0.10869999999999999, mean=0.00, median=0.0008
ME4 OP3: min=-0.1433, max=0.1092, mean=0.00, median=0.0007000000000000001
ME4 OP4: min=-0.1691, max=0.1092, mean=0.00, median=0.0008
ME4 OP5: min=-0.1437, max=0.1124, mean=0.00, median=0.0009
BIG LoOP: min=-0.2059, max=0.154, mean=0.00, median=0.0005
ME5 OP2: min=-0.18460000000000001, max=0.1213, mean=0.00, median=0.0005
ME5 OP3: min=-0.20739999999999997, max=0.1109, mean=0.00, median=0.0005
ME5 OP4: min=-0.18989999999999999, max=0.1074, mean=0.00, median=0.0005
BIG HiOP: min=-0.1858, max=0.1363, mean=0.00, median=0.0006
```

### Date/Datetime Column Statistics
```
date: min=1963-07-01 00:00:00, max=2025-06-30 00:00:00
```

---

## french_portfolios_25_monthly_size_and_bm.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/ken_french_data_library/french_portfolios_25_monthly_size_and_bm.parquet`
**Size:** 304940 bytes | **Type:** Parquet | **Shape:** 1,188 rows × 26 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
SMALL LoBM                               Float64        
ME1 BM2                                  Float64        
ME1 BM3                                  Float64        
ME1 BM4                                  Float64        
SMALL HiBM                               Float64        
ME2 BM1                                  Float64        
ME2 BM2                                  Float64        
ME2 BM3                                  Float64        
ME2 BM4                                  Float64        
ME2 BM5                                  Float64        
ME3 BM1                                  Float64        
ME3 BM2                                  Float64        
ME3 BM3                                  Float64        
ME3 BM4                                  Float64        
ME3 BM5                                  Float64        
ME4 BM1                                  Float64        
ME4 BM2                                  Float64        
ME4 BM3                                  Float64        
ME4 BM4                                  Float64        
ME4 BM5                                  Float64        
BIG LoBM                                 Float64        
ME5 BM2                                  Float64        
ME5 BM3                                  Float64        
ME5 BM4                                  Float64        
BIG HiBM                                 Float64        
```

### Numeric Column Statistics
```
SMALL LoBM: min=-0.49472900000000003, max=1.478401, mean=0.01, median=0.0080745
ME1 BM2: min=-0.352371, max=1.2604680000000001, mean=0.01, median=0.0072510000000000005
ME1 BM3: min=-0.34326500000000004, max=0.828824, mean=0.01, median=0.0120065
ME1 BM4: min=-0.34978200000000004, max=1.048597, mean=0.01, median=0.013337
SMALL HiBM: min=-0.331102, max=0.9951730000000001, mean=0.02, median=0.013506500000000001
ME2 BM1: min=-0.324848, max=0.764962, mean=0.01, median=0.011373
ME2 BM2: min=-0.32177, max=0.7813880000000001, mean=0.01, median=0.0152125
ME2 BM3: min=-0.35196, max=0.755124, mean=0.01, median=0.0147225
ME2 BM4: min=-0.314326, max=0.80107, mean=0.01, median=0.0157025
ME2 BM5: min=-0.37953899999999996, max=0.899723, mean=0.01, median=0.0164745
ME3 BM1: min=-0.296956, max=0.569621, mean=0.01, median=0.0138485
ME3 BM2: min=-0.327129, max=0.410813, mean=0.01, median=0.014482499999999999
ME3 BM3: min=-0.31509, max=0.61247, mean=0.01, median=0.0142975
ME3 BM4: min=-0.350475, max=0.699311, mean=0.01, median=0.0152225
ME3 BM5: min=-0.358615, max=0.7378480000000001, mean=0.01, median=0.0139315
ME4 BM1: min=-0.314036, max=0.35469700000000004, mean=0.01, median=0.012522
ME4 BM2: min=-0.28685700000000003, max=0.56969, mean=0.01, median=0.013647
ME4 BM3: min=-0.307526, max=0.642951, mean=0.01, median=0.015027
ME4 BM4: min=-0.33862200000000003, max=0.689267, mean=0.01, median=0.0157445
ME4 BM5: min=-0.414556, max=0.866039, mean=0.01, median=0.016046499999999998
BIG LoBM: min=-0.284528, max=0.324293, mean=0.01, median=0.011678999999999998
ME5 BM2: min=-0.252044, max=0.39398000000000005, mean=0.01, median=0.011156
ME5 BM3: min=-0.32183799999999996, max=0.502782, mean=0.01, median=0.0117815
ME5 BM4: min=-0.367136, max=0.624421, mean=0.01, median=0.011085499999999998
BIG HiBM: min=-0.45555500000000004, max=0.9803919999999999, mean=0.01, median=0.0138665
```

### Date/Datetime Column Statistics
```
date: min=1926-07-01 00:00:00, max=2025-06-01 00:00:00
```

---

## french_portfolios_25_monthly_size_and_inv.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/ken_french_data_library/french_portfolios_25_monthly_size_and_inv.parquet`
**Size:** 194578 bytes | **Type:** Parquet | **Shape:** 744 rows × 26 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
SMALL LoINV                              Float64        
ME1 INV2                                 Float64        
ME1 INV3                                 Float64        
ME1 INV4                                 Float64        
SMALL HiINV                              Float64        
ME2 INV1                                 Float64        
ME2 INV2                                 Float64        
ME2 INV3                                 Float64        
ME2 INV4                                 Float64        
ME2 INV5                                 Float64        
ME3 INV1                                 Float64        
ME3 INV2                                 Float64        
ME3 INV3                                 Float64        
ME3 INV4                                 Float64        
ME3 INV5                                 Float64        
ME4 INV1                                 Float64        
ME4 INV2                                 Float64        
ME4 INV3                                 Float64        
ME4 INV4                                 Float64        
ME4 INV5                                 Float64        
BIG LoINV                                Float64        
ME5 INV2                                 Float64        
ME5 INV3                                 Float64        
ME5 INV4                                 Float64        
BIG HiINV                                Float64        
```

### Numeric Column Statistics
```
SMALL LoINV: min=-0.327046, max=0.44238999999999995, mean=0.01, median=0.0127755
ME1 INV2: min=-0.276557, max=0.267682, mean=0.01, median=0.013399999999999999
ME1 INV3: min=-0.284616, max=0.282749, mean=0.01, median=0.0161465
ME1 INV4: min=-0.300799, max=0.277328, mean=0.01, median=0.015130000000000001
SMALL HiINV: min=-0.32182499999999997, max=0.312182, mean=0.01, median=0.0081145
ME2 INV1: min=-0.300918, max=0.278108, mean=0.01, median=0.0157925
ME2 INV2: min=-0.277692, max=0.200152, mean=0.01, median=0.0158885
ME2 INV3: min=-0.256122, max=0.25766, mean=0.01, median=0.014023
ME2 INV4: min=-0.285565, max=0.276831, mean=0.01, median=0.0154245
ME2 INV5: min=-0.346901, max=0.27634000000000003, mean=0.01, median=0.012192999999999999
ME3 INV1: min=-0.273696, max=0.24623, mean=0.01, median=0.0151555
ME3 INV2: min=-0.270008, max=0.219544, mean=0.01, median=0.0150545
ME3 INV3: min=-0.23318899999999998, max=0.242726, mean=0.01, median=0.014238999999999998
ME3 INV4: min=-0.252253, max=0.246289, mean=0.01, median=0.015022500000000001
ME3 INV5: min=-0.30122699999999997, max=0.223137, mean=0.01, median=0.011324
ME4 INV1: min=-0.286492, max=0.218808, mean=0.01, median=0.015386500000000001
ME4 INV2: min=-0.23296299999999998, max=0.228431, mean=0.01, median=0.013876
ME4 INV3: min=-0.213447, max=0.229207, mean=0.01, median=0.0139215
ME4 INV4: min=-0.253423, max=0.19340900000000003, mean=0.01, median=0.012390000000000002
ME4 INV5: min=-0.27853300000000003, max=0.243443, mean=0.01, median=0.011656
BIG LoINV: min=-0.2043, max=0.23276, mean=0.01, median=0.012548499999999999
ME5 INV2: min=-0.179973, max=0.191565, mean=0.01, median=0.0102615
ME5 INV3: min=-0.190295, max=0.152946, mean=0.01, median=0.010758
ME5 INV4: min=-0.223614, max=0.195702, mean=0.01, median=0.0105155
BIG HiINV: min=-0.22681, max=0.23310199999999998, mean=0.01, median=0.0121585
```

### Date/Datetime Column Statistics
```
date: min=1963-07-01 00:00:00, max=2025-06-01 00:00:00
```

---

## french_portfolios_25_monthly_size_and_op.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/ken_french_data_library/french_portfolios_25_monthly_size_and_op.parquet`
**Size:** 194341 bytes | **Type:** Parquet | **Shape:** 744 rows × 26 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
SMALL LoOP                               Float64        
ME1 OP2                                  Float64        
ME1 OP3                                  Float64        
ME1 OP4                                  Float64        
SMALL HiOP                               Float64        
ME2 OP1                                  Float64        
ME2 OP2                                  Float64        
ME2 OP3                                  Float64        
ME2 OP4                                  Float64        
ME2 OP5                                  Float64        
ME3 OP1                                  Float64        
ME3 OP2                                  Float64        
ME3 OP3                                  Float64        
ME3 OP4                                  Float64        
ME3 OP5                                  Float64        
ME4 OP1                                  Float64        
ME4 OP2                                  Float64        
ME4 OP3                                  Float64        
ME4 OP4                                  Float64        
ME4 OP5                                  Float64        
BIG LoOP                                 Float64        
ME5 OP2                                  Float64        
ME5 OP3                                  Float64        
ME5 OP4                                  Float64        
BIG HiOP                                 Float64        
```

### Numeric Column Statistics
```
SMALL LoOP: min=-0.32557200000000003, max=0.422028, mean=0.01, median=0.00723
ME1 OP2: min=-0.283566, max=0.29440500000000003, mean=0.01, median=0.013572500000000001
ME1 OP3: min=-0.288344, max=0.267148, mean=0.01, median=0.015235499999999999
ME1 OP4: min=-0.292117, max=0.896401, mean=0.01, median=0.014085
SMALL HiOP: min=-0.326825, max=0.271516, mean=0.01, median=0.0144335
ME2 OP1: min=-0.330946, max=0.33029000000000003, mean=0.01, median=0.012119
ME2 OP2: min=-0.30593800000000004, max=0.262587, mean=0.01, median=0.0159475
ME2 OP3: min=-0.27133, max=0.250255, mean=0.01, median=0.0155665
ME2 OP4: min=-0.270295, max=0.280188, mean=0.01, median=0.01494
ME2 OP5: min=-0.328563, max=0.26802, mean=0.01, median=0.0160305
ME3 OP1: min=-0.336354, max=0.263965, mean=0.01, median=0.011667
ME3 OP2: min=-0.290374, max=0.218189, mean=0.01, median=0.013766500000000001
ME3 OP3: min=-0.241213, max=0.215368, mean=0.01, median=0.013724
ME3 OP4: min=-0.24647, max=0.22499199999999997, mean=0.01, median=0.013742
ME3 OP5: min=-0.277793, max=0.243126, mean=0.01, median=0.015418999999999999
ME4 OP1: min=-0.267613, max=0.202632, mean=0.01, median=0.012501
ME4 OP2: min=-0.229866, max=0.19933499999999998, mean=0.01, median=0.0139285
ME4 OP3: min=-0.233019, max=0.20671199999999998, mean=0.01, median=0.013684000000000002
ME4 OP4: min=-0.251339, max=0.191918, mean=0.01, median=0.013222000000000001
ME4 OP5: min=-0.25166, max=0.21343, mean=0.01, median=0.015137000000000001
BIG LoOP: min=-0.275389, max=0.219619, mean=0.01, median=0.010040499999999999
ME5 OP2: min=-0.198274, max=0.170909, mean=0.01, median=0.0099825
ME5 OP3: min=-0.20184999999999997, max=0.19799499999999998, mean=0.01, median=0.0122215
ME5 OP4: min=-0.185027, max=0.204984, mean=0.01, median=0.0119805
BIG HiOP: min=-0.223974, max=0.172439, mean=0.01, median=0.011029500000000001
```

### Date/Datetime Column Statistics
```
date: min=1963-07-01 00:00:00, max=2025-06-01 00:00:00
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

## nyu_call_report.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/nyu_call_report/nyu_call_report.parquet`
**Size:** 376.4 MB | **Type:** Parquet | **Shape:** 1,919,810 rows × 187 columns

### Columns
```
rssdid                                   String         
chartertype                              String          (0.0% null)
cert                                     String          (0.0% null)
bhcid                                    String          (0.0% null)
date                                     Datetime(time_unit='ns', time_zone=None)
name                                     String         
assets                                   Float64         (0.2% null)
reloans                                  Float64         (12.9% null)
cash                                     Float64         (0.5% null)
persloans                                Float64         (15.9% null)
agloans                                  Float64         (4.2% null)
subordinateddebt                         Float64         (3.7% null)
equity                                   Float64         (3.1% null)
demanddep                                Float64         (0.7% null)
transdep                                 Float64         (28.4% null)
brokereddep                              Float64         (27.2% null)
brokereddeple100k                        Float64         (32.6% null)
brokereddepeq100k                        Float64         (42.4% null)
timedepge100k                            Float64         (1.6% null)
timedeple100k                            Float64         (29.1% null)
cdge100k                                 Float64         (41.4% null)
timedepge250k                            Float64         (86.4% null)
timedeple250k                            Float64         (86.4% null)
ciloans                                  Float64         (0.5% null)
loans                                    Float64         (12.5% null)
loansnet                                 Float64         (0.2% null)
fedfundsrepoasset                        Float64         (0.2% null)
tradingassets                            Float64         (27.0% null)
securities                               Float64         (2.2% null)
securities_ammcost                       Float64         (55.1% null)
securitiesheldtomaturity                 Float64         (55.1% null)
securitiesavailableforsale               Float64         (55.1% null)
liabilities                              Float64         (0.5% null)
deposits                                 Float64         (3.0% null)
foreigndep                               Float64        
nonintbeardep                            Float64         (28.8% null)
intbeardep                               Float64         (28.8% null)
intbearfordep                            Float64         (98.6% null)
fedfundsrepoliab                         Float64         (0.2% null)
tradingliabilities                       Float64         (55.1% null)
otherborrowedmoney                       Float64         (12.3% null)
timesavdep                               Float64         (3.3% null)
nontransdep                              Float64         (26.8% null)
timedep                                  Float64         (29.1% null)
timedepuninsured                         Float64         (2.1% null)
savdep                                   Float64         (28.8% null)
totsavdep                                Float64         (29.1% null)
numemployees                             Float64         (19.3% null)
qavgbaldue                               Float64         (25.9% null)
qavgtreasuriesagencydebt                 Float64         (71.3% null)
qavgmbs                                  Float64         (71.3% null)
qavgothersecurities                      Float64         (71.3% null)
qavgtradingassets                        Float64         (73.2% null)
qavgfedfundsrepoasset                    Float64         (1.7% null)
qavgloans                                Float64         (4.2% null)
qavgreloans1to4fam                       Float64         (83.0% null)
qavgreloansother                         Float64         (83.0% null)
qavgagloans                              Float64         (76.7% null)
qavgciloans                              Float64         (67.7% null)
qavgpersccards                           Float64         (71.5% null)
qavgpersother                            Float64         (71.5% null)
qavgforloans                             Float64         (98.6% null)
qavgleases                               Float64         (38.1% null)
qavgassets                               Float64         (12.4% null)
qavgtransdep                             Float64         (38.1% null)
qavgsavdep                               Float64         (71.3% null)
qavgtimedepge100k                        Float64         (67.2% null)
qavgcdge100k                             Float64         (49.8% null)
qavgtimedeple100k                        Float64         (67.2% null)
qavgtimedeple250k                        Float64         (96.3% null)
qavgtimedepge250k                        Float64         (96.3% null)
qavgfordep                               Float64         (98.8% null)
qavgfedfundsrepoliab                     Float64         (12.6% null)
qavgtradingandotherborrowed              Float64         (55.5% null)
qavgpersloans                            Float64         (71.5% null)
qavgreloans                              Float64         (67.4% null)
qavgsecurities                           Float64         (71.3% null)
securities_less_3m                       Float64         (64.0% null)
securities_3m_1y                         Float64         (64.0% null)
securities_1y_3y                         Float64         (64.0% null)
securities_3y_5y                         Float64         (64.0% null)
securities_5y_15y                        Float64         (64.0% null)
securities_over_15y                      Float64         (64.0% null)
securitiestreasury_less_3m               Float64         (64.0% null)
securitiestreasury_3m_1y                 Float64         (64.0% null)
securitiestreasury_1y_3y                 Float64         (64.0% null)
securitiestreasury_3y_5y                 Float64         (64.0% null)
securitiestreasury_5y_15y                Float64         (64.0% null)
securitiestreasury_over_15y              Float64         (64.0% null)
securitiesrmbs_less_3m                   Float64         (64.0% null)
securitiesrmbs_3m_1y                     Float64         (64.0% null)
securitiesrmbs_1y_3y                     Float64         (64.0% null)
securitiesrmbs_3y_5y                     Float64         (64.0% null)
securitiesrmbs_5y_15y                    Float64         (64.0% null)
securitiesrmbs_over_15y                  Float64         (64.0% null)
securitiesothermbs_less_3y               Float64         (64.0% null)
securitiesothermbs_over_3y               Float64         (64.0% null)
loansleases_mat_less_1y                  Float64         (63.8% null)
securities_mat_less_1y                   Float64         (63.8% null)
resloans_less_3m                         Float64         (64.0% null)
resloans_3m_1y                           Float64         (64.0% null)
resloans_1y_3y                           Float64         (64.0% null)
resloans_3y_5y                           Float64         (64.0% null)
resloans_5y_15y                          Float64         (64.0% null)
resloans_over_15y                        Float64         (64.0% null)
loansleases_less_3m                      Float64         (64.0% null)
loansleases_3m_1y                        Float64         (64.0% null)
loansleases_1y_3y                        Float64         (64.0% null)
loansleases_3y_5y                        Float64         (64.0% null)
loansleases_5y_15y                       Float64         (64.0% null)
loansleases_over_15y                     Float64         (64.0% null)
timedeple100k_less_3m                    Float64         (67.7% null)
timedeple100k_3m_1y                      Float64         (67.7% null)
timedeple100k_1y_3y                      Float64         (67.7% null)
timedeple100k_over_3y                    Float64         (67.7% null)
timedeple100k_less_1y                    Float64         (67.6% null)
timedepge100k_less_3m                    Float64         (67.7% null)
timedepge100k_3m_1y                      Float64         (67.7% null)
timedepge100k_1y_3y                      Float64         (67.7% null)
timedepge100k_over_3y                    Float64         (67.7% null)
timedeple250k_less_3m                    Float64         (96.3% null)
timedeple250k_3m_1y                      Float64         (96.3% null)
timedeple250k_1y_3y                      Float64         (96.3% null)
timedeple250k_over_3y                    Float64         (96.3% null)
timedeple250k_less_1y                    Float64         (96.3% null)
timedepge250k_less_3m                    Float64         (96.3% null)
timedepge250k_3m_1y                      Float64         (96.3% null)
timedepge250k_1y_3y                      Float64         (96.3% null)
timedepge250k_over_3y                    Float64         (96.3% null)
interestratederivatives                  Float64         (59.8% null)
interestratederivatives_par              Float64         (87.3% null)
grosshedging                             Float64         (59.8% null)
fixedrateswaps                           Float64         (66.5% null)
totalswaps                               Float64         (32.6% null)
floatingrateswaps                        Float64         (66.5% null)
nethedging                               Float64         (66.5% null)
grosstrading                             Float64         (59.8% null)
year                                     String         
month                                    String         
quarter                                  String         
day                                      String         
dateq                                    Datetime(time_unit='ns', time_zone=None)
dividendoncommonstock                    Float64         (56.4% null)
exponpremises                            Float64         (25.2% null)
intanddivincsecurities                   Float64         (29.3% null)
intandnonintexp                          Float64         (25.1% null)
intexp                                   Float64         (28.8% null)
intexpalldep                             Float64         (25.5% null)
intexpdomdep                             Float64         (25.5% null)
intexpfedfundsrepoliab                   Float64         (25.3% null)
intexpfordep                             Float64         (0.6% null)
intexpsavdep                             Float64         (38.2% null)
intexpsubordinated                       Float64         (27.8% null)
intexpcdge100k                           Float64         (61.8% null)
intexptimedep                            Float64         (39.8% null)
intexptimedepge100k                      Float64         (68.9% null)
intexptimedeple100k                      Float64         (68.9% null)
intexptradingandborrowed                 Float64         (28.1% null)
intexptransdep                           Float64         (38.2% null)
intincagloans                            Float64         (76.8% null)
intincassets                             Float64         (28.8% null)
intincbaldue                             Float64         (25.2% null)
intincciloans                            Float64         (67.8% null)
intincfedfundsrepoasset                  Float64         (25.2% null)
intincforloans                           Float64         (98.8% null)
intincleases                             Float64         (25.7% null)
intincloans                              Float64         (25.5% null)
intincmbs                                Float64         (71.3% null)
intincpersother                          Float64         (71.6% null)
intincreloansother                       Float64         (83.0% null)
intincothersecurities                    Float64         (67.7% null)
intincpersccards                         Float64         (71.6% null)
intincpersloans                          Float64         (71.6% null)
intincreloans                            Float64         (67.5% null)
intinctreasuriesagencydebt               Float64         (71.3% null)
loanleaselossprovision                   Float64         (25.1% null)
netinc                                   Float64         (25.1% null)
intincnet                                Float64         (28.8% null)
nonintexp                                Float64         (28.8% null)
nonintinc                                Float64         (28.8% null)
operinc                                  Float64         (25.1% null)
salaries                                 Float64         (25.1% null)
domdepservicecharges                     Float64         (25.4% null)
tradingrevenue                           Float64         (71.5% null)
intincreloans1to4fam                     Float64         (83.0% null)
intexptimedeple250k                      Float64         (96.3% null)
intexptimedepge250k                      Float64         (96.3% null)
```

### Numeric Column Statistics
```
assets: min=0.0, max=2690959000.0, mean=825842.44, median=57515.0
reloans: min=0.0, max=477733526.0, mean=138734.47, median=11102.0
cash: min=-708.0, max=508253000.0, mean=84764.11, median=3221.0
persloans: min=0.0, max=167520368.0, mean=43189.48, median=3598.0
agloans: min=0.0, max=6508000.0, mean=4535.94, median=614.0
subordinateddebt: min=0.0, max=29191000.0, mean=6173.88, median=0.0
equity: min=-939749.0, max=256755000.0, mean=78660.31, median=5213.0
demanddep: min=0.0, max=1077952576.0, mean=101129.81, median=7171.0
transdep: min=0.0, max=436889000.0, mean=106318.22, median=16534.0
brokereddep: min=-5.0, max=127955391.0, mean=36338.69, median=0.0
brokereddeple100k: min=0.0, max=63525000.0, mean=12988.17, median=0.0
brokereddepeq100k: min=0.0, max=29231911.0, mean=4983.58, median=0.0
timedepge100k: min=0.0, max=143676362.0, mean=87254.75, median=5141.0
timedeple100k: min=0.0, max=117145420.0, mean=83614.56, median=18713.0
cdge100k: min=0.0, max=24393123.0, mean=22054.23, median=2334.0
timedepge250k: min=0.0, max=70785000.0, mean=81479.25, median=6604.0
timedeple250k: min=0.0, max=129245692.0, mean=194889.67, median=41434.0
ciloans: min=-1.0, max=189448000.0, mean=83002.67, median=4532.0
loans: min=0.0, max=755800605.0, mean=288709.07, median=26295.0
loansnet: min=-32633.0, max=1029545000.0, mean=420291.45, median=30511.0
fedfundsrepoasset: min=0.0, max=320811000.0, mean=38514.80, median=1075.0
tradingassets: min=-156.0, max=380337000.0, mean=60560.62, median=0.0
securities: min=0.0, max=470089000.0, mean=142718.53, median=13070.0
securities_ammcost: min=0.0, max=464284000.0, mean=269591.78, median=21978.0
securitiesheldtomaturity: min=0.0, max=254190000.0, mean=48051.89, median=10.0
securitiesavailableforsale: min=0.0, max=398870000.0, mean=222182.64, median=16200.0
liabilities: min=-43.0, max=2447353000.0, mean=719964.65, median=51650.0
deposits: min=-2139062144.0, max=1577444000.0, mean=375230.60, median=47874.0
foreigndep: min=0.0, max=589762000.0, mean=66805.66, median=0.0
nonintbeardep: min=0.0, max=560667000.0, mean=135453.07, median=8722.0
intbeardep: min=0.0, max=1063057000.0, mean=439633.01, median=53973.0
intbearfordep: min=0.0, max=520316000.0, mean=4459846.04, median=72823.0
fedfundsrepoliab: min=0.0, max=276478000.0, mean=50560.18, median=0.0
tradingliabilities: min=0.0, max=143684000.0, mean=45471.75, median=0.0
otherborrowedmoney: min=0.0, max=212698000.0, mean=69139.36, median=0.0
timesavdep: min=0.0, max=1274064000.0, mean=415974.57, median=39315.0
nontransdep: min=0.0, max=1247684000.0, mean=503475.20, median=44918.0
timedep: min=0.0, max=260821782.0, mean=151142.34, median=28639.0
timedepuninsured: min=0.0, max=143676362.0, mean=61605.06, median=4247.0
savdep: min=0.0, max=1144622000.0, mean=317335.58, median=14030.0
totsavdep: min=-126838.0, max=1211090000.0, mean=344011.58, median=22512.0
numemployees: min=-292.0, max=1607556.0, mean=192.82, median=31.0
qavgbaldue: min=-77.0, max=487713000.0, mean=69892.80, median=324.0
qavgtreasuriesagencydebt: min=0.0, max=147644000.0, mean=60008.69, median=6776.0
qavgmbs: min=0.0, max=345453000.0, mean=193314.31, median=4633.5
qavgothersecurities: min=0.0, max=171050000.0, mean=86569.90, median=5274.0
qavgtradingassets: min=-271.0, max=395964000.0, mean=109135.71, median=0.0
qavgfedfundsrepoasset: min=0.0, max=299806000.0, mean=35092.13, median=1426.0
qavgloans: min=0.0, max=890008000.0, mean=365467.30, median=30020.0
qavgreloans1to4fam: min=0.0, max=382413298.0, mean=352564.96, median=27267.0
qavgreloansother: min=0.0, max=146254000.0, mean=278353.52, median=41769.0
qavgagloans: min=0.0, max=6059000.0, mean=11917.71, median=1736.0
qavgciloans: min=0.0, max=241237000.0, mean=207808.72, median=11977.0
qavgpersccards: min=0.0, max=145955000.0, mean=69520.35, median=0.0
qavgpersother: min=0.0, max=91928000.0, mean=81730.16, median=3490.0
qavgforloans: min=-65143.0, max=333795000.0, mean=2002755.24, median=4258.0
qavgleases: min=-3753.0, max=25377000.0, mean=11222.95, median=0.0
qavgassets: min=0.0, max=2471436000.0, mean=765242.38, median=62124.0
qavgtransdep: min=0.0, max=270231000.0, mean=39734.36, median=7816.0
qavgsavdep: min=0.0, max=1099653000.0, mean=670795.29, median=27010.0
qavgtimedepge100k: min=0.0, max=140237656.0, mean=96464.89, median=13871.0
qavgcdge100k: min=0.0, max=24315430.0, mean=21066.66, median=2773.0
qavgtimedeple100k: min=0.0, max=127334276.0, mean=112919.04, median=24338.0
qavgtimedeple250k: min=0.0, max=87714000.0, mean=219044.87, median=38847.0
qavgtimedepge250k: min=0.0, max=60613090.0, mean=114751.17, median=8553.0
qavgfordep: min=0.0, max=535240000.0, mean=4942261.86, median=74518.0
qavgfedfundsrepoliab: min=0.0, max=277030000.0, mean=58482.67, median=0.0
qavgtradingandotherborrowed: min=0.0, max=187361000.0, mean=131037.86, median=2.0
qavgpersloans: min=0.0, max=203894000.0, mean=151250.51, median=3625.0
qavgreloans: min=0.0, max=478987000.0, mean=528229.85, median=72151.0
qavgsecurities: min=0.0, max=436703000.0, mean=339892.90, median=25022.0
securities_less_3m: min=0.0, max=106370361.0, mean=30368.04, median=601.0
securities_3m_1y: min=0.0, max=73541000.0, mean=14466.01, median=1208.0
securities_1y_3y: min=0.0, max=111517000.0, mean=30252.44, median=2893.0
securities_3y_5y: min=0.0, max=94822000.0, mean=25275.44, median=2446.0
securities_5y_15y: min=0.0, max=81775033.0, mean=57072.81, median=5497.0
securities_over_15y: min=0.0, max=317684000.0, mean=78495.98, median=320.0
securitiestreasury_less_3m: min=0.0, max=105938918.0, mean=27018.85, median=431.0
securitiestreasury_3m_1y: min=0.0, max=73284000.0, mean=12230.80, median=858.0
securitiestreasury_1y_3y: min=0.0, max=110811000.0, mean=27829.55, median=2501.0
securitiestreasury_3y_5y: min=0.0, max=93331000.0, mean=22037.67, median=2001.0
securitiestreasury_5y_15y: min=0.0, max=68811000.0, mean=30642.11, median=3252.0
securitiestreasury_over_15y: min=0.0, max=50687293.0, mean=12704.00, median=0.0
securitiesrmbs_less_3m: min=0.0, max=10184290.0, mean=3349.20, median=0.0
securitiesrmbs_3m_1y: min=0.0, max=3512483.0, mean=2235.21, median=0.0
securitiesrmbs_1y_3y: min=0.0, max=16306115.0, mean=2422.89, median=0.0
securitiesrmbs_3y_5y: min=0.0, max=61749128.0, mean=3237.77, median=0.0
securitiesrmbs_5y_15y: min=0.0, max=77485779.0, mean=26430.70, median=317.0
securitiesrmbs_over_15y: min=0.0, max=316462000.0, mean=65791.98, median=0.0
securitiesothermbs_less_3y: min=0.0, max=56098000.0, mean=18944.37, median=0.0
securitiesothermbs_over_3y: min=0.0, max=76242000.0, mean=40467.11, median=0.0
loansleases_mat_less_1y: min=0.0, max=343067000.0, mean=195540.26, median=17618.0
securities_mat_less_1y: min=0.0, max=92485000.0, mean=20537.43, median=1227.0
resloans_less_3m: min=0.0, max=65112000.0, mean=17677.91, median=986.0
resloans_3m_1y: min=0.0, max=23554000.0, mean=16126.16, median=1764.0
resloans_1y_3y: min=0.0, max=31765000.0, mean=19034.60, median=2873.0
resloans_3y_5y: min=0.0, max=31761000.0, mean=20922.30, median=1978.0
resloans_5y_15y: min=0.0, max=65545197.0, mean=39275.77, median=1447.0
resloans_over_15y: min=0.0, max=185277000.0, mean=66438.32, median=326.0
loansleases_less_3m: min=0.0, max=583445000.0, mean=389337.86, median=15307.0
loansleases_3m_1y: min=0.0, max=78364000.0, mean=68543.66, median=10647.5
loansleases_1y_3y: min=0.0, max=112295000.0, mean=107814.36, median=14210.0
loansleases_3y_5y: min=0.0, max=98491000.0, mean=97304.62, median=11707.0
loansleases_5y_15y: min=0.0, max=115264000.0, mean=106881.22, median=6610.0
loansleases_over_15y: min=0.0, max=202708000.0, mean=86232.95, median=1190.0
timedeple100k_less_3m: min=0.0, max=47259000.0, mean=27219.82, median=5716.0
timedeple100k_3m_1y: min=0.0, max=72801155.0, mean=49953.79, median=11375.0
timedeple100k_1y_3y: min=0.0, max=20275000.0, mean=25610.59, median=4603.0
timedeple100k_over_3y: min=0.0, max=17637000.0, mean=9611.55, median=674.0
timedeple100k_less_1y: min=0.0, max=108375017.0, mean=76406.80, median=17166.0
timedepge100k_less_3m: min=0.0, max=98667000.0, mean=44620.69, median=3810.0
timedepge100k_3m_1y: min=0.0, max=78616626.0, mean=33946.85, median=6446.0
timedepge100k_1y_3y: min=0.0, max=20604594.0, mean=14048.55, median=1980.0
timedepge100k_over_3y: min=0.0, max=10076000.0, mean=6613.55, median=300.0
timedeple250k_less_3m: min=0.0, max=18491000.0, mean=42490.74, median=7200.0
timedeple250k_3m_1y: min=0.0, max=37619000.0, mean=93975.09, median=16356.0
timedeple250k_1y_3y: min=0.0, max=28614000.0, mean=61004.03, median=9938.0
timedeple250k_over_3y: min=0.0, max=15008000.0, mean=24000.98, median=2252.0
timedeple250k_less_1y: min=0.0, max=50099000.0, mean=134230.38, median=23392.0
timedepge250k_less_3m: min=0.0, max=54639000.0, mean=65075.42, median=1532.0
timedepge250k_3m_1y: min=0.0, max=18425000.0, mean=31771.68, median=3480.0
timedepge250k_1y_3y: min=0.0, max=19013567.0, mean=12216.75, median=1570.0
timedepge250k_over_3y: min=0.0, max=51710000.0, mean=9032.62, median=256.0
interestratederivatives: min=0.0, max=2446245923.0, mean=279434.41, median=0.0
interestratederivatives_par: min=0.0, max=336151000.0, mean=137342.26, median=0.0
grosshedging: min=0.0, max=2446245923.0, mean=322885.89, median=0.0
fixedrateswaps: min=0.0, max=1314948769.0, mean=83095.03, median=0.0
totalswaps: min=0.0, max=59969864000.0, mean=6470696.29, median=0.0
floatingrateswaps: min=-5.0, max=59951858000.0, mean=11184368.95, median=0.0
nethedging: min=-59933852000.0, max=23553000.0, mean=-11101273.92, median=0.0
grosstrading: min=0.0, max=75137030000.0, mean=14965753.14, median=0.0
dividendoncommonstock: min=-3664770.0, max=11400000.0, mean=2553.04, median=0.0
exponpremises: min=-1435000.0, max=3247000.0, mean=830.23, median=76.0
intanddivincsecurities: min=-3952000.0, max=4186000.0, mean=1750.50, median=229.0
intandnonintexp: min=-23572000.0, max=20642000.0, mean=11551.80, median=1142.0
intexp: min=-10933000.0, max=13799000.0, mean=4142.82, median=480.0
intexpalldep: min=-7391000.0, max=7032000.0, mean=3100.19, median=450.0
intexpdomdep: min=-6367000.0, max=3557902.0, mean=2408.41, median=449.0
intexpfedfundsrepoliab: min=-594000.0, max=2896000.0, mean=434.13, median=0.0
intexpfordep: min=-1024000.0, max=5325000.0, mean=518.34, median=0.0
intexpsavdep: min=-1947000.0, max=1793000.0, mean=777.17, median=76.0
intexpsubordinated: min=-866000.0, max=552000.0, mean=99.78, median=0.0
intexpcdge100k: min=-84000.0, max=1101673.0, mean=535.49, median=55.0
intexptimedep: min=-4281000.0, max=2352550.0, mean=1452.85, median=296.0
intexptimedepge100k: min=-1888000.0, max=1276114.0, mean=673.47, median=97.0
intexptimedeple100k: min=-2393000.0, max=1640531.0, mean=900.84, median=178.0
intexptradingandborrowed: min=-2082000.0, max=6175000.0, mean=633.63, median=0.0
intexptransdep: min=-139000.0, max=1093000.0, mean=138.03, median=28.0
intincagloans: min=-688065.0, max=688569.0, mean=189.58, median=29.0
intincassets: min=-22972000.0, max=22379000.0, mean=11499.64, median=1285.0
intincbaldue: min=-391000.0, max=1546000.0, mean=311.03, median=3.0
intincciloans: min=-3609000.0, max=2536000.0, mean=3201.90, median=199.0
intincfedfundsrepoasset: min=-204000.0, max=3665000.0, mean=295.25, median=17.0
intincforloans: min=-691000.0, max=7593000.0, mean=40789.94, median=15.0
intincleases: min=-843000.0, max=637000.0, mean=151.32, median=0.0
intincloans: min=-18198000.0, max=18477000.0, mean=8531.87, median=907.0
intincmbs: min=-3222000.0, max=3983000.0, mean=1615.76, median=38.0
intincpersother: min=-2318000.0, max=1405000.0, mean=1220.38, median=68.0
intincreloansother: min=-2924000.0, max=1916977.0, mean=3398.19, median=596.0
intincothersecurities: min=-672000.0, max=1887000.0, mean=630.04, median=36.0
intincpersccards: min=-2527000.0, max=11317000.0, mean=2291.27, median=0.0
intincpersloans: min=-2492000.0, max=11479000.0, mean=3511.66, median=71.0
intincreloans: min=-10838000.0, max=10007000.0, mean=7621.88, median=1166.0
intinctreasuriesagencydebt: min=-239000.0, max=669000.0, mean=365.24, median=49.0
loanleaselossprovision: min=-9044000.0, max=9790785.0, mean=1247.54, median=25.0
netinc: min=-13469374.0, max=8833000.0, mean=2337.24, median=166.0
intincnet: min=-12039000.0, max=18662000.0, mean=7356.97, median=726.0
nonintexp: min=-12639000.0, max=16551000.0, mean=7310.88, median=583.0
nonintinc: min=-7074000.0, max=12466271.0, mean=4624.34, median=110.0
operinc: min=-30046000.0, max=33270000.0, mean=16052.01, median=1421.0
salaries: min=-4991000.0, max=7483000.0, mean=3148.13, median=289.0
domdepservicecharges: min=-2084000.0, max=2989434.0, mean=656.43, median=54.0
tradingrevenue: min=-7587000.0, max=5288000.0, mean=714.39, median=0.0
intincreloans1to4fam: min=-7914000.0, max=5820618.0, mean=3944.56, median=392.0
intexptimedeple250k: min=-16516.0, max=512000.0, mean=912.48, median=118.0
intexptimedepge250k: min=-4056.0, max=522042.0, mean=507.17, median=29.0
```

### Date/Datetime Column Statistics
```
date: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
dateq: min=1976-03-31 00:00:00, max=2020-03-31 00:00:00
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

## data_1996-01_2012-01.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/options/data_1996-01_2012-01.parquet`
**Size:** 58.6 MB | **Type:** Parquet | **Shape:** 3,410,570 rows × 15 columns

### Columns
```
secid                                    Float64        
date                                     Datetime(time_unit='ns', time_zone=None)
open                                     Float64        
close                                    Float64        
cp_flag                                  String         
exdate                                   Datetime(time_unit='ns', time_zone=None)
impl_volatility                          Float64         (7.1% null)
tb_m3                                    Float64         (0.8% null)
volume                                   Float64        
open_interest                            Float64        
best_bid                                 Float64        
best_offer                               Float64        
strike_price                             Float64        
contract_size                            Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
secid: min=108105.0, max=108105.0, mean=108105.00, median=108105.0
open: min=598.48, max=1564.98, mean=1160.29, median=1177.68
close: min=598.48, max=1565.15, mean=1160.47, median=1177.6
impl_volatility: min=0.02094, max=8.977526, mean=0.31, median=0.247122
tb_m3: min=0.0, max=6.24, mean=1.95, median=1.06
volume: min=0.0, max=200777.0, mean=381.46, median=0.0
open_interest: min=0.0, max=370769.0, mean=7069.23, median=564.0
best_bid: min=0.0, max=1916.3, mean=136.26, median=53.9
best_offer: min=0.05, max=1921.2, mean=138.52, median=56.6
strike_price: min=50000.0, max=3000000.0, mean=1100222.13, median=1110000.0
contract_size: min=100.0, max=100.0, mean=100.00, median=100.0
__index_level_0__: min=0, max=499999, mean=146085.49, median=104869.0
```

### Date/Datetime Column Statistics
```
date: min=1996-01-04 00:00:00, max=2012-01-31 00:00:00
exdate: min=1996-01-20 00:00:00, max=2014-12-20 00:00:00
```

---

## data_2012-02_2019-12.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/options/data_2012-02_2019-12.parquet`
**Size:** 261.2 MB | **Type:** Parquet | **Shape:** 15,803,328 rows × 15 columns

### Columns
```
secid                                    Float64        
date                                     Datetime(time_unit='ns', time_zone=None)
open                                     Float64        
close                                    Float64        
cp_flag                                  String         
exdate                                   Datetime(time_unit='ns', time_zone=None)
impl_volatility                          Float64         (11.7% null)
tb_m3                                    Float64         (0.8% null)
volume                                   Float64        
open_interest                            Float64        
best_bid                                 Float64        
best_offer                               Float64        
strike_price                             Float64        
contract_size                            Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
secid: min=108105.0, max=108105.0, mean=108105.00, median=108105.0
open: min=1277.82, max=3247.23, mean=2403.07, median=2450.66
close: min=1278.04, max=3240.02, mean=2403.43, median=2457.59
impl_volatility: min=0.012578, max=8.992139, mean=0.27, median=0.20988
tb_m3: min=-0.02, max=2.43, mean=1.07, median=1.02
volume: min=0.0, max=124136.0, mean=133.64, median=0.0
open_interest: min=0.0, max=624873.0, mean=1700.71, median=15.0
best_bid: min=0.0, max=3115.1, mean=219.28, median=57.0
best_offer: min=0.05, max=3134.3, mean=222.72, median=59.2
strike_price: min=100000.0, max=4800000.0, mean=2098406.93, median=2125000.0
contract_size: min=100.0, max=100.0, mean=100.00, median=100.0
__index_level_0__: min=0, max=499999, mean=238963.73, median=234175.0
```

### Date/Datetime Column Statistics
```
date: min=2012-02-01 00:00:00, max=2019-12-31 00:00:00
exdate: min=2012-02-03 00:00:00, max=2022-12-16 00:00:00
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

## CRSP_TFZ_CONSOLIDATED.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/CRSP_TFZ_CONSOLIDATED.parquet`
**Size:** 94.1 MB | **Type:** Parquet | **Shape:** 2,486,659 rows × 23 columns

### Columns
```
kytreasno                                Float64        
kycrspid                                 String         
tcusip                                   String         
caldt                                    Datetime(time_unit='ns', time_zone=None)
tdatdt                                   Datetime(time_unit='ns', time_zone=None)
tmatdt                                   Datetime(time_unit='ns', time_zone=None)
tfcaldt                                  Datetime(time_unit='ns', time_zone=None)
tdbid                                    Float64         (0.0% null)
tdask                                    Float64         (0.0% null)
tdaccint                                 Float64        
tdyld                                    Float64         (0.0% null)
price                                    Float64         (0.0% null)
tdpubout                                 Float64         (2.4% null)
tdtotout                                 Float64         (0.9% null)
tdpdint                                  Float64        
tcouprt                                  Float64        
itype                                    Float64        
original_maturity                        Float64        
years_to_maturity                        Float64        
tdduratn                                 Float64        
tdretnua                                 Float64         (0.1% null)
days_to_maturity                         Int64          
callable                                 Boolean        
```

### Numeric Column Statistics
```
kytreasno: min=200636.0, max=208417.0, mean=204528.16, median=204054.0
tdbid: min=43.5, max=176.328125, mean=104.51, median=100.96875
tdask: min=43.546875, max=176.390625, mean=104.59, median=101.03125
tdaccint: min=0.0, max=11.86908390823, mean=1.35, median=0.91304347826087
tdyld: min=-0.016641617296462, max=0.0065577934599587, mean=0.00, median=0.00011577937035561
price: min=44.05672554347826, max=182.7192679558011, mean=105.90, median=102.3569972826087
tdpubout: min=1.0, max=120001.0, mean=19560.14, median=14459.0
tdtotout: min=4.0, max=148501.0, mean=24552.97, median=18864.0
tdpdint: min=0.0, max=11.913043478261, mean=0.02, median=0.0
tcouprt: min=0.125, max=16.25, mean=5.41, median=4.875
itype: min=1.0, max=2.0, mean=1.75, median=2.0
original_maturity: min=1.0, max=40.0, mean=11.03, median=7.0
years_to_maturity: min=0.0, max=30.0, mean=6.20, median=3.0
tdduratn: min=-1.0, max=9160.066986023601, mean=1650.45, median=1110.9959172226
tdretnua: min=-0.10941117224377, max=0.12811078405138, mean=0.00, median=0.000145321567561345
days_to_maturity: min=1, max=11053, mean=2262.67, median=1211.0
```

### Date/Datetime Column Statistics
```
caldt: min=1970-01-02 00:00:00, max=2025-06-30 00:00:00
tdatdt: min=1955-02-15 00:00:00, max=2025-06-30 00:00:00
tmatdt: min=1970-02-15 00:00:00, max=2055-05-15 00:00:00
tfcaldt: min=1970-01-01 00:00:00, max=1970-01-01 00:00:00
```

---

## CRSP_TFZ_DAILY.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/CRSP_TFZ_DAILY.parquet`
**Size:** 123.4 MB | **Type:** Parquet | **Shape:** 3,183,517 rows × 14 columns

### Columns
```
kytreasno                                Float64        
kycrspid                                 String         
caldt                                    Datetime(time_unit='ns', time_zone=None)
tdbid                                    Float64         (0.0% null)
tdask                                    Float64         (0.0% null)
tdaccint                                 Float64        
tdyld                                    Float64         (5.9% null)
price                                    Float64         (0.0% null)
tdduratn                                 Float64         (5.9% null)
tdretnua                                 Float64         (6.0% null)
tdpubout                                 Float64         (16.9% null)
tdtotout                                 Float64         (2.1% null)
tdpdint                                  Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
kytreasno: min=200629.0, max=208161.0, mean=204351.50, median=203999.0
tdbid: min=43.5, max=179.4375, mean=104.37, median=100.453125
tdask: min=43.546875, max=179.5625, mean=104.46, median=100.51171875
tdaccint: min=0.0, max=11.86908390823, mean=1.14, median=0.63012295081967
tdyld: min=-0.016641617296462, max=0.0065577934599587, mean=0.00, median=0.000123679096319495
price: min=44.05672554347826, max=185.0088315217391, mean=105.55, median=101.5925546448087
tdduratn: min=-1.0, max=9160.066986023601, mean=1434.01, median=893.0038337727699
tdretnua: min=-0.10941117224377, max=0.12811078405138, mean=0.00, median=0.000136260667250115
tdpubout: min=1.0, max=116796.0, mean=17513.59, median=13013.0
tdtotout: min=4.0, max=249728.0, mean=22858.05, median=17037.0
tdpdint: min=0.0, max=11.913043478261, mean=0.02, median=0.0
__index_level_0__: min=0, max=499999, mean=240877.51, median=234706.0
```

### Date/Datetime Column Statistics
```
caldt: min=1970-01-02 00:00:00, max=2023-12-29 00:00:00
```

---

## CRSP_TFZ_INFO.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/CRSP_TFZ_INFO.parquet`
**Size:** 79231 bytes | **Type:** Parquet | **Shape:** 2,234 rows × 8 columns

### Columns
```
kytreasno                                Float64        
kycrspid                                 String         
tcusip                                   String         
tdatdt                                   Datetime(time_unit='ns', time_zone=None) (0.0% null)
tmatdt                                   Datetime(time_unit='ns', time_zone=None)
tcouprt                                  Float64        
itype                                    Float64        
original_maturity                        Float64         (0.0% null)
```

### Numeric Column Statistics
```
kytreasno: min=200018.0, max=208417.0, mean=204555.76, median=204010.5
tcouprt: min=0.125, max=16.25, mean=4.63, median=4.0
itype: min=1.0, max=2.0, mean=1.91, median=2.0
original_maturity: min=1.0, max=40.0, mean=6.04, median=5.0
```

### Date/Datetime Column Statistics
```
tdatdt: min=1916-01-01 00:00:00, max=2025-06-30 00:00:00
tmatdt: min=1926-03-15 00:00:00, max=2055-05-15 00:00:00
```

---

## CRSP_TFZ_with_runness.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/CRSP_TFZ_with_runness.parquet`
**Size:** 94.2 MB | **Type:** Parquet | **Shape:** 2,486,659 rows × 24 columns

### Columns
```
kytreasno                                Float64        
kycrspid                                 String         
tcusip                                   String         
caldt                                    Datetime(time_unit='ns', time_zone=None)
tdatdt                                   Datetime(time_unit='ns', time_zone=None)
tmatdt                                   Datetime(time_unit='ns', time_zone=None)
tfcaldt                                  Datetime(time_unit='ns', time_zone=None)
tdbid                                    Float64         (0.0% null)
tdask                                    Float64         (0.0% null)
tdaccint                                 Float64        
tdyld                                    Float64         (0.0% null)
price                                    Float64         (0.0% null)
tdpubout                                 Float64         (2.4% null)
tdtotout                                 Float64         (0.9% null)
tdpdint                                  Float64        
tcouprt                                  Float64        
itype                                    Float64        
original_maturity                        Float64        
years_to_maturity                        Float64        
tdduratn                                 Float64        
tdretnua                                 Float64         (0.1% null)
days_to_maturity                         Int64          
callable                                 Boolean        
run                                      Int64          
```

### Numeric Column Statistics
```
kytreasno: min=200636.0, max=208417.0, mean=204528.16, median=204054.0
tdbid: min=43.5, max=176.328125, mean=104.51, median=100.96875
tdask: min=43.546875, max=176.390625, mean=104.59, median=101.03125
tdaccint: min=0.0, max=11.86908390823, mean=1.35, median=0.91304347826087
tdyld: min=-0.016641617296462, max=0.0065577934599587, mean=0.00, median=0.00011577937035561
price: min=44.05672554347826, max=182.7192679558011, mean=105.90, median=102.3569972826087
tdpubout: min=1.0, max=120001.0, mean=19560.14, median=14459.0
tdtotout: min=4.0, max=148501.0, mean=24552.97, median=18864.0
tdpdint: min=0.0, max=11.913043478261, mean=0.02, median=0.0
tcouprt: min=0.125, max=16.25, mean=5.41, median=4.875
itype: min=1.0, max=2.0, mean=1.75, median=2.0
original_maturity: min=1.0, max=40.0, mean=11.03, median=7.0
years_to_maturity: min=0.0, max=30.0, mean=6.20, median=3.0
tdduratn: min=-1.0, max=9160.066986023601, mean=1650.45, median=1110.9959172226
tdretnua: min=-0.10941117224377, max=0.12811078405138, mean=0.00, median=0.000145321567561345
days_to_maturity: min=1, max=11053, mean=2262.67, median=1211.0
run: min=0, max=84, mean=19.01, median=14.0
```

### Date/Datetime Column Statistics
```
caldt: min=1970-01-02 00:00:00, max=2025-06-30 00:00:00
tdatdt: min=1955-02-15 00:00:00, max=2025-06-30 00:00:00
tmatdt: min=1970-02-15 00:00:00, max=2055-05-15 00:00:00
tfcaldt: min=1970-01-01 00:00:00, max=1970-01-01 00:00:00
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

## treasury_auction_stats.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/us_treasury_returns/treasury_auction_stats.parquet`
**Size:** 1.9 MB | **Type:** Parquet | **Shape:** 10,631 rows × 120 columns

### Columns
```
cusip                                    String         
issueDate                                Datetime(time_unit='ns', time_zone=None)
securityType                             String         
securityTerm                             String         
maturityDate                             Datetime(time_unit='ns', time_zone=None)
interestRate                             Float64         (76.3% null)
refCpiOnIssueDate                        String         
refCpiOnDatedDate                        String         
announcementDate                         Datetime(time_unit='ns', time_zone=None)
auctionDate                              Datetime(time_unit='ns', time_zone=None)
auctionDateYear                          String         
datedDate                                Datetime(time_unit='ns', time_zone=None) (74.9% null)
accruedInterestPer1000                   Float64         (84.9% null)
accruedInterestPer100                    Float64         (99.0% null)
adjustedAccruedInterestPer1000           Float64         (97.6% null)
adjustedPrice                            Float64         (97.6% null)
allocationPercentage                     Float64         (0.1% null)
allocationPercentageDecimals             String         
announcedCusip                           String         
auctionFormat                            String         
averageMedianDiscountRate                Float64         (25.1% null)
averageMedianInvestmentRate              Float64         (77.8% null)
averageMedianPrice                       Float64         (54.1% null)
averageMedianDiscountMargin              String         
averageMedianYield                       String         
backDated                                Null            (100.0% null)
backDatedDate                            Datetime(time_unit='ns', time_zone=None) (91.2% null)
bidToCoverRatio                          Float64         (30.3% null)
callDate                                 Datetime(time_unit='ns', time_zone=None) (99.8% null)
callable                                 Null            (100.0% null)
calledDate                               Datetime(time_unit='ns', time_zone=None) (99.8% null)
cashManagementBillCMB                    Null            (100.0% null)
closingTimeCompetitive                   String         
closingTimeNoncompetitive                String         
competitiveAccepted                      String         
competitiveBidDecimals                   String         
competitiveTendered                      String         
competitiveTendersAccepted               String         
corpusCusip                              String         
cpiBaseReferencePeriod                   String         
currentlyOutstanding                     String         
directBidderAccepted                     String         
directBidderTendered                     String         
estimatedAmountOfPubliclyHeldMaturingSecuritiesByType String         
fimaIncluded                             Null            (100.0% null)
fimaNoncompetitiveAccepted               String         
fimaNoncompetitiveTendered               String         
firstInterestPeriod                      String         
firstInterestPaymentDate                 Datetime(time_unit='ns', time_zone=None) (74.9% null)
floatingRate                             Null            (100.0% null)
frnIndexDeterminationDate                String         
frnIndexDeterminationRate                String         
highDiscountRate                         String         
highInvestmentRate                       String         
highPrice                                String         
highDiscountMargin                       String         
highYield                                String         
indexRatioOnIssueDate                    String         
indirectBidderAccepted                   String         
indirectBidderTendered                   String         
interestPaymentFrequency                 String         
lowDiscountRate                          String         
lowInvestmentRate                        String         
lowPrice                                 String         
lowDiscountMargin                        String         
lowYield                                 String         
maturingDate                             Datetime(time_unit='ns', time_zone=None) (27.1% null)
maximumCompetitiveAward                  String         
maximumNoncompetitiveAward               String         
maximumSingleBid                         String         
minimumBidAmount                         String         
minimumStripAmount                       String         
minimumToIssue                           String         
multiplesToBid                           String         
multiplesToIssue                         String         
nlpExclusionAmount                       String         
nlpReportingThreshold                    String         
noncompetitiveAccepted                   String         
noncompetitiveTendersAccepted            String         
offeringAmount                           String         
originalCusip                            String         
originalDatedDate                        Datetime(time_unit='ns', time_zone=None) (94.8% null)
originalIssueDate                        Datetime(time_unit='ns', time_zone=None) (31.3% null)
originalSecurityTerm                     String         
pdfFilenameAnnouncement                  String         
pdfFilenameCompetitiveResults            String         
pdfFilenameNoncompetitiveResults         String         
pdfFilenameSpecialAnnouncement           String         
pricePer100                              String         
primaryDealerAccepted                    String         
primaryDealerTendered                    String         
reopening                                Null            (100.0% null)
securityTermDayMonth                     String         
securityTermWeekYear                     String         
series                                   String         
somaAccepted                             String         
somaHoldings                             String         
somaIncluded                             Null            (100.0% null)
somaTendered                             String         
spread                                   String         
standardInterestPaymentPer1000           String         
strippable                               Null            (100.0% null)
term                                     String         
tiinConversionFactorPer1000              String         
tips                                     Null            (100.0% null)
totalAccepted                            Float64         (0.1% null)
totalTendered                            Float64         (0.1% null)
treasuryRetailAccepted                   String         
treasuryRetailTendersAccepted            String         
type                                     String         
unadjustedAccruedInterestPer1000         String         
unadjustedPrice                          String         
updatedTimestamp                         String         
xmlFilenameAnnouncement                  String         
xmlFilenameCompetitiveResults            String         
xmlFilenameSpecialAnnouncement           String         
tintCusip1                               String         
tintCusip2                               String         
tintCusip1DueDate                        Datetime(time_unit='ns', time_zone=None) (99.8% null)
tintCusip2DueDate                        Datetime(time_unit='ns', time_zone=None) (100.0% null)
```

### Numeric Column Statistics
```
interestRate: min=0.125, max=16.25, mean=4.11, median=3.25
accruedInterestPer1000: min=0.0, max=36.72798, mean=1.50, median=0.00679
accruedInterestPer100: min=0.000250021, max=0.940779263, mean=0.20, median=0.076733322
adjustedAccruedInterestPer1000: min=0.0, max=9.15983, mean=1.39, median=0.48111
adjustedPrice: min=81.754227, max=132.953297, mean=101.53, median=100.067434
allocationPercentage: min=0.01, max=100.0, mean=49.65, median=49.68
averageMedianDiscountRate: min=0.0, max=18.48, mean=3.48, median=3.1
averageMedianInvestmentRate: min=2.73, max=18.88, mean=7.46, median=6.53
averageMedianPrice: min=0.0, max=105.27, mean=58.24, median=95.758
bidToCoverRatio: min=1.11, max=10.72, mean=3.08, median=2.91
totalAccepted: min=25000000.0, max=95686476000.0, mean=27233926058.99, median=24000020800.0
totalTendered: min=72950000.0, max=287396859400.0, mean=80361361502.74, median=58729039000.0
```

### Date/Datetime Column Statistics
```
issueDate: min=1979-11-15 00:00:00, max=2025-08-15 00:00:00
maturityDate: min=1980-04-03 00:00:00, max=2055-08-15 00:00:00
announcementDate: min=1979-10-24 00:00:00, max=2025-07-31 00:00:00
auctionDate: min=1979-10-31 00:00:00, max=2025-08-07 00:00:00
datedDate: min=1979-11-15 00:00:00, max=2025-08-15 00:00:00
backDatedDate: min=2008-01-15 00:00:00, max=2025-07-15 00:00:00
callDate: min=2004-11-15 00:00:00, max=2009-11-15 00:00:00
calledDate: min=2004-11-15 00:00:00, max=2009-11-15 00:00:00
firstInterestPaymentDate: min=1980-05-15 00:00:00, max=2026-02-15 00:00:00
maturingDate: min=1996-02-15 00:00:00, max=2025-08-15 00:00:00
originalDatedDate: min=2005-02-15 00:00:00, max=2025-05-15 00:00:00
originalIssueDate: min=1979-01-18 00:00:00, max=2025-06-03 00:00:00
tintCusip1DueDate: min=2027-12-15 00:00:00, max=2055-08-15 00:00:00
tintCusip2DueDate: min=2055-02-15 00:00:00, max=2055-02-15 00:00:00
```

---

## idrssd_to_lei.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_bank_premium/idrssd_to_lei.parquet`
**Size:** 2.0 MB | **Type:** Parquet | **Shape:** 36,715 rows × 8 columns

### Columns
```
id_rssd                                  Float64        
nm_lgl                                   String         
lei                                      String         
lei_legalname                            String         
source                                   String         
match_type                               Float64        
link_bdate                               String         
link_edate                               String         
```

### Numeric Column Statistics
```
id_rssd: min=82.0, max=6026703.0, mean=3264419.97, median=3745898.0
match_type: min=1.0, max=6.0, mean=2.72, median=1.0
```

---

## lei_legalevents.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_bank_premium/lei_legalevents.parquet`
**Size:** 30.3 MB | **Type:** Parquet | **Shape:** 1,404,312 rows × 13 columns

### Columns
```
lei                                      String         
legalentityeventtype                     String         
legalentityeventeffectivedate            String          (0.1% null)
validationdocuments                      String         
validationreference                      String          (88.2% null)
event_status                             String         
group_type                               String         
group_id                                 String          (97.3% null)
group_sequence_no                        String          (99.6% null)
legalentityeventrecordeddate             String          (44.1% null)
rec_bdate                                Date           
rec_edate                                Date           
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
__index_level_0__: min=0, max=499999, mean=236224.85, median=234051.5
```

### Date/Datetime Column Statistics
```
rec_bdate: min=2022-03-01, max=2024-12-31
rec_edate: min=2022-03-07, max=2024-12-31
```

---

## lei_main.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_bank_premium/lei_main.parquet`
**Size:** 588.6 MB | **Type:** Parquet | **Shape:** 33,620,169 rows × 9 columns

### Columns
```
lei_record_id                            Float64        
most_recent                              Float64        
lei                                      String         
legalname                                String         
entitycategory                           String          (47.4% null)
entitystatus                             String         
rec_bdate                                Date           
rec_edate                                Date           
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
lei_record_id: min=1.0, max=40967469.0, mean=19145521.04, median=16810085.0
most_recent: min=0.0, max=1.0, mean=0.08, median=0.0
__index_level_0__: min=0, max=499999, mean=249320.68, median=249103.0
```

### Date/Datetime Column Statistics
```
rec_bdate: min=2017-05-01, max=2024-12-31
rec_edate: min=2017-05-01, max=2024-12-31
```

---

## lei_otherentnames.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_bank_premium/lei_otherentnames.parquet`
**Size:** 37.4 MB | **Type:** Parquet | **Shape:** 1,222,254 rows × 8 columns

### Columns
```
lei                                      String         
otherentityname                          String          (0.0% null)
otherentitynamelang                      String          (28.2% null)
transliterated                           Float64        
rowid                                    Float64        
rec_bdate                                Date           
rec_edate                                Date           
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
transliterated: min=0.0, max=1.0, mean=0.41, median=0.0
rowid: min=0.0, max=31.0, mean=0.12, median=0.0
__index_level_0__: min=0, max=499999, mean=224746.91, median=203708.5
```

### Date/Datetime Column Statistics
```
rec_bdate: min=2017-05-01, max=2024-12-31
rec_edate: min=2017-05-02, max=2024-12-31
```

---

## lei_successorentity.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_bank_premium/lei_successorentity.parquet`
**Size:** 3.2 MB | **Type:** Parquet | **Shape:** 63,369 rows × 7 columns

### Columns
```
lei                                      String         
legalname                                String         
successorlei                             String          (17.0% null)
successorname                            String          (0.0% null)
entityexpirationdate                     String          (67.6% null)
rec_bdate                                Date           
rec_edate                                Date           
```

### Date/Datetime Column Statistics
```
rec_bdate: min=2017-05-01, max=2024-12-31
rec_edate: min=2017-05-23, max=2024-12-31
```

---

## wrds_bank_crsp_link.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_bank_premium/wrds_bank_crsp_link.parquet`
**Size:** 49786 bytes | **Type:** Parquet | **Shape:** 1,495 rows × 6 columns

### Columns
```
rssd9001                                 Decimal(precision=7, scale=0)
permco                                   Decimal(precision=5, scale=0)
name                                     String         
inst_type                                String          (0.1% null)
dt_start                                 Date           
dt_end                                   Date           
```

### Date/Datetime Column Statistics
```
dt_start: min=1986-06-30, max=2024-07-12
dt_end: min=1986-10-31, max=2024-09-30
```

---

## wrds_call_research.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_bank_premium/wrds_call_research.parquet`
**Size:** 806.0 MB | **Type:** Parquet | **Shape:** 2,002,806 rows × 373 columns

### Columns
```
rssd9001                                 Decimal(precision=7, scale=0)
rcon9804                                 Float64         (8.2% null)
date                                     Datetime(time_unit='ns', time_zone=None)
rssdsubmissiondate                       Datetime(time_unit='ns', time_zone=None) (68.5% null)
rssd9050                                 Decimal(precision=5, scale=0) (0.1% null)
rssd9055                                 Decimal(precision=6, scale=0) (0.1% null)
rssd9048                                 Float64         (10.1% null)
assets                                   Float64         (0.2% null)
cash                                     Float64         (0.5% null)
securities                               Float64         (2.2% null)
securities_asu                           Float64         (2.1% null)
securities_ammcost                       Float64         (52.8% null)
securities_mv                            Float64         (25.1% null)
securitiesheldtomaturity                 Float64         (52.9% null)
securitiesavailableforsale               Float64         (52.8% null)
fedfundsrepoasset                        Float64         (0.3% null)
loansnet_ui                              Float64         (0.2% null)
loansnet_uiar                            Float64         (30.6% null)
loansnet                                 Float64         (0.2% null)
reloans                                  Float64         (0.9% null)
agloans                                  Float64         (4.2% null)
ciloans                                  Float64         (0.4% null)
otherciloans                             Float64         (25.2% null)
otherbankacceptances                     Float64         (58.0% null)
loansandacceptances                      Float64         (16.0% null)
persloans                                Float64         (3.7% null)
leaserec                                 Float64         (2.3% null)
loanlossallowance                        Float64         (3.3% null)
transriskreserve                         Float64         (27.6% null)
intanassets                              Float64         (25.0% null)
fixedassets                              Float64         (3.3% null)
currcoin                                 Float64         (24.4% null)
treasurysec                              Float64         (11.9% null)
usgovobligations                         Float64         (4.4% null)
stateobligations                         Float64         (27.8% null)
earnedincome                             Float64         (3.5% null)
residentialmbsat                         Float64         (82.0% null)
commercialmbsat                          Float64         (82.0% null)
loans1to4fam                             Float64         (3.9% null)
realoansnonres                           Float64         (3.3% null)
mbsassets                                Float64         (27.8% null)
absassets                                Float64         (68.5% null)
structuredat                             Float64         (82.0% null)
absandstructuredat                       Float64         (82.0% null)
tradingassets                            Float64         (25.9% null)
loans                                    Float64         (0.4% null)
unearnedincome                           Float64         (0.4% null)
constloans                               Float64         (3.3% null)
goodwill                                 Float64         (31.7% null)
liabilitiesandequity                     Float64         (3.3% null)
liabilities                              Float64         (0.5% null)
totaldebtnetsub                          Float64         (1.0% null)
totaldep                                 Float64         (2.8% null)
deposits                                 Float64         (3.0% null)
foreigndep                               Float64        
demanddep                                Float64         (0.8% null)
transdep                                 Float64         (27.4% null)
fedfundsrepoliab                         Float64         (0.3% null)
mortgagedebt                             Float64         (42.9% null)
llprfstock                               Float64         (66.6% null)
prfstock                                 Float64         (36.2% null)
cumuladjforeigncurr                      Float64         (99.0% null)
undivprofits                             Float64         (87.6% null)
capitalreserve                           Float64         (87.6% null)
nowacct                                  Float64         (65.0% null)
unreallossonequitysecnet                 Float64         (87.2% null)
acceptliabilities                        Float64         (36.4% null)
otherliabilities                         Float64         (14.9% null)
subordinateddebt                         Float64         (3.7% null)
surplus                                  Float64         (3.6% null)
ppstkandsurp                             Float64         (27.7% null)
mandconvdebtnet                          Float64         (64.4% null)
commonstock                              Float64         (4.3% null)
surplus_np                               Float64         (44.8% null)
retainedearning                          Float64         (42.1% null)
aoci                                     Float64         (68.3% null)
timesavdep                               Float64         (3.3% null)
timedep                                  Float64         (28.1% null)
timedepge100k                            Float64         (1.6% null)
timedeple100k                            Float64         (28.1% null)
domdepuninsured                          Float64         (40.9% null)
alldepuninsured                          Float64         (40.1% null)
timedepuninsured                         Float64         (2.1% null)
nontransdep                              Float64         (25.7% null)
depositgt100k                            Float64         (63.5% null)
numacctgt100k                            Float64         (63.5% null)
depositgt250k                            Float64         (77.4% null)
numacctgt250k                            Float64         (77.4% null)
rtdepositgt250k                          Float64         (77.4% null)
rtnumacctgt250k                          Float64         (77.4% null)
cdge100k                                 Float64         (43.8% null)
timedepge250k                            Float64         (83.1% null)
timedeple250k                            Float64         (83.1% null)
totsavdep                                Float64         (28.1% null)
savdep                                   Float64         (27.8% null)
brokereddep                              Float64         (26.2% null)
brokereddeple100k                        Float64         (35.3% null)
brokereddepeq100k                        Float64         (44.7% null)
otherborrowedmoney                       Float64         (11.8% null)
otherbrmandnt                            Float64         (42.9% null)
intbearfddep                             Float64         (27.3% null)
intbeardep                               Float64         (27.8% null)
intbearfordep                            Float64         (98.6% null)
subsid_minorint                          Float64         (19.5% null)
tradingliabilities                       Float64         (52.8% null)
persloanschargeoff                       Float64         (64.6% null)
res1_4famloanchargeoff                   Float64         (66.1% null)
intexptimedepge100k                      Float64         (69.5% null)
intexptimedeple100k                      Float64         (69.5% null)
intexptimedeple250k                      Float64         (92.5% null)
intexptimedepge250k                      Float64         (92.5% null)
intexptimedep                            Float64         (37.7% null)
tradingrevenue                           Float64         (71.3% null)
tier1cap                                 Float64         (58.9% null)
cet1cap                                  Float64         (90.1% null)
additionaltier1cap                       Float64         (90.0% null)
avgtotalassets                           Float64         (59.0% null)
tier2cap                                 Float64         (70.0% null)
tier3cap                                 Float64         (80.1% null)
totalriskcap                             Float64         (50.2% null)
riskweightedassets                       Float64         (60.5% null)
tier1levratio                            Float64         (59.0% null)
cet1ratio                                Float64         (91.5% null)
tier1ratio                               Float64         (60.5% null)
totalriskcapratio                        Float64         (60.5% null)
capitalbuffer                            Float64         (92.8% null)
riskweightedassetsbd                     Float64         (70.0% null)
loanexcessallowance                      Float64         (60.5% null)
riskassets0                              Float64         (50.8% null)
riskassets20                             Float64         (50.8% null)
riskassets50                             Float64         (50.8% null)
riskassets100                            Float64         (50.8% null)
riskassets150                            Float64         (92.7% null)
riskassets300                            Float64         (92.7% null)
riskassets600                            Float64         (92.7% null)
riskassets1250                           Float64         (92.7% null)
allriskassets0                           Float64         (50.8% null)
allriskassets20                          Float64         (50.8% null)
allriskassets50                          Float64         (50.8% null)
allriskassets100                         Float64         (50.8% null)
allriskassets150                         Float64         (92.7% null)
allriskassets300                         Float64         (92.7% null)
allriskassets600                         Float64         (92.7% null)
allriskassets1250                        Float64         (92.7% null)
securitizationexponbs1250                Float64         (92.7% null)
securitizationexpoffbs1250               Float64         (92.7% null)
qavgbaldue                               Float64         (24.8% null)
intincbaldue                             Float64         (14.3% null)
qavgtreasuriesagencydebt                 Float64         (68.5% null)
intinctreasuriesagencydebt               Float64         (68.5% null)
qavgmbs                                  Float64         (68.5% null)
intincmbs                                Float64         (68.5% null)
qavgothersecurities                      Float64         (68.5% null)
intincothersecurities                    Float64         (55.2% null)
qavgtradingassets                        Float64         (74.1% null)
qavgfedfundsrepoasset                    Float64         (1.7% null)
intincfedfundsrepoasset                  Float64         (14.0% null)
qavgloans                                Float64         (4.2% null)
intincloans                              Float64         (14.5% null)
qavgreloans1to4fam                       Float64         (79.8% null)
intincreloans1to4fam                     Float64         (79.8% null)
qavgreloansother                         Float64         (79.8% null)
intincreloansother                       Float64         (79.8% null)
qavgagloans                              Float64         (74.9% null)
qavgagloans_v2                           Float64         (49.9% null)
intincagloans                            Float64         (74.9% null)
intincagloans_v2                         Float64         (49.9% null)
qavgciloans                              Float64         (65.1% null)
intincciloans                            Float64         (65.1% null)
qavgpersccards                           Float64         (68.8% null)
intincpersccards                         Float64         (68.8% null)
qavgpersother                            Float64         (68.8% null)
intincpersother                          Float64         (68.8% null)
qavgforloans                             Float64         (98.6% null)
intincforloans                           Float64         (98.8% null)
qavgleases                               Float64         (36.7% null)
intincleases                             Float64         (14.7% null)
qavgassets                               Float64         (12.0% null)
intincassets                             Float64         (27.6% null)
qavgtransdep                             Float64         (36.7% null)
intexptransdep                           Float64         (36.7% null)
qavgsavdep                               Float64         (68.5% null)
intexpsavdep                             Float64         (36.7% null)
qavgtimedepge100k                        Float64         (68.5% null)
qavgcdge100k                             Float64         (51.9% null)
qavgtimedeple100k                        Float64         (68.5% null)
qavgtimedeple250k                        Float64         (92.5% null)
qavgtimedepge250k                        Float64         (92.5% null)
qavgtimedep                              Float64         (61.0% null)
qavgfordep                               Float64         (98.8% null)
intexpfordep                             Float64        
qavgfedfundsrepoliab                     Float64         (12.1% null)
intexpfedfundsrepoliab                   Float64         (14.2% null)
qavgtradingandotherborrowed              Float64         (54.1% null)
intexptradingandborrowed                 Float64         (23.5% null)
intexptradingandborrowed_v2              Float64         (18.2% null)
qavgpersloans                            Float64         (68.8% null)
intincpersloans                          Float64         (68.8% null)
persloansintinc                          Float64         (64.8% null)
qavgreloans                              Float64         (64.8% null)
qavgreloans_v2                           Float64         (39.2% null)
intincreloans                            Float64         (64.8% null)
qavgsecurities                           Float64         (68.5% null)
securities_less_3m                       Float64         (61.5% null)
securities_3m_1y                         Float64         (61.5% null)
securities_1y_3y                         Float64         (61.5% null)
securities_3y_5y                         Float64         (61.5% null)
securities_5y_15y                        Float64         (61.5% null)
securities_over_15y                      Float64         (61.5% null)
securitiestreasury_less_3m               Float64         (61.5% null)
securitiestreasury_3m_1y                 Float64         (61.5% null)
securitiestreasury_1y_3y                 Float64         (61.5% null)
securitiestreasury_3y_5y                 Float64         (61.5% null)
securitiestreasury_5y_15y                Float64         (61.5% null)
securitiestreasury_over_15y              Float64         (61.5% null)
securitiesrmbs_less_3m                   Float64         (61.5% null)
securitiesrmbs_3m_1y                     Float64         (61.5% null)
securitiesrmbs_1y_3y                     Float64         (61.5% null)
securitiesrmbs_3y_5y                     Float64         (61.5% null)
securitiesrmbs_5y_15y                    Float64         (61.5% null)
securitiesrmbs_over_15y                  Float64         (61.5% null)
securitiesothermbs_less_3y               Float64         (61.5% null)
securitiesothermbs_over_3y               Float64         (61.5% null)
loansleases_mat_less_1y                  Float64         (61.4% null)
securities_mat_less_1y                   Float64         (61.4% null)
resloans_less_3m                         Float64         (61.5% null)
resloans_3m_1y                           Float64         (61.5% null)
resloans_1y_3y                           Float64         (61.5% null)
resloans_3y_5y                           Float64         (61.5% null)
resloans_5y_15y                          Float64         (61.5% null)
resloans_over_15y                        Float64         (61.5% null)
loansleases_less_3m                      Float64         (61.5% null)
loansleases_3m_1y                        Float64         (61.5% null)
loansleases_1y_3y                        Float64         (61.5% null)
loansleases_3y_5y                        Float64         (61.5% null)
loansleases_5y_15y                       Float64         (61.5% null)
loansleases_over_15y                     Float64         (61.5% null)
timedeple100k_less_3m                    Float64         (69.0% null)
timedeple100k_3m_1y                      Float64         (69.0% null)
timedeple100k_1y_3y                      Float64         (69.0% null)
timedeple100k_over_3y                    Float64         (69.0% null)
timedeple100k_less_1y                    Float64         (68.8% null)
timedepge100k_less_3m                    Float64         (69.0% null)
timedepge100k_3m_1y                      Float64         (69.0% null)
timedepge100k_1y_3y                      Float64         (69.0% null)
timedepge100k_over_3y                    Float64         (69.0% null)
timedeple250k_less_3m                    Float64         (92.5% null)
timedeple250k_3m_1y                      Float64         (92.5% null)
timedeple250k_1y_3y                      Float64         (92.5% null)
timedeple250k_over_3y                    Float64         (92.5% null)
timedeple250k_less_1y                    Float64         (92.5% null)
timedepge250k_less_3m                    Float64         (92.5% null)
timedepge250k_3m_1y                      Float64         (92.5% null)
timedepge250k_1y_3y                      Float64         (92.5% null)
timedepge250k_over_3y                    Float64         (92.5% null)
interestratederivatives                  Float64         (55.3% null)
interestratederivatives_par              Float64         (87.8% null)
grosshedging                             Float64         (55.3% null)
fixedrateswaps                           Float64         (66.8% null)
totalswaps                               Float64         (34.2% null)
floatingrateswaps                        Float64         (66.8% null)
nethedging                               Float64         (66.8% null)
grosstrading                             Float64         (55.3% null)
cdssold                                  Float64         (81.6% null)
cdspurchased                             Float64         (81.6% null)
trssold                                  Float64         (81.6% null)
trspurchased                             Float64         (81.6% null)
creditdersold                            Float64         (65.0% null)
creditderpurchased                       Float64         (65.0% null)
intexpdomdep                             Float64         (14.5% null)
operinc                                  Float64         (14.0% null)
domloanintinc                            Float64         (14.5% null)
creditcardintinc                         Float64         (39.4% null)
intincnet                                Float64         (27.6% null)
tradingassetintinc                       Float64         (35.1% null)
nonintinc                                Float64         (27.6% null)
domintexp                                Float64         (27.6% null)
intexp                                   Float64         (27.6% null)
intexpalldep                             Float64         (14.5% null)
mmdacctdepexp                            Float64         (68.2% null)
othersavdepexp                           Float64         (68.2% null)
nonintexp                                Float64         (27.6% null)
exponpremises                            Float64         (14.3% null)
salaries                                 Float64         (14.0% null)
equity_lastq4                            Float64         (45.1% null)
netinc                                   Float64         (14.0% null)
netincbec                                Float64         (14.3% null)
stocknetsale                             Float64         (41.6% null)
changestobuscomb                         Float64         (41.4% null)
prfdiv                                   Float64         (38.0% null)
commondiv                                Float64         (38.0% null)
equity                                   Float64         (3.2% null)
domdepservicecharges                     Float64         (14.5% null)
intandnonintexp                          Float64         (14.0% null)
numemployees                             Float64         (18.7% null)
intexpsubordinated                       Float64         (19.5% null)
intanddivincsecurities                   Float64         (28.1% null)
loanleaselossprovision                   Float64         (14.0% null)
totloanchargeoff                         Float64         (14.2% null)
totloanrecoveries                        Float64         (14.0% null)
loanleaseallowance                       Float64         (40.9% null)
realloanchargeoff                        Float64         (64.9% null)
ciloanchargeoff                          Float64         (28.1% null)
maxcreditexp_1_4fam                      Float64         (73.3% null)
q_operinc                                Float64         (24.2% null)
q_domloanintinc                          Float64         (24.7% null)
q_domintexp                              Float64         (27.8% null)
q_creditcardintinc                       Float64         (39.5% null)
q_intincnet                              Float64         (27.8% null)
q_tradingassetintinc                     Float64         (35.3% null)
q_nonintinc                              Float64         (27.8% null)
q_intexp                                 Float64         (27.8% null)
q_intexpalldep                           Float64         (24.7% null)
q_mmdacctdepexp                          Float64         (68.3% null)
q_othersavdepexp                         Float64         (68.3% null)
q_nonintexp                              Float64         (27.8% null)
q_exponpremises                          Float64         (24.3% null)
q_salaries                               Float64         (24.3% null)
q_netinc                                 Float64         (24.2% null)
q_netincbec                              Float64         (24.3% null)
q_stocknetsale                           Float64         (57.0% null)
q_changestobuscomb                       Float64         (56.7% null)
q_prfdiv                                 Float64         (54.2% null)
q_commondiv                              Float64         (54.2% null)
q_domdepservicecharges                   Float64         (24.5% null)
q_intandnonintexp                        Float64         (24.2% null)
q_intexpsubordinated                     Float64         (29.7% null)
q_intanddivincsecurities                 Float64         (28.3% null)
q_loanleaselossprovision                 Float64         (24.2% null)
q_totloanchargeoff                       Float64         (24.4% null)
q_totloanrecoveries                      Float64         (24.2% null)
q_loanleaseallowance                     Float64         (56.5% null)
q_realloanchargeoff                      Float64         (64.9% null)
q_ciloanchargeoff                        Float64         (28.3% null)
q_persloanschargeoff                     Float64         (64.7% null)
q_res1_4famloanchargeoff                 Float64         (66.2% null)
q_intexptimedepge100k                    Float64         (70.1% null)
q_intexptimedeple100k                    Float64         (70.1% null)
q_intexptimedeple250k                    Float64         (92.5% null)
q_intexptimedepge250k                    Float64         (92.5% null)
q_intexptimedep                          Float64         (38.3% null)
q_tradingrevenue                         Float64         (71.5% null)
q_intincbaldue                           Float64         (24.3% null)
q_intinctreasuriesagencydebt             Float64         (68.6% null)
q_intincmbs                              Float64         (68.6% null)
q_intincothersecurities                  Float64         (65.1% null)
q_intincfedfundsrepoasset                Float64         (24.3% null)
q_intincloans                            Float64         (24.7% null)
q_intincreloans1to4fam                   Float64         (79.8% null)
q_intincreloansother                     Float64         (79.8% null)
q_intincagloans                          Float64         (75.0% null)
q_intincagloans_v2                       Float64         (50.0% null)
q_intincciloans                          Float64         (65.2% null)
q_intincpersccards                       Float64         (68.8% null)
q_intincpersother                        Float64         (68.8% null)
q_intincforloans                         Float64         (98.8% null)
q_intincleases                           Float64         (24.8% null)
q_intincassets                           Float64         (27.8% null)
q_intexptransdep                         Float64         (36.8% null)
q_intexpsavdep                           Float64         (36.8% null)
q_intexpfordep                           Float64         (0.6% null)
q_intexpfedfundsrepoliab                 Float64         (24.4% null)
q_intexptradingandborrowed               Float64         (30.0% null)
q_intincpersloans                        Float64         (68.8% null)
q_persloansintinc                        Float64         (64.9% null)
q_intincreloans                          Float64         (64.9% null)
q_intexpdomdep                           Float64         (24.7% null)
avgirate_timedep                         Decimal(precision=6, scale=4) (63.2% null)
avgirate_timedep_ytd                     Decimal(precision=7, scale=4) (38.4% null)
avgirate_savdep                          Decimal(precision=6, scale=4) (69.2% null)
avgirate_fordep                          Decimal(precision=7, scale=4) (99.1% null)
fedfundsrate                             Float64        
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
rcon9804: min=0.0, max=59.0, mean=40.11, median=51.0
rssd9048: min=0.0, max=720.0, mean=199.96, median=200.0
assets: min=0.0, max=3503360000.0, mean=1010370.16, median=60989.0
cash: min=-708.0, max=760259000.0, mean=113769.99, median=3420.0
securities: min=0.0, max=941745000.0, mean=183550.50, median=13645.0
securities_asu: min=0.0, max=941778000.0, mean=183697.64, median=13649.0
securities_ammcost: min=0.0, max=938488000.0, mean=345190.40, median=23438.0
securities_mv: min=0.0, max=933080000.0, mean=232210.41, median=17674.0
securitiesheldtomaturity: min=0.0, max=683054000.0, mean=80834.30, median=0.0
securitiesavailableforsale: min=0.0, max=484943000.0, mean=263051.57, median=17422.0
fedfundsrepoasset: min=0.0, max=388555000.0, mean=46439.29, median=1000.0
loansnet_ui: min=0.0, max=1331054000.0, mean=511647.05, median=32888.0
loansnet_uiar: min=-33530.0, max=1308630000.0, mean=290658.73, median=21392.0
loansnet: min=-32633.0, max=1308719000.0, mean=503081.18, median=32422.0
reloans: min=0.0, max=508082000.0, mean=232024.24, median=15199.0
agloans: min=0.0, max=6508000.0, mean=4967.38, median=626.0
ciloans: min=-1.0, max=353653000.0, mean=123597.74, median=4773.0
otherciloans: min=0.0, max=353653000.0, mean=156171.92, median=6238.0
otherbankacceptances: min=0.0, max=833753.0, mean=310.53, median=0.0
loansandacceptances: min=0.0, max=75990000.0, mean=13814.92, median=0.0
persloans: min=0.0, max=274517000.0, mean=80396.53, median=3539.0
leaserec: min=-7321.0, max=25990000.0, mean=8229.37, median=0.0
loanlossallowance: min=-85980.0, max=32071000.0, mean=8650.79, median=405.0
transriskreserve: min=0.0, max=1878000.0, mean=18.67, median=0.0
intanassets: min=-1235.0, max=79167395.0, mean=22876.19, median=0.0
fixedassets: min=0.0, max=25404000.0, mean=8646.16, median=876.0
currcoin: min=-1502.0, max=19379000.0, mean=5206.38, median=402.0
treasurysec: min=0.0, max=362667000.0, mean=29449.24, median=1101.0
usgovobligations: min=0.0, max=46728000.0, mean=17973.74, median=2773.0
stateobligations: min=0.0, max=32747000.0, mean=8434.30, median=0.0
earnedincome: min=-243.0, max=14419000.0, mean=3500.87, median=396.0
residentialmbsat: min=0.0, max=620819000.0, mean=312914.81, median=8039.0
commercialmbsat: min=0.0, max=94613000.0, mean=43930.29, median=0.0
loans1to4fam: min=0.0, max=381105461.0, mean=127001.20, median=7194.0
realoansnonres: min=0.0, max=104535000.0, mean=65672.80, median=3324.0
mbsassets: min=0.0, max=642419000.0, mean=121091.96, median=1408.0
absassets: min=0.0, max=92685653.0, mean=17599.66, median=0.0
structuredat: min=0.0, max=67207000.0, mean=17184.26, median=0.0
absandstructuredat: min=0.0, max=72599000.0, mean=39073.57, median=0.0
tradingassets: min=-156.0, max=475614000.0, mean=69968.27, median=0.0
loans: min=0.0, max=1331054000.0, mean=505193.41, median=33158.0
unearnedincome: min=-93000.0, max=2631000.0, mean=858.31, median=18.0
constloans: min=0.0, max=39864847.0, mean=21196.45, median=512.0
goodwill: min=-446.0, max=57347715.0, mean=19329.71, median=0.0
liabilitiesandequity: min=0.0, max=3503360000.0, mean=919450.08, median=59183.0
liabilities: min=-43.0, max=3198322000.0, mean=880266.60, median=54700.0
totaldebtnetsub: min=-43.0, max=3198068000.0, mean=877347.17, median=54721.5
totaldep: min=-2139062144.0, max=2635021000.0, mean=591850.55, median=50565.0
deposits: min=-2139062144.0, max=2201118000.0, mean=503128.67, median=50566.0
foreigndep: min=0.0, max=652858000.0, mean=75906.41, median=0.0
demanddep: min=0.0, max=1077952576.0, mean=137826.66, median=7588.0
transdep: min=0.0, max=1009197000.0, mean=162673.94, median=17773.0
fedfundsrepoliab: min=0.0, max=276478000.0, mean=55643.66, median=0.0
mortgagedebt: min=0.0, max=418762.0, mean=164.13, median=0.0
llprfstock: min=0.0, max=1077952576.0, mean=8075.60, median=0.0
prfstock: min=0.0, max=1500000.0, mean=112.52, median=0.0
cumuladjforeigncurr: min=-871000.0, max=116316.0, mean=-2515.62, median=0.0
undivprofits: min=-218899.0, max=4100000.0, mean=4972.49, median=714.0
capitalreserve: min=-5335.0, max=220100.0, mean=320.70, median=0.0
nowacct: min=0.0, max=9706000.0, mean=18294.66, median=5361.0
unreallossonequitysecnet: min=-503619.0, max=174711.0, mean=21.12, median=0.0
acceptliabilities: min=0.0, max=11257000.0, mean=3577.02, median=0.0
otherliabilities: min=-662.0, max=175038000.0, mean=27658.68, median=498.0
subordinateddebt: min=0.0, max=29191000.0, mean=6447.92, median=0.0
surplus: min=-164630.0, max=176728000.0, mean=52489.40, median=1500.0
ppstkandsurp: min=0.0, max=3632500.0, mean=573.31, median=0.0
mandconvdebtnet: min=0.0, max=900000.0, mean=334.25, median=0.0
commonstock: min=0.0, max=8002000.0, mean=3430.53, median=466.0
surplus_np: min=-589.0, max=176728000.0, mean=88825.65, median=2838.0
retainedearning: min=-26643496.0, max=1077952576.0, mean=106555.99, median=4243.0
aoci: min=-31999000.0, max=8890000.0, mean=-6518.01, median=2.0
timesavdep: min=0.0, max=1713783000.0, mean=501667.31, median=41474.0
timedep: min=0.0, max=303937000.0, mean=163037.17, median=29483.0
timedepge100k: min=0.0, max=204954000.0, mean=97941.60, median=5528.0
timedeple100k: min=0.0, max=117145420.0, mean=87911.05, median=18697.0
domdepuninsured: min=-1666166.0, max=1227175500.0, mean=343107.45, median=10284.0
alldepuninsured: min=-1666166.0, max=1661078500.0, mean=465052.70, median=10315.0
timedepuninsured: min=0.0, max=148857000.0, mean=63831.10, median=4414.0
nontransdep: min=0.0, max=1672667000.0, mean=610122.29, median=47422.0
depositgt100k: min=0.0, max=302588000.0, mean=126940.91, median=12123.0
numacctgt100k: min=0.0, max=786675.0, mean=350.71, median=60.0
depositgt250k: min=0.0, max=1438563000.0, mean=912771.74, median=44825.0
numacctgt250k: min=0.0, max=1284130.0, mean=806.34, median=87.0
rtdepositgt250k: min=0.0, max=29768000.0, mean=6001.44, median=291.0
rtnumacctgt250k: min=0.0, max=22656.0, mean=8.82, median=1.0
cdge100k: min=0.0, max=24393123.0, mean=22054.23, median=2334.0
timedepge250k: min=0.0, max=148857000.0, mean=90146.72, median=7521.0
timedeple250k: min=0.0, max=155080000.0, mean=208924.81, median=41073.5
totsavdep: min=-126838.0, max=1644994000.0, mean=442901.54, median=24208.0
savdep: min=0.0, max=1634859000.0, mean=408293.12, median=15171.0
brokereddep: min=-5.0, max=139426000.0, mean=45109.65, median=0.0
brokereddeple100k: min=0.0, max=63525000.0, mean=13022.95, median=0.0
brokereddepeq100k: min=0.0, max=29231911.0, mean=4994.38, median=0.0
otherborrowedmoney: min=0.0, max=253149000.0, mean=77062.21, median=0.0
otherbrmandnt: min=0.0, max=55727000.0, mean=19919.90, median=0.0
intbearfddep: min=0.0, max=1880595000.0, mean=657670.49, median=56894.0
intbeardep: min=0.0, max=1475667000.0, mean=553594.39, median=57142.0
intbearfordep: min=0.0, max=573728000.0, mean=5078730.16, median=71521.0
subsid_minorint: min=-7859.0, max=8488305.0, mean=635.19, median=0.0
tradingliabilities: min=0.0, max=146927000.0, mean=49225.67, median=0.0
persloanschargeoff: min=-960.0, max=19169126.0, mean=3853.66, median=10.0
res1_4famloanchargeoff: min=-75.0, max=6512000.0, mean=626.98, median=0.0
intexptimedepge100k: min=-2194.0, max=3899253.0, mean=1662.73, median=216.0
intexptimedeple100k: min=-2611.0, max=4690030.0, mean=2267.78, median=399.0
intexptimedeple250k: min=-1586.0, max=4730000.0, mean=2631.81, median=256.0
intexptimedepge250k: min=-15000.0, max=6733000.0, mean=1375.57, median=72.0
intexptimedep: min=-246641.0, max=8532072.0, mean=3654.38, median=638.0
tradingrevenue: min=-4058000.0, max=26694000.0, mean=2690.49, median=0.0
tier1cap: min=-157278.0, max=282482000.0, mean=152031.02, median=13088.0
cet1cap: min=-114774.0, max=217622000.0, mean=272670.07, median=26210.0
additionaltier1cap: min=0.0, max=3632500.0, mean=2125.70, median=0.0
avgtotalassets: min=-106.0, max=3402079000.0, mean=1675656.30, median=125888.0
tier2cap: min=0.0, max=43382000.0, mean=29553.90, median=1070.0
tier3cap: min=0.0, max=14516.0, mean=0.05, median=0.0
totalriskcap: min=-157278.0, max=302050000.0, mean=149845.26, median=11271.0
riskweightedassets: min=0.0, max=1673296870.0, mean=1271076.16, median=82104.0
tier1levratio: min=-38.87735849056604, max=213.70209999999997, mean=0.12, median=0.09797700000000001
cet1ratio: min=-0.7290449999999999, max=742.833333, mean=0.27, median=0.15056049999999999
tier1ratio: min=-23.0, max=742.833333, mean=0.24, median=0.1436
totalriskcapratio: min=-23.0, max=742.833333, mean=0.25, median=0.1549755148129338
capitalbuffer: min=-0.033578, max=734.833333, mean=0.20, median=0.0811085
riskweightedassetsbd: min=0.0, max=1676474870.0, mean=1541526.57, median=100272.0
loanexcessallowance: min=-10.0, max=18093954.0, mean=4432.27, median=0.0
riskassets0: min=-575.0, max=1177434000.0, mean=232224.96, median=1590.0
riskassets20: min=-103.0, max=608731000.0, mean=278473.42, median=13662.0
riskassets50: min=0.0, max=363005000.0, mean=187949.94, median=8032.0
riskassets100: min=0.0, max=802369000.0, mean=670236.55, median=30567.0
riskassets150: min=0.0, max=29488000.0, mean=36119.11, median=717.0
riskassets300: min=0.0, max=596082.0, mean=449.60, median=0.0
riskassets600: min=0.0, max=53000.0, mean=13.00, median=0.0
riskassets1250: min=0.0, max=348000.0, mean=65.53, median=0.0
allriskassets0: min=-575.0, max=1224456000.0, mean=313056.30, median=1600.0
allriskassets20: min=-103.0, max=830280000.0, mean=346930.37, median=13712.0
allriskassets50: min=0.0, max=424874000.0, mean=220498.81, median=8142.0
allriskassets100: min=0.0, max=1207479000.0, mean=832793.30, median=31337.0
allriskassets150: min=0.0, max=38366400.0, mean=42897.44, median=734.0
allriskassets300: min=0.0, max=596082.0, mean=449.69, median=0.0
allriskassets600: min=0.0, max=53000.0, mean=13.00, median=0.0
allriskassets1250: min=0.0, max=622000.0, mean=194.82, median=0.0
securitizationexponbs1250: min=0.0, max=348000.0, mean=65.54, median=0.0
securitizationexpoffbs1250: min=0.0, max=486000.0, mean=106.01, median=0.0
qavgbaldue: min=-77.0, max=767833000.0, mean=106303.07, median=426.0
intincbaldue: min=-299724.0, max=23020000.0, mean=893.33, median=6.0
qavgtreasuriesagencydebt: min=0.0, max=364492000.0, mean=88062.36, median=6887.0
intinctreasuriesagencydebt: min=-17000.0, max=4568000.0, mean=1090.43, median=102.0
qavgmbs: min=0.0, max=636181000.0, mean=249426.18, median=5252.0
intincmbs: min=-13368.0, max=12937000.0, mean=4494.85, median=84.0
qavgothersecurities: min=0.0, max=171050000.0, mean=101994.72, median=6000.0
intincothersecurities: min=-8804.0, max=7894000.0, mean=1379.53, median=35.0
qavgtradingassets: min=-271.0, max=420914000.0, mean=133909.14, median=0.0
qavgfedfundsrepoasset: min=0.0, max=393360000.0, mean=41432.96, median=1375.0
intincfedfundsrepoasset: min=-702.0, max=14190000.0, mean=726.18, median=39.0
qavgloans: min=0.0, max=1203546000.0, mean=440920.01, median=31892.0
intincloans: min=-7039.0, max=84075000.0, mean=20935.24, median=1864.0
qavgreloans1to4fam: min=0.0, max=382413298.0, mean=388547.72, median=29589.0
intincreloans1to4fam: min=-247.0, max=19364532.0, mean=10273.07, median=902.0
qavgreloansother: min=0.0, max=169525000.0, mean=333386.31, median=46301.0
intincreloansother: min=-501.0, max=9441000.0, mean=9740.06, median=1395.0
qavgagloans: min=0.0, max=6059000.0, mean=12857.12, median=1933.0
qavgagloans_v2: min=0.0, max=6059000.0, mean=8033.44, median=652.0
intincagloans: min=-1711.0, max=689000.0, mean=484.66, median=62.0
intincagloans_v2: min=-1711.0, max=689000.0, mean=339.37, median=19.0
qavgciloans: min=0.0, max=288934000.0, mean=236295.78, median=12577.0
intincciloans: min=-901.0, max=13871000.0, mean=8455.91, median=457.0
qavgpersccards: min=0.0, max=178753000.0, mean=83128.86, median=0.0
intincpersccards: min=-7039.0, max=24300000.0, mean=6686.70, median=0.0
qavgpersother: min=0.0, max=91928000.0, mean=96333.86, median=3490.0
intincpersother: min=-1967.0, max=7107000.0, mean=3450.91, median=146.0
qavgforloans: min=-65143.0, max=333795000.0, mean=2241518.45, median=4407.0
intincforloans: min=-1557.0, max=27256000.0, mean=105499.85, median=52.0
qavgleases: min=-3753.0, max=25377000.0, mean=11999.94, median=0.0
intincleases: min=-725000.0, max=1441000.0, mean=339.58, median=0.0
qavgassets: min=0.0, max=3450654000.0, mean=939808.13, median=65967.0
intincassets: min=-763091.0, max=151752000.0, mean=31880.19, median=2953.0
qavgtransdep: min=0.0, max=450163000.0, mean=74023.88, median=8349.0
intexptransdep: min=-37000.0, max=14598000.0, mean=563.81, median=59.0
qavgsavdep: min=0.0, max=1607649000.0, mean=834149.23, median=30426.0
intexpsavdep: min=-11665.0, max=9596000.0, mean=2140.24, median=166.0
qavgtimedepge100k: min=0.0, max=140237656.0, mean=96168.11, median=13795.5
qavgcdge100k: min=0.0, max=24315430.0, mean=21066.66, median=2773.0
qavgtimedeple100k: min=0.0, max=127334276.0, mean=112585.99, median=24235.0
qavgtimedeple250k: min=0.0, max=151705000.0, mean=235433.99, median=39127.0
qavgtimedepge250k: min=0.0, max=152749000.0, mean=115950.30, median=9975.0
qavgtimedep: min=0.0, max=304454000.0, mean=236091.88, median=42494.0
qavgfordep: min=0.0, max=581638000.0, mean=5639525.24, median=73000.0
intexpfordep: min=-369000.0, max=19754000.0, mean=1285.61, median=0.0
qavgfedfundsrepoliab: min=0.0, max=277030000.0, mean=64423.67, median=0.0
intexpfedfundsrepoliab: min=-361000.0, max=8957611.0, mean=951.15, median=0.0
qavgtradingandotherborrowed: min=0.0, max=250207000.0, mean=143283.57, median=30.0
intexptradingandborrowed: min=-133892.0, max=9822000.0, mean=1574.35, median=0.0
intexptradingandborrowed_v2: min=-133892.0, max=9822000.0, mean=1483.75, median=0.0
qavgpersloans: min=0.0, max=265348000.0, mean=179462.72, median=3621.0
intincpersloans: min=-7039.0, max=28902842.0, mean=10137.61, median=153.0
persloansintinc: min=-7039.0, max=28902842.0, mean=11451.58, median=186.0
qavgreloans: min=0.0, max=507267000.0, mean=590692.40, median=76566.0
qavgreloans_v2: min=0.0, max=507267000.0, mean=351513.21, median=33161.0
intincreloans: min=-501.0, max=25474227.0, mean=19600.07, median=2610.0
qavgsecurities: min=0.0, max=940322000.0, mean=439483.25, median=27182.0
securities_less_3m: min=0.0, max=106370361.0, mean=35985.87, median=624.0
securities_3m_1y: min=0.0, max=84351000.0, mean=18107.01, median=1208.0
securities_1y_3y: min=0.0, max=173048000.0, mean=38816.12, median=2961.0
securities_3y_5y: min=0.0, max=98539000.0, mean=32243.45, median=2541.0
securities_5y_15y: min=0.0, max=243786000.0, mean=74041.07, median=6107.0
securities_over_15y: min=0.0, max=610490000.0, mean=110682.43, median=454.0
securitiestreasury_less_3m: min=0.0, max=105938918.0, mean=32741.87, median=470.0
securitiestreasury_3m_1y: min=0.0, max=84261000.0, mean=15947.53, median=878.0
securitiestreasury_1y_3y: min=0.0, max=172673000.0, mean=36545.37, median=2570.0
securitiestreasury_3y_5y: min=0.0, max=98522000.0, mean=29089.74, median=2082.0
securitiestreasury_5y_15y: min=0.0, max=243261000.0, mean=43266.34, median=3617.0
securitiestreasury_over_15y: min=0.0, max=50687293.0, mean=15936.60, median=0.0
securitiesrmbs_less_3m: min=0.0, max=10184290.0, mean=3244.00, median=0.0
securitiesrmbs_3m_1y: min=0.0, max=3512483.0, mean=2159.48, median=0.0
securitiesrmbs_1y_3y: min=0.0, max=16306115.0, mean=2270.75, median=0.0
securitiesrmbs_3y_5y: min=0.0, max=61749128.0, mean=3153.71, median=0.0
securitiesrmbs_5y_15y: min=0.0, max=93947000.0, mean=30774.73, median=419.0
securitiesrmbs_over_15y: min=0.0, max=609436000.0, mean=94745.83, median=0.0
securitiesothermbs_less_3y: min=0.0, max=56098000.0, mean=20271.72, median=0.0
securitiesothermbs_over_3y: min=0.0, max=122325000.0, mean=50353.07, median=0.0
loansleases_mat_less_1y: min=0.0, max=343067000.0, mean=222088.08, median=18240.0
securities_mat_less_1y: min=0.0, max=120208000.0, mean=26005.96, median=1247.0
resloans_less_3m: min=0.0, max=65112000.0, mean=17465.11, median=1001.0
resloans_3m_1y: min=0.0, max=23554000.0, mean=16314.45, median=1811.0
resloans_1y_3y: min=0.0, max=31765000.0, mean=20020.26, median=3002.0
resloans_3y_5y: min=0.0, max=31761000.0, mean=23182.52, median=2198.0
resloans_5y_15y: min=0.0, max=88359000.0, mean=48558.82, median=1677.0
resloans_over_15y: min=0.0, max=189250000.0, mean=83293.25, median=401.0
loansleases_less_3m: min=0.0, max=715088000.0, mean=453129.01, median=15631.0
loansleases_3m_1y: min=0.0, max=128888000.0, mean=75142.46, median=11143.0
loansleases_1y_3y: min=0.0, max=193209000.0, mean=124215.80, median=15184.0
loansleases_3y_5y: min=0.0, max=177688000.0, mean=116011.63, median=12914.0
loansleases_5y_15y: min=0.0, max=178723000.0, mean=132446.85, median=7589.0
loansleases_over_15y: min=0.0, max=206330000.0, mean=106325.45, median=1450.0
timedeple100k_less_3m: min=0.0, max=47259000.0, mean=27137.19, median=5691.0
timedeple100k_3m_1y: min=0.0, max=72801155.0, mean=49803.12, median=11326.0
timedeple100k_1y_3y: min=0.0, max=20275000.0, mean=25533.92, median=4577.0
timedeple100k_over_3y: min=0.0, max=17637000.0, mean=9582.03, median=668.0
timedeple100k_less_1y: min=0.0, max=108375017.0, mean=76177.90, median=17092.0
timedepge100k_less_3m: min=0.0, max=98667000.0, mean=44494.53, median=3789.0
timedepge100k_3m_1y: min=0.0, max=78616626.0, mean=33840.19, median=6412.0
timedepge100k_1y_3y: min=0.0, max=20604594.0, mean=13998.61, median=1965.0
timedepge100k_over_3y: min=0.0, max=10076000.0, mean=6591.54, median=300.0
timedeple250k_less_3m: min=0.0, max=54869000.0, mean=51814.10, median=7511.0
timedeple250k_3m_1y: min=0.0, max=89244000.0, mean=111357.97, median=17289.0
timedeple250k_1y_3y: min=0.0, max=28614000.0, mean=56363.64, median=8778.0
timedeple250k_over_3y: min=0.0, max=15008000.0, mean=19931.27, median=1821.0
timedeple250k_less_1y: min=0.0, max=144111000.0, mean=160999.43, median=24661.0
timedepge250k_less_3m: min=0.0, max=114078000.0, mean=59850.41, median=1925.0
timedepge250k_3m_1y: min=0.0, max=63660000.0, mean=40081.95, median=4382.0
timedepge250k_1y_3y: min=0.0, max=19013567.0, mean=11231.57, median=1552.0
timedepge250k_over_3y: min=0.0, max=51710000.0, mean=7541.46, median=0.0
interestratederivatives: min=0.0, max=2446245923.0, mean=319331.21, median=0.0
interestratederivatives_par: min=0.0, max=336151000.0, mean=137342.26, median=0.0
grosshedging: min=0.0, max=2446245923.0, mean=356854.51, median=0.0
fixedrateswaps: min=0.0, max=1314948769.0, mean=116391.14, median=0.0
totalswaps: min=0.0, max=59969864000.0, mean=7742213.21, median=0.0
floatingrateswaps: min=-5.0, max=59951858000.0, mean=13136472.82, median=0.0
nethedging: min=-59933852000.0, max=39549000.0, mean=-13020081.67, median=0.0
grosstrading: min=0.0, max=75137030000.0, mean=15455980.26, median=0.0
cdssold: min=0.0, max=11593648945.0, mean=977065.27, median=0.0
cdspurchased: min=0.0, max=11593648945.0, mean=1005011.87, median=0.0
trssold: min=0.0, max=57643426.0, mean=10481.41, median=0.0
trspurchased: min=0.0, max=58567000.0, mean=16874.28, median=0.0
creditdersold: min=0.0, max=11593648945.0, mean=559550.23, median=0.0
creditderpurchased: min=0.0, max=11593648945.0, mean=583408.45, median=0.0
intexpdomdep: min=-216517.0, max=29686000.0, mean=5805.75, median=932.0
operinc: min=-1125733.0, max=208658000.0, mean=39895.43, median=2975.0
domloanintinc: min=-7039.0, max=76512000.0, mean=19464.91, median=1863.0
creditcardintinc: min=-7039.0, max=24300000.0, mean=4200.32, median=0.0
intincnet: min=-797874.0, max=93321000.0, mean=21049.24, median=1694.0
tradingassetintinc: min=-2064.0, max=11071000.0, mean=772.44, median=0.0
nonintinc: min=-1228913.0, max=56906000.0, mean=13270.92, median=258.0
domintexp: min=-176583.0, max=44551000.0, mean=9413.44, median=1042.0
intexp: min=-176583.0, max=58431000.0, mean=10831.39, median=1043.0
intexpalldep: min=-195000.0, max=43566000.0, mean=7308.78, median=933.0
mmdacctdepexp: min=-1335.0, max=2868000.0, mean=1059.65, median=106.0
othersavdepexp: min=-5024.0, max=1009000.0, mean=566.89, median=80.0
nonintexp: min=-172742.0, max=78648000.0, mean=20788.91, median=1361.0
exponpremises: min=-10776.0, max=7861000.0, mean=1996.07, median=152.0
salaries: min=-1860.0, max=37835000.0, mean=8113.39, median=589.0
equity_lastq4: min=-452175.0, max=303620000.0, mean=140125.09, median=11657.0
netinc: min=-24593679.0, max=47496000.0, mean=6449.79, median=339.0
netincbec: min=-24597066.0, max=47493000.0, mean=6467.70, median=337.0
stocknetsale: min=-1950000.0, max=16193099.0, mean=488.36, median=0.0
changestobuscomb: min=-43568000.0, max=62722000.0, mean=3137.57, median=0.0
prfdiv: min=-600.0, max=196000.0, mean=18.63, median=0.0
commondiv: min=-1895.0, max=61000000.0, mean=5165.10, median=75.0
equity: min=-939749.0, max=317802000.0, mean=95924.91, median=5550.0
domdepservicecharges: min=-1721.0, max=10857344.0, mean=1533.36, median=101.0
intandnonintexp: min=-119840.0, max=137079000.0, mean=28329.39, median=2396.0
numemployees: min=-292.0, max=1607556.0, mean=204.01, median=31.0
intexpsubordinated: min=-17950.0, max=2101000.0, mean=227.04, median=0.0
intanddivincsecurities: min=-4933.0, max=18740000.0, mean=4822.18, median=506.0
loanleaselossprovision: min=-9068000.0, max=29395292.0, mean=2809.65, median=49.0
totloanchargeoff: min=-1150.0, max=21277000.0, mean=3060.93, median=41.0
totloanrecoveries: min=-3087.0, max=2538000.0, mean=606.30, median=12.0
loanleaseallowance: min=-81274.0, max=32071000.0, mean=13992.16, median=881.0
realloanchargeoff: min=-509.0, max=13707068.0, mean=1684.75, median=0.0
ciloanchargeoff: min=-41.0, max=3820000.0, mean=654.63, median=3.0
maxcreditexp_1_4fam: min=0.0, max=8281000.0, mean=649.97, median=0.0
q_operinc: min=-30046000.0, max=56620000.0, mean=18368.26, median=1478.0
q_domloanintinc: min=-17507000.0, max=21219000.0, mean=9001.97, median=945.0
q_domintexp: min=-9909000.0, max=14206000.0, mean=3926.97, median=473.0
q_creditcardintinc: min=-2527000.0, max=16658762.0, mean=1757.92, median=0.0
q_intincnet: min=-12039000.0, max=24586000.0, mean=8669.73, median=768.0
q_tradingassetintinc: min=-994000.0, max=3572000.0, mean=316.35, median=0.0
q_nonintinc: min=-7074000.0, max=16819000.0, mean=5372.75, median=117.0
q_intexp: min=-10933000.0, max=18361000.0, mean=4508.09, median=474.0
q_intexpalldep: min=-7391000.0, max=13168000.0, mean=3344.57, median=443.0
q_mmdacctdepexp: min=-33762.0, max=1095000.0, mean=438.82, median=49.0
q_othersavdepexp: min=-24531.0, max=331000.0, mean=232.62, median=36.0
q_nonintexp: min=-12639000.0, max=22381000.0, mean=8563.77, median=620.0
q_exponpremises: min=-1435000.0, max=2248000.0, mean=916.36, median=80.0
q_salaries: min=-4991000.0, max=10750000.0, mean=3714.93, median=308.0
q_netinc: min=-13469374.0, max=13999000.0, mean=2908.90, median=176.0
q_netincbec: min=-13469299.0, max=14000000.0, mean=2905.21, median=175.0
q_stocknetsale: min=-4726610.0, max=16193099.0, mean=217.93, median=0.0
q_changestobuscomb: min=-43617000.0, max=62413000.0, mean=1781.85, median=0.0
q_prfdiv: min=-47436.0, max=162000.0, mean=10.40, median=0.0
q_commondiv: min=-3664770.0, max=35000000.0, mean=2996.66, median=0.0
q_domdepservicecharges: min=-2084000.0, max=2989434.0, mean=706.94, median=55.0
q_intandnonintexp: min=-23572000.0, max=39980000.0, mean=13088.80, median=1181.0
q_intexpsubordinated: min=-866000.0, max=552000.0, mean=105.14, median=0.0
q_intanddivincsecurities: min=-3952000.0, max=5712000.0, mean=1974.45, median=230.0
q_loanleaselossprovision: min=-9044000.0, max=10396000.0, mean=1322.38, median=25.0
q_totloanchargeoff: min=-3594000.0, max=9586000.0, mean=1450.06, median=18.0
q_totloanrecoveries: min=-267000.0, max=1428627.0, mean=280.97, median=5.0
q_loanleaseallowance: min=-3501000.0, max=25481070.0, mean=5096.13, median=51.0
q_realloanchargeoff: min=-2084000.0, max=3961392.0, mean=711.65, median=0.0
q_ciloanchargeoff: min=-581000.0, max=1244000.0, mean=282.43, median=0.0
q_persloanschargeoff: min=-792000.0, max=7924000.0, mean=1588.22, median=4.0
q_res1_4famloanchargeoff: min=-1235174.0, max=1820000.0, mean=254.64, median=0.0
q_intexptimedepge100k: min=-1888000.0, max=1276114.0, mean=671.14, median=97.0
q_intexptimedeple100k: min=-2393000.0, max=1640531.0, mean=897.31, median=177.0
q_intexptimedeple250k: min=-34247.0, max=1758000.0, mean=1207.09, median=121.0
q_intexptimedepge250k: min=-30000.0, max=2277000.0, mean=637.25, median=34.0
q_intexptimedep: min=-4281000.0, max=3060000.0, mean=1499.52, median=288.0
q_tradingrevenue: min=-7587000.0, max=9114000.0, mean=1001.82, median=0.0
q_intincbaldue: min=-1173357.0, max=6898000.0, mean=430.60, median=3.0
q_intinctreasuriesagencydebt: min=-239000.0, max=1833000.0, mean=451.38, median=47.0
q_intincmbs: min=-3222000.0, max=3983000.0, mean=1832.42, median=40.0
q_intincothersecurities: min=-672000.0, max=2102000.0, mean=719.42, median=40.0
q_intincfedfundsrepoasset: min=-204000.0, max=3773000.0, mean=336.04, median=15.0
q_intincloans: min=-18198000.0, max=23212000.0, mean=9680.95, median=946.0
q_intincreloans1to4fam: min=-7914000.0, max=5820618.0, mean=4172.12, median=417.0
q_intincreloansother: min=-2924000.0, max=2451000.0, mean=4033.02, median=648.0
q_intincagloans: min=-688065.0, max=688569.0, mean=200.45, median=32.0
q_intincagloans_v2: min=-688065.0, max=688569.0, mean=140.00, median=9.0
q_intincciloans: min=-3609000.0, max=3782000.0, mean=3490.34, median=206.0
q_intincpersccards: min=-2527000.0, max=16658762.0, mean=2810.41, median=0.0
q_intincpersother: min=-2318000.0, max=1829000.0, mean=1414.65, median=67.0
q_intincforloans: min=-691000.0, max=7593000.0, mean=43254.64, median=18.0
q_intincleases: min=-843000.0, max=637000.0, mean=156.30, median=0.0
q_intincassets: min=-22972000.0, max=42185000.0, mean=13177.58, median=1330.0
q_intexptransdep: min=-139000.0, max=4024000.0, mean=254.13, median=27.0
q_intexpsavdep: min=-1947000.0, max=3192000.0, mean=904.35, median=76.0
q_intexpfordep: min=-1024000.0, max=5325000.0, mean=527.66, median=0.0
q_intexpfedfundsrepoliab: min=-594000.0, max=2896000.0, mean=437.19, median=0.0
q_intexptradingandborrowed: min=-2082000.0, max=6175000.0, mean=711.84, median=0.0
q_intincpersloans: min=-2492000.0, max=18112500.0, mean=4225.05, median=70.0
q_persloansintinc: min=-2492000.0, max=18112500.0, mean=4758.74, median=83.0
q_intincreloans: min=-10838000.0, max=10007000.0, mean=8069.49, median=1209.0
q_intexpdomdep: min=-6367000.0, max=9013000.0, mean=2648.49, median=443.0
fedfundsrate: min=0.0007000000000000001, max=0.191, mean=0.06, median=0.0545
__index_level_0__: min=0, max=499999, mean=249651.21, median=249649.0
```

### Date/Datetime Column Statistics
```
date: min=1976-03-31 00:00:00, max=2024-03-31 00:00:00
rssdsubmissiondate: min=2005-07-12 21:51:43, max=2024-11-14 17:39:51
```

---

## wrds_struct_rel_ultimate.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_bank_premium/wrds_struct_rel_ultimate.parquet`
**Size:** 246.8 MB | **Type:** Parquet | **Shape:** 12,598,205 rows × 12 columns

### Columns
```
reln_year                                Int64          
focal_rssd_id                            Decimal(precision=7, scale=0)
focal_name                               String          (0.2% null)
position                                 Int64          
immediate_rssd_id                        Decimal(precision=7, scale=0)
immediate_name                           String          (0.2% null)
primary_flag                             Int64          
ultimate_rssd_id                         Decimal(precision=7, scale=0)
ultimate_name                            String          (0.2% null)
recursive_flag                           Int64          
tree                                     String         
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
reln_year: min=1923, max=2025, mean=2008.41, median=2010.0
position: min=0, max=31, mean=3.66, median=3.0
primary_flag: min=0, max=1, mean=0.64, median=1.0
recursive_flag: min=0, max=1, mean=0.02, median=0.0
__index_level_0__: min=0, max=499999, mean=248433.47, median=248035.0
```

---

## CRSP_Comp_Link_Table.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_crsp_compustat/CRSP_Comp_Link_Table.parquet`
**Size:** 752347 bytes | **Type:** Parquet | **Shape:** 39,192 rows × 6 columns

### Columns
```
gvkey                                    String         
permno                                   Float64        
linktype                                 String         
linkprim                                 String         
linkdt                                   Datetime(time_unit='ns', time_zone=None)
linkenddt                                Datetime(time_unit='ns', time_zone=None) (26.4% null)
```

### Numeric Column Statistics
```
permno: min=10000.0, max=93436.0, mean=51742.16, median=53502.0
```

### Date/Datetime Column Statistics
```
linkdt: min=1949-07-01 00:00:00, max=2024-12-31 00:00:00
linkenddt: min=1958-12-23 00:00:00, max=2025-01-31 00:00:00
```

---

## CRSP_stock_ciz.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_crsp_compustat/CRSP_stock_ciz.parquet`
**Size:** 99.3 MB | **Type:** Parquet | **Shape:** 5,117,080 rows × 17 columns

### Columns
```
permno                                   Int64          
permco                                   Int64          
mthcaldt                                 Datetime(time_unit='ns', time_zone=None)
issuertype                               String         
securitytype                             String         
securitysubtype                          String         
sharetype                                String         
usincflg                                 String         
primaryexch                              String         
conditionaltype                          String         
tradingstatusflg                         String         
mthret                                   Float64         (1.6% null)
mthretx                                  Float64         (1.6% null)
shrout                                   Float64         (0.1% null)
mthprc                                   Float64         (1.6% null)
jdate                                    Datetime(time_unit='ns', time_zone=None)
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
permno: min=10000, max=93436, mean=52253.69, median=54148.0
permco: min=2, max=60123, mean=22973.22, median=21102.0
mthret: min=-1.0, max=39.0, mean=0.01, median=0.0
mthretx: min=-1.0, max=39.0, mean=0.01, median=0.0
shrout: min=1.0, max=29206400.0, mean=48419.85, median=8500.0
mthprc: min=0.0006, max=724040.0, mean=37.35, median=14.75
__index_level_0__: min=0, max=499999, mean=245618.85, median=244145.5
```

### Date/Datetime Column Statistics
```
mthcaldt: min=1925-12-31 00:00:00, max=2024-12-31 00:00:00
jdate: min=1925-12-31 00:00:00, max=2024-12-31 00:00:00
```

---

## Compustat.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_crsp_compustat/Compustat.parquet`
**Size:** 11.0 MB | **Type:** Parquet | **Shape:** 578,269 rows × 10 columns

### Columns
```
gvkey                                    String         
datadate                                 Datetime(time_unit='ns', time_zone=None)
at                                       Float64         (16.2% null)
pstkl                                    Float64         (16.3% null)
txditc                                   Float64         (23.2% null)
pstkrv                                   Float64         (16.7% null)
seq                                      Float64         (18.1% null)
pstk                                     Float64         (16.8% null)
year                                     Int32          
__index_level_0__                        Int64          
```

### Numeric Column Statistics
```
at: min=0.0, max=4349731.0, mean=6123.65, median=112.8
pstkl: min=-0.421, max=526300.0, mean=35.58, median=0.0
txditc: min=-285.769, max=92344.0, mean=112.06, median=0.0
pstkrv: min=-67.0, max=526300.0, mean=36.62, median=0.0
seq: min=-86154.0, max=649368.0, mean=1061.90, median=43.6245
pstk: min=-252.0, max=139966.0, mean=30.69, median=0.0
year: min=1959, max=2025, mean=1998.41, median=1999.0
__index_level_0__: min=0, max=499999, mean=221458.75, median=210865.0
```

### Date/Datetime Column Statistics
```
datadate: min=1959-01-31 00:00:00, max=2025-07-31 00:00:00
```

---

## FF_FACTORS.parquet
**Path:** `/Users/jbejarano/GitRepositories/ftsfr/_data/wrds_crsp_compustat/FF_FACTORS.parquet`
**Size:** 44036 bytes | **Type:** Parquet | **Shape:** 1,188 rows × 9 columns

### Columns
```
date                                     Datetime(time_unit='ns', time_zone=None)
mktrf                                    Decimal(precision=6, scale=6)
smb                                      Float64        
hml                                      Float64        
rf                                       Decimal(precision=5, scale=5)
year                                     Float64        
month                                    Float64        
umd                                      Decimal(precision=6, scale=6) (0.5% null)
dateff                                   Date            (0.5% null)
```

### Numeric Column Statistics
```
smb: min=-0.1741, max=0.3596, mean=0.00, median=0.0006
hml: min=-0.1383, max=0.3552, mean=0.00, median=0.0014
year: min=1926.0, max=2025.0, mean=1975.50, median=1975.5
month: min=1.0, max=12.0, mean=6.50, median=6.5
```

### Date/Datetime Column Statistics
```
date: min=1926-07-31 00:00:00, max=2025-06-30 00:00:00
dateff: min=1926-07-31, max=2024-12-31
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