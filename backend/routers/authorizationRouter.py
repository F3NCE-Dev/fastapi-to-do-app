from fastapi import APIRouter, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from repository import AuthorizationRepository

from schemas import UserLogin

router = APIRouter(tags=["Authorization"])

config = AuthXConfig()
config.JWT_SECRET_KEY = "SKEY"
config.JWT_ACCESS_COOKIE_NAME = "App_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

@router.post("/register")
async def register(data: UserLogin):
    result = await AuthorizationRepository.register_new_user(data)
    return result

@router.post("/login")
async def login(credentials: UserLogin, response: Response):
    print(credentials.username)
    user = await AuthorizationRepository.get_user_by_username(
        credentials.username
    )
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    if credentials.username == user.username and credentials.password == user.hashed_password:
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@router.get("/protected", dependencies=[Depends(security.access_token_required)], summary="Check an user access")
def protected():
    return {"detail": "You have an access"}

@router.post("/set_image", summary="set a profile picture")
async def set_profile_image(user_id: int):
    ...

@router.get("/get_profile_image", summary="get an user profile picture")
async def get_profile_image(user_id: int):
    ...