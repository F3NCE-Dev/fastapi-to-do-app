from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from schemas import UserAuthData, UserID, StatusResponse, LoginResponse
from repository import AuthorizationRepository
from auth.dependencies import DBSession, CurrentUser

from typing import Annotated

router = APIRouter(tags=["Authorization"])

@router.post("/register", response_model=StatusResponse)
async def register(userRegister: UserAuthData, db: DBSession):
    username = await AuthorizationRepository.register_user(userRegister, db)
    return {"success": True, "detail": f"{username} has successfully registered"}

@router.post("/login", response_model=LoginResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DBSession):
    credentials = UserAuthData(
        username=form_data.username,
        password=form_data.password,
    )

    token = await AuthorizationRepository.login_user(credentials, db) 
    return {"access_token": token, "token_type": "bearer"}

@router.get("/user", response_model=UserID)
async def get_current_user_handler(current_user: CurrentUser):
    return await AuthorizationRepository.get_user(current_user)
