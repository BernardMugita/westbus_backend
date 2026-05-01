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

class ClaimStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    
class InsuranceClaim(Base):
    __tablename__ = "insurance_claims"

    claim_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    insurance_id: Mapped[str] = mapped_column(String(36), ForeignKey("insurance_policies.insurance_id"), nullable=False)
    incident_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    claim_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    amount_claimed: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    amount_approved: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)
    status: Mapped[ClaimStatus] = mapped_column(SqlEnum(ClaimStatus), default=ClaimStatus.PENDING)
    repair_estimate: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_eat)
    
    def to_dict(self):
        return {
            "claim_id": self.claim_id,
            "insurance_id": self.insurance_id,
            "incident_date": self.incident_date.isoformat(),
            "claim_date": self.claim_date.isoformat(),
            "amount_claimed": float(self.amount_claimed),
            "amount_approved": float(self.amount_approved) if self.amount_approved is not None else None,
            "status": self.status.value,
            "repair_estimate": float(self.repair_estimate) if self.repair_estimate is not None else None,
            "created_at": self.created_at.isoformat(),
        }
