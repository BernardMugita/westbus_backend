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

class DriverAssignment(Base):
    __tablename__ = "driver_assignments"

    assignment_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    driver_id: Mapped[str] = mapped_column(String(36), ForeignKey("drivers.driver_id"), nullable=False)
    vehicle_id: Mapped[str] = mapped_column(String(36), ForeignKey("vehicles.vehicle_id"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat, onupdate=now_eat)

    def to_dict(self):
        return {
            "assignment_id": self.assignment_id,
            "driver_id": self.driver_id,
            "vehicle_id": self.vehicle_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_current": self.is_current,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }