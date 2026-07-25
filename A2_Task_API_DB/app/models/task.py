from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int
    title: str
    done: bool

class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Title of the task"
    )

class TaskUpdate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    done: bool

class TaskStats(BaseModel):
    total: int
    done: int
    open: int