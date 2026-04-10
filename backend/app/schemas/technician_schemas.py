from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date
from typing import List, Optional
from .base import PaginationInfo

class TechnicianStatsResponse(BaseModel):
    total_assigned: int
    in_progress: int
    completed: int
    pending: int
    technician_name: str

class TechnicianBookingListItem(BaseModel):
    id: UUID
    booking_number: str
    customer_name: str
    customer_phone: str
    service_name: str
    brand_name: str
    model_name: str
    status: str
    final_price: float
    preferred_date: date
    preferred_time_slot: str
    service_location: str
    full_address_snapshot: Optional[dict] = None
    customer_notes: Optional[str] = None
    technician_notes: Optional[str] = None
    assigned_at: Optional[datetime] = None
    created_at: datetime

class TechnicianBookingListResponse(BaseModel):
    bookings: List[TechnicianBookingListItem]
    pagination: PaginationInfo

class TechnicianBookingDetailResponse(TechnicianBookingListItem):
    device_storage: Optional[str] = None
    device_color: Optional[str] = None
    device_condition_description: Optional[str] = None
    is_under_warranty: bool
    data_backup_requested: bool

class TechnicianCustomerListItem(BaseModel):
    id: UUID
    full_name: str
    phone: str
    email: Optional[str] = None
    status: str
    is_phone_verified: bool
    created_at: datetime
    total_bookings: int

class TechnicianCustomerListResponse(BaseModel):
    customers: List[TechnicianCustomerListItem]
    pagination: PaginationInfo
