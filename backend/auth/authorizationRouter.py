from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import UserORM

from auth.dependencies import get_db, get_current_user
from auth.security import create_access_token

from typing import Annotated

security = HTTPBasic()

auth_router = APIRouter(tags=["Authorization"])

@auth_router.post("/register")
async def register(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserORM).where(UserORM.username == username))

    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already exists")

    user = UserORM(
        username=username,
        #password_hash=hash_password(password),
        password=password
    )
    db.add(user)
    await db.commit()

    return {"message": "User registered successfully"}

@auth_router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserORM).where(UserORM.username == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@auth_router.get("/get_current_user")
def get_current_user_handler(current_user: UserORM = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
    }