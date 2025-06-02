# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from api.model import Model
from api.database import get_random_samples, get_user, register_user
from api.schemas import WineSample, User, Token, PredictionResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from api.auth import verify_password, create_access_token, get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
model = Model(model_name="wine-quality-model")
model.load()  # preload the model

# Middleware and rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# -- Health check --
@app.get("/health")
@limiter.limit("5/minute")
def health(request: Request):
    return {"status": "ok"}

# -- Auth endpoints --
@app.post("/token", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/register")
@limiter.limit("5/minute")
def register(user: User, request: Request):
    register_user(user.email, user.password)
    return {"msg": "User created"}

# -- DB data access (secured) --
@app.get("/samples")
@limiter.limit("5/minute")
def samples(request: Request, user: str = Depends(get_current_user)):
    return get_random_samples()

# -- ML Prediction (secured) --
@app.post("/predict", response_model=PredictionResponse)
@limiter.limit("5/minute")
def predict(
    request: Request,
    sample: WineSample,
    current_user: str = Depends(get_current_user)
):
    sample_data = sample.dict()
    try:
        prediction = model.predict(sample_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {str(e)}")
    return PredictionResponse(quality_prediction=prediction)



