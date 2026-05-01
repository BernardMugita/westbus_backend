from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class MaintenanceScheduleCreate(BaseModel):
    vehicle_id: str
    service_type: str
    interval_km: int
    interval_days: int
    last_done_km: Optional[int] = None
    last_done_date: Optional[datetime] = None
    status: Optional[str] = None


class MaintenanceScheduleUpdate(BaseModel):
    vehicle_id: Optional[str] = None
    service_type: Optional[str] = None
    interval_km: Optional[int] = None
    interval_days: Optional[int] = None
    last_done_km: Optional[int] = None
    last_done_date: Optional[datetime] = None
    status: Optional[str] = None


class MaintenanceScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
