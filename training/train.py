import os
import click
import pandas as pd
import sklearn.metrics as metrics
from pathlib import Path
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import mlflow
from shared.utils import get_engine
from tqdm import tqdm

@click.command()
@click.option('--name', '-n', default = None, help='Model name to save the model')
def main(name: str) -> None:
    # create database engine
    engine = get_engine()

    # load data from database
    data_split = {
        "train": None,
        "test": None,
        "valid": None
    }

    for split in data_split.keys():
        query = f"""
        SELECT w.*
        FROM wine_samples w
        JOIN wine_samples_split s ON w.id = s.id
        WHERE s.split_group = '{split}'
        """

        data_split[split] = pd.read_sql(query, engine)
    
    # define feature and label vectors
    features = ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',
        'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',
        'ph', 'sulphates', 'alcohol']

    
    X_train = data_split['train'][features].to_numpy()
    y_train = data_split['train']['quality'].to_numpy()
    X_val = data_split['valid'][features].to_numpy()
    y_val = data_split['valid']['quality'].to_numpy()
    X_test = data_split['test'][features].to_numpy()
    y_test = data_split['test']['quality'].to_numpy()

    # test various models
    # scale data
    # scaler = StandardScaler()
    # X_train = scaler.fit_transform(X_train)
    # X_val = scaler.transform(X_val)
    # X_test = scaler.transform(X_test)
    # model = MLPClassifier(max_iter=1000, random_state=42, hidden_layer_sizes=(32,64,128), 
    #                     activation='relu', solver='adam', learning_rate='invscaling',
    #                     learning_rate_init=0.001, alpha=0.01)
    # model = SVC(kernel='rbf', random_state=42)
    # model = LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs', 
    #                             multi_class='multinomial', C=1.0, penalty='l2')

    # TODO: if other model than random forest will be used, scaler must be used and exported and integrated into API so that the data is scaled before prediction

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    tqdm(model.fit(X_train, y_train), desc="Training model", total=len(X_train))

    acc_train = metrics.accuracy_score(y_train, model.predict(X_train))
    acc_val = metrics.accuracy_score(y_val, model.predict(X_val))
    acc_test = metrics.accuracy_score(y_test, model.predict(X_test))

    # MLflow Setup
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_URI", "http://localhost:5000"))
    mlflow.set_experiment("wine-quality")

    with mlflow.start_run() as run:
        mlflow.log_param("model_type", "RandomForest")
        mlflow.log_metric("accuracy_train", acc_train)
        mlflow.log_metric("accuracy_val", acc_val)
        mlflow.log_metric("accuracy_test", acc_test)

        signature = mlflow.models.infer_signature(X_train, model.predict(X_train))

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            signature=signature,
            registered_model_name=name if name else "wine-quality-model"
        )

        print(f" Registered Model '{name}'.")


if __name__ == "__main__":
    main()
