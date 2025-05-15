import os
import time
import pandas as pd 
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

def data_exploration(df:pd.DataFrame, title:str) -> None:
    """
    Function to explore the dataset.
    Args:
        df (pd.DataFrame): The DataFrame to explore.
        title (str): Title for the exploration output.
    """ 
    print("-----------------------------------")
    print(f'{title} - Head:\n', df.head())
    print("-----------------------------------")
    print('Columns:', len(df.columns))
    print('Rows:', len(df))
    print("-----------------------------------")
    print('Summary:\n', df.describe().round(2))
    print("-----------------------------------")
    print("Missing Values:\n", df.isnull().sum())
    print("-----------------------------------")

def get_engine():
    db_user = os.getenv("POSTGRES_USER", "wine123")
    db_pass = os.getenv("POSTGRES_PASSWORD", "wine123")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5433")
    db_name = os.getenv("POSTGRES_DB", "wine-quality-db")

    url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    print(url)
    return create_engine(url)

def wait_for_db(engine):
    for _ in range(10):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("DB is ready.")
                return
        except OperationalError:
            print("Waiting for DB...")
            time.sleep(5)
    raise Exception("DB not ready after retries.")

def main() -> None:
    engine = get_engine()

    wait_for_db(engine)

    # create the wine_samples table if it doesn't exist
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS wine_samples (
                id SERIAL PRIMARY KEY,
                fixed_acidity REAL,
                volatile_acidity REAL,
                citric_acid REAL,
                residual_sugar REAL,
                chlorides REAL,
                free_sulfur_dioxide REAL,
                total_sulfur_dioxide REAL,
                density REAL,
                ph REAL,
                sulphates REAL,
                alcohol REAL,
                quality INTEGER,
                wine_type TEXT
            )
        """))
    print("wine_samples table ensured.")

    # Prepare paths
    white_path = Path('./winequality-white.csv')
    red_path = Path('./winequality-red.csv')

    # Load datasets
    white = pd.read_csv(white_path, sep=';')
    red = pd.read_csv(red_path, sep=';')

    # Add wine type column
    white["wine_type"] = "white"
    red["wine_type"] = "red"

    # Combine datasets into one
    combined_df = pd.concat([white, red], ignore_index=True)

    # Explore data
    data_exploration(red, "Red Wine Quality Dataset")
    data_exploration(white, "White Wine Quality Dataset")
    data_exploration(combined_df, "Combined Dataset")

    # Insert combined data into DB
    combined_df.columns = [col.strip().replace(" ", "_").lower() for col in combined_df.columns]

    combined_df.to_sql('wine_samples', engine, if_exists="append", index=False)
    print(f"Finished import")

    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS wine_samples_split"))
        conn.execute(text("""
            CREATE TABLE wine_samples_split AS
            SELECT id, random() AS split_random
            FROM wine_samples;
        """))
        conn.execute(text("""
            ALTER TABLE wine_samples_split ADD COLUMN split_group TEXT;
        """))
        conn.execute(text("""
            UPDATE wine_samples_split
            SET split_group = CASE
                WHEN split_random <= 0.8 THEN 'train'
                WHEN split_random <= 0.9 THEN 'valid'
                ELSE 'test'
            END;
        """))
    print("Created train/valid/test split.")

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS model_registry (
                id SERIAL PRIMARY KEY,
                model_name TEXT,
                version TEXT,
                type TEXT,
                path TEXT,
                accuracy_train REAL,
                accuracy_val REAL,
                accuracy_test REAL
            );
        """))
        conn.execute(text("""
            INSERT INTO model_registry (model_name, version, type, path, accuracy_train, accuracy_val, accuracy_test)
            VALUES ('rf', '20250508_155226', 'RandomForestClassifier', 'models/rf.pkl', 1, 0.70032054, 0.67701864);
        """))
        print("Created model registry and example model.")

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE,
                password TEXT
            );
        """))
        conn.execute(text("""
            INSERT INTO users (email, password)
            VALUES ('test_user', 'test_password')
            ON CONFLICT (email) DO NOTHING;
        """))
        print("Created users table and test user.")
        
if __name__ == "__main__":
    main()

    

