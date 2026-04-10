from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from ..database import Base

class Brand(Base):
    __tablename__ = "brands"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    logo_url = Column(String(500))
    category = Column(String(20), nullable=False, default="smartphone")
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=999)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    models = relationship("DeviceModel", back_populates="brand", cascade="all, delete-orphan")


class DeviceModel(Base):
    __tablename__ = "device_models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    model_name = Column(String(200), nullable=False)
    model_number = Column(String(100))
    image_url = Column(String(500))
    release_year = Column(Integer)
    category = Column(String(20), default="smartphone")
    storage_variants = Column(JSONB, default=list)
    color_variants = Column(JSONB, default=list)
    original_price = Column(Numeric(10, 2))
    is_active = Column(Boolean, default=True)
    is_popular = Column(Boolean, default=False)
    display_order = Column(Integer, default=999)
    repair_complexity = Column(Integer)
    avg_repair_time_minutes = Column(Integer, default=60)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    brand = relationship("Brand", back_populates="models")
    pricing = relationship("ServicePricing", back_populates="device_model", cascade="all, delete-orphan")
