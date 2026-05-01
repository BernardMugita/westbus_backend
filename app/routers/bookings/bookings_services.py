from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.bookings.bookings_schemas import BookingCreate, BookingUpdate, BookingResponse
from app.routers.bookings.bookings_controller import BookingController

router = APIRouter(prefix="/bookings", tags=["bookings"])
controller = BookingController()


@router.post("/", response_model=BookingResponse)
async def create_bookings(data: BookingCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_bookings(db=db, data=data, authorization=authorization)


@router.get("/", response_model=BookingResponse)
async def get_all_bookings(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_bookings(db=db, authorization=authorization)


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_bookings(booking_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_bookings(db=db, booking_id=booking_id, authorization=authorization)


@router.patch("/{booking_id}", response_model=BookingResponse)
async def update_bookings(booking_id: str, data: BookingUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_bookings(db=db, booking_id=booking_id, data=data, authorization=authorization)


@router.delete("/{booking_id}", response_model=BookingResponse)
async def delete_bookings(booking_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_bookings(db=db, booking_id=booking_id, authorization=authorization)
