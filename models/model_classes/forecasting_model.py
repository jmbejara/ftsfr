from abc import ABC, abstractmethod

class forecasting_model(ABC):
    @abstractmethod
    def _train(self):
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
        Predicts using the model, adds it to the object, and saves the 
        predictions.
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