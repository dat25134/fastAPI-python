from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, models
from app.services import user_service
from app.api import deps
from app.schemas.response import ResponseSuccess

router = APIRouter()

@router.get("/", response_model=ResponseSuccess[List[schemas.user.User]])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = await user_service.get_users(db, skip=skip, limit=limit)
    return ResponseSuccess(data=users)

@router.post("/", response_model=ResponseSuccess[schemas.user.User])
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = await user_service.create_user(db, user_in=user_in)
    return ResponseSuccess(data=user)

@router.get("/me", response_model=ResponseSuccess[schemas.user.User])
async def read_user_me(
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return ResponseSuccess(data=current_user)
