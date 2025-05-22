import os
import click
import yaml
import pickle
import pandas as pd
import sklearn.metrics as metrics
from sqlalchemy import create_engine
from sqlalchemy import text
from pathlib import Path
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from datetime import datetime
import mlflow
from dotenv import load_dotenv

def get_engine():
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_name = os.getenv("POSTGRES_DB")

    url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    print(url)
    return create_engine(url)

@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--name', '-n', default = None, help='Model name to save the model')
def main(verbose: bool, name: str) -> None:
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


    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("wine-quality")
    n_estimators = 100
    random_state = 42
    with mlflow.start_run():
        # random forest worked best so far and worked better without scaling
        model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)

        # fit model
        model.fit(X_train, y_train)
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("random_state", random_state)
        # predict
        # trainig
        y_pred_train = model.predict(X_train)
        confusion_matrix_train = metrics.confusion_matrix(y_train, y_pred_train)
        accuracy_train = metrics.accuracy_score(y_train, y_pred_train)
        mlflow.log_metric("train_acc", accuracy_train)
        # val
        y_pred = model.predict(X_val)
        confusion_matrix_val = metrics.confusion_matrix(y_val, y_pred)
        accuracy_val = metrics.accuracy_score(y_val, y_pred)
        mlflow.log_metric("val_acc", accuracy_val)
        # test
        y_pred = model.predict(X_test)
        confusion_matrix_test = metrics.confusion_matrix(y_test, y_pred)
        accuracy_test = metrics.accuracy_score(y_test, y_pred)
        mlflow.log_metric("test_acc", accuracy_test)

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
            fp = Path("models")
            os.makedirs(fp, exist_ok=True)
            model_path = fp / f"{name}.pkl"
            with open(model_path, 'wb') as file:
                pickle.dump(model, file)
            print(f"Model saved to {model_path}")

            mlflow.log_artifact(model_path)

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
                    "path": str(model_path),
                    "accuracy_train": accuracy_train,
                    "accuracy_val": accuracy_val,
                    "accuracy_test": accuracy_test
                })


                print("Model registered in SQL.")
        else:
            print("Model not saved. Use --name to save the model.")

if __name__ == "__main__":
    main()