from fastapi import HTTPException

from models.user import UserORM
from auth.security import create_access_token, hash_password
from config.config import settings

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import re
import secrets
import httpx
import jwt

class OAuthRepository:
    @classmethod
    async def oauth_google_login_register(cls, code: str, db: AsyncSession) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://oauth2.googleapis.com/token",
                data={
                    "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
                    "client_secret": settings.OAUTH_GOOGLE_CLIENT_SECRET,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.REDIRECT_URI,
                    "code": code,
                })
            res = response.json()
        
            if "error" in res:
                raise HTTPException(status_code=400, detail=res.get("error_description", "OAuth error"))

            id_token = res["id_token"]
            user_data = jwt.decode(id_token, algorithms=["RS256"], options={"verify_signature": not settings.DEBUG_MODE})
            
            email = user_data.get("email")
            name = user_data.get("name") or user_data.get("given_name")

            if not email:
                raise HTTPException(status_code=400, detail="Email not found in token")

            result = await db.execute(select(UserORM).where(UserORM.email == email))
            user = result.scalar_one_or_none()

            if user:
                return create_access_token({"sub": user.username})

            base_name = name if name else email.split("@")[0]
            clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', base_name)
            if not clean_name:
                clean_name = "user"

            username = clean_name
            counter = 1

            while True:
                res = await db.execute(select(UserORM).where(UserORM.username == username))
                if not res.scalar_one_or_none():
                    break
                username = f"{clean_name}{counter}"
                counter += 1

            random_password = secrets.token_urlsafe(16)
            user = UserORM(username=username, password=hash_password(random_password), email=email)
            db.add(user)
            await db.commit()

            return create_access_token({"sub": user.username})

    @classmethod
    async def github_login_register(cls, code: str, db: AsyncSession) -> str:
        params = {
        'client_id': settings.OAUTH_GITHUB_CLIENT_ID,
        'client_secret': settings.OAUTH_GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.REDIRECT_URI
        }

        headers = {'Accept': 'application/json'}

        async with httpx.AsyncClient() as client:
            response = await client.post(url="https://github.com/login/oauth/access_token", params=params, headers=headers)
            response_json = response.json()

            if "error" in response_json:
                raise HTTPException(status_code=400, detail=response_json.get("error_description", "GitHub OAuth error"))

            access_token = response_json['access_token']
            
            headers.update({'Authorization': f'Bearer {access_token}'})
            response = await client.get(url="https://api.github.com/user", headers=headers)
            user_data = response.json()

        result = await db.execute(select(UserORM).where(UserORM.github_id == user_data['id']))
        user = result.scalar_one_or_none()

        if user:
            return create_access_token({"sub": user.username})

        base_name = user_data['login']
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', base_name)
        if not clean_name:
            clean_name = "github_user"

        username = clean_name
        counter = 1

        while True:
            res = await db.execute(select(UserORM).where(UserORM.username == username))
            if not res.scalar_one_or_none():
                break
            username = f"{clean_name}{counter}"
            counter += 1

        random_password = secrets.token_urlsafe(16)
        user = UserORM(username=username, password=hash_password(random_password), github_id=user_data['id'])
        db.add(user)
        await db.commit()

        return create_access_token({"sub": user.username})