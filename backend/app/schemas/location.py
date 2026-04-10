from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class AddressBase(BaseModel):
    label: Optional[str] = None
    address_line1: str
    address_line2: Optional[str] = None
    landmark: Optional[str] = None
    city: str
    state: str
    pincode: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: bool = False
    is_active: bool = True

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
