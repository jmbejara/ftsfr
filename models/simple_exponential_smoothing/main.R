# Load required libraries
library(stringr)
library(here)
library(RcppTOML)
library(arrow)
library(dplyr)
library(forecast)
library(pbapply)
# install.packages(c("stringr", "here", "rcpptoml", "arrow", "dplyr", "forecast", "pbapply"))

# Load environment variables - using Sys.getenv approach instead of dotenv
# If environment variables are set via conda/pixi, this will use them
# Otherwise fall back to default paths
DATA_DIR <- Sys.getenv("DATA_DIR", unset = file.path(dirname(dirname(getwd())), "_data"))
OUTPUT_DIR <- Sys.getenv("OUTPUT_DIR", unset = file.path(dirname(dirname(getwd())), "_output"))


# Load dataset paths
datasets_info <- parseTOML(file.path(DATA_DIR, "ftsfa_datasets_paths.toml"))

# Calculate MASE (Mean Absolute Scaled Error)
calculate_mase <- function(y_true, y_pred, training_set, seasonality = 1) {
  n_train <- length(training_set)
  h <- length(y_true)
  
  # Calculate the numerator: sum of absolute errors
  numerator <- sum(abs(y_true - y_pred))
  
  # Calculate the denominator: scaled in-sample naive forecast error
  if (seasonality >= n_train) {
    # Handle case where seasonality is larger than the training set
    denominator <- sum(abs(diff(training_set)))
  } else {
    # Use seasonal naive forecast for denominator
    denominator <- sum(abs(training_set[(seasonality+1):n_train] - training_set[1:(n_train-seasonality)]))
  }
  
  # Adjust denominator as per the formula
  denominator <- denominator * (h / (n_train - seasonality))
  
  # Handle edge cases
  if (denominator == 0) {
    return(NA)
  }
  
  return(numerator / denominator)
}

# Fit Simple Exponential Smoothing model and generate forecasts
forecast_ses <- function(train_data, test_length, alpha = NULL) {
  tryCatch({
    # Use the forecast package to fit Simple Exponential Smoothing
    model <- ets(train_data, model = "ANN", alpha = alpha) # Simple exponential smoothing
    forecast_values <- forecast(model, h = test_length)
    return(forecast_values$mean)
  }, error = function(e) {
    message("Error in SES forecasting: ", e$message)
    return(rep(NA, test_length))
  })
}

# Read data
file_path <- file.path(DATA_DIR, datasets_info$treas_yield_curve_zero_coupon)
df <- read_parquet(file_path)

# Define forecasting parameters
test_ratio <- 0.2  # Use last 20% of the data for testing
seasonality <- 5  # 5 for weekly patterns (business days)

# Get unique entities
entities <- unique(df$entity)
mase_values <- numeric(0)

cat(sprintf("Running Simple Exponential Smoothing forecasting for %d entities...\n", length(entities)))

# Process each entity separately
results <- pblapply(entities, function(entity) {
  # Filter data for the current entity
  entity_data <- df %>% 
    filter(entity == !!entity) %>% 
    arrange(date) %>%
    filter(!is.na(value))
  
  if (nrow(entity_data) <= 10) {
    return(NA)  # Skip entities with too few observations
  }
  
  # Extract values
  values <- entity_data$value
  
  # Determine train/test split
  n <- length(values)
  test_size <- max(1, round(n * test_ratio))
  train_size <- n - test_size
  
  train_data <- values[1:train_size]
  test_data <- values[(train_size+1):n]
  
  forecast_horizon <- length(test_data)
  
  # Generate forecasts using Simple Exponential Smoothing
  forecasts <- forecast_ses(train_data, forecast_horizon)
  
  # Calculate MASE for this entity
  entity_mase <- calculate_mase(test_data, forecasts, train_data, seasonality)
  
  return(entity_mase)
})

# Filter out NA values
mase_values <- unlist(results)
mase_values <- mase_values[!is.na(mase_values)]

# Calculate mean and median MASE across all entities
mean_mase <- mean(mase_values)
median_mase <- median(mase_values)

cat("\nSimple Exponential Smoothing Forecasting Results:\n")
cat(sprintf("Number of entities successfully forecasted: %d\n", length(mase_values)))
cat(sprintf("Mean MASE: %.4f\n", mean_mase))
cat(sprintf("Median MASE: %.4f\n", median_mase))

# Save results
results_df <- data.frame(
  model = "Simple Exponential Smoothing",
  seasonality = seasonality,
  mean_mase = mean_mase,
  median_mase = median_mase,
  entity_count = length(mase_values)
)

write.csv(results_df, file.path(OUTPUT_DIR, "raw_results", "simple_exponential_smoothing_results.csv"), row.names = FALSE)
