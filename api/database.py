from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv
from app.auth import hash_password
from fastapi import HTTPException

load_dotenv()



def get_random_samples(limit=10):
    engine = get_engine()
    df = pd.read_sql(text(
        """
        SELECT *
        FROM wine_samples w
        JOIN wine_samples_split s ON w.id = s.id
        WHERE s.split_group = 'test'
        ORDER BY random()
        LIMIT :limit;
        """
    ), engine, params={"limit": limit})
    df = df.drop(columns=["split_random", "split_group"])
    return df.to_dict(orient="records")

def get_model_registry():
    engine = get_engine()
    df = pd.read_sql(text("SELECT * FROM model_registry"), engine)
    return df.to_dict(orient="records")

def get_user(email):
    engine = get_engine()
    df = pd.read_sql(
        text("SELECT * FROM users WHERE email = :email"),
        engine,
        params={"email": email}
    )
    return df.to_dict(orient="records")[0] if not df.empty else None

def register_user(email, password):
    engine = get_engine()
    hashed_pw = hash_password(password)
    with engine.begin() as conn:  # begin() sorgt für automatisches commit/rollback
        result = conn.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": email}
        )
        if result.fetchone():
            raise HTTPException(status_code=400, detail="User already exists")
        conn.execute(
            text("INSERT INTO users (email, password) VALUES (:email, :password)"),
            {"email": email, "password": hashed_pw}
        )
    print(f"User with email {email} inserted.")

