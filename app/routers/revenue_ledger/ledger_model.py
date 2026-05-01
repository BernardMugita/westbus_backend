from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum as SqlEnum, ForeignKey, DateTime, Numeric, Text
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

class RevenueSource(str, Enum):
    BOOKING = "Booking"
    MANUAL = "Manual"
    ADJUSTMENT = "Adjustment"
    REFUND = "Refund"

class RevenueType(str, Enum):
    TICKET = "Ticket"
    CHARTER = "Charter"
    OTHER = "Other"

class PaymentMethod(str, Enum):
    CASH = "Cash"
    MPESA = "M-Pesa"
    BANK = "Bank"
    CARD = "Card"
    OTHER = "Other"

class RevenueLedger(Base):
    __tablename__ = "revenue_ledger"

    revenue_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    trip_id: Mapped[str] = mapped_column(String(36), ForeignKey("trips.trip_id"), nullable=False)
    revenue_source: Mapped[RevenueSource] = mapped_column(SqlEnum(RevenueSource), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    revenue_type: Mapped[RevenueType] = mapped_column(SqlEnum(RevenueType), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)
    recorded_by: Mapped[str] = mapped_column(String(100), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    def to_dict(self):
        return {
            "revenue_id": self.revenue_id,
            "trip_id": self.trip_id,
            "revenue_source": self.revenue_source.value,
            "amount": float(self.amount),
            "revenue_type": self.revenue_type.value,
            "recorded_at": self.recorded_at.isoformat(),
            "recorded_by": self.recorded_by,
            "notes": self.notes,
        }