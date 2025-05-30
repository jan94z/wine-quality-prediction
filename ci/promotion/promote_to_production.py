from mlflow.tracking import MlflowClient
import os
import click
# TODO

@click.command()
@click.option("--version", "-v", default=None, help="Model version to promote. If not provided, the latest version will be used.")
def main(version):
    client = MlflowClient(os.environ.get("MLFLOW_URI", "http://localhost:5000"))
    model_name = "wine-quality-model"   

    if version:
        model = client.get_model_version(model_name, version)
        if not model:
            raise Exception(f"Model version {version} not found for model {model_name}.")
    else:
        # get latest version
        model = client.get_registered_model(model_name).latest_versions[0]

    # Check if the model is in staging
    client
    
    if alias in ["Archived", "Staging", "Production"]:
        client.set_registered_model_alias(model_name, str(alias), model.version)
    else:
        raise ValueError("Alias must be either 'Staging', 'Production', or 'Archived'.")
        
    print(f"Model version {version} promoted to {alias}.")


if __name__ == "__main__":
    main()
