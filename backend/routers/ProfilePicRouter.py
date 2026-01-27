from fastapi import APIRouter, UploadFile

from repository import ProfilePicture
from auth.dependencies import CurrentUser, DBSession
from schemas import StatusResponse

router = APIRouter(tags=["Profile picture"])

@router.post("/upload_profile_picture", response_model=StatusResponse)
async def upload_profile_picture(data: UploadFile, current_user: CurrentUser, db: DBSession):
    filename = await ProfilePicture.upload_user_profile_picture(data=data, username=current_user.username, user_id=current_user.id, db=db)
    return {"success": True, "detail": f"{filename} has successfully uploaded"}

@router.delete("/delete_profile_picture", response_model=StatusResponse)
async def delete_profile_picture(current_user: CurrentUser, db: DBSession):
    await ProfilePicture.delete_user_profile_picture(current_user.id, db)
    return {"success": True, "detail": "Profile picture has successfully deleted"}

@router.get("/get_profile_picture")
async def get_profile_picture_url(current_user: CurrentUser, db: DBSession) -> str:
    path = await ProfilePicture.get_user_profile_picture_url(current_user.id, db)
    return path
