from fastapi import APIRouter, Depends, HTTPException, status
from auth.base_config import auth_backend, fastapi_users
from auth.models import User
from auth.schemas import UserRead, UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])
router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))

def get_current_user(user: User = Depends(fastapi_users.current_user())):
    """Get the current authenticated user."""
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    return user

protected_router = APIRouter()

@protected_router.get("/protected-route", response_model=dict)
def protected_route(user: User = Depends(get_current_user)):
    """Get the protected route for authenticated users."""
    return {"message": f"Hello, {user.username}"}

@router.get("/unprotected-route", response_model=dict)
def unprotected_route():
    """Get the unprotected route for anonymous users."""
    return {"message": "Hello, anonymous"}


router.include_router(protected_router)
