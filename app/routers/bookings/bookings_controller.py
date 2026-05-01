from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.bookings.bookings_model import Booking
from app.routers.bookings.bookings_schemas import BookingCreate, BookingUpdate, BookingResponse
from app.config.core.middlewares import requires_auth, requires_admin


class BookingController:
    def __init__(self):
        pass

    @requires_admin
    async def create_bookings(self, db: AsyncSession, data: BookingCreate, authorization: str = Header(...), **kwargs) -> BookingResponse:
        """
        Create a new Booking record. Admin only.
        Args:
            db (AsyncSession): Database session
            data (BookingCreate): Booking data
            authorization (str): Bearer token
        Returns:
            BookingResponse
        """
        try:
            record = Booking(**data.model_dump())
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return BookingResponse(status="success", message="Booking created successfully", payload=record.__dict__)
        except HTTPException as e:
            return BookingResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=BookingResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_all_bookings(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> BookingResponse:
        """
        Get all Booking records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            BookingResponse
        """
        try:
            result = await db.execute(select(Booking))
            records = result.scalars().all()
            return BookingResponse(
                status="success",
                message="Bookings retrieved successfully",
                payload=[r.__dict__ for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=BookingResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_bookings(self, db: AsyncSession, booking_id: str, authorization: str = Header(...), **kwargs) -> BookingResponse:
        """
        Get a single Booking by ID.
        Args:
            db (AsyncSession): Database session
            booking_id (str): Booking primary key
            authorization (str): Bearer token
        Returns:
            BookingResponse
        """
        try:
            result = await db.execute(select(Booking).where(Booking.booking_id == booking_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
            return BookingResponse(status="success", message="Booking retrieved successfully", payload=record.__dict__)
        except HTTPException as e:
            return BookingResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=BookingResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_bookings(self, db: AsyncSession, booking_id: str, data: BookingUpdate, authorization: str = Header(...), **kwargs) -> BookingResponse:
        """
        Update a Booking record. Admin only.
        Args:
            db (AsyncSession): Database session
            booking_id (str): Booking primary key
            data (BookingUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            BookingResponse
        """
        try:
            result = await db.execute(select(Booking).where(Booking.booking_id == booking_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return BookingResponse(status="success", message="Booking updated successfully", payload=record.__dict__)
        except HTTPException as e:
            return BookingResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=BookingResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_bookings(self, db: AsyncSession, booking_id: str, authorization: str = Header(...), **kwargs) -> BookingResponse:
        """
        Delete a Booking record. Admin only.
        Args:
            db (AsyncSession): Database session
            booking_id (str): Booking primary key
            authorization (str): Bearer token
        Returns:
            BookingResponse
        """
        try:
            result = await db.execute(select(Booking).where(Booking.booking_id == booking_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
            await db.delete(record)
            await db.commit()
            return BookingResponse(status="success", message="Booking deleted successfully")
        except HTTPException as e:
            return BookingResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=BookingResponse(status="error", message=str(e)).model_dump()
            )
