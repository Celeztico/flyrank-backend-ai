from fastapi import FastAPI
from app.routes.tasks import router as task_router

app = FastAPI()

@app.get("/")
def root():
    return {"name": "Task API", "version":"1.0", "endpoints":["/tasks", "/health"]}

@app.get("/health")
def health():
    return {"status":"ok"}

app.include_router(task_router)