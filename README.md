# wine-quality-prediction
This project provides a simple machine learning API to predict wine quality based on physicochemical properties. It uses a trained classification model to predict the wine's quality score and exposes the prediction functionality through a FastAPI web service.\
The project includes:
* A SQL database to store wine samples and features
* A machine learning model trained on the Wine Quality dataset
* A FastAPI backend to provide prediction and data access endpoints
* Docker support to containerize and run the service easily
* Deployment configuration for running the service on Azure App Service
The project is in progress and aims to cover basic ML deployment workflows including model serving, SQL integration, API design and container-based deployment.

## Project in progress
For the project management refer to:
https://github.com/users/jan94z/projects/3

## Information DUMP as long as project is in progress
```bash
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
sudo apt-get install -y python3-venv
```

```bash
python3 -m venv ".venv"
source .venv/bin/activate
pip install --upgrade pip
```

```bash
sudo ./docker docker compose up -d
sudo docker cp winequality-red.csv wine-quality-db:/csv_data/winequality-red.csv
sudo docker cp winequality-white.csv wine-quality-db:/csv_data/winequality-white.csv
```
create SQL

```SQL
CREATE TABLE wine_samples (
    id SERIAL PRIMARY KEY,
    fixed_acidity REAL,
    volatile_acidity REAL,
    citric_acid REAL,
    residual_sugar REAL,
    chlorides REAL,
    free_sulfur_dioxide REAL,
    total_sulfur_dioxide REAL,
    density REAL,
    ph REAL,
    sulphates REAL,
    alcohol REAL,
    quality INTEGER,
    wine_type TEXT
);
```

```python
python ./data/data_preparation.py --p csv_directory --e True
```
P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis. 
Modeling wine preferences by data mining from physicochemical properties.
In Decision Support Systems, Elsevier, 47(4):547-553. ISSN: 0167-9236.\
Available at: http://dx.doi.org/10.1016/j.dss.2009.05.016 \
Data available at: https://archive.ics.uci.edu/dataset/186/wine+quality
