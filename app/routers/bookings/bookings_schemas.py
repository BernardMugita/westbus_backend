from pydantic import BaseModel, ConfigDict
from typing import Optional


class BookingCreate(BaseModel):
    trip_id: str
    passenger_name: str
    contact_phone: Optional[str] = None
    seats_booked: int
    booking_type: Optional[str] = None
    booking_status: Optional[str] = None
    total_amount: float


class BookingUpdate(BaseModel):
    trip_id: Optional[str] = None
    passenger_name: Optional[str] = None
    contact_phone: Optional[str] = None
    seats_booked: Optional[int] = None
    booking_type: Optional[str] = None
    booking_status: Optional[str] = None
    total_amount: Optional[float] = None


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
