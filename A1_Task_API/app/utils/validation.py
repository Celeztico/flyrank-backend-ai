from fastapi.exceptions import RequestValidationError


def get_validation_error_message(exc: RequestValidationError) -> str:
    """
    Convert FastAPI/Pydantic validation errors into
    user-friendly API error messages.
    """

    error = exc.errors()[0]

    error_type = error["type"]

    if error_type == "missing":
        field = error["loc"][-1]
        return f"{field.replace('_', ' ').title()} is required."

    if error_type == "string_too_short":
        field = error["loc"][-1]
        return f"{field.replace('_', ' ').title()} cannot be empty."

    if error_type == "json_invalid":
        return "Request body contains invalid JSON."

    return "Invalid request."