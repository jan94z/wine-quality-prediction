from fastapi import FastAPI
from app.model import Model
from app.database import get_random_samples, get_model_registry
from app.schemas import WineSample, ModelInput

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/token")
def token():
    pass

@app.get("/samples")
def samples():
    return get_random_samples()

@app.get("/models")
def models():
    return get_model_registry()

@app.post("/predict")
def predict(sample: WineSample, model_input: ModelInput):
    model = Model(model_path=model_input.model_path)
    sample_data = [
        sample.fixed_acidity,
        sample.volatile_acidity,
        sample.citric_acid,
        sample.residual_sugar,
        sample.chlorides,
        sample.free_sulfur_dioxide,
        sample.total_sulfur_dioxide,
        sample.density,
        sample.ph,
        sample.sulphates,
        sample.alcohol
    ]
    prediction = model.predict(sample_data)
    return {"quality_prediction": prediction}
