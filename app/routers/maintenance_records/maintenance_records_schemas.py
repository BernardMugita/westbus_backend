from pydantic import BaseModel, ConfigDict
from typing import Optional


class MaintenanceRecordCreate(BaseModel):
    vehicle_id: str
    driver_id: Optional[str] = None
    maintenance_date: str
    type: str
    cost: float
    odometer_km: Optional[int] = None
    garage_name: Optional[str] = None
    next_due_km: Optional[int] = None


class MaintenanceRecordUpdate(BaseModel):
    vehicle_id: Optional[str] = None
    driver_id: Optional[str] = None
    maintenance_date: Optional[str] = None
    type: Optional[str] = None
    cost: Optional[float] = None
    odometer_km: Optional[int] = None
    garage_name: Optional[str] = None
    next_due_km: Optional[int] = None


class MaintenanceRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
