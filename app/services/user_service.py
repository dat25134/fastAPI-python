from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories import user_repository
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import get_password_hash, verify_password
from typing import List, Optional

class UserService:
    async def get_users(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        from sqlalchemy.future import select
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        user = await user_repository.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system.",
            )
        
        # Hashing password and delegating to repository
        hashed_password = get_password_hash(user_in.password)
        return await user_repository.create(
            db, obj_in=user_in, hashed_password=hashed_password
        )

    async def authenticate(self, db: AsyncSession, email: str, password: str) -> Optional[User]:
        user = await user_repository.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

user_service = UserService()
