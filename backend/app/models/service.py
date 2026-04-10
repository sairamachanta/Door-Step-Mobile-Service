from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Numeric, func, Date, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from ..database import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = Column(String(200), nullable=False, unique=True)
    service_type = Column(String(50), nullable=False, default="general")
    description = Column(Text)
    icon_name = Column(String(50))
    icon_color = Column(String(7), default="#6366F1")
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=999)
    requires_parts = Column(Boolean, default=True)
    is_diagnostic = Column(Boolean, default=False)
    typical_symptoms = Column(JSONB, default=list)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    pricing = relationship("ServicePricing", back_populates="service", cascade="all, delete-orphan")


class ServicePricing(Base):
    __tablename__ = "service_pricing"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_model_id = Column(UUID(as_uuid=True), ForeignKey("device_models.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    part_name = Column(String(200))
    part_grade = Column(String(20)) # original, oem, aaa_plus, compatible, refurbished
    part_cost = Column(Numeric(10, 2), nullable=False, default=0)
    labor_cost = Column(Numeric(10, 2), nullable=False, default=0)
    # total_cost and discounted_price are generated columns in SQL
    final_price = Column(Numeric(10, 2), nullable=False, default=0)
    estimated_time_min = Column(Integer, default=30)
    estimated_time_max = Column(Integer, default=60)
    warranty_months = Column(Integer, default=6)
    is_doorstep_available = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    availability_status = Column(String(20), default="available")
    effective_from = Column(Date, default=func.current_date())
    effective_to = Column(Date)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    device_model = relationship("DeviceModel", back_populates="pricing")
    service = relationship("Service", back_populates="pricing")


class ServiceAddon(Base):
    __tablename__ = "service_addons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    icon_name = Column(String(50))
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=999)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
