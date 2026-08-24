from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["Public"])

@router.get("/info")
def public_info():
    return {
        "message": "This is a public endpoint",
        "authenticated": False
    }