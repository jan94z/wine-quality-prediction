import os
import time
import pandas as pd 
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from shared.utils import get_engine, query, hash_password

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

def main() -> None:
    engine = get_engine()

    wait_for_db(engine)

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

    # create the wine_samples table

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
          ["""SELECT setseed(0);""", # set seed for reproducibility
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

    # Create users table and insert test user
    query(engine,
            [   """
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    email TEXT UNIQUE,
                    password TEXT
                );
                """, # create a new table for users
                f"""
                INSERT INTO users (email, password)
                VALUES ('{os.environ.get("TEST_USER", "test_user")}', '{hash_password(os.environ.get("TEST_USER_PASSWORD", "test_password"))}')
                ON CONFLICT (email) DO NOTHING;
                """ # insert a test user into the table
            ]
            )
    print("Created users table and test user.")
        
if __name__ == "__main__":
    main()

    

