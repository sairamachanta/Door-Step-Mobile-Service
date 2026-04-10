import asyncio
import uuid
from datetime import datetime
from sqlalchemy import select, func
from app.database import engine, SessionLocal
from app.models.system import SystemMetadata, SystemSettings

async def sync_metadata():
    print("Starting metadata synchronization...")
    
    metadata_items = [
        # User Roles
        {"category": "USER_ROLE", "code": "admin", "label": "Administrator", "ui_config": {"color": "purple", "icon": "shield"}, "display_order": 1},
        {"category": "USER_ROLE", "code": "technician", "label": "Technician", "ui_config": {"color": "blue", "icon": "wrench"}, "display_order": 2},
        {"category": "USER_ROLE", "code": "customer", "label": "Customer", "ui_config": {"color": "green", "icon": "user"}, "display_order": 3},
        # User Status
        {"category": "USER_STATUS", "code": "active", "label": "Active", "ui_config": {"color": "emerald"}, "display_order": 1},
        {"category": "USER_STATUS", "code": "suspended", "label": "Suspended", "ui_config": {"color": "red"}, "display_order": 2},
        {"category": "USER_STATUS", "code": "blocked", "label": "Blocked", "ui_config": {"color": "slate"}, "display_order": 3},
        # Booking Status
        {"category": "BOOKING_STATUS", "code": "pending", "label": "Pending Arrival", "ui_config": {"color": "amber", "is_active": True, "can_admin_set": True, "can_technician_set": False}, "display_order": 1},
        {"category": "BOOKING_STATUS", "code": "confirmed", "label": "Confirmed", "ui_config": {"color": "blue", "is_active": True, "can_admin_set": True, "can_technician_set": False}, "display_order": 2},
        {"category": "BOOKING_STATUS", "code": "assigned", "label": "Dispatched", "ui_config": {"color": "violet", "is_active": True, "can_admin_set": True, "can_technician_set": False}, "display_order": 3},
        {"category": "BOOKING_STATUS", "code": "in_progress", "label": "In Progress", "ui_config": {"color": "orange", "is_active": True, "can_admin_set": True, "can_technician_set": True}, "display_order": 4},
        {"category": "BOOKING_STATUS", "code": "completed", "label": "Completed", "ui_config": {"color": "emerald", "is_active": False, "can_admin_set": True, "can_technician_set": True}, "display_order": 5},
        {"category": "BOOKING_STATUS", "code": "cancelled", "label": "Cancelled", "ui_config": {"color": "red", "is_active": False, "can_admin_set": True, "can_technician_set": True}, "display_order": 6},
        # Admin Tabs
        {"category": "ADMIN_TAB", "code": "users", "label": "Manage Users", "display_order": 1},
        {"category": "ADMIN_TAB", "code": "technicians", "label": "Manage Technicians", "display_order": 2},
        {"category": "ADMIN_TAB", "code": "admins", "label": "Manage Admins", "display_order": 3},
        {"category": "ADMIN_TAB", "code": "bookings", "label": "Bookings & Ops", "display_order": 4},
        # Technician Tabs
        {"category": "TECHNICIAN_TAB", "code": "jobs", "label": "My Jobs", "display_order": 1},
        {"category": "TECHNICIAN_TAB", "code": "customers", "label": "Customers", "display_order": 2},
    ]

    settings_items = [
        {"key": "APP_NAME", "value": "Doorstep mobile services", "description": "Application Name", "is_public": True},
        {"key": "CURRENCY_SYMBOL", "value": "₹", "description": "Local Currency Symbol", "is_public": True},
        {"key": "OTP_EXPIRY_MINUTES", "value": "5", "description": "OTP validity duration", "data_type": "int", "is_public": True},
        {"key": "SUPPORT_PHONE", "value": "+91 9000000001", "description": "Customer Support Contact", "is_public": True},
    ]

    async with SessionLocal() as session:
        # Sync Metadata
        for item in metadata_items:
            result = await session.execute(
                select(SystemMetadata).where(
                    SystemMetadata.category == item["category"],
                    SystemMetadata.code == item["code"]
                )
            )
            existing = result.scalars().first()
            if existing:
                existing.label = item["label"]
                existing.ui_config = item.get("ui_config", {})
                existing.display_order = item["display_order"]
                print(f"Updated metadata: {item['category']} - {item['code']}")
            else:
                new_item = SystemMetadata(**item)
                session.add(new_item)
                print(f"Created metadata: {item['category']} - {item['code']}")
        
        # Sync Settings
        for item in settings_items:
            result = await session.execute(
                select(SystemSettings).where(SystemSettings.key == item["key"])
            )
            existing = result.scalars().first()
            if existing:
                existing.value = item["value"]
                existing.description = item["description"]
                existing.is_public = item["is_public"]
                print(f"Updated setting: {item['key']}")
            else:
                new_item = SystemSettings(**item)
                session.add(new_item)
                print(f"Created setting: {item['key']}")
        
        await session.commit()
    
    print("Synchronization complete!")

if __name__ == "__main__":
    asyncio.run(sync_metadata())
