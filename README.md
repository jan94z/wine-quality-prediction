# WORK IN PROGRESS
This is a practice project of mine to cover basic ML deployment workflows including model serving, SQL integration, API design, API security / auth, container-based deployment, MLops basics (Mlflow, CI/CD) and unit/integration tests. Besides the coding part, I am also trying to work as agile as possible in an one-person project without real world users/customers - check out the kanban board [here](https://github.com/users/jan94z/projects/3)


# Wine Quality Prediction
This project provides a machine learning API to predict wine quality based on physicochemical properties[^1]. It uses a classification model to predict the wine's quality score and exposes the prediction functionality through a FastAPI web service. 
The project includes:
* A PostgreSQL database to store wine samples and user login data
* A machine learning model trained on the Wine quality dataset
* Mlflow to track experiments and for model versionin 
* A FastAPI backend to provide prediction and secure data access endpoints
* Docker support to containerize and run the service easily
* CI/CD workflows to automatically run tests when pull requests are made or something is pushed to main
* ...\

## Installation guide
```bash
sudo docker compose up --build -d db db-init
sudo docker compose up --build -d mlflow
sudo docker compose up --build -d training
sudo docker compose up --build -d promotion
sudo docker compose run --rm promotion --alias production


sudo docker compose run --rm training --name yourModel
```



### User
Download this repo and execute ...
```bash
sudo docker compose up --build -d db db-init
sudo docker compose up --build -d mlflow
sudo docker compose up --build -d training
sudo docker compose run --rm training --name yourModel
```


http://localhost:5000/

Then you can open http://localhost:8000/docs in your browser. 

API calls:
* /health: Checks API health
* /samples: Randomly lists 5 samples of the wine quality dataset from the deployed DB
* /models: Prints the DB model registry.
*  /pred: Predicts the wine quality of a given sample as json input. The model path needs to be entered, too.


### Dev
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
```basb
pip install requirements.txt
```
```basb
sudo docker compose -f docker/docker-compose.yml up --build db
```
```bash
python -m docker.init.init_db.py
```
```bash
python -m training.train_model -n "model_name" -v
```
```bash
uvicorn app.main:app --reload
```

```bash
PYTHONPATH=. pytest -v
```

[^1]:P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis. 
Modeling wine preferences by data mining from physicochemical properties.
In Decision Support Systems, Elsevier, 47(4):547-553. ISSN: 0167-9236.\
Available at: http://dx.doi.org/10.1016/j.dss.2009.05.016 \
Data available at: https://archive.ics.uci.edu/dataset/186/wine+quality

