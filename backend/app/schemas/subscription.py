from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date
from typing import List, Optional, Any

class ProtectionPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    discounted_price: Optional[float] = None
    duration_months: int = 12
    features: List[str] = []
    is_popular: bool = False
    is_active: bool = True

class ProtectionPlanCreate(ProtectionPlanBase):
    pass

class ProtectionPlan(ProtectionPlanBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserSubscriptionBase(BaseModel):
    user_id: UUID
    plan_id: UUID
    start_date: datetime
    end_date: datetime
    status: str = "active"

class UserSubscription(UserSubscriptionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    plan: Optional[ProtectionPlan] = None

    class Config:
        from_attributes = True

class PurchaseRequest(BaseModel):
    plan_id: UUID
