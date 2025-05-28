from mlflow.tracking import MlflowClient
import os

client = MlflowClient(os.environ.get("MLFLOW_URI", "http://localhost:5000"))
model_name = "wine-quality-model"

version = input("Which model version to promote to production? (e.g., 3) or leave empty for latest version: ").strip()
if version == "":
    versions = client.search_model_versions(f"name='{model_name}'")
    latest = max([int(v.version) for v in versions if not v.aliases], default=None)

client.set_registered_model_alias(
    name=model_name,
    alias="production",
    version=version
)
print(f"Model version {version} promoted to 'production'.")
