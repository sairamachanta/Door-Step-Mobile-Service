from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, List, Any
from ..database import get_db
from ..models.system import SystemMetadata, SystemSettings
from pydantic import BaseModel

router = APIRouter(prefix="/api/metadata", tags=["Metadata"])

class MetadataResponse(BaseModel):
    categories: Dict[str, List[Dict[str, Any]]]
    settings: Dict[str, Any]

@router.get("", response_model=MetadataResponse)
async def get_system_metadata(db: AsyncSession = Depends(get_db)):
    # Fetch all active metadata
    meta_result = await db.execute(
        select(SystemMetadata)
        .where(SystemMetadata.is_active == True)
        .order_by(SystemMetadata.category, SystemMetadata.display_order)
    )
    metadatas = meta_result.scalars().all()
    
    categories = {}
    for meta in metadatas:
        if meta.category not in categories:
            categories[meta.category] = []
        categories[meta.category].append({
            "code": meta.code,
            "label": meta.label,
            "ui_config": meta.ui_config
        })
    
    # Fetch all public settings
    settings_result = await db.execute(
        select(SystemSettings).where(SystemSettings.is_public == True)
    )
    settings_list = settings_result.scalars().all()
    
    settings_dict = {s.key: s.value for s in settings_list}
    
    return MetadataResponse(categories=categories, settings=settings_dict)
