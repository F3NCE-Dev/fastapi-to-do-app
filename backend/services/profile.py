from fastapi import HTTPException, UploadFile

from models.user import UserORM
from auth.security import create_access_token, hash_password
from config.config import settings

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pathlib import Path
import aiofiles

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
    async def edit_password(cls, user_id: int, password: str, db: AsyncSession) -> str:
        user = await db.get(UserORM, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.password = hash_password(password=password)
        await db.commit()

        return create_access_token({"sub": user.username})

    @classmethod
    async def upload_user_profile_picture(cls, data: UploadFile, user_id: int, db: AsyncSession) -> str:
        result = await db.execute(select(UserORM).where(UserORM.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(404, "User not found")

        if data.content_type not in ("image/jpeg", "image/png"):
            raise HTTPException(400, "Invalid image type")

        filename = Path(data.filename).name

        user_dir = Path(settings.STATIC_DIR) / settings.PROFILE_PICTURES_FOLDER_NAME / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        file_path = user_dir / filename

        old_path = user.picture_path

        if old_path != settings.DEFAULT_USER_PROFILE_PIC_PATH:
            old_file = Path(old_path)
            if old_file.exists():
                old_file.unlink()
            
        async with aiofiles.open(file_path, "wb") as file:
            await file.write(await data.read())
        
        user.picture_path = file_path.as_posix()
            
        await db.commit()
        return filename

    @classmethod
    async def delete_user_profile_picture(cls, user_id: int, db: AsyncSession) -> None:
        result = await db.execute(select(UserORM).where(UserORM.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(404, "User not found")

        file_path = user.picture_path

        if file_path == settings.DEFAULT_USER_PROFILE_PIC_PATH:
            return
        
        file_obj = Path(file_path)
        if file_obj.exists():
            file_obj.unlink()

        user.picture_path = settings.DEFAULT_USER_PROFILE_PIC_PATH
        await db.commit()

    @classmethod
    async def get_user_profile_picture_url(cls, user_id: int, db: AsyncSession) -> str | None:
        result = await db.execute(select(UserORM).where(UserORM.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(404, "User not found")

        return user.picture_path