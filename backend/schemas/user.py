from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated

UsernameStr = Annotated[str, StringConstraints(min_length=1, max_length=25, pattern=r"^[a-zA-Z0-9_-]+$")]
PasswordStr = Annotated[str, StringConstraints(min_length=5, max_length=25)]

class UserAuthData(BaseModel):
    username: UsernameStr
    password: PasswordStr

class UserNewName(BaseModel):
    new_name: UsernameStr

class UserID(BaseModel):
    id: int
    username: str

class NewPassword(BaseModel):
    password: PasswordStr
