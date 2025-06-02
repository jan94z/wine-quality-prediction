# Wine Quality Prediction - ML Deployment Practice Project
Status: *Work in Progress* 

This project is a hands-on exercise in end-to-end machine learning deployment, focusing on real-world MLOps patterns:
* Model serving (FastAPI)
* SQL integration (PostgreSQL)
* API design & security (JWT)
* Containerization (Docker)
* Experiment tracking & model registry (MLflow)
* CI/CD & Testing (GitHub Actions, unit/integration tests)
* Agile development (solo Kanban: [Project Board](https://github.com/users/jan94z/projects/3))

## Project Overview
This repository provides an end-to-end solution for predicting wine quality based on physicochemical properties[^1], built for practical MLOps learning and demonstration:
* Database: PostgreSQL for data and user management
* Model Training: Classification model trained on the Wine Quality dataset
* Experiment Tracking & Model Management: MLflow for logging runs and managing production models
* API: FastAPI web service for secure model inference and data access
* Security: JWT-based authentication and protected endpoints
* Deployment: Docker Compose for local orchestration; ready for Kubernetes/cloud migration
* CI/CD: Automated builds, tests, and Docker image pushes via GitHub Actions

## Quick Start
### Requirements
* [Docker](https://docs.docker.com/get-docker/)
* Basic familiarity with command line

### Running the Full Stack with Docker Compose
This will start all core services, train a default Random Forest model, and promote it to the "Production" stage so the API can use it automatically for predictions. If you want to train a different model or change hyperparameters, update ```train.py``` before running the training step. Model promotion is handled locally for now—see Step 4 for how to promote a new model version to "Production." You can retrain and promote as often as you like to experiment with different models.
```bash
# Step 1: Start database and initialize data
docker compose -f docker-compose.yml up --build -d db
docker compose -f docker-compose.yml build db-init

# Step 2: Start MLflow tracking server
sudo docker compose up --build -d mlflow

# Step 3: Train and register a model
docker compose -f docker-compose.yml build training
docker compose -f docker-compose.yml run --rm training

# Step 4: (Optional) Promote a model to "production"
docker compose -f docker-compose.yml build promotion
docker compose -f docker-compose.yml run --rm promotion --alias Production

# Step 5: Start the API
docker compose -f docker-compose.yml up --build -d api
```
* API docs: http://localhost:8000/docs
* MLflow UI: http://localhost:5000/

### API Endpoints
All endpoints (except /health and /token) require a valid authentication token. Use the /token endpoint to obtain a JWT after registering or logging in.
* ```GET /health``` Simple health check; returns API status.
* ```POST /token```Obtain an access token (JWT) by providing a valid username and password. Request body: username, password (form data).
* ```POST /register``` Register a new user with email and password. Request body: JSON with email and password.
* ```GET /samples``` Return a random sample of wine dataset rows from the database. Requires authentication.
* ```POST /predict```
Predict wine quality for the provided sample (input as JSON with all features). Uses the current production model loaded from MLflow. Requires authentication. Request body: wine sample features (JSON).

## Project Status & Next Steps
* ✔️ Local development & Docker Compose orchestration complete
* ✔️ Model registry and promotion via MLflow
* ✔️ API with authentication and CI/CD
* 🚧 Local Kubernetes and Azure cloud deployment in progress (see azure-deploy branch soon)

[^1]:P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis. 
Modeling wine preferences by data mining from physicochemical properties.
In Decision Support Systems, Elsevier, 47(4):547-553. ISSN: 0167-9236.\
Available at: http://dx.doi.org/10.1016/j.dss.2009.05.016 \
Data available at: https://archive.ics.uci.edu/dataset/186/wine+quality

