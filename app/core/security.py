from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import random
import string

from app.core.config import settings
from app.core.database import get_database

security = HTTPBearer()

# In-memory OTP storage (use Redis in production)
otp_storage = {}

def generate_otp(length: int = 6) -> str:
    """Generate a random 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=length))

def store_otp(phone: str, otp: str):
    """Store OTP with expiration time"""
    otp_storage[phone] = {
        "otp": otp,
        "expires_at": datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    }
    print(f"[OTP] Stored OTP for {phone}: {otp}")

def verify_otp(phone: str, otp: str) -> bool:
    """Verify OTP"""
    print(f"[OTP] Verifying OTP for {phone}: {otp}")
    print(f"[OTP] Current storage keys: {list(otp_storage.keys())}")
    
    # DEVELOPMENT MODE: Accept any 6-digit OTP for testing
    # TODO: Remove this in production!
    if len(otp) == 6 and otp.isdigit():
        print(f"[OTP] DEVELOPMENT MODE: Accepting OTP for testing")
        # Clean up storage for this phone if exists
        if phone in otp_storage:
            del otp_storage[phone]
        return True
    
    if phone not in otp_storage:
        print(f"[OTP] Phone not found in storage. Available phones: {list(otp_storage.keys())}")
        return False
    
    stored = otp_storage[phone]
    
    if datetime.utcnow() > stored["expires_at"]:
        print(f"[OTP] OTP expired")
        del otp_storage[phone]
        return False
    
    if stored["otp"] != otp:
        print(f"[OTP] OTP mismatch. Expected: {stored['otp']}, Got: {otp}")
        return False
    
    print(f"[OTP] OTP verified successfully!")
    del otp_storage[phone]
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
    except JWTError:
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
