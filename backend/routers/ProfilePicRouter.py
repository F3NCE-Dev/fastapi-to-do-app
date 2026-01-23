from fastapi import APIRouter, UploadFile, Depends, HTTPException

from repository import ProfilePicture
from database import UserORM
from auth.dependencies import get_current_user

from pathlib import Path
import aiofiles

router = APIRouter(tags=["Profile picture"])

@router.post("/upload_profile_picture")
async def upload_profile_picture(data: UploadFile, current_user: UserORM = Depends(get_current_user)):
    if data.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(400, "Invalid image type")

    filename = Path(data.filename).name

    user_dir = Path("media/users") / current_user.username
    user_dir.mkdir(parents=True, exist_ok=True)

    file_path = user_dir / filename

    old_path = await ProfilePicture.get_user_profile_picture_url(current_user.id)

    async with aiofiles.open(file_path, "wb") as file:
        await file.write(await data.read())

    await ProfilePicture.upload_user_profile_picture(user_id=current_user.id, path=str(file_path))

    if old_path and old_path != str(file_path):
        old_file = Path(old_path)
        if old_file.exists():
            old_file.unlink()

    return {"detail": f"{filename} has successfully uploaded"}

@router.get("/get_profile_picture")
async def get_profile_picture_url(current_user: UserORM = Depends(get_current_user)):
    path = await ProfilePicture.get_user_profile_picture_url(current_user.id)
    return path
