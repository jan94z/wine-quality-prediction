from passlib.context import CryptContext
import os 
from sqlalchemy import create_engine, text

def get_engine():
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

def query(engine, queries:list[str], commit:bool=True) -> None:
    """ 
    Function to execute a list of SQL queries.
    Args:
        engine: SQLAlchemy engine object.
        queries (list[str]): List of SQL queries to execute.
    """
    for query in queries:
        if commit:
            with engine.begin() as conn:
                conn.execute(text(query))
        else:
            with engine.connect() as conn:
                conn.execute(text(query))

def hash_password(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)
