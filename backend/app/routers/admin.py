from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from typing import List, Optional
from app.config import settings
from app.schemas.admin_schemas import (
    AdminStatsResponse, 
    AdminUserListItem,
    AdminUserListResponse, 
    AdminBookingListItem,
    AdminBookingListResponse,
    AdminBookingAssignResponse
)
from app.schemas.base import GenericResponse
import uuid

from ..database import get_db
from ..models import User, Booking, SystemMetadata
from ..schemas.auth import UserResponse
from ..utils.rbac import admin_only
from ..utils.dependencies import get_current_active_user
from ..utils.security import get_password_hash
from pydantic import BaseModel
from ..utils.metadata import MetadataHelper

router = APIRouter(prefix="/api/admin", tags=["admin"])


# --- Schemas (inline for simplicity) ---

class StaffCreate(BaseModel):
    full_name: str
    phone: str
    password: str
    role: str # admin or technician


class StatusUpdate(BaseModel):
    status: str  # active, inactive, suspended


class RoleUpdate(BaseModel):
    role: str


class BookingAssign(BaseModel):
    technician_id: uuid.UUID


class BookingStatusUpdate(BaseModel):
    status: str
    admin_notes: Optional[str] = None


# --- Stats ---

@router.get("/stats", response_model=AdminStatsResponse, dependencies=[Depends(admin_only)])
async def get_admin_stats(db: AsyncSession = Depends(get_db)):
    """Global stats for admin dashboard (admin only)."""
    # 1. Fetch Metadata for dynamic lookups
    meta_res = await db.execute(
        select(SystemMetadata).where(
            SystemMetadata.category.in_(["USER_ROLE", "USER_STATUS", "BOOKING_STATUS"])
        )
    )
    metadata = meta_res.scalars().all()

    # Helper function to get code by category/criteria
    def get_code(category, code=None, order=None, is_active=None):
        for m in metadata:
            if m.category == category:
                if code and m.code == code: return m.code
                if order is not None and m.display_order == order: return m.code
                if is_active is not None and m.ui_config.get("is_active") == is_active: return m.code
        return None

    def get_codes(category, is_active=None):
        codes = []
        for m in metadata:
            if m.category == category:
                if is_active is not None:
                    if m.ui_config.get("is_active") == is_active:
                        codes.append(m.code)
                else:
                    codes.append(m.code)
        return codes

    # Role codes
    cust_role = get_code("USER_ROLE", code="customer") or "customer"
    tech_role = get_code("USER_ROLE", code="technician") or "technician"
    admin_role = get_code("USER_ROLE", code="admin") or "admin"

    # User Status codes
    active_status = get_code("USER_STATUS", code="active") or "active"
    susp_status = get_code("USER_STATUS", code="suspended") or "suspended"

    # Booking Status codes
    pending_status = get_code("BOOKING_STATUS", order=1) or "pending"
    active_booking_statuses = get_codes("BOOKING_STATUS", is_active=True)
    if not active_booking_statuses:
        active_booking_statuses = ["confirmed", "assigned", "in_progress"]
    comp_status = get_code("BOOKING_STATUS", code="completed") or "completed"

    # 2. Perform counts using dynamic codes
    total_users = (await db.execute(
        select(func.count(User.id)).where(User.role == cust_role, User.status == active_status)
    )).scalar() or 0

    total_technicians = (await db.execute(
        select(func.count(User.id)).where(User.role == tech_role, User.status == active_status)
    )).scalar() or 0

    total_bookings = (await db.execute(
        select(func.count(Booking.id))
    )).scalar() or 0

    pending_bookings = (await db.execute(
        select(func.count(Booking.id)).where(Booking.status == pending_status)
    )).scalar() or 0

    active_bookings = (await db.execute(
        select(func.count(Booking.id)).where(
            Booking.status.in_(active_booking_statuses)
        )
    )).scalar() or 0

    completed_bookings = (await db.execute(
        select(func.count(Booking.id)).where(Booking.status == comp_status)
    )).scalar() or 0

    total_revenue = (await db.execute(
        select(func.coalesce(func.sum(Booking.final_price), 0))
        .where(Booking.status == comp_status)
    )).scalar() or 0

    total_suspended = (await db.execute(
        select(func.count(User.id)).where(User.status == susp_status)
    )).scalar() or 0

    suspended_customers = (await db.execute(
        select(func.count(User.id)).where(User.role == cust_role, User.status == susp_status)
    )).scalar() or 0

    suspended_technicians = (await db.execute(
        select(func.count(User.id)).where(User.role == tech_role, User.status == susp_status)
    )).scalar() or 0

    suspended_admins = (await db.execute(
        select(func.count(User.id)).where(User.role == admin_role, User.status == susp_status)
    )).scalar() or 0

    total_admins = (await db.execute(
        select(func.count(User.id)).where(User.role == admin_role, User.status == active_status)
    )).scalar() or 0

    return AdminStatsResponse(
        total_customers=total_users,
        total_technicians=total_technicians,
        total_admins=total_admins,
        total_bookings=total_bookings,
        pending_bookings=pending_bookings,
        active_bookings=active_bookings,
        completed_bookings=completed_bookings,
        total_revenue=float(total_revenue),
        total_suspended=total_suspended,
        suspended_users=suspended_customers,
        suspended_technicians=suspended_technicians,
        suspended_admins=suspended_admins,
    )


# --- Technician Management ---

@router.get("/technicians", response_model=List[UserResponse], dependencies=[Depends(admin_only)])
async def list_technicians(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all technicians (admin only)."""
    tech_role = await MetadataHelper.get_code_by_fallback(db, "USER_ROLE", "technician")
    query = select(User).where(User.role == tech_role)
    if status:
        query = query.where(User.status == status)
    query = query.order_by(User.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/staff", response_model=List[UserResponse], dependencies=[Depends(admin_only)])
async def list_staff(
    role: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all staff (admin + technician) (admin only)."""
    admin_role = await MetadataHelper.get_code_by_fallback(db, "USER_ROLE", "admin")
    tech_role = await MetadataHelper.get_code_by_fallback(db, "USER_ROLE", "technician")
    
    query = select(User).where(User.role.in_([admin_role, tech_role]))
    if role:
        query = query.where(User.role == role)
    query = query.order_by(User.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/staff", response_model=UserResponse, dependencies=[Depends(admin_only)])
async def create_staff(
    staff_in: StaffCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new staff account (admin only)."""
    # Validate role against metadata
    role_check = await db.execute(
        select(SystemMetadata).where(SystemMetadata.category == "USER_ROLE", SystemMetadata.code == staff_in.role)
    )
    if not role_check.scalars().first():
        role_list_result = await db.execute(select(SystemMetadata.code).where(SystemMetadata.category == "USER_ROLE"))
        valid_roles = role_list_result.scalars().all()
        raise HTTPException(status_code=400, detail=f"Invalid role. Choose from {valid_roles}")

    # Check phone unique
    existing = (await db.execute(
        select(User).where(User.phone == staff_in.phone)
    )).scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    new_staff = User(
        id=uuid.uuid4(),
        phone=staff_in.phone,
        full_name=staff_in.full_name,
        role=staff_in.role,
        password_hash=get_password_hash(staff_in.password),
        is_phone_verified=True,
        status="active"
    )
    db.add(new_staff)
    await db.commit()
    await db.refresh(new_staff)
    return new_staff


@router.patch("/staff/{user_id}/status", response_model=GenericResponse, dependencies=[Depends(admin_only)])
async def update_staff_status(
    user_id: uuid.UUID,
    body: StatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Activate or deactivate a staff member (admin only)."""
    # Validate status against metadata
    status_check = await db.execute(
        select(SystemMetadata).where(SystemMetadata.category == "USER_STATUS", SystemMetadata.code == body.status)
    )
    if not status_check.scalars().first():
        status_list_result = await db.execute(select(SystemMetadata.code).where(SystemMetadata.category == "USER_STATUS"))
        valid_statuses = status_list_result.scalars().all()
        raise HTTPException(status_code=400, detail=f"Invalid status. Choose from {valid_statuses}")

    admin_role = await MetadataHelper.get_code_by_fallback(db, "USER_ROLE", "admin")
    tech_role = await MetadataHelper.get_code_by_fallback(db, "USER_ROLE", "technician")
    
    result = await db.execute(
        select(User).where(User.id == user_id, User.role.in_([admin_role, tech_role]))
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Staff member not found")

    # Root Admin protection removed as it's now dynamically seeded

    user.status = body.status
    await db.commit()
    return GenericResponse(success=True, message=f"Staff status updated to {body.status}")


@router.patch("/users/{user_id}/role", response_model=GenericResponse, dependencies=[Depends(admin_only)])
async def update_user_role(
    user_id: uuid.UUID,
    body: RoleUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update any user's role (admin only). Allows promoting/demoting."""
    # Validate role against metadata
    role_check = await db.execute(
        select(SystemMetadata).where(SystemMetadata.category == "USER_ROLE", SystemMetadata.code == body.role)
    )
    if not role_check.scalars().first():
        role_list_result = await db.execute(select(SystemMetadata.code).where(SystemMetadata.category == "USER_ROLE"))
        valid_roles = role_list_result.scalars().all()
        raise HTTPException(status_code=400, detail=f"Invalid role. Choose from {valid_roles}")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = body.role
    await db.commit()
    return GenericResponse(success=True, message=f"User role updated to {body.role}")

@router.delete("/users/{user_id}", response_model=GenericResponse, dependencies=[Depends(admin_only)])
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Permanently delete a user (admin only)."""
    from sqlalchemy.exc import IntegrityError
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # SuperAdmin protection removed as it's now dynamically seeded

    try:
        await db.delete(user)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete user because they have active bookings or other linked records. Try deactivating them instead."
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error during deletion: {str(e)}")
        
    return GenericResponse(success=True, message="User deleted successfully")


# --- Customer Management ---

@router.get("/users", response_model=AdminUserListResponse, dependencies=[Depends(admin_only)])
async def list_users(
    role: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """List users with filtering, search and pagination (admin only)."""
    query = select(User)

    if role:
        query = query.where(User.role == role)
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

    # Booking counts per user
    user_ids = [u.id for u in users]
    booking_counts = {}
    if user_ids:
        bc_result = await db.execute(
            select(Booking.user_id, func.count(Booking.id).label("count"))
            .where(Booking.user_id.in_(user_ids))
            .group_by(Booking.user_id)
        )
        booking_counts = {row.user_id: row.count for row in bc_result}

    user_list = [
        AdminUserListItem(
            id=u.id,
            full_name=u.full_name,
            phone=u.phone,
            email=u.email,
            role=u.role,
            status=u.status,
            is_protected=u.is_protected,
            is_phone_verified=u.is_phone_verified,
            created_at=u.created_at,
            total_bookings=booking_counts.get(u.id, 0),
        )
        for u in users
    ]

    return AdminUserListResponse(
        users=user_list,
        pagination={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit,
        },
    )


@router.patch("/customers/{customer_id}/status", response_model=GenericResponse, dependencies=[Depends(admin_only)])
async def update_customer_status(
    customer_id: uuid.UUID,
    body: StatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Ban or unban a customer (admin only)."""
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


# --- Booking Management ---

@router.get("/bookings", response_model=AdminBookingListResponse, dependencies=[Depends(admin_only)])
async def list_all_bookings(
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """List all bookings across all users (admin only)."""
    from sqlalchemy.orm import joinedload

    query = (
        select(Booking)
        .options(
            joinedload(Booking.user),
            joinedload(Booking.service),
            joinedload(Booking.device_brand),
            joinedload(Booking.device_model),
        )
    )

    if status and status != "all":
        query = query.where(Booking.status == status)

    count_q = select(func.count()).select_from(
        select(Booking).where(Booking.status == status).subquery()
        if (status and status != "all")
        else select(Booking).subquery()
    )
    total = (await db.execute(count_q)).scalar() or 0

    query = query.order_by(Booking.created_at.desc()).offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    bookings_raw = result.unique().scalars().all()

    bookings = [
        AdminBookingListItem(
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
            technician_id=b.technician_id,
            created_at=b.created_at,
        )
        for b in bookings_raw
    ]

    return AdminBookingListResponse(
        bookings=bookings,
        pagination={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit,
        },
    )


@router.patch("/bookings/{booking_id}/assign", response_model=AdminBookingAssignResponse, dependencies=[Depends(admin_only)])
async def assign_booking_to_technician(
    booking_id: uuid.UUID,
    body: BookingAssign,
    db: AsyncSession = Depends(get_db)
):
    """Assign a booking to a technician and update status to 'assigned' (admin only)."""
    from datetime import datetime

    tech_role = await MetadataHelper.get_code_by_fallback(db, "USER_ROLE", "technician")
    assigned_status = await MetadataHelper.get_code_by_fallback(db, "BOOKING_STATUS", "assigned")

    # Verify technician exists
    tech = (await db.execute(
        select(User).where(User.id == body.technician_id, User.role == tech_role)
    )).scalars().first()
    if not tech:
        raise HTTPException(status_code=404, detail="Technician not found")

    # Verify booking exists
    booking = (await db.execute(
        select(Booking).where(Booking.id == booking_id)
    )).scalars().first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.technician_id = body.technician_id
    booking.status = assigned_status
    booking.assigned_at = datetime.utcnow()
    await db.commit()

    return AdminBookingAssignResponse(
        success=True,
        message=f"Booking assigned to {tech.full_name}",
        booking_id=booking_id,
        technician_id=body.technician_id,
        technician_name=tech.full_name,
    )


@router.patch("/bookings/{booking_id}/status", response_model=GenericResponse, dependencies=[Depends(admin_only)])
async def update_booking_status_admin(
    booking_id: uuid.UUID,
    body: BookingStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update booking status (admin only)."""
    valid_res = await db.execute(
        select(SystemMetadata.code).where(
            SystemMetadata.category == "BOOKING_STATUS",
            SystemMetadata.ui_config["can_admin_set"].astext == "true"
        )
    )
    valid = valid_res.scalars().all()
    if not valid:
        valid = ["pending", "confirmed", "assigned", "in_progress", "completed", "cancelled"]
    
    if body.status not in valid:
        raise HTTPException(status_code=400, detail=f"Invalid status. Choose from {valid}")

    booking = (await db.execute(
        select(Booking).where(Booking.id == booking_id)
    )).scalars().first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status = body.status
    if body.admin_notes:
        booking.admin_notes = body.admin_notes
    await db.commit()
    return GenericResponse(success=True, message=f"Booking status updated to {body.status}")
