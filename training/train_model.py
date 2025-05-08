import os
import click
import yaml
import pickle
import pandas as pd
import sklearn.metrics as metrics
import utils.utils as utils
from sqlalchemy import create_engine
from sqlalchemy import text
from pathlib import Path
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from datetime import datetime


@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--name', '-n', default = None, help='Model name to save the model')
def main(verbose: bool, name: str) -> None:
    # get database URL from docker-compose
    script_dir = Path(__file__).resolve().parent
    docker_compose_path = script_dir.parent / "docker" / "docker-compose.yml"
    with open(docker_compose_path, 'r') as file:
        docker_compose = yaml.safe_load(file)
    DATABASE_URL = utils.parse_docker_compose(docker_compose)

    # create database engine
    engine = create_engine(DATABASE_URL)

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

    # random forest worked best so far and worked better without scaling
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # fit model
    model.fit(X_train, y_train)
    # predict
    # traing
    y_pred_train = model.predict(X_train)
    confusion_matrix_train = metrics.confusion_matrix(y_train, y_pred_train)
    accuracy_train = metrics.accuracy_score(y_train, y_pred_train)
    # val
    y_pred = model.predict(X_val)
    confusion_matrix_val = metrics.confusion_matrix(y_val, y_pred)
    accuracy_val = metrics.accuracy_score(y_val, y_pred)
    # test
    y_pred = model.predict(X_test)
    confusion_matrix_test = metrics.confusion_matrix(y_test, y_pred)
    accuracy_test = metrics.accuracy_score(y_test, y_pred)

    if verbose:
        print(f"Model: {model.__class__.__name__}")
        # performance on training set
        print(f"Training Accuracy: {accuracy_train:.4f}")
        print("Confusion Matrix (Train):")
        print(confusion_matrix_train)
        # performance on validation set
        print(f"Validation Accuracy: {accuracy_val:.4f}")
        print("Confusion Matrix (Validation):")
        print(confusion_matrix_val)
        # performance on test set
        print(f"Test Accuracy: {accuracy_test:.4f}")
        print("Confusion Matrix (Test):")
        print(confusion_matrix_test)
    
    # save model
    if name:
        complete_path = f"training/models"
        complete_path = Path(complete_path)
        os.makedirs(complete_path, exist_ok=True)
        model_path = complete_path / f"{name}.pkl"
        with open(model_path, 'wb') as file:
            pickle.dump(model, file)
        print(f"Model saved to {model_path}")

        # Connect to DB
        with engine.begin() as conn:
            insert_query = text("""
            INSERT INTO model_registry (model_name, version, type, path, accuracy_train, accuracy_val, accuracy_test)
            VALUES (:model_name, :version, :type, :path, :accuracy_train, :accuracy_val, :accuracy_test);
            """)

            conn.execute(insert_query, {
                "model_name": name,
                "version": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "type": model.__class__.__name__,
                "path": f"model/{name}.pkl",
                "accuracy_train": accuracy_train,
                "accuracy_val": accuracy_val,
                "accuracy_test": accuracy_test
            })


            print("Model registered in SQL.")
    else:
        print("Model not saved. Use --name to save the model.")

if __name__ == "__main__":
    main()