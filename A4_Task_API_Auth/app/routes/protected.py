from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter(prefix="/protected", tags=["Protected"])

security = HTTPBearer()

@router.get("/profile")
def profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    return {
        "message": "Protected profile endpoint",
        "authenticated": True,
    }

@router.get("/dashboard")
def dashboard(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    return {
        "message": "Protected dashboard endpoint",
        "authenticated": True,
    }