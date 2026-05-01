from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.maintenance_records.maintenance_model import MaintenanceRecord
from app.routers.maintenance_records.maintenance_records_schemas import MaintenanceRecordCreate, MaintenanceRecordUpdate, MaintenanceRecordResponse
from app.routers.core.middlewares import requires_auth, requires_admin


class MaintenanceRecordController:
    def __init__(self):
        pass

    @requires_admin
    async def create_maintenance_records(self, db: AsyncSession, data: MaintenanceRecordCreate, authorization: str = Header(...), **kwargs) -> MaintenanceRecordResponse:
        """
        Create a new MaintenanceRecord record. Admin only.
        Args:
            db (AsyncSession): Database session
            data (MaintenanceRecordCreate): MaintenanceRecord data
            authorization (str): Bearer token
        Returns:
            MaintenanceRecordResponse
        """
        try:
            record = MaintenanceRecord(**data.model_dump())
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return MaintenanceRecordResponse(status="success", message="MaintenanceRecord created successfully", payload=record.__dict__)
        except HTTPException as e:
            return MaintenanceRecordResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=MaintenanceRecordResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_all_maintenance_records(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> MaintenanceRecordResponse:
        """
        Get all MaintenanceRecord records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            MaintenanceRecordResponse
        """
        try:
            result = await db.execute(select(MaintenanceRecord))
            records = result.scalars().all()
            return MaintenanceRecordResponse(
                status="success",
                message="MaintenanceRecords retrieved successfully",
                payload=[r.__dict__ for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=MaintenanceRecordResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_maintenance_records(self, db: AsyncSession, maintenance_id: str, authorization: str = Header(...), **kwargs) -> MaintenanceRecordResponse:
        """
        Get a single MaintenanceRecord by ID.
        Args:
            db (AsyncSession): Database session
            maintenance_id (str): MaintenanceRecord primary key
            authorization (str): Bearer token
        Returns:
            MaintenanceRecordResponse
        """
        try:
            result = await db.execute(select(MaintenanceRecord).where(MaintenanceRecord.maintenance_id == maintenance_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MaintenanceRecord not found")
            return MaintenanceRecordResponse(status="success", message="MaintenanceRecord retrieved successfully", payload=record.__dict__)
        except HTTPException as e:
            return MaintenanceRecordResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=MaintenanceRecordResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_maintenance_records(self, db: AsyncSession, maintenance_id: str, data: MaintenanceRecordUpdate, authorization: str = Header(...), **kwargs) -> MaintenanceRecordResponse:
        """
        Update a MaintenanceRecord record. Admin only.
        Args:
            db (AsyncSession): Database session
            maintenance_id (str): MaintenanceRecord primary key
            data (MaintenanceRecordUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            MaintenanceRecordResponse
        """
        try:
            result = await db.execute(select(MaintenanceRecord).where(MaintenanceRecord.maintenance_id == maintenance_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MaintenanceRecord not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return MaintenanceRecordResponse(status="success", message="MaintenanceRecord updated successfully", payload=record.__dict__)
        except HTTPException as e:
            return MaintenanceRecordResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=MaintenanceRecordResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_maintenance_records(self, db: AsyncSession, maintenance_id: str, authorization: str = Header(...), **kwargs) -> MaintenanceRecordResponse:
        """
        Delete a MaintenanceRecord record. Admin only.
        Args:
            db (AsyncSession): Database session
            maintenance_id (str): MaintenanceRecord primary key
            authorization (str): Bearer token
        Returns:
            MaintenanceRecordResponse
        """
        try:
            result = await db.execute(select(MaintenanceRecord).where(MaintenanceRecord.maintenance_id == maintenance_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MaintenanceRecord not found")
            await db.delete(record)
            await db.commit()
            return MaintenanceRecordResponse(status="success", message="MaintenanceRecord deleted successfully")
        except HTTPException as e:
            return MaintenanceRecordResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=MaintenanceRecordResponse(status="error", message=str(e)).model_dump()
            )
