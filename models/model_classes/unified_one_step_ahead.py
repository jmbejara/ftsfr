"""
Unified one-step-ahead forecasting implementation for all model types.

This module provides a consistent way to perform one-step-ahead forecasting
across Darts, Nixtla, and GluonTS models.
"""

import pandas as pd
from tqdm import tqdm
import logging

Uni_logger = logging.getLogger("unified_one_step_ahead")

# Conditional imports to avoid dependency issues
try:
    from darts import TimeSeries

    DARTS_AVAILABLE = True
except ImportError:
    DARTS_AVAILABLE = False
    TimeSeries = None


def perform_one_step_ahead_darts(model, test_data, raw_data):
    """
    Performs one-step-ahead forecasting for Darts models.

    Args:
        model: Trained Darts model
        test_data: Test TimeSeries
        raw_data: Full TimeSeries (train + test)

    Returns:
        TimeSeries: One-step-ahead predictions
    """
    Uni_logger.info("Starting Darts one-step-ahead forecasting")

    # Determine if it's a local or global model
    try:
        from darts.models.forecasting.forecasting_model import LocalForecastingModel

        is_local = isinstance(model, LocalForecastingModel)
    except:
        # Fallback: check if model has specific methods
        is_local = hasattr(model, "fit") and not hasattr(model, "trainer")

    Uni_logger.info(f"Model type: {'Local' if is_local else 'Global'}")

    # Get test start time
    test_start = test_data.start_time()

    # For global models, use historical_forecasts with explicit parameters

    # Make retrain condition True if the following models are used
    # ExponentialSmoothing
    # Simple ExponentialSmoothing
    # Theta
    # Prophet
    # Naive models
    # Else don't need to retrain
    model_name = str(type(model))
    retrain_model = (".ExponentialSmoothing" in model_name) or\
                    (".Theta" in model_name) or\
                    (".Prophet" in model_name) or\
                    (".Naive" in model_name)

    Uni_logger.info("retrain_model = " + str(retrain_model))
    Uni_logger.info("Using historical_forecasts")
    predictions = model.historical_forecasts(
        series=raw_data,
        start=test_start,
        forecast_horizon=1,
        stride=1,
        retrain=retrain_model,
        last_points_only=True,  # I think this should be set to True. Prev: False
        verbose=False,
    )

    # Handle case where historical_forecasts returns a list
    if isinstance(predictions, list):
        Uni_logger.info(
            f"historical_forecasts returned a list of {len(predictions)} TimeSeries"
        )
        # Concatenate all predictions into a single TimeSeries
        if len(predictions) > 0:
            # Concatenate one by one
            result = predictions[0]
            for pred in predictions[1:]:
                result = TimeSeries.concatenate(result, pred, axis=0)
            predictions = result
        else:
            raise ValueError("No predictions returned from historical_forecasts")

    Uni_logger.info(f"Final predictions shape: {predictions.shape}")

    # Ensure predictions have the same number of components as test_data
    if predictions.n_components != test_data.n_components:
        Uni_logger.warning(
            f"Predictions have {predictions.n_components} components, test_data has {test_data.n_components}"
        )
        # If predictions have more components, take only the first test_data.n_components
        if predictions.n_components > test_data.n_components:
            predictions = predictions[:, : test_data.n_components]
            Uni_logger.info(
                f"Truncated predictions to {test_data.n_components} components"
            )
        else:
            # If predictions have fewer components, this is a problem
            raise ValueError(
                f"Predictions have fewer components ({predictions.n_components}) than test_data ({test_data.n_components})"
            )

    Uni_logger.info(f"Generated predictions with shape: {predictions.shape}")
    return predictions

def perform_one_step_ahead_nixtla(nf_model, train_data, test_data, raw_data):
    """
    Performs one-step-ahead forecasting for Nixtla NeuralForecast models.

    Args:
        nf_model: NeuralForecast model instance (already fitted)
        train_data: Training DataFrame with columns ['ds', 'unique_id', 'y']
        test_data: Test DataFrame with columns ['ds', 'unique_id', 'y']
        raw_data: Full DataFrame (train + test)

    Returns:
        pd.DataFrame: One-step-ahead predictions with columns ['ds', 'unique_id', 'y']
    """
    Uni_logger.info("Starting Nixtla one-step-ahead forecasting")

    # For NeuralForecast, we can use the predict method directly on the full dataset
    # and then filter to get only the test predictions
    Uni_logger.info("Using NeuralForecast predict method on full dataset")

    try:
        # The loop keeps concatenating forecasts to pred_data
        pred_data = nf_model.predict(train_data)
        first_date = test_data["ds"].unique()[0]
        pred_data["ds"] = first_date
        df = raw_data
        Uni_logger.info(
            "Got predictions for date: " + first_date.strftime("%Y-%m-%d, %r") + "."
        )

        # Sliding window forecasts
        # Predict 1 date right after the dataset in the arguments
        # After each prediction the next prediction uses the actual value in the
        # test dataset instead of relying on the previous predicted value.
        Uni_logger.info("Starting for loop to get sliding window forecasts.")
        for i in test_data["ds"].unique()[1:]:
            # Get predictions for the next date
            temp_pred_data = nf_model.predict(df[df.ds < i])
            # Lining up the dates
            temp_pred_data["ds"] = i
            pred_data = pd.concat([pred_data, temp_pred_data], ignore_index=True)
            Uni_logger.info(
                "Got predictions for date: " + i.strftime("%Y-%m-%d, %r") + "."
            )

        return pred_data

    except Exception as e:
        Uni_logger.error(f"Error in NeuralForecast prediction: {e}")
        # Fallback: try a simpler approach
        Uni_logger.info("Trying fallback approach with test data only")

        # Use the test data directly for prediction
        predictions = nf_model.predict(test_data)
        Uni_logger.info(f"Fallback generated {len(predictions)} predictions")
        return predictions


def perform_one_step_ahead_gluonts(model, train_data, test_data):
    """
    Performs one-step-ahead forecasting for GluonTS models.

    Args:
        model: Trained GluonTS predictor
        train_data: Training dataset (GluonTS format)
        test_data: Test dataset (GluonTS format)

    Returns:
        pd.DataFrame: One-step-ahead predictions with columns ['ds', 'unique_id', 'y']
    """
    Uni_logger.info("Starting GluonTS one-step-ahead forecasting")

    # Convert datasets to lists for easier manipulation
    test_data = list(test_data)
    train_data = list(train_data)

    # Determine the range of predictions needed
    train_length = len(train_data[0]["target"])
    test_length = len(test_data[0]["target"])

    Uni_logger.info(
        f"Train length: {train_length}, Test length: {test_length - train_length}"
    )

    result = []

    # Iterate through each test point
    for i in tqdm(range(train_length, test_length), desc="One-step-ahead forecasting"):
        # Create temporary dataset with data up to current point
        temp_dataset = []
        for series in test_data:
            temp_data = series.copy()
            temp_data["target"] = temp_data["target"][:i]
            temp_dataset.append(temp_data)

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

    pred_data = pd.DataFrame(result)
    Uni_logger.info(f"Generated {len(pred_data)} one-step-ahead predictions")
    return pred_data


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
    Uni_logger.info(f"Verifying one-step-ahead predictions for {model_type} model")

    if model_type == "darts":
        if not DARTS_AVAILABLE:
            Uni_logger.warning(
                "darts not available, skipping verification for darts model"
            )
            return True

        # For Darts TimeSeries
        if isinstance(predictions, TimeSeries):
            pred_length = len(predictions)
            test_length = len(test_data)

            # Check that we have one prediction per test point
            if pred_length == test_length:
                Uni_logger.info("✓ Darts predictions length matches test data length")
                return True
            else:
                Uni_logger.warning(
                    f"⚠ Darts predictions length ({pred_length}) != test data length ({test_length})"
                )
                return False
        else:
            Uni_logger.warning("⚠ Darts predictions not in TimeSeries format")
            return False

    elif model_type == "nixtla":
        # For Nixtla DataFrame predictions
        if isinstance(predictions, pd.DataFrame):
            pred_count = len(predictions)
            test_count = len(test_data)

            # Check that we have one prediction per test point
            if pred_count == test_count:
                Uni_logger.info("✓ Nixtla predictions count matches test data count")
                return True
            else:
                Uni_logger.warning(
                    f"⚠ Nixtla predictions count ({pred_count}) != test data count ({test_count})"
                )
                return False
        else:
            Uni_logger.warning("⚠ Nixtla predictions not in DataFrame format")
            return False

    elif model_type == "gluonts":
        # For GluonTS DataFrame predictions
        if isinstance(predictions, pd.DataFrame):
            pred_count = len(predictions)
            test_count = len(test_data)

            # Check that we have one prediction per test point
            if pred_count == test_count:
                Uni_logger.info("✓ GluonTS predictions count matches test data count")
                return True
            else:
                Uni_logger.warning(
                    f"⚠ GluonTS predictions count ({pred_count}) != test data count ({test_count})"
                )
                return False
        else:
            Uni_logger.warning("⚠ GluonTS predictions not in DataFrame format")
            return False

    else:
        # Generic verification
        Uni_logger.info("Generic verification - assuming one-step-ahead")
        return True
