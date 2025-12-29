from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from app.core.database import get_db
from app.core.config import settings
from app.core.security import (
    generate_otp, store_otp, verify_otp, 
    create_access_token, get_current_user, otp_storage
)
from app.models.models import User
from app.schemas.schemas import (
    OTPRequest, OTPVerify, Token, UserResponse, 
    UserProfileCreate, UserProfileUpdate, LocationUpdate
)

router = APIRouter()

@router.post("/send-otp")
async def send_otp(request: OTPRequest):
    """Send OTP to phone number"""
    otp = generate_otp()
    store_otp(request.phone, otp)
    
    # In production, send OTP via SMS service (Twilio, etc.)
    # For development, we return the OTP
    print(f"[AUTH] OTP sent for {request.phone}: {otp}")
    return {
        "message": "OTP sent successfully",
        "phone": request.phone,
        "otp": otp  # Remove this in production!
    }

@router.post("/verify-otp", response_model=Token)
async def verify_otp_endpoint(request: OTPVerify, db: AsyncSession = Depends(get_db)):
    """Verify OTP and return access token"""
    print(f"[AUTH] Verifying OTP for phone: {request.phone}, OTP: {request.otp}")
    
    if not verify_otp(request.phone, request.otp):
        print(f"[AUTH] OTP verification FAILED for {request.phone}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    print(f"[AUTH] OTP verification SUCCESS for {request.phone}")
    
    # Check if user exists
    result = await db.execute(select(User).where(User.phone == request.phone))
    user = result.scalar_one_or_none()
    
    is_new_user = False
    if not user:
        # Create new user
        user = User(phone=request.phone, is_verified=True)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        is_new_user = True
    else:
        user.is_verified = True
        await db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.phone},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "phone": user.phone,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "gender": user.gender,
            "role": user.role,
            "professional_type": user.professional_type,
            "city": user.city,
            "state": user.state,
            "bio": user.bio,
            "avatar": user.avatar,
            "sports_interests": user.sports_interests,
            "onboarding_completed": user.onboarding_completed,
            "is_new_user": is_new_user,
            "is_verified": user.is_verified
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

@router.post("/profile", response_model=UserResponse)
async def create_profile(
    profile: UserProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create/Update user profile after OTP verification"""
    current_user.name = profile.name
    current_user.email = profile.email
    current_user.age = profile.age
    current_user.gender = profile.gender
    current_user.role = profile.role
    current_user.professional_type = profile.professional_type
    current_user.city = profile.city
    current_user.state = profile.state
    current_user.bio = profile.bio
    current_user.sports_interests = profile.sports_interests
    current_user.player_position = profile.player_position
    current_user.playing_style = profile.playing_style
    current_user.certification = profile.certification
    current_user.experience_years = profile.experience_years
    current_user.children_count = profile.children_count
    current_user.onboarding_completed = True
    
    await db.flush()
    await db.refresh(current_user)
    
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user profile"""
    if profile.name is not None:
        current_user.name = profile.name
    if profile.email is not None:
        current_user.email = profile.email
    if profile.age is not None:
        current_user.age = profile.age
    if profile.gender is not None:
        current_user.gender = profile.gender
    if profile.role is not None:
        current_user.role = profile.role
    if profile.professional_type is not None:
        current_user.professional_type = profile.professional_type
    if profile.city is not None:
        current_user.city = profile.city
    if profile.state is not None:
        current_user.state = profile.state
    if profile.bio is not None:
        current_user.bio = profile.bio
    if profile.avatar is not None:
        current_user.avatar = profile.avatar
    if profile.sports_interests is not None:
        current_user.sports_interests = profile.sports_interests
    if profile.player_position is not None:
        current_user.player_position = profile.player_position
    if profile.playing_style is not None:
        current_user.playing_style = profile.playing_style
    if profile.certification is not None:
        current_user.certification = profile.certification
    if profile.experience_years is not None:
        current_user.experience_years = profile.experience_years
    if profile.children_count is not None:
        current_user.children_count = profile.children_count
    if profile.onboarding_completed is not None:
        current_user.onboarding_completed = profile.onboarding_completed
    
    await db.flush()
    await db.refresh(current_user)
    
    return current_user

@router.put("/location")
async def update_location(
    location: LocationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user's current location"""
    current_user.latitude = location.latitude
    current_user.longitude = location.longitude
    
    await db.flush()
    
    return {
        "message": "Location updated successfully",
        "latitude": current_user.latitude,
        "longitude": current_user.longitude
    }

@router.get("/debug/otp-storage")
async def debug_otp_storage():
    """Debug endpoint to check OTP storage (REMOVE IN PRODUCTION!)"""
    from datetime import datetime
    storage_info = {}
    for phone, data in otp_storage.items():
        storage_info[phone] = {
            "otp": data["otp"],
            "expires_at": data["expires_at"].isoformat(),
            "is_expired": datetime.utcnow() > data["expires_at"]
        }
    return {
        "count": len(otp_storage),
        "storage": storage_info
    }

