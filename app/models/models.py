from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from bson import ObjectId

# Helper for MongoDB ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}


# Base model with common fields
class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


# User Model
class User(MongoBaseModel):
    phone: str = Field(..., index=True)
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    
    # Role-based fields
    role: Optional[str] = None  # Player, Parent, Professional
    professional_type: Optional[str] = None  # Umpire, Coach, Trainer, Venue Owner, etc.
    
    # Location
    city: Optional[str] = None
    state: str = "Gujarat"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Profile
    bio: Optional[str] = None
    avatar: Optional[str] = None
    
    # Sports preferences
    sports_interests: Optional[List[str]] = []
    
    # Player-specific fields
    player_position: Optional[str] = None
    playing_style: Optional[str] = None
    
    # Professional-specific fields
    certification: Optional[str] = None
    experience_years: Optional[int] = None
    
    # Parent-specific fields
    children_count: Optional[int] = None
    
    # System fields
    is_active: bool = True
    is_verified: bool = False
    onboarding_completed: bool = False


# Sports Stats Model
class SportsStats(MongoBaseModel):
    user_id: str = Field(..., index=True)
    sport_type: str
    
    # Universal stats
    matches_played: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    
    # Sport-specific stats (flexible JSON)
    detailed_stats: Optional[dict] = {}
    
    # Performance metrics
    rating: float = 0.0
    achievements: Optional[List[dict]] = []


# Venue Model
class Venue(MongoBaseModel):
    owner_id: Optional[str] = None
    
    # Basic Info
    name: str
    description: Optional[str] = None
    venue_type: Optional[str] = None
    
    # Sports & Facilities
    sports_available: Optional[List[str]] = []
    amenities: Optional[List[str]] = []
    
    # Location
    city: str = Field(..., index=True)
    state: str = "Gujarat"
    address: Optional[str] = None
    landmark: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Pricing & Availability
    price_per_hour: float
    weekend_price: Optional[float] = None
    peak_hour_price: Optional[float] = None
    currency: str = "INR"
    
    # Operating Hours
    opening_time: Optional[str] = None
    closing_time: Optional[str] = None
    operating_days: Optional[List[str]] = []
    
    # Venue Details
    capacity: Optional[int] = None
    surface_type: Optional[str] = None
    indoor_outdoor: Optional[str] = None
    images: Optional[List[str]] = []
    
    # Contact & Social
    contact_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    # Ratings & Reviews
    rating: float = 0.0
    total_reviews: int = 0
    
    # Business Metrics
    total_bookings: int = 0
    is_verified: bool = False
    is_featured: bool = False
    
    # Status
    is_active: bool = True


# Booking Model
class Booking(MongoBaseModel):
    booking_number: str = Field(..., index=True)
    
    # Relationships
    user_id: str
    venue_id: str
    
    # Booking Details
    sport_type: Optional[str] = None
    booking_date: str
    start_time: str
    end_time: str
    duration_hours: Optional[float] = None
    
    # Players & Team
    player_count: Optional[int] = None
    team_name: Optional[str] = None
    contact_person: Optional[str] = None
    contact_number: Optional[str] = None
    
    # Pricing
    base_price: float
    additional_charges: Optional[List[dict]] = []
    discount_amount: float = 0.0
    total_amount: float
    
    # Payment
    payment_status: str = "pending"
    payment_method: Optional[str] = None
    paid_amount: float = 0.0
    payment_date: Optional[datetime] = None
    transaction_id: Optional[str] = None
    
    # Split Pay
    is_split_payment: bool = False
    split_payment_data: Optional[List[dict]] = []
    split_payment_link: Optional[str] = None
    
    # Status & Lifecycle
    status: str = "confirmed"
    booking_source: str = "app"
    
    # Notes & Special Requests
    special_requests: Optional[str] = None
    admin_notes: Optional[str] = None
    cancellation_reason: Optional[str] = None
    cancelled_at: Optional[datetime] = None


# Venue Review Model
class VenueReview(MongoBaseModel):
    venue_id: str
    user_id: str
    booking_id: Optional[str] = None
    
    rating: int  # 1-5
    review_text: Optional[str] = None
    images: Optional[List[str]] = []
    
    # Detailed Ratings
    cleanliness_rating: Optional[int] = None
    facilities_rating: Optional[int] = None
    staff_rating: Optional[int] = None
    value_rating: Optional[int] = None
    
    is_verified: bool = False
    helpful_count: int = 0


# Venue Slot Model
class VenueSlot(MongoBaseModel):
    venue_id: str
    
    date: str  # "2025-01-15"
    start_time: str  # "18:00"
    end_time: str  # "19:00"
    
    is_available: bool = True
    booking_id: Optional[str] = None
    
    price: Optional[float] = None
    blocked_reason: Optional[str] = None


# Shop Model
class Shop(MongoBaseModel):
    owner_id: Optional[str] = None
    
    # Basic Info
    name: str
    description: Optional[str] = None
    shop_type: Optional[str] = None
    category: Optional[str] = None
    
    # Products & Services
    products: Optional[List[dict]] = []
    specialization: Optional[List[str]] = []
    brands_available: Optional[List[str]] = []
    
    # Location
    city: str = Field(..., index=True)
    state: str = "Gujarat"
    address: Optional[str] = None
    landmark: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Contact & Business
    contact_number: str
    whatsapp_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    # Business Details
    established_year: Optional[int] = None
    gst_number: Optional[str] = None
    license_number: Optional[str] = None
    
    # Operating Hours
    opening_time: Optional[str] = None
    closing_time: Optional[str] = None
    operating_days: Optional[List[str]] = []
    
    # Media
    logo: Optional[str] = None
    images: Optional[List[str]] = []
    catalogue_pdf: Optional[str] = None
    
    # Ratings & Stats
    rating: float = 0.0
    total_reviews: int = 0
    total_enquiries: int = 0
    
    # Features
    home_delivery: bool = False
    online_payment: bool = False
    bulk_orders: bool = False
    custom_manufacturing: bool = False
    
    # Listing
    is_featured: bool = False
    is_verified: bool = False
    is_active: bool = True


# Job Model
class Job(MongoBaseModel):
    posted_by: str
    
    # Job Details
    title: str
    job_type: str
    description: str
    sport_type: Optional[str] = None
    
    # Employment Type
    employment_type: Optional[str] = None
    experience_required: Optional[str] = None
    certification_required: Optional[List[str]] = []
    
    # Location
    city: str = Field(..., index=True)
    state: str = "Gujarat"
    location_type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Compensation
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_type: Optional[str] = None
    currency: str = "INR"
    other_benefits: Optional[List[str]] = []
    
    # Requirements
    skills_required: Optional[List[str]] = []
    language_required: Optional[List[str]] = []
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    
    # Application
    application_deadline: Optional[datetime] = None
    how_to_apply: Optional[str] = None
    application_email: Optional[str] = None
    application_phone: Optional[str] = None
    application_url: Optional[str] = None
    
    # Stats
    views_count: int = 0
    applications_count: int = 0
    
    # Status
    status: str = "active"
    is_featured: bool = False
    is_verified: bool = False
    expires_at: Optional[datetime] = None


# Dictionary Model (includes Academies)
class Dictionary(MongoBaseModel):
    # Content
    term: str
    sport: str
    category: Optional[str] = None
    
    # Location (for Academies)
    city: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Contact (for Academies)
    contact_number: Optional[str] = None
    contact_email: Optional[str] = None
    
    # Details
    definition: str
    explanation: Optional[str] = None
    examples: Optional[List[str]] = []
    
    # Media
    images: Optional[List[str]] = []
    video_url: Optional[str] = None
    diagram_url: Optional[str] = None
    
    # Related Content
    related_terms: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    
    # Multilingual Support
    gujarati_term: Optional[str] = None
    hindi_term: Optional[str] = None
    
    # Stats
    views_count: int = 0
    helpful_count: int = 0
    
    # SEO & Organization
    slug: Optional[str] = None
    difficulty_level: Optional[str] = None
    
    is_featured: bool = False
    is_active: bool = True


# Tournament Model
class Tournament(MongoBaseModel):
    organizer_id: str
    
    # Basic Info
    name: str
    description: Optional[str] = None
    sport_type: str
    tournament_type: Optional[str] = None
    
    # Format Details
    format: Optional[str] = None
    team_size: Optional[int] = None
    max_teams: int
    min_teams: Optional[int] = None
    current_teams: int = 0
    
    # Categories
    age_category: Optional[str] = None
    gender_category: Optional[str] = None
    skill_level: Optional[str] = None
    
    # Location
    city: str = Field(..., index=True)
    state: str = "Gujarat"
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    venue_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Schedule
    start_date: datetime
    end_date: Optional[datetime] = None
    registration_start: Optional[datetime] = None
    registration_deadline: datetime
    
    # Fees & Prizes
    entry_fee: float = 0
    currency: str = "INR"
    prize_pool: Optional[float] = None
    prize_distribution: Optional[List[dict]] = []
    
    # Registration Requirements
    documents_required: Optional[List[str]] = []
    team_composition_rules: Optional[dict] = {}
    
    # Rules & Regulations
    rules: Optional[str] = None
    match_rules: Optional[dict] = {}
    ball_type: Optional[str] = None
    
    # Media & Branding
    banner_image: Optional[str] = None
    logo: Optional[str] = None
    images: Optional[List[str]] = []
    
    # Contact
    contact_person: Optional[str] = None
    contact_number: Optional[str] = None
    contact_email: Optional[str] = None
    
    # Features
    live_scoring: bool = False
    live_streaming: bool = False
    certificates_provided: bool = False
    
    # Stats
    views_count: int = 0
    
    # Status
    status: str = "upcoming"
    is_featured: bool = False
    is_verified: bool = False
    is_active: bool = True


# Team Model
class Team(MongoBaseModel):
    captain_id: str
    tournament_id: Optional[str] = None
    
    # Team Details
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    sport_type: str
    
    # Location
    city: str
    state: str = "Gujarat"
    home_ground: Optional[str] = None
    
    # Team Info
    logo: Optional[str] = None
    jersey_color: Optional[str] = None
    founded_year: Optional[int] = None
    team_type: Optional[str] = None
    
    # Players
    players: Optional[List[dict]] = []
    total_players: int = 0
    
    # Management
    coach_name: Optional[str] = None
    manager_name: Optional[str] = None
    manager_contact: Optional[str] = None
    
    # Stats
    matches_played: int = 0
    matches_won: int = 0
    matches_lost: int = 0
    matches_drawn: int = 0
    
    # Documents
    documents: Optional[List[dict]] = []
    
    # Status
    is_verified: bool = False
    is_active: bool = True


# Tournament Registration Model
class TournamentRegistration(MongoBaseModel):
    registration_number: str
    
    # Relationships
    tournament_id: str
    team_id: str
    registered_by: str
    
    # Registration Details
    registration_date: datetime = Field(default_factory=datetime.utcnow)
    
    # Team Roster
    team_roster: Optional[List[dict]] = []
    captain_name: Optional[str] = None
    captain_contact: Optional[str] = None
    vice_captain_name: Optional[str] = None
    
    # Payment
    entry_fee: float = 0
    payment_status: str = "pending"
    payment_method: Optional[str] = None
    payment_date: Optional[datetime] = None
    transaction_id: Optional[str] = None
    
    # Documents Submission
    documents_submitted: Optional[List[dict]] = []
    documents_verified: bool = False
    
    # Status
    status: str = "pending"
    approval_date: Optional[datetime] = None
    approved_by: Optional[str] = None
    rejection_reason: Optional[str] = None
    
    # Notes
    special_requests: Optional[str] = None
    admin_notes: Optional[str] = None
