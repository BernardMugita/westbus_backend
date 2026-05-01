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

class LoanRepayment(Base):
    __tablename__ = "loan_repayments"

    repayment_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    loan_id: Mapped[str] = mapped_column(String(36), ForeignKey("loans.loan_id"), nullable=False)
    payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    amount_paid: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    principal_portion: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    interest_portion: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    outstanding_balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    receipt_ref: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)

    def to_dict(self):
        return {
            "repayment_id": self.repayment_id,
            "loan_id": self.loan_id,
            "payment_date": self.payment_date.isoformat(),
            "amount_paid": float(self.amount_paid),
            "principal_portion": float(self.principal_portion),
            "interest_portion": float(self.interest_portion),
            "outstanding_balance": float(self.outstanding_balance),
            "receipt_ref": self.receipt_ref,
            "created_at": self.created_at.isoformat(),
        }