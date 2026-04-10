from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, delete
from typing import Optional, Union
from datetime import datetime, timedelta
from ..database import get_db
from ..models import User, OTPVerification, RefreshToken, SystemSettings
from ..schemas import (
    UserCreate, UserResponse, OTPRequest, OTPResponse, OTPVerify, 
    LoginRequest, LoginOTPRequest, Token, TokenRefresh, 
    ForgotPasswordRequest, ResetPasswordRequest,
    EncryptedRequest, EncryptedResponse, FirebaseVerifyRequest, FirebaseResetPasswordRequest
)
from ..utils.encryption import EncryptionHelper
import firebase_admin.auth as firebase_auth
from ..schemas.base import GenericResponse
from ..utils.metadata import MetadataHelper
from ..utils import (
    get_password_hash, verify_password, create_access_token, create_refresh_token, 
    generate_otp, get_current_user, get_current_active_user, ALGORITHM
)
from ..config import settings
from jose import jwt, JWTError
import uuid

async def get_otp_expiry(db: AsyncSession) -> int:
    """Fetch OTP expiry minutes from system settings."""
    result = await db.execute(select(SystemSettings.value).where(SystemSettings.key == "OTP_EXPIRY_MINUTES"))
    val = result.scalar()
    try:
        return int(val) if val else 10
    except (ValueError, TypeError):
        return 10

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.get("/public-key")
async def get_public_key():
    return {"public_key": EncryptionHelper.get_public_key()}

@router.post("/signup", response_model=Union[OTPResponse, EncryptedResponse])
async def signup(body: Union[EncryptedRequest, UserCreate], db: AsyncSession = Depends(get_db)):
    user_data = body
    symmetric_key = None

    if isinstance(body, EncryptedRequest):
        try:
            symmetric_key = EncryptionHelper.decrypt_symmetric_key(body.encrypted_key)
            decrypted_data = EncryptionHelper.decrypt_data(
                body.ciphertext, symmetric_key, body.iv, body.tag
            )
            user_data = UserCreate(**decrypted_data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Decryption failed: {str(e)}")

    # Check if phone already exists
    result = await db.execute(select(User).where(User.phone == user_data.phone))
    if result.scalars().first():
        raise HTTPException(status_code=409, detail="Phone number already registered")
    
    # Check if email exists (if provided)
    if user_data.email:
        result = await db.execute(select(User).where(User.email == user_data.email))
        if result.scalars().first():
            raise HTTPException(status_code=409, detail="Email already registered")

    # Create User
    new_user = User(
        phone=user_data.phone,
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=get_password_hash(user_data.password),
        referral_code=user_data.referral_code, # Add logic to verify referral later if needed
        is_phone_verified=False
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Generate OTP
    otp_code = generate_otp()
    expiry_min = await get_otp_expiry(db)
    expires_at = datetime.utcnow() + timedelta(minutes=expiry_min)
    otp_entry = OTPVerification(
        phone=user_data.phone,
        otp_code=otp_code,
        otp_type="signup",
        expires_at=expires_at
    )
    db.add(otp_entry)
    await db.commit()

    # Mock Send OTP
    print(f"--- MOCK SMS to {user_data.phone}: Your OTP is {otp_code} ---")

    otp_resp = OTPResponse(
        success=True, 
        message="OTP sent to your phone", 
        user_id=new_user.id,
        phone=new_user.phone
    )

    if symmetric_key:
        return EncryptionHelper.encrypt_response(otp_resp.dict(), symmetric_key)

    return otp_resp

@router.post("/verify-otp", response_model=Union[Token, EncryptedResponse])
async def verify_otp(body: Union[EncryptedRequest, OTPVerify], db: AsyncSession = Depends(get_db)):
    otp_data = body
    symmetric_key = None
    if isinstance(body, EncryptedRequest):
        try:
            symmetric_key = EncryptionHelper.decrypt_symmetric_key(body.encrypted_key)
            decrypted_data = EncryptionHelper.decrypt_data(body.ciphertext, symmetric_key, body.iv, body.tag)
            otp_data = OTPVerify(**decrypted_data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Decryption failed: {str(e)}")

    # Find latest OTP
    result = await db.execute(
        select(OTPVerification)
        .where(
            OTPVerification.phone == otp_data.phone,
            OTPVerification.otp_type == otp_data.otp_type, 
            OTPVerification.is_verified == False
        )
        .order_by(OTPVerification.created_at.desc())
    )
    otp_record = result.scalars().first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP request")
    
    if otp_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")
    
    if otp_record.otp_code != otp_data.otp_code:
        raise HTTPException(status_code=400, detail="Invalid OTP code")
    
    # Mark Verified
    otp_record.is_verified = True
    await db.commit()

    # Update User
    result = await db.execute(select(User).where(User.phone == otp_data.phone))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_phone_verified = True
    await db.commit()
    await db.refresh(user)

    # Generate Tokens
    access_token = create_access_token(subject=user.id)
    refresh_token_str = create_refresh_token(subject=user.id)
    
    refresh_token_entry = RefreshToken(
        user_id=user.id, 
        token=refresh_token_str, 
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(refresh_token_entry)
    await db.commit()

    user_schema = UserResponse.model_validate(user)

    response_data = {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer",
        "user": user_schema.model_dump()
    }
    
    if symmetric_key:
        return EncryptionHelper.encrypt_response(response_data, symmetric_key)

    return response_data

@router.post("/verify-firebase", response_model=Union[EncryptedResponse, dict])
async def verify_firebase(
    request: EncryptedRequest,
    db: AsyncSession = Depends(get_db)
):
    # Decrypt request
    payload = EncryptionHelper.decrypt_request(request)
    symmetric_key = EncryptionHelper.decrypt_key(request.encrypted_key)
    firebase_data = FirebaseVerifyRequest(**payload)

    # 1. Verify token with Firebase Admin
    try:
        decoded_token = firebase_auth.verify_id_token(firebase_data.id_token)
        fb_phone = decoded_token.get('phone_number', '')
        
        # Verify the phone matches the user claim (stripping +91 if necessary)
        if not fb_phone.endswith(firebase_data.phone):
            raise ValueError("Token phone number mismatch")
            
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase Auth token")
        
    # 2. Check if User Exists
    result = await db.execute(select(User).where(User.phone == firebase_data.phone))
    user = result.scalars().first()

    # 3. Create User if they don't exist (Signup Flow via Firebase)
    if not user:
        if not firebase_data.full_name or not firebase_data.password:
            raise HTTPException(status_code=400, detail="User not found. Full name and password required to register.")
            
        hashed_password = get_password_hash(firebase_data.password)
        active_status = await MetadataHelper.get_code_by_fallback(db, "USER_STATUS", "active")
        customer_role = await MetadataHelper.get_code_by_fallback(db, "USER_ROLE", "customer")
        
        user = User(
            id=uuid.uuid4(),
            full_name=firebase_data.full_name,
            phone=firebase_data.phone,
            email=firebase_data.email,
            password_hash=hashed_password,
            status=active_status,
            role=customer_role,
            is_phone_verified=True,
            referral_code=firebase_data.referral_code
        )
        db.add(user)
    else:
        # Mark phone as verified if it wasn't already
        user.is_phone_verified = True

    await db.commit()
    await db.refresh(user)

    # 4. Generate Standard Backend Tokens
    access_token = create_access_token(subject=user.id)
    refresh_token_str = create_refresh_token(subject=user.id)
    
    refresh_token_entry = RefreshToken(
        user_id=user.id, 
        token=refresh_token_str, 
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(refresh_token_entry)
    await db.commit()

    user_resp = UserResponse.model_validate(user)
    
    response_data = {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer",
        "user": user_resp.model_dump(mode='json')
    }
    
    return EncryptionHelper.encrypt_response(response_data, symmetric_key)


@router.post("/resend-otp", response_model=Union[EncryptedResponse, dict])
async def resend_otp(body: Union[EncryptedRequest, OTPRequest], db: AsyncSession = Depends(get_db)):
    request = body
    symmetric_key = None
    if isinstance(body, EncryptedRequest):
        try:
            symmetric_key = EncryptionHelper.decrypt_symmetric_key(body.encrypted_key)
            decrypted_data = EncryptionHelper.decrypt_data(body.ciphertext, symmetric_key, body.iv, body.tag)
            request = OTPRequest(**decrypted_data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Decryption failed: {str(e)}")
    
    # Rate Limit Check (Simple 30s check)
    result = await db.execute(
        select(OTPVerification)
        .where(OTPVerification.phone == request.phone, OTPVerification.otp_type == request.otp_type)
        .order_by(OTPVerification.created_at.desc())
    )
    last_otp = result.scalars().first()
    if last_otp and (datetime.utcnow() - last_otp.created_at).total_seconds() < 30:
        raise HTTPException(status_code=429, detail="Please wait 30 seconds before resending OTP")

    otp_code = generate_otp()
    expiry_min = await get_otp_expiry(db)
    expires_at = datetime.utcnow() + timedelta(minutes=expiry_min)
    otp_entry = OTPVerification(
        phone=request.phone,
        otp_code=otp_code,
        otp_type=request.otp_type,
        expires_at=expires_at
    )
    db.add(otp_entry)
    await db.commit()

    print(f"--- MOCK SMS to {request.phone}: Your OTP is {otp_code} ---")
    
    otp_resp = OTPResponse(success=True, message="OTP resent successfully", phone=request.phone)
    if symmetric_key:
        return EncryptionHelper.encrypt_response(otp_resp.dict(), symmetric_key)
    return otp_resp

@router.post("/login", response_model=Union[Token, EncryptedResponse])
async def login(body: Union[EncryptedRequest, LoginRequest], db: AsyncSession = Depends(get_db)):
    login_data = body
    symmetric_key = None

    if isinstance(body, EncryptedRequest):
        try:
            symmetric_key = EncryptionHelper.decrypt_symmetric_key(body.encrypted_key)
            decrypted_data = EncryptionHelper.decrypt_data(
                body.ciphertext, symmetric_key, body.iv, body.tag
            )
            login_data = LoginRequest(**decrypted_data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Decryption failed: {str(e)}")

    result = await db.execute(select(User).where(User.phone == login_data.phone))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")
        
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    active_status = await MetadataHelper.get_code_by_fallback(db, "USER_STATUS", "active")
    if user.status != active_status:
        raise HTTPException(status_code=403, detail="Account is not active")

    user.last_login = datetime.utcnow()
    await db.commit()

    access_token = create_access_token(subject=user.id)
    refresh_token_str = create_refresh_token(subject=user.id)

    refresh_token_entry = RefreshToken(
        user_id=user.id, 
        token=refresh_token_str, 
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(refresh_token_entry)
    await db.commit()

    token_resp = Token(
        access_token=access_token, 
        refresh_token=refresh_token_str, 
        token_type="Bearer", 
        user=user
    )

    if symmetric_key:
        return EncryptionHelper.encrypt_response(token_resp.dict(), symmetric_key)
    
    return token_resp

@router.post("/login-otp", response_model=Union[OTPResponse, EncryptedResponse])
async def login_with_otp(body: Union[EncryptedRequest, LoginOTPRequest], db: AsyncSession = Depends(get_db)):
    request = body
    symmetric_key = None
    if isinstance(body, EncryptedRequest):
        try:
            symmetric_key = EncryptionHelper.decrypt_symmetric_key(body.encrypted_key)
            decrypted_data = EncryptionHelper.decrypt_data(body.ciphertext, symmetric_key, body.iv, body.tag)
            request = LoginOTPRequest(**decrypted_data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Decryption failed: {str(e)}")

    result = await db.execute(select(User).where(User.phone == request.phone))
    user = result.scalars().first()
    
    if not user:
         raise HTTPException(status_code=404, detail="User not found")
    
    if user.status != "active":
        raise HTTPException(status_code=403, detail="Account is not active")

    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    otp_entry = OTPVerification(
        phone=request.phone,
        otp_code=otp_code,
        otp_type="login",
        expires_at=expires_at
    )
    db.add(otp_entry)
    await db.commit()

    print(f"--- MOCK SMS to {request.phone}: Your Login OTP is {otp_code} ---")
    
    otp_resp = OTPResponse(success=True, message="OTP sent for login", user_id=user.id, phone=user.phone)
    if symmetric_key:
        return EncryptionHelper.encrypt_response(otp_resp.dict(), symmetric_key)
    return otp_resp


@router.post("/forgot-password", response_model=Union[OTPResponse, EncryptedResponse])
async def forgot_password(body: Union[EncryptedRequest, ForgotPasswordRequest], db: AsyncSession = Depends(get_db)):
    request = body
    symmetric_key = None
    if isinstance(body, EncryptedRequest):
        try:
            symmetric_key = EncryptionHelper.decrypt_symmetric_key(body.encrypted_key)
            decrypted_data = EncryptionHelper.decrypt_data(body.ciphertext, symmetric_key, body.iv, body.tag)
            request = ForgotPasswordRequest(**decrypted_data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Decryption failed: {str(e)}")

    result = await db.execute(select(User).where(User.phone == request.phone))
    user = result.scalars().first()
    
    if not user:
        # Don't reveal user existence, but for now we'll throw 404 for simplicity as per requirements prompt implied flow involving check
        raise HTTPException(status_code=404, detail="User not found")

    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    otp_entry = OTPVerification(
        phone=request.phone,
        otp_code=otp_code,
        otp_type="forgot_password",
        expires_at=expires_at
    )
    db.add(otp_entry)
    await db.commit()

    print(f"--- MOCK SMS to {request.phone}: Your Password Reset OTP is {otp_code} ---")

    otp_resp = OTPResponse(success=True, message="OTP sent for password reset", phone=request.phone)
    if symmetric_key:
        return EncryptionHelper.encrypt_response(otp_resp.dict(), symmetric_key)
    return otp_resp

@router.post("/reset-password", response_model=Union[GenericResponse, EncryptedResponse])
async def reset_password(body: Union[EncryptedRequest, ResetPasswordRequest], db: AsyncSession = Depends(get_db)):
    request = body
    symmetric_key = None
    if isinstance(body, EncryptedRequest):
        try:
            symmetric_key = EncryptionHelper.decrypt_symmetric_key(body.encrypted_key)
            decrypted_data = EncryptionHelper.decrypt_data(body.ciphertext, symmetric_key, body.iv, body.tag)
            request = ResetPasswordRequest(**decrypted_data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Decryption failed: {str(e)}")
    
    # Verify OTP
    result = await db.execute(
        select(OTPVerification)
        .where(
            OTPVerification.phone == request.phone,
            OTPVerification.otp_type == "forgot_password",
            OTPVerification.is_verified == False # Should be verified? Or we verify it here? Prompt says "Verify OTP" as step 1.
            # Usually verify-otp endpoint is called first, which marks it verified. 
            # Or we can verify it here again. Let's assume we verify it here implicitly or explicitly.
            # Prompt Flow: 1. Verify OTP, 2. Check Passwords...
            # If we reuse /verify-otp, the user gets a token. 
            # But specific flow here usually implies verifying the code provided in *this* request.
        )
        .order_by(OTPVerification.created_at.desc())
    )
    otp_record = result.scalars().first()
    
    if not otp_record or otp_record.otp_code != request.otp_code:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    if otp_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    # Mark OTP as verified/used
    otp_record.is_verified = True
    
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Update User
    result = await db.execute(select(User).where(User.phone == request.phone))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.password_hash = get_password_hash(request.new_password)
    
    # Invalidate all refresh tokens
    await db.execute(delete(RefreshToken).where(RefreshToken.user_id == user.id))
    
    await db.commit()
    
    resp = GenericResponse(success=True, message="Password reset successful").dict()
    if symmetric_key:
        return EncryptionHelper.encrypt_response(resp, symmetric_key)
    return resp

@router.post("/reset-password-firebase", response_model=Union[GenericResponse, EncryptedResponse])
async def reset_password_firebase(
    request: EncryptedRequest,
    db: AsyncSession = Depends(get_db)
):
    # Decrypt request
    payload = EncryptionHelper.decrypt_request(request)
    symmetric_key = EncryptionHelper.decrypt_key(request.encrypted_key)
    reset_data = FirebaseResetPasswordRequest(**payload)

    # 1. Verify token with Firebase Admin
    try:
        decoded_token = firebase_auth.verify_id_token(reset_data.id_token)
        fb_phone = decoded_token.get('phone_number', '')
        
        # Verify the phone matches the user claim
        if not fb_phone.endswith(reset_data.phone):
            raise ValueError("Token phone number mismatch")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase Auth token")

    if reset_data.new_password != reset_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # 2. Find User
    result = await db.execute(select(User).where(User.phone == reset_data.phone))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # 3. Update Password
    user.password_hash = get_password_hash(reset_data.new_password)
    
    # Invalidate all refresh tokens
    await db.execute(delete(RefreshToken).where(RefreshToken.user_id == user.id))
    
    await db.commit()
    
    resp = GenericResponse(success=True, message="Password reset successful").dict()
    return EncryptionHelper.encrypt_response(resp, symmetric_key)

@router.post("/refresh", response_model=Token)
async def refresh_token(request: TokenRefresh, db: AsyncSession = Depends(get_db)):
    # Verify token format
    try:
        payload = jwt.decode(request.refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
             raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check DB
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == request.refresh_token))
    stored_token = result.scalars().first()
    
    if not stored_token:
         raise HTTPException(status_code=401, detail="Token not found")
         
    if stored_token.is_revoked:
         raise HTTPException(status_code=401, detail="Token revoked")
         
    if stored_token.expires_at < datetime.utcnow():
         raise HTTPException(status_code=401, detail="Token expired")
         
    # Generate new Access Token
    access_token = create_access_token(subject=user_id)
    
    # Fetch user for response
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return Token(
        access_token=access_token,
        refresh_token=request.refresh_token, # Return same refresh token or rotate? Prompt says "Generate new access token". Reusing refresh token for now.
        token_type="Bearer",
        user=user
    )

@router.post("/logout", response_model=GenericResponse)
async def logout(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Invalidate all refresh tokens for this user (or just the one used? Prompt says "Revoke all refresh tokens for user")
    await db.execute(
        delete(RefreshToken).where(RefreshToken.user_id == current_user.id)
    )
    await db.commit()
    return GenericResponse(success=True, message="Logged out successfully")

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    user_resp = UserResponse.from_orm(current_user)
    user_resp.is_protected = False
    return user_resp
