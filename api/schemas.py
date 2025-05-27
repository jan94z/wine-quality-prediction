from pydantic import BaseModel, EmailStr

class WineSample(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    ph: float
    sulphates: float
    alcohol: float

class ModelInput(BaseModel):
    model_name: str
    model_stage: str = "Production"  # Optional: can switch between Staging/Production
class User(BaseModel):
    email: EmailStr
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str

class PredictionResponse(BaseModel):
    quality_prediction: int

