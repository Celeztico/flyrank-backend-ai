from fastapi import HTTPException
from app.data import tasks
from app.models.task import Task, TaskCreate, TaskUpdate

def get_tasks(done: bool | None = None, search: str | None = None) -> list[Task]:
    """
    Return all tasks, optionally filtered by completion/search
    """
    filtered_task= tasks
    
    if done is not None:
        filtered_task = [ task for task in filtered_task if task.done == done ]
    
    if search is not None:
        filtered_task = [ task for task in filtered_task if search.lower() in task.title.lower() ]
    
    return filtered_task

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
