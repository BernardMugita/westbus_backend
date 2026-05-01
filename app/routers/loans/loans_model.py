from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Integer, Boolean, Enum as SqlEnum, ForeignKey, DateTime, Numeric, Text
from datetime import datetime, timezone, timedelta
from app.config.core.models import Base
from decimal import Decimal
from enum import Enum
import uuid

EAT = timezone(timedelta(hours=3))

def now_eat():
    return datetime.now(EAT)

def gen_uuid():
    return str(uuid.uuid4())

class LoanStatus(str, Enum):
    ACTIVE = "Active"
    PAID = "Paid"
    DEFAULTED = "Defaulted"
    
class Loan(Base):
    __tablename__ = "loans"

    loan_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    vehicle_id: Mapped[str] = mapped_column(String(36), ForeignKey("vehicles.vehicle_id"), nullable=False)
    lender: Mapped[str] = mapped_column(String(100), nullable=False)
    principal_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    interest_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    total_payable: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    monthly_installment: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[LoanStatus] = mapped_column(SqlEnum(LoanStatus), default=LoanStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)

    def to_dict(self):
        return {
            "loan_id": self.loan_id,
            "vehicle_id": self.vehicle_id,
            "lender": self.lender,
            "principal_amount": float(self.principal_amount),
            "interest_rate": float(self.interest_rate),
            "total_payable": float(self.total_payable),
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "monthly_installment": float(self.monthly_installment),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }