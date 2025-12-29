from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta
import math

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import Venue, Booking, VenueReview, VenueSlot, User
from app.schemas.schemas import (
    VenueCreate, VenueUpdate, VenueResponse,
    BookingCreate, BookingResponse, SplitPaymentRequest,
    ReviewCreate, ReviewResponse
)

router = APIRouter()

@router.get("/venues", response_model=List[VenueResponse])
async def get_venues(
    city: Optional[str] = None,
    sport: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    amenities: Optional[str] = Query(None),  # Comma-separated: "Parking,Cafeteria"
    indoor_outdoor: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_km: Optional[float] = 10.0,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    Smart Search & Filter Venues (B1 & B2)
    - Search by sport, location, price range
    - Filter by amenities, rating, indoor/outdoor
    - Nearby search using lat/long
    """
    query = select(Venue).where(Venue.is_active == True)
    
    # City filter
    if city:
        query = query.where(Venue.city == city)
    
    # Sport filter
    if sport:
        query = query.where(Venue.sports_available.contains([sport]))
    
    # Price range filter
    if min_price:
        query = query.where(Venue.price_per_hour >= min_price)
    if max_price:
        query = query.where(Venue.price_per_hour <= max_price)
    
    # Rating filter
    if min_rating:
        query = query.where(Venue.rating >= min_rating)
    
    # Amenities filter
    if amenities:
        amenity_list = amenities.split(',')
        for amenity in amenity_list:
            query = query.where(Venue.amenities.contains([amenity.strip()]))
    
    # Indoor/Outdoor filter
    if indoor_outdoor:
        query = query.where(Venue.indoor_outdoor == indoor_outdoor)
    
    # Search by name, description, landmark
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Venue.name.ilike(search_term),
                Venue.description.ilike(search_term),
                Venue.landmark.ilike(search_term)
            )
        )
    
    # Nearby search (B3 - Map Integration prep)
    if latitude and longitude:
        # Haversine distance calculation
        # Filter venues within radius
        query = query.where(
            and_(
                Venue.latitude.isnot(None),
                Venue.longitude.isnot(None)
            )
        )
    
    # Pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    venues = result.scalars().all()
    
    # If nearby search, calculate and sort by distance
    if latitude and longitude and venues:
        venues_with_distance = []
        for venue in venues:
            if venue.latitude and venue.longitude:
                # Haversine formula
                lat1, lon1 = math.radians(latitude), math.radians(longitude)
                lat2, lon2 = math.radians(venue.latitude), math.radians(venue.longitude)
                
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                
                a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
                c = 2 * math.asin(math.sqrt(a))
                distance = 6371 * c  # Earth radius in km
                
                if distance <= radius_km:
                    venues_with_distance.append((venue, distance))
        
        # Sort by distance
        venues_with_distance.sort(key=lambda x: x[1])
        venues = [v[0] for v in venues_with_distance]
    
    return venues


@router.get("/venues/{venue_id}", response_model=VenueResponse)
async def get_venue(venue_id: int, db: AsyncSession = Depends(get_db)):
    """Get detailed venue information"""
    result = await db.execute(select(Venue).where(Venue.id == venue_id))
    venue = result.scalar_one_or_none()
    
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    
    return venue


@router.get("/venues/{venue_id}/slots")
async def get_venue_slots(
    venue_id: int,
    date: str,  # Format: "2025-01-15"
    db: AsyncSession = Depends(get_db)
):
    """
    Real-Time Slot Availability (B4)
    Returns available and booked slots for a specific date
    """
    # Get venue
    venue_result = await db.execute(select(Venue).where(Venue.id == venue_id))
    venue = venue_result.scalar_one_or_none()
    
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    
    # Generate time slots based on operating hours
    opening = venue.opening_time  # "06:00"
    closing = venue.closing_time  # "23:00"
    
    # Parse hours
    open_hour = int(opening.split(':')[0])
    close_hour = int(closing.split(':')[0])
    
    # Generate hourly slots
    slots = []
    for hour in range(open_hour, close_hour):
        start_time = f"{hour:02d}:00"
        end_time = f"{hour+1:02d}:00"
        
        # Check if slot is booked
        booking_result = await db.execute(
            select(Booking).where(
                and_(
                    Booking.venue_id == venue_id,
                    Booking.booking_date == date,
                    Booking.start_time == start_time,
                    Booking.status.in_(["confirmed", "pending"])
                )
            )
        )
        booking = booking_result.scalar_one_or_none()
        
        # Determine price (peak hours, weekends)
        slot_price = venue.price_per_hour
        hour_num = hour
        
        # Peak hours (6 PM - 10 PM)
        if 18 <= hour_num < 22 and venue.peak_hour_price:
            slot_price = venue.peak_hour_price
        
        # Weekend pricing
        from datetime import datetime
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        if date_obj.weekday() >= 5 and venue.weekend_price:  # Saturday = 5, Sunday = 6
            slot_price = venue.weekend_price
        
        slots.append({
            "start_time": start_time,
            "end_time": end_time,
            "is_available": booking is None,
            "price": slot_price,
            "booking_id": booking.id if booking else None
        })
    
    return {
        "venue_id": venue_id,
        "date": date,
        "slots": slots
    }


@router.post("/bookings", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new booking (B4)
    """
    # Verify venue exists
    venue_result = await db.execute(
        select(Venue).where(Venue.id == booking_data.venue_id)
    )
    venue = venue_result.scalar_one_or_none()
    
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    
    # Check slot availability
    existing_booking = await db.execute(
        select(Booking).where(
            and_(
                Booking.venue_id == booking_data.venue_id,
                Booking.booking_date == booking_data.booking_date,
                Booking.start_time == booking_data.start_time,
                Booking.status.in_(["confirmed", "pending"])
            )
        )
    )
    
    if existing_booking.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="This slot is already booked"
        )
    
    # Calculate duration and price
    start_hour = int(booking_data.start_time.split(':')[0])
    end_hour = int(booking_data.end_time.split(':')[0])
    duration = end_hour - start_hour
    
    # Dynamic pricing
    base_price = venue.price_per_hour * duration
    
    # Apply peak hour pricing if applicable
    date_obj = datetime.strptime(booking_data.booking_date, "%Y-%m-%d")
    if date_obj.weekday() >= 5 and venue.weekend_price:
        base_price = venue.weekend_price * duration
    
    # Generate booking number
    import random
    booking_number = f"BK-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    
    # Create booking
    new_booking = Booking(
        booking_number=booking_number,
        user_id=current_user.id,
        venue_id=booking_data.venue_id,
        sport_type=booking_data.sport_type,
        booking_date=booking_data.booking_date,
        start_time=booking_data.start_time,
        end_time=booking_data.end_time,
        duration_hours=duration,
        player_count=booking_data.player_count,
        team_name=booking_data.team_name,
        contact_person=booking_data.contact_person,
        contact_number=booking_data.contact_number,
        special_requests=booking_data.special_requests,
        base_price=base_price,
        total_amount=base_price,
        status="confirmed",
        payment_status="pending"
    )
    
    db.add(new_booking)
    
    # Update venue booking count
    venue.total_bookings += 1
    
    await db.flush()
    await db.refresh(new_booking)
    
    return new_booking


@router.post("/bookings/{booking_id}/split-pay")
async def create_split_payment(
    booking_id: int,
    split_data: SplitPaymentRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Split Pay Feature (B5)
    Generate payment links for splitting costs among friends
    """
    # Get booking
    result = await db.execute(
        select(Booking).where(Booking.id == booking_id)
    )
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Calculate split amounts
    total_participants = len(split_data.participants)
    amount_per_person = booking.total_amount / (total_participants + 1)  # +1 for booker
    
    # Generate payment links for each participant
    split_payment_details = []
    for participant in split_data.participants:
        payment_link = f"https://app.sportsdiary.com/pay/{booking.booking_number}/{participant.get('phone', 'unknown')}"
        split_payment_details.append({
            "name": participant.get('name'),
            "phone": participant.get('phone'),
            "amount": participant.get('amount', amount_per_person),
            "payment_link": payment_link,
            "status": "pending"
        })
    
    # Update booking
    booking.is_split_payment = True
    booking.split_payment_data = split_payment_details
    booking.split_payment_link = f"https://app.sportsdiary.com/pay/{booking.booking_number}"
    
    await db.flush()
    await db.refresh(booking)
    
    return {
        "booking_id": booking_id,
        "split_payment_enabled": True,
        "total_amount": booking.total_amount,
        "amount_per_person": amount_per_person,
        "participants": split_payment_details,
        "payment_link": booking.split_payment_link
    }


@router.get("/bookings/my-bookings", response_model=List[BookingResponse])
async def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all bookings for current user"""
    result = await db.execute(
        select(Booking).where(Booking.user_id == current_user.id).order_by(Booking.created_at.desc())
    )
    bookings = result.scalars().all()
    return bookings


@router.post("/venues/{venue_id}/reviews", response_model=ReviewResponse)
async def create_review(
    venue_id: int,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit a venue review"""
    # Check if venue exists
    venue_result = await db.execute(select(Venue).where(Venue.id == venue_id))
    venue = venue_result.scalar_one_or_none()
    
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    
    # Create review
    new_review = VenueReview(
        venue_id=venue_id,
        user_id=current_user.id,
        booking_id=review_data.booking_id,
        rating=review_data.rating,
        review_text=review_data.review_text,
        cleanliness_rating=review_data.cleanliness_rating,
        facilities_rating=review_data.facilities_rating,
        staff_rating=review_data.staff_rating,
        value_rating=review_data.value_rating
    )
    
    db.add(new_review)
    
    # Update venue rating
    review_result = await db.execute(
        select(func.avg(VenueReview.rating), func.count(VenueReview.id))
        .where(VenueReview.venue_id == venue_id)
    )
    avg_rating, review_count = review_result.one()
    
    venue.rating = float(avg_rating) if avg_rating else 0.0
    venue.total_reviews = review_count + 1
    
    await db.flush()
    await db.refresh(new_review)
    
    return new_review


@router.get("/venues/{venue_id}/reviews", response_model=List[ReviewResponse])
async def get_venue_reviews(
    venue_id: int,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """Get all reviews for a venue"""
    result = await db.execute(
        select(VenueReview)
        .where(VenueReview.venue_id == venue_id)
        .order_by(VenueReview.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    reviews = result.scalars().all()
    return reviews

