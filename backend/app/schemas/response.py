from pydantic import BaseModel, ConfigDict

class StatusResponse(BaseModel):
    success: bool
    detail: str

class TaskAddResponse(BaseModel):
    success: bool
    task_id: int

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)
