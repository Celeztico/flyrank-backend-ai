import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

INITIAL_TASKS = [
    ("Learn FastAPI", 0),
    ("Build Task API", 0),
    ("Test CRUD endpoints", 1),
]

def get_connection() -> psycopg.Connection:
    """
    Creates and returns a connection to the SQLite DB
    """
    return psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )

def initialise_database():
    """
    Creates the database tables and seeds initial data if required.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
        """)
        cur.execute("SELECT COUNT(*) FROM tasks")
        task_count = cur.fetchone()[0]
        if task_count == 0:
            cur.executemany(
                "INSERT INTO tasks(title, done) VALUES (%s, %s)",
                INITIAL_TASKS,
            )
        conn.commit()
    finally:
        conn.close()

def reset_database():
    """
    Resets the database to its initial development state
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM tasks")
        cur.execute("TRUNCATE TABLE tasks RESTART IDENTITY")
        conn.commit()
    finally:
        conn.close()
        
    initialise_database()