# auth.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os

# register user and hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT token creation
def create_access_token(data: dict, expires_delta: timedelta = None):
    load_dotenv()
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM"))

# get current user from token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_current_user(token: str = Depends(oauth2_scheme)):
    load_dotenv()
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    return response




