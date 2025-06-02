import mlflow
import os
import pandas as pd

class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None

    def load(self):
        # TESTING: Skip model loading if SKIP_MODEL_LOAD is set
        if os.getenv("SKIP_MODEL_LOAD") == "1":
            print("Skipping model loading for test")
            return
        else:
            if self.model is None:
                tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow:5000")
                mlflow.set_tracking_uri(tracking_uri)
                model_uri = f"models:/{self.model_name}@Production"
                print(f"Loading model from {model_uri}")
                self.model = mlflow.pyfunc.load_model(model_uri)

    def predict(self, data):
        # TESTING: Skip model prediction if SKIP_MODEL_LOAD is set
        if os.getenv("SKIP_MODEL_LOAD") == "1":
            print("Skipping model prediction for test")
            return 5
        # Convert the input accordingly
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame([data])
        # Prediction output as int
        result = self.model.predict(data)
        return int(result[0])
