from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date
from typing import List, Optional, Any

class ServiceBase(BaseModel):
    service_name: str
    service_type: str = "general"
    description: Optional[str] = None
    icon_name: Optional[str] = None
    icon_color: str = "#6366F1"
    is_active: bool = True
    display_order: int = 999
    requires_parts: bool = True
    is_diagnostic: bool = False
    typical_symptoms: List[str] = []

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ServicePricingBase(BaseModel):
    device_model_id: UUID
    service_id: UUID
    part_name: Optional[str] = None
    part_grade: Optional[str] = None
    part_cost: float = 0
    labor_cost: float = 0
    final_price: float = 0
    estimated_time_min: int = 30
    estimated_time_max: int = 60
    warranty_months: int = 6
    is_doorstep_available: bool = True
    is_active: bool = True
    availability_status: str = "available"
    effective_from: date
    effective_to: Optional[date] = None

class ServicePricingCreate(ServicePricingBase):
    pass

class ServicePricing(ServicePricingBase):
    id: UUID
    service: Optional[Service] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ServiceAddonBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    icon_name: Optional[str] = None
    is_active: bool = True
    display_order: int = 999

class ServiceAddonCreate(ServiceAddonBase):
    pass

class ServiceAddon(ServiceAddonBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
