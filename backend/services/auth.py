from fastapi import HTTPException, status

from models.user import UserORM
from schemas.user import UserAuthData, UserID
from auth.security import create_access_token, hash_password, verify_password

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class AuthorizationRepository:
    @classmethod
    async def register_user(cls, data: UserAuthData, db: AsyncSession) -> str:
        result = await db.execute(select(UserORM).where(UserORM.username == data.username))

        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already exists")

        user = UserORM(
            username=data.username,
            password=hash_password(data.password)
        )
        db.add(user)
        await db.commit()

        return user.username

    @classmethod
    async def login_user(cls, data: UserAuthData, db: AsyncSession) -> str:
        result = await db.execute(select(UserORM).where(UserORM.username == data.username))
        user = result.scalar_one_or_none()

        if not user or not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        return create_access_token({"sub": user.username})

    @classmethod
    async def get_user(cls, data: UserID) -> UserID:
        return UserID(
            id=data.id,
            username=data.username,
        )

    