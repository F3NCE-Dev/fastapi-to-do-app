from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import UserORM
from schemas import UserLogin, User_ID

from auth.dependencies import get_db, get_current_user
from auth.security import create_access_token, hash_password, verify_password

from typing import Annotated

security = HTTPBasic()

router = APIRouter(tags=["Authorization"])

@router.post("/register")
async def register(
    userLogin: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserORM).where(UserORM.username == userLogin.username))

    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already exists")

    user = UserORM(
        username=userLogin.username,
        password=hash_password(userLogin.password)
    )
    db.add(user)
    await db.commit()

    return {"message": "User registered successfully"}

@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserORM).where(UserORM.username == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.get("/get_current_user")
def get_current_user_handler(current_user: UserORM = Depends(get_current_user)) -> User_ID:
    return {
        "id": current_user.id,
        "username": current_user.username,
    }