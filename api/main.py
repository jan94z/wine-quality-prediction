from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.model import Model
from app.database import get_random_samples, get_model_registry, get_user, register_user
from app.schemas import WineSample, ModelInput, User, Token
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# middleware and rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
# app.add_middleware(HTTPSRedirectMiddleware)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost"])

# @app.middleware("http")
# async def add_security_headers(request, call_next):
#     response = await call_next(request)
#     response.headers["X-Content-Type-Options"] = "nosniff"
#     response.headers["X-Frame-Options"] = "DENY"
#     response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
#     return response

# API endpoints
# HEALTH CHECK
@app.get("/health")
@limiter.limit("5/minute")
def health(request:Request):
    return {"status": "ok"}

@app.get("/secure")
@limiter.limit("5/minute")
def secure_route(request:Request, current_user: str = Depends(get_current_user)):
    return {"msg": f"Hello, {current_user}"}

# USER
@app.post("/token", response_model=Token)
@limiter.limit("5/minute")
def login(request:Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid password")
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/register")
@limiter.limit("5/minute")
def register(user: User, request:Request):
    register_user(user.email, user.password)
    return {"msg": "User created"}

# ACCESS DB
@app.get("/samples")
@limiter.limit("5/minute")
def samples(request:Request, user: str = Depends(get_current_user)):
    return get_random_samples()

@app.get("/models")
@limiter.limit("5/minute")
def models(request:Request, user : str = Depends(get_current_user)):
    return get_model_registry()  

# PREDICTION
@app.post("/predict")
@limiter.limit("5/minute")
def predict(request:Request, sample: WineSample, model_input: ModelInput, current_user: str = Depends(get_current_user)):
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



