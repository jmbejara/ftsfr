from abc import ABC, abstractmethod
import logging

foreMod_logger = logging.getLogger("forecasting_model")


class forecasting_model(ABC):
    @abstractmethod
    def train(self):
        """
        Trains the model.
        """
        pass

    @abstractmethod
    def load_model(self):
        """
        Loads saved model.
        """
        pass

    @abstractmethod
    def forecast(self):
        """
        Predicts using the model, adds it to the object. Sliding window
        forecasts.
        """
        pass

    @abstractmethod
    def load_forecast(self):
        """
        Loads saved forecasts.
        """
        pass

    @abstractmethod
    def calculate_error(self):
        """
        Loads predicted values and returns error metric.
        """
        pass

    @abstractmethod
    def print_summary(self):
        """
        Prints class-specific summary table of values.
        """
        pass

    @abstractmethod
    def save_results(self):
        """
        Saves class-specific summary results.
        """
        pass

    def print_sep(self):
        """
        Prints a separator line.
        """
        sep = ""
        for i in range(67):
            sep += "-"
        print(sep)

    def one_step_ahead_forecast(self):
        """
        Unified one-step-ahead forecasting implementation.

        This method ensures consistent evaluation across all model types:
        1. Model is trained once on training data (80%)
        2. For each point in test period, forecasts one step ahead using
           all actual historical data up to that point
        3. No retraining occurs during the test period

        This method should be called by the forecast() method in each model class.
        """
        foreMod_logger.info("Starting unified one-step-ahead forecasting")

        # Check if we have the necessary attributes
        if (
            not hasattr(self, "model")
            or not hasattr(self, "train_data")
            or not hasattr(self, "test_data")
        ):
            raise AttributeError(
                "Model must have 'model', 'train_data', and 'test_data' attributes"
            )

        # Model should already be trained at this point
        if not hasattr(self.model, "is_fitted") or not self.model.is_fitted:
            foreMod_logger.warning(
                "Model appears to not be fitted. Ensure train() was called before forecast()"
            )

        foreMod_logger.info("One-step-ahead forecasting completed")

        # Subclasses should implement the actual forecasting logic
        raise NotImplementedError("Subclasses must implement one_step_ahead_forecast")

    def main_workflow(self):
        """
        Train the model -> Save the model -> Get predictions ->
        Save predictions -> Calculate error -> Print summary -> Save results
        """
        foreMod_logger.info("main_workflow called.")
        self.train()
        self.save_model()
        self.forecast()
        self.save_forecast()
        self.calculate_error()
        self.print_summary()
        self.save_results()

    def training_workflow(self):
        """
        Train the model -> Save the model
        """
        foreMod_logger.info("training_workflow called.")
        self.train()
        self.save_model()

    def inference_workflow(self):
        """
        Load the model -> Get predictions -> Save predictions ->
        Calculate error -> Print summary -> Save results
        """
        foreMod_logger.info("inference_workflow called.")
        self.load_model()
        self.forecast()
        self.save_forecast()
        self.calculate_error()
        self.print_summary()
        self.save_results()
