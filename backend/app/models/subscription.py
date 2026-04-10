from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Numeric, func, Date, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from ..database import Base

class ProtectionPlan(Base):
    __tablename__ = "protection_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    discounted_price = Column(Numeric(10, 2))
    duration_months = Column(Integer, default=12)
    features = Column(JSONB, default=list) # List of strings
    is_popular = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    subscriptions = relationship("UserSubscription", back_populates="plan")


class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("protection_plans.id"), nullable=False)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="active") # active, expired, cancelled
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="subscriptions")
    plan = relationship("ProtectionPlan", back_populates="subscriptions")
