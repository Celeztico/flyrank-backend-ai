from fastapi import HTTPException
from app.database import get_connection , reset_database
from app.models.task import Task, TaskCreate, TaskUpdate, TaskStats

def get_tasks(
    done: bool | None = None,
    search: str | None = None,
    limit: int | None = None,
    offset: int = 0,
) -> list[Task]:
    """
    Return tasks, optionally filtered by completion status,
    search query, and paginated using limit/offset.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        query = "SELECT * FROM tasks"
        conditions = []
        parameters = []

        # building filtering conditions
        if done is not None:
            conditions.append("done = ?")
            parameters.append(int(done))
        
        if search is not None:
            conditions.append("title LIKE ?")
            parameters.append(f"%{search}%")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # building pagination conditions
        query += " ORDER BY id ASC LIMIT ? OFFSET ?"
        if limit is not None:
            parameters.append(limit)
        else:
            parameters.append(-1)

        parameters.append(offset)

        cur.execute(query, parameters)

        rows = cur.fetchall()
        
        return [
            Task(
                id=row["id"],
                title=row["title"],
                done=bool(row["done"])
            ) for row in rows
        ]
    finally:
        conn.close()

def get_task(task_id: int) -> Task:
    """
    Return task by id
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": f"Task with id {task_id} not found"
                }
            )
        return Task(
            id=row["id"],
            title=row["title"],
            done=bool(row["done"])
        )
    finally:
        conn.close()

def create_task(task_create: TaskCreate) -> Task:
    """
    Create a new task, store it in database, and return the created task.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO tasks(title, done) VALUES(?, ?)", 
            (task_create.title, 0),
        )
        next_id = cur.lastrowid
        conn.commit()

        return Task(
            id=next_id,
            title=task_create.title,
            done=False
        )
    finally:
        conn.close()

def update_task(
        task_id: int,
        task_update: TaskUpdate
) -> Task:
    """
    Update existing task of given id and return it
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        get_task(task_id)

        cur.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?", 
            (
                task_update.title, 
                int(task_update.done), 
                task_id
            ),
        )
        conn.commit()

        return Task(
            id=task_id,
            title=task_update.title,
            done=task_update.done
        )
    finally:
        conn.close()

def delete_task(task_id: int) -> None:
    """
    Delete a task of given id
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        get_task(task_id)
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    finally:
        conn.close()

def get_stats() -> TaskStats:
    """
    Return statistics for all tasks.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT COUNT(*) AS total, COALESCE(SUM(done),0) AS done FROM tasks")
        row = cur.fetchone()

        return TaskStats(
            total=row["total"],
            done=row["done"],
            open=row["total"] - row["done"],
        )
    finally:
        conn.close()

def reset_tasks() -> list[Task]:
    """
    Reset the database to the initial seeded state
    and return the seeded tasks.
    """
    reset_database()
    return get_tasks()
