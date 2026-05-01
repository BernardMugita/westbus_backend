from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.maintenance_schedules.schedules_model import MaintenanceSchedule
from app.routers.maintenance_schedules.maintenance_schedules_schemas import MaintenanceScheduleCreate, MaintenanceScheduleUpdate, MaintenanceScheduleResponse
from app.config.core.middlewares import requires_auth, requires_admin


class MaintenanceScheduleController:
    def __init__(self):
        pass

    @requires_admin
    async def create_maintenance_schedules(self, db: AsyncSession, data: MaintenanceScheduleCreate, authorization: str = Header(...), **kwargs) -> MaintenanceScheduleResponse:
        """
        Create a new MaintenanceSchedule record. Admin only.
        Args:
            db (AsyncSession): Database session
            data (MaintenanceScheduleCreate): MaintenanceSchedule data
            authorization (str): Bearer token
        Returns:
            MaintenanceScheduleResponse
        """
        try:
            record = MaintenanceSchedule(
                vehicle_id=data.vehicle_id,
                service_type=data.service_type,
                interval_km=data.interval_km,
                interval_days=data.interval_days,
                last_done_km=data.last_done_km,
                last_done_date=data.last_done_date,
                status=data.status
            )
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return MaintenanceScheduleResponse(status="success", message="MaintenanceSchedule created successfully", payload=record.to_dict())
        except HTTPException as e:
            return MaintenanceScheduleResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=MaintenanceScheduleResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_all_maintenance_schedules(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> MaintenanceScheduleResponse:
        """
        Get all MaintenanceSchedule records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            MaintenanceScheduleResponse
        """
        try:
            result = await db.execute(select(MaintenanceSchedule))
            records = result.scalars().all()
            return MaintenanceScheduleResponse(
                status="success",
                message="MaintenanceSchedules retrieved successfully",
                payload=[r.to_dict() for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=MaintenanceScheduleResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_maintenance_schedules(self, db: AsyncSession, schedule_id: str, authorization: str = Header(...), **kwargs) -> MaintenanceScheduleResponse:
        """
        Get a single MaintenanceSchedule by ID.
        Args:
            db (AsyncSession): Database session
            schedule_id (str): MaintenanceSchedule primary key
            authorization (str): Bearer token
        Returns:
            MaintenanceScheduleResponse
        """
        try:
            result = await db.execute(select(MaintenanceSchedule).where(MaintenanceSchedule.schedule_id == schedule_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MaintenanceSchedule not found")
            return MaintenanceScheduleResponse(status="success", message="MaintenanceSchedule retrieved successfully", payload=record.to_dict())
        except HTTPException as e:
            return MaintenanceScheduleResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=MaintenanceScheduleResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_maintenance_schedules(self, db: AsyncSession, schedule_id: str, data: MaintenanceScheduleUpdate, authorization: str = Header(...), **kwargs) -> MaintenanceScheduleResponse:
        """
        Update a MaintenanceSchedule record. Admin only.
        Args:
            db (AsyncSession): Database session
            schedule_id (str): MaintenanceSchedule primary key
            data (MaintenanceScheduleUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            MaintenanceScheduleResponse
        """
        try:
            result = await db.execute(select(MaintenanceSchedule).where(MaintenanceSchedule.schedule_id == schedule_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MaintenanceSchedule not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return MaintenanceScheduleResponse(status="success", message="MaintenanceSchedule updated successfully", payload=record.to_dict())
        except HTTPException as e:
            return MaintenanceScheduleResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=MaintenanceScheduleResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_maintenance_schedules(self, db: AsyncSession, schedule_id: str, authorization: str = Header(...), **kwargs) -> MaintenanceScheduleResponse:
        """
        Delete a MaintenanceSchedule record. Admin only.
        Args:
            db (AsyncSession): Database session
            schedule_id (str): MaintenanceSchedule primary key
            authorization (str): Bearer token
        Returns:
            MaintenanceScheduleResponse
        """
        try:
            result = await db.execute(select(MaintenanceSchedule).where(MaintenanceSchedule.schedule_id == schedule_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MaintenanceSchedule not found")
            await db.delete(record)
            await db.commit()
            return MaintenanceScheduleResponse(status="success", message="MaintenanceSchedule deleted successfully")
        except HTTPException as e:
            return MaintenanceScheduleResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=MaintenanceScheduleResponse(status="error", message=str(e)).model_dump()
            )
