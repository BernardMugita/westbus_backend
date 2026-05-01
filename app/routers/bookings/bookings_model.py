from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Integer, Boolean, Enum as SqlEnum, ForeignKey, DateTime, Numeric, Text
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from enum import Enum
import uuid
from app.routers.core.models import Base

EAT = timezone(timedelta(hours=3))

def now_eat():
    return datetime.now(EAT)

def gen_uuid():
    return str(uuid.uuid4())

class BookingType(str, Enum):
    ONLINE = "Online"
    AGENT = "Agent"
    PHYSICAL = "Physical"

class BookingStatus(str, Enum):
    RESERVED = "Reserved"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    
class Booking(Base):
    __tablename__ = "bookings"

    booking_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    trip_id: Mapped[str] = mapped_column(String(36), ForeignKey("trips.trip_id"), nullable=False)
    passenger_name: Mapped[str] = mapped_column(String(100), nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(20), nullable=True)
    seats_booked: Mapped[int] = mapped_column(Integer, nullable=False)
    booking_type: Mapped[BookingType] = mapped_column(SqlEnum(BookingType), default=BookingType.ONLINE)
    booking_status: Mapped[BookingStatus] = mapped_column(SqlEnum(BookingStatus), default=BookingStatus.RESERVED)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat, onupdate=now_eat)


    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "trip_id": self.trip_id,
            "passenger_name": self.passenger_name,
            "contact_phone": self.contact_phone,
            "seats_booked": self.seats_booked,
            "booking_type": self.booking_type.value,
            "booking_status": self.booking_status.value,
            "total_amount": float(self.total_amount),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }