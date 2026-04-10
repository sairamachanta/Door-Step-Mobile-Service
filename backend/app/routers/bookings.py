from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
import uuid
from datetime import datetime, date

from ..database import get_db
from sqlalchemy.orm import joinedload
from ..models import Brand, DeviceModel, Service, ServicePricing, Booking, Address, TimeSlot, ServiceCenter, SystemMetadata, SystemSettings
from ..schemas.device import Brand as BrandSchema, DeviceModel as ModelSchema
from ..schemas.service import Service as ServiceSchema, ServicePricing as PricingSchema, ServiceAddon as AddonSchema
from ..schemas.booking import (
    Booking as BookingSchema, 
    BookingCreate, 
    TimeSlot as TimeSlotSchema, 
    ServiceCenter as ServiceCenterSchema,
    BookingListResponse as BookingListItem # Reusing for list
)
from app.schemas.admin_schemas import PaginationInfo
from pydantic import BaseModel
from ..utils.dependencies import get_current_active_user
from ..utils.metadata import MetadataHelper
from ..models import User

router = APIRouter(prefix="/api", tags=["Bookings"])

# --- Brands ---

@router.get("/brands", response_model=List[BrandSchema])
async def get_brands(
    category: Optional[str] = Query(None, regex="^(smartphone|feature_phone|both)$"),
    active_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    query = select(Brand)
    filters = []
    if active_only:
        filters.append(Brand.is_active == True)
    both_cat = await MetadataHelper.get_code_by_fallback(db, "DEVICE_CATEGORY", "both")
    if category:
        if category == both_cat:
            filters.append(Brand.category == both_cat)
        else:
            filters.append(or_(Brand.category == category, Brand.category == both_cat))
    
    if filters:
        query = query.where(and_(*filters))
    
    query = query.order_by(Brand.display_order.asc(), Brand.name.asc())
    
    result = await db.execute(query)
    return result.scalars().all()

# --- Models ---

@router.get("/models", response_model=List[ModelSchema])
async def get_models(
    brandId: Optional[uuid.UUID] = None,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    query = select(DeviceModel)
    filters = []
    if active_only:
        filters.append(DeviceModel.is_active == True)
    if brandId:
        filters.append(DeviceModel.brand_id == brandId)
        
    if filters:
        query = query.where(and_(*filters))
        
    query = query.order_by(
        DeviceModel.is_popular.desc(),
        DeviceModel.display_order.asc(),
        DeviceModel.release_year.desc()
    )
    
    result = await db.execute(query)
    return result.scalars().all()

# --- Services & Pricing ---

@router.get("/services/pricing", response_model=List[PricingSchema])
async def get_services_pricing(
    modelId: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    # Join Pricing with Services
    query = (
        select(ServicePricing)
        .join(Service, ServicePricing.service_id == Service.id)
        .where(
            and_(
                ServicePricing.device_model_id == modelId,
                ServicePricing.is_active == True,
                Service.is_active == True,
                ServicePricing.effective_from <= date.today(),
                or_(ServicePricing.effective_to == None, ServicePricing.effective_to >= date.today())
            )
        )
        .order_by(Service.service_type, Service.display_order)
    )
    
    result = await db.execute(query)
    pricing_list = result.scalars().all()
    
    # We need to ensure the service object is loaded for each pricing record
    # Since we are using join, we should probably use select(ServicePricing).options(joinedload(ServicePricing.service))
    # Let's adjust for efficiency
    from sqlalchemy.orm import joinedload
    query = query.options(joinedload(ServicePricing.service))
    result = await db.execute(query)
    return result.unique().scalars().all()

@router.get("/pricing/{pricingId}/details", response_model=PricingSchema)
async def get_pricing_details(
    pricingId: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy.orm import joinedload
    query = (
        select(ServicePricing)
        .options(
            joinedload(ServicePricing.service),
            joinedload(ServicePricing.device_model).joinedload(DeviceModel.brand)
        )
        .where(ServicePricing.id == pricingId)
    )
    
    result = await db.execute(query)
    pricing = result.unique().scalar_one_or_none()
    
    if not pricing:
        raise HTTPException(status_code=404, detail="Pricing record not found")
        
    return pricing

# --- Availability & Slots ---

@router.get("/availability", response_model=List[TimeSlotSchema])
async def get_availability(
    date_val: date = Query(..., alias="date"),
    db: AsyncSession = Depends(get_db)
):
    query = select(TimeSlot).where(and_(TimeSlot.date == date_val, TimeSlot.is_active == True))
    result = await db.execute(query)
    slots = result.scalars().all()
    
    # If no slots in DB for this date, we could generate default ones or return empty
    # For now, let's return what's in DB (seeded)
    return slots

@router.get("/service-centers", response_model=List[ServiceCenterSchema])
async def get_service_centers(
    city: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(ServiceCenter).where(ServiceCenter.is_active == True)
    if city:
        query = query.where(ServiceCenter.city == city)
    
    result = await db.execute(query)
    return result.scalars().all()

# --- Bookings ---

@router.post("/bookings/create", response_model=BookingSchema)
async def create_new_booking(
    booking_in: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Get the pricing snapshot
    pricing_query = select(ServicePricing).where(ServicePricing.id == booking_in.service_pricing_id)
    pricing_res = await db.execute(pricing_query)
    pricing = pricing_res.scalar_one_or_none()
    
    if not pricing:
        raise HTTPException(status_code=400, detail="Invalid service pricing ID")
    
    # Calculate costs (simplistic for now, should include coupon logic)
    # The schemas/booking.py should ideally handle some of this or we do it here.
    
    # Get Address snapshot if doorstep
    address_snapshot = None
    if booking_in.service_location == "doorstep" and booking_in.address_id:
        addr_query = select(Address).where(and_(Address.id == booking_in.address_id, Address.user_id == current_user.id))
        addr_res = await db.execute(addr_query)
        addr = addr_res.scalar_one_or_none()
        if addr:
            address_snapshot = {
                "label": addr.label,
                "address_line1": addr.address_line1,
                "address_line2": addr.address_line2,
                "city": addr.city,
                "state": addr.state,
                "pincode": addr.pincode
            }
    
    new_booking = Booking(
        user_id=current_user.id,
        device_brand_id=booking_in.device_brand_id,
        device_model_id=booking_in.device_model_id,
        service_id=booking_in.service_id,
        service_pricing_id=booking_in.service_pricing_id,
        device_storage=booking_in.device_storage,
        device_color=booking_in.device_color,
        device_purchase_date=booking_in.device_purchase_date,
        is_under_warranty=booking_in.is_under_warranty,
        device_condition_description=booking_in.device_condition_description,
        device_photos=booking_in.device_photos,
        selected_part_grade=pricing.part_grade,
        quoted_part_cost=pricing.part_cost,
        quoted_labor_cost=pricing.labor_cost,
        quoted_subtotal=pricing.part_cost + pricing.labor_cost, # Basic
        # Logic for discounts should go here
        discount_amount=0, 
        final_price=pricing.final_price, # Snapshot from pricing table
        preferred_date=booking_in.preferred_date,
        preferred_time_slot=booking_in.preferred_time_slot,
        estimated_duration_minutes=pricing.estimated_time_max,
        service_location=booking_in.service_location,
        address_id=booking_in.address_id,
        full_address_snapshot=address_snapshot,
        data_backup_requested=booking_in.data_backup_requested,
        privacy_agreement_signed=booking_in.privacy_agreement_signed,
        device_insurance_opted=booking_in.device_insurance_opted,
        customer_notes=booking_in.customer_notes,
        payment_method=booking_in.payment_method,
        status=await MetadataHelper.get_code_by_order(db, "BOOKING_STATUS", 1) or "pending",
        payment_status=await MetadataHelper.get_code_by_fallback(db, "PAYMENT_STATUS", "pending")
    )
    
    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)
    return new_booking

class UserBookingListResponse(BaseModel):
    bookings: List[BookingListItem]
    pagination: PaginationInfo

@router.get("/bookings", response_model=UserBookingListResponse)
async def get_my_bookings(
    status: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get active user's bookings with filters and joined data"""
    query = (
        select(Booking)
        .outerjoin(User, Booking.technician_id == User.id)
        .options(
            joinedload(Booking.service),
            joinedload(Booking.device_brand),
            joinedload(Booking.device_model)
        )
        .add_columns(User.full_name.label("tech_name"))
        .where(Booking.user_id == current_user.id)
    )
    
    if status and status.lower() != 'all':
        if status.lower() == 'active':
            # Dynamic active status detection from metadata
            active_statuses = await MetadataHelper.get_codes(db, "BOOKING_STATUS", is_active=True)
            if not active_statuses:
                active_statuses = ['pending', 'confirmed', 'assigned', 'in_progress']
            query = query.where(Booking.status.in_(active_statuses))
        else:
            query = query.where(Booking.status == status.lower())
    
    if search:
        query = query.where(
            or_(
                Booking.booking_number.ilike(f"%{search}%"),
                Service.service_name.ilike(f"%{search}%")
            )
        )
    
    # Count total for pagination
    count_query = select(func.count()).select_from(query.subquery())
    total_res = await db.execute(count_query)
    total = total_res.scalar() or 0
    
    # Paging and ordering
    query = query.order_by(Booking.created_at.desc()).offset((page - 1) * limit).limit(limit)
    
    result = await db.execute(query)
    rows = result.unique().all()
    
    bookings = []
    for row in rows:
        b = row[0]
        tech_name = row[1]
        bookings.append({
            "id": b.id,
            "booking_number": b.booking_number,
            "service_name": b.service.service_name,
            "service_icon": b.service.icon_name or "Smartphone",
            "service_type": b.service.service_type,
            "brand_name": b.device_brand.name,
            "model_name": b.device_model.model_name,
            "status": b.status,
            "final_price": b.final_price or 0,
            "preferred_date": b.preferred_date,
            "preferred_time_slot": b.preferred_time_slot,
            "service_location": b.service_location,
            "technician_name": tech_name or "Awaiting Assignment",
            "created_at": b.created_at
        })
    
    return {
        "bookings": bookings,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        }
    }

@router.get("/bookings/{bookingId}", response_model=BookingSchema)
async def get_booking_by_id(
    bookingId: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Booking).where(and_(Booking.id == bookingId, Booking.user_id == current_user.id))
    result = await db.execute(query)
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    return booking
