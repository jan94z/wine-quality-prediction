import pickle
import numpy as np

def test_model_prediction():
    model_path = "/home/jan/wine-quality-prediction/models/rf.pkl"
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    X_sample = np.array([[7.0, 0.27, 0.36, 20.7, 0.045,
                          45.0, 170.0, 1.001, 3.0, 0.45, 8.8]])
    pred = model.predict(X_sample)
    
    assert isinstance(pred[0], (int, np.integer))
    assert 0 <= pred[0] <= 10

def test_model_performance():
    pass

from mlflow.tracking import MlflowClient
import mlflow.pyfunc
import pandas as pd

client = MlflowClient()
model_name = "wine-quality-model"
# Find the latest with alias "staging"
staging_version = None
for v in client.search_model_versions(f"name='{model_name}'"):
    if "staging" in (v.aliases or []):
        staging_version = v.version
        break

if not staging_version:
    raise Exception("No model in staging.")

model_uri = f"models:/{model_name}@staging"
model = mlflow.pyfunc.load_model(model_uri=model_uri)

# Load test data (replace with your own logic)
X_test = pd.read_csv("test_data.csv")
y_test = X_test.pop("target")
preds = model.predict(X_test)
accuracy = (preds == y_test).mean()
print(f"Accuracy: {accuracy:.4f}")
if accuracy < 0.8:
    raise Exception("Model accuracy below threshold.")
