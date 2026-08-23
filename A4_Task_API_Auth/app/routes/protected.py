from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.service import verify_access_token
from supabase_auth.errors import AuthApiError

router = APIRouter(prefix="/protected", tags=["Protected"])

security = HTTPBearer()

@router.get("/profile")
def profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        response = verify_access_token(credentials.credentials)
    except AuthApiError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = response.user
    
    return {
        "id": user.id,
        "email": user.email,
    }

@router.get("/dashboard")
def dashboard(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        verify_access_token(credentials.credentials)
    except AuthApiError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return {
        "message": "Protected dashboard endpoint",
        "authenticated": True,
    }