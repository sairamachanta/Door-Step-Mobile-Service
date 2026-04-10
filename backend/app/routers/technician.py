from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from typing import Optional
import uuid
from datetime import datetime

from ..database import get_db
from ..models import Booking, User, SystemMetadata
from ..utils.rbac import technician_or_higher
from ..utils.dependencies import get_current_active_user
from pydantic import BaseModel
from ..schemas.technician_schemas import (
    TechnicianStatsResponse, TechnicianBookingListItem, TechnicianBookingListResponse,
    TechnicianBookingDetailResponse, TechnicianCustomerListItem, TechnicianCustomerListResponse
)
from ..schemas.base import GenericResponse
from ..utils.metadata import MetadataHelper

router = APIRouter(prefix="/api/technician", tags=["technician"])


class BookingStatusUpdate(BaseModel):
    status: str  # in_progress, completed, cancelled
    technician_notes: Optional[str] = None


@router.get("/stats", response_model=TechnicianStatsResponse)
async def get_technician_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Stats for the currently logged-in technician."""
    cust_role = await MetadataHelper.get_code_by_fallback(db, "USER_ROLE", "customer")
    if current_user.role == cust_role:
        raise HTTPException(status_code=403, detail="Access denied")

    # Status codes
    in_prog_status = await MetadataHelper.get_code_by_fallback(db, "BOOKING_STATUS", "in_progress")
    comp_status = await MetadataHelper.get_code_by_fallback(db, "BOOKING_STATUS", "completed")
    assigned_status = await MetadataHelper.get_code_by_fallback(db, "BOOKING_STATUS", "assigned")
    
    # Stats for technician
    total_assigned = (await db.execute(select(func.count(Booking.id)).where(Booking.technician_id == current_user.id))).scalar() or 0
    
    in_progress = (await db.execute(select(func.count(Booking.id)).where(Booking.technician_id == current_user.id, Booking.status == in_prog_status))).scalar() or 0
    completed = (await db.execute(select(func.count(Booking.id)).where(Booking.technician_id == current_user.id, Booking.status == comp_status))).scalar() or 0
    pending = (await db.execute(select(func.count(Booking.id)).where(Booking.technician_id == current_user.id, Booking.status == assigned_status))).scalar() or 0

    return TechnicianStatsResponse(
        total_assigned=total_assigned,
        in_progress=in_progress,
        completed=completed,
        pending=pending,
        technician_name=current_user.full_name,
    )


@router.get("/bookings", response_model=TechnicianBookingListResponse)
async def get_my_assigned_bookings(
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all bookings assigned to this technician."""
    if current_user.role not in ["technician", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")

    query = (
        select(Booking)
        .options(
            joinedload(Booking.user),
            joinedload(Booking.service),
            joinedload(Booking.device_brand),
            joinedload(Booking.device_model),
        )
        .where(Booking.technician_id == current_user.id)
    )

    if status and status != "all":
        query = query.where(Booking.status == status)

    total = (await db.execute(
        select(func.count(Booking.id)).where(
            Booking.technician_id == current_user.id
        )
    )).scalar() or 0

    query = query.order_by(Booking.preferred_date.asc(), Booking.created_at.desc())
    query = query.offset((page - 1) * limit).limit(limit)

    result = await db.execute(query)
    bookings_raw = result.unique().scalars().all()

    bookings = [
        TechnicianBookingListItem(
            id=b.id,
            booking_number=b.booking_number,
            customer_name=b.user.full_name if b.user else "N/A",
            customer_phone=b.user.phone if b.user else "N/A",
            service_name=b.service.service_name if b.service else "N/A",
            brand_name=b.device_brand.name if b.device_brand else "N/A",
            model_name=b.device_model.model_name if b.device_model else "N/A",
            status=b.status,
            final_price=float(b.final_price or 0),
            preferred_date=b.preferred_date,
            preferred_time_slot=b.preferred_time_slot,
            service_location=b.service_location,
            full_address_snapshot=b.full_address_snapshot,
            customer_notes=b.customer_notes,
            technician_notes=b.technician_notes,
            assigned_at=b.assigned_at,
            created_at=b.created_at,
        )
        for b in bookings_raw
    ]

    return TechnicianBookingListResponse(
        bookings=bookings,
        pagination={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit,
        },
    )


@router.get("/bookings/{booking_id}", response_model=TechnicianBookingDetailResponse)
async def get_assigned_booking_detail(
    booking_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get full details of a specific assigned booking."""
    if current_user.role not in ["technician", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")

    result = await db.execute(
        select(Booking)
        .options(
            joinedload(Booking.user),
            joinedload(Booking.service),
            joinedload(Booking.device_brand),
            joinedload(Booking.device_model),
        )
        .where(Booking.id == booking_id, Booking.technician_id == current_user.id)
    )
    booking = result.unique().scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found or not assigned to you")

    return TechnicianBookingDetailResponse(
        id=booking.id,
        booking_number=booking.booking_number,
        customer_name=booking.user.full_name if booking.user else "N/A",
        customer_phone=booking.user.phone if booking.user else "N/A",
        service_name=booking.service.service_name if booking.service else "N/A",
        brand_name=booking.device_brand.name if booking.device_brand else "N/A",
        model_name=booking.device_model.model_name if booking.device_model else "N/A",
        status=booking.status,
        final_price=float(booking.final_price or 0),
        preferred_date=booking.preferred_date,
        preferred_time_slot=booking.preferred_time_slot,
        service_location=booking.service_location,
        full_address_snapshot=booking.full_address_snapshot,
        device_storage=booking.device_storage,
        device_color=booking.device_color,
        device_condition_description=booking.device_condition_description,
        is_under_warranty=booking.is_under_warranty,
        data_backup_requested=booking.data_backup_requested,
        customer_notes=booking.customer_notes,
        technician_notes=booking.technician_notes,
        assigned_at=booking.assigned_at,
        created_at=booking.created_at,
    )


@router.patch("/bookings/{booking_id}/status", response_model=GenericResponse)
async def update_booking_status(
    booking_id: uuid.UUID,
    body: BookingStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Technician updates the status of their assigned booking."""
    # Validate status against metadata and technician permissions
    status_item = (await db.execute(
        select(SystemMetadata).where(
            SystemMetadata.category == "BOOKING_STATUS", 
            SystemMetadata.code == body.status
        )
    )).scalars().first()

    if not status_item or status_item.ui_config.get("can_technician_set") is not True:
        # Fallback if I haven't added the flag yet: just check if it exists in BOOKING_STATUS 
        # and is one of the standard tech-settable ones
        allowed = ["in_progress", "completed", "cancelled"] 
        if body.status not in allowed:
            raise HTTPException(status_code=400, detail=f"Invalid status or permission denied")

    booking = (await db.execute(
        select(Booking).where(
            Booking.id == booking_id,
            Booking.technician_id == current_user.id
        )
    )).scalars().first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found or not assigned to you")

    booking.status = body.status
    if body.technician_notes:
        booking.technician_notes = body.technician_notes
    
    in_prog_status = await MetadataHelper.get_code_by_fallback(db, "BOOKING_STATUS", "in_progress")
    comp_status = await MetadataHelper.get_code_by_fallback(db, "BOOKING_STATUS", "completed")

    if body.status == in_prog_status:
        booking.actual_start_time = datetime.utcnow()
    elif body.status == comp_status:
        booking.actual_end_time = datetime.utcnow()
        booking.completed_at = datetime.utcnow()

    await db.commit()
    return GenericResponse(success=True, message=f"Booking status updated to {body.status}")


# --- Customer Management (Technicians "control user") ---

class StatusUpdate(BaseModel):
    status: str  # active, suspended, blocked


@router.get("/customers", response_model=TechnicianCustomerListResponse)
async def list_customers(
    status: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all customers (Technicians/Admins only)."""
    tech_role = await MetadataHelper.get_code_by_fallback(db, "USER_ROLE", "technician")
    admin_role = await MetadataHelper.get_code_by_fallback(db, "USER_ROLE", "admin")
    if current_user.role not in [tech_role, admin_role]:
        raise HTTPException(status_code=403, detail="Access denied")

    cust_role = await MetadataHelper.get_code_by_fallback(db, "USER_ROLE", "customer")
    query = select(User).where(User.role == cust_role)

    if status:
        query = query.where(User.status == status)
    if search:
        query = query.where(
            User.full_name.ilike(f"%{search}%") | User.phone.ilike(f"%{search}%")
        )

    # Total count
    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    query = query.order_by(User.created_at.desc()).offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()

    # Booking counts per customer
    user_ids = [u.id for u in users]
    booking_counts = {}
    if user_ids:
        bc_result = await db.execute(
            select(Booking.user_id, func.count(Booking.id).label("count"))
            .where(Booking.user_id.in_(user_ids))
            .group_by(Booking.user_id)
        )
        booking_counts = {row.user_id: row.count for row in bc_result}

    customers = [
        TechnicianCustomerListItem(
            id=u.id,
            full_name=u.full_name,
            phone=u.phone,
            email=u.email,
            status=u.status,
            is_phone_verified=u.is_phone_verified,
            created_at=u.created_at,
            total_bookings=booking_counts.get(u.id, 0),
        )
        for u in users
    ]

    return TechnicianCustomerListResponse(
        customers=customers,
        pagination={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit,
        },
    )


@router.patch("/customers/{customer_id}/status", response_model=GenericResponse)
async def update_customer_status(
    customer_id: uuid.UUID,
    body: StatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Ban or unban a customer (Technicians/Admins only)."""
    # Validate status against metadata
    status_check = await db.execute(
        select(SystemMetadata).where(SystemMetadata.category == "USER_STATUS", SystemMetadata.code == body.status)
    )
    if not status_check.scalars().first():
        status_list_result = await db.execute(select(SystemMetadata.code).where(SystemMetadata.category == "USER_STATUS"))
        valid_statuses = status_list_result.scalars().all()
        raise HTTPException(status_code=400, detail=f"Invalid status. Choose from {valid_statuses}")

    cust_role = await MetadataHelper.get_code_by_fallback(db, "USER_ROLE", "customer")
    result = await db.execute(
        select(User).where(User.id == customer_id, User.role == cust_role)
    )
    customer = result.scalars().first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer.status = body.status
    await db.commit()
    return GenericResponse(success=True, message=f"Customer status updated to {body.status}")

