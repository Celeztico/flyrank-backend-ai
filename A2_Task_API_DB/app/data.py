from app.models.task import Task
import copy

initial_tasks = [
    Task(
        id=1,
        title="Study FastAPI",
        done=False,
    ),
    Task(
        id=2,
        title="Build CRUD API",
        done=False,
    ),
    Task(
        id=3,
        title="Push to GitHub",
        done=True,
    ),
]

tasks = copy.deepcopy(initial_tasks)