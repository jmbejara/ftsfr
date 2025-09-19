# Forecasting System Documentation

## Overview

This forecasting system provides robust time series forecasting using both **statistical models** (StatsForecast) and **neural network models** (NeuralForecast). The system includes comprehensive data preprocessing, quality filtering, and evaluation capabilities designed to handle real-world financial time series data with missing values, irregular patterns, and varying lengths.

### Key Features

- **Robust Preprocessing Pipeline**: Handles missing data, irregular grids, and quality filtering
- **Unified Data Processing**: Same preprocessing for both statistical and neural models
- **Adaptive Quality Requirements**: Different standards based on data frequency (daily, monthly, etc.)
- **Graceful Error Handling**: Warnings instead of crashes for data quality issues
- **Comprehensive Evaluation**: Multiple metrics (MASE, MSE, RMSE, R²oos) with proper handling

### When to Use Which Models

**StatsForecast Models** (`forecast_stats.py`):
- Use for: Well-behaved time series with clear patterns
- Good for: Baseline comparisons, fast computation, interpretable results
- Models: AutoARIMA, AutoETS, Seasonal Naive, etc.
- Best suited for: Series with sufficient length and regular patterns

**NeuralForecast Models** (`forecast_neural.py`):
- Use for: Complex patterns, cross-series learning, longer series
- Good for: Non-linear relationships, capturing complex seasonality
- Models: AutoNBEATS, AutoNHITS, AutoDeepAR, AutoTransformer, etc.
- Best suited for: Panel data with multiple series of similar nature

---

## Data Processing Pipeline

The system uses a **5-step robust preprocessing pipeline** that ensures data quality and consistency across all models:

### Step 1: Raw Data Loading & Cleaning

**What happens:**
- Load data from `.parquet` files
- Standardize column names (`unique_id`, `ds`, `y`)
- Remove system columns (e.g., `__index_level_*`)
- Convert to proper data types (Float32 for `y`)
- Handle infinite and NaN values

**Why this matters:**
- Ensures consistent data format across all datasets
- Prevents downstream errors from malformed data
- Standardizes missing value representation

### Step 2: Canonical Grid Building

**What happens:**
- Use `fill_gaps()` with `start='per_serie'` and `end='per_serie'`
- Create regular time grids for each series individually
- No artificial padding at the beginning or end of series
- Preserve natural start/end dates for each time series

**Why this matters:**
- Time series models require regular grids (no missing dates)
- `per_serie` approach avoids artificial data creation
- Each series maintains its natural timeline
- Missing values become explicit (NaN) rather than missing dates

**Example:**
```
Before: Series A has [2020-01, 2020-03, 2020-05] (missing Feb, Apr)
After:  Series A has [2020-01, 2020-02, 2020-03, 2020-04, 2020-05]
        with NaN for Feb and Apr
```

### Step 3: Train/Test Splitting

**What happens:**
- Split each series individually: last `test_size` observations = test
- Remaining observations = training
- No imputation in test period (keeps original NaN values)
- Test size based on data frequency:
  - Monthly (ME): 36 months
  - Daily (D): 90 days
  - Quarterly (QE): 12 quarters

**Why this matters:**
- Realistic evaluation setup (always predict recent periods)
- Never contaminate test data with imputed values
- Consistent evaluation windows across datasets
- Each series contributes the same amount to test evaluation

### Step 4: Quality Filtering

**What happens:**
- Check minimum data requirements (frequency-aware and scaled to the forecast horizon)
- Filter out series with insufficient variation (near-constant)
- Remove series with too many gaps (>60% missing in training)
- Ensure sufficient data in both training and test periods

**Base Quality Requirements by Frequency:**

| Frequency | Base Min Total | Base Min Train | Base Min Test | Variance Threshold |
|-----------|----------------|----------------|---------------|-------------------|
| Monthly (ME) | 16 | 12 | 4 | 0.001 |
| Daily (D) | 16 | 12 | 4 | 0.001 |
| Quarterly (QE) | 27 | 18 | 9 | 0.01 |
| Yearly (YE) | 40 | 30 | 10 | 0.05 |

These are **starting points**. When the evaluation window is long (for example a 36-month test set) the pipeline automatically scales the thresholds so that:
- Training retains at least ~75% of the forecast horizon for monthly data (50% for daily)
- The test window has at least ~25% non-null observations
- The total grid length is large enough to support the required training coverage (e.g. 36-month test + 27 train -> 63 total)

**Example:** Monthly dataset with a 36-month holdout -> requirements become 63 total observations, 27 non-null in training, and 9 non-null in test. These adaptive thresholds avoid filtering everything out while still ensuring the models see enough history to learn.

**Why this matters:**
- Models need sufficient data to learn patterns
- Very sparse or constant series produce unreliable forecasts
- Different frequencies and test windows need different amounts of history
- Prevents misleading results from poor-quality data

### Step 5: Light Train-Only Imputation

**What happens:**
- Apply forward-fill imputation **only to training data**
- Add gap indicator flags (`is_gap`, `has_value`)
- Never impute test data (keeps NaN for proper evaluation)
- Models can use gap flags to understand data quality

**Why this matters:**
- Statistical models often can't handle NaN values
- Neural models drop training windows with NaN targets
- Forward-fill is conservative (no future information)
- Gap flags help models understand data reliability
- Test data remains untouched for honest evaluation

---

## Model-Specific Considerations

### StatsForecast Models

**Data Requirements:**
- Need regular grids (no missing dates)
- Cannot handle NaN values inside series
- Work best with moderate-length series (50-500 observations)
- Require sufficient variation to estimate parameters

**How the Pipeline Helps:**
- Grid building ensures regular timestamps
- Train-only imputation removes NaN from training
- Quality filtering removes problematic series
- Test data kept clean for proper MASE calculation

**Common Models:**
- **AutoARIMA**: Automatically selects ARIMA parameters
- **AutoETS**: Exponential smoothing with automatic selection
- **Seasonal Naive**: Simple seasonal baseline
- **Historic Average**: Overall mean baseline

### NeuralForecast Models

**Data Requirements:**
- Need regular grids (no missing dates)
- Drop training windows containing NaN targets
- Benefit from larger datasets (panel effects)
- Can handle complex non-linear patterns

**How the Pipeline Helps:**
- Grid building ensures regular timestamps
- Light imputation increases available training windows
- Quality filtering ensures sufficient series length
- Gap flags provide model awareness of data quality

**Common Models:**
- **AutoNBEATS**: Neural basis expansion (interpretable)
- **AutoNHITS**: Hierarchical interpolation transformer
- **AutoDeepAR**: Probabilistic autoregressive model
- **AutoTransformer**: Attention-based sequence model

---

## Usage Examples

### Basic Statistical Forecasting

```bash
# Run AutoARIMA on monthly CDS data
python forecast_stats.py --dataset ftsfr_CDS_bond_basis_non_aggregated --model auto_arima

# Debug mode (faster, limited data)
python forecast_stats.py --dataset ftsfr_he_kelly_manela_factors_monthly --model auto_arima --debug
```

### Basic Neural Forecasting

```bash
# Run AutoNBEATS on monthly factor data
python forecast_neural.py --dataset ftsfr_he_kelly_manela_factors_monthly --model auto_nbeats

# Debug mode (fewer hyperparameter samples)
python forecast_neural.py --dataset ftsfr_CDS_bond_basis_non_aggregated --model auto_nhits --debug
```

### Available Models

**Statistical Models** (`forecast_stats.py`):
- `auto_arima` - Automatic ARIMA selection
- `auto_ets` - Automatic exponential smoothing
- `auto_ces` - Complex exponential smoothing
- `seasonal_naive` - Seasonal random walk baseline
- `theta` - Theta method forecasting

**Neural Models** (`forecast_neural.py`):
- `auto_nbeats` - Neural basis expansion
- `auto_nhits` - Hierarchical interpolation transformer
- `auto_deepar` - Deep autoregressive model
- `auto_dlinear` - Deep linear model
- `auto_vanilla_transformer` - Vanilla transformer
- `auto_tide` - Time-series dense encoder

---

## Expected Outputs

### Console Output

Both scripts provide detailed progress information:

```
============================================================
Simple Forecast Statistics with Cross-Validation
============================================================
Dataset: ftsfr_he_kelly_manela_factors_monthly
Model: auto_arima

1. Loading Dataset: ftsfr_he_kelly_manela_factors_monthly
----------------------------------------
Frequency: MS (Polars: 1mo)
Seasonality: 1
Test size (last N observations): 36

2. Loading and Preprocessing Data
----------------------------------------
Raw data loaded: 15000 observations, 1250 series
==================================================
ROBUST PREPROCESSING PIPELINE
==================================================
  Building canonical time grid...
    Grid built: 1250 ’ 1250 series
  Splitting train/test (test_size=36)...
    Split completed: 12000 train, 3000 test observations
  Filtering series by data quality...
    Requirements: {'min_total_obs': 99, 'min_train_obs': 72, 'min_test_obs': 27, 'variance_threshold': 0.001, 'max_gap_ratio': 0.6}
  Final result: 85 series passed all quality checks
==================================================
Final data for CV: 8500 observations, 85 series

[... cross-validation progress ...]

6. Model Performance Summary
----------------------------------------
+-----------+------------+-----------+------------+-------------+
| Model     |   Avg MASE |   Avg MSE |   Avg RMSE |   Avg R2oos |
+===========+============+===========+============+=============+
| AutoARIMA |     0.8234 |    2.4567 |     1.5674 |      0.1234 |
+-----------+------------+-----------+------------+-------------+
```

### File Outputs

**Error Metrics CSV** (`./_output/forecasting/error_metrics/{dataset}/{model}.csv`):
```csv
model_name,dataset_name,MASE,MSE,RMSE,R2oos,time_taken
auto_arima,ftsfr_he_kelly_manela_factors_monthly,0.8234,2.4567,1.5674,0.1234,45.67
```

**Lightning Logs** (Neural models only, `./_output/forecasting/logs/{dataset}/{model}/`):
- Hyperparameter optimization trials
- Training logs and checkpoints
- Model performance metrics

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. "No series meet the data quality requirements"

**Problem**: All series filtered out during quality checks.

**Causes & Solutions**:
- **Too sparse data**: Many series have >60% missing values
  - *Solution*: Use datasets with better coverage, or relax `max_gap_ratio` in `robust_preprocessing.py`
- **Too short series**: Series don't meet minimum length requirements
  - *Solution*: Use smaller test sizes, or datasets with longer series
- **Near-constant series**: No variation in values
  - *Solution*: Check data processing, ensure proper scaling

**Debug**: Run with `--debug` to see first 5 series quality checks:
```bash
python forecast_stats.py --dataset your_dataset --model auto_arima --debug
```

#### 2. "MASE is exactly 0.0" Warning

**Problem**: Mean Absolute Scaled Error = 0, indicating potential issues.

**Common Causes**:
- Model produces constant predictions
- Actual values are constant or very similar
- Data scaling issues in neural models

**Solutions**:
- Check data quality (use debug mode to see actual vs predicted values)
- Try different models (neural models often more robust)
- Verify time series has sufficient variation

**Note**: This is now a *warning* not an error - the system continues with other metrics.

#### 3. Neural Models Taking Too Long

**Problem**: Hyperparameter optimization is slow.

**Solutions**:
- Use `--debug` mode (2 samples instead of 20)
- Choose simpler models (`auto_dlinear`, `auto_nlinear`)
- Reduce `max_steps` in model configurations
- Use smaller datasets for testing

#### 4. Memory Issues with Large Datasets

**Problem**: Out of memory errors during processing.

**Solutions**:
- Use `--debug` mode to limit series count
- Implement chunked processing for very large datasets
- Increase system memory or use cloud instances
- Filter to most important series before processing

#### 5. Inconsistent Results Between Runs

**Problem**: Different metrics on repeated runs.

**Causes**:
- Neural models use random initialization
- Cross-validation window alignment varies
- Data quality filtering varies (if data changes)

**Solutions**:
- Set random seeds in model configurations
- Use larger datasets for more stable results
- Average results across multiple runs
- Use statistical models for reproducible baselines

---

## Performance Optimization Tips

### For Faster Development

1. **Use Debug Mode**: `--debug` flag limits data and iterations
2. **Test on Small Datasets**: Validate pipeline before large runs
3. **Start with Simple Models**: `auto_arima` or `auto_dlinear` are fastest
4. **Parallel Processing**: Both systems use multiple cores automatically

### For Production Runs

1. **Data Quality**: Pre-filter datasets to remove very sparse series
2. **Model Selection**: Neural models for complex patterns, statistical for baselines
3. **Hyperparameter Tuning**: Increase `num_samples` for better neural performance
4. **Resource Planning**: Neural models need 2-10x more time than statistical

### Memory Management

1. **Chunked Processing**: Process large datasets in chunks
2. **Clean Intermediate Results**: Remove temporary files regularly
3. **Monitor Usage**: Watch memory during neural training
4. **Lightning Logs**: Clean up old training logs periodically

---

## Technical Implementation Details

### File Structure

```
src/forecasting/
   README.md                        # This documentation
   forecast_stats.py               # Statistical forecasting script
   forecast_neural.py              # Neural forecasting script
   robust_preprocessing.py         # Unified preprocessing pipeline
   forecast_utils.py               # Shared utility functions
   [other utility scripts]
```

### Key Functions

**`robust_preprocess_pipeline()`**: Complete preprocessing pipeline
- Input: Raw dataframe, frequency, test_size, seasonality
- Output: Filtered train_df and test_df with quality guarantees

**`get_data_requirements()`**: Adaptive quality requirements by frequency
**`build_canonical_grid()`**: Create regular time grids with fill_gaps
**`filter_series_by_quality()`**: Remove problematic series
**`evaluate_cv()`**: Comprehensive model evaluation with multiple metrics

### Dependencies

- **Polars**: Fast dataframe operations
- **StatsForecast**: Classical time series models
- **NeuralForecast**: Neural network models with auto-tuning
- **utilsforecast**: Preprocessing and evaluation utilities
- **Optuna**: Hyperparameter optimization (neural models)
- **PyTorch Lightning**: Neural model training framework

---

## Contributing & Customization

### Adding New Datasets

1. Add dataset configuration to `datasets.toml`
2. Ensure proper frequency and seasonality settings
3. Test with debug mode first
4. Document any dataset-specific considerations

### Adding New Models

**Statistical Models** (forecast_stats.py):
1. Import model from StatsForecast
2. Add to `model_mapping` dictionary
3. Update argument parser choices
4. Test with various datasets

**Neural Models** (forecast_neural.py):
1. Import from NeuralForecast
2. Create configuration function (see examples)
3. Add to `model_mapping` with proper config
4. Test with debug mode first

### Modifying Quality Requirements

Edit `get_data_requirements()` in `robust_preprocessing.py`:
- Adjust multipliers by frequency
- Change variance thresholds
- Modify gap ratio limits
- Add new frequency types

**Be careful**: Stricter requirements = fewer series but better quality.
Looser requirements = more series but potential quality issues.

---

## System Architecture

```
Raw Data (.parquet)
        “
Basic Cleaning & Standardization
        “
Canonical Grid Building (fill_gaps)
        “
Train/Test Splitting (per series)
        “
Quality Filtering (adaptive by frequency)
        “
Light Train-Only Imputation
        “
Cross-Validation Forecasting
        “
Comprehensive Evaluation
        “
Results (CSV + Console)
```

This architecture ensures **consistent, high-quality preprocessing** for both statistical and neural models while handling the real-world complexities of financial time series data.