from fastapi import APIRouter, UploadFile

from repository import ProfileEditRepository
from dependencies import CurrentUser, DBSession
from schemas import StatusResponse, UserNewName, LoginResponse

router = APIRouter(tags=["Profile Edit"])

@router.patch("/rename-profile", response_model=LoginResponse)
async def rename_profile(new_name_data: UserNewName, current_user: CurrentUser, db: DBSession):
    new_token = await ProfileEditRepository.rename_user_profile(new_name_data.new_name, current_user.id, db)
    return {"access_token": new_token, "token_type": "bearer"}

@router.post("/upload-profile-picture", response_model=StatusResponse)
async def upload_profile_picture(data: UploadFile, current_user: CurrentUser, db: DBSession):
    filename = await ProfileEditRepository.upload_user_profile_picture(data=data, user_id=current_user.id, db=db)
    return {"success": True, "detail": f"{filename} has successfully uploaded"}

@router.delete("/delete-profile-picture", response_model=StatusResponse)
async def delete_profile_picture(current_user: CurrentUser, db: DBSession):
    await ProfileEditRepository.delete_user_profile_picture(current_user.id, db)
    return {"success": True, "detail": "Profile picture has successfully deleted"}

@router.get("/get-profile-picture")
async def get_profile_picture_url(current_user: CurrentUser, db: DBSession) -> str:
    path = await ProfileEditRepository.get_user_profile_picture_url(current_user.id, db)
    return path
