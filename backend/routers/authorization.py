from fastapi import APIRouter, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig

from schemas import UserLogin

router = APIRouter(tags=["Authorization"])

config = AuthXConfig()
config.JWT_SECRET_KEY = "S KEY"
config.JWT_ACCESS_COOKIE_NAME = "App access token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

@router.post("/login")
def login(credentials: UserLogin, response: Response):
    if credentials.username == "test" and credentials.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@router.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"detail": "You have an access"}
