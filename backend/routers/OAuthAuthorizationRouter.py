from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import RedirectResponse

from config.config import settings
from auth.dependencies import DBSession
from auth.OAuthDependencies import generate_google_oauth_uri
from repository import AuthorizationRepository
from schemas import LoginResponse

from typing import Annotated
import aiohttp
import jwt

router = APIRouter(tags=["OAuth Authorization"])

@router.get("/google/url")
def get_google_oauth_url():
    uri = generate_google_oauth_uri()
    return RedirectResponse(url=uri, status_code=302)

@router.post("/google/callback", response_model=LoginResponse)
async def handle_code(code: Annotated[str, Body(embed=True)], db: DBSession):    
    async with aiohttp.ClientSession() as session, session.post(
        url="https://oauth2.googleapis.com/token",
        data={
            "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
            "client_secret": settings.OAUTH_GOOGLE_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:5500/frontend/index.html",
            "code": code,
        },
    ) as response:
        res = await response.json()
        
        if "error" in res:
            raise HTTPException(status_code=400, detail=res.get("error_description", "OAuth error"))

        id_token = res["id_token"]
        user_data = jwt.decode(id_token, algorithms=["RS256"], options={"verify_signature": False})
        
        email = user_data.get("email")
        name = user_data.get("name") or user_data.get("given_name")

        if not email:
            raise HTTPException(status_code=400, detail="Email not found in token")

        token = await AuthorizationRepository.oauth_login_register(email, name, db)
        return {"access_token": token, "token_type": "bearer"}
