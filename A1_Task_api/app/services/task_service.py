from fastapi import HTTPException
from app.data import tasks
from app.models.task import Task, TaskCreate, TaskUpdate

def get_tasks() -> list[Task]:
    """
    Return all tasks
    """
    return tasks

def get_task(task_id: int) -> Task:
    """
    Return task by id
    """

    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(
        status_code=404,
        details=f"Task with id {task_id} not found"
    )