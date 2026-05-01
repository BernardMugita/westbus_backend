from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.trips.trips_model import Trip
from app.routers.trips.trips_schemas import TripCreate, TripUpdate, TripResponse
from app.config.core.middlewares import requires_auth, requires_admin


class TripController:
    def __init__(self):
        pass

    @requires_admin
    async def create_trips(self, db: AsyncSession, data: TripCreate, authorization: str = Header(...), **kwargs) -> TripResponse:
        """
        Create a new Trip record. Admin only.
        Args:
            db (AsyncSession): Database session
            data (TripCreate): Trip data
            authorization (str): Bearer token
        Returns:
            TripResponse
        """
        try:
            record = Trip(
                vehicle_id=data.vehicle_id,
                driver_id=data.driver_id,
                route_id=data.route_id,
                start_time=data.start_time,
                end_time=data.end_time,
                expected_duration_min=data.expected_duration_min,
                distance_km=data.distance_km,
                status=data.status
            )
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return TripResponse(status="success", message="Trip created successfully", payload=record.to_dict())
        except HTTPException as e:
            return TripResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=TripResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_all_trips(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> TripResponse:
        """
        Get all Trip records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            TripResponse
        """
        try:
            result = await db.execute(select(Trip))
            records = result.scalars().all()
            return TripResponse(
                status="success",
                message="Trips retrieved successfully",
                payload=[r.to_dict() for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=TripResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_trips(self, db: AsyncSession, trip_id: str, authorization: str = Header(...), **kwargs) -> TripResponse:
        """
        Get a single Trip by ID.
        Args:
            db (AsyncSession): Database session
            trip_id (str): Trip primary key
            authorization (str): Bearer token
        Returns:
            TripResponse
        """
        try:
            result = await db.execute(select(Trip).where(Trip.trip_id == trip_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
            return TripResponse(status="success", message="Trip retrieved successfully", payload=record.to_dict())
        except HTTPException as e:
            return TripResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=TripResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_trips(self, db: AsyncSession, trip_id: str, data: TripUpdate, authorization: str = Header(...), **kwargs) -> TripResponse:
        """
        Update a Trip record. Admin only.
        Args:
            db (AsyncSession): Database session
            trip_id (str): Trip primary key
            data (TripUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            TripResponse
        """
        try:
            result = await db.execute(select(Trip).where(Trip.trip_id == trip_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return TripResponse(status="success", message="Trip updated successfully", payload=record.to_dict())
        except HTTPException as e:
            return TripResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=TripResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_trips(self, db: AsyncSession, trip_id: str, authorization: str = Header(...), **kwargs) -> TripResponse:
        """
        Delete a Trip record. Admin only.
        Args:
            db (AsyncSession): Database session
            trip_id (str): Trip primary key
            authorization (str): Bearer token
        Returns:
            TripResponse
        """
        try:
            result = await db.execute(select(Trip).where(Trip.trip_id == trip_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
            await db.delete(record)
            await db.commit()
            return TripResponse(status="success", message="Trip deleted successfully")
        except HTTPException as e:
            return TripResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=TripResponse(status="error", message=str(e)).model_dump()
            )
