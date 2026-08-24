from fastapi import APIRouter, HTTPException, status
from supabase import AuthApiError, AuthWeakPasswordError

from app.auth.schemas import AuthRequest
from app.auth.service import signup_user, login_user, logout_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(request: AuthRequest):
    if not request.email or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )
    if len(request.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password should be at least 6 characters",
        )
    
    try:
        response = signup_user(request.email, request.password)
    except (AuthApiError, AuthWeakPasswordError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    if response.user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create user",
        )

    return response.user

@router.post("/login")
def login(request: AuthRequest):
    if not request.email or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )

    try:
        response = login_user(request.email, request.password)
    except AuthApiError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials",
        )

    if response.session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials",
        )

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
    }

@router.post("/logout")
def logout():
    logout_user()
    return{
        "message": "Logged out successfully",
    }