from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from uuid import UUID
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    full_name: str
    phone: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    pass
    password: str
    referral_code: Optional[str] = None

class UserResponse(UserBase):
    id: UUID
    role: str
    status: str
    is_protected: bool = False
    is_phone_verified: bool
    is_email_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserStats(BaseModel):
    total_bookings: int
    loyalty_points: int
    wallet_balance: float
    member_since: str

# --- OTP Schemas ---
class FirebaseVerifyRequest(BaseModel):
    id_token: str
    phone: str
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    referral_code: Optional[str] = None

class FirebaseResetPasswordRequest(BaseModel):
    id_token: str
    phone: str
    new_password: str
    confirm_password: str

class OTPRequest(BaseModel):
    phone: str
    otp_type: str = "signup" # signup, login, forgot_password

class OTPVerify(BaseModel):
    phone: str
    otp_code: str
    otp_type: str

class OTPResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[UUID] = None
    phone: str

# --- Login & Token Schemas ---
class LoginRequest(BaseModel):
    phone: str
    password: str

class LoginOTPRequest(BaseModel):
    phone: str
    use_otp: bool = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse

class TokenRefresh(BaseModel):
    refresh_token: str

class ForgotPasswordRequest(BaseModel):
    phone: str

class ResetPasswordRequest(BaseModel):
    phone: str
    otp_code: str
    new_password: str
    confirm_password: str

# --- E2EE Schemas ---
class EncryptedRequest(BaseModel):
    ciphertext: str
    encrypted_key: str
    iv: str
    tag: str

class EncryptedResponse(BaseModel):
    ciphertext: str
    iv: str
    tag: str
