from pydantic import BaseModel, ConfigDict
from typing import Optional


class TripCreate(BaseModel):
    vehicle_id: str
    driver_id: str
    route_id: str
    start_time: str
    end_time: Optional[str] = None
    expected_duration_min: Optional[int] = None
    distance_km: Optional[float] = None
    status: Optional[str] = None


class TripUpdate(BaseModel):
    vehicle_id: Optional[str] = None
    driver_id: Optional[str] = None
    route_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    expected_duration_min: Optional[int] = None
    distance_km: Optional[float] = None
    status: Optional[str] = None


class TripResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
