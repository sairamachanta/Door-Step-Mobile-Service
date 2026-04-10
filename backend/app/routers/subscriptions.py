from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, timedelta
import uuid

from ..database import get_db
from ..models import User, ProtectionPlan, UserSubscription
from ..schemas.subscription import ProtectionPlan as PlanSchema, UserSubscription as UserSubSchema, PurchaseRequest
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["Subscriptions"])

@router.get("/plans", response_model=List[PlanSchema])
async def get_plans(db: AsyncSession = Depends(get_db)):
    """List all available protection plans"""
    query = select(ProtectionPlan).where(ProtectionPlan.is_active == True).order_by(ProtectionPlan.price.asc())
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/subscriptions/my", response_model=Optional[UserSubSchema])
async def get_my_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get active user subscription"""
    query = select(UserSubscription).where(
        and_(
            UserSubscription.user_id == current_user.id,
            UserSubscription.status == "active",
            UserSubscription.end_date >= datetime.now()
        )
    ).order_by(UserSubscription.created_at.desc()).limit(1)
    
    result = await db.execute(query)
    return result.scalar_one_or_none()

@router.post("/subscriptions/purchase")
async def purchase_plan(
    request: PurchaseRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Purchase a protection plan (Mock payment integration)"""
    # Check if plan exists
    plan_query = select(ProtectionPlan).where(ProtectionPlan.id == request.plan_id)
    plan_res = await db.execute(plan_query)
    plan = plan_res.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    # Cancel existing subscriptions
    # In a real app, you might upgrade/pro-rate
    
    # Create new subscription
    new_sub = UserSubscription(
        user_id=current_user.id,
        plan_id=plan.id,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=plan.duration_months * 30),
        status="active"
    )
    
    db.add(new_sub)
    await db.commit()
    await db.refresh(new_sub)
    
    return {"message": "Plan purchased successfully", "subscription_id": new_sub.id}
