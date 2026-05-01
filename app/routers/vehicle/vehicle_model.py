from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Enum as SqlEnum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime, timezone, timedelta
from app.config.core.models import Base
from enum import Enum
from typing import Optional
import uuid

EAT = timezone(timedelta(hours=3))

def now_eat():
    return datetime.now(EAT)

def gen_uuid():
    return str(uuid.uuid4())

class VehicleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    MAINTENANCE = "MAINTENANCE"
    RETIRED = "RETIRED"

class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    images: Mapped[Optional[list]] = mapped_column(ARRAY(String), nullable=True)
    registration_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[VehicleStatus] = mapped_column(SqlEnum(VehicleStatus), default=VehicleStatus.ACTIVE)
    purchase_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    license_expiry: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat, onupdate=now_eat)

    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "images": self.images or [],
            "registration_number": self.registration_number,
            "model": self.model,
            "capacity": self.capacity,
            "status": self.status.value,
            "purchase_date": self.purchase_date.isoformat() if self.purchase_date else None,
            "license_expiry": self.license_expiry.isoformat() if self.license_expiry else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }