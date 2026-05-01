from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional


class DriverAssignmentCreate(BaseModel):
    driver_id: str
    vehicle_id: str
    start_date: datetime
    end_date: Optional[datetime] = None
    is_current: Optional[bool] = None
 

class DriverAssignmentUpdate(BaseModel):
    driver_id: Optional[str] = None
    vehicle_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: Optional[bool] = None


class DriverAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
