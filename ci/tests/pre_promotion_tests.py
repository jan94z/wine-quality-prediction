import pickle
import numpy as np
from mlflow.tracking import MlflowClient
import mlflow.pyfunc
import pandas as pd

# TODO CONTINUE
# WE DONT NEED TO TEST THE MODEL HERE, bc we have already the stats in mlflow -> look for stats in mlflow and then test passed
# lf staging is non sense, bc we want to test before putting it into staging

client = MlflowClient()
model_name = "wine-quality-model"

staging_version = None
for v in client.search_model_versions(f"name='{model_name}'"):
    if "staging" in (v.aliases or []):
        staging_version = v.version
        break
if not staging_version:
    raise Exception("No model in staging.")

model_uri = f"models:/{model_name}@staging"
model = mlflow.pyfunc.load_model(model_uri=model_uri)






