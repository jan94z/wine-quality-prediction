# auth.py
import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)

# pw verification
def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_context = CryptContext(schemes=[os.environ.get("CRYPT_CONTEXT", "bcyrpt")], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

# JWT token creation
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    secret = os.environ.get("JWT_SECRET_KEY")
    algorithm = os.environ.get("JWT_ALGORITHM", "HS256")
    if not secret:
        logger.error("JWT_SECRET_KEY not set in environment")
        raise RuntimeError("JWT_SECRET_KEY not set in environment")
    return jwt.encode(to_encode, secret, algorithm=algorithm)

# get current user from token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
def get_current_user(token: str = Depends(oauth2_scheme)):
    secret = os.environ.get("JWT_SECRET_KEY")
    algorithm = os.environ.get("JWT_ALGORITHM", "HS256")
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            logger.error("Token does not contain a valid username")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        logger.error("JWTError: Invalid token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")



