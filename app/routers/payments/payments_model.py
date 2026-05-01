from sqlalchemy.orm import Mapped, mapped_column
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

class PaymentMethod(str, Enum):
    CASH = "Cash"
    MPESA = "M-Pesa"
    BANK = "Bank"
    CARD = "Card"
    OTHER = "Other"

class PaymentStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"

class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    booking_id: Mapped[str] = mapped_column(String(36), ForeignKey("bookings.booking_id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(SqlEnum(PaymentMethod), nullable=False)
    payment_status: Mapped[PaymentStatus] = mapped_column(SqlEnum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_ref: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "booking_id": self.booking_id,
            "amount": float(self.amount),
            "payment_method": self.payment_method.value,
            "payment_status": self.payment_status.value,
            "transaction_ref": self.transaction_ref,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "created_at": self.created_at.isoformat(),
        }