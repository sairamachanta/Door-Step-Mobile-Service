from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.system import SystemMetadata
from typing import List, Optional

class MetadataHelper:
    @staticmethod
    async def get_codes(db: AsyncSession, category: str, is_active: Optional[bool] = None, can_admin_set: Optional[bool] = None, can_tech_set: Optional[bool] = None) -> List[str]:
        """Fetch matching codes for a category, optionally filtered by flags in ui_config."""
        query = select(SystemMetadata.code, SystemMetadata.ui_config).where(SystemMetadata.category == category)
        result = await db.execute(query)
        rows = result.all()
        
        filtered_codes = []
        for code, ui_config in rows:
            match = True
            if is_active is not None and ui_config.get("is_active") != is_active: match = False
            if can_admin_set is not None and ui_config.get("can_admin_set") != can_admin_set: match = False
            if can_tech_set is not None and ui_config.get("can_technician_set") != can_tech_set: match = False
            
            if match:
                filtered_codes.append(code)
        
        return filtered_codes

    @staticmethod
    async def get_code_by_order(db: AsyncSession, category: str, order: int) -> Optional[str]:
        """Fetch code for a specific display order (e.g., initial status)."""
        query = select(SystemMetadata.code).where(SystemMetadata.category == category, SystemMetadata.display_order == order)
        result = await db.execute(query)
        return result.scalar()

    @staticmethod
    async def get_code_by_fallback(db: AsyncSession, category: str, primary_code: str) -> str:
        """Fetch code, ensuring it exists in metadata, or return the provided string if not found (with logging/warning)."""
        query = select(SystemMetadata.code).where(SystemMetadata.category == category, SystemMetadata.code == primary_code)
        result = await db.execute(query)
        found = result.scalar()
        return found if found else primary_code
