# Financial Time Series Forecasting Repository (FTSFR) Paper - To-Do List

## 1. Introduction and Motivation
**Write introduction emphasizing the critical need for standardized benchmarks in macro-finance**

_STATUS:_ Not started

Detailed tasks:
- Establish that time series forecasting is ubiquitous and prevalent in macroeconomics and finance domains
- Highlight the current gap: no existing standardized benchmarks for evaluating forecasting algorithms in macro-finance
- Explain why apples-to-apples comparisons are impossible without standardized datasets
- Stress that researchers currently evaluate their own models on arbitrarily chosen datasets, making comparisons meaningless
- Position this work as filling a critical gap in quantitative finance research
- Emphasize that this complements (not substitutes) the Monash benchmark - researchers interested in economics and finance would use this benchmark, while those in other domains might use Monash, but ideally both should be used
- Make clear that the lack of standardization is particularly problematic in finance where data often requires subscriptions (WRDS, Bloomberg, etc.)

## 2. Literature Review and Positioning
**Position the paper relative to existing benchmarks and establish the canonical nature of chosen cleaning methods**

_STATUS:_ Not started

Detailed tasks:
- Review the Monash Time Series Forecasting Archive and explain how FTSFR follows their established template
- Introduce He, Kelly, Manela (2017) as the anchor paper for asset class selection and cleaning methods
  - Explain how they surveyed multiple asset classes and chose canonical papers for each
  - List the specific asset classes they cover and why these are comprehensive
- Introduce Siriwardane, Sunderam, & Wallen (2022) "Segmented Arbitrage" as the anchor for arbitrage spread construction
  - Explain how they assembled various arbitrage trades across asset classes
  - List the specific arbitrage spreads and their importance for understanding market efficiency
- Emphasize that the choice to follow these papers is deliberate - not doing anything novel is a FEATURE, not a bug
  - The goal is standardization using well-established, canonical methods
  - Each cleaning method represents the consensus approach in its respective literature
- Acknowledge that some dataset choices are somewhat ad hoc but are anchored by these survey-style papers

## 3. Data Repository Overview
**Provide high-level description of the repository structure and contents**

_STATUS:_ Not started

Detailed tasks:
- Describe the automated data pulling framework
  - Explain how the code automates end-to-end process from data pull to final cleaning
  - Note that most data comes from WRDS (commonly available at universities) and Bloomberg
  - Provide overview of the dodo.py task automation system
- List the major categories of data:
  - Asset returns across multiple classes (following He, Kelly, Manela)
  - Arbitrage spreads (following Siriwardane et al.)
  - Macroeconomic indicators for forecasting
  - Financial institution data for stability monitoring
- Explain the dual purpose: both for forecasting benchmarks AND for replicating important finance papers
- Note that replication code for many of these papers was not previously publicly available - this is a key contribution

## 4. Asset Class Datasets (Following He, Kelly, Manela)
**Document each asset class dataset with its canonical cleaning method**

_STATUS:_ Not started

For EACH asset class, create a subsection that includes:
- Which specific paper's cleaning method is being replicated
- Why this dataset/asset class is important for macro-finance
- Key cleaning decisions and their justifications
- Summary statistics that match the original paper (proving correct replication)

Asset classes to cover:
- **Equity**: Fama-French 25 portfolios and CRSP universe
  - Explain exclusion of small stocks, ADRs, etc. following Fama-French (1993)
  - Show replication of key statistics
- **US Bonds**: Government and corporate bonds
  - Government: CRSP maturity-sorted portfolios  
  - Corporate: Nozawa (2017) yield-spread sorted portfolios
  - Explain why US government and corporate are combined (high correlation)
- **Sovereign Bonds**: Borri and Verdelhan (2012) portfolios
  - Two-way sort on US equity correlation and S&P rating
- **Options**: Constantinides, Jackwerth and Savov (2013) S&P 500 portfolios
  - 54 portfolios sorted by moneyness and maturity
  - Leverage-adjusted returns methodology
- **Foreign Exchange**: Combined datasets
  - Lettau et al. (2014) interest rate differential sorted
  - Menkhoff et al. (2012) momentum sorted
- **Commodities**: Yang (2013) methodology
  - 31 commodities with futures up to 4 months
  - Selection criteria based on data availability
- **CDS**: Markit data following Palhares (2013)
  - 5-year contracts sorted by spread
  - Return calculation methodology

## 5. Arbitrage Spread Datasets (Following Siriwardane et al.)
**Document each arbitrage spread construction**

_STATUS:_ Not started

For EACH arbitrage spread:
- Explain the economic intuition behind the trade
- Detail the exact construction methodology
- Show replication of statistics from Siriwardane et al.
- Discuss what violations of these spreads tell us about market segmentation

Spreads to cover:
- **CIP (Covered Interest Parity)**: Construction using spot, forward FX and interest rates
- **Box Spread**: Options-based arbitrage using put-call parity
- **Equity Spot-Futures**: Cash vs futures arbitrage
- **Treasury Spot-Futures**: Government bond basis trades  
- **Treasury Swap Spread**: Treasury vs interest rate swap arbitrage
- **TIPS-Treasury**: Inflation-linked vs nominal bond spreads
- **CDS-Bond Basis**: Credit default swap vs cash bond arbitrage

## 6. Additional Macro-Finance Datasets
**Document datasets for macroeconomic forecasting and financial stability monitoring**

_STATUS:_ Not started

Detailed tasks:
- **Bank Call Report Data**: NYU archive (Schnabl)
  - Explain importance for financial stability monitoring
  - Key series selection (leverage, liquidity, etc.)
- **Treasury Yield Curve**: Fed data following Gürkaynak et al.
  - Zero-coupon curve construction
  - Importance for asset pricing and monetary policy
- **Industrial Production**: Following Foerster et al. methodology
  - Sectoral vs aggregate shocks
- **FRED-MD**: Macroeconomic indicators
  - Selection criteria and transformations
- **Bank-specific metrics**: Using WRDS Bank Premium
  - Systemic risk indicators
  - Bank health metrics

## 7. Replication Results and Validation
**Demonstrate successful replication of all source papers**

_STATUS:_ Not started

Detailed tasks:
- Create comprehensive replication tables showing:
  - Original paper's summary statistics
  - Our replication results
  - Any discrepancies and their explanations
- Include specific sections for:
  - He, Kelly, Manela factor loadings and test portfolio returns
  - Siriwardane et al. arbitrage spread statistics
  - Individual dataset paper replications (Nozawa, Borri & Verdelhan, etc.)
- Document any data quality issues discovered
- Explain any necessary deviations from original methodologies
- Provide robustness checks where appropriate

## 8. Baseline Forecasting Methodology
**Define forecasting approach following Monash template**

_STATUS:_ Not started

Detailed tasks:
- Justify choice of error metrics:
  - Use same metrics as Monash for consistency (MASE, sMAPE, RMSE, etc.)
  - Explain why scale-free metrics are important for cross-dataset comparison
  - Discuss metric selection for different data types (prices vs returns, etc.)
- Select baseline forecasting models:
  - Traditional: ARIMA, ETS, Theta, etc. (matching Monash)
  - Machine Learning: Random Forest, XGBoost, etc.
  - Deep Learning: LSTM, Transformer, N-BEATS, etc.
  - Use same model implementations as Monash where possible
- Define evaluation methodology:
  - Train/test splits appropriate for financial data
  - Handling of structural breaks
  - Treatment of different data frequencies

## 9. Baseline Results and Analysis
**Present comprehensive forecasting results across all datasets**

_STATUS:_ Not started

Detailed tasks:
- Create results tables in exact same format as Monash paper:
  - One table per error metric
  - Models in columns, datasets in rows
  - Highlight best performer per dataset
- Analyze patterns in results:
  - Which models work best for which asset classes
  - How financial data differs from Monash datasets
  - Role of data frequency and sample size
  - Impact of financial crises and regime changes
- Compare with Monash findings where applicable
- Discuss implications for practitioners

## 10. Implementation and Code Documentation
**Explain technical architecture and usage**

_STATUS:_ Not started

Detailed tasks:
- Document the automation framework:
  - dodo.py task structure
  - Dependency management
  - Configuration system (config.toml)
- Provide clear usage instructions:
  - Required subscriptions (WRDS, Bloomberg)
  - Installation process  
  - How to run specific datasets
  - How to add new datasets
- Explain design decisions:
  - Why certain technologies were chosen
  - Trade-offs in automation approach
  - Extensibility considerations
- Include code examples for common tasks

## 11. Reproducibility and Data Availability
**Ensure full reproducibility of all results**

_STATUS:_ Not started

Detailed tasks:
- Document exact data vintage used
- Provide checksums for all processed datasets
- Include random seeds for all stochastic processes
- Detail computational environment:
  - Package versions (requirements.txt)
  - Hardware used for baseline results
  - Approximate runtimes
- Explain data access requirements:
  - Which subscriptions are needed for which datasets
  - How to request access
  - Alternative data sources where available
- Create reproducibility checklist

## 12. Paper Writing and Formatting
**Ensure paper follows academic standards and journal requirements**

_STATUS:_ Not started

Detailed tasks:
- Follow structure of Monash paper closely:
  - Similar section organization
  - Comparable level of detail
  - Same table/figure formats where appropriate
- Include all standard sections:
  - Abstract emphasizing contribution
  - Proper keyword selection
  - Data availability statement
  - Code availability statement
  - Acknowledgments of data providers
- Prepare supplementary materials:
  - Extended results tables
  - Additional robustness checks
  - Detailed data descriptions
- Ensure proper citations for all replicated methods

## 13. Future Work and Extensions
**Outline potential extensions while keeping current scope focused**

_STATUS:_ Not started

Detailed tasks:
- Discuss potential additional datasets:
  - Real estate (REITs)
  - Cryptocurrencies
  - ESG metrics
  - Alternative data
- Propose enhanced forecasting methods:
  - Ensemble approaches
  - Transfer learning across asset classes
  - Incorporating economic priors
- Suggest infrastructure improvements:
  - Real-time data updates
  - Cloud deployment
  - API access
- Note community contribution guidelines

## 14. Final Checks and Submission Preparation
**Ensure paper and repository are publication-ready**

_STATUS:_ Not started

Detailed tasks:
- Verify all replication results one final time
- Run all baseline forecasts with fresh seeds
- Check all hyperlinks and data URLs
- Ensure code runs on clean environment
- Get feedback from domain experts
- Prepare journal submission materials:
  - Cover letter emphasizing contribution
  - Response to anticipated reviewer concerns
  - Highlight practical impact for researchers
- Create project website with:
  - Easy download links
  - Visualization of results
  - Community forum for questions
