from fastapi import HTTPException
from app.data import tasks, initial_tasks
from app.database import get_connection
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
        query += " ORDER BY ID ASC LIMIT ? OFFSET ?"
        if limit is not None:
            parameters.append(limit)
        else:
            parameters.append(-1)

        parameters.append(offset)

        print(query)
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

    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(
        status_code=404,
        detail={
            "error": f"Task with id {task_id} not found"
        }
    )

def create_task(task_create: TaskCreate) -> Task:
    """
    Create a new task, assign it the next available ID,
store it in memory, and return it.
    """
    next_id = max((task.id for task in tasks), default=0)+1

    new_task = Task(
        id=next_id,
        title=task_create.title,
        done=False
    )

    tasks.append(new_task)

    return new_task

def update_task(
        task_id: int,
        task_update: TaskUpdate
) -> Task:
    """
    Update existing task of given id and return it
    """
    task = get_task(task_id)

    task.title = task_update.title

    task.done=task_update.done

    return task

def delete_task(task_id: int) -> None:
    task = get_task(task_id)
    tasks.remove(task)
    return

def get_stats() -> TaskStats:
    total = len(tasks)
    done = len([ task for task in tasks if task.done ])
    return TaskStats(
        total=total,
        done=done,
        open= total - done,
    )

def reset_tasks():
    tasks.clear()
    tasks.extend(initial_tasks)
    return tasks
