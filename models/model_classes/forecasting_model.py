from abc import ABC, abstractmethod
import traceback
import logging

fm_logger = logging.getLogger("forecasting_model")


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

    def main_workflow(self):
        """
        Trains the model -> Saves the model -> Get predictions ->
        Saves predictions -> Calculates error -> Prints summary -> Saves results
        """
        fm_logger.info("main_workflow called.")
        self.train()
        self.save_model()
        self.forecast()
        self.save_forecast()
        self.calculate_error()
        self.print_summary()
        self.save_results()

    def training_workflow(self):
        """
        Trains the model -> Saves the model
        """
        fm_logger.info("training_workflow called.")
        self.train()
        self.save_model()

    def inference_workflow(self):
        """
        Loads the model -> Get predictions -> Saves predictions ->
        Calculates error -> Prints summary -> Saves results
        """
        fm_logger.info("inference_workflow called.")
        self.load_model()
        self.forecast()
        self.save_forecast()
        self.calculate_error()
        self.print_summary()
        self.save_results()
