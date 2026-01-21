from datetime import datetime, timedelta
from typing import Optional
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import random
import string
import hashlib
import hmac
from cryptography.fernet import Fernet

from app.core.config import settings
from app.core.database import get_database

security = HTTPBearer()

# In-memory OTP storage with rate limiting (use Redis in production)
otp_storage = {}
otp_attempts = {}  # Track failed attempts for rate limiting

def generate_otp(length: int = 6) -> str:
    """Generate a random 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=length))

def hash_otp(otp: str, phone: str) -> str:
    """Hash OTP with phone number for secure storage"""
    return hashlib.sha256(f"{otp}{phone}{settings.OTP_SECRET_KEY}".encode()).hexdigest()

def store_otp(phone: str, otp: str):
    """Store OTP with expiration time and hashing"""
    otp_hash = hash_otp(otp, phone)
    otp_storage[phone] = {
        "otp_hash": otp_hash,
        "expires_at": datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES),
        "attempts": 0,
        "created_at": datetime.utcnow()
    }
    # Reset attempts counter
    otp_attempts[phone] = {"failed_attempts": 0, "last_attempt": None}
    print(f"[OTP] Stored OTP for {phone} (hashed)")

def verify_otp(phone: str, otp: str) -> bool:
    """Verify OTP with rate limiting and security checks"""
    print(f"[OTP] Verifying OTP for {phone}")
    
    # Check rate limiting
    if phone in otp_attempts:
        failed_attempts = otp_attempts[phone]["failed_attempts"]
        if failed_attempts >= settings.OTP_MAX_ATTEMPTS:
            print(f"[OTP] Rate limit exceeded for {phone}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed attempts. Please try again later."
            )
    
    if phone not in otp_storage:
        print(f"[OTP] Phone not found in storage")
        return False
    
    stored = otp_storage[phone]
    
    # Check expiration
    if datetime.utcnow() > stored["expires_at"]:
        print(f"[OTP] OTP expired")
        del otp_storage[phone]
        if phone in otp_attempts:
            del otp_attempts[phone]
        return False
    
    # Verify OTP hash
    provided_hash = hash_otp(otp, phone)
    if not hmac.compare_digest(provided_hash, stored["otp_hash"]):
        print(f"[OTP] OTP mismatch")
        # Increment failed attempts
        if phone not in otp_attempts:
            otp_attempts[phone] = {"failed_attempts": 0, "last_attempt": None}
        otp_attempts[phone]["failed_attempts"] += 1
        otp_attempts[phone]["last_attempt"] = datetime.utcnow()
        return False
    
    print(f"[OTP] OTP verified successfully!")
    # Clean up
    del otp_storage[phone]
    if phone in otp_attempts:
        del otp_attempts[phone]
    return True

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except InvalidTokenError:
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Get current authenticated user from MongoDB"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise credentials_exception
    
    phone: str = payload.get("sub")
    if phone is None:
        raise credentials_exception
    
    # Get user from MongoDB
    db = get_database()
    user = await db.users.find_one({"phone": phone})
    
    if user is None:
        raise credentials_exception
    
    return user
