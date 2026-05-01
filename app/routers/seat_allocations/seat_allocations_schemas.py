from pydantic import BaseModel, ConfigDict
from typing import Optional


class SeatAllocationCreate(BaseModel):
    trip_id: str
    booking_id: Optional[str] = None
    seat_number: str
    status: Optional[str] = None


class SeatAllocationUpdate(BaseModel):
    trip_id: Optional[str] = None
    booking_id: Optional[str] = None
    seat_number: Optional[str] = None
    status: Optional[str] = None


class SeatAllocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
