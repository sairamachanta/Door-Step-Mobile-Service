from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date
from typing import List, Optional
from .base import PaginationInfo, GenericResponse

class AdminStatsResponse(BaseModel):
    total_customers: int
    total_technicians: int
    total_admins: int
    total_bookings: int
    pending_bookings: int
    active_bookings: int
    completed_bookings: int
    total_revenue: float
    total_suspended: int
    suspended_users: int
    suspended_technicians: int
    suspended_admins: int

class AdminUserListItem(BaseModel):
    id: UUID
    full_name: str
    phone: str
    email: Optional[str] = None
    role: str
    status: str
    is_protected: bool = False
    created_at: datetime
    total_bookings: int

    class Config:
        from_attributes = True

class AdminUserListResponse(BaseModel):
    users: List[AdminUserListItem]
    pagination: PaginationInfo

class AdminBookingListItem(BaseModel):
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
    technician_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AdminBookingListResponse(BaseModel):
    bookings: List[AdminBookingListItem]
    pagination: PaginationInfo

class AdminBookingAssignResponse(BaseModel):
    success: bool
    message: str
    booking_id: UUID
    technician_id: UUID
    technician_name: str
