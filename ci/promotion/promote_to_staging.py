from mlflow.tracking import MlflowClient
import os

def main():
    client = MlflowClient(os.environ.get("MLFLOW_URI", "http://localhost:5000"))
    model_name = "wine-quality-model"

    # Find latest version WITHOUT alias "staging" or "production"
    versions = client.search_model_versions(f"name='{model_name}'")
    # Choose the latest registered (no alias), e.g., by highest version number
    latest = max([int(v.version) for v in versions if not v.aliases], default=None)
    if not latest:
        raise Exception("No model version found without alias.")

    client.set_registered_model_alias(
        name=model_name,
        alias="staging",
        version=str(latest)
    )
    print(f"Assigned 'staging' alias to model version {latest}.")

if __name__ == "__main__":
    main()