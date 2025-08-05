"""
Unified one-step-ahead forecasting implementation for all model types.

This module provides a consistent way to perform one-step-ahead forecasting
across Darts, Nixtla, and GluonTS models.
"""

import numpy as np
import pandas as pd
from darts import TimeSeries
from darts.models.forecasting.forecasting_model import LocalForecastingModel, GlobalForecastingModel
from tqdm import tqdm
import logging

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
        is_local = hasattr(model, 'fit') and not hasattr(model, 'trainer')
    
    logger.info(f"Model type: {'Local' if is_local else 'Global'}")
    
    # Get test start time
    test_start = test_series.start_time()
    test_end = test_series.end_time()
    
    # For global models, use historical_forecasts with explicit parameters
    if not is_local:
        logger.info("Using historical_forecasts for global model")
        predictions = model.historical_forecasts(
            series=raw_series,
            start=test_start,
            forecast_horizon=1,
            stride=1,
            retrain=False,  # Model already trained, don't retrain
            last_points_only=False,
            verbose=False
        )
    else:
        # For local models, we need to be more careful
        logger.info("Performing manual one-step-ahead for local model")
        predictions_list = []
        
        # Get the frequency of the series
        freq = train_series.freq
        
        # Iterate through each test point
        test_dates = pd.date_range(start=test_start, end=test_end, freq=freq)
        
        for i, current_date in enumerate(tqdm(test_dates, desc="One-step-ahead forecasting")):
            # Get all data up to current point (excluding current point)
            historical_data = raw_series[:current_date]
            
            # For local models, we need to ensure we don't retrain
            # We'll use the already fitted model
            pred = model.predict(n=1, series=historical_data)
            predictions_list.append(pred)
        
        # Concatenate all predictions
        # Each prediction is a TimeSeries of length 1
        values = np.concatenate([p.values() for p in predictions_list])
        predictions = TimeSeries.from_times_and_values(
            times=test_dates,
            values=values,
            freq=freq
        )
    
    logger.info(f"Generated {len(predictions)} one-step-ahead predictions")
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
    
    # Get unique test dates
    test_dates = sorted(test_df['ds'].unique())
    logger.info(f"Forecasting for {len(test_dates)} test dates")
    
    predictions = []
    
    for i, test_date in enumerate(tqdm(test_dates, desc="One-step-ahead forecasting")):
        # Get all data before this test date
        historical_data = raw_df[raw_df['ds'] < test_date]
        
        # Predict one step ahead
        pred = nf_model.predict(historical_data)
        
        # Align the prediction date
        pred['ds'] = test_date
        predictions.append(pred)
    
    # Concatenate all predictions
    pred_df = pd.concat(predictions, ignore_index=True)
    
    logger.info(f"Generated {len(pred_df)} one-step-ahead predictions")
    return pred_df


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
    
    logger.info(f"Train length: {train_length}, Test length: {test_length - train_length}")
    
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
            if hasattr(pred, 'samples'):
                # SampleForecast format
                result.append({
                    'ds': pred.start_date.to_timestamp() if hasattr(pred.start_date, 'to_timestamp') else pred.start_date,
                    'unique_id': pred.item_id if hasattr(pred, 'item_id') else None,
                    'y': pred.samples.mean().item() if pred.samples.ndim > 1 else pred.samples.item()
                })
            else:
                # Convert to SampleForecast if needed
                sample_pred = pred.to_sample_forecast(1)
                result.append({
                    'ds': sample_pred.start_date.to_timestamp() if hasattr(sample_pred.start_date, 'to_timestamp') else sample_pred.start_date,
                    'unique_id': sample_pred.item_id if hasattr(sample_pred, 'item_id') else None,
                    'y': sample_pred.samples.mean().item() if sample_pred.samples.ndim > 1 else sample_pred.samples.item()
                })
    
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
        # For Darts TimeSeries
        if isinstance(predictions, TimeSeries):
            pred_length = len(predictions)
            test_length = len(test_data)
            
            # Check that we have one prediction per test point
            if pred_length == test_length:
                logger.info(f"✓ Prediction length ({pred_length}) matches test length ({test_length})")
                return True
            else:
                logger.warning(f"✗ Prediction length ({pred_length}) doesn't match test length ({test_length})")
                return False
    
    elif model_type in ["nixtla", "gluonts"]:
        # For DataFrame predictions
        if isinstance(predictions, pd.DataFrame):
            pred_dates = sorted(predictions['ds'].unique())
            test_dates = sorted(test_data['ds'].unique())
            
            # Check that prediction dates match test dates
            if len(pred_dates) == len(test_dates):
                logger.info(f"✓ Number of prediction dates ({len(pred_dates)}) matches test dates ({len(test_dates)})")
                
                # Check if dates actually match
                dates_match = all(pd.to_datetime(p) == pd.to_datetime(t) for p, t in zip(pred_dates, test_dates))
                if dates_match:
                    logger.info("✓ Prediction dates align with test dates")
                    return True
                else:
                    logger.warning("✗ Prediction dates don't align with test dates")
                    return False
            else:
                logger.warning(f"✗ Number of prediction dates ({len(pred_dates)}) doesn't match test dates ({len(test_dates)})")
                return False
    
    logger.warning(f"Unable to verify one-step-ahead for model type: {model_type}")
    return False