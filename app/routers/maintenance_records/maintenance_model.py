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

class MaintenanceType(str, Enum):
    OIL_CHANGE = "Oil change"
    BRAKE_PAD = "Brake pad"
    TYRE = "Tyre"
    ENGINE = "Engine"
    ELECTRICAL = "Electrical"
    OTHER = "Other"

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    maintenance_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    vehicle_id: Mapped[str] = mapped_column(String(36), ForeignKey("vehicles.vehicle_id"), nullable=False)
    driver_id: Mapped[str] = mapped_column(String(36), ForeignKey("drivers.driver_id"), nullable=True)
    maintenance_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    type: Mapped[MaintenanceType] = mapped_column(SqlEnum(MaintenanceType), nullable=False)
    cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    odometer_km: Mapped[int] = mapped_column(Integer, nullable=True)
    garage_name: Mapped[str] = mapped_column(String(100), nullable=True)
    next_due_km: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)

    def to_dict(self):
        return {
            "maintenance_id": self.maintenance_id,
            "vehicle_id": self.vehicle_id,
            "driver_id": self.driver_id,
            "maintenance_date": self.maintenance_date.isoformat(),
            "type": self.type.value,
            "cost": float(self.cost),
            "odometer_km": self.odometer_km,
            "garage_name": self.garage_name,
            "next_due_km": self.next_due_km,
            "created_at": self.created_at.isoformat(),
        }