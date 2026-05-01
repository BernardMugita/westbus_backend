from pydantic import BaseModel, ConfigDict
from typing import Optional


class DriverScoreHistoryCreate(BaseModel):
    driver_id: str
    period_start: str
    period_end: str
    score: float
    on_time_count: Optional[int] = None
    total_trips: Optional[int] = None
    fuel_overuse_ratio: Optional[float] = None
    revenue_efficiency: Optional[float] = None
    safety_flag: Optional[bool] = None


class DriverScoreHistoryUpdate(BaseModel):
    driver_id: Optional[str] = None
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    score: Optional[float] = None
    on_time_count: Optional[int] = None
    total_trips: Optional[int] = None
    fuel_overuse_ratio: Optional[float] = None
    revenue_efficiency: Optional[float] = None
    safety_flag: Optional[bool] = None


class DriverScoreHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
