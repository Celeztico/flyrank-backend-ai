import sqlite3
from  pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "tasks.db"

INITIAL_TASKS = [
    ("Learn FastAPI", 0),
    ("Build Task API", 0),
    ("Test CRUD endpoints", 1),
]

def get_connection() -> sqlite3.Connection:
    """
    Creates and returns a connection to the SQLite DB
    """
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def initialise_database():
    """
    Creates the database tables and seeds initial data if required.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL
        )
        """)
        cur.execute("SELECT COUNT(*) FROM tasks")
        task_count = cur.fetchone()[0]
        if task_count == 0:
            cur.executemany(
                "INSERT INTO tasks(title, done) VALUES (?, ?)",
                INITIAL_TASKS
            )
        conn.commit()
    finally:
        conn.close()