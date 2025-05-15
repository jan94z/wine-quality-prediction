from fastapi import FastAPI
from app.model import Model
from app.database import get_random_samples, get_model_registry
from app.schemas import WineSample, ModelInput
from slowapi import Limiter
from slowapi.util import get_remote_address
#from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
#from starlette.middleware.trustedhost import TrustedHostMiddleware


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
#app.add_middleware(HTTPSRedirectMiddleware)
#app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost"])

# @app.middleware("http")
# async def add_security_headers(request, call_next):
#     response = await call_next(request)
#     response.headers["X-Content-Type-Options"] = "nosniff"
#     response.headers["X-Frame-Options"] = "DENY"
#     response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    # return response

# API endpoints
# HEALTH CHECK
@app.get("/health")
@limiter.limit("5/minute")
def health():
    return {"status": "ok"}

@app.get("/secure")
@limiter.limit("5/minute")
def secure_route():
    return {"msg": "sicher"}

# USER
@app.get("/login")
@limiter.limit("5/minute")
def login(email: str, passwod: str):
    pass

@app.get("/register")
@limiter.limit("5/minute")
def register(email: str, password: str):
    pass

# ACCESS DB
@app.get("/samples")
@limiter.limit("5/minute")
def samples():
    return get_random_samples()

@app.get("/models")
@limiter.limit("5/minute")
def models():
    return get_model_registry()  

# PREDICTION
@app.post("/predict")
@limiter.limit("5/minute")
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



