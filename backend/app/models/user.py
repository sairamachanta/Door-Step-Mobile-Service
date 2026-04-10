from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func, text, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="customer") # customer, technician, admin
    status = Column(String, default="active") # active, inactive, suspended, blocked
    profile_image = Column(String)
    is_phone_verified = Column(Boolean, default=False)
    is_email_verified = Column(Boolean, default=False)
    referral_code = Column(String, unique=True)
    referred_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime)
    wallet_balance = Column(Numeric(10, 2), default=0.0)
    loyalty_points = Column(Integer, default=0)

    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    bookings = relationship("Booking", foreign_keys="[Booking.user_id]", back_populates="user")
    subscriptions = relationship("UserSubscription", back_populates="user", cascade="all, delete-orphan")
    
    @property
    def is_protected(self) -> bool:
        return False


class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String, nullable=False)
    otp_code = Column(String, nullable=False)
    otp_type = Column(String) # signup, login, forgot_password
    is_verified = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="refresh_tokens")
