from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories import user_repository
from app.schemas.user import UserCreate
from app.models.user import User
from typing import List

class UserService:
    async def get_users(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Xử lý logic lấy danh sách người dùng.
        """
        from sqlalchemy.future import select
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        """
        Xử lý logic nghiệp vụ tạo người dùng (Business Logic).
        """
        # Kiểm tra user tồn tại
        user = await user_repository.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system.",
            )
        
        # Gọi Repository để tạo mới
        return await user_repository.create(db, obj_in=user_in)

user_service = UserService()
