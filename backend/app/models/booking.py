from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Numeric, func, Date, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from ..database import Base

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    discount_type = Column(String(20)) # percentage, fixed, flat
    discount_value = Column(Numeric(10, 2), nullable=False)
    min_order_amount = Column(Numeric(10, 2), default=0)
    max_discount_amount = Column(Numeric(10, 2))
    valid_from = Column(Date, default=func.current_date())
    valid_to = Column(Date)
    usage_limit = Column(Integer)
    used_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class TimeSlot(Base):
    __tablename__ = "time_slots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, nullable=False)
    slot_time = Column(String(50), nullable=False)
    total_capacity = Column(Integer, default=10)
    booked_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())


class ServiceCenter(Base):
    __tablename__ = "service_centers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    address_line1 = Column(String(200))
    address_line2 = Column(String(200))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    phone = Column(String(20))
    email = Column(String(100))
    operating_hours = Column(JSONB)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_number = Column(String(50), unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    device_brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id"))
    device_model_id = Column(UUID(as_uuid=True), ForeignKey("device_models.id"))
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"))
    service_pricing_id = Column(UUID(as_uuid=True), ForeignKey("service_pricing.id"))

    # Device details
    device_storage = Column(String(50))
    device_color = Column(String(50))
    device_purchase_date = Column(Date)
    is_under_warranty = Column(Boolean, default=False)
    device_condition_description = Column(Text)
    device_photos = Column(JSONB, default=list)

    # Pricing details (snapshot)
    selected_part_grade = Column(String(20))
    quoted_part_cost = Column(Numeric(10, 2))
    quoted_labor_cost = Column(Numeric(10, 2))
    quoted_subtotal = Column(Numeric(10, 2))
    discount_amount = Column(Numeric(10, 2), default=0)
    coupon_code = Column(String(50))
    final_price = Column(Numeric(10, 2))

    # Scheduling
    preferred_date = Column(Date)
    preferred_time_slot = Column(String(50))
    estimated_duration_minutes = Column(Integer)
    actual_start_time = Column(DateTime)
    actual_end_time = Column(DateTime)

    # Location
    service_location = Column(String(20)) # doorstep, service_center
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id", ondelete="SET NULL"))
    full_address_snapshot = Column(JSONB)

    # Assignment
    technician_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    assigned_at = Column(DateTime)

    # Status tracking
    status = Column(String(50), default="pending")
    payment_status = Column(String(50), default="pending")
    payment_method = Column(String(50))

    # Safety & Insurance
    data_backup_requested = Column(Boolean, default=False)
    privacy_agreement_signed = Column(Boolean, default=False)
    device_insurance_opted = Column(Boolean, default=False)
    insurance_premium = Column(Numeric(10, 2))
    insurance_coverage_amount = Column(Numeric(10, 2))

    # Notes
    customer_notes = Column(Text)
    technician_notes = Column(Text)
    admin_notes = Column(Text)

    # Cancellation
    cancelled_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    cancellation_reason = Column(Text)
    cancelled_at = Column(DateTime)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    confirmed_at = Column(DateTime)
    completed_at = Column(DateTime)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="bookings")
    device_brand = relationship("Brand")
    device_model = relationship("DeviceModel")
    service = relationship("Service")
    service_pricing = relationship("ServicePricing")
    address = relationship("Address", foreign_keys=[address_id])
    cancelled_by_user = relationship("User", foreign_keys=[cancelled_by])
    technician = relationship("User", foreign_keys=[technician_id])
