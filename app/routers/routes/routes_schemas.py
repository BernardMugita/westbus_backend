from pydantic import BaseModel, ConfigDict
from typing import Optional


class RouteCreate(BaseModel):
    route_name: str
    stop_order: Optional[str] = None
    distance_km: Optional[float] = None
    estimated_duration_min: Optional[int] = None
    is_active: Optional[bool] = None


class RouteUpdate(BaseModel):
    route_name: Optional[str] = None
    stop_order: Optional[str] = None
    distance_km: Optional[float] = None
    estimated_duration_min: Optional[int] = None
    is_active: Optional[bool] = None


class RouteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
