from sqlalchemy.orm import Mapped, mapped_column
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

class Route(Base):
    __tablename__ = "routes"

    route_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    route_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    stop_order: Mapped[str] = mapped_column(Text, nullable=True)
    distance_km: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=True)
    estimated_duration_min: Mapped[int] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat, onupdate=now_eat)

    def to_dict(self):
        return {
            "route_id": self.route_id,
            "route_name": self.route_name,
            "stop_order": self.stop_order,
            "distance_km": float(self.distance_km) if self.distance_km is not None else None,
            "estimated_duration_min": self.estimated_duration_min,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }