from pydantic import BaseModel, ConfigDict
from typing import Optional


class RevenueLedgerCreate(BaseModel):
    payment_id: Optional[str] = None
    booking_id: Optional[str] = None
    trip_id: str
    revenue_source: str
    amount: float
    revenue_type: str
    payment_method: Optional[str] = None
    transaction_ref: Optional[str] = None
    recorded_by: Optional[str] = None
    notes: Optional[str] = None


class RevenueLedgerUpdate(BaseModel):
    payment_id: Optional[str] = None
    booking_id: Optional[str] = None
    trip_id: Optional[str] = None
    revenue_source: Optional[str] = None
    amount: Optional[float] = None
    revenue_type: Optional[str] = None
    payment_method: Optional[str] = None
    transaction_ref: Optional[str] = None
    recorded_by: Optional[str] = None
    notes: Optional[str] = None


class RevenueLedgerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
