from fastapi import APIRouter
from app.models.task import Task
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
    summary="Get all tasks",
    description="Returns all tasks stored in memory",
)
def get_task(task_id: int):
    return task_service.get_task(task_id)