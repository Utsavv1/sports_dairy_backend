from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# OTP Schemas
class OTPRequest(BaseModel):
    phone: str

class OTPVerify(BaseModel):
    phone: str
    otp: str

# User Schemas
class UserProfileCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    role: Optional[str] = None  # Player, Parent, Professional
    professional_type: Optional[str] = None  # Umpire, Coach, etc.
    city: Optional[str] = None
    state: Optional[str] = "Gujarat"
    bio: Optional[str] = None
    sports_interests: Optional[List[str]] = None
    player_position: Optional[str] = None
    playing_style: Optional[str] = None
    certification: Optional[str] = None
    experience_years: Optional[int] = None
    children_count: Optional[int] = None

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    role: Optional[str] = None
    professional_type: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None
    sports_interests: Optional[List[str]] = None
    player_position: Optional[str] = None
    playing_style: Optional[str] = None
    certification: Optional[str] = None
    experience_years: Optional[int] = None
    children_count: Optional[int] = None
    onboarding_completed: Optional[bool] = None

class LocationUpdate(BaseModel):
    latitude: float
    longitude: float

class UserResponse(BaseModel):
    id: int
    phone: str
    name: Optional[str]
    email: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    role: Optional[str]
    professional_type: Optional[str]
    city: Optional[str]
    state: Optional[str]
    bio: Optional[str]
    avatar: Optional[str]
    sports_interests: Optional[List[str]]
    player_position: Optional[str]
    playing_style: Optional[str]
    certification: Optional[str]
    experience_years: Optional[int]
    children_count: Optional[int]
    is_verified: bool
    onboarding_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Sports Stats Schemas
class SportsStatsCreate(BaseModel):
    sport_type: str
    matches_played: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    detailed_stats: Optional[dict] = None
    rating: Optional[float] = 0.0
    achievements: Optional[List[dict]] = None

class SportsStatsResponse(BaseModel):
    id: int
    user_id: int
    sport_type: str
    matches_played: int
    wins: int
    losses: int
    draws: int
    detailed_stats: Optional[dict]
    rating: float
    achievements: Optional[List[dict]]
    created_at: datetime

    class Config:
        from_attributes = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[dict] = None

# Venue Schemas
class VenueBase(BaseModel):
    name: str
    description: Optional[str] = None
    venue_type: Optional[str] = None
    sports_available: List[str]
    amenities: Optional[List[str]] = None
    city: str
    state: str = "Gujarat"
    address: str
    landmark: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    price_per_hour: float
    weekend_price: Optional[float] = None
    peak_hour_price: Optional[float] = None
    opening_time: str
    closing_time: str
    operating_days: List[str]
    capacity: Optional[int] = None
    surface_type: Optional[str] = None
    indoor_outdoor: Optional[str] = None
    images: Optional[List[str]] = None
    contact_number: str
    email: Optional[EmailStr] = None
    website: Optional[str] = None

class VenueCreate(VenueBase):
    pass

class VenueUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    sports_available: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    price_per_hour: Optional[float] = None
    images: Optional[List[str]] = None
    is_active: Optional[bool] = None

class VenueResponse(VenueBase):
    id: int
    owner_id: Optional[int]
    rating: float
    total_reviews: int
    total_bookings: int
    is_verified: bool
    is_featured: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Booking Schemas
class BookingCreate(BaseModel):
    venue_id: int
    sport_type: str
    booking_date: str
    start_time: str
    end_time: str
    player_count: Optional[int] = None
    team_name: Optional[str] = None
    contact_person: str
    contact_number: str
    special_requests: Optional[str] = None

class SplitPaymentRequest(BaseModel):
    booking_id: int
    participants: List[dict]  # [{"name": "John", "phone": "+91...", "amount": 500}]

class BookingResponse(BaseModel):
    id: int
    booking_number: str
    user_id: int
    venue_id: int
    sport_type: str
    booking_date: str
    start_time: str
    end_time: str
    duration_hours: Optional[float]
    player_count: Optional[int]
    team_name: Optional[str]
    base_price: float
    total_amount: float
    payment_status: str
    status: str
    is_split_payment: bool
    split_payment_data: Optional[List[dict]]
    split_payment_link: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Venue Review Schemas
class ReviewCreate(BaseModel):
    venue_id: int
    booking_id: Optional[int] = None
    rating: int
    review_text: Optional[str] = None
    cleanliness_rating: Optional[int] = None
    facilities_rating: Optional[int] = None
    staff_rating: Optional[int] = None
    value_rating: Optional[int] = None

class ReviewResponse(BaseModel):
    id: int
    venue_id: int
    user_id: int
    rating: int
    review_text: Optional[str]
    helpful_count: int
    created_at: datetime

    class Config:
        from_attributes = True

# Shop Schemas
class ShopBase(BaseModel):
    name: str
    description: Optional[str] = None
    shop_type: Optional[str] = None
    category: Optional[str] = None
    products: Optional[List[dict]] = None
    specialization: Optional[List[str]] = None
    brands_available: Optional[List[str]] = None
    city: str
    state: str = "Gujarat"
    address: str
    landmark: Optional[str] = None
    contact_number: str
    whatsapp_number: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    opening_time: Optional[str] = None
    closing_time: Optional[str] = None
    operating_days: Optional[List[str]] = None
    home_delivery: bool = False
    online_payment: bool = False
    bulk_orders: bool = False
    custom_manufacturing: bool = False

class ShopCreate(ShopBase):
    pass

class ShopUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    products: Optional[List[dict]] = None
    contact_number: Optional[str] = None
    is_active: Optional[bool] = None

class ShopResponse(ShopBase):
    id: int
    owner_id: Optional[int]
    rating: float
    total_reviews: int
    total_enquiries: int
    is_featured: bool
    is_verified: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Job Schemas
class JobBase(BaseModel):
    title: str
    job_type: str
    description: str
    sport_type: Optional[str] = None
    employment_type: str
    experience_required: Optional[str] = None
    certification_required: Optional[List[str]] = None
    city: str
    state: str = "Gujarat"
    location_type: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_type: Optional[str] = None
    currency: Optional[str] = "INR"
    other_benefits: Optional[List[str]] = None
    skills_required: Optional[List[str]] = None
    language_required: Optional[List[str]] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    application_deadline: Optional[datetime] = None
    how_to_apply: Optional[str] = None
    application_email: Optional[str] = None
    application_phone: Optional[str] = None
    application_url: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

class JobResponse(JobBase):
    id: int
    posted_by: int
    views_count: int
    applications_count: int
    status: str
    is_featured: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Dictionary Schemas
class DictionaryBase(BaseModel):
    term: str
    sport: str
    category: Optional[str] = None
    definition: str
    explanation: Optional[str] = None
    examples: Optional[List[str]] = None
    related_terms: Optional[List[int]] = None
    tags: Optional[List[str]] = None
    gujarati_term: Optional[str] = None
    hindi_term: Optional[str] = None
    difficulty_level: Optional[str] = None

class DictionaryCreate(DictionaryBase):
    pass

class DictionaryUpdate(BaseModel):
    definition: Optional[str] = None
    explanation: Optional[str] = None
    examples: Optional[List[str]] = None
    is_active: Optional[bool] = None

class DictionaryResponse(DictionaryBase):
    id: int
    slug: str
    views_count: int
    helpful_count: int
    is_featured: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Tournament Schemas
class TournamentBase(BaseModel):
    name: str
    description: Optional[str] = None
    sport_type: str
    tournament_type: Optional[str] = None
    format: Optional[str] = None
    team_size: Optional[int] = None
    max_teams: int
    min_teams: Optional[int] = None
    age_category: Optional[str] = None
    gender_category: Optional[str] = None
    skill_level: Optional[str] = None
    city: str
    state: str = "Gujarat"
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    registration_start: Optional[datetime] = None
    registration_deadline: datetime
    entry_fee: float = 0
    prize_pool: Optional[float] = None
    prize_distribution: Optional[List[dict]] = None
    documents_required: Optional[List[str]] = None
    rules: Optional[str] = None
    contact_person: Optional[str] = None
    contact_number: Optional[str] = None
    contact_email: Optional[EmailStr] = None

class TournamentCreate(TournamentBase):
    pass

class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    current_teams: Optional[int] = None
    is_active: Optional[bool] = None

class TournamentResponse(TournamentBase):
    id: int
    organizer_id: int
    current_teams: int
    views_count: int
    status: str
    is_featured: bool
    is_verified: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Team Schemas
class TeamBase(BaseModel):
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    sport_type: str
    city: str
    state: str = "Gujarat"
    home_ground: Optional[str] = None
    team_type: Optional[str] = None
    players: Optional[List[dict]] = None
    coach_name: Optional[str] = None
    manager_name: Optional[str] = None
    manager_contact: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    players: Optional[List[dict]] = None
    is_active: Optional[bool] = None

class TeamResponse(TeamBase):
    id: int
    captain_id: int
    tournament_id: Optional[int]
    total_players: int
    matches_played: int
    matches_won: int
    matches_lost: int
    matches_drawn: int
    is_verified: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Organizer Team/Manager Schemas
class OrganizerManagerCreate(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    role_description: Optional[str] = None  # e.g., "Assistant Manager", "Tournament Coordinator"
    permissions: Optional[List[str]] = None  # ["create_tournament", "edit_tournament", "manage_registrations"]
    # Full profile fields (organizer creates complete profile)
    age: Optional[int] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = "Gujarat"
    bio: Optional[str] = None
    sports_interests: Optional[List[str]] = None

class OrganizerManagerAddExisting(BaseModel):
    user_id: str  # ID of existing user to add as manager
    role_description: Optional[str] = None
    permissions: List[str] = ["create_tournament", "edit_tournament", "view_registrations"]

class OrganizerManagerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role_description: Optional[str] = None
    permissions: Optional[List[str]] = None
    is_active: Optional[bool] = None

class OrganizerManagerResponse(BaseModel):
    id: str
    organizer_id: str
    manager_user_id: Optional[str]  # If manager has created an account
    name: str
    phone: str
    email: Optional[str]
    role_description: Optional[str]
    permissions: List[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_active: Optional[datetime] = None

    class Config:
        from_attributes = True

# Tournament Registration Schemas
class TournamentRegistrationCreate(BaseModel):
    tournament_id: int
    team_id: int
    team_roster: List[dict]
    captain_name: str
    captain_contact: str
    vice_captain_name: Optional[str] = None
    special_requests: Optional[str] = None

class TournamentRegistrationUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None
    documents_verified: Optional[bool] = None
    rejection_reason: Optional[str] = None

class TournamentRegistrationResponse(BaseModel):
    id: int
    registration_number: str
    tournament_id: int
    team_id: int
    registered_by: int
    captain_name: str
    captain_contact: str
    entry_fee: float
    payment_status: str
    status: str
    documents_verified: bool
    registration_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# Professional Availability Schemas
class ProfessionalAvailabilityCreate(BaseModel):
    sport_type: str
    available_from_date: datetime
    available_to_date: Optional[datetime] = None
    available_days: Optional[List[str]] = None  # ["Monday", "Tuesday", etc.]
    available_time_slots: Optional[List[dict]] = None  # [{"start": "18:00", "end": "22:00"}]
    per_match_fee: float
    match_types: Optional[List[str]] = None
    can_play: bool = True
    can_coach: bool = False
    can_umpire: bool = False
    min_notice_hours: int = 24
    max_bookings_per_week: Optional[int] = None

class ProfessionalAvailabilityUpdate(BaseModel):
    available_from_date: Optional[datetime] = None
    available_to_date: Optional[datetime] = None
    available_days: Optional[List[str]] = None
    available_time_slots: Optional[List[dict]] = None
    per_match_fee: Optional[float] = None
    match_types: Optional[List[str]] = None
    can_play: Optional[bool] = None
    can_coach: Optional[bool] = None
    can_umpire: Optional[bool] = None
    min_notice_hours: Optional[int] = None
    max_bookings_per_week: Optional[int] = None
    is_active: Optional[bool] = None

class ProfessionalAvailabilityResponse(BaseModel):
    id: str
    professional_id: str
    professional_name: str
    professional_type: str
    sport_type: str
    city: str
    state: str
    available_from_date: datetime
    available_to_date: Optional[datetime]
    available_days: Optional[List[str]]
    available_time_slots: Optional[List[dict]]
    per_match_fee: float
    currency: str
    match_types: Optional[List[str]]
    can_play: bool
    can_coach: bool
    can_umpire: bool
    min_notice_hours: int
    max_bookings_per_week: Optional[int]
    rating: float
    total_bookings: int
    total_reviews: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Professional Booking Schemas
class ProfessionalBookingCreate(BaseModel):
    professional_id: str
    tournament_id: Optional[str] = None
    match_id: Optional[str] = None
    match_date: datetime
    match_start_time: str
    match_end_time: str
    sport_type: str
    match_type: str
    location: str
    venue_address: Optional[str] = None
    role: str  # Player, Coach, Umpire, Trainer
    special_requests: Optional[str] = None
    contact_number: Optional[str] = None
    contact_email: Optional[str] = None

class ProfessionalBookingUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None
    cancellation_reason: Optional[str] = None

class ProfessionalBookingResponse(BaseModel):
    id: str
    booking_number: str
    professional_id: str
    booked_by: str
    tournament_id: Optional[str]
    match_id: Optional[str]
    booking_date: datetime
    match_date: datetime
    match_start_time: str
    match_end_time: str
    sport_type: str
    match_type: str
    location: str
    role: str
    per_match_fee: float
    total_amount: float
    currency: str
    payment_status: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
