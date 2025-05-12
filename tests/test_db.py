import pytest
from sqlalchemy import create_engine, text

# connect to DB
DATABASE_URL = "postgresql://wine123:wine123@localhost:5433/wine-quality-db"

@pytest.fixture(scope="module")
def test_db():
    engine = create_engine(DATABASE_URL)
    # create table for testing
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS test_users (
                id SERIAL PRIMARY KEY,
                username TEXT,
                password TEXT
            )
        """))
        conn.execute(text("INSERT INTO test_users (username, password) VALUES ('jan', 'secret')"))

    yield engine

    # drop table after tests
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS test_users"))

def test_user_insert(test_db):
    with test_db.connect() as conn:
        result = conn.execute(text("SELECT * FROM test_users WHERE username='jan'"))
        row = result.fetchone()
        assert row is not None
        assert row.username == 'jan'
