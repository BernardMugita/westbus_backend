from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional


class LoanRepaymentCreate(BaseModel):
    loan_id: str
    payment_date: datetime
    amount_paid: float
    principal_portion: float
    interest_portion: float
    # outstanding_balance: Optional[float]
    receipt_ref: Optional[str] = None


class LoanRepaymentUpdate(BaseModel):
    loan_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    amount_paid: Optional[float] = None
    principal_portion: Optional[float] = None
    interest_portion: Optional[float] = None
    outstanding_balance: Optional[float] = None
    receipt_ref: Optional[str] = None


class LoanRepaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
