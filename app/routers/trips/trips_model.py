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

class TripStatus(str, Enum):
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    ONGOING = "Ongoing"


class Trip(Base):
    __tablename__ = "trips"

    trip_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    vehicle_id: Mapped[str] = mapped_column(String(36), ForeignKey("vehicles.vehicle_id"), nullable=False)
    driver_id: Mapped[str] = mapped_column(String(36), ForeignKey("drivers.driver_id"), nullable=False)
    route_id: Mapped[str] = mapped_column(String(36), ForeignKey("routes.route_id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    expected_duration_min: Mapped[int] = mapped_column(Integer, nullable=True)
    distance_km: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=True)
    status: Mapped[TripStatus] = mapped_column(SqlEnum(TripStatus), default=TripStatus.ONGOING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat, onupdate=now_eat)
    
    def to_dict(self):
        return {
            "trip_id": self.trip_id,
            "vehicle_id": self.vehicle_id,
            "driver_id": self.driver_id,
            "route_id": self.route_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "expected_duration_min": self.expected_duration_min,
            "distance_km": float(self.distance_km) if self.distance_km else None,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }