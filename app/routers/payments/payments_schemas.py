from pydantic import BaseModel, ConfigDict
from typing import Optional


class PaymentCreate(BaseModel):
    booking_id: str
    amount: float
    payment_method: str
    payment_status: Optional[str] = None
    transaction_ref: Optional[str] = None
    paid_at: Optional[str] = None


class PaymentUpdate(BaseModel):
    booking_id: Optional[str] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    transaction_ref: Optional[str] = None
    paid_at: Optional[str] = None


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
