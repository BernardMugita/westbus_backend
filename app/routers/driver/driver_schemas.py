from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional


class DriverCreate(BaseModel):
    name: str
    license_number: str
    phone: Optional[str] = None
    hire_date: Optional[datetime] = None
    status: Optional[str] = None


class DriverUpdate(BaseModel):
    name: Optional[str] = None
    license_number: Optional[str] = None
    phone: Optional[str] = None
    hire_date: Optional[datetime] = None
    status: Optional[str] = None


class DriverResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
