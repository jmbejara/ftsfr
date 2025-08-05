# Unified One-Step-Ahead Forecasting Implementation

## Overview

This document describes the unified one-step-ahead forecasting implementation that ensures consistent evaluation across all model types (Darts, Nixtla, and GluonTS).

## Key Features

### 1. **True One-Step-Ahead Forecasting**
- Model is trained **once** on the training data (80%)
- For each point in the test period, the model forecasts **one step ahead** using all actual historical data up to that point
- **No retraining** occurs during the test period
- Predictions are **never** fed back as inputs

### 2. **Consistent Behavior Across All Model Types**

#### Darts Models (Local & Global)
- Previously: Used `historical_forecasts` with default parameters
- Issue: Local models would retrain by default (`retrain=True`)
- Solution: Unified implementation handles both local and global models correctly
  - Global models use `historical_forecasts` with `retrain=False`
  - Local models use manual one-step-ahead loop to avoid retraining

#### Nixtla Models
- Previously: Already implemented correctly with manual loop
- Now: Uses unified implementation for consistency and verification

#### GluonTS Models  
- Previously: Already implemented correctly with manual loop
- Now: Uses unified implementation for consistency and verification

### 3. **Verification System**
Each forecast includes automatic verification to ensure:
- Number of predictions matches test period length
- Prediction dates align with test dates
- Clear logging indicates success/failure of verification

## Implementation Details

### Core Module: `unified_one_step_ahead.py`

Contains three main functions:

1. **`perform_one_step_ahead_darts()`**
   - Handles both Local and Global Darts models
   - Uses `historical_forecasts` for global models with explicit parameters
   - Uses manual loop for local models to avoid retraining

2. **`perform_one_step_ahead_nixtla()`**
   - Iterates through test dates
   - Uses all historical data up to each test point
   - Returns DataFrame with predictions

3. **`perform_one_step_ahead_gluonts()`**
   - Creates temporary datasets with appropriate history
   - Handles different prediction formats (SampleForecast, etc.)
   - Returns DataFrame with predictions

4. **`verify_one_step_ahead()`**
   - Verifies prediction count matches test period
   - Checks date alignment for DataFrame predictions
   - Provides clear logging of verification results

### Modified Classes

All model classes now use the unified implementation:

1. **DartsMain** - Base implementation for all Darts models
2. **DartsGlobal** - Inherits unified behavior from DartsMain  
3. **DartsLocal** - Uses DartsMain's unified implementation
4. **NixtlaMain** - Updated to use unified implementation
5. **GluontsMain** - Updated to use unified implementation

## Usage

No changes required to existing model usage. The unified implementation is automatically used when calling the `forecast()` method:

```python
# Train model
model.train()

# Perform one-step-ahead forecasting
model.forecast()  # Now uses unified implementation

# Results are automatically verified
# Check logs for verification status
```

## Benefits

1. **Consistency**: All models now use the same evaluation methodology
2. **Correctness**: Ensures true one-step-ahead forecasting (no data leakage)
3. **Transparency**: Clear logging shows what's happening and verifies results
4. **Maintainability**: Single implementation to maintain instead of multiple

## Logging

The implementation provides detailed logging:

```
INFO - Starting unified one-step-ahead forecasting
INFO - Model type: Local/Global
INFO - Forecasting for N test dates
INFO - ✓ One-step-ahead forecasting verified
```

Or in case of issues:
```
WARNING - ⚠ One-step-ahead forecasting verification failed
```

## Technical Notes

### Darts Local Models
- Local models like ARIMA cannot use `retrain=False` reliably
- Manual iteration ensures no retraining occurs
- Model state is preserved throughout evaluation

### Performance Considerations
- One-step-ahead forecasting requires N predictions for N test points
- This is inherently slower than multi-step forecasting
- Progress bars show forecasting progress
- Consider using smaller test sets for faster evaluation during development

### Future Enhancements
- Parallel processing for independent series
- Caching of intermediate results
- Support for probabilistic forecasts (num_samples > 1)