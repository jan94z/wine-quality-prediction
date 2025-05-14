from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

def get_engine():
    load_dotenv()
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_name = os.getenv("POSTGRES_DB")

    url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    print(url)
    return create_engine(url)

def get_random_samples(limit=10):
    engine = get_engine()
    query = f"""
    SELECT *
    FROM wine_samples w 
    JOIN wine_samples_split s ON w.id = s.id 
        WHERE s.split_group = 'test' 
    ORDER BY random() 
    LIMIT {limit};
    """
    df = pd.read_sql(query, engine)
    df = df.drop(columns=["split_random", "split_group"])
    return df.to_dict(orient="records")

def get_model_registry():
    engine = get_engine()
    query = "SELECT * FROM model_registry"
    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")

def register_user(email, password):
    engine = get_engine()
    # print if email already exists
    check_query = f"SELECT * FROM users WHERE email = '{email}'"
    insert_query = f"""
    INSERT INTO users (email, password) 
    VALUES ('{email}', '{password}'
    ON CONFLICT (email)
    DO NOTHING;
    """
    with engine.connect() as conn:
        result = conn.execute(check_query)
        if result.fetchone():
            print(f"User with email {email} already exists.")
            return
        else:
            print(f"User with email {email} does not exist. Inserting new user.")
            conn.execute(insert_query)
            print(f"User with email {email} inserted.")