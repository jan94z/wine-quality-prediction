import os
import click
from mlflow.tracking import MlflowClient

@click.command()
@click.option("--alias", "--a", default="staging", help="Alias to assign to the model version.")
@click.option("--version", "-v", default=None, help="Model version to promote. If not provided, the latest version will be used.")
def main(alias, version):
    client = MlflowClient(os.environ.get("MLFLOW_URI", "http://localhost:5000"))
    model_name = "wine-quality-model"

    if version == "":
        versions = client.search_model_versions(f"name='{model_name}'")
        latest = max([int(v.version) for v in versions if not v.aliases], default=None)
        version = str(latest) if latest is not None else None
    if not version:
        raise Exception("No model version specified or found without alias.")

    client.set_registered_model_alias(
        name=model_name,
        alias=str(alias),
        version=version
    )
    print(f"Model version {version} promoted to 'production'.")
