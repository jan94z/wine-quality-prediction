from sqlalchemy import create_engine
import pandas as pd
import os

def get_engine():
    db_user = os.getenv("POSTGRES_USER", "wine123")
    db_pass = os.getenv("POSTGRES_PASSWORD", "wine123")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5433")
    db_name = os.getenv("POSTGRES_DB", "wine-quality-db")

    url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    print(url)
    return create_engine(url)

def get_random_samples(limit=10):
    engine = get_engine()
    query = f"SELECT * FROM wine_samples w JOIN wine_samples_split s ON w.id = s.id WHERE s.split_group = 'test' ORDER BY random() LIMIT {limit}"
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

def get_model_registry():
    engine = get_engine()
    query = "SELECT * FROM model_registry"
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

if __name__ == "__main__":
    get_random_samples()