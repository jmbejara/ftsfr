#!/bin/bash
# Test script to demonstrate workflow separation

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test dataset setup
export DATASET_PATH="../_data/ftsfr_us_treasury_returns.parquet"
# Optional: override dataset configuration
# export SEASONALITY="10"  # Override from datasets_config.toml

echo -e "${BLUE}=== Testing Workflow Separation ===${NC}"
echo "Dataset: US Treasury Returns (auto-configured)"
echo "Model: ARIMA"
echo ""
echo "Configuration will be loaded from datasets_config.toml"
echo ""

# Step 1: Training
echo -e "${GREEN}Step 1: Training Phase${NC}"
echo "Running: python run_model.py --model arima --workflow train"
python run_model.py --model arima --workflow train

echo ""
echo -e "${GREEN}Model saved to: ${OUTPUT_DIR}/models/arima/us_treasury_returns/${NC}"
ls -la ${OUTPUT_DIR}/models/arima/us_treasury_returns/
echo ""

# Step 2: Inference
echo -e "${GREEN}Step 2: Inference Phase${NC}"
echo "Running: python run_model.py --model arima --workflow inference"
python run_model.py --model arima --workflow inference

echo ""
echo -e "${GREEN}Predictions saved to: ${OUTPUT_DIR}/forecasts/arima/us_treasury_returns/${NC}"
ls -la ${OUTPUT_DIR}/forecasts/arima/us_treasury_returns/
echo ""

# Step 3: Evaluation
echo -e "${GREEN}Step 3: Evaluation Phase${NC}"
echo "Running: python run_model.py --model arima --workflow evaluate"
python run_model.py --model arima --workflow evaluate

echo ""
echo -e "${GREEN}Results saved to: ${OUTPUT_DIR}/raw_results/arima/${NC}"
ls -la ${OUTPUT_DIR}/raw_results/arima/
echo ""

echo -e "${BLUE}=== Workflow Separation Test Complete ===${NC}"