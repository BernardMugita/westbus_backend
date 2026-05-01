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

class PolicyType(str, Enum):
    COMPREHENSIVE = "Comprehensive"
    THIRD_PARTY = "Third-party"
    PSV = "PSV"
    
class InsuranceStatus(str, Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"

class InsurancePolicy(Base):
    __tablename__ = "insurance_policies"

    insurance_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    vehicle_id: Mapped[str] = mapped_column(String(36), ForeignKey("vehicles.vehicle_id"), nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    policy_type: Mapped[PolicyType] = mapped_column(SqlEnum(PolicyType), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    premium_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[InsuranceStatus] = mapped_column(SqlEnum(InsuranceStatus), default=InsuranceStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat, onupdate=now_eat)