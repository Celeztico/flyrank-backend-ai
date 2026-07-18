from fastapi import FastAPI, Request
from app.routes.tasks import router as task_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.utils import validation

app = FastAPI(
    title="Task API",
    description="A simple RESTful Task Management API built for the FlyRank Backend Internship Assignment.",
    version="1.0.0",
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=400,
        content={
            "error": validation.get_validation_error_message(exc)
        }
    )

@app.get("/")
def root():
    return {"name": "Task API", "version":"1.0", "endpoints":["/tasks", "/health"]}

@app.get("/health")
def health():
    return {"status":"ok"}

app.include_router(task_router)