from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import os
import sys
sys.path.append("..")
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "testuser1": User(username="testuser1", password=pwd_context.hash("password1234")),
    "testuser2": User(username="testuser2", password=pwd_context.hash("password6789")),
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str) -> User:
    user = fake_users_db.get(username)
    if user is None:
        return None
    return user


def authenticate_user(username: str, password: str) -> User:
    user = get_user(username)
    if user is None or not verify_password(password, user.password):
        return None
    return user


async def get_user(username: str = Depends(oauth2_scheme)) -> User:
    user = get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

