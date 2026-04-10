from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date
from typing import List, Optional, Any

class CouponBase(BaseModel):
    code: str
    description: Optional[str] = None
    discount_type: str
    discount_value: float
    min_order_amount: float = 0
    max_discount_amount: Optional[float] = None
    valid_from: date
    valid_to: Optional[date] = None
    usage_limit: Optional[int] = None
    is_active: bool = True

class CouponCreate(CouponBase):
    pass

class Coupon(CouponBase):
    id: UUID
    used_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TimeSlotBase(BaseModel):
    date: date
    slot_time: str
    total_capacity: int = 10
    is_active: bool = True

class TimeSlot(TimeSlotBase):
    id: UUID
    booked_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class ServiceCenterBase(BaseModel):
    name: str
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    operating_hours: Optional[Any] = None
    is_active: bool = True

class ServiceCenter(ServiceCenterBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    device_brand_id: UUID
    device_model_id: UUID
    service_id: UUID
    service_pricing_id: UUID
    device_storage: Optional[str] = None
    device_color: Optional[str] = None
    device_purchase_date: Optional[date] = None
    is_under_warranty: bool = False
    device_condition_description: Optional[str] = None
    device_photos: List[str] = []
    selected_part_grade: Optional[str] = None
    coupon_code: Optional[str] = None
    preferred_date: date
    preferred_time_slot: str
    service_location: str
    address_id: Optional[UUID] = None
    data_backup_requested: bool = False
    privacy_agreement_signed: bool = False
    device_insurance_opted: bool = False
    customer_notes: Optional[str] = None
    payment_method: str

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: UUID
    booking_number: str
    user_id: Optional[UUID] = None
    quoted_part_cost: Optional[float] = None
    quoted_labor_cost: Optional[float] = None
    quoted_subtotal: Optional[float] = None
    discount_amount: float = 0
    final_price: Optional[float] = None
    estimated_duration_minutes: Optional[int] = None
    status: str
    payment_status: str
    full_address_snapshot: Optional[Any] = None
    technician_id: Optional[UUID] = None
    assigned_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookingListResponse(BaseModel):
    id: UUID
    booking_number: str
    service_name: str
    service_icon: str
    service_type: str
    brand_name: str
    model_name: str
    status: str
    final_price: float
    preferred_date: date
    preferred_time_slot: str
    service_location: str
    technician_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
