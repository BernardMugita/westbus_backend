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

class MaintenanceScheduleStatus(str, Enum):
    UPCOMING = "Upcoming"
    OVERDUE = "Overdue"
    DONE = "Done"
    
class MaintenanceSchedule(Base):
    __tablename__ = "maintenance_schedules"

    schedule_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    vehicle_id: Mapped[str] = mapped_column(String(36), ForeignKey("vehicles.vehicle_id"), nullable=False)
    service_type: Mapped[str] = mapped_column(String(100), nullable=False)
    interval_km: Mapped[int] = mapped_column(Integer, nullable=False)
    interval_days: Mapped[int] = mapped_column(Integer, nullable=False)
    last_done_km: Mapped[int] = mapped_column(Integer, nullable=True)
    last_done_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[MaintenanceScheduleStatus] = mapped_column(SqlEnum(MaintenanceScheduleStatus), default=MaintenanceScheduleStatus.UPCOMING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat, onupdate=now_eat)
    
    def to_dict(self):
        return {
            "schedule_id": self.schedule_id,
            "vehicle_id": self.vehicle_id,
            "service_type": self.service_type,
            "interval_km": self.interval_km,
            "interval_days": self.interval_days,
            "last_done_km": self.last_done_km,
            "last_done_date": self.last_done_date.isoformat() if self.last_done_date else None,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }