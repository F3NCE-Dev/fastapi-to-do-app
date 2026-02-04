from fastapi import HTTPException, UploadFile, status

from database import TaskORM, UserORM, FileORM
from schemas import TaskAdd, Task, UserAuthData, UserID
from auth.security import create_access_token, hash_password, verify_password
from config.config import settings

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pathlib import Path
import re
import secrets
import aiofiles
import httpx
import jwt

class TaskRepository:
    @classmethod
    async def add_task(cls, data: TaskAdd, user_id: int, db: AsyncSession) -> int:
        task = TaskORM(**data.model_dump(), user_id=user_id)
        db.add(task)
        await db.commit()
        return task.id
        
    @classmethod
    async def delete_task(cls, id: int, user_id: int, db: AsyncSession) -> None:
        result = await db.execute(select(TaskORM).where(TaskORM.id == id, TaskORM.user_id == user_id))

        task = result.scalar_one_or_none()

        if task is None:
            raise HTTPException(status_code=404, detail="There is no task with that name")

        await db.delete(task)
        await db.commit()

    @classmethod
    async def set_task(cls, id: int, status: bool, user_id: int, db: AsyncSession) -> None:
        result = await db.execute(select(TaskORM).where(TaskORM.id == id, TaskORM.user_id == user_id))
        task = result.scalar_one_or_none()

        if task is None:
            raise HTTPException(status_code=404, detail="There is no task with that id")
        
        task.status = status

        await db.commit()

    @classmethod
    async def get_all_tasks(cls, user_id: int, db: AsyncSession) -> list[Task]:
        result = await db.execute(select(TaskORM).where(TaskORM.user_id == user_id))
        task_models = result.scalars().all()
        task_schemas = [Task.model_validate(task_model) for task_model in task_models]
        return task_schemas

class AuthorizationRepository:
    @classmethod
    async def register_user(cls, data: UserAuthData, db: AsyncSession) -> str:
        result = await db.execute(select(UserORM).where(UserORM.username == data.username))

        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already exists")

        user = UserORM(
            username=data.username,
            password=hash_password(data.password)
        )
        db.add(user)
        await db.commit()

        return user.username

    @classmethod
    async def login_user(cls, data: UserAuthData, db: AsyncSession) -> str:
        result = await db.execute(select(UserORM).where(UserORM.username == data.username))
        user = result.scalar_one_or_none()

        if not user or not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        return create_access_token({"sub": user.username})

    @classmethod
    async def get_user(cls, data: UserID) -> UserID:
        return UserID(
            id=data.id,
            username=data.username,
        )

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

class ProfileEditRepository:
    @classmethod
    async def rename_user_profile(cls, new_name: str, user_id: int, db: AsyncSession) -> str:
        result_existing = await db.execute(select(UserORM).where(UserORM.username == new_name))
        if result_existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already exists")

        result = await db.execute(select(UserORM).where(UserORM.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.username = new_name
        await db.commit()

        return create_access_token({"sub": new_name})

    @classmethod
    async def upload_user_profile_picture(cls, data: UploadFile, user_id: int, db: AsyncSession) -> str:
        if data.content_type not in ("image/jpeg", "image/png"):
            raise HTTPException(400, "Invalid image type")

        filename = Path(data.filename).name

        user_dir = settings.PROFILE_PICTURES_PATH / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        file_path = user_dir / filename

        old_path = await ProfileEditRepository.get_user_profile_picture_url(user_id, db)

        async with aiofiles.open(file_path, "wb") as file:
            await file.write(await data.read())

        if old_path and old_path != file_path.as_posix() and old_path != settings.DEFAULT_USER_PROFILE_PIC_URL:
            old_file = Path(old_path)
            if old_file.exists():
                old_file.unlink()

        result = await db.execute(select(FileORM).where(FileORM.user_id == user_id))
        file = result.scalar_one_or_none()

        if file:
            file.path = file_path.as_posix()
        else:
            file = FileORM(user_id=user_id, path=file_path.as_posix())
            db.add(file)
            
        await db.commit()
        return filename

    @classmethod
    async def delete_user_profile_picture(cls, user_id: int, db: AsyncSession) -> None:
        file_path = await ProfileEditRepository.get_user_profile_picture_url(user_id, db)

        if not file_path or file_path == settings.DEFAULT_USER_PROFILE_PIC_URL:
            raise HTTPException(404, "Profile picture not found")
        
        file_obj = Path(file_path)
        if file_obj.exists():
            file_obj.unlink()

            result = await db.execute(select(FileORM).where(FileORM.user_id == user_id))
            await db.delete(result.scalar_one_or_none())
            await db.commit()

    @classmethod
    async def get_user_profile_picture_url(cls, user_id: int, db: AsyncSession) -> str | None:
        result = await db.execute(select(FileORM).where(FileORM.user_id == user_id))
        file = result.scalar_one_or_none()

        return file.path if file else settings.DEFAULT_USER_PROFILE_PIC_URL
