from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta, datetime
from bson import ObjectId
from typing import Optional

from app.core.database import get_database
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
    # Validate phone format
    if not request.phone.startswith("+91") or len(request.phone) != 13:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number format. Use +91XXXXXXXXXX"
        )
    
    otp = generate_otp()
    store_otp(request.phone, otp)
    
    # Log OTP to console for debugging
    print(f"[AUTH] OTP sent for {request.phone}: {otp}")
    
    # Return OTP in response (for development/testing)
    return {
        "message": "OTP sent successfully to your phone number",
        "phone": request.phone,
        "otp": otp,  # Show OTP on screen
        "expires_in_minutes": settings.OTP_EXPIRE_MINUTES
    }

@router.post("/verify-otp", response_model=Token)
async def verify_otp_endpoint(request: OTPVerify):
    """Verify OTP and return access token"""
    print(f"[AUTH] Verifying OTP for phone: {request.phone}")
    
    # Validate OTP format
    if not request.otp.isdigit() or len(request.otp) != 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP must be 6 digits"
        )
    
    # Verify OTP (this will raise HTTPException if rate limited)
    if not verify_otp(request.phone, request.otp):
        print(f"[AUTH] OTP verification FAILED for {request.phone}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    print(f"[AUTH] OTP verification SUCCESS for {request.phone}")
    
    # Get database
    db = get_database()
    
    # Check if user exists
    user_data = await db.users.find_one({"phone": request.phone})
    
    is_new_user = False
    if not user_data:
        # Create new user
        new_user = {
            "phone": request.phone,
            "is_verified": True,
            "is_active": True,
            "onboarding_completed": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = await db.users.insert_one(new_user)
        user_data = await db.users.find_one({"_id": result.inserted_id})
        is_new_user = True
    else:
        # Update verification status
        await db.users.update_one(
            {"_id": user_data["_id"]},
            {"$set": {"is_verified": True, "updated_at": datetime.utcnow()}}
        )
        user_data = await db.users.find_one({"_id": user_data["_id"]})
    
    # Create access token
    access_token = create_access_token(
        data={"sub": request.phone},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Convert MongoDB _id to string
    user_data["id"] = str(user_data["_id"])
    
    print(f"[AUTH] User authenticated: {request.phone}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_data["id"],
            "phone": user_data.get("phone"),
            "name": user_data.get("name"),
            "email": user_data.get("email"),
            "age": user_data.get("age"),
            "gender": user_data.get("gender"),
            "role": user_data.get("role"),
            "professional_type": user_data.get("professional_type"),
            "city": user_data.get("city"),
            "state": user_data.get("state"),
            "bio": user_data.get("bio"),
            "avatar": user_data.get("avatar"),
            "sports_interests": user_data.get("sports_interests", []),
            "onboarding_completed": user_data.get("onboarding_completed", False),
            "is_new_user": is_new_user,
            "is_verified": user_data.get("is_verified", False)
        }
    }

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    # Convert MongoDB _id to string and return clean response
    return {
        "id": str(current_user["_id"]),
        "phone": current_user.get("phone"),
        "name": current_user.get("name"),
        "email": current_user.get("email"),
        "age": current_user.get("age"),
        "gender": current_user.get("gender"),
        "role": current_user.get("role"),
        "professional_type": current_user.get("professional_type"),
        "city": current_user.get("city"),
        "state": current_user.get("state"),
        "latitude": current_user.get("latitude"),
        "longitude": current_user.get("longitude"),
        "bio": current_user.get("bio"),
        "avatar": current_user.get("avatar"),
        "sports_interests": current_user.get("sports_interests", []),
        "player_position": current_user.get("player_position"),
        "playing_style": current_user.get("playing_style"),
        "certification": current_user.get("certification"),
        "experience_years": current_user.get("experience_years"),
        "children_count": current_user.get("children_count"),
        "onboarding_completed": current_user.get("onboarding_completed", False),
        "is_verified": current_user.get("is_verified", False),
        "is_active": current_user.get("is_active", True),
        "created_at": current_user.get("created_at"),
        "updated_at": current_user.get("updated_at")
    }

@router.get("/users/search")
async def search_users(
    query: str,
    role: Optional[str] = None,
    city: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    """Search for users by name, role, or location"""
    db = get_database()
    
    # Build search query
    search_filter = {"is_active": True}
    
    # Text search on name
    if query:
        search_filter["name"] = {"$regex": query, "$options": "i"}
    
    # Filter by role
    if role:
        search_filter["role"] = role
    
    # Filter by city
    if city:
        search_filter["city"] = {"$regex": city, "$options": "i"}
    
    # Execute search
    users_cursor = db.users.find(search_filter).skip(skip).limit(limit)
    users = await users_cursor.to_list(length=limit)
    
    # Return public profile information
    results = []
    for user in users:
        results.append({
            "id": str(user["_id"]),
            "name": user.get("name", "Anonymous"),
            "role": user.get("role"),
            "professional_type": user.get("professional_type"),
            "city": user.get("city"),
            "state": user.get("state"),
            "bio": user.get("bio"),
            "avatar": user.get("avatar"),
            "sports_interests": user.get("sports_interests", []),
            "is_verified": user.get("is_verified", False)
        })
    
    return {
        "results": results,
        "total": len(results)
    }

@router.get("/users/{user_id}")
async def get_user_by_id(user_id: str):
    """Get user profile by user ID (public profile)"""
    db = get_database()
    
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Fetch tournaments created by this user
    tournaments = []
    try:
        tournaments_cursor = db.tournaments.find(
            {"organizer_id": user_id, "is_active": True}
        ).sort([("start_date", -1)]).limit(10)
        tournaments_list = await tournaments_cursor.to_list(length=10)
        
        for tournament in tournaments_list:
            tournaments.append({
                "id": str(tournament["_id"]),
                "name": tournament.get("name"),
                "sport_type": tournament.get("sport_type"),
                "tournament_type": tournament.get("tournament_type"),
                "city": tournament.get("city"),
                "state": tournament.get("state"),
                "start_date": tournament.get("start_date"),
                "end_date": tournament.get("end_date"),
                "status": tournament.get("status"),
                "current_teams": tournament.get("current_teams", 0),
                "max_teams": tournament.get("max_teams", 0),
                "prize_pool": tournament.get("prize_pool"),
                "entry_fee": tournament.get("entry_fee"),
                "is_featured": tournament.get("is_featured", False),
                "is_verified": tournament.get("is_verified", False)
            })
    except Exception as e:
        print(f"Error fetching tournaments: {e}")
    
    # Fetch jobs posted by this user
    jobs = []
    try:
        jobs_cursor = db.jobs.find(
            {"posted_by": user_id, "status": "active"}
        ).sort([("created_at", -1)]).limit(10)
        jobs_list = await jobs_cursor.to_list(length=10)
        
        for job in jobs_list:
            jobs.append({
                "id": str(job["_id"]),
                "title": job.get("title"),
                "job_type": job.get("job_type"),
                "sport_type": job.get("sport_type"),
                "employment_type": job.get("employment_type"),
                "city": job.get("city"),
                "state": job.get("state"),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "salary_type": job.get("salary_type"),
                "experience_required": job.get("experience_required"),
                "application_deadline": job.get("application_deadline"),
                "status": job.get("status"),
                "is_featured": job.get("is_featured", False),
                "is_verified": job.get("is_verified", False)
            })
    except Exception as e:
        print(f"Error fetching jobs: {e}")
    
    # Return public profile information with tournaments and jobs
    return {
        "id": str(user["_id"]),
        "name": user.get("name", "Anonymous"),
        "role": user.get("role"),
        "professional_type": user.get("professional_type"),
        "city": user.get("city"),
        "state": user.get("state"),
        "bio": user.get("bio"),
        "avatar": user.get("avatar"),
        "sports_interests": user.get("sports_interests", []),
        "player_position": user.get("player_position"),
        "playing_style": user.get("playing_style"),
        "certification": user.get("certification"),
        "experience_years": user.get("experience_years"),
        "is_verified": user.get("is_verified", False),
        "tournaments": tournaments,
        "jobs": jobs
    }

@router.post("/profile")
async def create_profile(
    profile: UserProfileCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create/Update user profile after OTP verification"""
    db = get_database()
    
    update_data = {
        "name": profile.name,
        "email": profile.email,
        "age": profile.age,
        "gender": profile.gender,
        "city": profile.city,
        "state": profile.state,
        "bio": profile.bio,
        "sports_interests": profile.sports_interests,
        "player_position": profile.player_position,
        "playing_style": profile.playing_style,
        "certification": profile.certification,
        "experience_years": profile.experience_years,
        "children_count": profile.children_count,
        "updated_at": datetime.utcnow()
    }
    
    # Only set role and professional_type if provided
    if profile.role:
        update_data["role"] = profile.role
    if profile.professional_type:
        update_data["professional_type"] = profile.professional_type
    
    # Don't mark onboarding as completed yet - user still needs to select role
    # update_data["onboarding_completed"] = True
    
    # Remove None values
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": update_data}
    )
    
    # Fetch updated user
    updated_user = await db.users.find_one({"_id": current_user["_id"]})
    
    # Convert ObjectId to string and clean up response
    return {
        "id": str(updated_user["_id"]),
        "phone": updated_user.get("phone"),
        "name": updated_user.get("name"),
        "email": updated_user.get("email"),
        "age": updated_user.get("age"),
        "gender": updated_user.get("gender"),
        "role": updated_user.get("role"),
        "professional_type": updated_user.get("professional_type"),
        "city": updated_user.get("city"),
        "state": updated_user.get("state"),
        "bio": updated_user.get("bio"),
        "avatar": updated_user.get("avatar"),
        "sports_interests": updated_user.get("sports_interests", []),
        "player_position": updated_user.get("player_position"),
        "playing_style": updated_user.get("playing_style"),
        "certification": updated_user.get("certification"),
        "experience_years": updated_user.get("experience_years"),
        "children_count": updated_user.get("children_count"),
        "onboarding_completed": updated_user.get("onboarding_completed", False),
        "is_verified": updated_user.get("is_verified", False),
        "is_active": updated_user.get("is_active", True),
        "created_at": updated_user.get("created_at"),
        "updated_at": updated_user.get("updated_at")
    }

@router.put("/profile")
async def update_profile(
    profile: UserProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update user profile"""
    db = get_database()
    
    # Build update dictionary with only provided fields
    update_data = {}
    if profile.name is not None:
        update_data["name"] = profile.name
    if profile.email is not None:
        update_data["email"] = profile.email
    if profile.age is not None:
        update_data["age"] = profile.age
    if profile.gender is not None:
        update_data["gender"] = profile.gender
    if profile.role is not None:
        update_data["role"] = profile.role
    if profile.professional_type is not None:
        update_data["professional_type"] = profile.professional_type
    if profile.city is not None:
        update_data["city"] = profile.city
    if profile.state is not None:
        update_data["state"] = profile.state
    if profile.bio is not None:
        update_data["bio"] = profile.bio
    if profile.avatar is not None:
        update_data["avatar"] = profile.avatar
    if profile.sports_interests is not None:
        update_data["sports_interests"] = profile.sports_interests
    if profile.player_position is not None:
        update_data["player_position"] = profile.player_position
    if profile.playing_style is not None:
        update_data["playing_style"] = profile.playing_style
    if profile.certification is not None:
        update_data["certification"] = profile.certification
    if profile.experience_years is not None:
        update_data["experience_years"] = profile.experience_years
    if profile.children_count is not None:
        update_data["children_count"] = profile.children_count
    if profile.onboarding_completed is not None:
        update_data["onboarding_completed"] = profile.onboarding_completed
    
    update_data["updated_at"] = datetime.utcnow()
    
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": update_data}
    )
    
    # Fetch updated user
    updated_user = await db.users.find_one({"_id": current_user["_id"]})
    
    # Return clean response
    return {
        "id": str(updated_user["_id"]),
        "phone": updated_user.get("phone"),
        "name": updated_user.get("name"),
        "email": updated_user.get("email"),
        "age": updated_user.get("age"),
        "gender": updated_user.get("gender"),
        "role": updated_user.get("role"),
        "professional_type": updated_user.get("professional_type"),
        "city": updated_user.get("city"),
        "state": updated_user.get("state"),
        "latitude": updated_user.get("latitude"),
        "longitude": updated_user.get("longitude"),
        "bio": updated_user.get("bio"),
        "avatar": updated_user.get("avatar"),
        "sports_interests": updated_user.get("sports_interests", []),
        "player_position": updated_user.get("player_position"),
        "playing_style": updated_user.get("playing_style"),
        "certification": updated_user.get("certification"),
        "experience_years": updated_user.get("experience_years"),
        "children_count": updated_user.get("children_count"),
        "onboarding_completed": updated_user.get("onboarding_completed", False),
        "is_verified": updated_user.get("is_verified", False),
        "is_active": updated_user.get("is_active", True),
        "created_at": updated_user.get("created_at"),
        "updated_at": updated_user.get("updated_at")
    }

@router.put("/location")
async def update_location(
    location: LocationUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update user's current location"""
    db = get_database()
    
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "updated_at": datetime.utcnow()
        }}
    )
    
    return {
        "message": "Location updated successfully",
        "latitude": location.latitude,
        "longitude": location.longitude
    }

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout endpoint - client should clear token from localStorage"""
    return {
        "message": "Logged out successfully. Please clear your token from localStorage."
    }
