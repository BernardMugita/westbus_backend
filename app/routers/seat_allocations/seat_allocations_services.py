from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.seat_allocations.seat_allocations_schemas import SeatAllocationCreate, SeatAllocationUpdate, SeatAllocationResponse
from app.routers.seat_allocations.seat_allocations_controller import SeatAllocationController

router = APIRouter(prefix="/seat-allocations", tags=["seat-allocations"])
controller = SeatAllocationController()


@router.post("/", response_model=SeatAllocationResponse)
async def create_seat_allocations(data: SeatAllocationCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_seat_allocations(db=db, data=data, authorization=authorization)


@router.get("/", response_model=SeatAllocationResponse)
async def get_all_seat_allocations(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_seat_allocations(db=db, authorization=authorization)


@router.get("/{seat_allocation_id}", response_model=SeatAllocationResponse)
async def get_seat_allocations(seat_allocation_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_seat_allocations(db=db, seat_allocation_id=seat_allocation_id, authorization=authorization)


@router.patch("/{seat_allocation_id}", response_model=SeatAllocationResponse)
async def update_seat_allocations(seat_allocation_id: str, data: SeatAllocationUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_seat_allocations(db=db, seat_allocation_id=seat_allocation_id, data=data, authorization=authorization)


@router.delete("/{seat_allocation_id}", response_model=SeatAllocationResponse)
async def delete_seat_allocations(seat_allocation_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_seat_allocations(db=db, seat_allocation_id=seat_allocation_id, authorization=authorization)
