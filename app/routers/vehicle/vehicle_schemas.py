from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class VehicleCreate(BaseModel):
    registration_number: str
    model: str
    capacity: int
    status: Optional[str] = None
    purchase_date: Optional[datetime] = None
    license_expiry: Optional[datetime] = None


class VehicleUpdate(BaseModel):
    registration_number: Optional[str] = None
    model: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = None
    purchase_date: Optional[str] = None
    license_expiry: Optional[str] = None


class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
