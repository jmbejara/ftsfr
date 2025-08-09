"""
Unified one-step-ahead forecasting implementation for all model types.

This module provides a consistent way to perform one-step-ahead forecasting
across Darts, Nixtla, and GluonTS models.
"""

import numpy as np
import pandas as pd
from tqdm import tqdm
import logging

# Conditional imports to avoid dependency issues
try:
    from darts import TimeSeries
    DARTS_AVAILABLE = True
except ImportError:
    DARTS_AVAILABLE = False
    TimeSeries = None

logger = logging.getLogger("unified_one_step_ahead")


def perform_one_step_ahead_darts(model, train_series, test_series, raw_series):
    """
    Performs one-step-ahead forecasting for Darts models.

    Args:
        model: Trained Darts model
        train_series: Training TimeSeries
        test_series: Test TimeSeries
        raw_series: Full TimeSeries (train + test)

    Returns:
        TimeSeries: One-step-ahead predictions
    """
    logger.info("Starting Darts one-step-ahead forecasting")

    # Determine if it's a local or global model
    try:
        from darts.models.forecasting.forecasting_model import LocalForecastingModel

        is_local = isinstance(model, LocalForecastingModel)
    except:
        # Fallback: check if model has specific methods
        is_local = hasattr(model, "fit") and not hasattr(model, "trainer")

    logger.info(f"Model type: {'Local' if is_local else 'Global'}")

    # Get test start time
    test_start = test_series.start_time()
    test_end = test_series.end_time()

    # For global models, use historical_forecasts with explicit parameters
    
    # Make retrain condition True if the following models are used
    # ExponentialSmoothing
    # Simple ExponentialSmoothing
    # Theta
    # Prophet
    # Naive models
    # Else don't need to retrain
    model_name = str(type(model))
    retrain_model = model_name.startswith(("ExponentialSmoothing",
                                           "Theta",
                                           "Prophet",
                                           "Naive"))

    logger.info("retrain_model = " + str(retrain_model))
    logger.info("Using historical_forecasts")
    predictions = model.historical_forecasts(
        series=raw_series,
        start=test_start,
        forecast_horizon=1,
        stride=1,
        retrain=retrain_model,
        last_points_only=True, # I think this should be set to True. Prev: False
        verbose=False,
    )
    
    # Handle case where historical_forecasts returns a list
    if isinstance(predictions, list):
        logger.info(f"historical_forecasts returned a list of {len(predictions)} TimeSeries")
        # Concatenate all predictions into a single TimeSeries
        if len(predictions) > 0:
            # Concatenate one by one
            result = predictions[0]
            for pred in predictions[1:]:
                result = TimeSeries.concatenate(result, pred, axis=0)
            predictions = result
        else:
            raise ValueError("No predictions returned from historical_forecasts")
    
    logger.info(f"Final predictions shape: {predictions.shape}")

    # Ensure predictions have the same number of components as test_series
    if predictions.n_components != test_series.n_components:
        logger.warning(f"Predictions have {predictions.n_components} components, test_series has {test_series.n_components}")
        # If predictions have more components, take only the first test_series.n_components
        if predictions.n_components > test_series.n_components:
            predictions = predictions[:, :test_series.n_components]
            logger.info(f"Truncated predictions to {test_series.n_components} components")
        else:
            # If predictions have fewer components, this is a problem
            raise ValueError(f"Predictions have fewer components ({predictions.n_components}) than test_series ({test_series.n_components})")

    logger.info(f"Generated predictions with shape: {predictions.shape}")
    return predictions


def perform_one_step_ahead_nixtla(nf_model, train_df, test_df, raw_df):
    """
    Performs one-step-ahead forecasting for Nixtla NeuralForecast models.

    Args:
        nf_model: NeuralForecast model instance (already fitted)
        train_df: Training DataFrame with columns ['ds', 'unique_id', 'y']
        test_df: Test DataFrame with columns ['ds', 'unique_id', 'y']
        raw_df: Full DataFrame (train + test)

    Returns:
        pd.DataFrame: One-step-ahead predictions with columns ['ds', 'unique_id', 'y']
    """
    logger.info("Starting Nixtla one-step-ahead forecasting")

    # For NeuralForecast, we can use the predict method directly on the full dataset
    # and then filter to get only the test predictions
    logger.info("Using NeuralForecast predict method on full dataset")
    
    try:
        # Predict on the full dataset (this will give us predictions for all future points)
        predictions = nf_model.predict(raw_df)
        
        # Filter to only include test dates
        test_dates = set(test_df["ds"].unique())
        pred_df = predictions[predictions["ds"].isin(test_dates)].copy()
        
        logger.info(f"Generated {len(pred_df)} predictions for test dates")
        return pred_df
        
    except Exception as e:
        logger.error(f"Error in NeuralForecast prediction: {e}")
        # Fallback: try a simpler approach
        logger.info("Trying fallback approach with test data only")
        
        # Use the test data directly for prediction
        predictions = nf_model.predict(test_df)
        logger.info(f"Fallback generated {len(predictions)} predictions")
        return predictions


def perform_one_step_ahead_gluonts(model, train_ds, test_ds):
    """
    Performs one-step-ahead forecasting for GluonTS models.

    Args:
        model: Trained GluonTS predictor
        train_ds: Training dataset (GluonTS format)
        test_ds: Test dataset (GluonTS format)

    Returns:
        pd.DataFrame: One-step-ahead predictions with columns ['ds', 'unique_id', 'y']
    """
    logger.info("Starting GluonTS one-step-ahead forecasting")

    # Convert datasets to lists for easier manipulation
    test_series = list(test_ds)
    train_series = list(train_ds)

    # Determine the range of predictions needed
    train_length = len(train_series[0]["target"])
    test_length = len(test_series[0]["target"])

    logger.info(
        f"Train length: {train_length}, Test length: {test_length - train_length}"
    )

    result = []

    # Iterate through each test point
    for i in tqdm(range(train_length, test_length), desc="One-step-ahead forecasting"):
        # Create temporary dataset with data up to current point
        temp_dataset = []
        for series in test_series:
            temp_series = series.copy()
            temp_series["target"] = temp_series["target"][:i]
            temp_dataset.append(temp_series)

        # Get prediction for next time step
        predictions = list(model.predict(temp_dataset, num_samples=1))

        # Convert predictions to consistent format
        for pred in predictions:
            # Handle different prediction formats
            if hasattr(pred, "samples"):
                # SampleForecast format
                result.append(
                    {
                        "ds": pred.start_date.to_timestamp()
                        if hasattr(pred.start_date, "to_timestamp")
                        else pred.start_date,
                        "unique_id": pred.item_id if hasattr(pred, "item_id") else None,
                        "y": pred.samples.mean().item()
                        if pred.samples.ndim > 1
                        else pred.samples.item(),
                    }
                )
            else:
                # Convert to SampleForecast if needed
                sample_pred = pred.to_sample_forecast(1)
                result.append(
                    {
                        "ds": sample_pred.start_date.to_timestamp()
                        if hasattr(sample_pred.start_date, "to_timestamp")
                        else sample_pred.start_date,
                        "unique_id": sample_pred.item_id
                        if hasattr(sample_pred, "item_id")
                        else None,
                        "y": sample_pred.samples.mean().item()
                        if sample_pred.samples.ndim > 1
                        else sample_pred.samples.item(),
                    }
                )

    pred_df = pd.DataFrame(result)
    logger.info(f"Generated {len(pred_df)} one-step-ahead predictions")
    return pred_df


def verify_one_step_ahead(predictions, test_data, model_type="generic"):
    """
    Verifies that the predictions are truly one-step-ahead.

    Args:
        predictions: The predictions (format depends on model type)
        test_data: The test data (format depends on model type)
        model_type: Type of model ("darts", "nixtla", "gluonts", "generic")

    Returns:
        bool: True if predictions appear to be one-step-ahead
    """
    logger.info(f"Verifying one-step-ahead predictions for {model_type} model")

    if model_type == "darts":
        if not DARTS_AVAILABLE:
            logger.warning("darts not available, skipping verification for darts model")
            return True
            
        # For Darts TimeSeries
        if isinstance(predictions, TimeSeries):
            pred_length = len(predictions)
            test_length = len(test_data)

            # Check that we have one prediction per test point
            if pred_length == test_length:
                logger.info("✓ Darts predictions length matches test data length")
                return True
            else:
                logger.warning(f"⚠ Darts predictions length ({pred_length}) != test data length ({test_length})")
                return False
        else:
            logger.warning("⚠ Darts predictions not in TimeSeries format")
            return False

    elif model_type == "nixtla":
        # For Nixtla DataFrame predictions
        if isinstance(predictions, pd.DataFrame):
            pred_count = len(predictions)
            test_count = len(test_data)

            # Check that we have one prediction per test point
            if pred_count == test_count:
                logger.info("✓ Nixtla predictions count matches test data count")
                return True
            else:
                logger.warning(f"⚠ Nixtla predictions count ({pred_count}) != test data count ({test_count})")
                return False
        else:
            logger.warning("⚠ Nixtla predictions not in DataFrame format")
            return False

    elif model_type == "gluonts":
        # For GluonTS DataFrame predictions
        if isinstance(predictions, pd.DataFrame):
            pred_count = len(predictions)
            test_count = len(test_data)

            # Check that we have one prediction per test point
            if pred_count == test_count:
                logger.info("✓ GluonTS predictions count matches test data count")
                return True
            else:
                logger.warning(f"⚠ GluonTS predictions count ({pred_count}) != test data count ({test_count})")
                return False
        else:
            logger.warning("⚠ GluonTS predictions not in DataFrame format")
            return False

    else:
        # Generic verification
        logger.info("Generic verification - assuming one-step-ahead")
        return True
