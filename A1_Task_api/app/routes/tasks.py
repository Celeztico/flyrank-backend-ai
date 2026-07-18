from fastapi import APIRouter
from app.models.task import Task, TaskCreate
from app.services import task_service

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.get(
    "",
    response_model=list[Task],
    summary="Get all tasks",
    description="Returns all tasks stored in memory",
)
def get_tasks():
    return task_service.get_tasks()

@router.get(
    "/{task_id}",
    response_model=Task,
    summary="Get tasks with id task_id",
    description="Returns task_id from tasks in memory",
)
def get_task(task_id: int):
    return task_service.get_task(task_id)

@router.post(
    "",
    response_model=Task,
    status_code=201,
    summary="Create a task",
    description="Creates a new task and returns it",
)
def create_task(task_create: TaskCreate):
    return task_service.create_task(task_create)