from fastapi import APIRouter, HTTPException, Depends, status
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/profile")
def profile(
    user = Depends(get_current_user),
):    
    return {
        "id": user.id,
        "email": user.email,
    }

@router.get("/dashboard")
def dashboard(
    user = Depends(get_current_user),
):
    return {
        "message": "Protected dashboard endpoint",
        "authenticated": True,
    }