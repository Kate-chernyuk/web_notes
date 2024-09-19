from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
#import sys
#sys.path.append("..")
from app.models import User
from app.utils.auth import ( authenticate_user, get_user)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}}
)

USERS = {
    "testuser1": "password1234",
    "testuser2": "password6789"
}

@router.post("/login", response_model=User)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


@router.get("/me", response_model=User)
async def get_user(user: int = Depends(get_user)):
    return USERS[user]
