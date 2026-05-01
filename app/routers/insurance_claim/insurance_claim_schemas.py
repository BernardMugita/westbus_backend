from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional


class InsuranceClaimCreate(BaseModel):
    insurance_id: str
    incident_date: datetime
    claim_date: datetime
    amount_claimed: float
    amount_approved: Optional[float] = None
    status: Optional[str] = None
    repair_estimate: Optional[float] = None


class InsuranceClaimUpdate(BaseModel):
    insurance_id: Optional[str] = None
    incident_date: Optional[datetime] = None
    claim_date: Optional[datetime] = None
    amount_claimed: Optional[float] = None
    amount_approved: Optional[float] = None
    status: Optional[str] = None
    repair_estimate: Optional[float] = None


class InsuranceClaimResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
