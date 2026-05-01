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

class VehicleStatus(str, Enum):
    ACTIVE = "Active"
    MAINTENANCE = "Maintenance"
    RETIRED = "Retired"

class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    registration_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[VehicleStatus] = mapped_column(SqlEnum(VehicleStatus), default=VehicleStatus.ACTIVE)
    purchase_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    license_expiry: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat, onupdate=now_eat)
    
    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "registration_number": self.registration_number,
            "model": self.model,
            "capacity": self.capacity,
            "status": self.status.value,
            "purchase_date": self.purchase_date.isoformat() if self.purchase_date else None,
            "license_expiry": self.license_expiry.isoformat() if self.license_expiry else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }