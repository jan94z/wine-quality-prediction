import pickle
from pathlib import Path

class Model:
    def __init__(self, model_path:str):
        self.model = None
        self.model_path = Path(model_path)

    def load(self):
        if self.model is None:
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)

    def predict(self, data):
        self.load()
        return float(self.model.predict([data])[0])  # Single prediction
