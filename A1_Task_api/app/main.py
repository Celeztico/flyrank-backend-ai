from fastapi import FastAPI, Request
from app.routes.tasks import router as task_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=400,
        content={
                "error": "Title is required."
        }
    )

@app.get("/")
def root():
    return {"name": "Task API", "version":"1.0", "endpoints":["/tasks", "/health"]}

@app.get("/health")
def health():
    return {"status":"ok"}

app.include_router(task_router)