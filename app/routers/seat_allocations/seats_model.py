from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Integer, Boolean, Enum as SqlEnum, ForeignKey, DateTime, Numeric, Text
from datetime import datetime, timezone, timedelta
from app.routers.core.models import Base
from decimal import Decimal
from enum import Enum
import uuid

EAT = timezone(timedelta(hours=3))

def now_eat():
    return datetime.now(EAT)

def gen_uuid():
    return str(uuid.uuid4())

class SeatStatus(str, Enum):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    OCCUPIED = "Occupied"
    CANCELLED = "Cancelled"

class SeatAllocation(Base):
    __tablename__ = "seat_allocations"

    seat_allocation_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    trip_id: Mapped[str] = mapped_column(String(36), ForeignKey("trips.trip_id"), nullable=False)
    booking_id: Mapped[str] = mapped_column(String(36), ForeignKey("bookings.booking_id"), nullable=True)
    seat_number: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[SeatStatus] = mapped_column(SqlEnum(SeatStatus), default=SeatStatus.AVAILABLE)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat, onupdate=now_eat)

    def to_dict(self):
        return {
            "seat_allocation_id": self.seat_allocation_id,
            "trip_id": self.trip_id,
            "booking_id": self.booking_id,
            "seat_number": self.seat_number,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }