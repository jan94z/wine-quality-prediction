import os
import time
import pandas as pd 
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from passlib.context import CryptContext
import click

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

def get_engine() -> None:
    """
    Function to get the database engine.
    Returns:
        engine: SQLAlchemy engine object.
    """
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_name = os.getenv("POSTGRES_DB")

    url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    print(url)
    return create_engine(url)

def wait_for_db(engine) -> None:
    """ 
    Function to wait for the database to be ready.
    Args:
        engine: SQLAlchemy engine object.
    """
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

def query(engine, queries:list[str]) -> None:
    """ 
    Function to execute a list of SQL queries.
    Args:
        engine: SQLAlchemy engine object.
        queries (list[str]): List of SQL queries to execute.
    """
    for query in queries:
        with engine.begin() as conn:
            conn.execute(text(query))

# register user and hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def main() -> None:
    load_dotenv()
    engine = get_engine()

    wait_for_db(engine)

    # Prepare paths
    white_path = Path('init/winequality-white.csv')
    red_path = Path('init/winequality-red.csv')

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

    # create the wine_samples table
    query(engine, ["""
            DROP TABLE IF EXISTS wine_samples"""]) # drop table if it exists])
    query(engine, ["""
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
        """])
    print("wine_samples table ensured.")
    combined_df.to_sql('wine_samples', engine, if_exists="append", index=False)
    print(f"Finished import")

    # Create train/valid/test split
    query(engine, 
          [
            """DROP TABLE IF EXISTS wine_samples_split""", # drop table if it exists
            """
            CREATE TABLE wine_samples_split AS
            SELECT
                id, 
                random() AS split_random
            FROM wine_samples;
            """, # create a new table with random values
            """ALTER TABLE wine_samples_split ADD COLUMN split_group TEXT;""", # add a new column for the split group
            """ 
            UPDATE wine_samples_split
            SET split_group = CASE
                WHEN split_random <= 0.8 THEN 'train'
                WHEN split_random <= 0.9 THEN 'valid'
                ELSE 'test'
            END;
            """ # update the split group based on the random values
          ]
          )

    print("Created train/valid/test split.")


    # Create model registry table
    query(engine,
            [
                """DROP TABLE IF EXISTS model_registry""", # drop table if it exists
                """
                CREATE TABLE model_registry (
                    id SERIAL PRIMARY KEY,
                    model_name TEXT,
                    version TEXT,
                    type TEXT,
                    path TEXT,
                    accuracy_train REAL,
                    accuracy_val REAL,
                    accuracy_test REAL
                );
                """, # create a new table for the model registry
                """
                INSERT INTO model_registry (model_name, version, type, path, accuracy_train, accuracy_val, accuracy_test)
                VALUES ('rf', '20250508_155226', 'RandomForestClassifier', 'models/rf.pkl', 1, 0.70032054, 0.67701864);
                """ # insert an example model into the registry
            ]
)
    print("Created model registry.")

    # Create users table and insert test user
    query(engine,
            [
                """DROP TABLE IF EXISTS users""", # drop table if it exists
                """
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    email TEXT UNIQUE,
                    password TEXT
                );
                """, # create a new table for users
                f"""
                INSERT INTO users (email, password)
                VALUES ('{os.getenv("TEST_USER")}', '{hash_password(os.getenv("TEST_USER_PASSWORD"))}')
                ON CONFLICT (email) DO NOTHING;
                """ # insert a test user into the table
            ]
            )
    print("Created users table and test user.")
        
if __name__ == "__main__":
    main()

    

