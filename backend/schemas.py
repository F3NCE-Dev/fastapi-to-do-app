from pydantic import BaseModel, ConfigDict, Field, constr

UsernameStr = constr(min_length=1, max_length=25, pattern=r"^[a-zA-Z0-9_-]+$")

class UserAuthData(BaseModel):
    username: str = UsernameStr
    password: str = Field(min_length=5, max_length=25)

class UserNewName(BaseModel):
    new_name: str = UsernameStr

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
