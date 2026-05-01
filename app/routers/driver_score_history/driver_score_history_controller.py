from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.driver_score_history.history_model import DriverScoreHistory
from app.routers.driver_score_history.driver_score_history_schemas import DriverScoreHistoryCreate, DriverScoreHistoryUpdate, DriverScoreHistoryResponse
from app.routers.core.middlewares import requires_auth, requires_admin


class DriverScoreHistoryController:
    def __init__(self):
        pass

    @requires_admin
    async def create_driver_score_history(self, db: AsyncSession, data: DriverScoreHistoryCreate, authorization: str = Header(...), **kwargs) -> DriverScoreHistoryResponse:
        """
        Create a new DriverScoreHistory record. Admin only.
        Args:
            db (AsyncSession): Database session
            data (DriverScoreHistoryCreate): DriverScoreHistory data
            authorization (str): Bearer token
        Returns:
            DriverScoreHistoryResponse
        """
        try:
            record = DriverScoreHistory(**data.model_dump())
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return DriverScoreHistoryResponse(status="success", message="DriverScoreHistory created successfully", payload=record.__dict__)
        except HTTPException as e:
            return DriverScoreHistoryResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverScoreHistoryResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_all_driver_score_history(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> DriverScoreHistoryResponse:
        """
        Get all DriverScoreHistory records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            DriverScoreHistoryResponse
        """
        try:
            result = await db.execute(select(DriverScoreHistory))
            records = result.scalars().all()
            return DriverScoreHistoryResponse(
                status="success",
                message="DriverScoreHistorys retrieved successfully",
                payload=[r.__dict__ for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverScoreHistoryResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_driver_score_history(self, db: AsyncSession, score_id: str, authorization: str = Header(...), **kwargs) -> DriverScoreHistoryResponse:
        """
        Get a single DriverScoreHistory by ID.
        Args:
            db (AsyncSession): Database session
            score_id (str): DriverScoreHistory primary key
            authorization (str): Bearer token
        Returns:
            DriverScoreHistoryResponse
        """
        try:
            result = await db.execute(select(DriverScoreHistory).where(DriverScoreHistory.score_id == score_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DriverScoreHistory not found")
            return DriverScoreHistoryResponse(status="success", message="DriverScoreHistory retrieved successfully", payload=record.__dict__)
        except HTTPException as e:
            return DriverScoreHistoryResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverScoreHistoryResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_driver_score_history(self, db: AsyncSession, score_id: str, data: DriverScoreHistoryUpdate, authorization: str = Header(...), **kwargs) -> DriverScoreHistoryResponse:
        """
        Update a DriverScoreHistory record. Admin only.
        Args:
            db (AsyncSession): Database session
            score_id (str): DriverScoreHistory primary key
            data (DriverScoreHistoryUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            DriverScoreHistoryResponse
        """
        try:
            result = await db.execute(select(DriverScoreHistory).where(DriverScoreHistory.score_id == score_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DriverScoreHistory not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return DriverScoreHistoryResponse(status="success", message="DriverScoreHistory updated successfully", payload=record.__dict__)
        except HTTPException as e:
            return DriverScoreHistoryResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverScoreHistoryResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_driver_score_history(self, db: AsyncSession, score_id: str, authorization: str = Header(...), **kwargs) -> DriverScoreHistoryResponse:
        """
        Delete a DriverScoreHistory record. Admin only.
        Args:
            db (AsyncSession): Database session
            score_id (str): DriverScoreHistory primary key
            authorization (str): Bearer token
        Returns:
            DriverScoreHistoryResponse
        """
        try:
            result = await db.execute(select(DriverScoreHistory).where(DriverScoreHistory.score_id == score_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DriverScoreHistory not found")
            await db.delete(record)
            await db.commit()
            return DriverScoreHistoryResponse(status="success", message="DriverScoreHistory deleted successfully")
        except HTTPException as e:
            return DriverScoreHistoryResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverScoreHistoryResponse(status="error", message=str(e)).model_dump()
            )
