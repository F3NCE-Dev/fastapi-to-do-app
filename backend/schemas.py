from pydantic import BaseModel, ConfigDict, Field

class UserAuthData(BaseModel):
    username: str = Field(min_length=1, max_length=25, pattern=r"^[a-zA-Z0-9_-]+$")
    password: str = Field(min_length=5, max_length=25)

class UserID(BaseModel):
    id: int
    username: str

class TaskAdd(BaseModel):
    task: str = Field(default="task", min_length=1, max_length=255)
    status: bool = False

class Task(TaskAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

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
