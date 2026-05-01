from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional


class InsurancePolicyCreate(BaseModel):
    vehicle_id: str
    provider: str
    policy_type: str
    start_date: datetime
    end_date: datetime
    premium_amount: float
    status: Optional[str] = None


class InsurancePolicyUpdate(BaseModel):
    vehicle_id: Optional[str] = None
    provider: Optional[str] = None
    policy_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    premium_amount: Optional[float] = None
    status: Optional[str] = None


class InsurancePolicyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
