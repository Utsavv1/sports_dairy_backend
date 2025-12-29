from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
import math

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Venue, Tournament, Shop, Job, Dictionary
from app.schemas.schemas import (
    VenueResponse, TournamentResponse, ShopResponse, 
    JobResponse, DictionaryResponse
)

router = APIRouter()

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates using Haversine formula (in km)"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


@router.get("/venues")
async def get_nearby_venues(
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    radius_km: float = Query(50, description="Search radius in kilometers"),
    sport_type: Optional[str] = None,
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get nearby venues based on user location"""
    # Use provided coordinates or fallback to user's stored location
    user_lat = latitude if latitude is not None else current_user.latitude
    user_lon = longitude if longitude is not None else current_user.longitude
    
    if user_lat is None or user_lon is None:
        # If no location available, return venues from user's city
        query = select(Venue).where(Venue.is_active == True)
        if current_user.city:
            query = query.where(Venue.city == current_user.city)
        if sport_type:
            query = query.where(Venue.sports_available.contains([sport_type]))
        query = query.limit(limit)
        
        result = await db.execute(query)
        venues = result.scalars().all()
        return {"venues": venues, "using_location": False}
    
    # Get all active venues with coordinates
    query = select(Venue).where(
        Venue.is_active == True,
        Venue.latitude.isnot(None),
        Venue.longitude.isnot(None)
    )
    
    if sport_type:
        query = query.where(Venue.sports_available.contains([sport_type]))
    
    result = await db.execute(query)
    all_venues = result.scalars().all()
    
    # Calculate distances and filter by radius
    venues_with_distance = []
    for venue in all_venues:
        distance = calculate_distance(user_lat, user_lon, venue.latitude, venue.longitude)
        if distance <= radius_km:
            venue_dict = {
                "id": venue.id,
                "name": venue.name,
                "description": venue.description,
                "venue_type": venue.venue_type,
                "sports_available": venue.sports_available,
                "amenities": venue.amenities,
                "city": venue.city,
                "state": venue.state,
                "address": venue.address,
                "latitude": venue.latitude,
                "longitude": venue.longitude,
                "price_per_hour": venue.price_per_hour,
                "rating": venue.rating,
                "images": venue.images,
                "distance_km": round(distance, 1)
            }
            venues_with_distance.append(venue_dict)
    
    # Sort by distance
    venues_with_distance.sort(key=lambda x: x['distance_km'])
    
    return {
        "venues": venues_with_distance[:limit],
        "using_location": True,
        "user_location": {"latitude": user_lat, "longitude": user_lon},
        "count": len(venues_with_distance)
    }


@router.get("/tournaments")
async def get_nearby_tournaments(
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    radius_km: float = Query(50, description="Search radius in kilometers"),
    sport_type: Optional[str] = None,
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get nearby tournaments based on user location"""
    user_lat = latitude if latitude is not None else current_user.latitude
    user_lon = longitude if longitude is not None else current_user.longitude
    
    if user_lat is None or user_lon is None:
        query = select(Tournament).where(
            Tournament.is_active == True,
            Tournament.status == "upcoming"
        )
        if current_user.city:
            query = query.where(Tournament.city == current_user.city)
        if sport_type:
            query = query.where(Tournament.sport_type == sport_type)
        query = query.limit(limit)
        
        result = await db.execute(query)
        tournaments = result.scalars().all()
        return {"tournaments": tournaments, "using_location": False}
    
    query = select(Tournament).where(
        Tournament.is_active == True,
        Tournament.status == "upcoming",
        Tournament.latitude.isnot(None),
        Tournament.longitude.isnot(None)
    )
    
    if sport_type:
        query = query.where(Tournament.sport_type == sport_type)
    
    result = await db.execute(query)
    all_tournaments = result.scalars().all()
    
    tournaments_with_distance = []
    for tournament in all_tournaments:
        distance = calculate_distance(user_lat, user_lon, tournament.latitude, tournament.longitude)
        if distance <= radius_km:
            tournament_dict = {
                "id": tournament.id,
                "name": tournament.name,
                "description": tournament.description,
                "sport_type": tournament.sport_type,
                "tournament_type": tournament.tournament_type,
                "city": tournament.city,
                "venue_name": tournament.venue_name,
                "start_date": tournament.start_date,
                "registration_deadline": tournament.registration_deadline,
                "entry_fee": tournament.entry_fee,
                "prize_pool": tournament.prize_pool,
                "banner_image": tournament.banner_image,
                "status": tournament.status,
                "distance_km": round(distance, 1)
            }
            tournaments_with_distance.append(tournament_dict)
    
    tournaments_with_distance.sort(key=lambda x: x['distance_km'])
    
    return {
        "tournaments": tournaments_with_distance[:limit],
        "using_location": True,
        "user_location": {"latitude": user_lat, "longitude": user_lon},
        "count": len(tournaments_with_distance)
    }


@router.get("/shops")
async def get_nearby_shops(
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    radius_km: float = Query(50, description="Search radius in kilometers"),
    category: Optional[str] = None,
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get nearby sports shops based on user location"""
    user_lat = latitude if latitude is not None else current_user.latitude
    user_lon = longitude if longitude is not None else current_user.longitude
    
    if user_lat is None or user_lon is None:
        query = select(Shop).where(Shop.is_active == True)
        if current_user.city:
            query = query.where(Shop.city == current_user.city)
        if category:
            query = query.where(Shop.category == category)
        query = query.limit(limit)
        
        result = await db.execute(query)
        shops = result.scalars().all()
        return {"shops": shops, "using_location": False}
    
    query = select(Shop).where(
        Shop.is_active == True,
        Shop.latitude.isnot(None),
        Shop.longitude.isnot(None)
    )
    
    if category:
        query = query.where(Shop.category == category)
    
    result = await db.execute(query)
    all_shops = result.scalars().all()
    
    shops_with_distance = []
    for shop in all_shops:
        distance = calculate_distance(user_lat, user_lon, shop.latitude, shop.longitude)
        if distance <= radius_km:
            shop_dict = {
                "id": shop.id,
                "name": shop.name,
                "description": shop.description,
                "shop_type": shop.shop_type,
                "category": shop.category,
                "city": shop.city,
                "address": shop.address,
                "contact_number": shop.contact_number,
                "rating": shop.rating,
                "logo": shop.logo,
                "images": shop.images,
                "distance_km": round(distance, 1)
            }
            shops_with_distance.append(shop_dict)
    
    shops_with_distance.sort(key=lambda x: x['distance_km'])
    
    return {
        "shops": shops_with_distance[:limit],
        "using_location": True,
        "user_location": {"latitude": user_lat, "longitude": user_lon},
        "count": len(shops_with_distance)
    }


@router.get("/jobs")
async def get_nearby_jobs(
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    radius_km: float = Query(100, description="Search radius in kilometers"),
    job_type: Optional[str] = None,
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get nearby jobs based on user location (for professionals)"""
    user_lat = latitude if latitude is not None else current_user.latitude
    user_lon = longitude if longitude is not None else current_user.longitude
    
    if user_lat is None or user_lon is None:
        query = select(Job).where(Job.status == "active")
        if current_user.city:
            query = query.where(Job.city == current_user.city)
        if job_type:
            query = query.where(Job.job_type == job_type)
        query = query.limit(limit)
        
        result = await db.execute(query)
        jobs = result.scalars().all()
        return {"jobs": jobs, "using_location": False}
    
    query = select(Job).where(Job.status == "active")
    
    if job_type:
        query = query.where(Job.job_type == job_type)
    
    result = await db.execute(query)
    all_jobs = result.scalars().all()
    
    # For jobs, we'll use city-based matching if no lat/lng, or calculate distance if available
    jobs_with_distance = []
    for job in all_jobs:
        if job.latitude and job.longitude:
            distance = calculate_distance(user_lat, user_lon, job.latitude, job.longitude)
        else:
            # Estimate distance based on city match
            distance = 0 if job.city == current_user.city else 999
        
        if distance <= radius_km:
            job_dict = {
                "id": job.id,
                "title": job.title,
                "job_type": job.job_type,
                "description": job.description,
                "sport_type": job.sport_type,
                "employment_type": job.employment_type,
                "city": job.city,
                "salary_min": job.salary_min,
                "salary_max": job.salary_max,
                "salary_type": job.salary_type,
                "application_deadline": job.application_deadline,
                "status": job.status,
                "distance_km": round(distance, 1) if distance < 999 else None
            }
            jobs_with_distance.append(job_dict)
    
    jobs_with_distance.sort(key=lambda x: x['distance_km'] if x['distance_km'] is not None else 999)
    
    return {
        "jobs": jobs_with_distance[:limit],
        "using_location": True,
        "user_location": {"latitude": user_lat, "longitude": user_lon},
        "count": len(jobs_with_distance)
    }


@router.get("/academies")
async def get_nearby_academies(
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    radius_km: float = Query(50, description="Search radius in kilometers"),
    sport: Optional[str] = None,
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get nearby sports academies based on user location"""
    user_lat = latitude if latitude is not None else current_user.latitude
    user_lon = longitude if longitude is not None else current_user.longitude
    
    if user_lat is None or user_lon is None:
        query = select(Dictionary).where(
            Dictionary.is_active == True,
            Dictionary.category == "Academy"
        )
        if current_user.city:
            query = query.where(Dictionary.city == current_user.city)
        if sport:
            query = query.where(Dictionary.sport == sport)
        query = query.limit(limit)
        
        result = await db.execute(query)
        academies = result.scalars().all()
        return {"academies": academies, "using_location": False}
    
    query = select(Dictionary).where(
        Dictionary.is_active == True,
        Dictionary.category == "Academy",
        Dictionary.latitude.isnot(None),
        Dictionary.longitude.isnot(None)
    )
    
    if sport:
        query = query.where(Dictionary.sport == sport)
    
    result = await db.execute(query)
    all_academies = result.scalars().all()
    
    academies_with_distance = []
    for academy in all_academies:
        distance = calculate_distance(user_lat, user_lon, academy.latitude, academy.longitude)
        if distance <= radius_km:
            academy_dict = {
                "id": academy.id,
                "term": academy.term,
                "sport": academy.sport,
                "category": academy.category,
                "definition": academy.definition,
                "city": academy.city,
                "address": academy.address,
                "contact_number": academy.contact_number,
                "images": academy.images,
                "distance_km": round(distance, 1)
            }
            academies_with_distance.append(academy_dict)
    
    academies_with_distance.sort(key=lambda x: x['distance_km'])
    
    return {
        "academies": academies_with_distance[:limit],
        "using_location": True,
        "user_location": {"latitude": user_lat, "longitude": user_lon},
        "count": len(academies_with_distance)
    }


@router.get("/all")
async def get_all_nearby(
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    radius_km: float = Query(50, description="Search radius in kilometers"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get counts of all nearby items"""
    user_lat = latitude if latitude is not None else current_user.latitude
    user_lon = longitude if longitude is not None else current_user.longitude
    
    # Get counts for all categories
    venues_result = await get_nearby_venues(user_lat, user_lon, radius_km, None, 100, db, current_user)
    tournaments_result = await get_nearby_tournaments(user_lat, user_lon, radius_km, None, 100, db, current_user)
    shops_result = await get_nearby_shops(user_lat, user_lon, radius_km, None, 100, db, current_user)
    jobs_result = await get_nearby_jobs(user_lat, user_lon, radius_km, None, 100, db, current_user)
    academies_result = await get_nearby_academies(user_lat, user_lon, radius_km, None, 100, db, current_user)
    
    return {
        "using_location": venues_result.get("using_location", False),
        "user_location": venues_result.get("user_location"),
        "radius_km": radius_km,
        "counts": {
            "venues": venues_result.get("count", len(venues_result.get("venues", []))),
            "tournaments": tournaments_result.get("count", len(tournaments_result.get("tournaments", []))),
            "shops": shops_result.get("count", len(shops_result.get("shops", []))),
            "jobs": jobs_result.get("count", len(jobs_result.get("jobs", []))),
            "academies": academies_result.get("count", len(academies_result.get("academies", [])))
        }
    }

