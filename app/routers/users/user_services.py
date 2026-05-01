from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.users.user_schemas import UserResponse, UserUpdate
from app.routers.users.user_controller import UserController

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

user_controller = UserController()

@router.post("/get_all_users", response_model=UserResponse)
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(...)
):
    return await user_controller.get_all_users(db=db, authorization=authorization)

@router.post("/get_user", response_model=UserResponse)
async def get_user(
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(...)
):
    return await user_controller.get_user(db=db, authorization=authorization)

@router.post("/edit_account", response_model=UserResponse)
async def edit_user(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(...)
):
    return await user_controller.edit_user(db=db, user_update=user_update, authorization=authorization)

@router.post("/delete_user/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(...)
):
    return await user_controller.delete_user(db=db, user_id=user_id, authorization=authorization)

@router.post("/delete_account", response_model=UserResponse)
async def delete_own_account(
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(...)
):
    return await user_controller.delete_own_account(db=db, authorization=authorization)