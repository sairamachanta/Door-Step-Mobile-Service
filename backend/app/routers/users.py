from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update
import uuid

from ..database import get_db
from ..models import User, Address, Booking
from ..schemas.location import Address as AddressSchema, AddressCreate
from ..schemas.auth import UserResponse, UserUpdate, UserStats, EncryptedRequest, EncryptedResponse
from ..utils.encryption import EncryptionHelper
from ..utils.dependencies import get_current_active_user
from sqlalchemy import func
from typing import Union

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me/addresses", response_model=List[AddressSchema])
async def get_my_addresses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Address).where(and_(Address.user_id == current_user.id, Address.is_active == True))
    query = query.order_by(Address.is_default.desc(), Address.created_at.desc())
    
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/me/addresses", response_model=AddressSchema)
async def create_address(
    address_in: AddressCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # If this address is set as default, unset others
    if address_in.is_default:
        await db.execute(
            update(Address)
            .where(Address.user_id == current_user.id)
            .values(is_default=False)
        )
    
    new_address = Address(
        user_id=current_user.id,
        **address_in.dict()
    )
    
    db.add(new_address)
    await db.commit()
    await db.refresh(new_address)
    return new_address

@router.delete("/me/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Address).where(and_(Address.id == address_id, Address.user_id == current_user.id))
    result = await db.execute(query)
    address = result.scalar_one_or_none()
    
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
        
    address.is_active = False
    await db.commit()
    return None

@router.patch("/me", response_model=Union[UserResponse, EncryptedResponse])
async def update_profile(
    body: Union[EncryptedRequest, UserUpdate],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    user_in = body
    symmetric_key = None
    
    if isinstance(body, EncryptedRequest):
        try:
            symmetric_key = EncryptionHelper.decrypt_symmetric_key(body.encrypted_key)
            decrypted_data = EncryptionHelper.decrypt_data(
                body.ciphertext, symmetric_key, body.iv, body.tag
            )
            user_in = UserUpdate(**decrypted_data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Decryption failed: {str(e)}")

    update_data = user_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    
    if symmetric_key:
        return EncryptionHelper.encrypt_response(UserResponse.from_orm(current_user).dict(), symmetric_key)
        
    return current_user

@router.get("/me/stats", response_model=UserStats)
async def get_user_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Total Bookings count
    count_query = select(func.count(Booking.id)).where(Booking.user_id == current_user.id)
    result = await db.execute(count_query)
    total_bookings = result.scalar() or 0
    
    # Real values from user model
    return UserStats(
        total_bookings=total_bookings,
        loyalty_points=current_user.loyalty_points or 0,
        wallet_balance=float(current_user.wallet_balance or 0.0),
        member_since=current_user.created_at.strftime("%b %Y")
    )
