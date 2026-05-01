from pydantic import BaseModel, ConfigDict
from typing import Optional


class ExpenseCreate(BaseModel):
    trip_id: str
    type: str
    amount: float
    receipt_image: Optional[str] = None
    incident_type: Optional[str] = None


class ExpenseUpdate(BaseModel):
    trip_id: Optional[str] = None
    type: Optional[str] = None
    amount: Optional[float] = None
    receipt_image: Optional[str] = None
    incident_type: Optional[str] = None


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
