from fastapi import APIRouter, UploadFile, Depends, HTTPException

from repository import ProfilePicture
from database import UserORM
from auth.dependencies import get_current_user
from config.config import settings

from pathlib import Path
import aiofiles

router = APIRouter(tags=["Profile picture"])

@router.post("/upload_profile_picture")
async def upload_profile_picture(data: UploadFile, current_user: UserORM = Depends(get_current_user)):
    if data.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(400, "Invalid image type")

    filename = Path(data.filename).name

    user_dir = Path(settings.PROFILE_PICTURES_PATH) / current_user.username
    user_dir.mkdir(parents=True, exist_ok=True)

    file_path = user_dir / filename

    old_path = await ProfilePicture.get_user_profile_picture_url(current_user.id)

    async with aiofiles.open(file_path, "wb") as file:
        await file.write(await data.read())

    await ProfilePicture.upload_user_profile_picture(user_id=current_user.id, path=str(file_path))

    if old_path and old_path != str(file_path) and old_path != settings.DEFAULT_USER_PROFILE_PIC:
        old_file = Path(old_path)
        if old_file.exists():
            old_file.unlink()

    return {"detail": f"{filename} has successfully uploaded"}

@router.delete("/delete_profile_picture")
async def delete_profile_picture(current_user: UserORM = Depends(get_current_user)):
    file_path = await ProfilePicture.get_user_profile_picture_url(current_user.id)

    if not file_path or file_path == settings.DEFAULT_USER_PROFILE_PIC:
        raise HTTPException(404, "Profile picture not found")

    await ProfilePicture.delete_user_profile_picture(current_user.id)
    
    file_obj = Path(file_path)
    if file_obj.exists():
        file_obj.unlink()

    return {"detail": "Profile picture has successfully deleted"}

@router.get("/get_profile_picture")
async def get_profile_picture_url(current_user: UserORM = Depends(get_current_user)) -> str:
    path = await ProfilePicture.get_user_profile_picture_url(current_user.id)
    return path
