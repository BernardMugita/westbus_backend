from pydantic import BaseModel, ConfigDict
from typing import Optional


class InsuranceClaimCreate(BaseModel):
    insurance_id: str
    incident_date: str
    claim_date: str
    amount_claimed: float
    amount_approved: Optional[float] = None
    status: Optional[str] = None
    repair_estimate: Optional[float] = None


class InsuranceClaimUpdate(BaseModel):
    insurance_id: Optional[str] = None
    incident_date: Optional[str] = None
    claim_date: Optional[str] = None
    amount_claimed: Optional[float] = None
    amount_approved: Optional[float] = None
    status: Optional[str] = None
    repair_estimate: Optional[float] = None


class InsuranceClaimResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
