from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.auth.auth_model import User
from app.routers.users.user_schemas import UserResponse, UserUpdate
from app.routers.core.middlewares import requires_auth, requires_admin

class UserController:
    def __init__(self):
        pass

    @requires_admin
    async def get_all_users(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> UserResponse:
        """
        Get all users. Admin only.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token from request header
        Returns:
            UserResponse: List of all users
        """
        try:
            result = await db.execute(select(User))
            users = result.scalars().all()

            return UserResponse(
                status="success",
                message="Users retrieved successfully",
                payload=[user.to_dict() for user in users]
            )

        except HTTPException as e:
            return UserResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=UserResponse(
                    status="error",
                    message="Error fetching users",
                    payload=str(e)
                ).model_dump()
            )

    @requires_auth
    async def get_user(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> UserResponse:
        """
        Get current authenticated user by ID from token.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token from request header
        Returns:
            UserResponse: User data
        """
        try:
            token_payload = kwargs.get("token_payload")
            user_id = token_payload.get("user_id")

            result = await db.execute(select(User).where(User.user_id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            return UserResponse(status="success", message="User retrieved successfully", payload=user.to_dict())

        except HTTPException as e:
            return UserResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=UserResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def edit_user(self, db: AsyncSession, user_update: UserUpdate, authorization: str = Header(...), **kwargs) -> UserResponse:
        """
        Edit current authenticated user's account.
        Args:
            db (AsyncSession): Database session
            user_update (UserUpdate): Fields to update
            authorization (str): Bearer token from request header
        Returns:
            UserResponse: Updated user data
        """
        try:
            token_payload = kwargs.get("token_payload")
            user_id = token_payload.get("user_id")

            result = await db.execute(select(User).where(User.user_id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            update_data = user_update.model_dump(exclude_none=True)
            for field, value in update_data.items():
                setattr(user, field, value)

            await db.commit()
            await db.refresh(user)

            return UserResponse(status="success", message="User updated successfully", payload=user.to_dict())

        except HTTPException as e:
            return UserResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=UserResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_user(self, db: AsyncSession, user_id: str, authorization: str = Header(...), **kwargs) -> UserResponse:
        """
        Delete a user by ID. Admin only.
        Args:
            db (AsyncSession): Database session
            user_id (str): ID of user to delete
            authorization (str): Bearer token from request header
        Returns:
            UserResponse: Deletion confirmation
        """
        try:
            result = await db.execute(select(User).where(User.user_id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            await db.delete(user)
            await db.commit()

            return UserResponse(status="success", message="User deleted successfully")

        except HTTPException as e:
            return UserResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=UserResponse(status="error", message=str(e)).model_dump()
            )
    
    @requires_auth
    async def delete_own_account(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> UserResponse:
        """
        Delete the currently authenticated user's own account.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token from request header
        Returns:
            UserResponse: Deletion confirmation
        """
        try:
            token_payload = kwargs.get("token_payload")
            user_id = token_payload.get("user_id")

            result = await db.execute(select(User).where(User.user_id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            await db.delete(user)
            await db.commit()

            return UserResponse(status="success", message="Account deleted successfully")

        except HTTPException as e:
            return UserResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=UserResponse(status="error", message=str(e)).model_dump()
            )