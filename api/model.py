import mlflow
import os
import pandas as pd

class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None

    def load(self):
        if self.model is None:
            tracking_uri = os.environ.get("MLFLOW_URI", "http://mlflow:5000")
            mlflow.set_tracking_uri(tracking_uri)
            model_uri = f"models:/{self.model_name}@production"
            self.model = mlflow.pyfunc.load_model(model_uri)

    def predict(self, data):
        self.load()
        # Convert the input accordingly
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame([data])
        # Prediction output as int
        result = self.model.predict(data)
        return int(result[0])
