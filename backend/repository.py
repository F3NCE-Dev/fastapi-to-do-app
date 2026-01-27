from fastapi import HTTPException, UploadFile, status

from database import TaskORM, UserORM, FileORM
from schemas import TaskAdd, Task, UserAuthData
from auth.security import create_access_token, hash_password, verify_password
from config.config import settings

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pathlib import Path
import aiofiles

class TaskRepository:
    @classmethod
    async def add_task(cls, data: TaskAdd, user_id: int, db: AsyncSession) -> int:
            task = TaskORM(**data.model_dump(), user_id=user_id)
            db.add(task)
            await db.flush()
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

class ProfilePicture:
    @classmethod
    async def upload_user_profile_picture(cls, data: UploadFile, username: str, user_id: int, db: AsyncSession) -> str:
        if data.content_type not in ("image/jpeg", "image/png"):
            raise HTTPException(400, "Invalid image type")

        filename = Path(data.filename).name

        user_dir = Path(settings.PROFILE_PICTURES_PATH) / username
        user_dir.mkdir(parents=True, exist_ok=True)

        file_path = user_dir / filename

        old_path = await ProfilePicture.get_user_profile_picture_url(user_id, db)

        async with aiofiles.open(file_path, "wb") as file:
            await file.write(await data.read())

        if old_path and old_path != str(file_path) and old_path != settings.DEFAULT_USER_PROFILE_PIC:
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
        file_path = await ProfilePicture.get_user_profile_picture_url(user_id, db)

        if not file_path or file_path == settings.DEFAULT_USER_PROFILE_PIC:
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

        return file.path if file else settings.DEFAULT_USER_PROFILE_PIC
