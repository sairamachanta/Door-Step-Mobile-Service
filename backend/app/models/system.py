from sqlalchemy import Column, String, Boolean, DateTime, Integer, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from ..database import Base

class SystemMetadata(Base):
    """
    Stores categorical business values like roles, statuses, types.
    Allows changing labels, colors, and adding new options without code changes.
    """
    __tablename__ = "system_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String(50), nullable=False, index=True) # e.g., 'USER_ROLE', 'BOOKING_STATUS'
    code = Column(String(50), nullable=False, index=True) # e.g., 'admin', 'pending'
    label = Column(String(100), nullable=False) # e.g., 'Administrator', 'Waiting for Technician'
    
    # UI configuration for this value
    ui_config = Column(JSONB, default=dict) # e.g., {"color": "red", "icon": "shield"}
    
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class SystemSettings(Base):
    """
    Stores global application rules, limits, and configuration.
    """
    __tablename__ = "system_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(100), nullable=False, unique=True, index=True)
    value = Column(String, nullable=False)
    description = Column(String)
    data_type = Column(String(20), default="string") # string, int, float, bool, json
    
    is_public = Column(Boolean, default=True) # Whether it can be shared with frontend
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
