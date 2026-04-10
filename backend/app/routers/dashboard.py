from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, or_, desc
from datetime import datetime, timedelta
import uuid

from ..database import get_db
from ..models import Service, Booking, User, Banner as BannerModel
from ..models.service import ServicePricing
from ..models.device import DeviceModel, Brand
from ..utils.dependencies import get_current_user
from pydantic import BaseModel
from ..utils.metadata import MetadataHelper

router = APIRouter(prefix="/api", tags=["Dashboard"])

# ==================== Schemas ====================

class BannerResponse(BaseModel):
    id: uuid.UUID
    image_url: str
    title: str
    description: Optional[str]
    cta_text: str
    cta_link: str
    display_order: int

class QuickAction(BaseModel):
    id: uuid.UUID
    name: str
    icon: str
    starting_price: float
    service_type: str
    color: str

class QuickActionResponse(BaseModel):
    quick_actions: List[QuickAction]

class DashboardStats(BaseModel):
    total_bookings: int
    scheduled_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    wallet_balance: float
    loyalty_points: int

class ActiveBookingResponse(BaseModel):
    id: uuid.UUID
    booking_number: str
    service: str
    technician: Optional[str]
    date: str
    status: str
    progress: int


class RecentBookingResponse(BaseModel):
    id: uuid.UUID
    title: str
    time: str
    status: str

# ==================== Endpoints ====================

@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user dashboard statistics"""
    
    # Count total bookings
    total_query = select(func.count(Booking.id)).where(Booking.user_id == current_user.id)
    total_result = await db.execute(total_query)
    total_bookings = total_result.scalar() or 0
    
    # Count scheduled bookings (dynamically determined by is_active flag)
    active_statuses = await MetadataHelper.get_codes(db, "BOOKING_STATUS", is_active=True)
    if not active_statuses:
        active_statuses = ['pending', 'confirmed', 'assigned', 'in_progress']
        
    scheduled_query = select(func.count(Booking.id)).where(
        and_(
            Booking.user_id == current_user.id,
            Booking.status.in_(active_statuses)
        )
    )
    scheduled_result = await db.execute(scheduled_query)
    scheduled_bookings = scheduled_result.scalar() or 0
    
    # Count completed bookings
    comp_status = await MetadataHelper.get_code_by_fallback(db, "BOOKING_STATUS", "completed")
    completed_query = select(func.count(Booking.id)).where(
        and_(
            Booking.user_id == current_user.id,
            Booking.status == comp_status
        )
    )
    completed_result = await db.execute(completed_query)
    completed_bookings = completed_result.scalar() or 0
    
    # Count cancelled bookings
    canc_status = await MetadataHelper.get_code_by_fallback(db, "BOOKING_STATUS", "cancelled")
    cancelled_query = select(func.count(Booking.id)).where(
        and_(
            Booking.user_id == current_user.id,
            Booking.status == canc_status
        )
    )
    cancelled_result = await db.execute(cancelled_query)
    cancelled_bookings = cancelled_result.scalar() or 0
    
    return DashboardStats(
        total_bookings=total_bookings,
        scheduled_bookings=scheduled_bookings,
        completed_bookings=completed_bookings,
        cancelled_bookings=cancelled_bookings,
        wallet_balance=float(current_user.wallet_balance or 0.0),
        loyalty_points=int(current_user.loyalty_points or 0)
    )


@router.get("/bookings/active", response_model=Optional[ActiveBookingResponse])
async def get_active_booking(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's current active booking"""
    
    # Find the most recent active booking
    active_statuses = await MetadataHelper.get_codes(db, "BOOKING_STATUS", is_active=True)
    if not active_statuses:
        active_statuses = ['pending', 'confirmed', 'assigned', 'in_progress']

    query = select(Booking, Service).outerjoin(
        User, Booking.technician_id == User.id
    ).join(
        Service, Booking.service_id == Service.id
    ).where(
        and_(
            Booking.user_id == current_user.id,
            Booking.status.in_(active_statuses)
        )
    ).add_columns(User.full_name.label("tech_name")).order_by(Booking.created_at.desc()).limit(1)
    
    result = await db.execute(query)
    row = result.first()
    
    if not row:
        return None
    
    booking = row[0]
    service = row[1]
    tech_name = row[2]
    
    # Calculate progress based on status
    progress_map = {
        'pending': 10,
        'confirmed': 30,
        'assigned': 60,
        'in_progress': 80
    }
    
    # Format date
    date_str = "Today" if booking.preferred_date == datetime.now().date() else booking.preferred_date.strftime("%d %b")
    time_str = booking.preferred_time_slot or "TBD"
    
    return ActiveBookingResponse(
        id=booking.id,
        booking_number=booking.booking_number,
        service=service.service_name,
        technician=tech_name or "Awaiting Assignment",
        date=f"{date_str}, {time_str}",
        status=booking.status.replace('_', ' ').title(),
        progress=progress_map.get(booking.status, 50)
    )


@router.get("/bookings/recent", response_model=List[RecentBookingResponse])
async def get_recent_bookings(
    limit: int = 3,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's recent bookings"""
    
    query = select(Booking, Service).join(
        Service, Booking.service_id == Service.id
    ).where(
        Booking.user_id == current_user.id
    ).order_by(Booking.created_at.desc()).limit(limit)
    
    result = await db.execute(query)
    rows = result.all()
    
    bookings = []
    for booking, service in rows:
        # Format time
        if booking.completed_at:
            time_diff = datetime.now() - booking.completed_at
            if time_diff.days == 0:
                time_str = "Today"
            elif time_diff.days == 1:
                time_str = "Yesterday"
            else:
                time_str = booking.completed_at.strftime("%d %b, %I:%M %p")
        elif booking.preferred_date:
            if booking.preferred_date > datetime.now().date():
                time_str = f"Scheduled for {booking.preferred_date.strftime('%d %b')}"
            else:
                time_str = booking.preferred_date.strftime("%d %b, %I:%M %p")
        else:
            time_str = booking.created_at.strftime("%d %b, %I:%M %p")
        
        # Determine status display
        comp_status = await MetadataHelper.get_code_by_fallback(db, "BOOKING_STATUS", "completed")
        pend_status = await MetadataHelper.get_code_by_fallback(db, "BOOKING_STATUS", "pending")
        conf_status = await MetadataHelper.get_code_by_fallback(db, "BOOKING_STATUS", "confirmed")

        status_display = "Completed" if booking.status == comp_status else "Upcoming" if booking.status in [pend_status, conf_status] else booking.status.replace('_', ' ').title()
        
        bookings.append(
            RecentBookingResponse(
                id=booking.id,
                title=service.service_name,
                time=time_str,
                status=status_display
            )
        )
    
    return bookings


@router.get("/dashboard/quick-actions", response_model=QuickActionResponse)
async def get_quick_actions(db: AsyncSession = Depends(get_db)):
    """Get quick action services for dashboard"""
    
    # Fetch top services by display order
    query = select(Service).where(
        Service.is_active == True
    ).order_by(Service.display_order.asc()).limit(8)
    
    result = await db.execute(query)
    services = result.scalars().all()
    
    actions = []
    for s in services:
        price_query = select(func.min(ServicePricing.final_price)).where(ServicePricing.service_id == s.id)
        min_price = (await db.execute(price_query)).scalar() or 0.0
        actions.append(
            QuickAction(
                id=s.id,
                name=s.service_name.split('(')[0].strip(),
                icon=s.icon_name or "Smartphone",
                starting_price=float(min_price),
                service_type=s.service_type,
                color=s.icon_color or "#6366F1"
            )
        )
    
    return QuickActionResponse(quick_actions=actions)


@router.get("/banners/active", response_model=List[BannerResponse])
async def get_active_banners(db: AsyncSession = Depends(get_db)):
    """Get active promotional banners from DB"""
    query = select(BannerModel).where(BannerModel.is_active == True).order_by(BannerModel.display_order.asc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/services/categories")
async def get_service_categories(db: AsyncSession = Depends(get_db)):
    """Get all service categories"""
    
    # Get distinct service types
    query = select(Service.service_type, func.count(Service.id).label('count')).where(
        Service.is_active == True
    ).group_by(Service.service_type)
    
    result = await db.execute(query)
    categories = []
    
    for row in result:
        service_type, count = row
        categories.append({
            "id": service_type,
            "name": service_type.replace('_', ' ').title(),
            "count": count,
            "icon": "Smartphone"  # Would map service_type to appropriate icon
        })
    
    return {"categories": categories}


class FeaturedService(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    icon: str
    starting_price: float
    is_popular: bool

class FeaturedServiceResponse(BaseModel):
    services: List[FeaturedService]

@router.get("/services/featured", response_model=FeaturedServiceResponse)
async def get_featured_services(db: AsyncSession = Depends(get_db)):
    """Get featured services"""
    
    query = select(Service).where(
        Service.is_active == True
    ).order_by(Service.display_order.asc()).limit(6)
    
    result = await db.execute(query)
    services = result.scalars().all()
    
    featured = []
    for service in services:
        featured.append(
            FeaturedService(
                id=service.id,
                name=service.service_name,
                description=service.description or "Professional repair service",
                icon=service.icon_name or "Smartphone",
                starting_price=499.0,
                is_popular=service.display_order <= 3
            )
        )
    
    return FeaturedServiceResponse(services=featured)


class ServiceListItem(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    type: str
    icon: str
    icon_color: str
    starting_price: float
    duration: str
    warranty: str

@router.get("/services", response_model=List[ServiceListItem])
async def get_services(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all services with optional filtering and search"""
    
    query = select(Service).where(Service.is_active == True)
    
    if category and category.lower() != 'all':
        query = query.where(Service.service_type == category.lower())
        
    if search:
        query = query.where(
            or_(
                Service.service_name.ilike(f"%{search}%"),
                Service.description.ilike(f"%{search}%")
            )
        )
        
    query = query.order_by(Service.display_order.asc())
    
    result = await db.execute(query)
    services = result.scalars().all()
    
    output = []
    for s in services:
        price_query = select(func.min(ServicePricing.final_price)).where(ServicePricing.service_id == s.id)
        min_price = (await db.execute(price_query)).scalar() or 0.0
        output.append(
            ServiceListItem(
                id=s.id,
                name=s.service_name,
                description=s.description or "Professional repair service",
                type=s.service_type,
                icon=s.icon_name or "Smartphone",
                icon_color=s.icon_color or "#6366F1",
                starting_price=float(min_price),
                duration="30-60 mins",
                warranty="6 months warranty"
            )
        )
    
    return output


class ServiceDetailResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    type: str
    icon: str
    icon_color: str
    requires_parts: bool
    is_diagnostic: bool
    typical_symptoms: List[str]

@router.get("/services/{service_id}", response_model=ServiceDetailResponse)
async def get_service_details(
    service_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information for a specific service"""
    
    query = select(Service).where(Service.id == service_id)
    result = await db.execute(query)
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
        
    return ServiceDetailResponse(
        id=service.id,
        name=service.service_name,
        description=service.description,
        type=service.service_type,
        icon=service.icon_name,
        icon_color=service.icon_color,
        requires_parts=service.requires_parts,
        is_diagnostic=service.is_diagnostic,
        typical_symptoms=service.typical_symptoms
    )
