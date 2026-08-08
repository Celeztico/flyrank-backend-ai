import os
import psycopg
from psycopg.rows import dict_row
from app.config import (
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
)

INITIAL_TASKS = [
    ("Learn FastAPI", False),
    ("Build Task API", False),
    ("Test CRUD endpoints", True),
]

def get_connection() -> psycopg.Connection:
    """
    Creates and returns a connection to the PostgreSQL DB
    """
    return psycopg.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        row_factory=dict_row,
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
        cur.execute("SELECT COUNT(*) AS count FROM tasks")
        task_count = cur.fetchone()["count"]
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
        cur.execute("TRUNCATE TABLE tasks RESTART IDENTITY")
        conn.commit()
    finally:
        conn.close()
        
    initialise_database()