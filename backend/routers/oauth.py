from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse

from dependencies import DBSession
from auth.OAuthDependencies import generate_google_oauth_uri, generate_github_oauth_uri
from services.oauth import OAuthRepository
from schemas.response import LoginResponse

from typing import Annotated

router = APIRouter(tags=["OAuth Authorization"])

@router.get("/google/url", response_class=RedirectResponse)
def get_google_oauth_url():
    return RedirectResponse(url=generate_google_oauth_uri(), status_code=302)

@router.post("/google/callback", response_model=LoginResponse)
async def handle_code(code: Annotated[str, Body(embed=True)], db: DBSession):
    token = await OAuthRepository.oauth_google_login_register(code, db)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/github/url", response_class=RedirectResponse)
def github_login():
    return RedirectResponse(url=generate_github_oauth_uri(), status_code=302)

@router.post("/github/callback", response_model=LoginResponse)
async def github_handle_code(code: Annotated[str, Body(embed=True)], db: DBSession):
    token = await OAuthRepository.github_login_register(code, db)
    return {"access_token": token, "token_type": "bearer"}
