from pydantic import BaseModel, HttpUrl
from uuid import UUID
from datetime import datetime
from typing import List, Optional, Any

class BrandBase(BaseModel):
    name: str
    logo_url: Optional[str] = None
    category: str = "smartphone"
    is_active: bool = True
    display_order: int = 999

class BrandCreate(BrandBase):
    pass

class Brand(BrandBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DeviceModelBase(BaseModel):
    brand_id: UUID
    model_name: str
    model_number: Optional[str] = None
    image_url: Optional[str] = None
    release_year: Optional[int] = None
    category: str = "smartphone"
    storage_variants: List[str] = []
    color_variants: List[str] = []
    original_price: Optional[float] = None
    is_active: bool = True
    is_popular: bool = False
    display_order: int = 999
    repair_complexity: Optional[int] = None
    avg_repair_time_minutes: int = 60

class DeviceModelCreate(DeviceModelBase):
    pass

class DeviceModel(DeviceModelBase):
    id: UUID
    brand: Optional[Brand] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
