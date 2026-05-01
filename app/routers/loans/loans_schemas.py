from pydantic import BaseModel, ConfigDict
from typing import Optional


class LoanCreate(BaseModel):
    vehicle_id: str
    lender: str
    principal_amount: float
    interest_rate: float
    total_payable: float
    start_date: str
    end_date: str
    monthly_installment: float
    status: Optional[str] = None


class LoanUpdate(BaseModel):
    vehicle_id: Optional[str] = None
    lender: Optional[str] = None
    principal_amount: Optional[float] = None
    interest_rate: Optional[float] = None
    total_payable: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    monthly_installment: Optional[float] = None
    status: Optional[str] = None


class LoanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    message: str
    payload: Optional[dict | list] = None
