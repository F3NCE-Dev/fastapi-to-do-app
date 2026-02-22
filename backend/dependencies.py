from fastapi import Depends, HTTPException, status

from database import new_session
from models.user import UserORM

from auth.security import oauth2_scheme
from config.config import settings

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import jwt

async def get_db():
    async with new_session() as session:
        yield session

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db),
) -> UserORM:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    result = await db.execute(select(UserORM).where(UserORM.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception

    return user

DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[UserORM, Depends(get_current_user)]
