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

class DriverScoreHistory(Base):
    __tablename__ = "driver_score_history"

    score_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    driver_id: Mapped[str] = mapped_column(String(36), ForeignKey("drivers.driver_id"), nullable=False)
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    on_time_count: Mapped[int] = mapped_column(Integer, default=0)
    total_trips: Mapped[int] = mapped_column(Integer, default=0)
    fuel_overuse_ratio: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=True)
    revenue_efficiency: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=True)
    safety_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)

    def to_dict(self):
        return {
            "score_id": self.score_id,
            "driver_id": self.driver_id,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "score": float(self.score),
            "on_time_count": self.on_time_count,
            "total_trips": self.total_trips,
            "fuel_overuse_ratio": float(self.fuel_overuse_ratio) if self.fuel_overuse_ratio else None,
            "revenue_efficiency": float(self.revenue_efficiency) if self.revenue_efficiency else None,
            "safety_flag": self.safety_flag,
            "created_at": self.created_at.isoformat(),
        }