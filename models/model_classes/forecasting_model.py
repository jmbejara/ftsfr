from abc import ABC, abstractmethod
import traceback

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

    def main_workflow(self):
        try:
            self.train()
            self.save_model()
            self.forecast()
            self.save_forecast()
            self.calculate_error()
            self.print_summary()
            self.save_results()
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in main workflow. " +
                  "Full traceback above \u2191")
            self.print_sep()
            return None
    
    def large_training_workflow(self):
        try:
            self.train()
            self.save_model()
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in heavy training workflow. " +
                  "Full traceback above \u2191")
            self.print_sep()
            return None
    
    def inference_workflow(self):
        try:
            self.load_model()
            self.forecast()
            self.save_forecast()
            self.calculate_error()
            self.print_summary()
            self.save_results()
        except Exception:
            self.print_sep()
            print(traceback.format_exc())
            print(f"\nError in inference workflow. " +
                  "Full traceback above \u2191")
            self.print_sep()
            return None
    
    def print_sep(self):
        sep = ""
        for i in range(67):
            sep += "-"
        print(sep)