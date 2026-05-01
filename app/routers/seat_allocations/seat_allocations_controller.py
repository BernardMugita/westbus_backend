from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.seat_allocations.seats_model import SeatAllocation
from app.routers.seat_allocations.seat_allocations_schemas import SeatAllocationCreate, SeatAllocationUpdate, SeatAllocationResponse
from app.routers.core.middlewares import requires_auth, requires_admin


class SeatAllocationController:
    def __init__(self):
        pass

    @requires_admin
    async def create_seat_allocations(self, db: AsyncSession, data: SeatAllocationCreate, authorization: str = Header(...), **kwargs) -> SeatAllocationResponse:
        """
        Create a new SeatAllocation record. Admin only.
        Args:
            db (AsyncSession): Database session
            data (SeatAllocationCreate): SeatAllocation data
            authorization (str): Bearer token
        Returns:
            SeatAllocationResponse
        """
        try:
            record = SeatAllocation(**data.model_dump())
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return SeatAllocationResponse(status="success", message="SeatAllocation created successfully", payload=record.__dict__)
        except HTTPException as e:
            return SeatAllocationResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=SeatAllocationResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_all_seat_allocations(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> SeatAllocationResponse:
        """
        Get all SeatAllocation records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            SeatAllocationResponse
        """
        try:
            result = await db.execute(select(SeatAllocation))
            records = result.scalars().all()
            return SeatAllocationResponse(
                status="success",
                message="SeatAllocations retrieved successfully",
                payload=[r.__dict__ for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=SeatAllocationResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_seat_allocations(self, db: AsyncSession, seat_allocation_id: str, authorization: str = Header(...), **kwargs) -> SeatAllocationResponse:
        """
        Get a single SeatAllocation by ID.
        Args:
            db (AsyncSession): Database session
            seat_allocation_id (str): SeatAllocation primary key
            authorization (str): Bearer token
        Returns:
            SeatAllocationResponse
        """
        try:
            result = await db.execute(select(SeatAllocation).where(SeatAllocation.seat_allocation_id == seat_allocation_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SeatAllocation not found")
            return SeatAllocationResponse(status="success", message="SeatAllocation retrieved successfully", payload=record.__dict__)
        except HTTPException as e:
            return SeatAllocationResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=SeatAllocationResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_seat_allocations(self, db: AsyncSession, seat_allocation_id: str, data: SeatAllocationUpdate, authorization: str = Header(...), **kwargs) -> SeatAllocationResponse:
        """
        Update a SeatAllocation record. Admin only.
        Args:
            db (AsyncSession): Database session
            seat_allocation_id (str): SeatAllocation primary key
            data (SeatAllocationUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            SeatAllocationResponse
        """
        try:
            result = await db.execute(select(SeatAllocation).where(SeatAllocation.seat_allocation_id == seat_allocation_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SeatAllocation not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return SeatAllocationResponse(status="success", message="SeatAllocation updated successfully", payload=record.__dict__)
        except HTTPException as e:
            return SeatAllocationResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=SeatAllocationResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_seat_allocations(self, db: AsyncSession, seat_allocation_id: str, authorization: str = Header(...), **kwargs) -> SeatAllocationResponse:
        """
        Delete a SeatAllocation record. Admin only.
        Args:
            db (AsyncSession): Database session
            seat_allocation_id (str): SeatAllocation primary key
            authorization (str): Bearer token
        Returns:
            SeatAllocationResponse
        """
        try:
            result = await db.execute(select(SeatAllocation).where(SeatAllocation.seat_allocation_id == seat_allocation_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SeatAllocation not found")
            await db.delete(record)
            await db.commit()
            return SeatAllocationResponse(status="success", message="SeatAllocation deleted successfully")
        except HTTPException as e:
            return SeatAllocationResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=SeatAllocationResponse(status="error", message=str(e)).model_dump()
            )
