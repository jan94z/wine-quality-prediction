from passlib.context import CryptContext
import os 
from sqlalchemy import create_engine, text

def get_engine():
    """
    Function to get the database engine.
    Returns:
        engine: SQLAlchemy engine object.
    """
    db_user = os.environ.get("POSTGRES_USER", "postgres")
    db_pass = os.environ.get("POSTGRES_PASSWORD", "postgres")
    db_host = os.environ.get("POSTGRES_HOST", "db")
    db_port = os.environ.get("POSTGRES_PORT", "5432")
    db_name = os.environ.get("POSTGRES_DB", "db")

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
                result = conn.execute(text(query))
        else:
            with engine.connect() as conn:
                result = conn.execute(text(query))

    return result

def hash_password(password: str) -> str:
    pwd_context = CryptContext(schemes=[os.environ.get("CRYPT_CONTEXT", "bcrypt")], deprecated="auto")
    return pwd_context.hash(password)
