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

class ExpenseType(str, Enum):
    FUEL = "Fuel"
    TOLL = "Toll"
    MAINTENANCE = "Maintenance"
    FOOD = "Food"
    OTHER = "Other"

class Expense(Base):
    __tablename__ = "expenses"

    expense_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    trip_id: Mapped[str] = mapped_column(String(36), ForeignKey("trips.trip_id"), nullable=False)
    type: Mapped[ExpenseType] = mapped_column(SqlEnum(ExpenseType), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    receipt_image: Mapped[str] = mapped_column(String(255), nullable=True)
    incident_type: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)
    
    def to_dict(self):
        return {
            "expense_id": self.expense_id,
            "trip_id": self.trip_id,
            "type": self.type.value,
            "amount": float(self.amount),
            "receipt_image": self.receipt_image,
            "incident_type": self.incident_type,
            "created_at": self.created_at.isoformat(),
        }
