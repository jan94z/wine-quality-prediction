from sqlalchemy import text
import pandas as pd
from shared.utils import get_engine, hash_password, query
from fastapi import HTTPException
import logging

engine = get_engine() # TODO: MIGRATE TO A STARTUP FUNCTION IN THE API MAIN.PY
logger = logging.getLogger(__name__)

def get_random_samples(limit: int = 10):
    try:
        df = pd.read_sql(
            text("""
                SELECT *
                FROM wine_samples w
                JOIN wine_samples_split s ON w.id = s.id
                WHERE s.split_group = 'test'
                ORDER BY random()
                LIMIT :limit;
            """),
            engine,
            params={"limit": limit}
        )
        df = df.drop(columns=["split_random", "split_group"])
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error getting random samples: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch samples.")

def get_user(email: str):
    try:
        df = pd.read_sql(
            text("SELECT * FROM users WHERE email = :email"),
            engine,
            params={"email": email}
        )
        return df.to_dict(orient="records")[0] if not df.empty else None
    except Exception as e:
        logger.error(f"Error fetching user {email}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch user.")

def register_user(email: str, password: str):
    hashed_pw = hash_password(password)
    try:
        # Check if user exists
        df = pd.read_sql(
            text("SELECT * FROM users WHERE email = :email"),
            engine,
            params={"email": email}
        )
        if not df.empty:
            raise HTTPException(status_code=400, detail="User already exists")
        # Register user
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO users (email, password) VALUES (:email, :password)"),
                {"email": email, "password": hashed_pw}
            )
            conn.commit()

        logger.info(f"User with email {email} inserted.")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user {email}: {e}")
        raise HTTPException(status_code=500, detail="User registration failed.")


