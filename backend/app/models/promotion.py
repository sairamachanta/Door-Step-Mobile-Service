from sqlalchemy import Column, String, Integer, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database import Base

class Banner(Base):
    __tablename__ = "banners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_url = Column(String(500), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(500))
    cta_text = Column(String(50), default="Book Now")
    cta_link = Column(String(200), default="/booking/select-brand")
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
